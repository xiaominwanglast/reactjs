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
from . import views_dbchange
from django.urls import path, include

urlpatterns = [
    # 数据库变更单操作
    path('info/', views_dbchange.DBInfoObject.as_view()),
    path('change/', views_dbchange.DBChangeObject.as_view()),
    path('change/<int:id>/', views_dbchange.DBChangeDetailObject.as_view()),
    path('change_order/', views_dbchange.DBChangeOrderObject.as_view()),
    path('change_order/<int:id>/', views_dbchange.DBChangeOrderDetailObject.as_view()),
    path('change_order/<int:id>/audit/', views_dbchange.DBChangeOrderAuditRecordObject.as_view()),
    path('change_history/<str:ids>/', views_dbchange.DBChangeHistoryDetailObject.as_view()),
    path('change_order/query/', views_dbchange.DBChangeOrderQuery.as_view()),
    path('change/notice/', views_dbchange.DBChangeNoticeObject.as_view()),
    path('get_type/', views_dbchange.DBChangeUpdateType.as_view()),
    path('execute/', views_dbchange.DBExecuteObject.as_view()),
    path('execute_history/<int:id>', views_dbchange.DBExecuteHistoryObject.as_view())
]