# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Reset_Logs(models.Model):
    """ 重置的账号历史 """
    id=models.AutoField(primary_key=True)
    username=models.CharField(u'用户登录名',max_length=100)
    displayname=models.CharField(u'真实姓名',max_length=100)
    account=models.TextField(u'账号',blank=True,default='')
    desc=models.TextField(u'描述',blank=True,default='')
    status=models.TextField(u'账号状态',blank=True,default='')
    create_time=models.DateTimeField(u'创建时间',auto_now_add = True)
    update_time=models.DateTimeField(u'更新时间',auto_now = True)

    def __unicode__(self):
        return self.id

class Account_Fake_Logs(models.Model):
    """ 重置的账号历史 """
    id=models.AutoField(primary_key=True)
    username=models.CharField(u'用户登录名',max_length=100)
    displayname=models.CharField(u'真实姓名',max_length=100)
    account=models.TextField(u'账号',blank=True,default='')
    desc=models.TextField(u'描述',blank=True,default='')
    status=models.TextField(u'账号状态',blank=True,default='')
    create_time=models.DateTimeField(u'创建时间',auto_now_add = True)
    update_time=models.DateTimeField(u'更新时间',auto_now = True)

    def __unicode__(self):
        return self.id

class Create_Cardid_Logs(models.Model):
    """ 伪造身份证号历史 """
    id=models.AutoField(primary_key=True)
    username=models.CharField(u'用户登录名',max_length=100)
    displayname=models.CharField(u'真实姓名',max_length=100)
    account=models.TextField(u'身份证号',blank=True,default='')
    desc=models.TextField(u'描述',blank=True,default='')
    status=models.TextField(u'账号状态',blank=True,default='')
    create_time=models.DateTimeField(u'创建时间',auto_now_add = True)
    update_time=models.DateTimeField(u'更新时间',auto_now = True)

    def __unicode__(self):
        return self.id
