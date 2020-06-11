# -*- coding: utf-8 -*-
import requests
import json
import os
import random
import string
import MySQLdb
from time import time


class HX_Mysql_Object():

    def __init__(self, mobilephone):
        self.mobilephone = mobilephone
        # self.user_id,self.customer_id = self.get_user_id()

    def connect_db_test(self):
        conn = MySQLdb.connect(
            host='221.228.75.188',
            port=40030,
            user='mycat',
            passwd='mycat',
            db='db_hesuan',
            charset='utf8'
        )
        cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.conn = conn
        self.cur = cur

    def connect_db_test_bx(self):
        conn = MySQLdb.connect(
            host='221.228.75.188',
            port=40000,
            user='mycat',
            passwd='mycat',
            db='db_hesuan',
            charset='utf8'
        )
        cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.conn = conn
        self.cur = cur

    def connect_db_test_T1(self):
        conn = MySQLdb.connect(
            host='172.16.0.140',
            port=4000,
            user='mycat_hexin_test',
            passwd='ZGJfaGVzdWFuQGhleGluZGFpa3VTest=',
            db='db_hesuan',
            charset='utf8'
        )
        cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.conn = conn
        self.cur = cur

    def connect_db_test_T2(self):
        conn = MySQLdb.connect(
            host='172.16.0.142',
            port=4000,
            user='mycat_hexin_test',
            passwd='ZGJfaGVzdWFuQGhleGluZGFpa3VTest=',
            db='db_hesuan',
            charset='utf8'
        )
        cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.conn = conn
        self.cur = cur

    def connect_db_test_T3(self):
        conn = MySQLdb.connect(
            host='172.16.0.146',
            port=4000,
            user='mycat_hexin_test',
            passwd='ZGJfaGVzdWFuQGhleGluZGFpa3VTest=',
            db='db_hesuan',
            charset='utf8'
        )
        cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.conn = conn
        self.cur = cur
    def disconnect_db(self):
        self.cur.close()
        self.conn.close()

    def get_user_id(self):
        self.connect_db_test()
        self.cur.execute(
            "SELECT * from s_user_master where phone='%s';" % self.mobilephone)
        items = self.cur.fetchall()
        self.disconnect_db()
        return items[0]['id'],items[0]['customer_id']
    def get_user_id_bx(self):
        self.connect_db_test_bx()
        self.cur.execute(
            "SELECT * from s_user_master where phone='%s';" % self.mobilephone)
        items = self.cur.fetchall()
        self.disconnect_db()
        return items[0]['id'],items[0]['customer_id']

    def get_user_id_T1(self):
        self.connect_db_test_T1()
        self.cur.execute(
            "SELECT * from s_user_master where phone='%s';" % self.mobilephone)
        items = self.cur.fetchall()
        self.disconnect_db()
        return items[0]['id'],items[0]['customer_id']

    def get_user_id_T2(self):
        self.connect_db_test_T2()
        self.cur.execute(
            "SELECT * from s_user_master where phone='%s';" % self.mobilephone)
        items = self.cur.fetchall()
        self.disconnect_db()
        return items[0]['id'], items[0]['customer_id']

    def get_user_id_T3(self):
        self.connect_db_test_T3()
        self.cur.execute(
            "SELECT * from s_user_master where phone='%s';" % self.mobilephone)
        items = self.cur.fetchall()
        self.disconnect_db()
        return items[0]['id'], items[0]['customer_id']

    def update_user_bank(self,bank_card): 
        self.user_id,self.customer_id = self.get_user_id()  
        if bank_card=='0':
            bank_card='6222020111122220000'
        else:
            bank_card='6222020111122220001'

        sql="UPDATE s_user_sign_record set bank_card='%s',bank_code='0102',bank_name='中国工商银行' where user_id='%s'" % (bank_card,self.user_id)
        print sql
        self.connect_db_test()
        sign= self.cur.execute(sql)
        self.conn.commit()
        self.disconnect_db()

        sql="UPDATE s_user_product_bankcard set bank_card='%s',open_bank_name='中国工商银行' where user_id='%s'" % (bank_card,self.user_id)
        print sql
        self.connect_db_test()
        sign= self.cur.execute(sql)
        self.conn.commit()

        self.disconnect_db()
        return sign

    def update_user_bank_bx(self,bank_card):  
        self.user_id,self.customer_id = self.get_user_id_bx()  
        if bank_card=='0':
            bank_card='6222020111122220000'
        else:
            bank_card='6222020111122220001'

        sql="UPDATE s_user_sign_record set bank_card='%s',bank_code='0102',bank_name='中国工商银行' where user_id='%s'" % (bank_card,self.user_id)
        print sql
        self.connect_db_test_bx()
        sign= self.cur.execute(sql)
        self.conn.commit()
        self.disconnect_db()

        sql="UPDATE s_user_product_bankcard set bank_card='%s',open_bank_name='中国工商银行' where user_id='%s'" % (bank_card,self.user_id)
        print sql
        self.connect_db_test_bx()
        sign= self.cur.execute(sql)
        self.conn.commit()

        self.disconnect_db()
        return sign

    def update_user_bank_T1(self, bank_card):
        self.user_id, self.customer_id = self.get_user_id_T1()
        if bank_card == '0':
            bank_card = '6222020111122220000'
        else:
            bank_card = '6222020111122220001'

        sql = "UPDATE s_user_sign_record set bank_card='%s',bank_code='0102',bank_name='中国工商银行' where user_id='%s'" % (
        bank_card, self.user_id)
        print sql
        self.connect_db_test_T1()
        sign = self.cur.execute(sql)
        self.conn.commit()
        self.disconnect_db()

        sql = "UPDATE s_user_product_bankcard set bank_card='%s',open_bank_name='中国工商银行' where user_id='%s'" % (
        bank_card, self.user_id)
        print sql
        self.connect_db_test_T1()
        sign = self.cur.execute(sql)
        self.conn.commit()
        self.disconnect_db()
        return sign

    def update_user_bank_T2(self, bank_card):
        self.user_id, self.customer_id = self.get_user_id_T2()
        if bank_card == '0':
            bank_card = '6222020111122220000'
        else:
            bank_card = '6222020111122220001'

        sql = "UPDATE s_user_sign_record set bank_card='%s',bank_code='0102',bank_name='中国工商银行' where user_id='%s'" % (
            bank_card, self.user_id)
        print sql
        self.connect_db_test_T2()
        sign = self.cur.execute(sql)
        self.conn.commit()
        self.disconnect_db()

        sql = "UPDATE s_user_product_bankcard set bank_card='%s',open_bank_name='中国工商银行' where user_id='%s'" % (
            bank_card, self.user_id)
        print sql
        self.connect_db_test_T2()
        sign = self.cur.execute(sql)
        self.conn.commit()
        self.disconnect_db()
        return sign

    def update_user_bank_T3(self, bank_card):
        self.user_id, self.customer_id = self.get_user_id_T3()
        if bank_card == '0':
            bank_card = '6222020111122220000'
        else:
            bank_card = '6222020111122220001'

        sql = "UPDATE s_user_sign_record set bank_card='%s',bank_code='0102',bank_name='中国工商银行' where user_id='%s'" % (
            bank_card, self.user_id)
        print sql
        self.connect_db_test_T3()
        sign = self.cur.execute(sql)
        self.conn.commit()
        self.disconnect_db()

        sql = "UPDATE s_user_product_bankcard set bank_card='%s',open_bank_name='中国工商银行' where user_id='%s'" % (
            bank_card, self.user_id)
        print sql
        self.connect_db_test_T3()
        sign = self.cur.execute(sql)
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
    mysql = HX_Mysql_Object(13600738937)
    print mysql.update_user_bank_T1('0')

