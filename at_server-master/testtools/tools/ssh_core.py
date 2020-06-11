# -*- coding: utf-8 -*-

import ssh

class SSH_Core():
    
    def __init__(self):
        
        pass
    
    def connect(self,host):
        self.client = ssh.SSHClient()
        self.client.set_missing_host_key_policy(ssh.AutoAddPolicy())
        self.client.connect(host, port=22, username="root", password="123456")

    def restart_server(self,name,env):
        
        name=name.split('_')[1]
        
        if env=='TEST1':
            parent_host="172.16.23.207"
            if name in ['batch','config','zuul','eureka','bs']:
                host="192.168.23.71"
            elif name in ['cs-br','ts','af']:
                host="192.168.23.72"
            elif name in ['cs-ao','ma','as','br']:
                host="192.168.23.73"
            elif name in ['cs-iam','dc','uc','iam']:
                host="192.168.23.74"
            elif name in ['ao','ic','nc']:
                host="192.168.23.75"
            else:
                host="error"
        elif env=='TEST2':
            parent_host="172.16.23.209"
            if name in ['batch','config','zuul','eureka','bs']:
                host="192.168.23.91"
            elif name in ['cs-br','ts','af']:
                host="192.168.23.92"
            elif name in ['cs-ao','ma','as','br']:
                host="192.168.23.93"
            elif name in ['cs-iam','dc','uc','iam']:
                host="192.168.23.94"
            elif name in ['ao','ic','nc']:
                host="192.168.23.95"
            else:
                host="error"
        elif env=='TEST3':
            parent_host="172.16.23.211"
            if name in ['batch','config','zuul','eureka','bs']:
                host="192.168.23.111"
            elif name in ['cs-br','ts','af']:
                host="192.168.23.112"
            elif name in ['cs-ao','ma','as','br']:
                host="192.168.23.113"
            elif name in ['cs-iam','dc','uc','iam']:
                host="192.168.23.114"
            elif name in ['ao','ic','nc']:
                host="192.168.23.115"
            else:
                host="error"
        else:
            parent_host="error"
        
        print name,env
        print parent_host
        print host

        self.connect(parent_host)
        stdin, stdout, stderr = self.client.exec_command("ssh %s \"su - tomcat -s /bin/bash -c \\\"/etc/init.d/chonggou_tongyong restart %s.jar\\\" \" " % (host,name))

        return stdout.read().replace('\n',"<br>")

# {
#     "micro_ao": {
#         "test1": {
#             "parent_host": "172.16.23.207",
#             "host": "192.168.23.75",
#             "source_dir": "/opt/app/share/ao",
#             "target_dir": "/opt/app/app_server_src/ao/server",
#             "command": {
#                 "restart": "su - tomcat -s /bin/bash -c \\\"/etc/init.d/chonggou_tongyong restart ao.jar\\\"",
#                 "stop": "su - tomcat -s /bin/bash -c \\\"/etc/init.d/chonggou_tongyong stop ao.jar\\\"",
#                 "check_md5": "cd $src_dir;md5sum -c $filename.md5"
#             }
#         },
#         "test2": {
#             "parent_host": "172.16.23.207",
#             "host": "192.168.23.75",
#             "source_dir": "/opt/app/share/ao",
#             "target_dir": "/opt/app/app_server_src/ao/server",
#             "command": {
#                 "restart": "su - tomcat -s /bin/bash -c \\\"/etc/init.d/chonggou_tongyong restart ao.jar\\\"",
#                 "stop": "su - tomcat -s /bin/bash -c \\\"/etc/init.d/chonggou_tongyong stop ao.jar\\\"",
#                 "check_md5": "cd $src_dir;md5sum -c $filename.md5"
#             }
#         }
#     }
# }

