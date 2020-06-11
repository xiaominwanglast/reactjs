from userapp.serializers import *
from rest_framework.response import Response
from rest_framework import generics
from flowapp.models import *
from wxwork.message import MessageObject
import json, datetime


class CheckAndAcceptBatch(generics.GenericAPIView):
    """
    产品人员验收提醒
    """

    # 配合文档，显示请求参数
    serializer_class = UsersSerializerParam

    def get(self, request):
        """
        上线完成后，针对昨天之前没有验收的单子进行提醒
        """

        orders = OnlineOrder.objects.filter(delete=1, status='上线完成',
                                            real_online_time__lt=datetime.datetime.now().strftime("%Y-%m-%d"))
        for order in orders:
            MessageObject.send(title='TMS 验收提醒', user_list=json.loads(order.product_users),
                               msg=f"【{order.status}-等待确认】【{order.system}】{order.title}",
                               forward=f"/flow/online/detail/{order.id}",
                               send_mode=['users'])
        return Response({"status": True, "message": "成功", "data": orders.count()})
