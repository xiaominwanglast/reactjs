from flowapp.views_testtask import *
from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.response import Response
from flowapp.models import *
from flowapp.serializers import *
from wxwork.message import MessageObject
import json, datetime
from projectapp.version_overview import UpdateVersionStage


class OnlineOrderFlowObject(generics.GenericAPIView):
    """
    上线流程的新增 (不对外)
    """

    # 配合文档，显示请求参数
    serializer_class = OnlineOrderSerializerParam

    def get_flow_object(self, **kwargs):
        if kwargs:
            try:
                return OnlineOrderFlow.objects.get(**kwargs)
            except OnlineOrderFlow.DoesNotExist:
                raise Http404

    def get_onlineorder_object(self, **kwargs):
        if kwargs:
            try:
                return OnlineOrder.objects.get(**kwargs)
            except OnlineOrder.DoesNotExist:
                raise Http404

    def actions(self, myonlineorderflow, change_fields, new_content):

        chinese_dict = {
            "checkpoint": "修改检查项为" + new_content[
                change_fields.index('checkpoint')] if 'checkpoint' in change_fields else '',
            "master": "修改负责人为 " + new_content[change_fields.index('master')] if 'master' in change_fields else '',
            "note": "修改备注内容",
            "status": f"修改状态为【{new_content[change_fields.index('status')] if 'status' in change_fields else ''}】",
        }

        actions = []
        for change_field in change_fields:
            try:
                actions.append(chinese_dict[change_field])
            except:
                pass

        return f"将【{myonlineorderflow.checkpoint}】{', '.join(actions)}"

    def post(self, request, onlineorder_id):
        """
        上线流程的新增
        """
        print(request.data.get('onlineorderflow'))
        # 1. 记录上线流程
        request.data['dev_users'] = []
        for data in json.loads(request.data.get('onlineorderflow')):

            # 保存每一条上线流程数据
            data['onlineorder_id'] = onlineorder_id
            if data.get('status'): data['check_time'] = datetime.datetime.now()
            serializer_flow = OnlineOrderFlowSerializer(data=data)
            if not serializer_flow.is_valid():
                return request
            serializer_flow.save()

            # 对负责人的处理
            if data.get('checkpoint') == '是否测试通过准许上线' and data.get('master') != None:
                request.data['test_users'] = json.dumps([data.get('master')], ensure_ascii=False)
            if data.get('checkpoint') == '生产环境产品人员验收' and data.get('master') != None:
                request.data['product_users'] = json.dumps([data.get('master')], ensure_ascii=False)
            if data.get('checkpoint') == '上线Checklist检查' and data.get('master') != None:
                request.data['dev_users'] += [data.get('master')]

        request.data['dev_users'] = json.dumps(request.data['dev_users'], ensure_ascii=False)

        return request

    def put(self, request, onlineorder_id):
        """
        上线流程的修改
        """
        print(request.data.get('onlineorderflow'))

        myonlineorder = self.get_onlineorder_object(id=onlineorder_id, delete=1)
        # 1. 记录上线流程

        for data in json.loads(request.data.get('onlineorderflow')):
            myonlineorderflow = self.get_flow_object(id=data['id'], delete=1)

            change_data = {}
            for key in list(data.keys()):
                if data[key] != myonlineorderflow.__getattribute__(key) and key not in ['create_time', 'update_time']:
                    change_data[key] = data[key]

            # 更新check_time
            if data.get('status') and myonlineorderflow.status != data.get('status'):
                data['check_time'] = datetime.datetime.now()

            # 保存数据
            serializer_flow = OnlineOrderFlowSerializer(myonlineorderflow, data=data)
            if not serializer_flow.is_valid():
                return request
            serializer_flow.save()

            # 插入操作记录
            old_content = [myonlineorderflow.__getattribute__(filed) for filed in change_data.keys()]
            if len(change_data.keys()) > 0:
                OnlineOrderOperation.objects.create(
                    onlineorder_id=myonlineorder.id,
                    username=request.session['user'].get('username'),
                    realname=request.session['user'].get('realname'),
                    change_fields=list(change_data.keys()),
                    old_content=old_content,
                    new_content=list(change_data.values()),
                    change_action=self.actions(myonlineorderflow, list(change_data.keys()), list(change_data.values()))
                )

        request.data['dev_users'] = []
        request.data['status'] = None
        checklist_sql_count = 0
        for flow in OnlineOrderFlow.objects.filter(onlineorder_id=onlineorder_id, delete=1).order_by('id'):

            # 对上线单的上线时间处理
            if flow.checkpoint == '确认上线' and flow.status == '通过' and myonlineorder.real_online_time == None:
                request.data['real_online_time'] = datetime.datetime.now()

            # 对上线单的负责人的更新处理
            if flow.checkpoint == '是否测试通过准许上线' and flow.master:
                request.data['test_users'] = json.dumps([flow.master], ensure_ascii=False)
            if flow.checkpoint == '生产环境产品人员验收' and flow.master:
                request.data['product_users'] = json.dumps([flow.master], ensure_ascii=False)
            if flow.checkpoint == '上线Checklist检查' and flow.master:
                request.data['dev_users'] += [flow.master]

            # 对上线状态的处理
            if flow.checkpoint == '上线发布内容确认' and flow.status == '通过':
                request.data['status'] = '上线确认'
            if flow.checkpoint == '上线包名及GIT确认' and flow.status == '通过':
                checklist_sql_count += 1
                if int(myonlineorder.template) == int(checklist_sql_count):
                    request.data['status'] = '预发布完成'
                else:
                    request.data['status'] = f'预发布中 ({checklist_sql_count}/{myonlineorder.template})'
            if flow.checkpoint == 'Pre环境功能验证' and flow.status == '通过':
                request.data['status'] = '预发验证完'
            if flow.checkpoint == '确认上线' and flow.status == '通过':
                request.data['status'] = '上线完成'
            if flow.checkpoint == '生产环境产品人员验收' and flow.status == '通过':
                request.data['status'] = '验收完成'

        request.data['dev_users'] = json.dumps(request.data['dev_users'], ensure_ascii=False)

        return request


