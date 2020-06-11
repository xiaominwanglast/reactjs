from rest_framework import generics, mixins
from rest_framework.response import Response
from .jenkins import Jenkins
from .serializers import *


class JenkinsServiceSyncObject(generics.GenericAPIView):
    """
    Jenkins中jobs服务的数据
    """

    def get(self, request):
        """
        同步Jenkins中的job数据
        """
        count = 0
        for (job_name, view_name) in Jenkins.get_jobs():
            servicec_object, created = NewServices.objects.get_or_create(job_name=job_name)
            servicec_object.view_name = view_name
            servicec_object.save()
            count += 1
        return Response({"status": True, "message": "成功", "data": count})


class JenkinsPMDSyncObject(generics.GenericAPIView):
    """
    同步PMD基准值
    """

    def get(self, request):
        """
        同步PMD基准值
        """
        count = 0
        for service_object in NewServices.objects.filter(delete=1).exclude(pmd_name=''):
            pmd_result = Jenkins.get_pmd_result(service_object.pmd_name)
            if int(service_object.high_priority_warnings) > int(pmd_result.get('numberOfHighPriorityWarnings')):
                service_object.high_priority_warnings = pmd_result.get('numberOfHighPriorityWarnings')
                count += 1
            if int(service_object.normal_priority_warnings) > int(pmd_result.get('numberOfNormalPriorityWarnings')):
                service_object.normal_priority_warnings = pmd_result.get('numberOfNormalPriorityWarnings')
                count += 1
            service_object.save()

        return Response({"status": True, "message": "成功", "data": count})


class JenkinsServiceObject(generics.GenericAPIView):
    """
    Jenkins中jobs服务的数据
    """

    def get(self, request):
        """
        Jenkins中jobs服务的数据
        """
        service_list = NewServices.objects.filter(delete=1).order_by("view_name")
        serializer = NewServiceListSerializer(service_list, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})


class JenkinsServiceBranchObject(generics.GenericAPIView):
    """
    Jenkins中jobs服务的分支数据
    """

    def get(self, request, job_name):
        """
        Jenkins中jobs服务的分支数据
        """
        return Response({"status": True, "message": "成功", "data": Jenkins.get_service_branch(job_name)})
