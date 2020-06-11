from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *


class DocumentDetail(generics.GenericAPIView):
    """
    查询、修改、删除 接口文档
    """

    serializer_class = DocumentSerializer

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Document.objects.get(**kwargs)
            except Document.DoesNotExist:
                raise Http404

    def get_service_object(self, **kwargs):
        if kwargs:
            try:
                return Service.objects.get(**kwargs)
            except Service.DoesNotExist:
                raise Http404

    @staticmethod
    def get_children(arg_list):
        if len(arg_list) == 1:
            if arg_list[0]['example']:
                try:
                    return json.loads(arg_list[0]['example'])
                except:
                    return arg_list[0]['example']
            else:
                return arg_list[0]['name']

        arg_object = {}
        for param in arg_list:
            if param['children']:
                if param['type'] == 'list':
                    arg_object[param['name']] = [DocumentDetail.get_children(param['children'])]
                else:
                    arg_object[param['name']] = DocumentDetail.get_children(param['children'])
            else:
                arg_object[param['name']] = param['example']

        return arg_object

    @staticmethod
    def get_request_params(request_document):
        arg_list = []
        for arg in request_document:
            if arg['type'] == 'list':
                arg_object = [DocumentDetail.get_children(arg['children'])]
            else:
                arg_object = DocumentDetail.get_children(arg['children'])
            arg_list.append(arg_object)
        return arg_list

    def get(self, request, department_id, service_id, function_id):
        """
        查询一个接口的文档
        """
        try:
            document = self.get_object(service_id=function_id, status=1)
            serializer = DocumentSerializer(document)
            request_document = json.loads(serializer.data['request'])
            data = serializer.data
            data['example'] = DocumentDetail.get_request_params(request_document)
            data['service_name'] = self.get_service_object(id=service_id).service_name
            data['function_name'] = self.get_service_object(id=function_id).service_name
            return Response({"status": True, "message": "成功", "data": data})
        except:
            service_name = self.get_service_object(id=service_id).service_name
            function_name = self.get_service_object(id=function_id).service_name
            blank_data = {
                "document": f'<p><span style="font-size: x-large; font-weight: bold;">一、接口方法</span></p><ul><li>{service_name}.{function_name}<br></li></ul><p><span style="font-size: x-large; font-weight: bold;">二、业务场景</span></p><ul><li>请填写</li></ul><p><span style="font-weight: bold; font-size: x-large;">三、注意事项</span></p><ul><li>请填写，若没有，请写无</li></ul>',
                "request": [],
                "response": [],
            }
            serializer = DocumentSerializer(blank_data)
            data = serializer.data
            data['service_name'] = self.get_service_object(id=service_id).service_name
            data['function_name'] = self.get_service_object(id=function_id).service_name
            data['example'] = ["还未添加文档信息"]
            return Response({"status": True, "message": "初始文档", "data": data})

    def post(self, request, department_id, service_id, function_id):
        """
        新增/修改一个接口的文档
        """
        if Document.objects.filter(service_id=function_id, status=1).exists():
            document = self.get_object(service_id=function_id, status=1)
            serializer = DocumentSaveSerializer(document, data=request.data)
        else:
            request.data['service_id'] = function_id
            serializer = DocumentSaveSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, department_id, service_id, function_id):
        """
        删除一个接口的文档
        """
        document = self.get_object(service_id=function_id, status=1)
        document.status = 0
        document.save()
        return Response({"status": True, "message": "成功", "data": ""})
