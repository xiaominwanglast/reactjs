# -*- coding: utf-8 -*-
import requests,time


def login(env,u,p):
    try:
        response=requests.post('http://{0}-managerdaikuan.2345.com/ucenter-server/userCenter/login'.format(env),
                      json={"username": u, "password": p})
        print env,response.text
        return response.cookies.get('jsid')
    except:
        return ''

def refresh(env,u,token):
    try:
        res=requests.get(
            'http://{0}-managerdaikuan.2345.com/ma-server/login?username={1}&token={2}'.format(env,u,token))
        print env,res.text
        if int(res.json().get('errorMsg').get('errCode')) == 0:
            return True
        else:
            return False

    except:
        print env,'error'
        return False


if __name__ == '__main__':

    token1 = ''
    token2 = ''
    token3 = ''
    tokenpre = ''


    while True:

        if not refresh('t1', 'autotest' , token1):

            token1 = login('t1', 'autotest', 'MTIzNDU2')

        if not refresh('t2', 'autotest' , token2):

            token2 = login('t2', 'autotest', 'MTIzNDU2')


        time.sleep(300)