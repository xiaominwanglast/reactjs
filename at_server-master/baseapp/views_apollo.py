from rest_framework import generics, mixins
from rest_framework.response import Response
import pymysql


class ApolloInfoObject(generics.GenericAPIView):
    """
    阿波罗基础数据
    """

    def get(self, request):
        """
        获取阿波罗app名称
        """
        conn = pymysql.connect(host="172.17.0.32", user="test_dkw", password="test_dkw", database="apolloconfigdb",
                               charset="utf8")
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "SELECT AppId,Name FROM app;"
        cursor.execute(sql)
        result = cursor.fetchall()
        data = []
        for items in result:
            data.append(f"{items['AppId']} / {items['Name']}")
        cursor.close()
        conn.close()
        return Response({"status": True, "message": "成功", "data": result})
