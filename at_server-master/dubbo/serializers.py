from rest_framework import serializers
from .models import *
import json


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'service_name', 'service_desc')


class ServiceSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'service_name', 'service_desc', 'parent_id')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'document', 'request', 'response')


class DocumentSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'service_id', 'document', 'request', 'response')


class DubboServiceSerializer(serializers.Serializer):
    env = serializers.CharField(label="环境", required=True, max_length=100)
    service = serializers.CharField(label="服务名", required=True, max_length=100)
    function = serializers.CharField(label="方法名", required=True, max_length=100)
    param = serializers.CharField(label="参数", required=True, max_length=1000)
    datatype = serializers.CharField(label="返回数据类型(json/table)", required=False, max_length=1000)


class MavenPomSerializer(serializers.Serializer):
    xml_data = serializers.CharField(label="xml数据", required=True, max_length=10000)


class DubboExampleSerializer(serializers.Serializer):
    table_data = serializers.CharField(label="table参数", required=True, max_length=1000)


class BaseDataSerializer(serializers.Serializer):
    env = serializers.CharField(label="环境", required=True, max_length=100)
    service_id = serializers.CharField(label="服务名", required=True, max_length=100)
