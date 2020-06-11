from userapp.models import Users
from userapp.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from userapp.ldapcore import *
import re
import json
import base64
from django.contrib.sessions import middleware
from baseapp.models import *
from django.conf import settings
from django.db.models import Q


class UserAuth(generics.GenericAPIView):
    """
    用户登录鉴权
    """

    # 配合文档，显示请求参数
    serializer_class = UsersSerializerParam

    def get(self, request):
        """
        判断用户session是否过期
        """
        user = request.session['user']
        serializer = UsersSerializer(user)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def post(self, request):
        """
        用户登录鉴权，域账号登录
        """
        username = request.data.get('username')
        password = request.data.get('password')

        # ldap验证身份
        ldap = ADUtil()
        ldap_user = ldap.auth(username, password)
        if ldap_user[0] != 'OK':
            return Response({"status": False, "message": "登录失败，身份验证出错", "data": ""})

        # 创建用户
        userinfo, created = Users.objects.get_or_create(username=username)
        if created:
            userinfo.realname = str(ldap_user[2]['displayName'], encoding='utf-8')
            userinfo.email = str(ldap_user[2]['mail'], encoding='utf-8')
        userinfo.group_data = str(ldap_user[2]['distinguishedName'], encoding='utf-8')
        group_data = re.findall("OU=(.*?),", userinfo.group_data, re.I)
        userinfo.business_group = group_data[-2]
        userinfo.department = "-".join(group_data[1:-2])
        userinfo.team = group_data[0]
        userinfo.department_list = json.dumps(group_data[:-1][::-1], ensure_ascii=False)
        userinfo.save()

        serializer = UsersSerializer(userinfo)

        department_list = json.loads(serializer.data.get('department_list'))
        if department_list[0] == '金融科技事业群':
            pass
        elif department_list == ["集团公司", "技术中心", "运维部"]:
            pass
        elif department_list == ["互联网事业群", "技术中心", "测试与质控部", "王牌与导购测试组"]:
            pass
        else:
            return Response({"status": False, "message": "权限不足，请联系管理员。(@肖刚 @陈高敏)", "data": {}})

        # 设置session
        request.session['user'] = serializer.data
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request):
        """
        用户退出登录
        """
        del request.session['user']
        return Response({"status": True, "message": "成功", "data": {}})


class UserList(generics.GenericAPIView):
    """
    用户列表
    """

    # 配合文档，显示请求参数
    serializer_class = UsersSerializerParam

    def get(self, request):
        """
        获取所有用户列表（可用于开发人员，测试人员等）
        """

        users = Users.objects.filter(business_group=request.session['user']['business_group']).order_by('-status', 'id')
        serializer = UsersSerializer(users, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def post(self, request):
        """
        根据用户名或姓名查询用户
        """
        query = request.data.get('query')
        users = Users.objects.filter(Q(username__icontains=query) | Q(realname__icontains=query)).order_by('-status',
                                                                                                           'id')
        serializer = UsersSerializer(users, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})


class UserSync(generics.GenericAPIView):
    """
    用户同步
    """

    serializer_class = UsersSerializerParam

    def post(self, request):
        """
        用户同步
        """
        # username = request.data.get('username')
        # password = request.data.get('password')
        username = str(base64.b64decode('Y2hlbmdt'), 'utf-8')
        password = str(base64.b64decode('dGRGMDA0MTYwMA=='), 'utf-8')

        # ldap验证身份
        ldap = ADUtil()
        ldap_users = ldap.get_all_users(username, password)

        Users.objects.all().update(status=0)

        for ldap_user in ldap_users:
            ldap_user = (1, 1, ldap_user)
            print(ldap_user)
            # 创建用户
            userinfo, created = Users.objects.get_or_create(
                username=str(ldap_user[2]['sAMAccountName'], encoding='utf-8'))
            if created:
                userinfo.realname = str(ldap_user[2]['displayName'], encoding='utf-8')
                try:
                    userinfo.email = str(ldap_user[2]['mail'], encoding='utf-8')
                except:
                    pass
            userinfo.group_data = str(ldap_user[2]['distinguishedName'], encoding='utf-8')
            group_data = re.findall("OU=(.*?),", userinfo.group_data, re.I)
            try:
                userinfo.business_group = group_data[-2]
            except:
                pass
            userinfo.department = "-".join(group_data[1:-2])
            userinfo.team = group_data[0]
            userinfo.department_list = json.dumps(group_data[:-1][::-1], ensure_ascii=False)
            userinfo.status = 1
            userinfo.save()

        # 同步部门列表
        department_list = Users.objects.filter(status=1).values_list('department_list', flat=True).distinct()
        for department in department_list:
            department_json = json.loads(department)
            if len(department_json)<=0:
                continue
            department_name = '-'.join(department_json)
            department_info, created = Departments.objects.get_or_create(name=department_name)
            if created:
                department_info.group = department_json[0]
                department_info.department_list = department
                department_info.save()

        return Response({"status": True, "message": "成功", "data": len(ldap_users)})


class UserCross(generics.GenericAPIView):
    """
    跨域获取用户信息
    """

    def get(self, request, session_id):
        """
        根据session_id查询用户信息
        """
        session_data = middleware.SessionMiddleware().SessionStore(session_id)
        user_info = session_data.get('user')
        return Response({"status": True, "message": "成功", "data": user_info})


class UserRedirectLogin(generics.GenericAPIView):
    """
    用户联合登录跳转
    """

    def get(self, request, name):
        """
        用户联合登录跳转
        """
        session_id = request.session.session_key
        if name == 'TMT':
            url = settings.TMT_CROSS_LOGIN
        elif name == 'DEVOPS':
            url = settings.DEVOPS_CROSS_LOGIN
        elif name == 'TESTNG':
            url = settings.TESTNG_CROSS_LOGIN
        return Response(status=301, headers={'location': f"{url}?session_id={session_id}"})
