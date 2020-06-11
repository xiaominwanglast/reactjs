# -*- coding: UTF-8 -*-

import ldap

from ldap.controls import SimplePagedResultsControl


# from django.conf import settings


class ADUtil:
    def __init__(self, base_dn="ldap://trump.local"):

        self.l = ldap.initialize(base_dn)

        self.l.protocol_version = ldap.VERSION3

        self.l.set_option(ldap.OPT_REFERRALS, 0)

    def get_all_users(self, username, password):

        base_dn = 'OU=上海二三四五网络科技有限公司,DC=trump,DC=local'
        self.l.simple_bind_s(username + "@trump.local", password)

        PAGE_SIZE = 500  # 设置每页返回的条数
        pg_ctrl = SimplePagedResultsControl(True, size=PAGE_SIZE, cookie="")
        userdata = []

        while True:
            msgid = self.l.search_ext(base_dn, ldap.SCOPE_ONELEVEL, "(&(objectClass=*))", None, serverctrls=[pg_ctrl])
            _a, res_data, _b, srv_ctrls = self.l.result3(msgid)
            userdata.extend(res_data)
            cookie = srv_ctrls[0].cookie
            if cookie:
                pg_ctrl.cookie = cookie
            else:
                break
        print('totalnum:', len(userdata))
        for u in userdata:
            retdict = {}
            print(u[1])
            for k, v in u[1].items():
                # print k,v[0]
                retdict[k] = v[0]
            print(retdict)


if __name__ == '__main__':
    n = ADUtil('ldap://trump.local')
    # n=ADUtil('ldap://trump.local')
    ret = n.get_all_users('xxxx', 'xxxx')
    import json

    # print(json.dumps(ret[2], ensure_ascii=False))
    # print ret[2]['displayName']
    # print ret[2]['mail']
    # print ret[2]['distinguishedName']
