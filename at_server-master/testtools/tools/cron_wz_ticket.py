# -*- coding: utf-8 -*-
import requests, time, redis, datetime


def signTicket():
    try:
        requests.post('http://172.16.0.141:10045/memberCenterJob/updateAccessToken')
    except:
        print u'刷新报错'
        return ''


def WZ_ACC_TOKEN(env):
    if env == 'T1':
        host = "172.16.0.140"
        password = "sider"
        db = 6
        port = 6379
    elif env == 'T2':
        host = "172.16.0.142"
        password = "daikuanwang_webserver"
        db = 6
        port = 6382
    elif env == 'T3':
        host = "172.16.0.146"
        password = "sider"
        db = 6
        port = 6379
    elif env == 'Dev':
        host = "172.17.16.53"
        password = "sider"
        db = 6
        port = 6379
    elif env == 'K1':
        host = "172.17.0.3"
        password = "docker-redis"
        db = 6
        port = 6379

    T1pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
    T1conn = redis.StrictRedis(connection_pool=T1pool)
    return T1conn.get("WZ_ACC_TOKEN")


def WZ_SIGN_TICKET(env):
    if env == 'T1':
        host = "172.16.0.140"
        password = "sider"
        db = 6
        port = 6379
    elif env == 'T2':
        host = "172.16.0.142"
        password = "daikuanwang_webserver"
        db = 6
        port = 6382
    elif env == 'T3':
        host = "172.16.0.146"
        password = "sider"
        db = 6
        port = 6379
    elif env == 'Dev':
        host = "172.17.16.53"
        password = "sider"
        db = 6
        port = 6379
    elif env == 'K1':
        host = "172.17.0.3"
        password = "docker-redis"
        db = 6
        port = 6379
    T1pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
    T1conn = redis.StrictRedis(connection_pool=T1pool)
    return T1conn.get("WZ_SIGN_TICKET")


def set_token_ticket(env, token, ticket):
    if env == 'T1':
        host = "172.16.0.140"
        password = "sider"
        db = 6
        port = 6379
    elif env == 'T2':
        host = "172.16.0.142"
        password = "daikuanwang_webserver"
        db = 6
        port = 6382
    elif env == 'T3':
        host = "172.16.0.146"
        password = "sider"
        db = 6
        port = 6379
    elif env == 'Dev':
        host = "172.17.16.53"
        password = "sider"
        db = 6
        port = 6379
    elif env == 'K1':
        host = "172.17.0.3"
        password = "docker-redis"
        db = 6
        port = 6379

    T1pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
    T1conn = redis.StrictRedis(connection_pool=T1pool)
    T1conn.set("WZ_ACC_TOKEN", token)
    T1conn.set("WZ_SIGN_TICKET", ticket)


if __name__ == '__main__':

    old_minute = 1
    while True:
        token = []
        ticket = []

        token.append(WZ_ACC_TOKEN("T1"))
        token.append(WZ_ACC_TOKEN("T2"))
        try:
            token.append(WZ_ACC_TOKEN("T3"))
        except:
            pass
        try:
            token.append(WZ_ACC_TOKEN("Dev"))
        except:
            pass

        try:
            token.append(WZ_ACC_TOKEN("K1"))
        except:
            pass

        ticket.append(WZ_SIGN_TICKET("T1"))
        ticket.append(WZ_SIGN_TICKET("T2"))
        try:
            ticket.append(WZ_SIGN_TICKET("T3"))
        except:
            pass
        try:
            ticket.append(WZ_SIGN_TICKET("Dev"))
        except:
            pass
        try:
            ticket.append(WZ_SIGN_TICKET("K1"))
        except:
            pass

        token = list(set(token))
        print token
        ticket = list(set(ticket))
        print ticket

        if len(token) > 1 or len(ticket) > 1:
            signTicket()
            time.sleep(1)

            set_token_ticket("T1", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))
            set_token_ticket("T2", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))

            try:
                set_token_ticket("T3", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))
            except:
                pass

            try:
                set_token_ticket("Dev", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))
            except:
                pass
            try:
                set_token_ticket("K1", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))
            except:
                pass

            print u'不同步，触发更新了！'
        else:
            print u'不用更新'
            minute = datetime.datetime.today().minute
            print old_minute, minute
            if minute in [0, 10, 20, 30, 40, 50] and old_minute != minute:
                signTicket()
                time.sleep(1)

                set_token_ticket("T1", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))
                set_token_ticket("T2", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))

                try:
                    set_token_ticket("T3", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))
                except:
                    pass
                try:
                    set_token_ticket("Dev", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))
                except:
                    pass

                try:
                    set_token_ticket("K1", WZ_ACC_TOKEN("T1"), WZ_SIGN_TICKET("T1"))
                except:
                    pass
                print u'10分钟触发一次更新'
                old_minute = minute

        time.sleep(2)
