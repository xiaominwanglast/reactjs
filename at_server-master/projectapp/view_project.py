from rest_framework import generics
from projectapp.serializers import *
from projectapp.base.utils import *

# 获取项目列表
class Projects(generics.GenericAPIView):
    '''获取项目列表'''
    serializer_class = GetProjectSerializerParam

    @retResponse()
    def get(self, request):
        temp = Project.objects.all()
        data = GetProjectSerializerParam(temp, many=True).data
        return True,data