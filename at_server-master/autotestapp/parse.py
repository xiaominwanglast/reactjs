import sys,json,os,time
import random,threading
from subprocess import getoutput
from rest_framework import generics,views
from rest_framework.response import Response
from rest_framework.request import Request
from autotestapp.serializers import *
from autotestapp.models import TestSuite,Project,Overview
from robot.api import TestData
from django.conf import settings
from autotestapp.views_factor import FactorCaseSaveObject

class parseSuite(generics.GenericAPIView):
    '''
        解析Suite文件
    '''
    serializer_class = pathSerializerParam
    def post(self,request, project_id):
        # serializer = pathSerializerParam(data=request.data)
        if project_id:
            # data = serializer.validated_data
            self.project_id = project_id
            type =  request.query_params.get('type')
            path = settings.CODEPATH if self.isContainer() else settings.LOCALCODEPATH
            tt = Project.objects.filter(id=self.project_id).values('project_code','git')
            projectpath = path + tt[0]['project_code']
            if os.path.exists(projectpath):
                cmd = 'cd ' + projectpath + ' && git pull'
                output = getoutput(cmd)
                # if 'Already up to date' in output:
                #     return Response({"status": True, "message": "成功", "data": '未发生变化，无需更新'})
            else:
                cmd = 'cd ' + path + ' && git clone ' + tt[0]['git']
                getoutput(cmd)

            currentMonth = self.currentMonth()
            lastMonth = self.lastMonth(int(currentMonth))

            if type:
                FactorCaseSaveObject().get(request)
                currentProjectCaseNum = FactorCase.objects.all().count()

                #记录用例数
                self.saveKeyValue(self.project_id, 'count', currentMonth, currentProjectCaseNum)
                caseTotalNum = TestSuite.objects.all().count() + currentProjectCaseNum
                self.saveKeyValue('0', 'count', currentMonth, caseTotalNum)

            else:
                self.delName()
                print('---path',projectpath)
                suite = TestData(source=projectpath)
                currentProjectCaseNum = self.getName(suite,suite.name)
                print('----- : ',currentProjectCaseNum)

                #记录用例数
                self.saveKeyValue(self.project_id, 'count', currentMonth, currentProjectCaseNum)
                caseTotalNum = TestSuite.objects.all().count()
                self.saveKeyValue('0', 'count', currentMonth, caseTotalNum)

            #记录用例增减数
            print(self.project_id, currentMonth, lastMonth)
            try:
                lastMonthProjectCaseNum = Overview.objects.filter(project_id=str(self.project_id), key='count', date=lastMonth).values('value')[0]['value']
            except:
                lastMonthProjectCaseNum = 0

            try:
                lastMonthAllCaseNum = Overview.objects.filter(project_id='0', key='count', date=lastMonth).values('value')[0]['value']
            except:
                lastMonthAllCaseNum = 0

            print(lastMonthProjectCaseNum,lastMonthAllCaseNum)
            self.saveKeyValue(self.project_id, 'addnum', currentMonth, str(int(currentProjectCaseNum) - int(lastMonthProjectCaseNum)))
            self.saveKeyValue('0', 'addnum', currentMonth, str(int(caseTotalNum) - int(lastMonthAllCaseNum)))

            return Response({"status": True, "message": "成功", "data": ''})
        else:
            return Response({"status": False, "message": "失败", "data": '参数错误'})

    def isContainer(self):
        from subprocess import getoutput
        output = getoutput('fdisk -l')
        return False if output else True

    def getName(self, suite, suiteName, count=0):
        if suite.testcase_table:
            print('Suite:', suiteName)
            count += len(suite.testcase_table)
            for test in suite.testcase_table:
                print('-', test.name)
                TestSuite(suite_name=suiteName, case_name=test.name, project_id=self.project_id).save()
        for child in suite.children:
            count = self.getName(child, suiteName + '.' + child.name, count)
        return count

    def delName(self):
        TestSuite.objects.filter(project_id=self.project_id).delete()

    def currentMonth(self):
        return time.strftime("%Y%m", time.localtime())

    def lastMonth(self, curMonth):
        month = curMonth % 100
        if month == 1:
            return str((int(str(curMonth)[:4]) - 1) * 100 + 12)
        else:
            return str(int(str(curMonth)[:4]) * 100 + int('%02d' % (month - 1)))

    def saveKeyValue(self,pid, key, month, num):
        try:
            currentProject = Overview.objects.get(project_id=pid, key=key, date=month)
            currentProject.value = num
            currentProject.save()
        except:
            Overview(project_id=pid, key=key, date=month, value=num).save()

class getSuiteName(generics.GenericAPIView):
    '''
        获取SuiteName
    '''
    serializer_class = getSuiteNameSerializerParam
    def get(self,request):
        try:
            print(request.query_params.get('project_id'))
            tempList = TestSuite.objects.filter(project_id=request.query_params.get('project_id')).values('suite_name').distinct()
            # TestSuite.objects.filter(project_id=request.query_params.get('project_id'))
            print(tempList)
            ret = TestSuiteSerializerParam(tempList, many=True)
            for i in ret.data:
                i['casenum'] = TestSuite.objects.filter(suite_name=i['suite_name']).count()
            return Response({"status": True, "message": "成功", "data": ret.data})
        except:
            return Response({"status": False, "message": "数据获取失败", "data": '失败'})

class getCaseName(generics.GenericAPIView):
    '''
        获取CaseName
    '''
    serializer_class = getCaseNameSerializerParam
    def get(self,request):
        try:
            print(request.query_params.get('project_id'),request.query_params.get('suite_name'))
            tempList = TestSuite.objects.filter(project_id=request.query_params.get('project_id'), suite_name=request.query_params.get('suite_name')).values("case_name")
            print(tempList)
            ret = TestSuiteSerializerParam(tempList, many=True)
            return Response({"status": True, "message": "成功", "data": ret.data})
        except:
            return Response({"status": False, "message": "数据获取失败", "data": '失败'})
