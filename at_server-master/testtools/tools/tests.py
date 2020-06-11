# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random, string
import requests
import json
import os
import random
import string
import MySQLdb


def aaa(db):
    conn = MySQLdb.connect(
        host='172.16.0.146',
        port=3308,
        user='test_dkw',
        passwd='test_dkw',
        db=db,
        charset='utf8'
    )
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute("show tables")
    items = cur.fetchall()
    data=[]
    for item in items:
        index = item.values()[0].split('_')[-1]

        try:
            index = str(int(index))
            table = '_'.join(item.values()[0].split('_')[:-1])+'_{x}'
        except:
            pass



        print item.keys()[0], item.values()[0]
        # print db, items


if __name__ == '__main__':

    listdbs = ['account_center_0', 'activity', 'alarm_center', 'api_center', 'api_gateway', 'apply_center',
               'batch_center', 'bi', 'bpa', 'bpa_101_center', 'call_center', 'call_inbound',
               'callcenter', 'chanpin_fenxi', 'collection', 'collection_activation', 'customer_center',
               'customer_service', 'daikuan_2345jr_com', 'daikuanwang_2345_com', 'datatransfer', 'db_hesuan1',
               'db_notice', 'dc_business', 'decision', 'dkwapp',
               'enterprise_member', 'esign', 'fk_fenxi', 'frontier_manager', 'growthcenter', 'hexin_base',
               'hexin_bill_0', 'hexin_business', 'hexin_callback', 'hexin_cat', 'hexin_cron',
               'hexin_fund_0', 'hexin_manager', 'hexin_proxy', 'hexin_rebalance', 'hexin_schedule', 'hexin_seal',
               'hexin_watcher', 'hexin_xiaodai', 'loan_center', 'ma', 'manage_center', 'market_center',
               'message_center', 'monitorcenter', 'ocean', 'operation', 'operation_coupon', 'performance_schema',
               'pms_account_register', 'pms_activation', 'pms_app_promotion', 'pms_apply', 'pms_loan', 'pms_login',
               'pms_manage', 'pms_open', 'pms_product_register', 'pms_register', 'product_center',
               'product_config_center', 'publiccms', 'scf_management', 'skynet', 'skynet_credit_line',
               'skynet_fact_material', 'skynet_geo', 'skynet_log', 'skynet_risk', 'skynet_rota', 'tickets', 'tms',
               'tripartite_center', 'ucenter', 'wcp', 'wfree_data_pro', 'wfree_loan_pro', 'wfree_member_pro',
               'xinyongjin', 'xinyongjin_channel']
    for db in listdbs:
        aaa(db)
