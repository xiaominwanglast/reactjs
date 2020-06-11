import pymysql
from Tower.settings import SIT_DATABASE


class MySQLOperating:
    def __init__(self, env, database):
        if env == 'T1':
            if database == 'auto_loan_entry' or database == 'auto_loan_intserv':
                self.connection = pymysql.connect(host=SIT_DATABASE['T1_CDW']['host'],
                                                  user=SIT_DATABASE['T1_CDW']['user'],
                                                  password=SIT_DATABASE['T1_CDW']['pwd'],
                                                  database=database,
                                                  port=SIT_DATABASE['T1_CDW']['port'],
                                                  charset='utf8mb4',
                                                  cursorclass=pymysql.cursors.DictCursor)

            else:
                self.connection = pymysql.connect(host=SIT_DATABASE['T1']['host'],
                                                  user=SIT_DATABASE['T1']['user'],
                                                  password=SIT_DATABASE['T1']['pwd'],
                                                  port=SIT_DATABASE['T1']['port'],
                                                  database=database,
                                                  charset='utf8mb4',
                                                  cursorclass=pymysql.cursors.DictCursor)

        if env == 'T2':
            if database == 'auto_loan_entry' or database == 'auto_loan_intserv':
                self.connection = pymysql.connect(host=SIT_DATABASE['T2_CDW']['host'],
                                                  user=SIT_DATABASE['T2_CDW']['user'],
                                                  password=SIT_DATABASE['T2_CDW']['pwd'],
                                                  database=database,
                                                  port=SIT_DATABASE['T2_CDW']['port'],
                                                  charset='utf8mb4',
                                                  cursorclass=pymysql.cursors.DictCursor)
            else:
                self.connection = pymysql.connect(host=SIT_DATABASE['T2']['host'],
                                                  user=SIT_DATABASE['T2']['user'],
                                                  password=SIT_DATABASE['T2']['pwd'],
                                                  port=SIT_DATABASE['T2']['port'],
                                                  database=database,
                                                  charset='utf8mb4',
                                                  cursorclass=pymysql.cursors.DictCursor)

        if env == 'T3':
            if database == 'auto_loan_entry' or database == 'auto_loan_intserv':
                self.connection = pymysql.connect(host=SIT_DATABASE['T3_CDW']['host'],
                                                  user=SIT_DATABASE['T3_CDW']['user'],
                                                  password=SIT_DATABASE['T1_CDW']['pwd'],
                                                  database=database,
                                                  port=SIT_DATABASE['T3_CDW']['port'],
                                                  charset='utf8mb4',
                                                  cursorclass=pymysql.cursors.DictCursor)

            else:
                self.connection = pymysql.connect(host=SIT_DATABASE['T3']['host'],
                                                  user=SIT_DATABASE['T3']['user'],
                                                  password=SIT_DATABASE['T3']['pwd'],
                                                  port=SIT_DATABASE['T3']['port'],
                                                  database=database,
                                                  charset='utf8mb4',
                                                  cursorclass=pymysql.cursors.DictCursor)

    def execute(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def close(self):
        self.connection.close()
