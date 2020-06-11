# -*- coding: UTF-8 -*-
import MySQLdb, time
from faker import Factory
import random, string


class TransData:
    def __init__(self, env):
        self.env = env

    def connect_db(self):

        if self.env == 'T1':
            conn = MySQLdb.connect(
                host='172.16.0.140',
                port=3306,
                user='test_dkw',
                passwd='test_dkw',
                db='xinyongjin',
                charset='utf8'
            )
            cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            self.conn = conn
            self.cur = cur
        elif self.env == 'T2':
            conn = MySQLdb.connect(
                host='172.16.0.142',
                port=3307,
                user='test_dkw',
                passwd='test_dkw',
                db='xinyongjin',
                charset='utf8'
            )
            cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            self.conn = conn
            self.cur = cur
        elif self.env == 'Dev':
            conn = MySQLdb.connect(
                host='172.17.16.53',
                port=3306,
                user='dev_ws',
                passwd='dev_ws',
                db='xinyongjin',
                charset='utf8'
            )
            cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            self.conn = conn
            self.cur = cur

    def disconnect_db(self):
        self.cur.close()
        self.conn.close()

    def insert_data(self, sql):
        self.connect_db()
        sign = self.cur.execute(sql)
        self.conn.commit()
        self.disconnect_db()
        return sign

    def query_data(self, sql):
        self.connect_db()
        self.cur.execute(sql)
        items = self.cur.fetchall()
        self.disconnect_db()
        return items

    def prepare_data(self, mobilephone):
        # s_user

        if mobilephone:
            phone = mobilephone
        else:
            phone = str(int(time.time() * 1000)+10000000000)[:11]
        fake = Factory.create('zh_CN')

        for i in range(100):
            person = fake.profile(fields=None, sex=None)
            if 1975 < int(person['ssn'][6:10]) < 1995 and int(person['ssn'][10:12]) not in [1, 2]:
                break
        bankcard = '620501' + ''.join(random.sample(string.digits, 10)) + ''.join(random.sample(string.digits, 3))
        idcard = person['ssn']

        print person
        user_name = person['name']

        sql = "INSERT INTO `xinyongjin`.`s_user`(`id`, `email`, `mobilephone`, `password`, `password_salt`, `deal_password`, `deal_password_salt`, `access_token`, `token`, `user_image`, `email_authentication`, `status`, `register_date`, `create_at`, `update_at`) " \
              "VALUES (NULL, NULL, '%s', 'BUm3yctZMqjyQ5adKWpoelTwPJU=', 'sYbr4coDK+hmYkcd//xn6Q==', 'fPm8hlE9TM5kx62SZ8hT2myQLNg=', NULL, NULL, '88BBD4ADC4352DB1CB71B3B1D2D9E68B1ED77DA29B214D7E042E63C7FE83D3A4', NULL, 0, 1, '2017-12-05 11:43:16', '2017-12-05 11:43:16', '2017-12-07 14:42:07');" % (
                  phone
              )
        self.insert_data(sql)

        sql = "select * from s_user where mobilephone='%s' order by id desc limit 1" % (phone)
        result = self.query_data(sql)
        user_id = result[0]['id']

        # s_user_identity
        sql = "INSERT INTO `xinyongjin`.`s_user_identity`(`id`, `user_id`, `identity_name`, `identity_card`, `apply_time`, `create_at`, `update_at`, `ocr`, `editType`) " \
              "VALUES (NULL, %s, '%s', '%s', '2018-02-05 17:14:13', '2018-02-05 17:14:13', NULL, 0, 0);" % (
                  user_id, user_name, idcard
              )
        self.insert_data(sql)

        # s_user_image_resource
        sql = "INSERT INTO `xinyongjin`.`s_user_image_resource`(`id`, `user_id`, `realname_front`, `realname_back`, `realname_user`, `realname_video`, `is_ocr_video`, `ftp_marker`, `apply_time`, `create_at`, `update_at`) " \
              "VALUES (NULL, %s, '/SL90001/48bdbca766962c6c9aa3/03/03-1--20171227180341.jpg', '/SL90001/48bdbca766962c6c9aa3/70/70-1--20171227180341.jpg', '/SL90001/48bdbca766962c6c9aa3/40/40-1--20171227180356.jpg', '/SL90001/48bdbca766962c6c9aa3/72/72-1--20171227180356.mp4', '0', 7, '2017-12-27 18:03:57', '2017-12-27 18:03:41', '2017-12-27 18:03:57');" % (
                  user_id
              )
        self.insert_data(sql)

        # s_user_bankcard

        sql = "INSERT INTO `xinyongjin`.`s_user_bankcard`(`id`, `user_id`, `bank_id`, `bankcard`, `mobilephone`, `card_province_id`, `card_city_id`, `apply_time`, `backcard_order`, `card_mode`, `create_at`, `update_at`) " \
              "VALUES (NULL, %s, 4, '%s', '%s', 2, 52, '2018-02-05 17:14:32', NULL, 1, '2018-02-05 17:14:31', NULL);" % (
                  user_id, bankcard, phone
              )
        self.insert_data(sql)

        # s_user_basic_info


        sql = "INSERT INTO `xinyongjin`.`s_user_basic_info`(`id`, `user_id`, `home_address`, `home_province`, `home_district`, `home_city`, `units_name`, `units_phone`, `units_address`, `units_province`, `units_city`, `units_district`, `relatives_name`, `relatives_phone`, `colleague_name`, `colleague_phone`, `friend_name`, `friend_phone`, `salary_date`, `apply_time`, `create_at`, `update_at`) " \
              "VALUES (NULL, %s, '金科路1220号13弄101室', 2, 500, 52, '自动生成账号有限公司', '010-55888666', '金科路1330号', 2, 52, 500, 'a家人', '18880000021', 'a同事', '18880000046', 'a朋友', '18880000018', NULL, '2017-12-28 09:10:38', '2017-12-28 09:10:37', '2017-12-28 09:10:38');" % (
                  user_id
              )
        self.insert_data(sql)

        # s_scorpio_user_record

        # vip_user
        sql = "INSERT INTO `xinyongjin`.`vip_user`(`id`, `user_id`, `product_id`, `mobile`, `transfer`, `group_id`) " \
              "VALUES (NULL, %s, 6, '%s', 0, 1);" % (
                  user_id, phone
              )
        self.insert_data(sql)

        # product_audit_status
        sql = "INSERT INTO `xinyongjin`.`s_user_product_audit_status`(`id`, `user_id`, `product_mst_id`, `contract_mst_id`, `admin_id`, `product_audit_id`, `audit_status`, `reason`, `reason_id`, `result_code`, `apply_progress`, `to_refuse_status`, `apply_time`, `approve_time`, `credit_status`, `create_at`, `update_at`) " \
              "VALUES (NULL, %s, 6, 18, NULL, 23779203, 190, NULL, NULL, NULL, 'apply-account-back', 1, '2017-12-28 09:16:43', '2017-12-28 09:23:46', NULL, '2017-12-28 09:16:43', '2017-12-28 09:42:03');" % (
                  user_id
              )
        print sql
        self.insert_data(sql)

        # s_user_finance_account
        sql = "INSERT INTO `xinyongjin`.`s_user_finance_account`(`id`, `user_id`, `sys_f_p_mst_id`, `loan_account_no`, `acct_status`, `period`, `repay_date`, `cre_lin_exp_date`, `acct_bal`, `base_tot_cre_line`, `base_rest_cre_line`, `base_used_cre_line`, `temp_tot_cre_line`, `temp_used_cre_line`, `temp_rest_cre_line`, `cre_line_status`, `open_status`, `credit_status`, `create_at`, `update_at`) " \
              "VALUES (NULL , %s, 6, '61712280923425240033', 90, NULL, NULL, NULL, NULL, 100000, 100000, NULL, NULL, NULL, NULL, 10, 1, 1, '2017-12-28 09:23:48', '2017-12-28 09:42:03');" % (
                  user_id
              )

        print sql
        try:
            self.insert_data(sql)
        except:
            print 'error..................'

        if self.env != 'Dev':
            # skynet_white_list
            sql = "INSERT INTO `skynet`.`skynet_white_list`(`id`, `id_no`, `phone_no`, `customer_type`, `overdue_rate`, `max_overdue_days`, `create_time`) " \
                  "VALUES (NULL, '%s', '%s', 'vip', 0.1000, 0, '2018-03-06 17:02:55');" % (
                      idcard, phone
                  )
            self.insert_data(sql)

        # identity_user
        sql = "INSERT INTO `xinyongjin`.`identity_user`(`id`, `user_id`, `identity_name`, `identity_card`, `mobile_phone`, `transfer`, `transfer_message`, `notify`, `batch_no`, `transfer_data`, `create_at`, `update_at`) " \
              "VALUES (NULL, %s, '%s', '%s', '%s', 0, '', 0, '', NULL, '2018-07-11 10:14:47', '2018-07-11 12:12:12');" % (
                  user_id, user_name, idcard, phone
              )
        print sql
        self.insert_data(sql)

        return phone, user_id, user_name, bankcard, idcard


if __name__ == '__main__':
    T = TransData('T1')
    T.prepare_data('')
