from django.db import models


# Create your models here.
class StoryPlan(models.Model):
    """ 项目 """
    id = models.AutoField(primary_key=True)
    zentao_id = models.IntegerField('标题', blank=True, default=0)
    zentao_url = models.CharField('禅道链接', blank=True, max_length=200, default='')
    title = models.CharField('标题', blank=True, max_length=200, default='')
    product_id = models.CharField('产品id', blank=True, max_length=10, default='0')
    product_name = models.CharField('产品名称', blank=True, max_length=10, default='0')
    product_master = models.CharField('产品负责人', blank=True, max_length=20, default='')
    version_id = models.CharField('版本id', blank=True, max_length=10, default='0')
    version_master = models.CharField('版本负责人', blank=True, max_length=20, default='')
    status = models.CharField('状态', blank=True, max_length=20, default='')  # “未开始”，“进行中”，“已上线”
    zentao_status = models.CharField('需求状态', blank=True, max_length=20, default='')
    type = models.CharField('类型', blank=True, max_length=100, default='')
    plan_id = models.CharField('计划id', blank=True, max_length=10, default='0')
    extra = models.CharField('其他', blank=True, max_length=100, default='')
    update_num = models.IntegerField('更新次数', blank=True, default=0)
    zentao_create_time = models.DateTimeField('需求提出时间', blank=True, null=True)
    online_time = models.DateTimeField('上线时间', blank=True, null=True)
    plan_online_time = models.DateTimeField('计划上线时间', blank=True, null=True)
    join_users = models.TextField('参与人员', blank=True, default='')
    duration_days = models.IntegerField('周期天数', blank=True, default=0)  # 周期天数
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')


class DevStage(models.Model):
    """ 项目 """
    id = models.AutoField(primary_key=True)
    version_id = models.CharField('版本id', blank=True, max_length=10, default='0')
    server_name = models.CharField('服务名称', blank=True, max_length=50, default='')
    code_scan_name = models.CharField('代码扫描名称', blank=True, max_length=50, default='')
    server_name_key = models.CharField('服务名称key', blank=True, max_length=50, default='')
    git_branch = models.CharField('git分支', blank=True, max_length=50, default='')
    sonar_bugs = models.CharField('sonar_bugs', max_length=11, default='')
    sonar_bugs_std = models.CharField('sonar_std_bugs', max_length=11, default='')
    sonar_vulnerabilities = models.CharField('sonar_vulnerabilities', max_length=11, default='')
    sonar_vulnerabilities_std = models.CharField('sonar_std_vulnerabilities', max_length=11, default='')
    high_priority_warnings = models.CharField('high_priority_warnings', max_length=11, default='')
    high_priority_warnings_std = models.CharField('high_priority_warnings_std', max_length=11, default='')
    normal_priority_warnings = models.CharField('normal_priority_warnings', max_length=11, default='')
    normal_priority_warnings_std = models.CharField('normal_priority_warnings_std', max_length=11, default='')
    is_codereview = models.IntegerField('是否codereview', blank=True, default=0)  # 0否 1是
    person_codereview = models.CharField('codereview人', blank=True, max_length=50, default='')
    sonar_status = models.CharField('sonar执行状态', blank=True, max_length=50, default='')
    jenkins_job_num = models.CharField('jenkins-job编号', blank=True, max_length=5, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')


class Version(models.Model):
    """ 版本表 """
    id = models.AutoField(primary_key=True)
    title = models.CharField('版本标题', blank=True, max_length=200, default='')
    product_title = models.CharField('所属产品名', blank=True, max_length=100, default='0')

    master_name = models.CharField('版本负责人（项目经理）', blank=True, max_length=20, default='')
    product_users = models.TextField('产品人员', blank=True, default='')
    dev_users = models.TextField('开发人员', blank=True, default='')
    test_users = models.TextField('测试人员', blank=True, default='')

    story_publish_done_time = models.DateField('需求发布时间', blank=True, null=True)
    story_plan_done_time = models.DateField('排期完成时间', blank=True, null=True)

    design_start_time = models.DateField('开始设计时间', blank=True, null=True)
    dev_start_time = models.DateField('开始开发时间', blank=True, null=True)
    test_start_time = models.DateField('提测时间', blank=True, null=True)
    online_plan_time = models.DateField('计划上线时间', blank=True, null=True)

    design_done_time = models.DateField('设计完成时间', blank=True, null=True)
    dev_done_time = models.DateField('开发完成时间', blank=True, null=True)
    test_done_time = models.DateField('测试完成时间', blank=True, null=True)
    online_done_time = models.DateField('上线完成时间', blank=True, null=True)

    stage = models.IntegerField('当前阶段', blank=True,
                                default=2)  # 默认排期阶段（1-需求发布阶段；2-排期；3-开发设计阶段；4-开始开发；5-提测；6-上线中；7-上线完成）
    status = models.CharField('当前阶段的状态/描述', blank=True, max_length=200, default='进行中')

    extra = models.CharField('其他', blank=True, max_length=100, default='')

    create_user = models.CharField('创建人姓名', blank=True, max_length=20, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')


class VersionChangeHistory(models.Model):
    """ 版本变更记录表 """
    id = models.AutoField(primary_key=True)
    version_id = models.CharField('版本id', blank=True, max_length=10, default='0')
    change_content = models.TextField('变更内容', blank=True, default='')
    create_user = models.CharField('创建人姓名', blank=True, max_length=20, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)


class Project(models.Model):
    """ 项目表 """
    id = models.AutoField(primary_key=True)
    project_id = models.CharField('项目id', blank=True, max_length=10, default='')
    project_name = models.CharField('项目名称', blank=True, max_length=10, default='')
    project_master = models.CharField('项目负责人', blank=True, max_length=10, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')


class VersionDesignStageFile(models.Model):
    """版本设计阶段"""
    id = models.AutoField(primary_key=True)
    version_id = models.CharField('版本id', blank=True, max_length=10, default='')
    category_name = models.CharField('文件类目id', blank=True, max_length=20, default='')  # design  interface  database schedule testcase
    file_name = models.TextField('文档名字', blank=True, default='')
    type = models.CharField('文件类型', blank=True, max_length=2, default='2')  # 1 上传的文档 、2 需求链接
    path = models.TextField('文档路径', blank=True, default='')
    remarks = models.TextField('备注信息', blank=True, default='暂无')
    create_user = models.CharField('上传人姓名', blank=True, max_length=20, default='')
    create_time = models.DateTimeField('操作时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')

    def __str__(self):
        return self.id
