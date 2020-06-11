from rest_framework import serializers
from .models import *

class FlagValidator():
    def __init__(self, base):
        self.base = base
    def __call__(self, value):
        if value != self.base:
            message = '用户输入的值必须是 %s.' % self.base
            raise serializers.ValidationError(message)

class TestToolsSerializerParam(serializers.ModelSerializer):
    operate_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = TestTools
        fields = ('user_name',
            'project', 'option', 'env', 'product', 'phone', 'operate_time')

class CreateAccountSerializerParam(serializers.ModelSerializer):
    # phone = serializers.CharField(label="手机号", required=True, max_length=11, min_length=11, error_messages={'required': '手机号不能为空'})
    # user_name = serializers.CharField(label="用户名", required=True, max_length=100, validators=[PasswordValidator('666'))
    operate_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = CreateAccount
        fields = ('__all__')

class UserDbSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = UserDb
        fields = ('__all__')

class ProductConfigSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = ProductConfig
        fields = ('__all__')

class BankBinSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = BankBin
        fields = ('__all__')

class OverdueLog(serializers.Serializer):
    env = serializers.CharField(label='环境')
    prod_id = serializers.CharField(label='产品')
    mobilephone = serializers.CharField(label='手机号')
    borrowdays = serializers.IntegerField(label='待还天数')
    period_id = serializers.IntegerField(label='贷款期限')

class IdcardInfoSerializerParam(serializers.ModelSerializer):
    operate_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # name = serializers.CharField(label="name", required=True, error_messages={'required': 'name不能为None'}, help_text='dadasd')
    # idcard = serializers.CharField(label="idcard", max_length=18, required=True, error_messages={'required': 'idcard不能为空'})
    class Meta:
        model = IdcardInfo
        fields = ('__all__')

class MongoCodeSerializerParam(serializers.Serializer):
    userId = serializers.CharField(label="userId", error_messages={'required': 'userId不能为空'}, help_text='dadasd')
    db = serializers.CharField(label="数据库", max_length=50, required=True,error_messages={'required': 'db不能为空'})
    collection = serializers.CharField(label="集合", max_length=50, required=True, error_messages={'required': 'collection不能为空'})

class QueryPageSerializerParam(serializers.Serializer):
    pageNo = serializers.IntegerField(label="pageNo", error_messages={'required': 'pageNo不能为空'}, help_text='dadasd')
    pageSize = serializers.IntegerField(label="pageSize", error_messages={'required': 'pageSize不能为空'}, help_text='dadasd')
    env = serializers.IntegerField(label="env")
    isme = serializers.IntegerField(label="isme", error_messages={'required': 'pageSize不能为空'}, help_text='dadasd')

class MongoCollectionsSerializerParam(serializers.Serializer):
    db = serializers.CharField(label="db", required=True, error_messages={'required': 'db不能为空'})

class DecryptSerializerParam(serializers.Serializer):
    data = serializers.CharField(label="data", required=True, error_messages={'required': 'data不能为空'})

class EndecryptSerializerParam(serializers.Serializer):
    text = serializers.CharField(label="text", required=True, error_messages={'required': 'text不能为空'})
    type = serializers.CharField(label="type", required=True, error_messages={'required': 'type不能为空'})

class RedisInfoSerializerParam(serializers.Serializer):
    env = serializers.CharField(label="env", required=True, error_messages={'required': 'env不能为空'})
    dbNum = serializers.CharField(label="dbNum", required=True, error_messages={'required': 'dbNum不能为空'})
    phone = serializers.CharField(label="phone", max_length=11, required=True, error_messages={'required': 'phone不能为空'})
    project = serializers.CharField(label="project", required=True, error_messages={'required': 'project不能为空'})
    product = serializers.CharField(label="project", required=True, error_messages={'required': 'product不能为空'})