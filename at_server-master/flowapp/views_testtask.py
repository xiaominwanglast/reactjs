from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.response import Response
from flowapp.models import *
from flowapp.serializers import *
from wxwork.message import MessageObject
import json
from userapp.models import *
from baseapp.models import *
from django.db.models import Q
from databaseapp import views_dbchange
from projectapp.version_overview import UpdateVersionStage

import threading


class TestTaskObject(generics.GenericAPIView):
    """
    提测单新增
    """

    # 配合文档，显示请求参数
    serializer_class = TestTaskSerializerParam

    def post(self, request):
        """
        提测单新增
        """
        # 1. 检查传入的参数，并保存
        print(request.data)
        request.data['status'] = '已提测'
        serializer = TestTaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 2. 保留一份历史版本
        serializer_history = TestTaskHistorySerializer(data=request.data)
        serializer_history.is_valid() and serializer_history.save()

        # 3. 记录操作记录
        TestTaskOperation.objects.create(
            testtask_id=serializer.data.get('id'),
            username=request.session['user'].get('username'),
            realname=request.session['user'].get('realname'),
            current_version=serializer_history.data.get('id'),
            change_action='创建提测单并提测'
        )

        # 4.发现企业消息
        user_list = json.loads(serializer.data.get("test_users"))
        user_list += json.loads(serializer.data.get("product_users"))
        user_list += json.loads(serializer.data.get("dev_users"))
        MessageObject.send(title='TMS 提交测试', user_list=user_list,
                           msg=f"【{serializer.data.get('status')}】{serializer.data.get('title')}",
                           forward=f"/flow/testtask/detail_v4/{serializer.data.get('id')}",
                           send_mode=['users', 'leaders'])

        # 异步数据库变更通知大数据
        db_change_order_ids = json.loads(serializer.data.get("sql_files"))
        threading.Thread(target=views_dbchange.DBChangeOrderAuditRecordObject().notice_bigdata,
                         args=(db_change_order_ids, '提测阶段',)).start()

        # 关联的版本更新为测试中
        for version_id in json.loads(serializer.data.get("version_id")):
            request.data.clear()
            request.data['id'] = version_id
            request.data['stage'] = '5'
            request.data['status'] = '进行中'
            UpdateVersionStage().put(request, version_id)

        return Response({"status": True, "message": "成功", "data": serializer.data})


class TestTaskQuery(generics.GenericAPIView, mixins.ListModelMixin):
    """
    条件查询提测单,什么参数都不传，返回所有
    """

    # 配合文档，显示请求参数
    serializer_class = TestTaskListSerializer

    # pagination_class = LimitOffsetPaginationCustomer

    def get_queryset(self):
        if 'real_submit_test_time' in self.request.data:
            self.request.data['real_submit_test_time__gte'] = self.request.data['real_submit_test_time'][0]
            self.request.data['real_submit_test_time__lte'] = self.request.data['real_submit_test_time'][1]
            del self.request.data['real_submit_test_time']
        if 'plan_online_time' in self.request.data:
            self.request.data['plan_online_time__gte'] = self.request.data['plan_online_time'][0]
            self.request.data['plan_online_time__lte'] = self.request.data['plan_online_time'][1]
            del self.request.data['plan_online_time']
        if self.request.data.get('type') == 'Q':
            del self.request.data['type']
            Qfilter = []
            for k, v in self.request.data.items():
                Qfilter.append(f"Q({k}=\'{v}\')")
            Qfilter = "|".join(Qfilter)
            now_tasks = TestTask.objects.filter(delete=1).filter(eval(Qfilter)).exclude(
                status='已上线').order_by('-id')[:9999999]
            finish_tasks = TestTask.objects.filter(delete=1).filter(eval(Qfilter)).filter(
                status='已上线').order_by('-id')[:9999999]
            all_tasks = now_tasks.union(finish_tasks)
        else:
            now_tasks = TestTask.objects.filter(delete=1).filter(**self.request.data).exclude(
                status='已上线').order_by('-id')[:9999999]
            finish_tasks = TestTask.objects.filter(delete=1).filter(**self.request.data).filter(
                status='已上线').order_by('-id')[:9999999]
            all_tasks = now_tasks.union(finish_tasks)

        return all_tasks

    def post(self, request):
        """
        条件查询提测单,什么参数都不传，返回所有
        """
        return self.list(request)


