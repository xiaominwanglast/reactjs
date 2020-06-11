from rest_framework import generics
from rest_framework.response import Response
from .serializers import *


class DepartmentListObject(generics.GenericAPIView):
    """
    获取团队列表
    """

    def get(self, request):
        depart_list = Departments.objects.filter(status=1, group=request.session['user']['business_group'])
        serializer = DepartmentListSerializer(depart_list, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})
