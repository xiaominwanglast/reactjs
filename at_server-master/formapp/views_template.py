from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.response import Response
from flowapp.models import *
from .serializers import *
from wxwork.message import MessageObject
import json
from django.db.models import Q
import threading


class TemplateObject(generics.GenericAPIView):
    """
    表单模板新增
    """

    # 配合文档，显示请求参数
    serializer_class = TemplateSerializerParam

    def post(self, request):
        """
        表单模板新增
        """
        # 1. 检查传入的参数，并保存
        print(request.data)
        request.data['create_user'] = request.session['user'].get('realname')
        request.data['update_user'] = request.session['user'].get('realname')
        serializer = TemplateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 2. 保留一份历史版本
        request.data['template_id'] = serializer.data['id']
        serializer_history = TemplateHistorySerializer(data=request.data)
        serializer_history.is_valid() and serializer_history.save()

        return Response({"status": True, "message": "成功", "data": serializer.data})

    def get(self, request):
        """
        获取所有模板列表
        """
        template = Template.objects.filter(delete=1)
        serializer = TemplateListSerializer(template, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})


class TemplateDetailObject(generics.GenericAPIView):
    """
    表单模板的修改、删除、详情
    """

    # 配合文档，显示请求参数
    serializer_class = TemplateSerializerParam

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Template.objects.get(**kwargs)
            except Template.DoesNotExist:
                raise Http404

    def put(self, request, id):
        """
        修改表单模板
        """

        my_template = self.get_object(id=id, delete=1)
        request.data['update_user'] = request.session['user'].get('realname')
        serializer = TemplateSerializer(my_template, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        request.data['template_id'] = serializer.data['id']
        serializer_history = TemplateHistorySerializer(data=request.data)
        serializer_history.is_valid() and serializer_history.save()

        return Response({"status": True, "message": "成功", "data": serializer.data})

    def get(self, request, id):
        """
        查询一个表单模板详情
        """
        my_template = self.get_object(id=id, delete=1)
        serializer = TemplateSerializer(my_template)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, id):
        """
        删除一个表单模板
        """
        my_template = self.get_object(id=id, delete=1)
        # todo 权限的控制，只有特定的角色才可以删除
        # return Response({"status": False, "message": "无权删除", "data": ""})
        my_template.delete = 0
        my_template.save()
        return Response({"status": True, "message": "成功", "data": ""})
