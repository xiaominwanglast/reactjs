# -*- coding: UTF-8 -*-

import base64
from pyDes import *
import io
import gzip
from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as pk
from Crypto.Hash import MD5, SHA


class Des():
    def __init__(self):
        self.key = "1qaz!@#$"
        self.iv = "\x01\x02\x03\x04\x05\x06\x07\x08"
        self.k = des(self.key, CBC, self.iv, pad=None, padmode=PAD_PKCS5)

        self.merchant_pub_key_test = '-----BEGIN RSA PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnIn2OR+oYWWn4KjIbcDkL+3oq9rOuggNHlAFsf/38Dmw0EbhKyULaryYEFqO2+HdnYmAAZSxj8itl5KhauZnMDCQj30LynzaxG8kd5wxZA2F0+AuHXvRaSbZkbjQKeJi+wgR7EtBRi6pQ6syDeHCB5ePBiZSMTlj0sBGU2B9SkeiMqY5qFfxo+gM0pr/N0SIvMH9nyFxxX9bB7h4/cyPhACSHR/D/iAZ+/+oOQjWaR/Maa+JG6EVSYaXPFSBVZN9piG41CAlPTiJLFvodZakIFKpsG5vFhhtYEjqwZcyA/wEk2fnR0QrUivQLShxBiizpn7R246PzzhCgqwUH9h+9QIDAQAB\n-----END RSA PUBLIC KEY-----'
        self.merchant_pri_key_test = '-----BEGIN RSA PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCcifY5H6hhZafgqMhtwOQv7eir2s66CA0eUAWx//fwObDQRuErJQtqvJgQWo7b4d2diYABlLGPyK2XkqFq5mcwMJCPfQvKfNrEbyR3nDFkDYXT4C4de9FpJtmRuNAp4mL7CBHsS0FGLqlDqzIN4cIHl48GJlIxOWPSwEZTYH1KR6IypjmoV/Gj6AzSmv83RIi8wf2fIXHFf1sHuHj9zI+EAJIdH8P+IBn7/6g5CNZpH8xpr4kboRVJhpc8VIFVk32mIbjUICU9OIksW+h1lqQgUqmwbm8WGG1gSOrBlzID/ASTZ+dHRCtSK9AtKHEGKLOmftHbjo/POEKCrBQf2H71AgMBAAECggEAcroqW3N4VOnMQDtzqfzVQMt823diS7Xa53x+sBaKAOZHUF6iaJyd4XyXdmTojv7bDbrYtk/kUx0hHRW6eD6lIgx15rQfECixrYZHk+JF0K6YhtCm+7Tjpc1zZ/mrlwb0xEcF28jL7kQEijPOW546NpY9nKQ5WRpWrv98i18MdIMmTciYvcurQfc/xsnAE1MiUK1387HGwLWq/Va4pSHgUIRlAoM5zKRMvQEmQGQJf32Mp6MNTwvsHh1NHiEWGKgeXMlofrkK8qNQDjFTWPOLk9cdsAI3RKrrTdQgX7uxeuwPGb7iHmiCwVkRGCrFSBA+MVyUeGB5skRJL2W+aNRgAQKBgQDIfGHRrlm/YFc0Bqsl96uIhpMGto8wa3i8WApaAX9LHRzozaUHQZhawJ5lp1P0WRuF8HKL3CuMqYVWJ6PEPFHZxZ4V5vkBeRY3vIbu9saWLoKP4bTOpO1KDcl9HYh2DIfBdvSXfbXzUCvgpF0Jiyx5PofG0pcXi69bJGSPGgvwwQKBgQDH4lxrWoCfAQlrJDuJnaP4r9/IK7eizzb+mzRmTH2s2lQckUTct0DVDkeo5Ipc14au/rKPJQ86Saenb9xK3IyPjhiAQsMk5dPZcd8HbQnZCKcTHjQLgzxHWPtYN0QGjFwpJ/k3wPijO6s+POum/wyRYSu2f+aoxYHDydGYDAJnNQKBgEEmcl9CSjXvp8bnV9y5tEtkeAjZcISqmAyUi6CeFfCh4FAi67sE7O6o45BjJNwlzNTkw0SB4sEOIZ9SuFw/wdWD65Bwg4CgCcFJCYxEM1qAeLsq/KeeXuIOwuhenYbHIaKT9n34QxVzex7AKt+8E1K/KD5LFwB2yyBSHj+GllTBAoGAIkTo2270xk4DM19O5dUlG6nrkAIOxdcI8rXhUfijQ1NbQFqXl8/DScPc/VPRdQFukeoQ6wHLjo66M7a16g/N+X6/LJ5FnrnYjFs9haRoH9Gf82MmQSMK3qCe1w0CmKzP0C6OR8TJ3BKK1WzUahkoKnSibfOXtC/Ig6zCRnMoplECgYEApjMhpVtdZdelfIPzhzWhKtJpCfe1vCpfnuXCcskf6FA72lZRv/NUqyxKauil4oZJh73Rm0dEDah8gUm2kAsUMAE66pZPGXjbWuafzD0OTcI3q/je1ouVlD6GkIG66/6i4lom1goR/bfzeE0FsR+n8xXa3vYNbgU7z8kTxBnJ3us=\n-----END RSA PRIVATE KEY-----'
        self.system_pub_key_test = '-----BEGIN RSA PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhBi6+a468xEg4xDaLJYo8ELf9rzSdPNnpNSQMwS5S2+kU7dZpSx0P+vE5xMz4XWp5kXhYY8faZO/xQPVVQRHkxv+R9YeEHX6wRVAOeJd2gWEeUTxJqahrCk9Djwl8Bx4Vve/Ac6VfRJtKG8h/dPDb+jfU01KIVsLgEHziV0Hiz6gyG4FFKbOtjWhYmr70+e9vLQRNZDpIAMOEw2zcZaNRpg2roZmr186sJIQzy04cDyTUXNrem6wviPQULHsQlAK1djT2R0z6roplh0kaKbvV/zMbMORTSqgpKq1g3/ZzBfq0Ro0y2ncCOKEqsO3cSzmzixckBwYCuORAcAdgJGEnwIDAQAB\n-----END RSA PUBLIC KEY-----'
        self.system_pri_key_test = '-----BEGIN RSA PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCEGLr5rjrzESDjENoslijwQt/2vNJ082ek1JAzBLlLb6RTt1mlLHQ/68TnEzPhdanmReFhjx9pk7/FA9VVBEeTG/5H1h4QdfrBFUA54l3aBYR5RPEmpqGsKT0OPCXwHHhW978BzpV9Em0obyH908Nv6N9TTUohWwuAQfOJXQeLPqDIbgUUps62NaFiavvT5728tBE1kOkgAw4TDbNxlo1GmDauhmavXzqwkhDPLThwPJNRc2t6brC+I9BQsexCUArV2NPZHTPquimWHSRopu9X/Mxsw5FNKqCkqrWDf9nMF+rRGjTLadwI4oSqw7dxLObOLFyQHBgK45EBwB2AkYSfAgMBAAECggEAUPyohbOgSK3Tr+MBIBzf9I3LqgaSMUmZ3aDE18Kpp+pGoVzkBTSAAUCXc+R+BliRVbC6QYnyBFSlWjDDdmAtUa/z8i8AN69dkUtqGRMD30tKsN7nyn6W2GpgGH4f9FpAHXG/FWiGlivZ6NRZzrkqNU5cvUHBlTmwj23f1fPHUEKt2Hh6iCwfWAixCu4fFaj3v5ezvjxghTwDzo0Im/W/WhdjCCtag90I1TYBnffCnK9guc7tW0Fd15bkKRmHvkomjui4O1kpiOJrFMOhekc+zoo27F/tElU9NYzhAz2rhJ3SDKPLNSrN3ZlPQreP+zCk9dqGllvbdXFdyj274PY8wQKBgQDSla2lBMMAYPe6eKlNZiUbVvTFWU2jCpKdzrgBqmoroyXIflU2KOp2n7cFHznk6V9uIQ5apBheAf0sdkemyB0sInH4tG86dJG89wwtCYkzOeNtHVZbcw0RAfc9FryhCxz2K7eoAAojhu3DgJ1CIGNEHudPzrHLEH5bRfOL6JWGhwKBgQCglb9Cn1Rtvh0YdX91KiW834UEAURGjsV59eK1xdvNHG8PKAWKpXL6O7q2Vk9TFzm5dH5nS4bdn7RkFsdwuiEZ7AJfdm13KuZq5MBXinzQSmLWT2iQFMSYQd55KcUkGJ2jDUbft6+5rWnuOPb2QPUPvvJL03gADh2gZGMy7I5/KQKBgQDOX0VXLP11h5H/OnSgl3PSATvLk6MUHy5kXMvTRhDaRv6mJ7iWZS6xpgAUku+HuHV/VgHdLmd66XQVeKzrc72zHOaYlytSHB8fEvTpxiig/SA2NMQGxw+NFWIYigm9wUhWr61ChRdqjbbBG3AB9/+QKMEDY0q1+Kn8BOeSuxKeTQKBgHdCHtN8fngt62/BuxGpZnNZUHDD/A+mcjP8Dw1NzsoKJtSLtWndK4F5IFXPzYN4yS7YvBM8fQFUXOTEIgOux2x34N9ClVMd8hdKoSmiOMV7qOFeAdqXAdXNfUpgYf9HpLJ15r+4q/FqPzRi683AOf8ioND9UK5BzXDTfPRRyBXZAoGAJzG+v1Nr4pRiH6s/3Te9n4mEe6+Sca5ZlbueuldbPjhSFVwAYnxElStL7DHnq6wGJhIKrAvUrluk/ZLVGtYbG54r0LMDMLErxem7hktU7weVu6/UNhIE/LgYJDW66YcVhNewR0g6RNeUzE8QP6Ij0Vk92fPcryy30MPmldlhv0A=\n-----END RSA PRIVATE KEY-----'

        self.merchant_pri_key_online = '-----BEGIN RSA PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDDGR1pD2KSlKJOCZxQ5sqp3kfXsuBQb5okxPz7oU3wl/AsGRWS7Cx9BeTe5GbRXJeUIx6r5Lb4QT8EJjCl0YWMcX5yX29XIrnU4o5V/rDhol7oUZk/HPleqYfHUTCG/L5dIN4xlcftzRDgL3yUF94sSTk24biBFdH4jeuwOEvJRYRZUIOdNgvvAFijSn0pnm4GA0V1GIwiitjpwOlVJKT1peoWH5JxjyINDLcPpglEr/gpEPAXbdPDaGRoOiWifPRf2uxuVu8oi4o27u1rL3qSECJ2lcPlhOdTSW9PYxW+kjnSCgSfj7r0Mbo5ErR2Clc4lLapH1xwJ1w7fAkCPUAzAgMBAAECggEAZfoqtU+lZpjqfX/ohSEdrczSIJ0PQvwSxkVxNtYJt0iz8VjrPfDVEESUbS1V0PllAbmZvp++Q+VW2wRbSVFLTS3FumLH//PWzr/dRnXqXwZQNX7xa1vpvOFAZ564jtZtaqBTg/eWmWYm/AfWRlJzfxKHJXi2yEJvjkwgdev3MSyKXiE35QJ1QMyRu36xKuCYuLnaWwWl6wjdi9P4Z3jXG0VoFKndz4bFyOElkoUpOWV6m4QM9FzLMpGONi2v6OFrBTL9svTn1sqhqRI9V9Yy/5G+mCe7jFMkSKgZTV6c9c7laIxBf5TrfZsSrGw9hPcRKroRq+lkC7xCphSYzFSogQKBgQD15XeXYwKJPq9BCnKgEKWqJVrhw03WwBUPGuZ3iVZUq+b+8r62b+5BE3tbBikn9WFpI1z9DrOdDmiqMHrm4iExjRH2DWwOBEt73waGAGWLUywY2NJYY3OAiiWOwhKpmzyEwXYrS61T4m28YcjSJ4y2gptTGbDV/pQM8ZdMIHARLQKBgQDLHU+7CZQL7lwxe8jSn5g+ueXTVjNx8R3XC5Vru2pdDSZSXyYhw+VaV2Dx82gbT+oW911RMU72YgqaPBUNFKVEgfhpAIY9e2YEJvl0YABCEJTlT/7Rlz3giidUfow/+8m56ViWKQe+0KuY3hy7UVN+Qt0T4bul+M6g8ArFAYGy3wKBgQC5PbvBHQJ9F+74xYEimkfjDK8RYosSG7QBpBc4uAqEUNf8+iu3zkyjU6TbJqH8iztt9AkKTnf6+i7Y/xqnMnUlGgwM24GqcYvX7mTAsC3PLsIKmdSkZ49Mp0Wx7PwYL20A6ak25pTVm79lahjaUJcNqwiOKs1v+I/ZzGpZHBqwpQKBgQC6G+d8h/BBZmzPYo7Gfzmu8AMoPCnzU212J8UH67gv/uaIP2rfMXIr7ziDOfbAX98soAe/Z6DknTz9yeO4EpzEQxrsi3B1UWZOk6+q9HQIFM15uGzSevRVlAEpqLK1xe43DRsArCPOscEp1wsYkBIi9P1BRGr+TxZ13LzhetnunQKBgQCRyig+2ZNFBUuvidRVll4MhFXMibqtJRcPRNtK7qiCjjhaEFy6rrLOrGe9za8ExGryWarFdLYvYzC2iLLRGdzVOMG3PLZEZvqIolkvVQNK15WqGDDEKE4xDnvbjDa4yIUcXoR1r+LSV93dj3IkjJINnDWo4Nr9LhN6/3jfs/UqZw==\n-----END RSA PRIVATE KEY-----'

        self.key2 = "cf410f84904a44cc8a7f48fc4134e8f9"[:24]
        self.k2 = triple_des(self.key2, ECB, padmode=PAD_PKCS5)

    def DesEncrypt(self, str):
        return base64.b64encode(self.k.encrypt(str))

    def DesDecrypt(self, str):
        return self.k.decrypt(base64.b64decode(str))

    def DesEncrypt_GZIP(self, str):
        buf = io.StringIO()
        f = gzip.GzipFile(mode='wb', fileobj=buf)
        try:
            f.write(str)
        finally:
            f.close()
        return self.DesEncrypt(base64.b64encode(buf.getvalue()))

    def DesDecrypt_GZIP(self, str):
        data = base64.b64decode(self.DesDecrypt(str))
        compressedstream = io.StringIO(data)
        gzipper = gzip.GzipFile(mode='rb', fileobj=compressedstream)
        return gzipper.read()

    def rsa_long_encrypt(self, pub_key_str, msg, length=100):
        """
        单次加密串的长度最大为 (key_size/8)-11
        1024bit的证书用100， 2048bit的证书用 200
        """
        pubobj = rsa.importKey(pub_key_str)
        pubobj = PKCS1_v1_5.new(pubobj)
        res = []
        for i in range(0, len(msg), length):
            res.append(pubobj.encrypt(msg[i:i + length]))
        return "".join(res)

    def rsa_long_decrypt(self, priv_key_str, msg, length=128):
        """
        1024bit的证书用128，2048bit证书用256位
        """
        privobj = rsa.importKey(priv_key_str)
        privobj = PKCS1_v1_5.new(privobj)
        res = []
        for i in range(0, len(msg), length):
            res.append(privobj.decrypt(msg[i:i + length], '无法解密 '))
        return "".join(res)

    def DesDecrypt_RSA(self, str, side, env):
        if side == 'client':
            if env == 'test':
                pri_key = self.merchant_pri_key_test

            if env == 'online':
                pri_key = self.merchant_pri_key_online
        else:
            if env == 'test':
                pri_key = self.system_pri_key_test
        crypto = base64.b64decode(str)
        return self.rsa_long_decrypt(pri_key, crypto, 256)

    def DesEncrypt_RSA(self, str, side, env):
        if side == 'client':
            if env == 'test':
                pub_key = self.merchant_pub_key_test
        else:
            if env == 'test':
                pub_key = self.system_pub_key_test
        msg = self.rsa_long_encrypt(pub_key, str, 200)
        return base64.b64encode(msg)

    def RSA_sign(self, content, side, env):
        if side == 'client':
            if env == 'test':
                pri_key = self.merchant_pri_key_test
        else:
            if env == 'test':
                pri_key = self.system_pri_key_test
        hash = MD5.new(content)
        signer = pk.new(rsa.importKey(pri_key))
        signn = signer.sign(hash)
        signn = base64.b64encode(signn)
        return signn

    def RSA_verify(self, source, sign, side, env):
        if side == 'client':
            if env == 'test':
                pub_key = self.merchant_pub_key_test
        else:
            if env == 'test':
                pub_key = self.system_pub_key_test
        pubkey = rsa.importKey(pub_key)
        signn = base64.b64decode(sign)
        verifier = pk.new(pubkey)
        return verifier.verify(SHA.new(source), signn)

    def DesEncrypt2(self, str):
        return base64.b64encode(self.k2.encrypt(str))


    def DesDecrypt2(self, str):
        return self.k2.decrypt(base64.b64decode(str))

    def unGzip(self,str_data):
        """
        :param str_data: 需要解压的内容
        :return: 解压后的内容
        """
        bs_data = base64.b64decode(str_data)
        compressed_stream = io.StringIO(bs_data)
        gzip_per = gzip.GzipFile(mode='rb', fileobj=compressed_stream)
        return gzip_per.read()

    def Gzip(self,str_data):
        """
        :param str_data: 需要压缩的内容
        :return: 压缩后的内容
        """
        buf = io.StringIO()
        f = gzip.GzipFile(mode='wb', fileobj=buf)
        try:
            f.write(str_data)
        finally:
            f.close()
        return base64.b64encode(buf.getvalue())

