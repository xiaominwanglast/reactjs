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
from . import views_testtask, views_onlineorder, views_batch
from django.urls import path, include

urlpatterns = [
    # 提测单操作
    path('testtask/', views_testtask.TestTaskObject.as_view()),
    path('testtask/query/', views_testtask.TestTaskQuery.as_view()),
    path('testtask/<int:id>/', views_testtask.TestTaskDetail.as_view()),
    path('testtask/<int:id>/operations/', views_testtask.TestTaskOperationDetail.as_view()),

    # 上线单操作
    path('onlineorder/', views_onlineorder.OnlineOrderObject.as_view()),
    path('onlineorder/<int:id>/', views_onlineorder.OnlineOrderDetail.as_view()),
    path('onlineorder/<int:id>/operations/', views_onlineorder.OnlineOrderOperationDetail.as_view()),
    path('onlineorder/<int:onlineorder_id>/flow/<int:onlineorderflow_id>/checklist/',
         views_onlineorder.OnlineOrderCheckListObject.as_view()),
    path('onlineorder/query/', views_onlineorder.OnlineOrderQuery.as_view()),

    # 定时任务
    path('batch/onlineorder/checkandacceptbatch/', views_batch.CheckAndAcceptBatch.as_view()),

]
