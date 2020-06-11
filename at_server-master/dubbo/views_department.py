from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *


class DepartmentList(generics.GenericAPIView):
    """
    查询所有dubbo接口部门提供方
    """

    serializer_class = ServiceSerializer

    def get(self, request):
        """
        返回所有dubbo接口部门提供方
        """
        departments = Service.objects.filter(status=1, parent_id=0)
        serializer = ServiceSerializer(departments, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def post(self, request):
        """
        新增一个部门
        """
        request.data['parent_id'] = 0
        serializer = ServiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})

        serializer.save()
        return Response({"status": True, "message": "成功", "data": serializer.data})


class DepartmentDetail(generics.GenericAPIView):
    """
    查询、修改、删除部门
    """

    serializer_class = ServiceSerializer

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Service.objects.get(**kwargs)
            except Service.DoesNotExist:
                raise Http404

    def get(self, request, department_id):
        """
        查询一个部门的详情
        """
        department = self.get_object(id=department_id, status=1)
        serializer = ServiceSerializer(department)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def put(self, request, department_id):
        """
        修改一个部门名称
        """
        department = self.get_object(id=department_id, status=1)
        serializer = ServiceSerializer(department, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, department_id):
        """
        删除一个部门
        """
        department = self.get_object(id=department_id, status=1)
        department.status = 0
        department.save()
        return Response({"status": True, "message": "成功", "data": ""})

