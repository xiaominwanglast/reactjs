#coding:utf-8
from django.conf import settings
from subprocess import Popen, PIPE
import threading
from autotestapp.views_report import *
class FactorCaseSaveObject(generics.GenericAPIView):
    """
    因子用例初始化数据更新
    """
    def get(self, request):
        """
        获取因子用例初始化数据
        """
        # pro = Popen('cd G:/gitlab/FactorPyTestProject & G: & pytest --collect-only', shell=True, stdout=PIPE,stderr=PIPE)
        pro = Popen(f'docker exec pytest-docker bash -c "cd {settings.CODEPATH}FactorPyTestProject && pytest --collect-only"', shell=True, stdout=PIPE,stderr=PIPE)
        out, err = pro.communicate()
        data =str(out, encoding = "utf-8")
        print (data)
        # factorData = re.findall(r"<Function (.*)>[\n|\r]\s+(.*?) --类型:(.*?)[\n|\r]", data)
        # factorList = []
        # for T in factorData:
        #     factorList.append(((T[0].split('_'))[1], T[0], (T[1].split('：'))[1], T[2]))
        factorCase=FactorCase.objects.filter(delete_flag=1)
        factorCase.delete()
        Packages = (data.split('Package'))
        factorList = []
        for p in Packages:
            package = re.findall(r'FactorPyTestProject/(.*?)>', p)
            if package:
                Modules = p.split('Module')
                for m in Modules:
                    module = re.findall(r'(.*?\.py)', m)
                    if module:
                        Classes = m.split('Class')
                        for c in Classes:
                            class_ = re.findall(r'(.*?)>', c)
                            factorData = re.findall(r"<Function (.*)>[\n|\r]\s+(.*?) --类型:(.*?)[\n|\r]", c)
                            for T in factorData:
                                factorList.append(((package[0].replace(' ', '') + '/' + module[0].replace(' ','') + '::' +class_[0].replace(' ', '') + '::' + T[0]), T[0],(T[1].split('：'))[1], T[2]))
        for fact in factorList:
            FactorCase.objects.update_or_create(factorCase=fact[1],factorName=fact[0],factorDesc=fact[2],factorType=fact[3],delete_flag=1)
        return Response({"status": True, "message": "成功", "data":factorList})


class FactorCaseListObject(generics.GenericAPIView, mixins.ListModelMixin):
    """
    因子用例展示列表
    """
    serializer_class = FactorCaseSerializer

    def get_queryset(self):
        factType=self.request.query_params.get('factType')
        if factType=='' or factType=='全部类型':
            factor_list = FactorCase.objects.filter(delete_flag=1).order_by("create_time")
        else:
            factor_list = FactorCase.objects.filter(delete_flag=1,factorType=self.request.query_params.get('factType')).order_by("create_time")
        return factor_list

    def get(self, request):
        """
        返回因子用例列表
        """
        return self.list(request)


class FactorCaseTypeListObject(generics.GenericAPIView):
    """
    获取所有因子类型用例
    """
    def get(self, request):
        """
        因子用例类型列表
        """
        factType=request.query_params.get('factType')
        if factType == '' or factType == '全部类型':
            myFactorResult = FactorCase.objects.filter(delete_flag=1).order_by("create_time")
        else:
            myFactorResult = FactorCase.objects.filter(delete_flag=1,factorType=factType).order_by("create_time")
        return Response({"status": True, "message": "成功", "data": myFactorResult.values()})


class FactorCaseRunObject(generics.GenericAPIView):
    """
    运行因子用例
    """
    serializer_class = FactorCaseSerializer
    def post(self, request):
        """运行因子用例"""
        request.data["user"]=request.session['user'].get('realname')
        request.data["name"]="车贷因子用例等{0}个".format(len(request.data['cases']))
        threading.Thread(target=self.runFactorCase, args=(request,)).start()
        return Response({"status": True, "message": "成功", "data": ""})

    def runFactorCase(self, request):
        print (request.data)
        timestamp = int(time.time())
        factorReport = AutoTestReportSaveObject().post(request)
        cases=request.data['cases']
        env = request.data['env']
        # caseeStr=" ".join(["CDWFactorCase/test_cdwAuto.py::TestcdwAutoFactor::"+i for i in cases])
        caseeStr=" ".join(cases)
        # pro = Popen('cd F:/SVNProject/FactorPyTestProject & F: & pytest {0} --html={1}/{2}/report.html'.format(caseeStr,settings.LOCALPYPATH, timestamp), shell=True, stdout=PIPE,stderr=PIPE)
        pro = Popen('docker exec pytest-docker bash -c "cd {0}FactorPyTestProject && pytest {1} --envopt {5} --html={2}{3}{4}/report.html"'.format(settings.CODEPATH,caseeStr, settings.LOGPATH, settings.STATIC_PYTEST_URL,timestamp,env), shell=True, stdout=PIPE,stderr=PIPE)
        out, err = pro.communicate()
        data =str(out, encoding = "utf-8")
        print (data)
        print('---开始调用解析日志---')
        request.data['report']= '{0}{1}{2}/report.html'.format(settings.LOGPATH, settings.STATIC_PYTEST_URL,timestamp)
        AutoTestReportModifyParamObject().put(request,factorReport.data['data']['id'])