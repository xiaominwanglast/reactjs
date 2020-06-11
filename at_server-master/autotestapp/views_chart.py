from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
import json
from .DealTestReport import DealDictValue

class ChatrsInfoObject(generics.GenericAPIView):

        def get(self, request, id):
            """
            测试数据概览
            :param request: project_id项目id
            :param id: 0是总的
            :return: all所有数据
            """
            if id == 0:
                failcase_detail_all = Overview.objects.filter(key='failcase').exclude(project_id="0")
                key_value = list(failcase_detail_all.values())
                # 遍历出 "value" {}不为空的所有failcase数据
                fail_case_list = [json.loads(i.get("value")) for i in key_value if i.get("value") != "{}"]
                fail_case_all = {}
                for iteam in fail_case_list:
                    DealDictValue().merge_dict(iteam, fail_case_all)
                failcase_detail_0, created = Overview.objects.get_or_create(project_id=id, key='failcase')
                #修改已存在project_id = 0 的所有数据
                failcase_detail_0.value = json.dumps(fail_case_all, ensure_ascii=False)
                failcase_detail_0.save()
                #处理数据

                try:
                    failcase_detail = Overview.objects.get(project_id=id, key='failcase')
                    key_value = json.loads(failcase_detail.value)
                    key_value2 = sorted(key_value.items(), key=lambda x: x[1], reverse=True)
                    failcase_data = []
                    for i in key_value2[:10]:
                        failcase_data.append({"name": i[0], "value": i[1]})
                except:
                    failcase_data = []
                addnum_data = {}
                addnum_detail = Overview.objects.filter(project_id=id, key='addnum')
                for addnum in addnum_detail:
                    addnum_data[addnum.date] = int(addnum.value)
            else:
                try:
                    failcase_detail = Overview.objects.get(project_id=id, key='failcase')
                    key_value = json.loads(failcase_detail.value)
                    key_value2 = sorted(key_value.items(), key=lambda x: x[1], reverse=True)
                    failcase_data = []
                    for i in key_value2[:10]:
                        failcase_data.append({"name": i[0], "value": i[1]})
                except:
                    failcase_data = []
                addnum_data = {}
                addnum_detail = Overview.objects.filter(project_id=id, key='addnum')
                for addnum in addnum_detail:
                    addnum_data[addnum.date] = int(addnum.value)

            return Response({"status": True, "message": "成功", "data": {"failcase": failcase_data, "addnum": addnum_data}})