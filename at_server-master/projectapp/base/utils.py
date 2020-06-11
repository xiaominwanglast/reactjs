from rest_framework.response import Response
from django.conf  import settings
def try_except(default='系统异常'):
    def dec(func):
        def wrapper(self, *args, **kwargs):
            try:
                code = func(self, *args, **kwargs)
                return Response({"status": True, "message": "成功", "data": code})
            except Exception:
                # self.revive() #不用顾虑，直接调用原来的类的方法
                return Response({"status": False, "message": "失败", "data": default})
        return wrapper
    return dec

def retResponse(default='系统异常'):
    def dec(func):
        def wrapper(self, *args, **kwargs):
            code = func(self, *args, **kwargs)
            if code[0]:
                return Response({"status": True, "message": "成功", "data": code[1]})
            else:
                return Response({"status": False, "message": "失败", "data": default})
        return wrapper
    return dec

import jenkins


class Jenkins():
    def __init__(self):
        self.server = jenkins.Jenkins(settings.TEST_JENKINS_HOST, username=settings.TEST_JENKINS_USERNAME, password=settings.TEST_JENKINS_API_TOKEN)
        jobs = self.server.get_jobs()
        print(jobs)
