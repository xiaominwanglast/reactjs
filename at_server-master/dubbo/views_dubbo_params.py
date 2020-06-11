from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .dubbo_java_core import DubboJava

DUBBOJAVA = DubboJava()


class ParamsDetail(generics.GenericAPIView):
    """
    查询dubbo服务的某个方法的具体参数
    """

    serializer_class = DocumentSerializer

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Document.objects.get(**kwargs)
            except Document.DoesNotExist:
                raise Http404

    def get_service_object(self, **kwargs):
        if kwargs:
            try:
                return Service.objects.get(**kwargs)
            except Service.DoesNotExist:
                raise Http404

    def get(self, request, department_id, service_id, function_id, env):
        """
        查询dubbo服务的某个方法的具体 原始参数
        """
        service_name = self.get_service_object(id=service_id).service_name
        function_name = self.get_service_object(id=function_id).service_name
        params = DUBBOJAVA.get_function_params(env, service_name, function_name)
        if params == "error":
            return Response({"status": False, "message": "失败,请检查pom.xml文件的依赖是否正确", "data": []})
        else:
            return Response({"status": True, "message": "成功", "data": params})
