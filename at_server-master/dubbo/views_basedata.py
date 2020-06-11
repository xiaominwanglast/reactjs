from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .zookeeper_core import ZKCore
from .dubbo_core import DubboCore


class BaseDataInfo(generics.GenericAPIView):
    """
    获取基础信息
    """

    serializer_class = BaseDataSerializer

    def post(self, request):
        """
        返回基础查询信息
        """

        service_id = request.data.get('service_id')
        env = request.data.get('env')

        ZK = ZKCore('T3')

        if service_id:
            service_name = Service.objects.get(id=service_id, status=1).service_name
            host, port = ZK.get_providers(service_name)
            if not host:
                return Response({"status": False, "message": f"{service_name}未在zookeeper上发现，或没有provider", "data": []})

            conn = DubboCore(host, port)
            function_list = conn.ls(service_name)
            if not function_list:
                return Response({"status": False, "message": f"{service_name}下，没有任何function", "data": []})
            return Response({"status": True, "message": "成功", "data": function_list})
        else:
            service_list = ZK.get_services()
            return Response({"status": True, "message": "成功", "data": service_list})
