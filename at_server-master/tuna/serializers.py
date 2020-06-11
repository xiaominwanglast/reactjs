from rest_framework import serializers
from .models import *


class NoneSerializer(serializers.Serializer):
    pass
    # team = serializers.CharField(label="示例", required=False, max_length=100)
