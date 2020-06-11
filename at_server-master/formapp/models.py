from django.db import models


class Template(models.Model):
    """ 表单模板 """
    id = models.AutoField(primary_key=True)
    title = models.TextField('模板名称', blank=True, default='')
    header_data = models.TextField('表单模板字段设计内容', blank=True, default='[]')
    template_columns = models.TextField('列字段', blank=True, default='[]')
    template_data = models.TextField('表单内容', blank=True, default='[]')
    create_user = models.CharField('创建者', blank=True, max_length=100, default='')
    update_user = models.CharField('更新者', blank=True, max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class TemplateHistory(models.Model):
    """ 表单模板历史版本 """
    id = models.AutoField(primary_key=True)
    title = models.TextField('模板名称', blank=True, default='')
    header_data = models.TextField('表单模板字段设计内容', blank=True, default='[]')
    template_columns = models.TextField('列字段', blank=True, default='[]')
    template_data = models.TextField('表单内容', blank=True, default='[]')
    update_user = models.CharField('更新者', blank=True, max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    template_id = models.CharField('表单模板id', blank=True, max_length=10, default='')

    def __str__(self):
        return self.id


class Project(models.Model):
    """ 项目 """
    id = models.AutoField(primary_key=True)
    title = models.TextField('模板名称', blank=True, default='')
    group_name = models.CharField('所属组', blank=True, max_length=100, default='')
    master = models.CharField('负责人', blank=True, max_length=100, default='')
    status = models.CharField('状态', blank=True, max_length=100, default='待完成')
    create_user = models.CharField('创建者', blank=True, max_length=100, default='')
    update_user = models.CharField('更新者', blank=True, max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class Task(models.Model):
    """ 任务 """
    id = models.AutoField(primary_key=True)
    title = models.TextField('模板名称', blank=True, default='')
    project_id = models.CharField('项目id', blank=True, max_length=100, default='')
    master = models.CharField('负责人', blank=True, max_length=100, default='')
    template_id = models.CharField('模板id', blank=True, max_length=100, default='')
    template_columns = models.TextField('模板列字段', blank=True, default='[]')
    template_data = models.TextField('模板表单内容', blank=True, default='[]')
    status = models.CharField('状态', blank=True, max_length=100, default='待完成')
    create_user = models.CharField('创建者', blank=True, max_length=100, default='')
    update_user = models.CharField('更新者', blank=True, max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class Form(models.Model):
    """ 表单内容 """
    id = models.AutoField(primary_key=True)
    task_id = models.CharField('任务id', blank=True, max_length=100, default='')
    data = models.TextField('模板表单内容', blank=True, default='[]')
    update_user = models.CharField('更新者', blank=True, max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class FormLogs(models.Model):
    """ 表单修改记录 """
    id = models.AutoField(primary_key=True)
    form_id = models.CharField('formid', blank=True, max_length=100, default='')
    key = models.TextField('key', blank=True, default='')
    title = models.TextField('列名', blank=True, default='')
    old = models.TextField('原值', blank=True, default='')
    new = models.TextField('新值', blank=True, default='')
    update_user = models.CharField('更新者', blank=True, max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.id