if __name__ == '__main__':
    des = Des()
    print(des.Gzip("asd"))


    # print des.DesDecrypt2("9gkQR54A8/u1wVR3NDpfEkgiINV6jRTkwTfrnPnAtNEOv9GenrVh7JO++7Z1WEmWYF/o2LNYGh41ZLD5BKtmfQ==")

    # print des.DesDecrypt(
    #     'Qj2hplJdxc1KqNPNbP7EpAQ39lxOTX2FnnxLJwzHhSDEUMdjf1JwDqFEAzGA yzuC8vXtWrofF2IElGew8vQivq6r1MXgxlR9HWehjbQezH+C56hGmGOm8FWf OSY+scW6f0/OriF6k/neLtw3rjI/O8/4NKlZ3/SNtptmrIqW+PSYybI1KDoo FY+HCmbR+4uHW6LZGX5Su+aPTfstngcoQAzcH19RtIaOlXE+i7YH1KXXBi1T 4Z45I1PNNGgQdBHeKDRAQwsrY0240D6zc2/DXS7Yo2kX3Z6Bd4N8dZ7Vs2eK QRSMv+fEqfr5PrEC1xTodNEWLKofEyu3d+n1ZEME/UN1vqsf26HNP1RQlw30 YEvknSR2Luvj7RE1fGrVX3S4IQRN4Yz+NPv95o1lUrpneCcg+ROmGRoKlAoW 66r/hNF4AW4oGuy0k5nLBIepRVD8Bjd1LjrTQJ55juz6FyvICYUCTwbtFxtt jpDO45Dt77g4Z8jS+6ejCW2eIs0aBP5xJ8ksihjzLL7a23t5TE5khbsznMjb Dpe2MfROW5rEhlkFVpbtfGCz2sJ+4JswOaVhvCuL4AMyTJfmxyzWfehTQGfE EeKdNP4MomHe1fW3gJMqxfv0YwlDvx8njyV7C7d+owczNW2h60A1Khiq+GT6 hQly2tj8h1q3KVTPlVzOrMntfvPYBPtdHDiW1X2W2FReVMWADwTgKfCUCd/6 ScLdeTl7SJCKcNDxitjZPGOWAkQ9MBpRuxT59RTAolZHBuHzsUANOdgpL/s+ kQivROM83K369pNMPvfGesOmvZQ+KVb4r1B32L+SCFSbll5KF/5fjKWps8Jb zfWvi9IerHBTGPaFnwcU8pMaraVK5BggsjRsDqQkRDfivecb1D1Wq1Dewiim Czb8kOyoiHuPovyOcXNXXbuTras0nn+bdvBNWkPnm8GtEoBXiCeCeckSuQwk Vce29PigaUfuiE2zrP6kbcSPILnwEjpxB/cVdN20eO42zjg3S27i9OSzMDwN 2S0gmBySNiDKwuDzo0fD1EiPHtclfsSnH3sYhEUBoZ28aDaHOcQfXo+PYw2M StKoasJuznimRvIQVMDAqjw05IIAOScSJ01qHVjyYu0qKk0I0/2DvvpiKWxO saW9T5DmZ56G')
    #
    # print des.DesEncrypt(
    #     '{"mobileApp":[{"appName":"喜马拉雅FM"},{"appName":"讯飞输入法"},{"appName":"小米风行播放插件"},{"appName":"WPS Office"},{"appName":"小米商城"},{"appName":"万能遥控"},{"appName":"小米PPTV播放器插件"},{"appName":"QQ"},{"appName":"微博"},{"appName":"小米视频追剧助手"},{"appName":"新闻资讯"},{"appName":"小米锁屏画报"},{"appName":"百度地图"},{"appName":"米家"},{"appName":"微信"},{"appName":"2345贷款王"},{"appName":"2345天气预报"},{"appName":"猎豹清理大师"},{"appName":"爱奇艺播放器"},{"appName":"TalkBack"},{"appName":"小米金融"},{"appName":"百度输入法小米版"},{"appName":"小米生活"},{"appName":"小米直播"},{"appName":"阅读"},{"appName":"语音设置"},{"appName":"贷款王极速版"},{"appName":"米聊"},{"appName":"视频电话"},{"appName":"KLO Bugreport"}]}')
    #
    # print des.DesDecrypt_GZIP(
    #     "eV7P7HhKzT3saTwGFiEHFSJ3lWV0+TenZkm7k5sW+2n8I1vE1vnRvZ1AHigg sz9Ur31rcLVB4nAc4J7WynWTRjk+CDYBjgtz/739VrmnGWfR5Wq6lJ0ArT8v y8LPQlwbFw14P+Tn3Ben0RPz77H5jbjLso/5l6CKKY0UguDguJXo9FBvJTgF fYaCgA0zop4Sk/FHnZYufdHYe/peRB7r5lHQc26flX9QqhSO8QjHmCMv44+d SN3yfJ7xDLeIKVyMhQFyvZorSQ97EZ0fsDX7nD+WwqnaH9tu0bYz2B915mdH 4N04+RDce+Dt73WHVxMHsGVhOC/fGaySUBRbNslZlkw+JVsYXkQaIhdMBKPZ ruGvSNAls0op2Xt3smG+VJVkQZglncgWZd4OfW5klBbpHHcV5SqcnEghHWsX KspKOBY/qS/d4197Hx9irxjrhMhMWIJxmyILnlgt4fx8xOhWmOIMTb4XuTvp yNXpGykETkMvfm82N/cPt309LqbFKVq2SUHy/K+ok70LkvEw1K0zw7H2k3IR Q4rU0hSO0ZZrYOyLXucta2ALnHenJUl58QFaSOcBrFqPv5jwXIrZy2L4gZ04 UttrXgO2QOexZPh+N7447ezo+DCnUalcm8DMepeQYM+j1XXYUzD52VURFzeN fGVYPKIZK+1YKiVF9tXOeT5ZFyDZXmRt2Y0bxJJ9dRTXmx8aZ3IXIQddvIOk S+rx2QqPaqr9WgoRdLw6xe/+O7tUS8sI2FgWRgpcULaL5j92KYwC1arFDWKN 2Avvhw9i6VW6G2gbmbSIJwmpC2DkRU36SFhMXvK0ZOGACdSzgPbacVtSAW2t RdFQ42lUtg+hw9zd7fFMwoKQj9womEj698etowsrWkQZncUBWERKCFUY1Xcy 4man11IX4FKdyfj0vnLfjtQFBCg5wtdK1wFuMc8dRbGeXkuRjXB/Xvb7aVRJ lIv0h9IQOxzslItMmR/ljQRrg2NHOQJ0mjYcMeaeoTbRMELJBMtC4uX6Neh5 lZYBAqr7tzqNQWNV4f2ZdPdRwRKyLtA85nwJwckpf434RqVfXaXONJ3vy1dA bRupduXEXx5X/Rv3YIicHjiugNuwWnEuXWTefoHmKG5QAUGS1h3Pw2wTe5V1 5pcFNre4wVRYtCx9C0UoHhfUeSmD+cr0HYtemer63XGXt6guKR1GFcR0xntF 9S27EsMWUW9L+xP5batgt6UE25oPK3p2yNyGEEzFxPHqWfX1dOGjFdu8BTcg iHqvO0BPCgFvQiAo0n/+9SjX/rypznOyzLjLshG/IVIQv691Wk2Ptkw3FfNL 8w8he20J/vxDsQqwZnvOR4eD7SweLZNMB/pPO9OIeZ/oL2bQEayETJTf7R/m 0YpWdLgt2+16dAtFD6AB/RRBzsaXrzfdgm+OBrXpjzbfxJ9IosDASZ3+Twz2 gF9wkhuZMm+BWJjI/2eAgvArV7mU5A3u91TUopComotAoPpTncp5tN5XOMIj oNdU2yIjn/3TDtNVoET8wGOploiBL7efsEG3pAV79B3U1Vw5VIay9tPzFSHs yG02E+cQ0NONUIPhCcOJ8/XieolezP604WQDzFIDtJx6dpWqa9A4s6if+W4f Jy2Iog8LTfiu+vF+OKkwPsmKz5NvLtUzK14qTL0BOH9wZaIC1mm3jC3etz4z +OiLsWg4/pxHStK/L2auD9PwvVVza0bMUWO75x+k/g29Gz2UjKWBZ3jvkC0P SjrGW52dDioR/xXziN9JJ0DKntdZU7YwYRiPsBQyXsGwda5esaeQ")
    #
    # print des.DesEncrypt_GZIP(
    #     '{"mobileApp":[{"appName":"喜马拉雅FM"},{"appName":"讯飞输入法"},{"appName":"小米风行播放插件"},{"appName":"WPS Office"},{"appName":"小米商城"},{"appName":"万能遥控"},{"appName":"小米PPTV播放器插件"},{"appName":"QQ"},{"appName":"微博"},{"appName":"小米视频追剧助手"},{"appName":"新闻资讯"},{"appName":"小米锁屏画报"},{"appName":"百度地图"},{"appName":"米家"},{"appName":"微信"},{"appName":"2345贷款王"},{"appName":"2345天气预报"},{"appName":"猎豹清理大师"},{"appName":"爱奇艺播放器"},{"appName":"TalkBack"},{"appName":"小米金融"},{"appName":"百度输入法小米版"},{"appName":"小米生活"},{"appName":"小米直播"},{"appName":"阅读"},{"appName":"语音设置"},{"appName":"贷款王极速版"},{"appName":"米聊"},{"appName":"视频电话"},{"appName":"KLO Bugreport"}]}')

    # print des.DesEncrypt_RSA("aaaaa")
    # print des.DesDecrypt_RSA(
    #     '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'
    #     , 'server','test')
    # print des.DesDecrypt_RSA(
    #     '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',
    #     'client','test')
    #
    # print des.DesDecrypt_RSA(
    #     'tW+JekNp22le7wb5QtvegpwBROb5blvM0CANdi7J3KpxYq+hBsZ6+LWJf+a92bjHinp/p2kUK6KXkMSTZzZUTnc6Eo7M7zLkrXQJnmiuFLZdFRQ461g2ElInU3qdIQkKQ3dkskjF4de5hEtT31bVKjP+yQ2HPCRjRN/7p1eBuqy0lbb6EJDa5t+pbscU6o34Ptx2fDMBXEdYI7aAt7mlgTob26w7gOXylBnfGB0O0smzWAmLXOqJhl8hhL3Pn1lQb3wkaaItGW//X7+/APyzvwimk/PFFe4qenOWa/RkXM36/csMgRVzK7SEySJhaeSlwt+B5kuFXpCUZMYnqPTfHGR0SZq4W9k+e+jby8Fbc6o41AgxhqsNTB/GLhRxm4Z6ASbFLdEy5wS6nTo3pqmi/P3WeFPW3hmaLm0zWjuBe/salQrixMBO9MgRiY+cuCGlEE312KuLuH2QKYeukIccIGnFaNpjJaS9JlnsS9dNG0ClqocjxFMuzAITWUThVvsJp1Zj7b3X6FHbzXWHmETvcVXvPkfneUHIH32lO6dgU5iRVFdziU5Z5+cuqgaBafmp4eHYeXyLvSvjnOhH1zy1wUfXAI/iepiLacnJvJ2JntKmCZS/cFl2KjRAs7xi7m7fYtyh0bsPhZN+BNHmsl4Lk0LJqX+PJh3g7gEG3h7vKVopewLrWzRcBvqkcBQrRjr09HFKBDZHV7Jw0irRFwwdP9+dIhUvyRAvL7rkANAzNV7GL6EDbzrwjiD9KpYXwbSFRdpI0AGl/FQo60ftB1Am307MzQ/gUklmY06TDK8IVOUnD4b8F2Z9cZRvfnevfU5PO0wEg/5cBdAEJrbdTFEziULu4xquzAxzffUOD3PvCIJbY8LG3I6VYWArKGHVDTCsTTPtmYWzZp6UZtg7QFCAAadnSydF7i83mWUqz9qYaZ7YiPzY35UHNaoKvIwjbqG/0QCjA01pnduv0EVlz0mpYtOIw7O9tQBrxGuB4n1npvVSuosIvR1Y0J2KULzv8iJh',
    #     'client','online')
    # print des.sign()
    # print des.verfity()
