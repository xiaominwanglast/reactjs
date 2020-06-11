"""
Django settings for Tower project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: Tower the secret key used in production secret!
SECRET_KEY = 'hq#o)9w18&bq1s9o5+8m9=nm1$4a+@%0d@@*ya14g(wyi4$$e1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_swagger',
    'flowapp',
    'userapp',
    'baseapp',
    'wxwork',
    'dubbo',
    'testtools',
    'databaseapp',
    'formapp',
    'autotestapp',
    'projectapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Tower.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Tower.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tower',
        'USER': 'tower',
        'PASSWORD': 'tower.com',
        'HOST': '172.17.0.121',
        'PORT': '3333',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/rf_logs/'
STATIC_PYTEST_URL ='pytest_logs/'
STATIC_TESTNG_URL = 'testng_logs/'

SESSION_COOKIE_NAME = 'Tower_session_id'

LDAP_BASE_DN = 'ldap://172.16.0.7'

# # 跨域增加忽略
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

# REST_FRAMEWORK = {
#     'DEFAULT_PARSER_CLASSES': (
#         'rest_framework.parsers.JSONParser',
#     )
# }


REST_FRAMEWORK = {

    'EXCEPTION_HANDLER': 'Tower.exceptions.custom_exception_handler',

    'DEFAULT_PERMISSION_CLASSES': [
        'Tower.permissions.CustomerPermission',
    ],
    'DEFAULT_PAGINATION_CLASS': 'Tower.pagination.LimitOffsetPaginationCustomer',
    'PAGE_SIZE': 10
}

WXWORK = {
    "send": True,
    "token": "93c5d08277c09793916e8ff767cdd03f",
    "title": "TMS 提醒",
    "custom_ip": "172.17.1.54",
    "custom_user": "chengm",
    "charset": "utf-8",
    "oa_server": "https://oa.2345.cn/RTXServer/Api/SendRtx",
    "tc_server": "http://tms.2345intra.com",
}

TMT_CROSS_LOGIN = "http://tmt.2345intra.com/api/user/crosslogin/"
DEVOPS_CROSS_LOGIN = "http://devops.2345intra.com/api/deploy/userauth/"
TESTNG_CROSS_LOGIN = "http://testng.2345intra.com/api/setSessionUserInfo"
# 服务器目录

LOGPATH = '/var/data/logs/'
CODEPATH = '/var/data/code/'

# 本地目录
LOCALLOGPATH = '/var/data/logs/'
LOCALCODEPATH = '/var/data/code/'
STATICFILES_DIRS = (LOGPATH,)

#禅道地址
ZENTAO_HOST = 'http://zentao.2345intra.com/zentao'

TEST_JENKINS_HOST = "http://jenkins.2345intra.com"
TEST_JENKINS_USERNAME = "chengm"
TEST_JENKINS_API_TOKEN = "116cdcb457019209b0e05b9f0dc5c30f77"

ONLINE_JENKINS_HOST = 'http://jenkins.jr.2345.net'
ONLINE_JENKINS_USERNAME = 'chenc'
ONLINE_JENKINS_API_TOKEN = '116bb03c7b6f473f63785d1927e0f24fab'

ONLINE_SONAR_HOST = 'http://sonar.2345intra.com'
TEST_SONAR_HOST = 'http://sonartest.2345intra.com'

STATIC_PYTEST_URL ='/pytest_logs/'
STATIC_TESTNG_URL = '/testng_logs/'


SIT_DATABASE = {"T1_CDW": {"host": "172.17.0.32", "port": 3311, "user": "test_ljd", "pwd": "test_ljd1"},
                "T2_CDW": {"host": "172.16.0.142", "port": 3311, "user": "test_ljd", "pwd": "test_ljd1"},
                "T3_CDW": {"host": "172.17.0.30", "port": 3311, "user": "test_ljd", "pwd": "test_ljd1"},
                "T1": {"host": "172.17.0.32", "port": 3306, "user": "test_ljd", "pwd": "test_ljd1"},
                "T2": {"host": "172.16.0.142", "port": 3307, "user": "test_ljd", "pwd": "test_ljd1"},
                "T3": {"host": "172.17.0.30", "port": 3306, "user": "test_ljd", "pwd": "test_ljd1"},
                "P1": {"host": "172.17.0.34", "port": 3306, "user": "test_ljd", "pwd": "test_ljd1"},
                "D1": {"host": "172.17.0.120", "port": 3306, "user": "test_ljd", "pwd": "test_ljd1"},
                "D2": {"host": "172.17.0.121", "port": 3306, "user": "test_ljd", "pwd": "test_ljd1"}}

envs = ['T1', 'T2', 'T3']