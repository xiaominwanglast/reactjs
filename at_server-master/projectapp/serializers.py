from rest_framework import serializers
from projectapp.models import *

class SyncDesiredSerializerParam(serializers.Serializer):
    desired = serializers.CharField(label="desired", required=True, error_messages={'required': 'desired不能为空'})
    # project = serializers.CharField(label="project", required=True, error_messages={'required': 'project不能为空'})
    # create_time = serializers.CharField(label="create_time", required=True, error_messages={'required': 'create_time不能为空'})

class GetStoryParamsSerializerParam(serializers.Serializer):
    product_name = serializers.CharField(label="product_name", required=False, allow_blank=True)
    version_id = serializers.CharField(label="version_id", required=False)
    zentao_create_time = serializers.ListField(label="zentao_create_time", required=False)
    online_time = serializers.ListField(label="online_time", required=False)
    is_version = serializers.ListField(label="is_version", required=False)

class GetStorySerializerParam(serializers.ModelSerializer):
    product_name = serializers.CharField(label="product_name", required=False, allow_blank=True)
    # # zentao_id = serializers.CharField(label="zentao_id", required=False, allow_blank=True)
    version_id = serializers.CharField(label="version_id", required=False)
    online_time = serializers.DateTimeField(label="online_time", format="%Y-%m-%d", required=False, read_only=True)
    plan_online_time = serializers.DateTimeField(label="plan_online_time", format="%Y-%m-%d", required=False,read_only=True)
    zentao_create_time = serializers.DateTimeField(label="zentao_create_time", format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    create_time = serializers.DateTimeField(label="create_time", format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = StoryPlan
        fields = '__all__'

class EditStorySerializerParam(serializers.ModelSerializer):
    # story_id = serializers.CharField(label="story_id", required=True, error_messages={'required': 'story_id不能为空'})
    version_master = serializers.CharField(label="version_master", required=False, allow_blank=True)
    status = serializers.CharField(label="status", required=False, allow_blank=True)
    # online_time = serializers.DateTimeField(label="online_time", format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # plan_online_time = serializers.DateTimeField(label="plan_online_time", format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = StoryPlan
        fields = ('version_master','status')

class GetVersionHistorySerializerParam(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(label="create_time", format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = VersionChangeHistory
        fields = '__all__'

class CreateVersionHistorySerializerParam(serializers.ModelSerializer):
    change_content = serializers.CharField(label="change_content", required=True, allow_blank=False)
    create_user = serializers.CharField(label="create_user", required=True, allow_blank=False)
    version_id = serializers.CharField(label="version_id", required=True, allow_blank=False)
    class Meta:
        model = VersionChangeHistory
        fields = '__all__'

class CreateVersionSerializerParam(serializers.ModelSerializer):
    title = serializers.CharField(label="title", required=True, allow_blank=False)
    product_title = serializers.CharField(label="product_title", required=True, allow_blank=False)
    master_name = serializers.CharField(label="master_name", required=True, allow_blank=False)
    class Meta:
        model = Version
        fields = ('title', 'product_title', 'create_user','master_name')

class UpdateVersionStatusSerializerParam(serializers.ModelSerializer):
    id = serializers.CharField(label="id", required=True, allow_blank=False)
    stage = serializers.CharField(label="stage", required=True, allow_blank=False)
    status = serializers.CharField(label="status", required=False, allow_blank=False)
    class Meta:
        model = Version
        fields = '__all__'

class GetVersionSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'

class GetVersionStorySerializerParam(serializers.ModelSerializer):
    class Meta:
        model = StoryPlan
        fields = ('id', 'version_id', 'title', 'zentao_url', 'join_users')

class PutVersionSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'

class PutVersionStorySerializerParam(serializers.ModelSerializer):
    class Meta:
        model = StoryPlan
        fields = ('id', 'version_id', 'status', 'join_users')

class UpdateVersionStoryStatusSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = StoryPlan
        fields = ('id', 'version_id', 'status')

class GetProjectSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('project_id', 'project_name')

#获取版本设计阶段文档列表
class GetVersionDesignsStageFilesSerializerParam(serializers.ModelSerializer):
    version_id = serializers.CharField(label="version_id", required=True, allow_blank=False)
    create_time = serializers.DateTimeField(label="create_time", format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = VersionDesignStageFile
        fields = '__all__'

class FileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=5000000, allow_empty_file=False, use_url=True)
    version_id = serializers.CharField(label="version_id", required=True, allow_blank=False)
    category_name = serializers.CharField(label="category_name",required=True, allow_blank=False)


class FilePostSerializer(serializers.ModelSerializer):
    version_id = serializers.CharField(label="version_id", required=True, allow_blank=False)

    class Meta:
        model = VersionDesignStageFile
        fields = '__all__'

class PutVersionDesignStageContentObjectSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = VersionDesignStageFile
        fields = ('file_name',"remarks")

class DeleteVersionDesignStageContentObjectSerializerParam(serializers.ModelSerializer):
    id = serializers.CharField(label="id", required=True, allow_blank=False)
    class Meta:
        model = VersionDesignStageFile
        fields = ('id')

class StartSonarSerializerParam(serializers.Serializer):
    server_name = serializers.CharField(label="server_name", required=True, error_messages={'required': 'server_name不能为空'})
    git_branch = serializers.CharField(label="git_branch", required=True, error_messages={'required': 'git_branch不能为空'})

class StartServerSerializerParam(StartSonarSerializerParam):
    env = serializers.CharField(label="env", required=True, error_messages={'required': 'env不能为空'})

class DevStageParamsSerializerParam(StartSonarSerializerParam):
    # server_name = serializers.CharField(label="server_name", required=True, error_messages={'required': 'server_name不能为空'})
    # git_branch = serializers.CharField(label="git_branch", required=True, error_messages={'required': 'git_branch不能为空'})
    version_id = serializers.CharField(label="version_id", required=True, error_messages={'required': 'version_id不能为空'})
    server_name_key = serializers.CharField(label="server_name_key", required=False)

class IdSerializerParam(serializers.Serializer):
    id = serializers.CharField(label="id", required=True, error_messages={'required': 'id不能为空'})

class ServerInfoSerializerParam(serializers.Serializer):
    version_id = serializers.CharField(label="version_id", required=True, error_messages={'required': 'version_id不能为空'})

class DevStageSerializerParam(serializers.ModelSerializer):
    class Meta:
        model = DevStage
        fields = '__all__'

