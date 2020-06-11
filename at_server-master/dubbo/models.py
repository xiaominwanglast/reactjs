from django.db import models
import json

class Service(models.Model):
    """ 服务表 """
    id = models.AutoField(primary_key=True)

    service_name = models.TextField('服务、方法名', blank=True, default='')
    service_desc = models.TextField('中文描述', blank=True, default='')
    parent_id = models.CharField('上级id', blank=True, max_length=100, default='0')
    status = models.CharField('状态', blank=True, max_length=100, default='1')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.id, self.service_name, self.service_desc,


class Document(models.Model):
    """ 接口文档 """
    id = models.AutoField(primary_key=True)
    service_id = models.CharField('service表的id', blank=True, max_length=100, default='0')
    document = models.TextField('文档说明', blank=True, default='')
    request = models.TextField('请求参数', blank=True, default='')
    response = models.TextField('响应参数', blank=True, default='')
    status = models.CharField('状态', blank=True, max_length=100, default='1')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.id, self.service_id,
