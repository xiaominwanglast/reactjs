# -*- coding: utf-8 -*-
import requests
import json
import os
import random
import string
import MySQLdb
from time import time


class Mysql_Object():

    def __init__(self, mobilephone):
        self.mobilephone = mobilephone
        # self.user_id = self.get_user_id()

    def connect_db_bs_iam(self):
        conn = MySQLdb.connect(
            host='180.101.195.217',
            port=5022,
            user='biz_data',
            passwd='C55DE2E68AA14F4B23528417E9A050FD',
            db='IAM',
            charset='utf8'
        )
        cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.conn = conn
        self.cur = cur


    def connect_db_ao_mc(self):
        conn = MySQLdb.connect(
            host='180.101.195.217',
            port=5022,
            user='biz_data',
            passwd='C55DE2E68AA14F4B23528417E9A050FD',
            db='AO',
            charset='utf8'
        )
        cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.conn = conn
        self.cur = cur


    def disconnect_db(self):
        self.cur.close()
        self.conn.close()

    def get_user_id(self):
        self.connect_db_bs_iam()
        self.cur.execute(
            "SELECT * FROM db_iam.s_user where mobilephone='%s';" % self.mobilephone)
        items = self.cur.fetchall()
        self.disconnect_db()
        return items[0]['id']

    def update_user_pwd(self):        
        sql="update s_user set password='%s',password_salt='%s',deal_password='%s' where mobilephone='%s';" % ('KeB73vEHCvSsaWcFv8N+NDBGsaE=','sXJY9vrlOooAX3m4R5WwWw==','fPm8hlE9TM5kx62SZ8hT2myQLNg=',self.mobilephone)
        print sql
        self.connect_db_bs_iam()
        sign= self.cur.execute(sql)
        self.conn.commit()
        self.disconnect_db()
        return sign

    # def get_register_not_idenity(self):
    #     self.connect_db_ao_mc()
    #     self.cur.execute(
    #         "select * from db_ao.s_user_finance where user_id='%s';" % self.user_id)
    #     items = self.cur.fetchall()
    #     self.disconnect_db()
    #     return items[0]['id']

if __name__ == '__main__':
    mysql = Mysql_Object(13810007232)
    print mysql.update_user_pwd()

