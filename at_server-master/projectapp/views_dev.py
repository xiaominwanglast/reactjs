import requests, re, datetime, json, time, threading
from rest_framework import generics, views
from projectapp.base.utils import *
from projectapp.models import DevStage
from baseapp.models import NewServices
from projectapp.serializers import *
from baseapp.sonar import Sonar
from django.conf import settings
from baseapp.jenkins import Jenkins as jk


def recordLog(temp, changecode, user,  version_id):
    data = temp
    data['change_content'] = changecode
    data['create_user'] = user
    data['version_id'] = version_id
    create = CreateVersionHistorySerializerParam(data=data)
    if create.is_valid():
        create.save()

class StartSonar(generics.GenericAPIView):
    """
        启动sonar
    """
    serializer_class = IdSerializerParam

    @retResponse()
    def post(self, request):
        serializer = IdSerializerParam(data=request.data)
        if serializer.is_valid():
            data = serializer.initial_data
            obj = DevStage.objects.get(id=data.get('id'))
            jenkins = Jenkins()
            jenkins.server.build_job(obj.code_scan_name, {'BRANCH_NAME': obj.git_branch})
            num = jenkins.server.get_job_info(obj.code_scan_name)['nextBuildNumber']
            print(num)
            data = {
                'sonar_status': '进行中',
                'jenkins_job_num':num
            }
            serializer = DevStageSerializerParam(obj, data=data)
            if serializer.is_valid():
                serializer.save()
            recordLog(data, "对服务{}及分支{}进行了sonar和pmd扫描".format(obj.server_name, obj.git_branch), request.session['user']['realname'],obj.version_id)
            return True,'启动sonar成功'
        else:
            return False,'启动sonar失败'

class StartServer(generics.GenericAPIView):
    """
        启动sonar
    """
    serializer_class = StartServerSerializerParam

    @retResponse()
    def post(self, request):
        serializer = StartServerSerializerParam(data=request.data)
        if serializer.is_valid():
            data = serializer.initial_data
            server_name = data.get('server_name')
            git_branch = data.get('git_branch')
            env = data.get('env')
            jenkins = Jenkins()
            jenkins.server.build_job(server_name, {'BRANCH_NAME': git_branch, 'test_env':env})
            return True,'服务启动成功'
        else:
            return False,serializer.errors


class CreateServerQL(generics.GenericAPIView):
    """
        创建服务质量
    """
    serializer_class = DevStageParamsSerializerParam
    @retResponse()
    def post(self, request):
        serializer = DevStageParamsSerializerParam(data=request.data)
        if serializer.is_valid():
            data = serializer.initial_data
            server_name = data.get('server_name')
            git_branch = data.get('git_branch')
            obj = NewServices.objects.get(job_name=server_name)
            # print(sonar_name_key.sonar_name)
            # print(sonar_name_key.values('sonar_name')[0]['sonar_name'])
            temp = {
                'code_scan_name': obj.pmd_name,
                'server_name': server_name,
                'git_branch': git_branch,
                'server_name_key': obj.sonar_name,
                'version_id':data.get('version_id'),
                'sonar_status':'未执行'
            }
            print(temp)
            serializer = DevStageSerializerParam(data=temp)
            if serializer.is_valid():
                serializer.save()
                recordLog(data, "关联了服务{}及分支{}".format(server_name, git_branch), request.session['user']['realname'], data.get('version_id'))
                return True,'服务添加成功'
            else:
                return False,serializer.errors

        else:
            return serializer.errors


class SonarCode(views.APIView):
    """
        接收sonar数据
    """
    # serializer_class = DevStageSerializerParam
    @retResponse()
    def post(self, request):
        print(request.data)
        server_name_key = request.data['project']['key']
        # git_branch = 'origin/' + request.data['branch']['name']
        value = Sonar.get_sonar_result(server_name_key, settings.TEST_SONAR_HOST)
        print(value)
        self.obj = DevStage.objects.filter(server_name_key=server_name_key, sonar_status='进行中').order_by('-id')
        print(333, self.obj[0].jenkins_job_num)
        self.sonar_standard_values = NewServices.objects.get(sonar_name=server_name_key)

        self.data = {
            'sonar_bugs': value['bugs'],
            'sonar_vulnerabilities': value['vulnerabilities'],
            'sonar_bugs_std':self.sonar_standard_values.sonar_standard_bugs,
            'sonar_vulnerabilities_std': self.sonar_standard_values.sonar_standard_vulnerabilities,
        }
        self.obj.update(**self.data)
        print('sonar更新成功')
        threading.Thread(target=self.getPmdValue,args=()).start()
        return True,'接收成功'

    def getPmdValue(self):
        print('查询pmdinfo' ,self.obj[0].jenkins_job_num,  self.obj[0].code_scan_name)
        for i in range(1, 100):
            # print(i, self.obj[0].jenkins_job_num, self.obj[0].code_scan_name)
            jkinfo = jk.get_pmd_jobnum_status_test(self.obj[0].jenkins_job_num,self.obj[0].code_scan_name)
            try:
                if jkinfo[1] == False:
                    if jkinfo[0] == 'FAILURE':
                        self.data['sonar_status'] = '已完成-失败'
                        print('pmd更新失败')
                        self.obj.update(**self.data)
                        return
                    else:
                        ret = jk.get_pmd_jobnum_result_test(self.obj[0].jenkins_job_num, self.obj[0].code_scan_name)
                        print(ret)
                        if ret:
                            self.data['high_priority_warnings'] = ret.get('numberOfHighPriorityWarnings')
                            self.data['high_priority_warnings_std'] = self.sonar_standard_values.high_priority_warnings
                            self.data['normal_priority_warnings'] = ret.get('numberOfNormalPriorityWarnings')
                            self.data['normal_priority_warnings_std'] = self.sonar_standard_values.normal_priority_warnings
                            self.data['sonar_status'] = '已完成'
                            print('pmd更新成功')
                            self.obj.update(**self.data)
                            return
                time.sleep(10)
            except:
                time.sleep(10)

        self.data['sonar_status'] = '已完成-失败'
        self.obj.update(**self.data)


class DevelopInfo(views.APIView):
    """
        查看版本服务信息
    """
    # serializer_class = ServerInfoSerializerParam
    @retResponse()
    def post(self, request, version_id):
        print(version_id)
        obj = DevStage.objects.filter(version_id=version_id, delete=1)
        serializer = DevStageSerializerParam(obj, many=True)
        return True,serializer.data

class CodeReview(generics.GenericAPIView):
    """
            确认codereview
        """
    serializer_class = IdSerializerParam

    @retResponse()
    def put(self, request):
        obj = DevStage.objects.get(id=request.data['id'])
        data = {
            'person_codereview':request.session['user'].get('realname')
        }
        serializer = DevStageSerializerParam(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            recordLog(data, "对服务{}及分支{}进行了codereview".format(obj.server_name, obj.git_branch), request.session['user']['realname'], obj.version_id)
            return True,'修改成功'
        else:
            return False,serializer.errors

class DelServer(generics.GenericAPIView):
    """
               删除添加服务
           """
    serializer_class = IdSerializerParam

    @try_except()
    def delete(self, request):
        data = request.data
        obj = DevStage.objects.get(id=data['id'])
        data = {
            'delete': 0,
        }
        serializer = DevStageSerializerParam(obj, data=data)
        if serializer.is_valid():
            serializer.save()

        recordLog(data, "取消了对服务{}及分支{}的关联".format(obj.server_name, obj.git_branch), request.session['user']['realname'], obj.version_id)
        return True,'删除成功'
