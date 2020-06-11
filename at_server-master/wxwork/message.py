from .models import *
import requests
from django.conf import settings
import json
from userapp.models import *
from baseapp.models import *


class MessageObject:
    @staticmethod
    def send(user_list, title=None, msg=None, forward=None, send_mode=['users']):
        receiver_list = []
        if 'users' in send_mode:
            # 发送给当前用户列表用户
            receiver_list += user_list
        if 'leaders' in send_mode:
            # 发送给用户及其部门领导
            for user in user_list:
                try:
                    department_list = Users.objects.get(realname=user).department_list
                    leaders = Departments.objects.get(department_list=department_list).leaders
                    receiver_list += json.loads(leaders)
                except:
                    print(f"无此人或部门{user}")
        if 'CTO' in send_mode:
            # 发送给CTO
            receiver_list += ['马东京', '陈建华']
        receiver_list = list(set(receiver_list))
        print("消息发送列表", receiver_list)
        MessageObject.send_users(receiver=receiver_list, title=title, msg=msg, forward=forward)

    @staticmethod
    def send_users(receiver, title=None, msg=None, forward=None):
        for receiver_username in receiver:
            if receiver_username:
                MessageObject.send_singer(receiver_username, title=title, msg=msg, forward=forward)

    @staticmethod
    def send_singer(receiver, title=None, msg=None, forward=None):

        data = {
            "token": settings.WXWORK["token"],
            "title": settings.WXWORK["title"],
            "custom_ip": settings.WXWORK["custom_ip"],
            "custom_user": settings.WXWORK["custom_user"],
            "charset": settings.WXWORK["charset"],
            # "forward": f"{settings.WXWORK['tc_server']}/flow/testtask/list",
        }
        if receiver: data['receiver'] = receiver
        if title: data['title'] = title
        if msg: data['msg'] = msg
        if forward: data['forward'] = f"{settings.WXWORK['tc_server']}{forward}"
        if not data['receiver'] or not data['title'] or not data['msg']:
            return False

        db_message = Message.objects.create(receiver=data['receiver'], title=data['title'], msg=data['msg'],
                                            forward=data.get('forward'))

        if not settings.WXWORK["send"]:
            return False
        try:
            response = requests.post(settings.WXWORK["oa_server"], data=data, timeout=5)
            db_message.result = response.json().get("message")
            db_message.save()
            return True
        except:
            db_message.result = "except"
            db_message.save()
            return False


if __name__ == '__main__':
    test = MessageObject()
    test.send(receiver="陈高敏", msg="test内容")