class OnlineOrderObject(generics.GenericAPIView):
    """
    上线单新增
    """

    # 配合文档，显示请求参数
    serializer_class = OnlineOrderSerializerParam

    def post(self, request):
        """
        上线单新增
        """

        print(request.data)

        # 1. 检查传入的参数，并保存
        request.data['status'] = '发起上线'
        serializer = OnlineOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 2. 记录操作记录
        OnlineOrderOperation.objects.create(
            onlineorder_id=serializer.data.get('id'),
            username=request.session['user'].get('username'),
            realname=request.session['user'].get('realname'),
            change_action='发起上线流程'
        )

        # 3. 记录上线流程
        request = OnlineOrderFlowObject().post(request, serializer.data.get('id'))

        # 4.更新负责人
        myOnlineOrder = OnlineOrder.objects.get(id=serializer.data.get('id'))
        serializer = OnlineOrderSerializer(myOnlineOrder, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 5.发现企业消息 ，发给相关人员+部门领导
        print('发给相关人员+流程负责人+部门领导')
        user_list = json.loads(serializer.data.get("users"))
        user_list += json.loads(serializer.data.get("dev_users"))
        user_list += json.loads(serializer.data.get("test_users"))
        user_list += json.loads(serializer.data.get("product_users"))
        MessageObject.send(title='TMS 上线提醒', user_list=user_list,
                           msg=f"【{serializer.data.get('status')}】【{serializer.data.get('system')}】{serializer.data.get('title')}",
                           forward=f"/flow/online/detail/{serializer.data.get('id')}", send_mode=['users', 'leaders'])

        # 异步数据库变更通知大数据
        for testtask_id in json.loads(myOnlineOrder.testtask):
            myTestTask = TestTask.objects.get(id=testtask_id)
            if int(myTestTask.version) <= 1:
                continue
            # db_change_order_ids = json.loads(myTestTask.sql_files)
            # threading.Thread(target=views_dbchange.DBChangeOrderAuditRecordObject().notice_bigdata,
            #                  args=(db_change_order_ids, '上线阶段',)).start()

            for version_id in json.loads(myTestTask.version_id):
                request.data.clear()
                request.data['id'] = version_id
                request.data['stage'] = '6'
                request.data['status'] = '进行中'
                UpdateVersionStage().put(request, version_id)

        return Response({"status": True, "message": "成功", "data": serializer.data})


class OnlineOrderQuery(generics.GenericAPIView, mixins.ListModelMixin):
    """
    条件查询上线单,什么参数都不传，返回所有
    """

    # 配合文档，显示请求参数
    serializer_class = OnlineOrderListSerializer

    def get_queryset(self):
        if 'real_online_time' in self.request.data:
            self.request.data['real_online_time__gte'] = self.request.data['real_online_time'][0] + ' 00:00:00'
            self.request.data['real_online_time__lte'] = self.request.data['real_online_time'][1] + ' 23:59:59'
            del self.request.data['real_online_time']

        if self.request.data.get('type') == 'Q':
            del self.request.data['type']
            Qfilter = []
            for k, v in self.request.data.items():
                Qfilter.append(f"Q({k}=\'{v}\')")
            Qfilter = "|".join(Qfilter)

            now_order = OnlineOrder.objects.filter(delete=1).filter(eval(Qfilter)).exclude(
                status__in=('上线完成', '验收完成')).order_by('-id')[:9999999]
            finish_order = OnlineOrder.objects.filter(delete=1).filter(eval(Qfilter)).filter(
                status='上线完成').order_by('-id')[:9999999]
            end_order = OnlineOrder.objects.filter(delete=1).filter(eval(Qfilter)).filter(
                status='验收完成').order_by('-id')[:9999999]
            all_order = now_order.union(finish_order, end_order)

        else:
            now_order = OnlineOrder.objects.filter(delete=1).filter(**self.request.data).exclude(
                status__in=('上线完成', '验收完成')).order_by('-id')[:9999999]
            finish_order = OnlineOrder.objects.filter(delete=1).filter(**self.request.data).filter(
                status='上线完成').order_by('-id')[:9999999]
            end_order = OnlineOrder.objects.filter(delete=1).filter(**self.request.data).filter(
                status='验收完成').order_by('-id')[:9999999]
            all_order = now_order.union(finish_order, end_order)

        return all_order

    def post(self, request):
        """
        条件查询提测单,什么参数都不传，返回所有
        """
        return self.list(request)


class OnlineOrderDetail(generics.GenericAPIView):
    """
    查询、修改、删除上线单
    """

    # permission_classes = (IsOwnerOrReadOnly,)
    # 配合文档，显示请求参数
    serializer_class = OnlineOrderSerializerParam

    def actions(self, change_fields, new_content):
        chinese_dict = {
            "title": "修改标题",
            "type": "修改类型为 " + new_content[change_fields.index('type')] if 'type' in change_fields else '',
            "system": "修改所属系统为 " + new_content[change_fields.index('system')] if 'system' in change_fields else '',
            "content": "修改上线内容",
            "template": "修改上线模板为 " + new_content[
                change_fields.index('template')] if 'template' in change_fields else '',
            "status": f"修改状态为【{new_content[change_fields.index('status')] if 'status' in change_fields else ''}】",
            "dev_team": "修改开发团队为" + new_content[change_fields.index('dev_team')] if 'dev_team' in change_fields else '',
            "real_online_time": "设置上线时间为 " + new_content[
                change_fields.index('real_online_time')].strftime(
                "%Y-%m-%d %H:%M:%S") if 'real_online_time' in change_fields else '',
            "testtask": "修改关联提测单为 " + new_content[
                change_fields.index('testtask')] if 'testtask' in change_fields else '',
            "users": "修改相关人员为 " + new_content[change_fields.index('users')] if 'users' in change_fields else '',
        }

        actions = []
        for change_field in change_fields:
            try:
                actions.append(chinese_dict[change_field])
            except:
                pass

        return " , ".join(actions)

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return OnlineOrder.objects.get(**kwargs)
            except OnlineOrder.DoesNotExist:
                raise Http404

    def get_flow_object(self, **kwargs):
        if kwargs:
            try:
                return OnlineOrderFlow.objects.get(**kwargs)
            except OnlineOrderFlow.DoesNotExist:
                raise Http404

    def get(self, request, id):
        """
        查询一个上线单的详情
        """
        myonlineorder = self.get_object(id=id, delete=1)
        serializer = OnlineOrderSerializer(myonlineorder)

        myonlineorderflow = OnlineOrderFlow.objects.filter(onlineorder_id=id).order_by('id')
        serializer_flow = OnlineOrderFlowSerializer(myonlineorderflow, many=True)

        data = serializer.data
        data['onlineorderflow'] = serializer_flow.data

        return Response({"status": True, "message": "成功", "data": data})

    def put(self, request, id):
        """
        修改一个上线单的内容
        """
        myonlineorder = self.get_object(id=id, delete=1)
        myonlineorder_old = self.get_object(id=id, delete=1)

        send_message_flag = False

        # 1. 修改保存的上线流程
        request = OnlineOrderFlowObject().put(request, myonlineorder.id)

        # 2. 修改关联的提测单状态为  “已上线”
        if request.data['status'] and myonlineorder.status != request.data['status']:
            print(request.data['status'])
            # 暂存data
            request_data = request.data.copy()
            # 进入这里，修改提测单状态
            if request.data['status'] == '上线完成':
                for testtask_id in json.loads(myonlineorder.testtask):
                    request.data.clear()
                    request.data['status'] = '已上线'
                    TestTaskDetail().put(request, testtask_id)
            # 还原data
            for (k, v) in request_data.items():
                request.data[k] = v

            # 发消息通知状态
            send_message_flag = True
        else:
            del request.data['status']

        # 3. 保存上线单
        serializer = OnlineOrderSerializer(myonlineorder, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 4. 保存操作记录
        change_data = request.data.copy()
        del change_data['onlineorderflow']
        del change_data['dev_users']
        del change_data['test_users']
        del change_data['product_users']
        keys = list(change_data.keys())
        print(keys)
        if 'onlineorderflow' in keys: keys.remove('onlineorderflow')
        old_content = [myonlineorder_old.__getattribute__(filed) for filed in keys]
        if len(keys) > 0:
            OnlineOrderOperation.objects.create(
                onlineorder_id=myonlineorder.id,
                username=request.session['user'].get('username'),
                realname=request.session['user'].get('realname'),
                change_fields=list(change_data.keys()),
                old_content=old_content,
                new_content=list(change_data.values()),
                change_action=self.actions(list(change_data.keys()), list(change_data.values()))
            )

        # 5.发现企业消息
        if send_message_flag:
            if serializer.data.get('status') == '上线完成':
                print('发给相关人员+流程负责人+部门领导+cto')
                user_list = json.loads(serializer.data.get("users"))
                user_list += json.loads(serializer.data.get("dev_users"))
                user_list += json.loads(serializer.data.get("test_users"))
                user_list += json.loads(serializer.data.get("product_users"))
                send_mode = ['users', 'leaders', 'CTO']

            elif serializer.data.get('status') == '验收完成':
                print('发给相关人员+流程负责人+部门领导')
                user_list = json.loads(serializer.data.get("users"))
                user_list += json.loads(serializer.data.get("dev_users"))
                user_list += json.loads(serializer.data.get("test_users"))
                user_list += json.loads(serializer.data.get("product_users"))
                send_mode = ['users', 'leaders']
            else:
                print('只发给上线流程中的负责人')
                user_list = json.loads(serializer.data.get("dev_users"))
                user_list += json.loads(serializer.data.get("test_users"))
                user_list += json.loads(serializer.data.get("product_users"))
                send_mode = ['users']

            MessageObject.send(title='TMS 上线提醒', user_list=user_list,
                               msg=f"【{serializer.data.get('status')}】【{serializer.data.get('system')}】{serializer.data.get('title')}",
                               forward=f"/flow/online/detail/{serializer.data.get('id')}",
                               send_mode=send_mode)

        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, id):
        """
        删除一个提测单
        """
        myonlineorder = self.get_object(id=id, delete=1)

        # todo 权限的控制，只有特定的角色才可以删除
        # return Response({"status": False, "message": "无权删除", "data": ""})

        myonlineorder.delete = 0
        myonlineorder.save()

        OnlineOrderOperation.objects.create(
            onlineorder_id=myonlineorder.id,
            username=request.session['user'].get('username'),
            realname=request.session['user'].get('realname'),
            change_action='删除上线单'
        )

        return Response({"status": True, "message": "成功", "data": ""})


class OnlineOrderOperationDetail(generics.GenericAPIView):
    """
    上线单操作历史
    """

    def get(self, request, id):
        """
        查询一个上线单的操作历史
        """
        myonlineorder_operations = OnlineOrderOperation.objects.filter(onlineorder_id=id).order_by('-id')
        serializer = OnlineOrderOperationSerializer(myonlineorder_operations, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})


