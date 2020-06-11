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
from userapp import views
from django.urls import path, include

urlpatterns = [
    url(r'^session/$', views.UserAuth.as_view()),
    path('users/', views.UserList.as_view()),
    path('usersync/', views.UserSync.as_view()),
    path('usercross/<str:session_id>/', views.UserCross.as_view()),
    path('usercrosslogin/<str:name>/', views.UserRedirectLogin.as_view()),

]
