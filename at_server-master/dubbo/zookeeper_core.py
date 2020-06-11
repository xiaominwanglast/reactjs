# -*- coding: utf-8 -*-

from kazoo.client import KazooClient
import urllib.parse
import re


class ZKCore:
    def __init__(self, env):
        if env == 'T1':
            self.host = '172.16.0.140'
            self.port = 2185
        elif env == 'T2':
            self.host = '172.16.0.142'
            self.port = 2185
        elif env == 'T3':
            self.host = '172.16.0.146'
            self.port = 2185

        self.zk = KazooClient(hosts='{0}:{1}'.format(self.host, self.port), read_only=True)
        self.zk.start()

    def get_providers(self, service_name):
        try:
            providers = self.zk.get_children("/dubbo/{0}/providers".format(service_name))
        except:
            return None, None

        if len(providers) <= 0:
            return None, None

        provider = urllib.parse.unquote(providers[0])
        provider = re.findall("dubbo://(.*?):(.*?)/", provider, re.I)[0]
        return provider

    def get_services(self):
        try:
            return self.zk.get_children("/dubbo/")
        except:
            return []


if __name__ == '__main__':
    ZK = ZKCore('T2')
    # print(ZK.get_providers("com.hexin.member.center.api.RegisterApi"))
    # print(ZK.get_services())

    from dubbo.dubbo_core import DubboCore

    count = 0
    for s in ZK.get_services():
        if s.startswith('com.hexin'):
            Host, Port =ZK.get_providers(s)
            conn = DubboCore(Host, Port)
            try:
                f = conn.ls(s)
                print(len(f),s,f)

                count += len(conn.ls(s))
            except:
                print("error",s)
            print('')
    print(count)
