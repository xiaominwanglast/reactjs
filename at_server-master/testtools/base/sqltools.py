import pymysql,os,sys,pymongo,redis
from testtools.base.config import dbInfo,productDict
from testtools.serializers import *
import time


def today():
    return time.strftime("%Y%m%d", time.localtime())


class DbTools():
    def __init__(self,env,phone,product = '2345借款'):
        # dbinfo = dbInfo[env]
        temp = UserDb.objects.filter(env=env)
        ret = UserDbSerializerParam(temp, many=True)
        dbinfo = ret.data[0]
        self.db = pymysql.connect(host = dbinfo['host'], port = dbinfo['port'], user = dbinfo['dbuser'], password = dbinfo['password'], autocommit = True)
        self.cur = self.db.cursor()
        self.phone = phone
        self.product = product
        self.getId()

    def getId(self):
        self.db.select_db('customer_center')
        sql = 'select a.id,b.id,b.prod_id from user a left join customer b on a.id = b.user_id where mobilephone_md5 = MD5({})'.format(self.phone)
        print(sql)
        self.cur.execute(sql)
        userInfo = self.cur.fetchall()
        if userInfo:
            self.userId = userInfo[0][0] #userid 用户
            self.userRemainder = self.userId % 100 % 20    #userid分表值
            self.customerId = userInfo[0][1] #立即贷对应的customerId
            self.cusRemainder = self.customerId % 100 % 20 #立即贷对应的customerId分表值
            self.customerIdPro = '' #产品对应的customerId
            self.cusRemainderPro = '' #产品对应的customerId分表值
            if len(userInfo) > 1:
                for i in userInfo:
                    if i[2] == productDict[self.product]['pid']:
                        self.customerIdPro = i[1]
                        self.cusRemainderPro = self.customerIdPro % 100 % 20
                        print(i[2],self.customerIdPro,self.cusRemainderPro)
                        self.isRegister = True
                if not self.customerIdPro:
                    self.isRegister = False
            elif len(userInfo) == 1:
                self.customerIdPro = self.customerId
                self.cusRemainderPro = self.cusRemainder
                self.isRegister = True
        else:
            self.isRegister = False

# db = DbTools('T3','18712370007')

class MongoDB():
    def __init__(self,env = 'T2', dbname = 'xinyongjin', collection = 'core_translation_201905'):
        self.host = '172.17.0.32' if env == 'T2' else '172.17.0.32'
        self.dbinfo = {
            'xinyongjin':{'password':"eGlueW9uZ2ppbgo=",'port':27017},
            'skynet':{'password':"c2t5bmV0QDIzNDUuY29t",'port':27018},
            'hexin_central':{'password':'hexin_central','port':27018},
        }
        print(dbname, collection)
        self.port = self.dbinfo[dbname]['port']
        self.conn = pymongo.MongoClient(self.host, self.port)
        self.db = self.conn[dbname]
        self.db.authenticate(dbname, self .dbinfo[dbname]['password'])
        self.col = self.db[collection]

class Redis():
    def __init__(self,env, dbNum=9):
        self._connectToRedis(env, dbNum)

    def _connectToRedis(self,env, dbNum):
        temp = RedisDbInfo.objects.filter(env=env)

        redisInfo = temp.values()[0]
        print(redisInfo, dbNum)
        if redisInfo:
            self.cur = redis.Redis(redisInfo['host'], port=redisInfo['port'], db=dbNum, password=redisInfo['password'])

