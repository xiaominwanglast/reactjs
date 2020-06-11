from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    user_list = serializers.CharField(label="用户", required=False, max_length=1000)
    title = serializers.CharField(label="标题", required=False, max_length=1000)
    message = serializers.CharField(label="内容", required=False, max_length=1000)
    key = serializers.CharField(label="密钥", required=False, max_length=100)
