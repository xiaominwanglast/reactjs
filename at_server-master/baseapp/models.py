from django.db import models


class Files(models.Model):
    """ 附件信息表 """
    id = models.AutoField(primary_key=True)
    user_id = models.CharField('用户id', max_length=10, blank=True, )
    file_name = models.CharField('文件名', max_length=200, blank=True, )
    file_size = models.CharField('文件大小', max_length=100, blank=True, )
    file_type = models.CharField('文件后缀', max_length=100, blank=True, )
    content_type = models.CharField('内容类型', max_length=100, blank=True, )
    file_path = models.TextField('文件位置', blank=True, default='')
    status = models.CharField('状态 1有效 0删除', blank=True, max_length=100, default='1')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.id


# class Departments(models.Model):
#     """ 部门表 """
#     id = models.AutoField(primary_key=True)
#     department_id = models.CharField('企业微信的部门id', max_length=10, blank=True, )
#     parent_id = models.CharField('父亲部门id', max_length=10, blank=True, )
#     name = models.CharField('部门名称', max_length=100, blank=True, )
#     order = models.CharField('在父部门中的次序值', max_length=10, blank=True, )
#     version = models.CharField('状态 1有效 0无效', blank=True, max_length=10, default='v1')
#     status = models.CharField('状态 1有效 0无效', blank=True, max_length=10, default='1')
#
#     def __str__(self):
#         return self.id

class Departments(models.Model):
    """ 部门表 """
    id = models.AutoField(primary_key=True)
    group = models.CharField('事业群', max_length=100, blank=True, )
    department_list = models.TextField('文件位置', blank=True, default='')
    name = models.CharField('部门名称', max_length=100, blank=True, )
    version = models.CharField('状态 1有效 0无效', blank=True, max_length=10, default='v1')
    leaders = models.TextField('部门负责人', blank=True, default='[]')
    status = models.CharField('状态 1有效 0无效', blank=True, max_length=10, default='1')

    """
        数据来源可以在user表内容完整后，进行如下操作
        SELECT DISTINCT department_list FROM userapp_users ORDER BY department_list;

        UPDATE baseapp_departments set name = REPLACE(REPLACE(REPLACE(department_list,'["',''),'"]',''),'", "','-');

        UPDATE baseapp_departments set `group` = substring_index(name, '-', 1);
    """

    def __str__(self):
        return self.id


class Services(models.Model):
    """ 服务表 """
    id = models.AutoField(primary_key=True)
    department_id = models.CharField('关联部门的department_id', max_length=10, blank=True, )
    name = models.CharField('部门名称', max_length=100, blank=True, )
    status = models.CharField('状态 1有效 0无效', blank=True, max_length=10, default='1')
    product_users = models.TextField('产品人员', blank=True, default='')
    dev_users = models.TextField('开发人员', blank=True, default='')
    test_users = models.TextField('测试人员', blank=True, default='')

    def __str__(self):
        return self.id


class NewServices(models.Model):
    """ 基础数据-Jenkins-Job/PMD/Sonar 的对应关系 """
    id = models.AutoField(primary_key=True)
    view_name = models.CharField('所属部门或项目', max_length=100, blank=True, )
    job_name = models.CharField('服务名', max_length=100, blank=True, )
    pmd_name = models.CharField('pmd的名字', max_length=100, blank=True, )
    high_priority_warnings = models.CharField('指标1', max_length=100, blank=True, default='9999999999')
    normal_priority_warnings = models.CharField('指标2', max_length=100, blank=True, default='9999999999')
    sonar_name = models.CharField('sonar名称', max_length=100, blank=True, )
    sonar_standard_bugs = models.CharField('bugs', max_length=100, blank=True, default='9999999999')
    sonar_standard_vulnerabilities = models.CharField('vulnerabilities', max_length=100, blank=True,
                                                      default='9999999999')
    sonar_standard_ncloc = models.CharField('ncloc', max_length=100, blank=True, default='9999999999')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    delete = models.CharField('删除标志 1存在 0删除', blank=True, max_length=1, default='1')
    jar_name = models.CharField('jar_name', max_length=500, blank=True, default='[]')
