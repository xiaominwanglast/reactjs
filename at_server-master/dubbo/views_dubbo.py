from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .dubbo_core import DubboCore
from .zookeeper_core import ZKCore
from .dubbo_java_core import DubboJava


class DubboService(generics.GenericAPIView):
    """
    调用dubbo服务
    """

    serializer_class = DubboServiceSerializer

    def post(self, request):
        """
        调用一个dubbo服务
        """
        service = request.data['service']
        function = request.data['function']
        param = request.data['param'][1:][:-1]
        env = request.data['env']
        datatype = request.data.get('datatype')

        # 从zk得到ip端口
        ZK = ZKCore(env)
        host, port = ZK.get_providers(service)
        if not host or not port:
            return Response({"status": False, "message": "服务未在zookeeper发现,可能未启动", "data": "服务未在zookeeper发现,可能未启动"})

        # 连接dubbo的telnet，进行请求
        conn = DubboCore(host, port)
        response = conn.invoke(service, function, param)

        try:
            data = json.loads(response)
        except:
            data = response

        print(data)
        if datatype == 'table':
            try:
                data = DubboJava.format_resopnse_json_to_table_data(data)
                print(json.dumps(data, ensure_ascii=False))
            except:
                return Response({"status": False, "message": "参数错误"})

        return Response({"status": True, "message": "成功", "data": data})
