import requests
import json

#
# class Zentao_cli(object):
#     session = None  # 用于实现单例类，避免多次申请sessionID
#     sid = None
#
#     def __init__(self, url, account, password, override=False):
#         self.url = url
#         self.account = account  # 账号
#         self.password = password  # 密码
#         self.session_override = override  # 是否覆盖原会话
#         self.pages = {
#             "sid": "/index.php?m=api&f=getSessionID&t=json",  # 获取sid的接口
#             "login": "/index.php?t=json&m=user&f=login&account={0}&password={1}&sid={2}",  # 登录的接口
#             "get_story_list_by_projectID": "/index.php?t=json&m=story&f=ajaxGetProjectStories&projectID={0}",
#             "get_story_list_by_account": "/index.php?"
#         }
#         self.s = None
#         self.sid = None
#
#     def req(self, url):
#         # 请求并返回结果
#         web = self.s.get(url)
#         if web.status_code == 200:
#             print(web.content)
#             resp = json.loads(web.content)
#             if resp.get("status") == "success":
#                 return True, resp
#             else:
#                 return False, resp
#
#     def login(self):
#         if self.s is None:
#             if not self.session_override and Zentao_cli.session is not None:
#                 self.s = Zentao_cli.session
#                 self.sid = Zentao_cli.sid
#             else:
#                 # 新建会话
#                 self.s = requests.session()
#                 res, resp = self.req(self.url.rstrip("/") + self.pages["sid"])
#                 if res:
#                     print("获取sessionID成功")
#                     self.sid = json.loads(resp["data"])["sessionID"]
#                     Zentao_cli.sid = self.sid
#                     login_res, login_resp = self.req(
#                         self.url.rstrip("/") + self.pages["login"].format(self.account, self.password, self.sid))
#                     if login_res:
#                         print("登录成功")
#                         Zentao_cli.session = self.s
#
#     def get_story_list_by_projectID(self, projectID):
#         # 根据projectID获取需求列表
#         req_url = self.url.rstrip("/") + self.pages["get_story_list_by_projectID"].format(str(projectID))
#         web = self.s.get(req_url)
#         if web.status_code == 200:
#             resp = json.loads(web.content.decode())
#             for k, v in resp.items():
#                 print(k, v)


if __name__ == "__main__":
    # cli = Zentao_cli("http://172.16.0.146:58080", "chengm", "5ibgeveR")
    # cli.login()
    # cli.get_story_list_by_projectID(17)


    import requests
    import json
    import hashlib


    def md5(src):
        m2 = hashlib.md5()
        m2.update(src.encode(encoding='UTF-8'))
        return m2.hexdigest()


    if __name__ == "__main__":
        pass
        # key = 'epc1eoe0c4cmf8oo23zud4f6ubtfd0hc'
        # # query='m=api&f=getSessionID&code=myApp'
        # query = 'code=myApp&m=api&f=getModel&module=user&methodName=loginAPI&params=a=1'
        # token = md5(md5(query) + key)
        # print(token)
        # url=f"http://127.0.0.1:3080/api.php?{query}&token={token}"
        # print(url)
        # r=requests.get(url)
        # print(r.text)
        # print(r.headers)


        # query = 'm=api&f=getModel&module=user&methodName=loginAPI&params=account=admin&params'
        # url=f"http://127.0.0.1:3080/?{query}"
        # print(url)
        # r=requests.get(url)
        # print(r.text)
        # print(r.headers)

        # url = f"http://127.0.0.1:3080/user-loginbytms.json"
        # print(url)
        # r = requests.post(url, data={'account': 'test1', 'sign': 'tms!@!#!asADAD@#'})
        # print(r.text)
        # print(r.headers)

        # url = f"http://172.16.0.146:58080/zentao/user-loginbytms.json"
        # print(url)
        # r = requests.post(url, data={'account': 'chengm', 'sign': 'tms!@!#!asADAD@#'})
        # print(r.text)
        # print(r.cookies.get('zentaosid'))


# http://127.0.0.1:3080/user-login.json?account=test1&password=admin123456
# http://127.0.0.1:3080/user-loginTMS.json?account=test1&password=admin123456
