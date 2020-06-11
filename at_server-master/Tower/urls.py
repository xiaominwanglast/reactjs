"""Tower URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from . import batch
from . import settings
from django.conf.urls.static import static


schema_view = get_swagger_view(title='Tower平台 API文档')

urlpatterns = [
    path('api/user/', include('userapp.urls')),
    path('api/flow/', include('flowapp.urls')),
    # path('api/dubbo/', include('dubbo.urls')),
    path('api/base/', include('baseapp.urls')),
    path('api/tuna/', include('tuna.urls')),
    path('api/database/', include('databaseapp.urls')),
    path('api/form/', include('formapp.urls')),
    path('api/wx/', include('wxwork.urls')),
    path('admin/', admin.site.urls),
    path('api/testtools/', include('testtools.urls')),
    path('api/autotest/', include('autotestapp.urls')),
    path('api/manage/', include('projectapp.urls')),
    path('', schema_view),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

