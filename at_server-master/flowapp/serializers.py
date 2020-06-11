from rest_framework import serializers
from .models import *


# ==============提测单====================

class TestTaskSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = TestTask
        fields = (
            'title', 'type', 'product_docs', 'service_name', 'service_branch', 'sql_files', 'content', 'notice',
            'performance_note', 'performance', 'product_users', 'dev_users', 'test_users', 'dev_team',
            'plan_submit_test_time',
            'plan_online_time', 'real_submit_test_time', 'real_online_time', 'status', 'version_id',
            'service_and_branch', 'system')


class TestTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTask
        fields = (
            'id', 'title', 'type', 'product_docs', 'service_name', 'service_branch', 'sql_files', 'content', 'notice',
            'performance_note', 'performance', 'product_users', 'dev_users', 'test_users', 'dev_team',
            'plan_submit_test_time', 'apollo_config',
            'plan_online_time', 'real_submit_test_time', 'real_online_time', 'status', 'version', 'version_id',
            'service_and_branch', 'system')


class TestTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTask
        fields = (
            'id', 'title', 'type', 'service_name', 'service_branch', 'product_users', 'dev_users', 'test_users',
            'dev_team', 'plan_submit_test_time', 'plan_online_time', 'real_submit_test_time', 'real_online_time',
            'status', 'sql_files', 'content', 'apollo_config', 'version', 'version_id', 'service_and_branch', 'system')


class TestTaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTaskHistory
        fields = (
            'id', 'title', 'type', 'product_docs', 'service_name', 'service_branch', 'sql_files', 'content', 'notice',
            'performance_note', 'performance', 'product_users', 'dev_users', 'test_users', 'dev_team',
            'plan_submit_test_time', 'plan_online_time',
            'real_submit_test_time', 'real_online_time', 'status', 'apollo_config', 'version_id', 'service_and_branch',
            'system')


class TestTaskQuerySerializer(serializers.Serializer):
    team = serializers.CharField(label="团队", required=False, max_length=100)
    status = serializers.CharField(label="状态", required=False, max_length=100)
    plan_test_time = serializers.DateField(label='计划提测时间', required=False)
    plan_online_time = serializers.DateField(label='计划上线时间', required=False)


class TestTaskOperationSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = TestTaskOperation
        fields = ('username', 'realname', 'change_action', 'create_time')


# ==============上线单====================


class OnlineOrderListSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    real_online_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)

    class Meta:
        model = OnlineOrder
        fields = '__all__'


class OnlineOrderSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = OnlineOrder
        fields = (
            'title', 'type', 'system', 'testtask', 'content', 'template', 'users')


class OnlineOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineOrder
        fields = '__all__'


class OnlineOrderFlowSerializer(serializers.ModelSerializer):
    check_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)

    class Meta:
        model = OnlineOrderFlow
        fields = '__all__'


class OnlineOrderOperationSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = OnlineOrderOperation
        fields = ('username', 'realname', 'change_action', 'create_time')


class OnlineOrderCheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineOrderChecklist
        fields = '__all__'
