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
from . import views_department, views_function, views_service, views_document
from . import views_dubbo, views_dubbo_params, views_dubbo_maven, views_dubbo_example, views_basedata
from django.urls import path, include

urlpatterns = [
    path('department/', views_department.DepartmentList.as_view()),
    path('department/<int:department_id>/service/', views_service.ServiceList.as_view()),
    path('department/<int:department_id>/service/<int:service_id>/function/', views_function.FunctionList.as_view()),
    path('department/<int:department_id>/', views_department.DepartmentDetail.as_view()),
    path('department/<int:department_id>/service/<int:service_id>/', views_service.ServiceDetail.as_view()),
    path('department/<int:department_id>/service/<int:service_id>/function/<int:function_id>/',
         views_function.FunctionDetail.as_view()),
    path('department/<int:department_id>/service/<int:service_id>/function/<int:function_id>/document/',
         views_document.DocumentDetail.as_view()),
    path('department/<int:department_id>/service/<int:service_id>/function/<int:function_id>/dubbo_params/<str:env>/',
         views_dubbo_params.ParamsDetail.as_view()),

    path('invoke/', views_dubbo.DubboService.as_view()),
    path('maven/', views_dubbo_maven.MavenDetail.as_view()),
    path('request_example/', views_dubbo_example.ExampleDetail.as_view()),
    path('basedata/', views_basedata.BaseDataInfo.as_view()),
]
