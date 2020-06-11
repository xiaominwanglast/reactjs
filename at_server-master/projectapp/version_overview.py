from rest_framework import generics, mixins
from rest_framework.response import Response
import datetime, json
from projectapp.serializers import *
from projectapp.base.utils import *


class GetVersion(generics.GenericAPIView):
    serializer_class = PutVersionSerializerParam

    @retResponse()
    def get(self, request, id):  # 获取版本
        version = Version.objects.get(id=id)
        serializers = GetVersionSerializerParam(version)
        temp = serializers.data
        story_list = StoryPlan.objects.filter(version_id=id)
        serializers2 = GetVersionStorySerializerParam(story_list, many=True)
        temp['story_list'] = serializers2.data
        return True, temp

    @retResponse()
    def put(self, request, id):
        # 更新版本表
        obj = Version.objects.get(id=id)
        serializer = PutVersionSerializerParam(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()

        #更新计划上线时间
        print(request.data)
        plan_online_time = request.data['online_plan_time']
        story_list = request.data['story_list']
        for story in story_list:
            StoryPlan.objects.filter(id=story['id']).update(plan_online_time=plan_online_time, version_master=json.loads(story['join_users'])[0])

        # 解除需求关联关系
        StoryPlan.objects.filter(version_id=id).update(version_id=0, join_users='')

        # 重新绑定需求关联关系
        story_list = request.data['story_list']
        print(story_list)
        for story in story_list:
            tmp = StoryPlan.objects.get(id=story['id'])
            story['status'] = '进行中'  # 关联需求，即把需求状态更新成‘进行中’
            serializer3 = PutVersionStorySerializerParam(tmp, data=story)
            if serializer3.is_valid():
                serializer3.save()

        # 插入变更
        data = request.data
        data['change_content'] = request.data['change_content']
        data['create_user'] = request.session['user']['realname']
        data['version_id'] = id
        create = CreateVersionHistorySerializerParam(data=data)
        if create.is_valid():
            create.save()
        return True, '修改成功'


class UpdateVersionStage(generics.GenericAPIView):
    serializer_class = UpdateVersionStatusSerializerParam

    @retResponse()
    def put(self, request, id):
        data = int(request.data['stage'])
        print('cur---',data)
        # 更新版本表
        obj = Version.objects.get(id=id)
        current_date = datetime.date.today()
        if data == 3:  # 排期完成，进入设计中
            request.data['story_plan_done_time'] = current_date
        elif data == 4:  # 设计完成，进入开发中
            request.data['design_done_time'] = current_date
        elif data == 5:  # 开发完成，进入测试中
            request.data['dev_done_time'] = current_date
        elif data == 6:  # 测试完成，进入上线中
            request.data['test_done_time'] = current_date
        elif data == 7:  # 上线完成
            request.data['online_done_time'] = current_date
            story_list = StoryPlan.objects.filter(version_id=id)
            today_date = datetime.datetime.today().date()
            for story in story_list:
                duration_days = int((datetime.datetime.today() - story.create_time).days) + 1
                StoryPlan.objects.filter(id=story.id).update(status='已上线', duration_days=duration_days, online_time=today_date)

        serializer = UpdateVersionStatusSerializerParam(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return True, '修改成功'


# 创建版本
class Versions(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = GetVersionSerializerParam

    def get(self, request):
        """获取所有版本"""
        return self.list(request)

    def get_queryset(self):
        data = self.request.query_params
        print(data)
        filter_dict = dict()
        product_title, version_title, stage, status, id = data.get("product_title"), data.get('title'), data.get(
            'stage'), data.get('status'), data.get('id')
        if product_title:
            filter_dict["product_title"] = product_title
        if version_title:
            filter_dict["title__contains"] = version_title
        if stage:
            filter_dict["stage"] = stage
        if status:
            filter_dict["status"] = status
        if id:
            filter_dict["id"] = id

        doing_version = Version.objects.filter(delete=1).exclude(stage=7).filter(**filter_dict).order_by('-id')[
                        :9999999]
        finish_version = Version.objects.filter(delete=1).filter(stage=7).filter(**filter_dict).order_by('-id')[
                         :9999999]

        all_version = doing_version.union(finish_version)
        return all_version

    @retResponse()
    def post(self, request):
        data = request.data
        data['create_user'] = request.session['user']['realname']
        data['master_name'] = json.dumps([request.session['user']['realname']], ensure_ascii=False)
        create = CreateVersionSerializerParam(data=data)
        if create.is_valid():
            create.save()

        return True, '创建成功'


# 获取版本变更历史
class GetVersionChangeHistory(generics.GenericAPIView):
    @retResponse()
    def get(self, request, id):
        temp = VersionChangeHistory.objects.filter(version_id=id).order_by('-id')
        serializer = GetVersionHistorySerializerParam(temp, many=True)
        print(temp)
        return True, serializer.data
