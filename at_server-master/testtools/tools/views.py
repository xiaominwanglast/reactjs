# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

from tools.transdata import *
from tools.des import *
from tools.mydb import *
from tools.models import *
from users import usercore
import json
from jenkins_core import Jenkins_Core
from web.render_template import mail_template
from send_mail import send_mail_core
from ssh_core import SSH_Core
from tools.hxdb import *
from bson.objectid import ObjectId
from isodate import parse_datetime as ISODate
from tools.create_credit import create_credit

login = usercore.Login()
des = Des()


def encrypt_or_decrypt(request):
    text = request.POST.get("text")
    type = request.POST.get("type")
    print 11111, type

    if type == 'encrypt':
        ret = des.DesEncrypt(text.encode('utf-8'))
    elif type == 'decrypt':
        ret = des.DesDecrypt(text.encode('utf-8'))
        try:
            ret = json.dumps(json.loads(ret), indent=4, sort_keys=False, ensure_ascii=False)
        except:
            pass
    elif type == 'decrypt_gzip':
        ret = des.DesDecrypt_GZIP(text.encode('utf-8'))
        try:
            ret = json.dumps(json.loads(ret), indent=4, sort_keys=False, ensure_ascii=False)
        except:
            pass
    elif type == 'encrypt_gzip':
        ret = des.DesEncrypt_GZIP(text.encode('utf-8'))



    elif type == 'decrypt_rsa':

        msg = eval(text.encode('utf-8'))

        if 'response' in msg:

            try:
                request = msg['request']['body']['encryptMessage']
                request = des.DesDecrypt_RSA(request, 'server', 'test')
                request = json.loads(request)
            except:
                request = None

            try:
                response = msg['response']['body']['encryptMessage']
                response = des.DesDecrypt_RSA(response, 'client', 'test')
                response = json.loads(response)
            except:
                response = None

        else:

            try:
                request = msg['request']['body']['encryptMessage']
                request = des.DesDecrypt_RSA(request, 'client', 'test')
                request = json.loads(request)
                response = None
            except:
                request = None

        ret = {u'request请求################################': request,
               u'response响应################################': response}

        try:
            ret = json.dumps(ret, indent=4, sort_keys=False, ensure_ascii=False)
        except:
            pass
    elif type == 'encrypt_rsa':
        msg = json.loads(text.encode('utf-8'))
        originMessage = str(msg['body']['originMessage'].encode('utf-8'))
        encode_str = des.DesEncrypt_RSA(originMessage, 'server', 'test')
        encode_sign = des.RSA_sign(originMessage, 'client', 'test')
        msg['body']['originMessage'] = None
        msg['body']['encryptMessage'] = encode_str
        msg['body']['signatureMessage'] = encode_sign
        msg['header']['isEncrypt'] = 'Y'
        msg['header']['isSign'] = 'Y'
        ret = json.dumps(msg, indent=4, sort_keys=False, ensure_ascii=False)

    elif type == 'decrypt_rsa_online':

        msg = eval(text.encode('utf-8'))

        if 'response' in msg:

            try:
                request = msg['request']['body']['encryptMessage']
                request = des.DesDecrypt_RSA(request, 'server', 'online')
                request = json.loads(request)
            except:
                request = None

            try:
                response = msg['response']['body']['encryptMessage']
                response = des.DesDecrypt_RSA(response, 'client', 'online')
                response = json.loads(response)
            except:
                response = None

        else:

            try:
                request = msg['request']['body']['encryptMessage']
                request = des.DesDecrypt_RSA(request, 'client', 'online')
                request = json.loads(request)
                response = None
            except:
                request = None

        ret = {u'request请求################################': request,
               u'response响应################################': response}

        try:
            ret = json.dumps(ret, indent=4, sort_keys=False, ensure_ascii=False)
        except:
            pass


    elif type == 'encrypt2':
        ret = des.DesEncrypt2(text.encode('utf-8'))
    elif type == 'decrypt2':
        ret = des.DesDecrypt2(text.encode('utf-8'))
        try:
            ret = json.dumps(json.loads(ret), indent=4, sort_keys=False, ensure_ascii=False)
        except:
            pass
    elif type == 'gzip':
        ret = des.Gzip(text.encode('utf-8'))
    elif type == 'upgzip':
        ret = des.unGzip(text.encode('utf-8'))
        try:
            ret = json.dumps(json.loads(ret), indent=4, sort_keys=False, ensure_ascii=False)
        except:
            pass

    return JsonResponse({"code": 1, "data": ret})


