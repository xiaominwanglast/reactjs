from testtools.base.sqltools import DbTools,MongoDB,Redis,today
from testtools.base.config import productDict
from rest_framework import generics
from rest_framework.response import Response
from testtools.serializers import *
import json,time,datetime
from datetime import datetime

class ChangeOperator(generics.GenericAPIView):

    """
        修改用户是否需要认证运营商
    """
    serializer_class = TestToolsSerializerParam
    def post(self,request, flag=None, way=None):
        if not request.data.get('phone') and not request.data.get('flag') and not request.data.get('env') and request.data.get('way'):
            return Response({"status": False, "message": "参数不能为空", "data":{}})
        else:
            tts = {}
            tts['phone'] = request.data.get('phone')

            if tts['phone'] and len(str(tts['phone']))==11 and str(tts['phone']).isdigit:
                print('收到的手机号为：', tts['phone'])
                tts['env'] = request.data.get('env')
                tts['product'] = request.data.get('product')
                envdb = DbTools(tts['env'],tts['phone'],tts['product'])
                print(envdb.isRegister)
                pid = productDict[request.data.get('product')]['pid']
                if envdb.isRegister:
                    if request.data.get('flag') in [0,1]:
                        if request.data.get('way') == 'operator':
                            tts['option'] = "不认证" if request.data.get('flag') else "认证"
                            project = '运营商'
                            dbase = 'bpa' if request.data.get('product') == '立即贷' else 'bpa_' + pid + '_center'
                            envdb.db.select_db(dbase)
                            #1不做 0要做
                            sql = 'update account_diff_record_{} set status={} where customer_id = {} and product_id ={};'.format(envdb.cusRemainderPro, request.data.get('flag'), envdb.customerIdPro, pid)
                            print(sql)
                            envdb.cur.execute(sql)
                        elif way  == 'card' or request.data.get('way') == 'card':
                            project = '信用卡'
                            dbase = 'bpa' if request.data.get('product') == '立即贷' else 'bpa_' + pid + '_center'
                            envdb.db.select_db(dbase)
                            flagTemp = 'false' if request.data.get('flag') or flag else 'true'
                            tts['option'] = "认证" if flagTemp == 'true' else "不认证"
                            sql = 'update user_tag_info_{} set tag="{}" where user_id = {} and product_id ={};'.format(envdb.userRemainder, flagTemp, envdb.userId, pid)
                            print(sql)
                            envdb.cur.execute(sql)
                        elif request.data.get('way') == 'ocr':
                            project = '人脸识别'
                            envdb.db.select_db('customer_center')
                            tts['option'] = 'FACE' if request.data.get('flag') else 'WZ'
                            sql = 'update customer_ocr_provider_{} set provider="{}" where customer_id = {} and product_id ={};'.format(envdb.cusRemainder, tts['option'], envdb.customerId, pid)
                            print(sql)
                            envdb.cur.execute(sql)
                        tts['user_name'] = request.session['user'].get('realname')
                        tts['project'] = project
                        print(tts)
                        serializer_operate = TestToolsSerializerParam(data=tts)
                        if serializer_operate.is_valid():
                            print(1111)
                            serializer_operate.save()
                        return Response({"status": True, "message": "修改成功", "data": {}})
                    else:
                        return Response({"status": False, "message": "修改失败", "data": {}})
                else:
                    return Response({"status": False, "message": "用户不存在", "data": {}})
            else:
                return Response({"status": False, "message": "手机号输入有误", "data": {}})



class GetOperateCode(generics.GenericAPIView):
    """
       获取操作记录
    """
    serializer_class = TestToolsSerializerParam
    def post(self,request):
        print(11111)
        # code = TestTools.objects.all()
        codeList = []
        tempList = TestTools.objects.filter(env=request.data.get('env')).order_by('-id')[:20]
        ret = TestToolsSerializerParam(tempList, many=True)
        if tempList:
            # for i in ret.data:
            #     print(list(i.items())[0][1])
                # codeList.append({'id':i.id, 'user_name':i.user_name, 'product':i.product, 'project':i.project, 'operate_time':i.operate_time, 'phone':i.phone, 'option':i.option, 'env':i.env})
            return Response({"status": True, "message": "请求成功", "data": ret.data})
        else:
            return Response({"status": True, "message": "请求成功", "data": []})

