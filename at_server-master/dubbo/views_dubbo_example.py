from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .views_document import DocumentDetail


class ExampleDetail(generics.GenericAPIView):
    """
    把table数据转换成请求示例的json
    """

    serializer_class = DubboExampleSerializer

    def post(self, request):
        """
        把table数据转换成请求示例的json
        """
        example_data = DocumentDetail.get_request_params(json.loads(request.data['table_data']))
        if not example_data:
            return Response({"status": False, "message": "失败,数据格式不正确", "data": []})
        else:
            return Response({"status": True, "message": "成功", "data": example_data})
