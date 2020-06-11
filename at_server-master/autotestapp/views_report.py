#coding:utf-8
import json,time,datetime
from rest_framework import generics, mixins,views
from rest_framework.response import Response
from .serializers import *
from .DealTestReport import *
from .DealTestReport import DealTestReport,DealDictValue
from django.db import close_old_connections

class AutoTestReportObject(generics.GenericAPIView):
    """
    自动化测试报告查询
    """

    def get(self, request,id):
        """
        获取自动化测试报告
        """
        testResult_list = TestResult.objects.get(id=id)
        serializer = TestResultDetailSerializer(testResult_list)
        return Response({"status": True, "message": "成功", "data": serializer.data})

class AutoTestReportTJObject(generics.GenericAPIView):
    """
    自动化测试数据统计
    """

    def get(self, request,id):
        """
        获取测试统计数据
        """
        myTestResultJson={}

        localYM = time.strftime("%Y%m", time.localtime(time.time()))
        if id==0:
            myTestResult = TestResult.objects.all()
            #执行总次数
            myTestResultJson['count_zx_times']=myTestResult.count()
            #本月用例执行总数
            localTestResult=[i for i in list(myTestResult.values()) if i.get("create_time") and i.get("create_time").strftime('%Y%m')==localYM]
            myTestResultJson['count_lc_all']=len(localTestResult)
            #用例执行总数量
            count_zx_all=[int(i.get('count')) for i in list(myTestResult.values()) if i.get('count') != '']
            myTestResultJson['count_zx_all']=sum(count_zx_all)
            #用例执行成功率
            #本月用例执行总数量
            #本月用例执行成功数量
            count_zx_lc_all = [int(i.get('count')) for i in list(myTestResult.values()) if i.get('count') != '' and i.get("create_time").strftime('%Y%m')==localYM]
            count_zx_lc_pass=[int(i.get('pass_count')) for i in list(myTestResult.values()) if i.get('pass_count') != '' and i.get("create_time").strftime('%Y%m')==localYM]
            if sum(count_zx_lc_all)==0:
                myTestResultJson['count_zx_pass']=0.0
            else:
                myTestResultJson['count_zx_pass'] = round(float(sum(count_zx_lc_pass) / sum(count_zx_lc_all)), 4)
        else:
            myTestResult = TestResult.objects.filter(project_id=id)
            #执行总次数
            myTestResultJson['count_zx_times']=myTestResult.count()
            # 本月用例执行总数
            localTestResult=[i for i in list(myTestResult.values()) if i.get("create_time") and i.get("create_time").strftime('%Y%m')==localYM]
            myTestResultJson['count_lc_all'] = len(localTestResult)
            #用例执行总数量
            count_zx_all=[int(i.get('count')) for i in list(myTestResult.values()) if i.get('count') != '']
            myTestResultJson['count_zx_all']=sum(count_zx_all)
            #用例执行成功率
            #本月用例执行总数量
            #本月用例执行成功数量
            count_zx_lc_all = [int(i.get('count')) for i in list(myTestResult.values()) if i.get('count') != '' and i.get("create_time").strftime('%Y%m')==localYM]
            count_zx_lc_pass=[int(i.get('pass_count')) for i in list(myTestResult.values()) if i.get('pass_count') != '' and i.get("create_time").strftime('%Y%m')==localYM]
            if sum(count_zx_lc_all)==0:
                myTestResultJson['count_zx_pass']=0.0
            else:
                myTestResultJson['count_zx_pass'] = round(float(sum(count_zx_lc_pass) / sum(count_zx_lc_all)), 4)

        #用例总数
        myOverViewCount=Overview.objects.filter(project_id=id,key="count")
        myOverViewList=[int(i.get('value')) for i in myOverViewCount.values() if i.get('value')]
        if myOverViewList:
            myTestResultJson['count_yl_all']=max(myOverViewList)
        else:
            myTestResultJson['count_yl_all']=0
        #本月用例增减数
        myOverViewCaseLocal=Overview.objects.filter(project_id=id,key="addnum",date=localYM)
        if not myOverViewCaseLocal.values():
            myTestResultJson['count_addnum']=0
        else:
            myTestResultJson['count_addnum']=int(myOverViewCaseLocal.values()[0].get('value',0))
        #用例新增数
        myOverViewCase = Overview.objects.filter(project_id=id,key="addnum")
        myOverViewCaseJson={}
        for i in myOverViewCase.values():
            if i.get('value'):
                myOverViewCaseJson[i.get('date')] = int(i.get('value'))
        myTestResultJson['count_data']=myOverViewCaseJson
        return Response({"status": True, "message": "成功", "data": myTestResultJson})

