from rest_framework import serializers
from .models import *
from Tower.settings import STATIC_URL,STATIC_PYTEST_URL
class TestResultDetailSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    report = serializers.SerializerMethodField()
    def get_report(self,obj):
        try:
            if obj.report !="":
                if 'rf' in obj.report:
                    return STATIC_URL+obj.report.split('/')[-3]+'/'+obj.report.split('/')[-2]
                elif 'py' in obj.report:
                    return STATIC_URL+'/'+STATIC_PYTEST_URL + obj.report.split('/')[-2]
                else:
                    return STATIC_URL+'/'+obj.report.split('/')[-3]+'/' + obj.report.split('/')[-2]
            else:
                return ''
        except:
            return ''

    class Meta:
        model = TestResult
        fields = "__all__"

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ("id","project_id", "name", "user", "env","status")

class TestReportSerializerModifyParam(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ("id","project_id","count","pass_count","fail_count","duration","status","report")


class OverViewModifyParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overview
        fields = ("project_id","key","value")

class pathSerializerParam(serializers.Serializer):
    # path = serializers.CharField(label="path", required=True, error_messages={'required': 'path不能为空'})
    project_id = serializers.CharField(label="project_id", required=True, error_messages={'required': 'project_id不能为空'})

class rfrunnerSerializerParam(serializers.Serializer):
    env = serializers.CharField(label="env", required=True, error_messages={'required': 'env不能为空'})
    suitename = serializers.ListField(label="suitename", required=True, error_messages={'required': 'suitename不能为空'})
    casename = serializers.ListField(label="casename")

class getSuiteNameSerializerParam(serializers.Serializer):
    project_id = serializers.CharField(label="project_id", required=True, error_messages={'required': 'project_id不能为空'})

class getCaseNameSerializerParam(serializers.Serializer):
    suite_name = serializers.CharField(label="suite_name", required=True, error_messages={'required': 'suite_name不能为空'})
    project_id = serializers.CharField(label="project_id", required=True, error_messages={'required': 'project_id不能为空'})

class TestSuiteSerializerParam(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = TestSuite
        fields = ('__all__')


class FactorCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorCase
        fields = ('factorName','factorCase','factorDesc','factorType','delete_flag')


# class TestChartsDetailSerializerParam(serializers.ModelSerializer):
#     class Meta:
#         model = Overview
#         fields = ('__all__')

