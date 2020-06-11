#coding:utf-8
from robot.api import ExecutionResult, ResultVisitor
import re
global suit_list
suit_list = {}

class ExecutionTimeChecker(ResultVisitor):
    def __init__(self,report):
        self.report=report

    def visit_test(self, test):
        if test.status == 'FAIL':
            bool=True
            caseName=''
            caseStr='test'
            while bool:
                if eval(caseStr):
                    caseName=caseName+'_'+eval(caseStr).name
                    caseStr = caseStr + '.parent'
                else:
                    bool=False
            caseName=caseName[1:]
            if caseName:
                if caseName not in suit_list.keys():
                    suit_list[caseName]=1
                else:
                    suit_list[caseName] = suit_list[caseName]+1
        return suit_list


class DealTestReport(object):
    def __init__(self,report):
        self.report=report

    def dealReport(self):
        print ('解析报告：{0}'.format(self.report))
        result = ExecutionResult(self.report)
        elapsedTime=result.suite.elapsedtime
        m, s = divmod(int(elapsedTime)/1000, 60)
        h, m = divmod(m, 60)
        elapsedStfTime="%02d:%02d:%02d" % (h, m, s)
        print ('解析报告：[{0}]-{1}-{2}'.format(elapsedStfTime,result.statistics.total.critical.failed,result.statistics.total.critical.passed))
        return (elapsedStfTime,result.statistics.total.critical.failed,result.statistics.total.critical.passed)

    def check_tests(self):
        result = ExecutionResult(self.report)
        result.visit(ExecutionTimeChecker(self.report))
        return suit_list

    def __del__(self):
        global suit_list
        suit_list={}

class DealDictValue(object):
    @staticmethod
    def merge_dict(x, y):
        for k, v in x.items():
            if k in y.keys():
                y[k] += v
            else:
                y[k] = v



class DealTestNGReport(object):
    def __init__(self,report):
        self.report=report
        self.fs=open(self.report,  encoding='utf-8')
        self.reportData=self.fs.read()

    def dealReport(self):
        print ('解析报告：{0}'.format(self.report))
        failed = re.search('failed="(\d+)"', self.reportData)
        passed = re.search('passed="(\d+)"', self.reportData)
        duration = re.search('duration-ms="(\d+)"', self.reportData)
        failed=int(failed.groups()[0])
        passed=int(passed.groups()[0])
        m, s = divmod(int(duration.groups()[0]) / 1000, 60)
        h, m = divmod(m, 60)
        duration = "%02d:%02d:%02d" % (h, m, s)
        return (duration,failed,passed)

    def dealCaseName(self):
        name = re.findall('<test-method status="FAIL" .*?name="(.*?)"', self.reportData)
        return DealListToDict().count_object(name)

    def __del__(self):
        self.fs.close()


class DealListToDict(object):
    @staticmethod
    def count_object(array):
        result_obj = {}
        for item in array:
            result_obj[item] = array.count(item)
        return result_obj


class DealPyTestReport(object):
    def __init__(self,report):
        self.report=report
        self.fs=open(self.report, encoding='utf-8')
        self.reportData=self.fs.read()

    def dealReport(self):
        print ('解析报告：{0}'.format(self.report))
        passed = re.search('<span class="passed">(\d+)\spassed</span>', self.reportData)
        failed = re.search('<span class="failed">(\d+)\sfailed</span>', self.reportData)
        duration = re.search('ran\sin\s(.*?)\sseconds', self.reportData)
        failed=int(failed.groups()[0])
        passed=int(passed.groups()[0])
        m, s = divmod(float(duration.groups()[0]), 60)
        h, m = divmod(m, 60)
        duration = "%02d:%02d:%02d" % (h, m, s)
        return (duration,failed,passed)

    def dealCaseName(self):
        name = re.findall('<td\sclass="col-result">Failed</td>\n\s+<td class="col-name">.*::(.*?)</td>', self.reportData)
        return DealListToDict().count_object(name)

    def __del__(self):
        self.fs.close()

    
if __name__=="__main__":
    print(DealTestReport("/Users/xiaosong/Desktop/output.xml").dealReport())
    print(DealTestReport("/Users/xiaosong/Desktop/output.xml").check_tests().keys())
