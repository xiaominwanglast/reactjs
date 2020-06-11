# -*- coding: utf-8 -*-

import json
import socket
import telnetlib


class DubboCore:
    # 定义私有属性
    __init = False
    __encoding = "gbk"
    __finish = b'dubbo>'  # 基于python3修改
    __connect_timeout = 10
    __read_timeout = 10

    # 定义构造方法
    def __init__(self, host, port):
        self.host = host
        self.port = port
        if host is not None and port is not None:
            self.__init = True

    def set_finish(self, finish):
        '''
        defualt is ``dubbo>``
        '''
        self.__finish = finish

    def set_encoding(self, encoding):
        '''
        If ``result retured by dubbo`` is a ``str`` instance and is encoded with an ASCII based encoding
        other than utf-8 (e.g. latin-1) then an appropriate ``encoding`` name
        must be specified. Encodings that are not ASCII based (such as UCS-2)
        are not allowed and should be decoded to ``unicode`` first.
        '''
        self.__encoding = encoding

    def set_connect_timeout(self, timeout):
        '''
        Defines a timeout for establishing a connection with a dubbo server.
        It should be noted that this timeout cannot usually exceed 75 seconds.

        defualt is ``10``
        '''
        self.__connect_timeout = timeout

    def set_read_timeout(self, timeout):
        '''
        Defines a timeout for reading a response expected from the dubbo server.

        defualt is ``10``
        '''
        self.__read_timeout = timeout

    def do(self, command):
        # 连接Telnet服务器
        try:
            tn = telnetlib.Telnet(host=self.host, port=self.port, timeout=self.__connect_timeout)
        except socket.error as err:
            print("[host:%s port:%s] %s" % (self.host, self.port, err))
            return

        # 触发doubble提示符
        tn.write(b'\n')  # 基于python3修改

        # 执行命令
        tn.read_until(self.__finish, timeout=self.__read_timeout)
        # command=command.encode()
        # print(self.host, self.port, command)
        tn.write(b'%s\n' % command.encode())  # 基于python3修改
        # tn.write(b'%s\n' % bytes(command))      #基于python3修改

        # 获取结果
        data = b''
        while data.find(self.__finish) == -1:
            data = tn.read_very_eager()
        data = data.split(b"dubbo>")  # 基于python3修改
        if b'elapsed:' in data[0]:
            data = data[0].split(b"\n")
        try:
            data = json.loads(data[0], encoding=self.__encoding)
        except:
            data = str(data[0], encoding=self.__encoding)

        tn.close()  # tn.write('exit\n')

        return data

    def invoke(self, interface, method, param):
        param = str(param.encode('unicode-escape')).replace("\\\\n", "")[2:][:-1].replace("\\\\u", "\\u")
        cmd = f'invoke {interface}.{method}({param})'
        # cmd = "%s %s.%s(%s)" % ('invoke', interface, method, param)
        return self.do(cmd)

    def ls(self, interface):
        cmd = f'ls {interface}'
        data = self.do(cmd)
        return data.strip().split('\r\n')

    def connect(host, port):
        return DubboCore(host, port)


if __name__ == '__main__':
    Host = '172.16.0.143'  # Doubble服务器IP
    Port = 20045  # Doubble服务端口

    # 初始化dubbo对象
    conn = DubboCore(Host, Port)

    interface = 'com.hexin.member.center.api.RegisterApi'
    method = 'isMobileExist'
    param = '{"class":"com.hexin.member.center.request.register.IsMobileExistReq", "mobilePhone":"18000000009"}'
    print(f'{interface}.{method}:{param}--->', conn.invoke(interface, method, param))

    Host = '172.16.0.141'  # Doubble服务器IP
    Port = 20880  # Doubble服务端口

    # 初始化dubbo对象
    conn = DubboCore(Host, Port)

    interface = 'com.hexin.business.service.api.service.BusinessCashierDubboService'
    method = 'cashierQueryOrder'
    param = '{"class":"com.hexin.business.service.api.dubbo.req.BusinessDubboRequest","header":{"class":"com.hexin.business.service.api.dubbo.req.BusinessDubboRequestHeader","merchantCode":"jkd","merchantName":"立即贷","requestId":"20180626130256229000000000070341","requestTime":"2018-06-26 13:02:56","serviceCode":"1611","versionId":"v1"},"body":{"class":"com.hexin.business.service.api.req.CashierOrderReqVO","merchantCode":"jkd","merchantUserId":"214338958027393206","productId":10002,"merchantOrderNo":"20180626130141213000000000085251","businessOrderNo":"20180626130141503231287960007512"}}'
    print(f'{interface}.{method}:{param}--->')
    print(conn.invoke(interface, method, param))



    Host = '172.16.0.141'  # Doubble服务器IP
    Port = 20045  # Doubble服务端口

    # 初始化dubbo对象
    conn = DubboCore(Host, Port)

    interface = 'com.hexin.member.center.api.HomeInfoApi'
    print(conn.ls(interface))