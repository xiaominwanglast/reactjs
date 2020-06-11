from rest_framework import generics
from rest_framework.response import Response
from projectapp.models import VersionDesignStageFile
from projectapp.serializers import *
from rest_framework.parsers import MultiPartParser, FileUploadParser
from django.conf import settings
import os, time, shutil
from django.http import FileResponse
from django.http import Http404
from django.utils.http import urlquote

class GetVersionDesignsStageFiles(generics.GenericAPIView):
    """
       版本设计阶段 获取文档列表
      """
    serializer_class = GetVersionDesignsStageFilesSerializerParam
    def get(self, request, id):
        values1 = VersionDesignStageFile.objects.filter(version_id=id, category_name='design', delete='1')
        values2 = VersionDesignStageFile.objects.filter(version_id=id, category_name='interface', delete='1')
        values3 = VersionDesignStageFile.objects.filter(version_id=id, category_name='database', delete='1')
        serializer1 = GetVersionDesignsStageFilesSerializerParam(values1, many=True)
        serializer2 = GetVersionDesignsStageFilesSerializerParam(values2, many=True)
        serializer3 = GetVersionDesignsStageFilesSerializerParam(values3, many=True)
        return Response({"status": True, "message": "成功", "data":{"design":serializer1.data,"interface":serializer2.data,"database":serializer3.data}})

class GetVersionScheduleFiles(generics.GenericAPIView):
    """
       获取排期文档列表
    """
    serializer_class = GetVersionDesignsStageFilesSerializerParam
    def get(self, request, id):
        values1 = VersionDesignStageFile.objects.filter(version_id=id, category_name='schedule', delete='1')
        serializer1 = GetVersionDesignsStageFilesSerializerParam(values1, many=True)
        return Response({"status": True, "message": "成功", "data":serializer1.data})

class GetVersionTestcaseFiles(generics.GenericAPIView):
    """
       获取测试用例文档列表
    """
    serializer_class = GetVersionDesignsStageFilesSerializerParam
    def get(self, request, id):
        values1 = VersionDesignStageFile.objects.filter(version_id=id, category_name='testcase', delete='1')
        serializer1 = GetVersionDesignsStageFilesSerializerParam(values1, many=True)
        return Response({"status": True, "message": "成功", "data":serializer1.data})

class FileUploadObject(generics.GenericAPIView):# 文件路径 金融超市/创建日期_版本号/具体文件 删除的时候 把这个文件移到/金融超市/Delete/创建日期_版本号/具体文件下
    """
    上传文件接口(只支持单文件上传)
    """
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        version = Version.objects.get(id=request.data['version_id'])
        files = request.FILES.getlist('file', None)
        file_object = files[0]
        file_name_prefix = '.'.join(file_object.name.split('.')[:-1])
        file_name_suffix = file_object.name.split('.')[-1] if '.' in file_object.name else ''
        file_name = f'{str(int((time.time()*1000)))}_{file_name_prefix}.{file_name_suffix}'
        file_dir = os.path.join(settings.BASE_DIR, 'files', 'project', version.product_title, version.create_time.strftime("%Y-%m-%d") + "_" + version.title)
        # for file_obj in files:
        if not os.path.exists(file_dir): os.makedirs(file_dir)
        file_path = os.path.join(file_dir, file_name)

        destination = open(file_path, 'wb+')
        for chunk in file_object.chunks():
            destination.write(chunk)
        destination.close()

        request.data['file_name'] = file_name
        request.data['path'] = file_path
        request.data['type'] = '1'
        request.data['create_user'] = request.session['user']['realname']
        print(request.data)
        serializer = FilePostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        # ret_data = serializer.data.copy()
        # del ret_data['file_path']

        # 插入变更
        data = request.data
        data['change_content'] = "上传了文档：" + file_name
        ##data['create_user']
        ##data['version_id']
        create = CreateVersionHistorySerializerParam(data=data)
        if create.is_valid():
            create.save()

        return Response({"status": True, "message": "成功", "data": ""})


