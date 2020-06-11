from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from django.conf import settings
import os, time
from django.http import FileResponse
from django.http import Http404
from django.utils.http import urlquote


class ServiceListObject(generics.GenericAPIView):
    """
    所有服务列表
    """
    serializer_class = ServiceListSerializer

    def get(self, request):
        service_list = Services.objects.filter(status=1).order_by("department_id")
        serializer = ServiceListSerializer(service_list, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})
