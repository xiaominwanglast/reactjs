from django.db import models


class DBInfo(models.Model):
    """ 数据库信息 """
    id = models.AutoField(primary_key=True)

    database = models.CharField('数据库名', blank=True, max_length=100, default='')
    type = models.CharField('类型(mysql/mongo/redis)', blank=True, max_length=100, default='')
    config = models.TextField('数据库连接信息', blank=True, default='{}')
    status = models.CharField('启用状态', blank=True, max_length=100, default='1')

    def __str__(self):
        return self.id


class DBChange(models.Model):
    """ 数据库变更内容 """
    id = models.AutoField(primary_key=True)
    dbinfo_id = models.CharField('数据库信息表id', blank=True, max_length=10, default='')
    database = models.CharField('数据库名', blank=True, max_length=100, default='')
    type = models.CharField('类型(mysql/mongo/redis)', blank=True, max_length=100, default='')
    content = models.TextField('内容', blank=True, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    update_type=models.CharField('提审类型', blank=True, max_length=200, default='')
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class DBChangeHistory(models.Model):
    """ 数据库变更内容的历史表 """
    id = models.AutoField(primary_key=True)
    dbchange_id = models.CharField('数据库信息表id', blank=True, max_length=10, default='')
    content = models.TextField('内容', blank=True, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class DBChangeOrder(models.Model):
    """ 数据库变更单 """
    id = models.AutoField(primary_key=True)
    title = models.TextField('标题', blank=True, default='')
    submit_user = models.CharField('真实姓名', max_length=100, blank=True, default='')
    dev_team = models.TextField('所属团队', blank=True, default='[]')
    check_users = models.TextField('审核人员', blank=True, default='[]')
    cc_users = models.TextField('抄送人员', blank=True, default='[]')
    note = models.TextField('备注', blank=True, default='[]')
    dbchange_ids = models.TextField('数据库变更内容ids', blank=True, default='[]')
    status = models.CharField('状态', blank=True, max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    execute_status = models.TextField('执行情况', blank=True, default='{}')
    check_time = models.DateTimeField('审核日期', null=True, blank=True)
    online_time = models.DateTimeField('上线日期', null=True, blank=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class DBChangeAuditRecord(models.Model):
    """ 数据库变更单审核记录表 """
    id = models.AutoField(primary_key=True)
    dbchangeorder_id = models.CharField('数据库变更单id', blank=True, max_length=10, default='')
    username = models.CharField('用户登录名', max_length=100, blank=True, )
    realname = models.CharField('真实姓名', max_length=100, blank=True, )
    content = models.TextField('内容', blank=True, default='')
    old_dbchangehistory_id = models.CharField('历史记录id', max_length=100, blank=True, default='[]')
    new_dbchangehistory_id = models.CharField('当前记录id', max_length=100, blank=True, default='[]')
    status = models.CharField('状态', blank=True, max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id


class DBChangeNotice(models.Model):
    """ 数据库变更通知表 """
    id = models.AutoField(primary_key=True)
    dbchangeorder_id = models.CharField('数据库变更单id', blank=True, max_length=10, default='')
    content = models.TextField('内容', blank=True, default='[]')
    notice_date = models.DateField('日期', null=True, blank=True)
    status = models.CharField('状态', blank=True, max_length=100, default='1')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.id


class DBExecuteRecordDetail(models.Model):
    """ 数据库执行记录表 """
    id = models.AutoField(primary_key=True)
    detail_id=models.CharField('detail表id', blank=False, max_length=10)
    order_id = models.CharField('order_id', max_length=10,blank=False)
    env = models.CharField('环境', max_length=20, blank=False)
    database = models.CharField('数据库名', blank=False, max_length=100)
    dbchangeorder_id = models.CharField('数据库变更单id', blank=True, max_length=10, default='')
    result = models.CharField('执行结果 1成功 0失败',blank=True,default='',max_length=10)
    sql_item = models.TextField('失败的sql', blank=True, default='')
    error_info = models.CharField('错误信息',blank=True,default='',max_length=1000)
    type = models.CharField('类型(mysql/mongo/redis)', blank=True, max_length=100, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.id


class DBExecuteRecord(models.Model):
    """ 数据库执行记录表 """
    id = models.AutoField(primary_key=True)
    order_id = models.CharField('order_id', max_length=10,blank=False)
    env = models.CharField('环境', max_length=20, blank=False)
    dbchangeorder_id = models.CharField('数据库变更单id', blank=True, max_length=10, default='')
    result = models.CharField('执行结果 1成功 0失败',blank=True,default='',max_length=10)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    executor = models.CharField('执行人', blank=False, max_length=20)

    def __str__(self):
        return self.id