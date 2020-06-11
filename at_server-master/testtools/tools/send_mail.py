# -*- coding: utf-8 -*-

import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart
import string
from email.header import Header  


def send_mail_core(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    mail_host="smtp.exmail.qq.com"
    mail_user="zendao@2345.com"    #用户名
    mail_pass="Zd@123"   #口令

    mail_postfix="2345.com"  #发件箱的后缀
    me="<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件

    msg['Subject'] = sub    #设置主题
    msg['From'] = "发布助手"  
    msg['To'] = to_list
    msg["Accept-Language"]="zh-CN"
    msg["Accept-Charset"]="ISO-8859-1,utf-8"

    to_list =string.splitfields(to_list, ",")

    try:  
        s = smtplib.SMTP()  
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list,msg.as_string())  #发送邮件
        s.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  

def send_mail(request):#mailto_list,sub,content): 
    mailto_list=request.GET.get("to")
    sub=request.GET.get("sub")
    content=request.GET.get("content")
    ret=[]
    for to in mailto_list.split(';'):
        if send_mail_core(to,sub,content):  
            ret.append([to,u'发送成功'])
        else:  
            ret.append([to,u'发送失败'])
    return HttpResponse(ret)

def send_mail_own(mailto_list,sub,content): 
    for to in mailto_list.split(';'):
        if send_mail_core(to,sub,content):  
            ret=to+u"---->发送成功"  
            print ret
        else:  
            ret=to+u"---->发送失败"
            print ret



# send_mail_core('chenc@2345.com,chengm@2345.com','中文','测试')