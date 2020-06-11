from .serializers import *
from rest_framework.response import Response
from rest_framework import generics


class Demo(generics.GenericAPIView):
    """
    用户列表
    """

    # 配合文档，显示请求参数
    serializer_class = NoneSerializer

    def get(self, request):
        """
        get示例
        """
        return Response({"status": True, "message": "成功", "data": "get"})

    def post(self, request):
        """
        post示例
        """
        return Response({"status": True, "message": "成功", "data": "post"})
