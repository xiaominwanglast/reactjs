from rest_framework import serializers
from .models import *


class FileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True)


class FilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('id', 'user_id', 'file_name', 'file_size', 'file_type', 'content_type', 'file_path')


class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('id', 'user_id', 'file_name', 'file_size', 'file_type', 'content_type')


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'


class ServiceListSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()

    # def get_department_name(self, obj):
    #     depart_name = []
    #
    #     def get_name(depart):
    #         depart_name.insert(0, depart.name)
    #         if depart.parent_id != '0':
    #             depart = Departments.objects.get(department_id=depart.parent_id)
    #             get_name(depart)
    #
    #     depart = Departments.objects.get(department_id=obj.department_id)
    #     get_name(depart)
    #
    #     return '-'.join(depart_name)
    def get_department_name(self, obj):
        return Departments.objects.get(id=obj.department_id).name

    class Meta:
        model = Services
        fields = ('id', 'department_id', 'name', 'department_name')


class NewServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewServices
        fields = "__all__"