class TestTaskDetail(generics.GenericAPIView):
    """
    查询、修改、删除提测单
    """

    # permission_classes = (IsOwnerOrReadOnly,)
    # 配合文档，显示请求参数
    serializer_class = TestTaskSerializerParam

    def actions(self, change_fields, new_content):
        chinese_dict = {
            "title": "修改标题",
            "type": "修改类型为" + new_content[change_fields.index('type')] if 'type' in change_fields else '',
            "product_docs": "修改需求文档项",
            "service_name": "修改涉及的服务",
            "service_branch": "修改提测分支为" + new_content[
                change_fields.index('service_branch')] if 'service_branch' in change_fields else '',
            "sql_files": "修改数据库变更文件",
            "content": "修改提测内容",
            "notice": "修改注意事项",
            "performance": "修改性能测试为" + new_content[
                change_fields.index('performance')] if 'performance' in change_fields else '',
            "performance_note": "修改性能测试内容",
            "product_users": "修改产品人员为" + new_content[
                change_fields.index('product_users')] if 'product_users' in change_fields else '',
            "dev_users": "修改开发人员为" + new_content[
                change_fields.index('dev_users')] if 'dev_users' in change_fields else '',
            "test_users": "修改测试人员为" + new_content[
                change_fields.index('test_users')] if 'test_users' in change_fields else '',
            "dev_team": "修改开发团队为" + new_content[change_fields.index('dev_team')] if 'dev_team' in change_fields else '',
            "plan_submit_test_time": "修改计划提测时间为" + new_content[
                change_fields.index('plan_submit_test_time')] if 'plan_submit_test_time' in change_fields else '',
            "plan_online_time": "修改计划上线时间为" + new_content[
                change_fields.index('plan_online_time')] if 'plan_online_time' in change_fields else '',
            "real_submit_test_time": "修改真正提测时间为" + new_content[
                change_fields.index('real_submit_test_time')] if 'real_submit_test_time' in change_fields else '',
            "real_online_time": "修改真正上线时间为" + new_content[
                change_fields.index('real_online_time')] if 'real_online_time' in change_fields else '',
            "status": "修改状态为" + new_content[change_fields.index('status')] if 'status' in change_fields else '',
            "apollo_config": "修改apollo配置",
            "version_id": "修改关联的版本",
            "service_and_branch": "修改服务与分支",
            "system": "修改所属项目",
        }

        actions = []
        for change_field in change_fields:
            actions.append(chinese_dict[change_field])

        return " , ".join(actions)

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return TestTask.objects.get(**kwargs)
            except TestTask.DoesNotExist:
                raise Http404

    def get(self, request, id):
        """
        查询一个提测单的详情
        """
        mytesttask = self.get_object(id=id, delete=1)
        serializer = TestTaskSerializer(mytesttask)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def put(self, request, id):
        """
        修改一个提测单的内容
        """
        mytesttask = self.get_object(id=id, delete=1)
        old_status = mytesttask.status
        old_content = [mytesttask.__getattribute__(filed) for filed in request.data.keys()]
        serializer = TestTaskSerializer(mytesttask, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        new_status = serializer.data.get('status')

        serializer_history = TestTaskHistorySerializer(data=serializer.data)
        serializer_history.is_valid() and serializer_history.save()

        TestTaskOperation.objects.create(
            testtask_id=mytesttask.id,
            username=request.session['user'].get('username'),
            realname=request.session['user'].get('realname'),
            change_fields=list(request.data.keys()),
            old_content=old_content,
            new_content=list(request.data.values()),
            current_version=serializer_history.data.get('id'),
            change_action=self.actions(list(request.data.keys()), list(request.data.values()))
        )
        if new_status == '已上线' and old_status != new_status:
            # 更新数据库审核单的状态
            if int(mytesttask.version) >= 2:
                changeorder_ids = json.loads(mytesttask.sql_files)
                for changeorder_id in changeorder_ids:
                    request.data.clear()
                    request.data['status'] = '已上线'
                    request.data['content'] = f'通过提测单【{mytesttask.title} #{mytesttask.id}#】 上线完成'
                    views_dbchange.DBChangeOrderAuditRecordObject().put(request, changeorder_id)
                    request.data.clear()

            for version_id in json.loads(mytesttask.version_id):
                request.data.clear()
                request.data['id'] = version_id
                request.data['stage'] = '7'
                UpdateVersionStage().put(request, version_id)
                request.data.clear()

        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, id):
        """
        删除一个提测单
        """
        mytesttask = self.get_object(id=id, delete=1)

        # todo 权限的控制，只有特定的角色才可以删除
        # return Response({"status": False, "message": "无权删除", "data": ""})

        mytesttask.delete = 0
        mytesttask.save()

        TestTaskOperation.objects.create(
            testtask_id=mytesttask.id,
            username=request.session['user'].get('username'),
            realname=request.session['user'].get('realname'),
            change_action='删除提测单'
        )

        return Response({"status": True, "message": "成功", "data": ""})


class TestTaskOperationDetail(generics.GenericAPIView):
    """
    提测单操作历史
    """

    def get(self, request, id):
        """
        查询一个提测单的操作历史
        """
        mytesttask_operations = TestTaskOperation.objects.filter(testtask_id=id).order_by('-id')
        serializer = TestTaskOperationSerializer(mytesttask_operations, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})
