#coding:utf-8
import random,threading


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpRequest
from testtools.base.jk import JK,getPhone
from testtools.base.config import flow,step
from testtools.sql_deal import ChangeOperator
from testtools.tools.create_credit import create_credit
from testtools.base.sqltools import DbTools
from testtools.serializers import *
import requests

def delCreditStep(product,flow):
    stepTemp = flow.copy()
    if '信用卡' in stepTemp:
        del stepTemp['信用卡']
    return stepTemp

class CreateUser(generics.GenericAPIView):
    """
           造号
    """
    serializer_class = CreateAccountSerializerParam
    def post(self,request):
        threading.Thread(target=self.createAccount,args=(request,)).start()
        return Response({"status": True, "message": "请求已经收到！", "data":{}})

    def createAccount(self,request):
        start,end,env,product,bin,otherNum = request.data.get('start'),request.data.get('end'),request.data.get('env'),request.data.get('product'),request.data.get('bin'),request.data.get('other')
        temp = Phone.objects.filter(id=1)
        phone = temp.values()[0]['phone']
        mobilephone = request.data.get('phone') if request.data.get('phone') else phone
        print(mobilephone)
        print(start, end, env, product,bin,otherNum)
        step = [x for x in range(start, end + 1)]
        step = step if 0 in step else [0] + step
        print(step)
        if product == '2345借款':
            # 设置信用卡认证
            if end == 3:
                ChangeOperator().post(request, flag=0, way='card')
            else:
                ChangeOperator().post(request, flag=1, way='card')
            stepInfo = list(flow.values())
        else:
            stepInfo = list(delCreditStep(product, flow).values())
        print(stepInfo)
        tt = JK(mobilephone, request.session['user'].get('realname'), env, product, step, request.data.get('serial_num'),bin,otherNum)
        temp.update(phone=phone+1) #保存手机号
        for i in step:
            test = 'tt.' + stepInfo[i] + '()'
            print('当前执行方法:',test)
            ret = eval(test)
            if not ret[0]:
                break

class GetStep(generics.GenericAPIView):
    """
           获取操作步骤
    """
    def get(self,request):
        product = request.query_params.dict()['product']
        step = flow.keys()
        if product !='2345借款':
            step = delCreditStep(product,flow).keys()
        return Response({"status": True, "message": "成功", "data":step})

class GetCurrentStepAndStatus(generics.GenericAPIView):
    """
           获取用户信息及造号过程状态
    """
    def get(self,request):
        i = 0
        while i<11:
            try:
                id = request.query_params.dict()['id']
                code = CreateAccount.objects.get(serial_num=id)
                ret = CreateAccountSerializerParam(code)
                if ret:
                    return Response({"status": True, "message": "成功", "data": ret.data})
            except:
                i += 1
                continue
        return Response({"status": False, "message": "失败", "data": {'errorinfo':'获取用户信息失败'}})

class GetAccountOperateCode(generics.GenericAPIView):
    """
       获取造号操作记录
    """
    serializer_class = QueryPageSerializerParam
    def post(self,request):
        print(11111)
        # code = TestTools.objects.all()
        pageNo = request.data.get('pageNo')
        pageSize = request.data.get('pageSize')
        env = request.data.get('env')
        isme = request.data.get('isme')
        # print((pageNo-1)*pageSize, pageNo*pageSize)
        if isme:
            total = CreateAccount.objects.filter(env=env, user_name=request.session['user'].get('realname')).count()
            tempList = CreateAccount.objects.filter(env=env,user_name=request.session['user'].get('realname')).order_by('-id')[(pageNo - 1) * pageSize:pageNo * pageSize]
        else:
            total = CreateAccount.objects.filter(env=env).count()
            tempList = CreateAccount.objects.filter(env=env).order_by('-id')[(pageNo-1)*pageSize:pageNo*pageSize]
        ret = CreateAccountSerializerParam(tempList, many=True)
        if tempList:
            # for i in ret.data:
            #     print(list(i.items())[0][1])
                # codeList.append({'id':i.id, 'user_name':i.user_name, 'product':i.product, 'project':i.project, 'operate_time':i.operate_time, 'phone':i.phone, 'option':i.option, 'env':i.env})
            return Response({"status": True, "message": "请求成功", "data": {'codeList':ret.data,'total':total}})
        else:
            return Response({"status": True, "message": "请求成功", "data": []})

class GetBankBinInfo(generics.GenericAPIView):
    """
       获取银行卡bin信息
    """
    def get(self,request):
        print(11111)
        tempList = BankBin.objects.all()
        ret = BankBinSerializerParam(tempList,many=True)
        print(ret.data)
        if tempList:
            return Response({"status": True, "message": "请求成功", "data": ret.data})
        else:
            return Response({"status": True, "message": "请求成功", "data": []})

class GetUserInfo(generics.GenericAPIView):
    """
       获取身份证信息
    """
    def get(self,request):
        idcard = request.GET.get("idcard")
        name = request.GET.get("name")
        phone = request.GET.get("phone")
        if idcard and name:
            tempList = IdcardInfo.objects.filter(name=name, idcard=idcard)
            if tempList:
                ret = IdcardInfoSerializerParam(tempList,many=True)
                return Response({"status": True, "message": "请求成功", "data": ret.data[0]})
        create = create_credit(cardid=idcard, name=name)
        name, gander, birthday_y, birthday_m, birthday_d, idcard_new, address_1, address_2 = create.create_all()
        print(idcard_new)
        national = "汉"
        # cardid_new_tab = idcard_new[:-6] + ' ' + idcard_new[-6:]
        if idcard_new:
            userInfo = {"username":request.session['user'].get('realname'),"name": name, "gander": gander, "birthday_y": birthday_y, "birthday_m": birthday_m,
                 "birthday_d": birthday_d, "idcard": str(idcard_new), "address_1": address_1,
                 "address_2": address_2, "national": national}
            if phone:
                userInfo['phone'] = phone
            serializer = IdcardInfoSerializerParam(data=userInfo)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": True, "message": "请求成功", "data":userInfo})
            else:
                return Response({"status": False, "message": "失败", "data": {'errorinfo': serializer.errors}})
        else:
            return Response({"status": False, "message": "失败", "data": {'errorinfo': '生成用户信息失败'}})

class GetUserInfoCode(generics.GenericAPIView):
    """
       获取身份证记录信息
    """
    serializer_class = QueryPageSerializerParam
    def post(self,request):
        # try:
        print(11111)
        pageNo = request.data.get('pageNo')
        pageSize = request.data.get('pageSize')
        isme = request.data.get('isme')
        print((pageNo-1)*pageSize, pageNo*pageSize)
        total = IdcardInfo.objects.all().count()
        print(total)
        if isme:
            tempList = IdcardInfo.objects.filter(username=request.session['user'].get('realname')).order_by('-id')[(pageNo - 1) * pageSize:pageNo * pageSize]
        else:
            tempList = IdcardInfo.objects.all().order_by('-id')[(pageNo-1)*pageSize:pageNo*pageSize]
        ret = IdcardInfoSerializerParam(tempList, many=True)
        if tempList:
            return Response({"status": True, "message": "请求成功", "data": {'codeList':ret.data,'total':total}})
        else:
            return Response({"status": True, "message": "请求成功", "data": []})
        # except:
        #     return Response({"status": False, "message": "请求失败", "data": []})
