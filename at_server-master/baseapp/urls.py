"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views_file, views_service, views_department, views_apollo, views_jenkins, views_sonar
from django.urls import path, include

urlpatterns = [

    # 文件上传、下载
    path('files/', views_file.FileUploadObject.as_view()),
    path('files/<int:id>/download/', views_file.FileDownloadObject.as_view()),
    path('files/<int:id>/preview/', views_file.FilePreviewObject.as_view()),

    path('files/<str:ids>/', views_file.FileListObject.as_view()),

    # 服务列表
    path('services/', views_service.ServiceListObject.as_view()),

    # 部门列表
    path('departments/', views_department.DepartmentListObject.as_view()),

    # 阿波罗列表
    path('apollos/', views_apollo.ApolloInfoObject.as_view()),

    # 各项同步
    path('new/services/sync/', views_jenkins.JenkinsServiceSyncObject.as_view()),
    path('new/pmd/sync/', views_jenkins.JenkinsPMDSyncObject.as_view()),
    path('new/sonar/sync/', views_sonar.SonarSyncObject.as_view()),

    # 服务列表
    path('new/services/', views_jenkins.JenkinsServiceObject.as_view()),
    path('new/services/<str:job_name>/branch/', views_jenkins.JenkinsServiceBranchObject.as_view()),
]
