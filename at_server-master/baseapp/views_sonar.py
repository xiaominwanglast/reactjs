from rest_framework import generics, mixins
from rest_framework.response import Response
from .sonar import Sonar
from .serializers import *


class SonarSyncObject(generics.GenericAPIView):
    """
    同步sonar基准值
    """

    def get(self, request):
        """
        同步sonar基准值
        """
        count = 0
        for service_object in NewServices.objects.filter(delete=1).exclude(sonar_name=''):
            result = Sonar.get_sonar_result(service_object.sonar_name)
            if int(service_object.sonar_standard_bugs) > int(result.get('bugs')):
                service_object.sonar_standard_bugs = result.get('bugs')
                count += 1
            if int(service_object.sonar_standard_vulnerabilities) > int(result.get('vulnerabilities')):
                service_object.sonar_standard_vulnerabilities = result.get('vulnerabilities')
                count += 1
            service_object.sonar_standard_ncloc = result.get('ncloc')
            service_object.save()

        return Response({"status": True, "message": "成功", "data": count})
