from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .zookeeper_core import ZKCore


class ServiceList(generics.GenericAPIView):
    """
    查询部门下所有的service
    """

    serializer_class = ServiceSerializer

    def get(self, request, department_id):
        """
        返回部门下所有的service名称
        """
        services = Service.objects.filter(status=1, parent_id=department_id)
        serializer = ServiceSerializer(services, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def post(self, request, department_id):
        """
        新增一个service
        """

        service_name = request.data['service_name']

        # 判断是否已经存在
        function_exist_count = Service.objects.filter(status=1, parent_id=department_id,
                                                      service_name=service_name).count()
        if function_exist_count > 0:
            return Response({"status": False, "message": f"{service_name}已经存在，无需再添加", "data": {}})

        ZK = ZKCore('T3')
        host, port = ZK.get_providers(service_name)
        if not host:
            return Response({"status": False, "message": f"{service_name}未在zookeeper上发现，或没有provider", "data": {}})

        request.data['parent_id'] = department_id
        serializer = ServiceSaveSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        return Response({"status": True, "message": "成功", "data": serializer.data})


class ServiceDetail(generics.GenericAPIView):
    """
    查询、修改、删除service
    """

    serializer_class = ServiceSerializer

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Service.objects.get(**kwargs)
            except Service.DoesNotExist:
                raise Http404

    def get(self, request, department_id, service_id):
        """
        查询一个service的详情
        """
        service = self.get_object(id=service_id, status=1)
        serializer = ServiceSerializer(service)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def put(self, request, department_id, service_id):
        """
        修改一个service
        """
        service = self.get_object(id=service_id, status=1)
        serializer = ServiceSerializer(service, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, department_id, service_id):
        """
        删除一个service
        """
        service = self.get_object(id=service_id, status=1)
        service.status = 0
        service.save()
        return Response({"status": True, "message": "成功", "data": ""})
