from testtools.tools.des import *
import json

class EnAndDecryption():
    def __init__(self):
        self.des = Des()
        self.wayList = [
            self.des.DesDecrypt,
            self.des.DesDecrypt2,
            self.des.DesDecrypt_GZIP,
            self.des.DesDecrypt_RSA,
            self.des.rsa_long_decrypt,
        ]
    def getdecode(self, data):
        # try:
        for i in self.wayList:
            try:
                ret = i(data.encode('utf-8'))
                if ret:
                    if str(ret, encoding="utf-8"):
                        try:
                            text = json.dumps(json.loads(str(ret, encoding="utf-8")), ensure_ascii=False, indent=4)
                        except:
                            text = str(ret, encoding="utf-8")
                    if text:
                        return text
            except:
                continue
        return '解密失败'
        # except:
        #     return '解密失败'
        # print(text)

if __name__ == '__main__':
    aa = EnAndDecryption()
    text = aa.getdecode('QYBnx4xqp0mdCFgewyzGUQ==')
    print(text)