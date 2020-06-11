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
from . import views_template, views_project, views_task, views_form
from django.urls import path, include

urlpatterns = [

    # 模板
    path('template/', views_template.TemplateObject.as_view()),
    path('template/<int:id>/', views_template.TemplateDetailObject.as_view()),

    # 项目
    path('project/', views_project.ProjectObject.as_view()),
    path('project/group/<str:group_name>/', views_project.ProjectListObject.as_view()),
    path('project/<int:id>/', views_project.ProjectDetailObject.as_view()),

    # 任务
    path('task/', views_task.TaskObject.as_view()),
    path('task/project/<int:project_id>/', views_task.TaskListObject.as_view()),
    path('task/<int:id>/', views_task.TaskDetailObject.as_view()),

    # 表单
    path('task/form/<int:task_id>/', views_form.FormObject.as_view()),
    path('form/<int:form_id>/', views_form.FormDetailObject.as_view()),
]