class  AutoTestReportSaveObject(generics.GenericAPIView):
    """
    自动化测试报告保存
    """
    serializer_class = TestResultSerializer
    def post(self, request):
        """
        自动化测试报告保存
        """
        print('调用模块存储初始化Running数据')
        request.data["status"]="Running"
        serializer = TestResultSerializer(data=request.data)
        if not serializer.is_valid():
            print('序列化不正确,初始化Running数据未存储')
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        print('调用模块存储初始化Running数据:{0}'.format(request.data))
        return Response({"status": True, "message": "成功", "data": serializer.data})

class  AutoTestReportModifyParamObject(generics.GenericAPIView):
    """
    自动化测试报告修改
    """
    serializer_class = TestReportSerializerModifyParam

    # def get(self, request, id):
    #     """
    #     查询一个自动化测试报告修改内容
    #     """
    #     myTestResult = TestResult.objects.get(product_id=id)
    #     serializer = TestResultSerializer(myTestResult)
    #     return Response({"status": True, "message": "成功", "data": serializer.data})

    def put(self, request, id):
        """
        自动化测试报告修改
        """
        #解析报告到测试结果表
        print('调用模块更新Running数据,请求数据：{0}'.format(request.data))
        close_old_connections()
        myTestResult = TestResult.objects.get(id=id)
        if request.data["report"]=="":
            request.data["status"] = "error"
            serializer = TestReportSerializerModifyParam(myTestResult, data=request.data)
            if not serializer.is_valid():
                print('反序列化不正确-未获取到report,请求数据：{0}'.format(request.data))
                return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
            serializer.save()
            print('调用模块更新Running数据-未获取到report,请求数据：{0}'.format(request.data))
            return Response({"status": True, "message": "测试报告不存在", "data": serializer.errors})
        print('调用模块更新Running数据-开始解析报告，请求数据：{0}'.format(request.data))

        if 'rf' in request.data["report"]:
            testData=DealTestReport(request.data["report"]).dealReport()
        elif 'py' in request.data["report"]:
            testData = DealPyTestReport(request.data["report"]).dealReport()
        else:
            testData = DealTestNGReport(request.data["report"]).dealReport()

        print('调用模块更新Running数据-获取报告解析:{0}'.format(testData))
        if not testData:
            request.data["status"] = "error"
        else:
            request.data["duration"]=testData[0]
            request.data["count"] =int(testData[1])+int(testData[2])
            request.data["pass_count"]=int(testData[2])
            request.data["fail_count"]=int(testData[1])
            if int(testData[1])==0:
                request.data["status"]="Pass"
            else:
                request.data["status"]="Fail"
        print('调用模块更新Running数据-处理后报告数据:{0}'.format(request.data))
        serializer = TestReportSerializerModifyParam(myTestResult, data=request.data)
        if not serializer.is_valid():
            print('反序列化不正确,不更新Running数据')
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()
        print('调用模块更新Running数据-保存数据成功')
        #解析报告修改概况总览表value值
        if 'rf' in request.data["report"]:
            caseData = DealTestReport(request.data["report"]).check_tests()
        elif 'py' in request.data["report"]:
            caseData = DealPyTestReport(request.data["report"]).dealCaseName()
        else:
            caseData = DealTestNGReport(request.data["report"]).dealCaseName()
        try:
            myOverView=Overview.objects.get(project_id=request.data["project_id"],key="failcase")
            caseDataValue=eval(myOverView.value)
            DealDictValue().merge_dict(caseData,caseDataValue)
            serializer_myOverView= OverViewModifyParamSerializer(myOverView,data={'project_id': myOverView.project_id, 'key':myOverView.key, 'value':json.dumps(caseDataValue,ensure_ascii=False)})
        except:
            serializer_myOverView= OverViewModifyParamSerializer(data={'project_id': request.data["project_id"], 'key':"failcase", 'value':json.dumps(caseData,ensure_ascii=False)})
        serializer_myOverView.is_valid() and serializer_myOverView.save()
        return Response({"status": True, "message": "成功", "data": serializer.data})

class AutoTestReportListObject(generics.GenericAPIView, mixins.ListModelMixin):
    """
    自动化测试报告报告展示列表
    """
    serializer_class = TestResultDetailSerializer

    def get_queryset(self):
        testResult_list = TestResult.objects.filter(project_id=self.request.query_params.get('project_id')).order_by("-create_time")
        return testResult_list

    def get(self, request):
        """
        条件查询,什么参数都不传，返回所有
        """
        return self.list(request)