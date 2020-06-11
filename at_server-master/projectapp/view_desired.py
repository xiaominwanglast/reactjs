import requests,re,datetime,json
from rest_framework import generics, mixins
from projectapp.base.utils import try_except
from projectapp.serializers import *
from projectapp.base.zentao import *
from userapp.models import Users
from projectapp.base.utils import *
from django.db.models import Q

zentaoStatus = {
    'opened':'已创建',
    'activated':'已激活',
    'closed':'已关闭',
    'changed':'已变更',
    'deleted':'已删除',
    'reviewed':'已审核',
    'edited':'已编辑'
}


class SyncDesiredNew(generics.GenericAPIView):
    """
       禅道需求/计划推送
    """
    serializer_class = SyncDesiredSerializerParam

    @retResponse()
    def post(self,request):
        data = request.data
        print(data)
        status = self.getZentaoInfo(data['objectID'])['story']['status']
        if status != 'draft':
            zentao_id, type = data['objectID'], data['objectType']
            obj = StoryPlan.objects.filter(zentao_id = zentao_id, type = type)
            if obj:
                obj = obj[0]
                if data['action'] in ['reviewed','closed','activated','deleted']:
                    obj.zentao_status = zentaoStatus[data['action']]
                obj.extra = data['extra']
                if data['action'] in ['changed']:
                    obj.update_num = obj.update_num + 1
                obj.title = re.search('.*::(.*)]', data['text']).group(1)

                if data['action'] == 'linked2plan':
                    obj.plan_id = data['extra']
                elif data['action'] == 'unlinkedfromplan':
                    obj.plan_id = '0'
                elif data['action'] in ['reviewed','activated']:
                    obj.zentao_create_time = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
                elif data['action'] == 'deleted':
                    obj.delete = '0'
            else:
                obj = StoryPlan()
                user = Users.objects.filter(username=data['actor']).values('realname')
                if user:
                    obj.product_master = user[0]['realname']
                else:
                    obj.product_master = data['actor']
                obj.zentao_id = data['objectID']
                obj.zentao_url = host + '/story-view-{}.html'.format(data['objectID'])
                obj.type = data['objectType']
                obj.status = '未安排'
                obj.product_id = data['product'][1:-1]
                obj.zentao_status = zentaoStatus[data['action']]
                obj.extra = data['extra']
                obj.zentao_create_time = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
                obj.title = re.search('.*::(.*)]', data['text']).group(1)
            #添加项目名称
            temp = Project.objects.filter(project_id__contains=f'"{obj.product_id}"')
            obj.product_name = temp[0].project_name if temp else '后台系统'
            obj.version_master = temp[0].project_master if temp else '王浩'
            #添加对应的计划id
            # planid = self.getPlanId(data['objectID'])
            # obj.plan_id = planid if planid and obj.type!='productplan' else 0
            obj.save()
            return True,'需求同步成功'
        else:
            return True,'草稿无需处理'

    def getPlanId(self, id):
        cookie = Zentao.login('admin')
        tt = Zentao.get_story(cookie, id)
        return json.loads(tt['data'])['story']['plan']

    def getZentaoInfo(self, id):
        cookie = Zentao.login('admin')
        tt = Zentao.get_story(cookie, id)
        print(tt['data'])
        return json.loads(tt['data'])

class SyncDesired(generics.GenericAPIView):
    """
       禅道需求/计划推送
    """
    serializer_class = SyncDesiredSerializerParam

    @retResponse()
    def post(self,request):
        data = request.data
        print(data)
        #只处理story事件
        if data['objectType'] != 'story':
            return True, '无需处理'

        status = self.getZentaoInfo(data['objectID'])['story']['status']
        #过滤草稿需求
        if status == 'draft':
            return True, '无需处理'

        zentao_id, type = data['objectID'], data['objectType']
        #查找操作的对象
        obj, create = StoryPlan.objects.get_or_create(zentao_id = zentao_id, type = type)
        if create:
            user = Users.objects.filter(username=data['actor']).values('realname')
            obj.product_master = user[0]['realname'] if user else data['actor']
            obj.zentao_id = data['objectID']
            obj.zentao_url = host + '/story-view-{}.html'.format(data['objectID'])
            obj.type = data['objectType']
            obj.product_id = data['product'][1:-1]
        if  data['action'] == 'opened' or (data['action'] == 'reviewed' and data['extra'] == 'Pass'):
            obj.status = '未安排'
            obj.zentao_create_time = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        elif data['action'] == 'activated':
            obj.zentao_create_time = datetime.datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
            obj.delete = '1'
        elif data['action'] == 'closed':
            if data['extra'] == 'Done':
                obj.status = '已上线'
                obj.version_id = obj.version_id if obj.version_id else -1
            if data['extra'] == 'Cancel':
                obj.status = '已取消'
                obj.delete = '0'
        elif data['action'] == 'deleted':
            obj.delete = '0'
        elif data['action'] == 'changed':
            obj.update_num = obj.update_num + 1
        obj.zentao_status = zentaoStatus[data['action']]
        obj.extra = data['extra']
        obj.title = re.search('.*::(.*)]', data['text']).group(1)

        #添加项目名称
        temp = Project.objects.filter(project_id__contains=f'"{obj.product_id}"')
        obj.product_name = temp[0].project_name if temp else '后台系统'
        obj.version_master = temp[0].project_master if temp else '王浩'
        #添加对应的计划id
        # planid = self.getPlanId(data['objectID'])
        # obj.plan_id = planid if planid and obj.type!='productplan' else 0
        obj.save()
        return True,'需求同步成功'


    def getPlanId(self, id):
        cookie = Zentao.login('admin')
        tt = Zentao.get_story(cookie, id)
        return json.loads(tt['data'])['story']['plan']

    def getZentaoInfo(self, id):
        cookie = Zentao.login('admin')
        tt = Zentao.get_story(cookie, id)
        print(tt['data'])
        return json.loads(tt['data'])