class FileDownloadObject(generics.GenericAPIView):
    """
    下载文件接口
    """
    def get_object(self, **kwargs):
        if kwargs:
            try:
                return VersionDesignStageFile.objects.get(**kwargs)
            except VersionDesignStageFile.DoesNotExist:
                raise Http404

    def get(self, request, id):
        file_object = self.get_object(id=id)
        file = open(file_object.path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename="{urlquote(file_object.file_name)}"'
        return response


class FileDeleteObject(generics.GenericAPIView):
    """
    删除文件接口
    """
    def get_object(self, **kwargs):
        if kwargs:
            try:
                return VersionDesignStageFile.objects.get(**kwargs)
            except VersionDesignStageFile.DoesNotExist:
                raise Http404
    #数据更新？ 文件怎么更新状态？或者删除
    def delete(self,request,id):
        obj = self.get_object(id=id, delete=1)

        version = Version.objects.get(id=obj.version_id)
        file_dir = os.path.join(settings.BASE_DIR, 'files', 'project', version.product_title, 'Delete', version.create_time.strftime("%Y-%m-%d") + "_" + version.title)
        if not os.path.exists(file_dir): os.makedirs(file_dir)
        file_path = os.path.join(file_dir, obj.file_name)
        shutil.move(obj.path, file_path)#移动文件或重命名

        # todo 权限的控制，只有特定的角色才可以删除
        # return Response({"status": False, "message": "无权删除", "data": ""})

        obj.delete = 0
        obj.path = file_path
        obj.save()

        # 插入变更
        data = request.data
        data['change_content'] = "删除了文档：" + obj.file_name
        data['create_user'] = request.session['user']['realname']
        data['version_id'] = obj.version_id
        create = CreateVersionHistorySerializerParam(data=data)
        if create.is_valid():
            create.save()

        return Response({"status": True, "message": "成功", "data": ""})




class VersionAddStageContentObject(generics.GenericAPIView):
    """版本设计阶段 添加一条内容"""
    serializer_class = GetVersionDesignsStageFilesSerializerParam

    def post(self,request):
        data = request.data
        print(data)
        data['type'] = '2'
        data['path'] = request.data['file_name']
        data['create_user'] = request.session['user']['realname']
        create = GetVersionDesignsStageFilesSerializerParam(data=data)
        if create.is_valid():
            create.save()

            # 插入变更
            data['change_content'] = "上传了文档URL：" + data['file_name']
            ##data['create_user']
            ##data['version_id']
            create = CreateVersionHistorySerializerParam(data=data)
            if create.is_valid():
                create.save()

            return Response({"status": True, "message": "成功", "data": ""})
        else:
            return Response({"status": False, "message": "失败", "data": ""})




class VersionHandleStageContentObject(generics.GenericAPIView):
    """版本设计阶段 修改 删除 一条内容"""
    serializer_class = PutVersionDesignStageContentObjectSerializerParam

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return VersionDesignStageFile.objects.get(**kwargs)
            except VersionDesignStageFile.DoesNotExist:
                raise Http404



    def put(self,request,id):
        obj = self.get_object(id=id, delete=1)
        obj.path = request.data['file_name']
        serializer = PutVersionDesignStageContentObjectSerializerParam(obj,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True, "message":"成功","data":""})
        else:
            return Response({"status":False, "message":"失败","data":""})

    def delete(self,request,id):
        obj = self.get_object(id=id, delete=1)

        # todo 权限的控制，只有特定的角色才可以删除
        # return Response({"status": False, "message": "无权删除", "data": ""})

        obj.delete = 0
        obj.save()

        # 插入变更
        data = request.data
        data['change_content'] = "删除了文档URL：" + obj.file_name
        data['create_user'] = request.session['user']['realname']
        data['version_id'] = obj.version_id
        create = CreateVersionHistorySerializerParam(data=data)
        if create.is_valid():
            create.save()

        return Response({"status": True, "message": "成功", "data": ""})