class OnlineOrderCheckListObject(generics.GenericAPIView):
    """
    上线单checklist新增
    """

    # 配合文档，显示请求参数
    serializer_class = OnlineOrderCheckListSerializer

    def get(self, request, onlineorder_id, onlineorderflow_id):
        print(onlineorderflow_id)
        myoochecklist = OnlineOrderChecklist.objects.filter(onlineorderflow_id=onlineorderflow_id, delete=1)
        serializer_checklist = OnlineOrderCheckListSerializer(myoochecklist, many=True)
        data = {}
        for row in serializer_checklist.data:
            if row['type'] not in data: data[row['type']] = []
            data[row['type']].append(row)
        return Response({"status": True, "message": "成功", "data": data})

    def post(self, request, onlineorder_id, onlineorderflow_id):
        """
        上线单checklist新增
        """
        # 1. 检查传入的参数，并保存
        print(request.data)

        OnlineOrderChecklist.objects.filter(onlineorderflow_id=onlineorderflow_id).update(delete=0)

        del request.data['onlineorder_id']
        del request.data['onlineorderflow_id']

        # 3. 记录上线流程
        for type, value in request.data.items():
            for data in value:
                data['onlineorderflow_id'] = onlineorderflow_id
                data['type'] = type
                serializer_checklist = OnlineOrderCheckListSerializer(data=data)
                if not serializer_checklist.is_valid():
                    return Response({"status": False, "message": "数据格式不正确", "data": serializer_checklist.errors})
                serializer_checklist.save()

        OnlineOrderOperation.objects.create(
            onlineorder_id=onlineorder_id,
            username=request.session['user'].get('username'),
            realname=request.session['user'].get('realname'),
            change_fields="[]",
            old_content="[]",
            new_content="[]",
            change_action="提交了上线Checklist检查表单"
        )

        return Response({"status": True, "message": "成功", "data": request.data})
