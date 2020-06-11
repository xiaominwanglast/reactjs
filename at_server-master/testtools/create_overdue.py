# -*- coding: utf-8 -*-
__author__ = "dpeng_Fan"

import pymysql
from rest_framework import generics,views
from rest_framework.response import Response
from testtools.serializers import *
from testtools.base.config import productDict

class OverDue(generics.GenericAPIView):
    """
       手机号造逾期
    """
    serializer_class = OverdueLog
    def post(self,request):
        env, prod_id, mobilephone, borrowdays, period_id = request.data.get('env'), request.data.get('prod_id'), request.data.get(
            'mobilephone'), request.data.get('borrowdays'), request.data.get('period_id')
        product = prod_id
        prod_id = productDict[prod_id]['pid']
        print(env, prod_id, mobilephone, borrowdays, period_id)
        if len(mobilephone) == 11:
            db = conn_Mysql(env)
            if not db.check_mobileExist(mobilephone)[0] or not db.get_uid_cid(mobilephone,prod_id)[0]:
                return Response({"status": False, "message": "手机号未注册，请注册借款后再试。", "data": {}})
            if not db.get_borrowinfoquery(prod_id)[0]:
                return Response({"status": False, "message": "当前状态不是待还款状态，请借款后再试。", "data": {}})
            db.update_hexin_bill_loan_info(borrowdays,period_id,prod_id)
            db.update_hexin_bill_repay_plan_info(period_id,borrowdays,prod_id)
            db.update_loan_center_order(borrowdays,period_id,prod_id)
            db.update_loan_center_order_history(borrowdays,period_id,prod_id)
            db.close_connect()
            data = {
                'user_name':request.session['user'].get('realname'),
                'project':'借款状态',
                'option':'逾期',
                'phone':mobilephone,
                'env':env,
                'product':product
            }
            serializer_operate = TestToolsSerializerParam(data=data)
            if serializer_operate.is_valid():
                print(1111)
                serializer_operate.save()
            return Response({"status": True, "message": "手机号状态已更改为逾期。", "data": {}})
        else:
            return Response({"status": False, "message": "手机号不是11位，请重新输入。", "data": {}})

class conn_Mysql(object):

    def __init__(self,env):
        temp = UserDb.objects.filter(env=env)
        ret = UserDbSerializerParam(temp, many=True)
        self.db_conf = ret.data[0]
        self.conn = pymysql.connect(
            host = self.db_conf["host"],
            port = self.db_conf["port"],
            user = self.db_conf["dbuser"],
            passwd = self.db_conf["password"],
            charset = "utf8"
        )
        self.cursor = self.conn.cursor()

    def check_mobileExist(self,mobilephone):
        sql = "SELECT *FROM customer_center.`user` WHERE mobilephone_md5 = MD5({0});".format\
            (mobilephone)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        try:
            if len(data) != 0:
                return True,
            else:
                return False, Response({"status": False, "message": "手机号未注册，请注册借款后再试。", "data": {}})

        except Exception:
            return False,Response({"status": False, "message": "手机号未注册，请注册借款后再试。", "data": {}})

    def get_borrowinfoquery(self,prod_id):
        sql = "select order_status from loan_center.order_{0} where customer_id = {1} AND product_id={2};".format\
            (self.get_cid_mod_num,self.cid2,prod_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        try:
            if data[0][0] ==106:
                return True,

        except Exception:
            return False,Response({"status": False, "message": "当前状态不是待还款状态，请借款后再试。", "data": {}})


    def get_uid_cid(self,mobilephone,prod_id):
        try:
            sql = "select * from customer_center.customer a join customer_center.user b on a.user_id = b.id WHERE " \
                  "b.mobilephone_md5 = MD5({0}) AND a.prod_id={1};".format(mobilephone,prod_id)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if len(data) == 1:
                self.uid,self.cid1,self.cid2 = data[0][1],data[0][-1],data[0][0]
                return True,self.uid,self.cid1,self.cid2
            else:
                return False,Response({"status": False, "message": "手机号未注册，请注册借款后再试。", "data": {}})
        except Exception:
            print("查询uid和cid失败！")

    @property
    def get_uid_mod_num(self):
        uid_mod_num =self.uid % 20
        return uid_mod_num

    @property
    def get_cid_mod_num(self):
        cid_mod_num =self.cid2 % 20
        return cid_mod_num

    def update_hexin_bill_loan_info(self,borrowdays,period_id,prod_id):
        # try:
        print(self.get_uid_mod_num,borrowdays-1,borrowdays,period_id,borrowdays,self.uid,prod_id)
        sql = "UPDATE hexin_bill_{0}.`loan_info`  set `begin_interest_date`=TIMESTAMPADD(DAY,-{1},curdate()),`interest_date`= TIMESTAMPADD(DAY,-{2},curdate()),`borrow_approve_date`=TIMESTAMPADD(DAY,-{2},curdate()),`next_repay_date`= TIMESTAMPADD(DAY,{3}-{2},curdate()),`last_overdue_start_date`=TIMESTAMPADD(DAY,{3}-{4}+1,curdate()) where `user_id`={5} AND interest_status = 1 and prod_id = {6}; ".format(self.get_uid_mod_num,borrowdays-1,borrowdays,period_id,borrowdays,self.uid,prod_id)
        print(sql)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data
        # except Exception:
        #     print('更新hexin_bill_loan_info表失败')

    def update_hexin_bill_repay_plan_info(self,period_id,borrowdays,prod_id):
        try:
            sql = "UPDATE hexin_bill_{0}.`repay_plan_info`  set `repay_date`=TIMESTAMPADD(DAY,{1}-{2},curdate())," \
                  "`interest`=0,overdue_interest=0,overdue_penalty=0,breach_penalty=0,grace_period_overdue_penalty=0 " \
                  "where `user_id`={3} AND stage_ret != 2 and prod_id = {4};  ".format(self.get_uid_mod_num,period_id,
                                                                                       borrowdays,self.uid,prod_id)
            print(sql)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception:
            print('更新hexin_bill_repay_plan_info表失败')

    def update_loan_center_order(self,borrowdays,period_id,prod_id):
        try:
            sql = "UPDATE loan_center.`order_{0}`  set `borrow_date`=TIMESTAMPADD(DAY,-{1},NOW()), " \
                  "`process_date`= TIMESTAMPADD(DAY,-{1},NOW()), `expiry_date`=TIMESTAMPADD(DAY,{2}-{1},curdate())" \
                  " where `customer_id`={3} AND  product_id = {4}; ".format(self.get_cid_mod_num,
                                                                            borrowdays,period_id,self.cid2,prod_id)
            print(sql)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception:
            print('更新loan_center_order表失败')

    def update_loan_center_order_history(self,borrowdays,period_id,prod_id):
        try:
            sql = "UPDATE loan_center.`order_history_{0}`  set `borrow_date`=TIMESTAMPADD(DAY,-{1},NOW()), " \
                  "`process_date`= TIMESTAMPADD(DAY,-{1},NOW()),`expiry_date`=TIMESTAMPADD(DAY,{2}-{1},curdate())" \
                  "where `customer_id`={3} AND  product_id = {4} and order_status = 106;  ".format(self.get_cid_mod_num,
                                                                                                   borrowdays,period_id, self.cid2,prod_id)
            print(sql)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception:
            print('更新loan_center_order_history表失败')

    def close_connect(self):
        '''关闭数据连接'''
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
