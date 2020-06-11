from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .zookeeper_core import ZKCore
from .dubbo_core import DubboCore


class FunctionList(generics.GenericAPIView):
    """
    查询service下所有的function名称
    """

    serializer_class = ServiceSerializer

    def get(self, request, department_id, service_id):
        """
        返回service下所有的function名称
        """
        functions = Service.objects.filter(status=1, parent_id=service_id)
        serializer = ServiceSerializer(functions, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def post(self, request, department_id, service_id):
        """
        新增一个function
        """
        service_name = Service.objects.get(id=service_id, status=1).service_name
        function_name = request.data['service_name']

        # 判断是否已经存在
        function_exist_count = Service.objects.filter(status=1, parent_id=service_id,
                                                      service_name=function_name).count()
        if function_exist_count > 0:
            return Response({"status": False, "message": f"{function_name}已经存在，无需再添加", "data": {}})

        # 检查service在zk上
        ZK = ZKCore('T3')
        host, port = ZK.get_providers(service_name)
        if not host:
            return Response({"status": False, "message": f"{service_name}未在zookeeper上发现，或没有provider", "data": {}})

        # 检查function是否存在
        conn = DubboCore(host, port)
        function_list = conn.ls(service_name)
        if function_name not in function_list:
            return Response(
                {"status": False,
                 "message": f"{function_name}未在{service_name}发现，请确认function名字正确，再确认pom.xml配置正确",
                 "data": {}})

        request.data['parent_id'] = service_id
        serializer = ServiceSaveSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        return Response({"status": True, "message": "成功", "data": serializer.data})


class FunctionDetail(generics.GenericAPIView):
    """
    查询、修改、删除function
    """

    serializer_class = ServiceSerializer

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Service.objects.get(**kwargs)
            except Service.DoesNotExist:
                raise Http404

    def get(self, request, department_id, service_id, function_id):
        """
        查询一个function的详情
        """
        function = self.get_object(id=function_id, status=1)
        serializer = ServiceSerializer(function)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def put(self, request, department_id, service_id, function_id):
        """
        修改一个function
        """
        function = self.get_object(id=function_id, status=1)
        serializer = ServiceSerializer(function, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, department_id, service_id, function_id):
        """
        删除一个function
        """
        function = self.get_object(id=function_id, status=1)
        function.status = 0
        function.save()
        return Response({"status": True, "message": "成功", "data": ""})
