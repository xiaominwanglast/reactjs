# -*- coding: utf-8 -*-

# from __future__ import print_function

from jenkinsapi.jenkins import Jenkins
from send_mail import send_mail_core
import re

class Jenkins_Core():
    
    def __init__(self,jenkins_url,username,password):
        
        # jenkins = Jenkins('http://172.16.23.49:8001/jenkins','chengm','123456')
        self.jenkins = Jenkins(jenkins_url,username,password)
    
    def build_job(self,job_name,job_params):
        
        # 判断job是不是在运行
        job = self.jenkins[job_name]

        if  job.is_queued_or_running():
            return -99,u'JOB正在运行中，请稍后再构建。',{"changelogs":[],"build_info":[]}


        # 构建job
        qi = job.invoke(build_params=job_params)
        if  job.is_queued() or job.is_running():
            qi.block_until_complete()

        build = qi.get_build()

        # 失败则返回错误日志

        logs=build.get_console()
        p = re.compile(r'CAPACITY]===>(.*?)channel started')
        m = p.search(logs)
        logs=logs.replace(m.group(),"").replace("\n","<br>")

        changelogs=build.get_changeset_items()
        changeset=[]
        if changelogs:
            for change in changelogs:
                changeset.append(change["date"]+":"+change["author"]["fullName"]+"=====>"+change["msg"])
        # changelogs= "<br>".join(changeset)

        info=build.get_actions()

        build_info=[]
        build_info.append(u"git地址=====>"+info["remoteUrls"][0])
        build_info.append(u"git分支=====>"+info["lastBuiltRevision"]["branch"][0]["name"])
        build_info.append(u"Commit =====>"+info["lastBuiltRevision"]["branch"][0]["SHA1"])

        content={"changelogs":changeset,"build_info":build_info}

        if build.is_good():
            # send_mail_core(maillist,'2楼-test1-ao重新发布成功',content)
            return 1,u'2楼-test1-ao重新发布成功',content

        # 成功就返回changelog
        else:
            # send_mail_core(maillist,'2楼-test1-ao重新发布失败',logs)
            return 0,u'2楼-test1-ao重新发布失败',content
        


if __name__ == '__main__':
    JK=Jenkins_Core('http://172.16.23.49:8001/jenkins','testteam','123456')
    job_name='micro_ao'
    job_params = {'branch': 'origin/master', 'machine': 'test1'}
    JK.build_job(job_name,job_params)
    # http://127.0.0.1:9999/publish_server/?job_name=micro_ao&job_params={"branch": "origin/master", "machine": "test1"}