class GetStory(generics.GenericAPIView, mixins.ListModelMixin):
    """
          获取需求/计划
       """

    serializer_class = GetStorySerializerParam

    # @try_except()
    def get(self,request):
        return self.list(request)

    def get_queryset(self):
        print(111111,self.request.query_params)
        serializer = GetStoryParamsSerializerParam(data=self.request.query_params)
        if serializer.is_valid():
            product_name = serializer.initial_data.get('product_name')
            version_id = serializer.initial_data.get('version_id')
            # if 'zentao_create_time' in serializer.initial_data:
            zentao_create_time = json.loads(serializer.initial_data.get('zentao_create_time','["",""]'))
            print(zentao_create_time)
            # if 'online_time' in serializer.initial_data:
            online_time = json.loads(serializer.initial_data.get('online_time','["",""]'))
            is_version = serializer.initial_data.get('is_version', '')
            print(1111, product_name, version_id)
            # 获取未完成的需求
            data = {
                'type__in':['story', 'productplan'],
                'delete':'1'
            }
            if version_id:
                data['version_id'] = version_id

            if zentao_create_time[0]:
                data['zentao_create_time__gte'] = zentao_create_time[0] + ' 00:00:00'
                data['zentao_create_time__lte'] = zentao_create_time[1] + ' 23:59:59'

            # if online_time[0]:
            #     start_time = online_time[0]
            #     end_time = online_time[1]
            #     print(online_time)
            #     temp = StoryPlan.objects.filter(**data).filter(status='未安排').filter((Q(online_time__gte = start_time)&Q(online_time__lte = end_time)) | Q(plan_online_time__gte = start_time)&Q(plan_online_time__lte = end_time)&Q(online_time=None)).order_by('-zentao_create_time')[:999999]
            #     temp1 = StoryPlan.objects.filter(**data).filter(status='进行中').filter((Q(online_time__gte = start_time)&Q(online_time__lte = end_time)) | Q(plan_online_time__gte = start_time)&Q(plan_online_time__lte = end_time)&Q(online_time=None)).order_by('-zentao_create_time')[:999999]
            #     temp2 = StoryPlan.objects.filter(**data).filter(status='已上线').filter((Q(online_time__gte = start_time)&Q(online_time__lte = end_time)) | Q(plan_online_time__gte = start_time)&Q(plan_online_time__lte = end_time)&Q(online_time=None)).order_by('-zentao_create_time')[:999999]
            # else:
            #     temp = StoryPlan.objects.filter(**data).filter(status='未安排').order_by('-zentao_create_time')[:999999]
            #     temp1 = StoryPlan.objects.filter(**data).filter(status='进行中').order_by('-zentao_create_time')[:999999]
            #     temp2 = StoryPlan.objects.filter(**data).filter(status='已上线').order_by('-zentao_create_time')[:999999]

            sql_bef = 'StoryPlan.objects.filter(**'
            sql_aft = ".order_by('-zentao_create_time')[:999999]"
            query_time = '.filter((Q(online_time__gte = start_time)&Q(online_time__lte = end_time)) | Q(plan_online_time__gte = start_time)&Q(plan_online_time__lte = end_time)&Q(online_time=None))'

            if online_time[0]:
                start_time = online_time[0]
                end_time = online_time[1]
                print(online_time)
            else:
                query_time = ''

            if is_version:
                print(222,data)
                datacp = data.copy()
                datacp['product_name'] = product_name
                sql = sql_bef + 'datacp)' + ".filter(status='未安排')" + query_time + sql_aft
                print(333,data)
                sql1 = sql_bef + 'data)' + ".filter(status='未安排')" + ".exclude(product_name=product_name)" + query_time + ".order_by('product_name')[:999999]"
                temp = eval(sql)
                temp1 = eval(sql1)
                return temp.union(temp1)
            else:
                if product_name:
                    data['product_name'] = product_name
                sql = sql_bef + 'data)' + ".filter(status='未安排')" + query_time + sql_aft
                sql1 = sql_bef + 'data)' + ".filter(status='进行中')" + query_time + sql_aft
                sql2 = sql_bef + 'data)' + ".filter(status='已上线')" + query_time + sql_aft
                temp = eval(sql)
                temp1 = eval(sql1)
                temp2 = eval(sql2)

        return temp.union(temp1,temp2)

class GetPlanStory(generics.GenericAPIView):
    """
          获取计划包含的需求
       """
    serializer_class = GetStorySerializerParam

    @retResponse()
    def get(self, request, id):
            temp = StoryPlan.objects.filter(plan_id=id).exclude(zentao_status__in=['已删除', '已关闭']).order_by('-id')
            return True,temp.values()

class EditStory(generics.GenericAPIView):
    """
          修改需求/计划
       """
    serializer_class = EditStorySerializerParam

    @retResponse()
    def put(self, request, id):
            # story_id = request.data.get('story_id')
            obj = StoryPlan.objects.get(id=id)
            print(request.data)
            serializer = EditStorySerializerParam(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return True,'修改成功'


