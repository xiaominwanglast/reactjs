from rest_framework import serializers
from userapp.models import *


class UsersSerializerParam(serializers.Serializer):
    username = serializers.CharField(label="用户名", required=True, max_length=100)
    password = serializers.CharField(label="密码", required=True, max_length=100)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'id', 'username', 'realname', 'email', 'business_group', 'department', 'team', 'group_data',
            'department_list', 'status')


class UsersSerializerNameMail(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'realname', 'email')
