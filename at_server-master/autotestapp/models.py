from django.db import models


class Project(models.Model):
    """ 项目 """
    id = models.AutoField(primary_key=True)
    name = models.TextField('名称', blank=True, default='')
    git = models.TextField('git地址', blank=True, default='')
    command = models.TextField('命令', blank=True, default='')
    project_code = models.CharField('项目代号', blank=True, max_length=100, default='')
    pid = models.CharField('pid', blank=True, max_length=10, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')


class TestSuite(models.Model):
    """ 测试用例表 """
    id = models.AutoField(primary_key=True)
    project_id = models.CharField('项目id', blank=True, max_length=10, default='')
    suite_name = models.TextField('suite名', blank=True, default='')
    case_name = models.TextField('case名', blank=True, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')


class TestResult(models.Model):
    """ 测试结果表 """
    id = models.AutoField(primary_key=True)
    project_id = models.CharField('项目id', blank=True, max_length=10, default='')
    name = models.TextField('名称', blank=True, default='')
    user = models.CharField('触发人', blank=True, max_length=100, default='')
    env = models.CharField('环境', blank=True, max_length=100, default='')
    count = models.CharField('执行用例总数', blank=True, max_length=100, default='')
    pass_count = models.CharField('成功数量', blank=True, max_length=100, default='')
    fail_count = models.CharField('失败数量', blank=True, max_length=100, default='')
    duration = models.CharField('执行时长', blank=True, max_length=100, default='')
    status = models.CharField('状态', blank=True, max_length=100, default='')
    report = models.TextField('报告地址', blank=True, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


class Overview(models.Model):
    """ 概况总览 """
    id = models.AutoField(primary_key=True)
    project_id = models.CharField('项目id', blank=True, max_length=10, default='')
    key = models.CharField('指标', blank=True, max_length=100, default='')
    date = models.CharField('时间', blank=True, max_length=100, default='')
    value = models.TextField('值', blank=True, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


class FactorCase(models.Model):
    """ 因子用例表 """
    id = models.AutoField(primary_key=True)
    factorName = models.CharField('因子名称', blank=True, max_length=100, default='')
    factorCase = models.CharField('因子测试用例', blank=True, max_length=100, default='')
    factorDesc = models.CharField('因子描述', blank=True, max_length=255, default='')
    factorType = models.CharField('因子类型', blank=True, max_length=100, default='')
    delete_flag = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)