class GetJkMongo(generics.GenericAPIView):
    """
       获取mongo数据
    """
    def get(self, request):
        from testtools.tools.des import Des
        serializer = MongoCodeSerializerParam(data=request.query_params)
        print(serializer.is_valid())
        if serializer.is_valid():
            userId = serializer.validated_data.get('userId')
            collection = serializer.validated_data.get('collection')
            db = serializer.validated_data.get('db')
            mg = MongoDB(dbname= db,collection=collection)
            dataList = []
            des = Des()
            print('userId=',userId)
            tempList = mg.col.find({"userId": userId}).sort('_id',-1).limit(10)
            print(tempList)
            if db == 'xinyongjin':
                for i in tempList:
                    response_originMessage = i.get('response', {}).get('body', {}).get('originMessage', '')
                    dataList.append({
                        '请求_originMessage':des.DesDecrypt2(i['request']['body']['originMessage']),
                        '响应_originMessage':des.DesDecrypt2(response_originMessage) if response_originMessage else '',
                        'tradeCode': i['tradeCode'],
                        'createAt': str(i['createAt'])[:19]
                    })
            elif db == 'hexin_central':
                code = 'serviceCode' if 'fund_adapter_packet' in collection else 'commandCode'
                for i in tempList:
                    # print(i)
                    response_originMessage = i.get('resDecryptMessage', '')
                    dataList.append({
                        '请求_originMessage':des.DesDecrypt2(i['reqDecryptMessage']),
                        '响应_originMessage':des.DesDecrypt2(response_originMessage) if response_originMessage else '',
                        'Code': i[code],
                        'createDate': str(i['createDate'])[:19]
                    })
            return Response({"status": True, "message": "请求成功", "data": dataList})
        return Response({"status": False, "message": "失败", "data": serializer.errors})

class GetCollections(generics.GenericAPIView):
    """
       获取当月collections
    """
    def get(self, request):
        serializer = MongoCollectionsSerializerParam(data=request.query_params)
        if serializer.is_valid():
            db = serializer.validated_data.get('db')
            mg = MongoDB(dbname=db)
            if db == 'xinyongjin':
                currentMonth = time.strftime("%Y%m",time.localtime())
            else:
                currentMonth = time.strftime("%Y_%m", time.localtime())
            print(currentMonth,type(currentMonth))
            collections = mg.db.collection_names()
            print(collections)
            print(type(collections))
            tempList = []
            for j in collections:
                if currentMonth in j:
                    if db == 'xinyongjin':
                        tempList.append(j)
                    else:
                        if 'fund' in j:
                            tempList.append(j)
            return Response({"status": True, "message": "查询成功", "data": tempList})
        else:
            return Response({"status": False, "message": "请求参数不合法", "data": serializer.errors})

class ClearRedisInfo(generics.GenericAPIView):
    """
       清理redis
    """
    serializer_class = RedisInfoSerializerParam
    def post(self, request):
        serializer = RedisInfoSerializerParam(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            env, dbNum, phone, project, product = data.get('env'),data.get('dbNum'), data.get('phone'),data.get('project'),data.get('product')
            redis = Redis(env, dbNum)
            envdb = DbTools(env, phone, product)
            if project == '借款验证码':
                try:
                    key = 'DYNAMIC_LIMIT_TIME_' + today() + '_' + str(envdb.userId)
                    print(key)
                    redis.cur.delete(key)
                    data = {
                        'user_name': request.session['user'].get('realname'),
                        'project': '借款验证码',
                        'option': '清除',
                        'phone': phone,
                        'env': env,
                        'product': product
                    }
                    serializer_operate = TestToolsSerializerParam(data=data)
                    if serializer_operate.is_valid():
                        print(1111)
                        serializer_operate.save()
                except:
                    return Response({"status": False, "message": "失败", "data": '用户不存在'})
            return Response({"status": True, "message": "处理成功", "data": ''})
        else:
            return Response({"status": False, "message": "请求参数不合法", "data": serializer.errors})