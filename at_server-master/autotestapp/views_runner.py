
import os,threading,time
from autotestapp.views_report import *
from django.conf import settings


class Rfrunner(generics.GenericAPIView):
    '''
    执行用例
    '''
    serializer_class = rfrunnerSerializerParam
    def post(self, request, project_id):
        self.env = request.data.get('env')
        print('project_id=',project_id)
        tt = Project.objects.filter(id=project_id).values('project_code')
        project_code = tt[0]['project_code']
        self.log_path = settings.LOGPATH + project_code
        self.code_path = settings.CODEPATH + project_code
        casename = self.getCasename(request.data.get('casename'))
        suitename = self.getSuitename(request.data.get('suitename'))
        threading.Thread(target=self.runCase,args=(request, project_id, project_code, casename, suitename)).start()
        return Response({"status": True, "message": "发起执行成功", "data": ''})

    def runCase(self, request, project_id, project_code, casename, suitename):
        timestamp = int(time.time())
        path = '{}/{}'.format(self.log_path, timestamp)
        print(path)
        cmd = 'docker exec rfrunner-docker pybot -v ENV:{} -d {} {} {} {}'.format(self.env, path, casename, suitename,self.code_path)
        print(cmd)
        request.data['project_id'] = project_id
        if request.data.get('casename'):
            if len(request.data.get('casename')) > 1:
                request.data['name'] = request.data.get('casename')[0] + ' 等Case'
            else:
                request.data['name'] = request.data.get('casename')[0]
        else:
            if len(request.data.get('suitename')) > 1:
                request.data['name'] = request.data.get('suitename')[0] + '等Suite'
            else:
                request.data['name'] = request.data.get('suitename')[0]
        print(request.data['name'])
        request.data['user'] = request.session['user'].get('realname')
        tt = AutoTestReportSaveObject().post(request)
        print(tt.data)
        print(self.isContainer())
        if self.isContainer():
            request.data['report'] = self.log_path + '/' + str(timestamp) + '/output.xml'
        else:
            request.data['report'] = settings.LOCALLOGPATH + project_code + '/' + str(timestamp) + '/output.xml'
        print('---',request.data['report'])
        os.system(cmd)
        print('---开始调用解析日志---')
        AutoTestReportModifyParamObject().put(request, tt.data['data']['id'])


    def getCasename(self,caseTemp):
        casename = ''
        if caseTemp:
            if isinstance(caseTemp, list):
                for i in caseTemp:
                    casename = casename + ' -t ' + i
            else:
                casename = '-t ' + caseTemp
        else:
            casename = ''
        return casename.replace('(','\(').replace(')','\)').replace('&','\&')

    def getSuitename(self,suiteTemp):
        suitename = ''
        if isinstance(suiteTemp, list):
            for i in suiteTemp:
                suitename = suitename + ' -s '+ i
        else:
            suitename = '-s ' + suiteTemp
        return suitename

    def isContainer(self):
        from subprocess import getoutput
        output = getoutput('fdisk -l')
        return False if output else True
