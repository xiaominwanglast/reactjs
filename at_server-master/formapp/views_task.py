from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.response import Response
from flowapp.models import *
from .serializers import *
from wxwork.message import MessageObject
import json
from django.db.models import Q
import threading


class TaskObject(generics.GenericAPIView):
    """
    任务新增
    """

    # 配合文档，显示请求参数
    serializer_class = TaskSerializerParam

    def post(self, request):
        """
        任务新增
        """
        # 1. 检查传入的参数，并保存
        print(request.data)
        request.data['create_user'] = request.session['user'].get('realname')
        request.data['update_user'] = request.session['user'].get('realname')
        template = Template.objects.get(id=request.data['template_id'], delete=1)
        request.data['template_columns'] = template.template_columns
        request.data['template_data'] = template.template_data
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 2.初始化form表
        for row in json.loads(template.template_data):
            Form.objects.create(task_id=serializer.data['id'], data=json.dumps(row, ensure_ascii=False))

        return Response({"status": True, "message": "成功", "data": serializer.data})


class TaskListObject(generics.GenericAPIView):
    """
    任务列表
    """

    def get(self, request, project_id):
        """
        获取project_id下的所有任务列表
        """
        task = Task.objects.filter(project_id=project_id, delete=1)
        serializer = TaskSerializer(task, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})


class TaskDetailObject(generics.GenericAPIView):
    """
    任务的修改、删除、详情
    """

    # 配合文档，显示请求参数
    serializer_class = TaskSerializerParam

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Task.objects.get(**kwargs)
            except Task.DoesNotExist:
                raise Http404

    def put(self, request, id):
        """
        修改任务
        """

        my_Task = self.get_object(id=id, delete=1)
        request.data['update_user'] = request.session['user'].get('realname')
        serializer = TaskSerializerParam(my_Task, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        return Response({"status": True, "message": "成功", "data": serializer.data})

    def get(self, request, id):
        """
        查询一个任务详情
        """
        my_Task = self.get_object(id=id, delete=1)
        serializer = TaskSerializer(my_Task)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, id):
        """
        删除一个任务
        """
        my_Task = self.get_object(id=id, delete=1)
        # todo 权限的控制，只有特定的角色才可以删除
        # return Response({"status": False, "message": "无权删除", "data": ""})
        my_Task.delete = 0
        my_Task.save()
        return Response({"status": True, "message": "成功", "data": ""})
