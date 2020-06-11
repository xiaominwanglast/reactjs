#coding:utf-8
import requests,json,random,os,base64,string,sys,time
from testtools.base.config import productDict
from testtools.base.sqltools import DbTools
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from testtools.tools.des import *
from testtools.serializers import *
from faker import Factory


def getNameAndCard():
    from faker import Factory
    fake = Factory.create('zh_CN')
    for i in range(1000):
        person = fake.profile(fields=None, sex=None)
        if 1975 < int(person['ssn'][6:10]) < 1995:
            break
    return person['name'], person['ssn']

def getPhone():
    fake = Factory.create('zh_CN')
    phone = fake.phone_number()
    if '188' in phone or '177' in phone:
        phone = getPhone()
    return phone

class JK():
    def __init__(self, mobilephone, userName, env, product, step, serial_num, bankbin, otherBankNum):
        self.ip = '%s.%s.%s.%s' % (random.randint(100, 250), random.randint(100, 250), random.randint(100, 250), random.randint(100, 250))
        self.userName = userName
        self.product = product
        self.env = env
        self.bankbin = bankbin if bankbin else '622010'
        self.otherBankNum = otherBankNum
        print('--------',self.bankbin, self.otherBankNum)
        temp = ProductConfig.objects.filter(name=product)
        ret = ProductConfigSerializerParam(temp, many=True)
        interFace = ret.data[0]
        self.period = interFace['period']
        self.purpose = interFace['purpose']
        self.fundId = interFace['fundId']
        self.host = interFace['host'].replace('env',str.lower(env))
        self.interface = json.loads(interFace['interface'])
        self.pid = interFace['pid']
        self.mobilephone = mobilephone
        self.step = step
        self.idcard = ''
        self.serial_num = serial_num
        self.serial_num_flag = 1
        self.vipType = interFace['type']
        self.headers = {
            'pid': self.pid,
            'terminalId': interFace['terminalId'],
            'bundleId': interFace['bundleId'],
            'version': interFace['version'],
            'channel': 'test_channel',
            "x-forwarded-for": self.ip,
        }
        self.session = requests.Session()
        self.session.headers = self.headers
        self.des = Des()
        self.dirpath = os.path.dirname(os.path.realpath(__file__))
        self.token = ''
        self.uid = ''
        self.cid = ''


    def saveOperatorLog(self,current_step, status, errorinfo='', url='', name='', bankcard='', idcard=''):
        self.current_step = current_step
        # print(operator_log)
        print(self.serial_num_flag)
        # phone = str(self.mobilephone)
        # phone = phone[:3] + ' ' + phone[3:7] + ' '+ phone[7:]
        if self.serial_num_flag == 1:
            operator_log = {
                'serial_num': self.serial_num,
                'user_name': self.userName,
                'env': self.env,
                'url': url,
                'product': self.product,
                'phone': self.mobilephone,
                'bankcard': bankcard,
                'idcard': idcard,
                'errorinfo': errorinfo,
                'current_step': current_step,
                'status': status,
                'uid':self.uid,
                'cid':self.cid,
            }
            serializer_operate = CreateAccountSerializerParam(data=operator_log)
            self.serial_num_flag += 1
        else:
            statusThis = status
            errorinfoThis = errorinfo
            urlThis = url
            if not self.uid and status not in ['running','fail']:
                try:
                    envdb = DbTools(self.env, self.mobilephone, self.product)
                    self.uid = envdb.userId
                    self.cid = str(envdb.customerId) + '--' + str(envdb.customerIdPro) if envdb.customerIdPro else str(
                        envdb.customerId)
                except:
                    statusThis = 'fail'
                    urlThis = url
                    errorinfoThis = str({'code':'fail','info':'未获取到用户信息，请检查数据库是否配置正确'})
            operator_log = {
                'url': urlThis,
                'errorinfo': errorinfoThis,
                'current_step': current_step,
                'status': statusThis,
                'uid': self.uid,
                'cid': self.cid,
            }
            if bankcard:
                operator_log['bankcard'] = bankcard
            if idcard:
                operator_log['idcard'] = idcard
                operator_log['name'] = name
            code = CreateAccount.objects.get(serial_num=self.serial_num)
            # operator_log['update_time']=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            print(operator_log)
            serializer_operate = CreateAccountSerializerParam(code, data=operator_log)

        if serializer_operate.is_valid():
            serializer_operate.save()
        return operator_log

    def registerAndLogin(self):
        self.saveOperatorLog('注册/登录', 'running')
        ret = self.getcode()
        if not ret[0]:
            return ret
        ret = self.loginByCode()
        return ret

    # @staticmethod
    def getcode(self):
        url = self.interface['获取验证码']
        data = {"mobilephone": self.mobilephone, "dynamicCodeType": "1"}
        print(self.host + url)
        # r = self.session.post(self.host + url, data=data)
        # print(data)
        # print(self.headers)
        # r = requests.post(self.host + url, data=data, headers=self.headers)
        # print(r.text)
        # ret = r.json()
        ret = self.postThree(self.host + url, data=data, headers=self.headers)
        if ret['code'] == 'success' and 'result' in ret and 'status' in ret['result'] and ret['result'][
            'status'] == 1:
            return True, str(ret)
        self.saveOperatorLog('注册/登录', 'fail', errorinfo=str(ret), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

    # @property
    def loginByCode(self):
        url = self.interface['注册/登录']
        data = {"mobilephone": str(self.mobilephone), "dynamicCode": "888888", "dynamicCodeType": "1"}
        # r = self.session.post(self.host + url, data=data)
        ret = self.postThree(self.host + url, data=data,headers=self.headers)
        if ret['code'] == 'success' and 'result' in ret and 'token' in ret['result']:
            self.token = ret['result']['token']
            self.headers['token'] = ret['result']['token']
            print(self.headers)
            self.saveOperatorLog('注册/登录', 'success')
            return True, str(ret)
        self.saveOperatorLog('注册/登录', 'fail',errorinfo=str(ret))
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

    def getProvider(self):
        url = self.interface['获取人脸Provider']
        data = {
            "versionCode": "1.1",
            "stage": "FACE"
        }
        headers = self.headers.copy()
        headers['Content-Type']='text/plain;charset=utf-8'
        data = self.des.DesEncrypt(json.dumps(data))
        # print(data)
        ret = self.postThree(self.host + url, data=data,  headers=headers)
        if ret['code'] == 'success':
            return True, ret
        self.saveOperatorLog('人脸OCR', 'fail', errorinfo=str(ret), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))


    def saveFaceAndOcr(self):
        self.saveOperatorLog('人脸OCR', 'running')
        # if 3 in self.step:
        ret = self.getProvider()
        if not ret[0]:
            return ret
        way = json.loads(self.des.DesDecrypt(ret[1]['result']))['provider']
        print(way)
        from faker import Factory
        fake = Factory.create('zh_CN')
        ret = self.saveFaceVerifyResult(way)
        if not ret[0]:
            return ret
        for i in range(1000):
            person = fake.profile(fields=None, sex=None)
            if 1975 < int(person['ssn'][6:10]) < 1995:
                break
        print(self.mobilephone, person['ssn'][6:10])
        print(person['name'],person['ssn'])
        ret = self.saveOcrVerifyResult(person['name'], person['ssn'], way)

        return ret

    # @property
    def saveFaceVerifyResult(self,way='FACE_ID'):
        url = self.interface['人脸']
        if way == 'FACE_ID':
            data = {
                "faceText":  "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"
            }
        else:
            data = {
                "faceText": "BtqQ9IM68lUfqfZ0Va7gaisR6+zLmGf8VkK/Y6blxXBYy9xrhpG0fvR7oyL33AkL8802dKbGHXv5CzMuzhKZ+eMfGnnsD9IIR8DiZwNO5XIG+5vSJlpHT5c1G55CsIhuWAKO3hFv2MOj6QdsILgpcVOzZIAcsxFcAFElkl5Y3eHnIHOf1cJerW0bPcvx4uRhquBMyGMsDzDo6nHgA6YIJs1dRiFgR7a5AwdVdixPP9M="
            }
        files = {
            "imageBest": ('imageBest.jpg', open(os.path.join(self.dirpath, 'images', 'avatar.jpg'), 'rb')),
            "imageEnv": ('imageEnv.jpg', open(os.path.join(self.dirpath, 'images', 'avatar.jpg'), 'rb')),
            "imageAction": ('imageAction0.jpg', open(os.path.join(self.dirpath, 'images', 'avatar.jpg'), 'rb')),
            "imageAction1": (
            'imageAction1.jpg', open(os.path.join(self.dirpath, 'images', 'avatar.jpg'), 'rb')),
            "imageAction2": (
            'imageAction2.jpg', open(os.path.join(self.dirpath, 'images', 'avatar.jpg'), 'rb')),
        }
        headers = self.headers.copy()
        # r = requests.post(self.host + url, data=data, files=files,headers=headers)
        ret = self.postThree(self.host + url, data=data, files=files, headers=headers)
        if ret['code'] == 'success' and ret['result'] == True:
            return True, str(ret)
        self.saveOperatorLog('人脸OCR', 'fail', errorinfo=str(ret), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

    def saveOcrVerifyResult(self, name, idcard, way='FACE_ID'):
        url = self.interface['ocr']
        idcard_front_file = open(os.path.join(self.dirpath, 'images', 'idcard_front.jpg'), 'rb')
        idcard_back_file = open(os.path.join(self.dirpath, 'images', 'idcard_back.jpg'), 'rb')
        print('----------xxxxxxxxx------------',idcard_front_file)
        files = {
            "frontFullImage": ('frontFullImage.jpg', idcard_front_file),
            "backFullImage": ('backFullImage.jpg', idcard_back_file),
        }
        if way == 'WZ':
            data ={
                "ocrId": "",
                "code": "0",
                "reedited": 0,
                "name": name,
                "validDate": "20090602-20190602",
                "idcard": idcard,
                "sign": "F70C189E85347E50D40C5ABF1B78A53203886711",
                "authority": "安徽省怀远县公安局",
                "nation": "汉",
                "warning": "00000000",
                "birth": idcard[6:14],
                "address": "西藏自治区六盘水市山亭边街k座",
                "versionCode": "1.1",
                "orderNo": "220000000000001560lYXgiV6PKL1jF0",
                "sex": "男"
            }
            data = self.des.DesEncrypt(json.dumps(data))
            data = {"ocrText": data}
            ret = self.postThree(self.host + url, data=data,files=files, headers=self.headers)
        else:
            data ={
                "ocrId": "",
                "code": "0",
                "reedited": 0,
                "name": name,
                "validDate": "20090619-20190615",
                "idcard": idcard,
                "sign": "",
                "authority": "安徽省怀远县公安局",
                "nation": "汉",
                "warning": "",
                "legality": {
                    "edited": 0.0,
                    "photoCopy": 0.0,
                    "temporaryIdPhoto": 0.0,
                    "screen": 0.0,
                    "idPhoto": 1.0
                },
                "birth": idcard[6:14],
                "address": "",
                "versionCode": "1.1",
                "orderNo": "",
                "sex": "女",
             }
            data = self.des.DesEncrypt(json.dumps(data))
            data = {"ocrText": data}
            # r = self.session.post(self.host + url, data=data, files=files)
            ret = self.postThree(self.host + url, data=data, files=files ,headers=self.headers)
        if ret['code'] == 'success':
            self.saveOperatorLog('人脸OCR', 'success', name=name, idcard=idcard)
            return True, str(ret)
        self.saveOperatorLog('人脸OCR', 'fail', errorinfo=str(ret), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

    def fullUserInfo(self):
        self.saveOperatorLog('填写资料', 'running')
        if self.product == '2345借款':
            ret = self.basicInfo()
        else:
             ret = self.basicTwo()
        return ret

    def basicTwo(self):
        url = self.interface['填写信息-基本信息']
        data = {
                "homeAddr": "幸福小区6号",
                "homeCityId": "62",
                "homeDistrictId": "604",
                "homeProvinceId": "5",
                "orgAddr": "幸福小区6号",
                "orgCityId": "53",
                "orgDistrictId": "518",
                "orgName": "奕铭图文",
                "orgProvinceId": "4"
            }
        ret = self.postThree(self.host + url, json=data, headers=self.headers)
        if ret['code'] != 'success':
            self.saveOperatorLog('填写资料', 'fail', errorinfo=str(ret), url=url)
            return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

        url = self.interface['填写信息-联系人']
        data = {
                "friendName": "测试2",
                "friendPhone": "19112340058",
                "relativeName": "测试145486",
                "relativePhone": "13412340056"
            }
        ret = self.postThree(self.host + url, json=data, headers=self.headers)
        if ret['code'] != 'success':
            self.saveOperatorLog('填写资料', 'fail', errorinfo=str(ret), url=url)
            return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))
        self.saveOperatorLog('填写资料', 'success')
        return True,

    def basicInfo(self):
        # if 3 in self.step:
        url = self.interface['填写信息']
        data = {
                "friendName": "测试2",
                "friendPhone": getPhone(),
                "marriageStatus": 0,
                "homeAddr": "幸福小区6号",
                "homeCityId": "78",
                "homeDistrictId": "712",
                "homeProvinceId": "6",
                "orgAddr": "幸福小区6号",
                "orgCityId": "114",
                "orgDistrictId": "990",
                "orgName": "你以为无故",
                "orgProvinceId": "8",
                "relativeName": "测试2",
                "relativePhone": getPhone()
            }
            # r = self.session.post(self.host + url, json=data)
        ret = self.postThree(self.host + url, json=data, headers=self.headers)
        if ret['code'] == 'success':
            self.saveOperatorLog('填写资料', 'success')
            return True, str(ret)
        self.saveOperatorLog('填写资料', 'fail', errorinfo=str(ret), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

    def openAccount(self):
        # if 5 in self.step:
        self.saveOperatorLog('开户', 'running')
        url = self.interface['开户']
        ret = self.postThree(self.host + url, headers=self.headers)
        if ret['code'] != 'success':
            self.saveOperatorLog('开户', 'fail', errorinfo=str(ret), url=url)
            return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))
        ret = self.getUserStatus()
        return ret

    def bankCardCredit(self):
        # if 9 in self.step:
        self.saveOperatorLog('信用卡', 'running')
        ret = self.bankCard('信用卡',2,8)
        return ret

    def bankCardDeposit(self):
        # if 6 in self.step:
        self.saveOperatorLog('储蓄卡', 'running')
        ret = self.bankCard('储蓄卡',1,8, self.bankbin, self.otherBankNum)
        return ret

    def bankCard(self,mark,type,bankId, bankbin='622010',other=''):
        #鉴权申请
        url = self.interface['绑卡鉴权申请']
        others = other if other else str(random.randint(1111111111,9999999999)) + '90'
        bankcard = bankbin + others
        # bankcard = '620501' + ''.join(random.sample(string.digits, 10)) + ''.join(random.sample(string.digits, 3))
        phone = getPhone()
        data = {
            'bankId': bankId,
            'bankcardNo': bankcard,
            'cardType': type,
            'dynamicCodeType': 4,
            # 'oldBankcardId':0,
            'reservedPhone':phone
        }
        # r = self.session.post(self.host + url, data=data)
        ret = self.postThree(self.host + url, data=data, headers=self.headers)
        if ret['code'] != 'success':
            self.saveOperatorLog(mark, 'fail', errorinfo=str(ret), url=url)
            return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))
        #鉴权确认
        url = self.interface['绑卡鉴权确认']
        data = {
            'bankId': bankId,
            'bankcardNo': bankcard,
            'cardType': type,
            'dynamicCodeType': 4,
            'reservedPhone': phone,
            'dynamicCode': 111111 if type==1 else 888888,
        }
        ret = self.postThree(self.host + url, data=data, headers=self.headers)
        if ret['code'] == 'success':
            self.saveOperatorLog(mark, 'success', bankcard=bankcard)
            return True, str(ret)
        self.saveOperatorLog(mark, 'fail', errorinfo=str(ret), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

    def authOperator(self):
        self.saveOperatorLog('运营商', 'running')
        url = self.interface['更新运营商状态']
        data = {
            'operator':1,
            'taskType':3,
        }
        # r = self.session.post(self.host + url, data=data)
        ret = self.postThree(self.host + url, data=data, headers=self.headers)
        if ret['code'] == 'success':
            self.saveOperatorLog('运营商', 'success')
            return True, str(ret)
        self.saveOperatorLog('运营商', 'fail', errorinfo=str(ret), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

    def getLoanInfo(self):
        # 预借款
        url = self.interface['获取预借款信息']
        data = {
            'amount': 100000,
            'originDevice': 2,
            'period': self.period,
            'unit': 2,
            'whiteList': 'true'
        }
        # r = self.session.post(self.host + url, data=data)
        ret = self.postThree(self.host + url, data=data, headers=self.headers)
        if ret['code'] == 'success':
            self.orderNo = ret['result']['protocol']['coreOrderNo']
            self.bankcardId = ret['result']['bankcard']['bankCard'][0]['bankcardId']
            self.riskNo = ret['result']['toBorrow']['riskNo']
            time.sleep(5)
            return True, str(ret)
        self.saveOperatorLog('借款', 'fail', errorinfo=str(ret), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

    def getLoanStatus(self):
        # 获取借款状态
        url = self.interface['获取借款状态']
        data = {
            'amount': 200000,
            'originDevice': 2,
            'whiteList': 'true',
            'riskNo': self.riskNo,
            'period': self.period,
            'tryTimes': 1,
        }
        # while True:
        ret = self.postThree(self.host + url, data=data, headers=self.headers)
        if ret['code'] == 'success' and ret['result']['status'] == 2:
            try:
                self.serviceSwitch = ret['result']['serviceSwitch']
            except:
                self.serviceSwitch = 'true'
                # print('可申请借款')
            return True, str(ret)
        self.saveOperatorLog('借款', 'fail', errorinfo=str(ret), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

    def borrowInfo(self):
        url = self.interface['借款结果查询']
        data = {
            'orderId':self.orderId,
        }
        for i in range(0,12):
            ret = self.postThree(self.host + url, data=data, headers=self.headers)
            if ret['code'] != 'success':
                self.saveOperatorLog('借款', 'fail', errorinfo=str(ret), url=url)
                return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))
            if ret['result']['borrowStatus'] == 106:
                self.saveOperatorLog('借款', 'success')
                return True,
            time.sleep(10)
        self.saveOperatorLog('借款', 'fail', errorinfo=str({'code':'fail','result':'订单一直在借款中，请查明原因，大概率是借款job未执行'}), url=url)
        return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

        #借款
    def prepareBorrow(self):
        # if 7 in self.step:
        self.saveOperatorLog('借款', 'running')
        ret = self.getLoanInfo()
        if not ret[0]:
            return ret
        ret = self.getLoanStatus()
        if not ret[0]:
            return ret
        url = self.interface['借款鉴权']
        #借款鉴权
        data = {
            'dynamicCodeType':7,
            'mobilephone':self.mobilephone,
            'coreOrderNo':self.orderNo,
            'bankcardId':self.bankcardId,
            'serviceSwitch':self.serviceSwitch,
        }
        print(data)
        # r = self.session.post(self.host + url, data=data)
        ret = self.postThree(self.host + url,data=data, headers=self.headers)
        print(111,ret)
        if ret['code'] != 'success':
            self.saveOperatorLog('借款', 'fail', errorinfo=str(ret), url=url)
            return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))

        #借款
        url = self.interface['借款']
        data = {"amount": 100000, "bankcardId": self.bankcardId, "dealPwd":"",
                "orderNo": self.orderNo, "period": str(self.period), "purpose": self.purpose, "reqUuid": 'gh' + str(int(time.time())), "fundId": self.fundId,
                "dynamicCodeType": "7", "dynamicCode": "888888", "mobilephone": self.mobilephone, "serviceSwitch": self.serviceSwitch,"type":self.vipType}
        # r = self.session.post(self.host + url, data=data)
        if self.pid in ['109','110']:
            data['orderType'] = '2'
        print(self.headers)
        ret = self.postThree(self.host + url, data=data, headers=self.headers)
        if ret['code'] != 'success':
            self.saveOperatorLog('借款', 'fail', errorinfo=str(ret), url=url)
            return False, u"<br/><br/>【接口】:{0}<br/><br/>【响应】:{1}".format(url, str(ret))
        self.orderId = ret['result']['orderId']
        ret = self.borrowInfo()
        return ret

    def getUserStatus(self):
        url = self.interface['获取用户状态']
        for i in range(0,20):
            time.sleep(5)
            # r = requests.post(self.host + url,headers=headers)
            ret = self.postThree(self.host + url, headers=self.headers)
            if ret['result']['status'] == 1:
                print('已开户完成，可进行绑卡并借款')
                self.saveOperatorLog('开户', 'success')
                return True,
            elif ret['result']['status'] in [3,5] :
                break
        self.saveOperatorLog('开户', 'fail', errorinfo=str(ret)+'---2代表一直在处理中,需要执行查询job, 3被拒 5进人工', url=url)
        return False,  u"<br/><br/>【接口】:{}<br/><br/>【响应】:{}".format(url,str(ret)+'3被拒 5人工')

    def runSuc(self,func,*args):
        while True:
            try:
                ret = func(*args)
                return ret
            except:
                time.sleep(2)
                continue

    def postThree(self,url, data=None, files=None, headers=None,json=None):
        print(data)
        i = 0
        while i<6:
            try:
                r = requests.post(url, data=data, files=files, headers=headers, json=json)
                print(url,'-----',r.status_code, type(r.status_code), r.text)
                print('5' not in str(r.status_code))
                if r.json()['code'] not in ['SYS_ERR_DEMOTION']:
                    return r.json()
                i += 1
                continue
            except:
                i += 1
                continue
        return {'code':'fail', 'info':'系统无响应，请查明原因或者重试'}

#     # def post(self,request):
#
# if __name__ == '__main__':
#     from faker import Factory
#
#     fake = Factory.create('zh_CN')
#
#     # for i in range(10):
#     try:
#         mobilephone = request['user']
#     except:
#         mobilephone = fake.phone_number()
#     # mobilephone='13600000635'
#     for i in range(1000):
#         person = fake.profile(fields=None, sex=None)
#         if 1975 < int(person['ssn'][6:10]) < 1995:
#             break
#     bankcard = '620501' + ''.join(random.sample(string.digits, 10)) + ''.join(random.sample(string.digits, 3))
#     print(mobilephone, person['ssn'][6:10])
#     print(person['name'])
#
#     tt = JK(mobilephone)
#
#     tt.getDynamicCode()
#     tt.loginByCode()
#     # tt.getUserStatus()
#     tt.saveFaceVerifyResult()
#     tt.saveOcrVerifyResult(person['name'], person['ssn'])
#     tt.basicInfo()
#     tt.bankCard(2)
#     tt.bankCard(1)
#     tt.openAccount()
#     tt.getUserStatus()
#     tt.prepareBorrow()


