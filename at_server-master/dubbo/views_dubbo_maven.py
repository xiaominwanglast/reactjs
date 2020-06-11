from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .dubbo_java_core import DubboJava
from django.conf import settings
import os


class MavenDetail(generics.GenericAPIView):
    """
    Maven更新与下载
    """

    serializer_class = MavenPomSerializer

    def read_pom(self):
        pom_file_path = os.path.join(settings.BASE_DIR, 'dubbo', 'maven', 'pom.xml')
        with open(pom_file_path, encoding='utf-8') as read_f:
            data = read_f.read()
        return data

    def write_pom(self, data):
        pom_file_path = os.path.join(settings.BASE_DIR, 'dubbo', 'maven', 'pom.xml')
        with open(pom_file_path, 'w', encoding='utf-8') as write_f:
            data = write_f.write(data)
        return data

    def get(self, request):
        """
        查询当前pom.xml的内容
        """
        return Response({"status": True, "message": "成功", "data": self.read_pom()})

    def put(self, request):
        """
        修改pom.xml的内容，并根据pom.xml的内容，下载jar，更新依赖
        """

        orgin_data = self.read_pom()

        self.write_pom(request.data['xml_data'])
        if DubboJava.update_dependency_jar_by_maven():
            return Response({"status": True, "message": "成功", "data": {}})
        else:
            self.write_pom(orgin_data)
            return Response({"status": False, "message": "更新失败，请检查xml正确性后重试", "data": {}})
