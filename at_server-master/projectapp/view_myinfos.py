from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.response import Response
from projectapp.models import *
from projectapp.serializers import *
from django.db.models import Q
import json
from django.conf import settings


class MyInfosQuery(generics.GenericAPIView):
    '''查询个人信息'''

    def get(self, request):
        nameCondition = '"' + request.session['user']['realname'] + '"'

        # 所有项目
        all_verison = Version.objects.filter(
            Q(product_users__icontains=nameCondition) | Q(dev_users__icontains=nameCondition) | Q(
                test_users__icontains=nameCondition) | Q(master_name__icontains=nameCondition))

        # 进行中的
        doingTask = all_verison.filter(delete=1).exclude(stage=7).order_by('-id')
        serializer1 = GetVersionSerializerParam(doingTask, many=True)

        # 动态
        dynamics = VersionChangeHistory.objects.filter(version_id__in=[do.id for do in doingTask]).order_by('-id')
        serializer2 = GetVersionHistorySerializerParam(dynamics, many=True)

        # 所有参与需求
        all_tasks = StoryPlan.objects.filter(join_users__icontains=nameCondition)
        # 未安排的需求 此处不用添加""
        no_version_id_tasks = StoryPlan.objects.filter(delete=1).filter(
            version_master__icontains=request.session['user']['realname']).filter(version_id=0).order_by('-id')
        serializer3 = GetStorySerializerParam(no_version_id_tasks, many=True)

        return Response({"status": True, "message": "成功",
                         "data": {"doing": serializer1.data, "dynamic": serializer2.data,
                                  "no_verison": serializer3.data, "taksCount": str(len(all_tasks)),
                                  "projectCount": str(len(all_verison))}})