@login.is_login
def reset_pwd(request):
    mobilephone = request.POST.get("mobilephone")

    if len(Reset_Logs.objects.filter(account=mobilephone.strip())):
        return JsonResponse({"code": -2, "data": {}})

    mysql = Mysql_Object(mobilephone)
    try:
        sign = mysql.update_user_pwd()
    except:
        sign = -1

    if sign == 1:
        Reset_Logs.objects.create(username=request.myuser.username,
                                  displayname=request.myuser.displayname,
                                  account=mobilephone.strip(),
                                  desc='',
                                  status=1)
    return JsonResponse({"code": sign, "data": {}})


def get_reset_logs():
    return Reset_Logs.objects.all().order_by('-id')


@login.is_login
def publish_server(request):
    job_name = request.GET.get("job_name")
    job_params = request.GET.get("job_params")

    JK = Jenkins_Core('http://172.16.23.49:8001/jenkins', 'testteam', '123456')
    job_params = json.loads(job_params)
    sign, msg, data = JK.build_job(job_name, job_params)
    # sign,msg,data=(1,"",{"changelogs":[],"build_info":["asd","asda","345"]})
    if sign != -99:
        mail_html = mail_template(request, data)
        send_mail_core("chengm@2345.com," + request.myuser.email, 'T1环境-AO重新发布', mail_html)
    return JsonResponse({"code": sign, "msg": msg})


@login.is_login
def restart_server(request):
    job_name = request.GET.get("job_name")
    env = request.GET.get("env")
    SSH = SSH_Core()
    data = SSH.restart_server(job_name, env)
    return JsonResponse({"code": 1, "msg": "重启完成", "data": data})


def hx_update_bank(request):
    mobilephone = request.GET.get("mobilephone")
    env = request.GET.get("env", "uat")
    bankcard = request.GET.get("bankcard", "0")
    HXObject = HX_Mysql_Object(mobilephone)
    if env == 'uat':
        HXObject.update_user_bank(bankcard)
    elif env == 'T1':
        HXObject.update_user_bank_T1(bankcard)
    elif env == 'T2':
        HXObject.update_user_bank_T2(bankcard)
    elif env == 'T3':
        HXObject.update_user_bank_T3(bankcard)
    elif env == 'bx':
        HXObject.update_user_bank_bx(bankcard)
    return JsonResponse({"code": 1, "msg": "完成"})


@login.is_login
def account_fake(request):
    mobilephone = request.GET.get("mobilephone")
    env = request.GET.get("env")

    transdata = TransData(env)
    phone, user_id, user_name, bankcard, idcard = transdata.prepare_data(mobilephone)
    if phone:
        Account_Fake_Logs.objects.create(username=request.myuser.username,
                                         displayname=request.myuser.displayname,
                                         account=phone,
                                         desc='【{5}】 用户id:{0},手机号:{1},姓名:{2},银行卡:{3},身份证:{4}'.format(user_id, phone,
                                                                                                     user_name,
                                                                                                     bankcard, idcard,
                                                                                                     env),
                                         status=1)
        return JsonResponse({"code": 1, "msg": "完成"})
    else:
        return JsonResponse({"code": 0, "msg": "失败"})


def get_account_fake_logs():
    return Account_Fake_Logs.objects.all().order_by('-id')


@login.is_login
def create_cardid(request):
    cardid = request.GET.get("cardid")
    name = request.GET.get("name")
    create = create_credit(cardid=cardid,name=name)
    name, gander, birthday_y, birthday_m, birthday_d, cardid_new, address_new_1, address_new_2 = create.create_all()
    national = "汉"
    # print cardid_new, cardid_new[:-6], cardid_new[-6:]
    cardid_new_tab = cardid_new[:-6] + ' ' + cardid_new[-6:]
    if cardid_new:
        # print "tools.view.list:", name, gander, birthday_y, birthday_m, birthday_d, cardid_new, address_new_1, address_new_2
        try:
            Create_Cardid_Logs.objects.create(username=request.myuser.username,
                                              displayname=request.myuser.displayname,
                                              account=cardid_new,
                                              desc='姓名:{0},性别:{1},{2}年{3}月{4}日,身份证:{5},民族:{6},地址:{7}{8}'.format(name,
                                                                                                                gander,
                                                                                                                birthday_y,
                                                                                                                birthday_m,
                                                                                                                birthday_d,
                                                                                                                cardid_new_tab,
                                                                                                                national,
                                                                                                                address_new_1,
                                                                                                                address_new_2),
                                              status=1)
        except:
            pass


        return JsonResponse(
            {"code": 1, "name": name, "gander": gander, "birthday_y": birthday_y, "birthday_m": birthday_m,
             "birthday_d": birthday_d, "cardid_new": cardid_new, "address_new_1": address_new_1,
             "address_new_2": address_new_2, "national": national})
    else:
        return JsonResponse({"code": 0, "msg": "失败"})


def get_create_cardid_logs():
    return Create_Cardid_Logs.objects.all().order_by('-id')[:300]
