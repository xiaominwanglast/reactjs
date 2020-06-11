# -*- coding: UTF-8 -*-

import ldap
from django.conf import settings
from ldap.controls import SimplePagedResultsControl


class ADUtil:
    def __init__(self, base_dn=settings.LDAP_BASE_DN):

        self.l = ldap.initialize(base_dn)

        self.l.protocol_version = ldap.VERSION3

        self.l.set_option(ldap.OPT_REFERRALS, 0)

    def auth(self, username, password):

        try:

            self.l.simple_bind_s(username + "@trump.local", password)

            base_dn = 'DC=trump,DC=local'
            searchScope = ldap.SCOPE_SUBTREE
            searchFiltername = "sAMAccountName"  # 通过samaccountname查找用户
            retrieveAttributes = None
            searchFilter = '(' + searchFiltername + "=" + username + '*)'
            ldap_result = self.l.search_s(base_dn, searchScope, searchFilter, retrieveAttributes)
            retdict = {}
            for k, v in ldap_result[0][1].items():
                # print k,v[0]
                retdict[k] = v[0]
            return 'OK', u'验证成功', retdict

        except:

            # logger.error('AUTH USER ERROR|%s|%s|' %(username, password), exc_info=1)

            return 'UNEXCEPTED_ERROR', u'未知错误', {}

    def get_all_users(self, username, password):

        base_dn = 'OU=上海二三四五网络科技有限公司,DC=trump,DC=local'
        self.l.simple_bind_s(username + "@trump.local", password)

        PAGE_SIZE = 500  # 设置每页返回的条数
        pg_ctrl = SimplePagedResultsControl(True, size=PAGE_SIZE, cookie="")
        userdata = []
        retdata=[]

        while True:
            msgid = self.l.search_ext(base_dn, ldap.SCOPE_SUBTREE, "(&(objectClass=person))", None,
                                      serverctrls=[pg_ctrl])
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
            for k, v in u[1].items():
                retdict[k] = v[0]
            retdata.append(retdict)
        return retdata


if __name__ == '__main__':
    n = ADUtil('ldap://trump.local')
    # print ret[2]['displayName']
    # print ret[2]['mail']
    # print ret[2]['distinguishedName']
