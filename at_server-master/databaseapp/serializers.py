from rest_framework import serializers
from .models import *
import json


class DBInfoSerializer(serializers.ModelSerializer):
    env = serializers.SerializerMethodField()

    def get_env(self, obj):
        return json.loads(obj.config)

    class Meta:
        model = DBInfo
        fields = ('id', 'database', 'type', 'env', 'status')


class DBChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBChange
        fields = ('id', "dbinfo_id", "database", "type", "content","update_type")


class DBChangeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DBChangeHistory
        fields = ('id', "dbchange_id", "content")


class DBChangeSerializerModifyParam(serializers.ModelSerializer):
    class Meta:
        model = DBChange
        fields = ("id", "content",)


class DBChangeOrderSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    online_time = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    database = serializers.SerializerMethodField()
    update_type = serializers.CharField(label="状态", required=False, max_length=200)


    def get_database(self, obj):
        database = []
        for id in json.loads(obj.dbchange_ids):
            tmp = DBChange.objects.get(id=id)
            database.append(f'{tmp.type}:{tmp.database}')
            # print ("xx:"+str(database))
        return database

    class Meta:
        model = DBChangeOrder
        fields = "__all__"


class DBChangeOrderSerializerModifyParam(serializers.ModelSerializer):
    class Meta:
        model = DBChangeOrder
        fields = ("id", "title", "dev_team", "status", "check_users", "cc_users", "note", "dbchange_ids",)


class DBChangeAuditRecordSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = DBChangeAuditRecord
        fields = (
            "id", "dbchangeorder_id", "username", "realname", "content", "status", "create_time",
            "old_dbchangehistory_id", "new_dbchangehistory_id")


class DBExecuteRecordDetailSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = DBExecuteRecordDetail
        fields = "__all__"


class DBExecuteRecordSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = DBExecuteRecord
        fields = "__all__"