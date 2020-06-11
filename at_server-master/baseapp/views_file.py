from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .serializers import *
from django.conf import settings
import os, time
from django.http import FileResponse
from django.http import Http404
from django.utils.http import urlquote
import chardet


class FileUploadObject(generics.GenericAPIView):
    """
    上传文件接口(只支持单文件上传)
    """
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        files = request.FILES.getlist('file', None)
        file_object = files[0]
        file_name_prefix = '.'.join(file_object.name.split('.')[:-1])
        file_name_suffix = file_object.name.split('.')[-1] if '.' in file_object.name else ''
        file_name = f'{str(int((time.time()*1000)))}_{file_name_prefix}.{file_name_suffix}'
        file_dir = os.path.join(settings.BASE_DIR, 'files', time.strftime("%Y-%m"))
        # for file_obj in files:
        if not os.path.exists(file_dir): os.makedirs(file_dir)
        file_path = os.path.join(file_dir, file_name)

        destination = open(file_path, 'wb+')
        for chunk in file_object.chunks():
            destination.write(chunk)
        destination.close()

        request.data['user_id'] = request.session['user'].get('id')
        request.data['file_name'] = file_name
        request.data['file_size'] = file_object.size
        request.data['file_type'] = file_name_suffix
        request.data['content_type'] = file_object.content_type
        request.data['file_path'] = file_path
        serializer = FilePostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        ret_data = serializer.data.copy()
        del ret_data['file_path']
        return Response({"status": True, "message": "成功", "data": ret_data})


class FileDownloadObject(generics.GenericAPIView):
    """
    下载文件接口
    """

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Files.objects.get(**kwargs)
            except Files.DoesNotExist:
                raise Http404

    def get(self, request, id):
        file_object = self.get_object(id=id)
        file = open(file_object.file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename="{urlquote(file_object.file_name)}"'
        return response


class FilePreviewObject(generics.GenericAPIView):
    """
    文件内容预览
    """

    def get_object(self, **kwargs):
        if kwargs:
            try:
                return Files.objects.get(**kwargs)
            except Files.DoesNotExist:
                raise Http404

    def get(self, request, id):

        file_object = self.get_object(id=id)
        print(file_object.content_type)
        if file_object.content_type not in ['text/plain', 'application/base64']:
            return Response({"status": False, "message": "此文件不支持预览", "data": "此文件不支持预览"})
        file = open(file_object.file_path, 'rb')
        f_read = file.read()
        f_charInfo = chardet.detect(f_read)
        print(f_charInfo)
        if not f_charInfo['encoding']: f_charInfo['encoding'] = 'utf-8'
        if f_charInfo['confidence'] > 0.8:
            f_read_decode = f_read.decode(f_charInfo['encoding'])
        else:
            f_read_decode = f_read
        return Response({"status": True, "message": "成功", "data": f_read_decode})


class FileListObject(generics.GenericAPIView):
    """
    附件列表接口，支持多个传id，逗号分隔
    """

    def get(self, request, ids):
        file_ids = ids.split(',')
        files_list = Files.objects.filter(id__in=file_ids)
        serializer = FileListSerializer(files_list, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})
