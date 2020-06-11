from rest_framework import generics, views
from rest_framework.response import Response
from .serializers import *


class ProjectObject(views.APIView):
    """
    项目结构
    """

    def get(self, requset):
        data = []
        root_projects = Project.objects.filter(delete=1, pid=0)
        for root_project in root_projects:
            projects = Project.objects.filter(delete=1, pid=root_project.id)
            children_tmp = []
            for project in projects:
                children_tmp.append({"name": project.name, "id": project.id})
            data.append({"name": root_project.name, "id": root_project.id, "children": children_tmp})
        return Response({"status": True, "message": "成功", "data": data})
