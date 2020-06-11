from django.db import models


class TestTask(models.Model):
    """ 提测单 """
    id = models.AutoField(primary_key=True)

    title = models.TextField('标题', blank=True, default='')
    type = models.CharField('类型', blank=True, max_length=100, default='')
    system = models.CharField('系统', blank=True, max_length=100, default='')
    product_docs = models.TextField('需求文档', blank=True, default='')
    service_name = models.TextField('服务名称', blank=True, default='')
    service_branch = models.TextField('git分支', blank=True, default='')
    service_and_branch = models.TextField('服务与分支', blank=True, default='[]')
    sql_files = models.TextField('数据库修改附件', blank=True, default='[]')
    version_id = models.TextField('关联的版本ids', blank=True, default='[]')
    content = models.TextField('提测内容', blank=True, default='')
    notice = models.TextField('注意事项', blank=True, default='')
    performance = models.CharField('是否需要性能测试', blank=True, max_length=100, default='')
    performance_note = models.TextField('性能测试内容', blank=True, default='')
    apollo_config = models.TextField('阿波罗配置', blank=True, default='[]')

    product_users = models.CharField('需求方', blank=True, max_length=600, default='[]')
    dev_users = models.CharField('开发人员', blank=True, max_length=600, default='[]')
    test_users = models.CharField('测试人员', blank=True, max_length=600, default='[]')
    dev_team = models.CharField('开发团队', blank=True, max_length=600, default='[]')

    plan_submit_test_time = models.DateField('计划提测时间', null=True, blank=True)
    plan_online_time = models.DateField('计划上线时间', null=True, blank=True)
    real_submit_test_time = models.DateField('真正提测时间', null=True, blank=True)
    real_online_time = models.DateField('真正上线时间', null=True, blank=True)

    status = models.CharField('状态', blank=True, max_length=100, default='')
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')
    version = models.CharField('当前版本号', blank=True, max_length=1, default='4')

    def __str__(self):
        return self.id, self.title


class TestTaskHistory(models.Model):
    """ 提测单历史版本 """
    id = models.AutoField(primary_key=True)

    title = models.TextField('标题', blank=True, default='')
    type = models.CharField('类型', blank=True, max_length=100, default='')
    system = models.CharField('系统', blank=True, max_length=100, default='')
    product_docs = models.TextField('需求文档', blank=True, default='')
    service_name = models.TextField('服务名称', blank=True, default='')
    service_branch = models.TextField('git分支', blank=True, default='')
    service_and_branch = models.TextField('服务与分支', blank=True, default='[]')
    sql_files = models.TextField('数据库修改附件', blank=True, default='[]')
    version_id = models.TextField('关联的版本ids', blank=True, default='[]')
    content = models.TextField('提测内容', blank=True, default='')
    notice = models.TextField('注意事项', blank=True, default='')
    performance = models.CharField('是否需要性能测试', blank=True, max_length=100, default='')
    performance_note = models.TextField('性能测试内容', blank=True, default='')
    apollo_config = models.TextField('阿波罗配置', blank=True, default='[]')

    product_users = models.CharField('需求方', blank=True, max_length=600, default='[]')
    dev_users = models.CharField('开发人员', blank=True, max_length=600, default='[]')
    test_users = models.CharField('测试人员', blank=True, max_length=600, default='[]')
    dev_team = models.CharField('开发团队', blank=True, max_length=600, default='[]')

    plan_submit_test_time = models.DateField('计划提测时间', null=True, blank=True)
    plan_online_time = models.DateField('计划上线时间', null=True, blank=True)
    real_submit_test_time = models.DateField('真正提测时间', null=True, blank=True)
    real_online_time = models.DateField('真正上线时间', null=True, blank=True)

    status = models.CharField('状态', blank=True, max_length=100, default='')
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')
    version = models.CharField('当前版本号', blank=True, max_length=1, default='4')


class TestTaskOperation(models.Model):
    """ 提测单操作记录表 """
    id = models.AutoField(primary_key=True)
    username = models.CharField('用户登录名', max_length=100)
    realname = models.CharField('真实姓名', max_length=100, blank=True, )
    testtask_id = models.CharField('关联的提测单id', max_length=10, blank=True, )
    change_fields = models.TextField('修改的数据列', blank=True, default='[]')
    old_content = models.TextField('旧值', blank=True, default='[]')
    new_content = models.TextField('新值', blank=True, default='[]')
    current_version = models.CharField('TestTaskHistory中的id', blank=True, max_length=10, default='')
    change_action = models.TextField('操作记录的简单描述', blank=True, default='')
    create_time = models.DateTimeField('操作时间', auto_now_add=True)


class OnlineOrder(models.Model):
    """ 上线单 """
    id = models.AutoField(primary_key=True)

    title = models.TextField('标题', blank=True, default='')
    type = models.CharField('类型', blank=True, max_length=100, default='')
    system = models.CharField('所属系统', blank=True, max_length=100, default='')
    testtask = models.TextField('提测单', blank=True, default='[]')
    users = models.TextField('相关人员', blank=True, default='[]')
    content = models.TextField('上线内容', blank=True, default='')
    template = models.CharField('模板', blank=True, max_length=100, default='')
    dev_team = models.TextField('开发团队', blank=True, default='[]')
    product_users = models.CharField('需求方', blank=True, max_length=600, default='[]')
    dev_users = models.CharField('开发人员', blank=True, max_length=600, default='[]')
    test_users = models.CharField('测试人员', blank=True, max_length=600, default='[]')
    status = models.CharField('状态', blank=True, max_length=100, default='')
    real_online_time = models.DateTimeField('真正上线时间', null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id, self.title


class OnlineOrderFlow(models.Model):
    """ 上线流程 """
    id = models.AutoField(primary_key=True)
    onlineorder_id = models.CharField('上线单id', blank=True, max_length=100, default='')
    checkpoint = models.TextField('检查项', blank=True, default='')
    master = models.CharField('负责人', blank=True, max_length=100, default='')
    status = models.CharField('状态', blank=True, max_length=100, default='')
    note = models.TextField('备注', blank=True, default='')
    check_time = models.DateTimeField('检查时间', blank=True, null=True, default=None)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class OnlineOrderChecklist(models.Model):
    """ 上线checklist """
    id = models.AutoField(primary_key=True)
    onlineorderflow_id = models.CharField('上线流程id', blank=True, max_length=100, default='')
    type = models.TextField('类型', blank=True, default='')
    checkpoint1 = models.TextField('检查项', blank=True, default='')
    checkpoint2 = models.TextField('检查项', blank=True, default='')
    master = models.CharField('负责人', blank=True, max_length=100, default='')
    status = models.CharField('状态', blank=True, max_length=100, default='')
    note = models.TextField('备注', blank=True, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class OnlineOrderOperation(models.Model):
    """ 上线单操作记录表 """
    id = models.AutoField(primary_key=True)
    username = models.CharField('用户登录名', max_length=100)
    realname = models.CharField('真实姓名', max_length=100, blank=True, )
    onlineorder_id = models.CharField('关联的上线单id', max_length=10, blank=True, )
    change_fields = models.TextField('修改的数据列', blank=True, default='[]')
    old_content = models.TextField('旧值', blank=True, default='[]')
    new_content = models.TextField('新值', blank=True, default='[]')
    change_action = models.TextField('操作记录的简单描述', blank=True, default='')
    create_time = models.DateTimeField('操作时间', auto_now_add=True)
