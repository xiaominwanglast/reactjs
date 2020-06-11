from django.shortcuts import render

from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.response import Response
from wxwork.message import MessageObject
from .serializers import *
import json


class WXMessageObject(generics.GenericAPIView):
    """
    微信消息发送
    """

    # 配合文档，显示请求参数
    serializer_class = MessageSerializer

    def post(self, request):
        """
        发送微信消息
        """
        if request.data.get('key') == 'cb8e30682b927f35':
            MessageObject.send(title=request.data.get('title'), user_list=request.data.get('user_list').split(","),
                               msg=request.data.get('message'), send_mode=['users'])
            return Response({"status": True, "message": "成功", "data": {}})
        else:
            return Response({"status": False, "message": "key错误", "data": {}})
