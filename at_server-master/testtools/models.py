from django.db import models
from datetime import datetime

class TestTools(models.Model):
    """ 进件流程操作记录 """
    id = models.AutoField(primary_key=True)
    user_name = models.CharField('操作人', max_length=20, blank=True, default='')
    project = models.CharField('操作项目', max_length=20, blank=True, default='')
    option = models.CharField('操作选项', max_length=20, blank=True, default='')
    env = models.CharField('环境', max_length=20, blank=True, default='')
    product = models.CharField('产品', max_length=20, blank=True, default='')
    phone = models.CharField('手机号', max_length=20, blank=True, default='')
    operate_time = models.DateTimeField('操作时间',auto_now_add=True)
    # operate_time = models.DateTimeField('操作时间', null=True, blank=True, default=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))

    status = models.CharField('状态', blank=True, max_length=100, default='0')
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')
    version = models.CharField('当前版本号', blank=True, max_length=1, default='3')

    def __str__(self):
        return self.id, self.user_name

class CreateAccount(models.Model):
    """ 造号操作记录 """
    id = models.AutoField(primary_key=True)
    serial_num = models.CharField('流水号', max_length=20, blank=True, default='')
    user_name = models.CharField('操作人', max_length=20, blank=True, default='')
    env = models.CharField('环境', max_length=20, blank=True, default='')
    product = models.CharField('产品', max_length=20, blank=True, default='')
    phone = models.CharField('手机号', max_length=20, blank=True, default='')
    uid =  models.CharField('userId', max_length=50, blank=True, default='')
    cid = models.CharField('customerId', max_length=100, blank=True, default='')
    bankcard = models.CharField('银行卡', max_length=20, blank=True, default='')
    name = models.CharField('姓名', max_length=20, blank=True, default='')
    idcard = models.CharField('身份证号', max_length=20, blank=True, default='')
    current_step = models.CharField('当前步骤', max_length=20, blank=True, default='')
    # operate_time = models.DateTimeField('操作时间', null=True, blank=True, default=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
    status = models.CharField('步骤状态', blank=True, max_length=100, default='')
    url = models.CharField('url', blank=True, max_length=100, default='')
    errorinfo = models.TextField('失败原因', blank=True, default='')
    operate_time = models.DateTimeField('操作时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')
    version = models.CharField('当前版本号', blank=True, max_length=1, default='3')

class UserDb(models.Model):
    """ 数据库配置 """
    id = models.AutoField(primary_key=True)
    host = models.CharField('数据库host', max_length=20, blank=True, default='')
    dbuser = models.CharField('用户名', max_length=20, blank=True, default='')
    password = models.CharField('密码', max_length=20, blank=True, default='')
    port = models.IntegerField('端口号', blank=True, default=0)
    env = models.CharField('环境', max_length=20, blank=True, default='')
    status = models.CharField('状态', blank=True, max_length=100, default='0')
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')
    version = models.CharField('当前版本号', blank=True, max_length=1, default='3')

class ProductConfig(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('产品名称', max_length=20, blank=True, default='')
    pid = models.CharField('pid', max_length=20, blank=True, default='')
    terminalId = models.CharField('terminalId', max_length=20, blank=True, default='')
    host = models.CharField('host', max_length=100, blank=True, default='')
    interface = models.TextField('接口信息', blank=True, default='')
    bundleId = models.CharField('bundleId', max_length=50, blank=True, default='')
    version = models.CharField('version', max_length=20, blank=True, default='')
    type = models.CharField('type', max_length=20, blank=True, default='')
    purpose = models.CharField('purpose', max_length=20, blank=True, default='')
    fundId = models.CharField('fundId', max_length=20, blank=True, default='')
    period = models.IntegerField('period',  blank=True, default=0)
    status = models.CharField('状态', blank=True, max_length=100, default='0')
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

class BankBin(models.Model):
    id = models.AutoField(primary_key=True)
    bankname = models.CharField('银行名称', max_length=20, blank=True, default='')
    bin = models.CharField('卡bin', max_length=20, blank=True, default='')
    type = models.CharField('卡类型', max_length=20, blank=True, default='储蓄卡')
    banknum = models.IntegerField('卡位数', blank=True, default=18)
    status = models.CharField('状态', blank=True, max_length=100, default='0')
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')
    version = models.CharField('当前版本号', blank=True, max_length=1, default='3')

class IdcardInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('姓名', max_length=20, blank=True, default='')
    username = models.CharField('操作人', max_length=20, blank=True, default='')
    gander = models.CharField('性别', max_length=20, blank=True, default='')
    idcard = models.CharField('身份证号', max_length=20, blank=True, default='')
    birthday_y = models.CharField('月', max_length=20, blank=True, default='')
    birthday_m = models.CharField('日', max_length=20, blank=True, default='')
    birthday_d = models.CharField('年', max_length=20, blank=True, default='')
    address_1 = models.CharField('地址1', max_length=20, blank=True, default='')
    address_2 = models.CharField('地址2', max_length=20, blank=True, default='')
    national = models.CharField('民族', max_length=20, blank=True, default='')
    phone = models.CharField('关联手机号', max_length=20, blank=True, default='')
    operate_time = models.DateTimeField('操作时间', auto_now_add=True)

class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.BigIntegerField('手机号',blank=True, default=0)
    env = models.CharField('环境', max_length=20, blank=True, default='')

class RedisDbInfo(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.CharField('数据库host', max_length=20, blank=True, default='')
    port = models.IntegerField('端口号', blank=True, default=0)
    password = models.CharField('密码', max_length=20, blank=True, default='')
    env = models.CharField('环境', max_length=20, blank=True, default='')
    status = models.CharField('状态', blank=True, max_length=100, default='0')
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')
    version = models.CharField('当前版本号', blank=True, max_length=1, default='3')
