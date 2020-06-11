from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.response import Response
from flowapp.models import *
from .serializers import *
from wxwork.message import MessageObject
import json
from django.db.models import Q
import threading


class FormObject(generics.GenericAPIView):
    """
    表单的详情
    """

    def get(self, request, task_id):
        """
        查询一个任务下的表单
        """
        my_form = Form.objects.filter(task_id=task_id, delete=1)

        data = []

        for row in my_form:
            tmp = json.loads(row.data)
            tmp['id'] = row.id
            data.append(tmp)

        my_task = Task.objects.get(id=task_id, delete=1)
        return Response({"status": True, "message": "成功",
                         "data": {'data': data, 'columns': json.loads(my_task.template_columns)}})


class FormDetailObject(generics.GenericAPIView):
    # 配合文档，显示请求参数
    serializer_class = FormSerializerParam

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Form.objects.get(**kwargs)
            except Form.DoesNotExist:
                raise Http404

    def put(self, request, form_id):
        """
        修改一行表单的内容
        """

        my_form = self.get_object(id=form_id, delete=1)
        key = request.data['key']
        old = request.data['old']
        new = request.data['new']
        print(key, old, new)

        data = json.loads(my_form.data)

        # if key not in data.keys():
        #     return Response({"status": False, "message": "这个值不属于这个表单", "data": "这个值不属于这个表单"})

        if data.get(key, '') != old:
            return Response({"status": False, "message": f"这个值已经被【{my_form.update_user}】更新为【{data[key]}】,有冲突哦！",
                             "data": {}})

        data[key] = new
        request.data['data'] = json.dumps(data, ensure_ascii=False)
        request.data['update_user'] = request.session['user'].get('realname')
        serializer = FormSerializer(my_form, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        my_task = Task.objects.get(id=my_form.task_id)
        for column in json.loads(my_task.template_columns):
            if column.get('key') == key:
                FormLogs.objects.create(form_id=form_id, key=key, title=column.get('title'),
                                        old=old, new=new, update_user=request.session['user'].get('realname'))
                break

        return Response({"status": True, "message": "成功", "data": serializer.data})
