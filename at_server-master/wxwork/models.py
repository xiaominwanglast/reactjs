from django.db import models


class Message(models.Model):
    """ 企业微信消息记录 """
    id = models.AutoField(primary_key=True)
    receiver = models.TextField('收信者', blank=True, default='')
    title = models.TextField('标题', blank=True, default='')
    msg = models.TextField('消息内容', blank=True, default='')
    forward = models.TextField('跳转地址', blank=True, default='')
    result = models.CharField('发送结果', blank=True, max_length=50, default='')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.id
