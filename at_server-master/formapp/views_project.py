from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.response import Response
from flowapp.models import *
from .serializers import *
from wxwork.message import MessageObject
import json
from django.db.models import Q
import threading


class ProjectObject(generics.GenericAPIView):
    """
    项目新增
    """

    # 配合文档，显示请求参数
    serializer_class = ProjectSerializerParam

    def post(self, request):
        """
        表单模板新增
        """
        # 1. 检查传入的参数，并保存
        print(request.data)
        request.data['create_user'] = request.session['user'].get('realname')
        request.data['update_user'] = request.session['user'].get('realname')
        serializer = ProjectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        return Response({"status": True, "message": "成功", "data": serializer.data})


class ProjectListObject(generics.GenericAPIView):
    """
    项目
    """

    def get(self, request, group_name):
        """
        获取group_name下的所有项目列表
        """
        template = Project.objects.filter(group_name=group_name, delete=1)
        serializer = ProjectSerializer(template, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})



class ProjectDetailObject(generics.GenericAPIView):
    """
    项目的修改、删除、详情
    """

    # 配合文档，显示请求参数
    serializer_class = ProjectSerializerParam

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Project.objects.get(**kwargs)
            except Project.DoesNotExist:
                raise Http404

    def put(self, request, id):
        """
        修改项目
        """

        my_project = self.get_object(id=id, delete=1)
        request.data['update_user'] = request.session['user'].get('realname')
        serializer = ProjectSerializer(my_project, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        return Response({"status": True, "message": "成功", "data": serializer.data})

    def get(self, request, id):
        """
        查询一个项目详情
        """
        my_project = self.get_object(id=id, delete=1)
        serializer = ProjectSerializer(my_project)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, id):
        """
        删除一个项目
        """
        my_project = self.get_object(id=id, delete=1)
        # todo 权限的控制，只有特定的角色才可以删除
        # return Response({"status": False, "message": "无权删除", "data": ""})
        my_project.delete = 0
        my_project.save()
        return Response({"status": True, "message": "成功", "data": ""})
