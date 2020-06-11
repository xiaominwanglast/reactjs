from rest_framework import serializers
from .models import *


# 模板
class TemplateSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('title', 'header_data', 'template_columns', 'template_data')


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class TemplateListSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Template
        fields = ('id', 'title', 'create_user', 'update_user', 'create_time', 'update_time')


class TemplateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateHistory
        fields = '__all__'


# 项目
class ProjectSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'group_name', 'master', 'status')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


# 任务

class TaskSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'project_id', 'master', 'template_id', 'status')


class TaskSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    update_time = serializers.SerializerMethodField(required=False, read_only=True)

    def get_update_time(self, obj):
        form_ids = Form.objects.filter(task_id=obj.id).values_list('id', flat=True)
        try:
            return FormLogs.objects.filter(form_id__in=form_ids).order_by('-id')[0].create_time.strftime(
                "%Y-%m-%d %H:%M:%S")
        except:
            return obj.update_time.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Task
        fields = '__all__'


# 表单

class FormSerializerParam(serializers.Serializer):
    key = serializers.CharField(label="key", required=True, max_length=100)
    old = serializers.CharField(label="旧值", required=True, max_length=1000)
    new = serializers.CharField(label="新值", required=True, max_length=1000)


class FormSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Form
        fields = '__all__'
