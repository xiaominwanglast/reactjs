import json
from testtools.base.ende import EnAndDecryption
from rest_framework import generics
from rest_framework.response import Response
from testtools.serializers import *
from testtools.tools.des import *

class Decryption(generics.GenericAPIView):
    """
        一键解密方法
    """
    serializer_class = DecryptSerializerParam
    def post(self, request):
        tempData = request.data.get('data')
        data = request.data.get('data').split('\n') if '\n' in tempData else request.data.get('data')

        # way = request.data.get('way')
        self.des = EnAndDecryption()
        text = []
        if data:
            if isinstance(data, list):
                for i,j in enumerate(data):
                    text.append(self.des.getdecode(j))
                # text = json.dumps(text, ensure_ascii=False, indent=4)
            else:
                text.append(self.des.getdecode(data))
        try:
            return Response({"status": True, "message": "请求成功", "data": text})
        except:
            return Response({"status": False, "message": "失败", "data": "失败"})

class Endecryption(generics.GenericAPIView):
    """
        单独加解密
    """
    serializer_class = EndecryptSerializerParam
    def post(self, request):
        text = request.data.get("data")
        text = text.encode('utf-8')
        type = request.data.get("type")
        print(text, type)
        des = Des()
        if type == 'encrypt':
            ret = des.DesEncrypt(text)
        elif type == 'decrypt':
            ret = des.DesDecrypt(text)
            print(ret)
            try:
                ret = json.dumps(json.loads(ret), indent=4)
                print(ret)
            except:
                pass
        elif type == 'decrypt_gzip':
            ret = des.DesDecrypt_GZIP(text)
            try:
                ret = json.dumps(json.loads(ret), indent=4)
            except:
                pass
        elif type == 'encrypt_gzip':
            ret = des.DesEncrypt_GZIP(text)
        elif type == 'decrypt_rsa':
            # msg = eval(text.encode('utf-8'))
            msg = text
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
                ret = json.dumps(ret, indent=4)
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
            ret = json.dumps(msg, indent=4)

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
                ret = json.dumps(ret, indent=4)
            except:
                pass


        elif type == 'encrypt2':
            ret = des.DesEncrypt2(text)
        elif type == 'decrypt2':
            ret = des.DesDecrypt2(text)
            try:
                ret = json.dumps(json.loads(ret), indent=4)
            except:
                pass
        elif type == 'gzip':
            ret = des.Gzip(text)
        elif type == 'upgzip':
            ret = des.unGzip(text)
            try:
                ret = json.dumps(json.loads(ret), indent=4)
            except:
                pass

        try:
            if ret:
                return Response({"status": True, "message": "成功", "data": ret})
            else:
                return Response({"status": False, "message": "失败", "data": ret})
        except:
            return Response({"status": False, "message": "失败", "data": ""})

