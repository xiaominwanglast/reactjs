from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.response import Response

from Tower.settings import envs
from .models import *
from .serializers import *
from wxwork.message import MessageObject
import json, datetime
from userapp.models import *
from baseapp.models import *
from django.db.models import Q
import os, re, time
import threading
from django.conf import settings
import platform
from databaseapp.db_tool import MySQLOperating


class DBInfoObject(generics.GenericAPIView):
    """
    数据库基础配置信息
    """

    def get(self, request):
        """
        数据库基础配置信息
        """
        dbs = DBInfo.objects.filter(status=1)
        serializer = DBInfoSerializer(dbs, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})


class DBChangeObject(generics.GenericAPIView):
    """
    数据库变更内容的新增
    """

    # 配合文档，显示请求参数
    serializer_class = DBChangeSerializer

    def post(self, request):
        """
        数据库变更内容的新增
        """
        # 1. 检查传入的参数，并保存

        serializer = DBChangeSerializer(data=request.data)
        print("request:" + str(request.data))
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 2. 保留一份历史版本
        serializer_history = DBChangeHistorySerializer(
            data={'dbchange_id': serializer.data.get('id'), 'content': serializer.data.get('content')})
        serializer_history.is_valid() and serializer_history.save()
        return Response({"status": True, "message": "成功", "data": serializer.data})


class DBChangeDetailObject(generics.GenericAPIView):
    """
    数据库变更内容的获取与修改
    """
    serializer_class = DBChangeSerializerModifyParam

    def get(self, request, id):
        """
        查询一个数据库变更内容
        """
        mydbchange = DBChange.objects.get(id=id, delete=1)
        serializer = DBChangeSerializer(mydbchange)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def put(self, request, id):
        """
        数据库变更内容的修改
        """
        # 1. 检查传入的参数，并保存
        mydbchange = DBChange.objects.get(id=id, delete=1)

        serializer = DBChangeSerializerModifyParam(mydbchange, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 2. 保留一份历史版本
        serializer_history = DBChangeHistorySerializer(
            data={'dbchange_id': serializer.data.get('id'), 'content': serializer.data.get('content')})
        serializer_history.is_valid() and serializer_history.save()

        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, id):
        """
        删除一个数据库变更内容
        """
        mydbchange = DBChange.objects.get(id=id, delete=1)

        mydbchange.delete = 0
        mydbchange.save()

        return Response({"status": True, "message": "成功", "data": ""})


class DBChangeOrderObject(generics.GenericAPIView):
    """
    数据库变更单的新增
    """

    # 配合文档，显示请求参数
    serializer_class = DBChangeOrderSerializer

    def post(self, request):
        """
        新增一个数据库变更单
        """
        # 1. 检查传入的参数，并保存
        request.data['status'] = '待审核'
        request.data['submit_user'] = request.session['user'].get('realname')
        request.data['dbchange_ids'] = json.dumps([abs(int(x)) for x in json.loads(request.data.get('dbchange_ids'))])
        serializer = DBChangeOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 2. 操作记录

        serializer_record = DBChangeAuditRecordSerializer(
            data={'dbchangeorder_id': serializer.data.get('id'), 'content': '', 'status': '提交变更单',
                  'username': request.session['user'].get('username'),
                  'realname': request.session['user'].get('realname')})
        if not serializer_record.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer_record.errors})
        serializer_record.save()

        # 3.发送企业消息
        user_list = [serializer.data.get("submit_user")]
        MessageObject.send(title='TMS 数据库审核', user_list=user_list,
                           msg=f"【{serializer.data.get('status')}】{serializer.data.get('title')}",
                           forward=f"/database/audit/detail/{serializer.data.get('id')}",
                           send_mode=['users', 'leaders'])
        print(serializer.data)
        user_list = json.loads(serializer.data.get("check_users"))
        MessageObject.send(title='TMS 数据库审核', user_list=user_list,
                           msg=f"【{serializer.data.get('status')}】{serializer.data.get('title')}",
                           forward=f"/database/audit/detail/{serializer.data.get('id')}",
                           send_mode=['users'])

        return Response({"status": True, "message": "成功", "data": serializer.data})


class DBChangeOrderQuery(generics.GenericAPIView, mixins.ListModelMixin):
    """
    条件查询审核单,什么参数都不传，返回所有
    """

    # 配合文档，显示请求参数
    serializer_class = DBChangeOrderSerializer

    # pagination_class = LimitOffsetPaginationCustomer

    def get_queryset(self):
        if 'create_time' in self.request.data:
            self.request.data['create_time__gte'] = self.request.data['create_time'][0] + ' 00:00:00'
            self.request.data['create_time__lte'] = self.request.data['create_time'][1] + ' 23:59:59'
            del self.request.data['create_time']
        if 'online_time' in self.request.data:
            self.request.data['online_time__gte'] = self.request.data['online_time'][0] + ' 00:00:00'
            self.request.data['online_time__lte'] = self.request.data['online_time'][1] + ' 23:59:59'
            del self.request.data['online_time']

        if self.request.data.get('type') == 'Q':
            del self.request.data['type']
            Qfilter = []
            for k, v in self.request.data.items():
                Qfilter.append(f"Q({k}=\'{v}\')")
            Qfilter = "|".join(Qfilter)

            now_order = DBChangeOrder.objects.filter(delete=1).filter(eval(Qfilter)).exclude(
                status__in=('已上线', '已通过')).order_by('-id')[:9999999]
            finish_order = DBChangeOrder.objects.filter(delete=1).filter(eval(Qfilter)).filter(
                status='已通过').order_by('-id')[:9999999]
            end_order = DBChangeOrder.objects.filter(delete=1).filter(eval(Qfilter)).filter(
                status='已上线').order_by('-id')[:9999999]
            all_order = now_order.union(finish_order, end_order)
            print(len(finish_order), len(end_order), len(all_order))

        else:
            now_order = DBChangeOrder.objects.filter(delete=1).filter(**self.request.data).exclude(
                status__in=('已上线', '已通过')).order_by('-id')[:9999999]
            finish_order = DBChangeOrder.objects.filter(delete=1).filter(**self.request.data).filter(
                status='已通过').order_by('-id')[:9999999]
            end_order = DBChangeOrder.objects.filter(delete=1).filter(**self.request.data).filter(
                status='已上线').order_by('-id')[:9999999]
            all_order = now_order.union(finish_order, end_order)

        for record in all_order:
            record.update_type = []
            rec = DBChange.objects.filter(id__in=json.loads(record.dbchange_ids))
            for i in rec:
                if (i.update_type):
                    record.update_type += json.loads(i.update_type)

            record.update_type = json.dumps(list(set(record.update_type)), ensure_ascii=False)

        return all_order

    def post(self, request):
        """
        条件查询提测单,什么参数都不传，返回所有
        """
        return self.list(request)


class DBChangeOrderDetailObject(generics.GenericAPIView):
    """
    数据库变更单的获取与修改
    """
    serializer_class = DBChangeOrderSerializerModifyParam

    def get(self, request, id):
        """
        查询一个变更单的内容
        """
        mydbchangeorder = DBChangeOrder.objects.get(id=id, delete=1)
        serializer = DBChangeOrderSerializer(mydbchangeorder)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    def put(self, request, id):
        """
        修改一个变更单的内容
        """
        dbchange_ids_raw = json.loads(request.data.get('dbchange_ids'))
        dbchange_ids = [int(x) for x in dbchange_ids_raw if int(x) > 0]
        dbchange_ids_add = [abs(int(x)) for x in dbchange_ids_raw if str(x).startswith('+')]
        dbchange_ids_delete = [abs(int(x)) for x in dbchange_ids_raw if str(x).startswith('-')]
        dbchange_ids_modify = [abs(int(x)) for x in dbchange_ids_raw if str(x).startswith('0')]

        new_dbchangehistory_id = []
        old_dbchangehistory_id = []
        for dbchange_id in dbchange_ids_raw:
            if str(dbchange_id).startswith('+'):
                old_dbchangehistory_id.append(0)
                new_dbchangehistory_id.append(
                    DBChangeHistory.objects.filter(dbchange_id=abs(int(dbchange_id)), delete=1).order_by('-id')[0].id)
            elif str(dbchange_id).startswith('-'):
                old_dbchangehistory_id.append(
                    DBChangeHistory.objects.filter(dbchange_id=abs(int(dbchange_id)), delete=1).order_by('-id')[0].id)
                new_dbchangehistory_id.append(0)
            elif str(dbchange_id).startswith('0'):
                old_dbchangehistory_id.append(
                    DBChangeHistory.objects.filter(dbchange_id=abs(int(dbchange_id)), delete=1).order_by('-id')[1].id)
                new_dbchangehistory_id.append(
                    DBChangeHistory.objects.filter(dbchange_id=abs(int(dbchange_id)), delete=1).order_by('-id')[0].id)

        dbchange_delete = []
        dbchange_add = []
        dbchange_modify = []

        for iid in dbchange_ids_delete:
            dbchange_delete.append(DBChange.objects.get(id=iid).database)
        for iid in dbchange_ids_add:
            dbchange_add.append(DBChange.objects.get(id=iid).database)
        for iid in dbchange_ids_modify:
            dbchange_modify.append(DBChange.objects.get(id=iid).database)

        content = []
        if len(dbchange_delete) > 0:
            content.append(f"删除--->{','.join(dbchange_delete)}")
        if len(dbchange_add) > 0:
            content.append(f"新增--->{','.join(dbchange_add)}")
        if len(dbchange_modify) > 0:
            content.append(f"修改--->{','.join(dbchange_modify)}")
        content = '\n'.join(content)

        # 1. 检查传入的参数，并保存
        mydbchangeorder = DBChangeOrder.objects.get(id=id, delete=1)
        request.data['dbchange_ids'] = json.dumps(dbchange_ids)
        request.data['status'] = '待审核'
        serializer = DBChangeOrderSerializerModifyParam(mydbchangeorder, data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer.errors})
        serializer.save()

        # 2. 操作记录
        serializer_record = DBChangeAuditRecordSerializer(
            data={'dbchangeorder_id': serializer.data.get('id'), 'content': content, 'status': '修改变更单并重新提交',
                  'username': request.session['user'].get('username'),
                  'realname': request.session['user'].get('realname'),
                  'new_dbchangehistory_id': json.dumps(new_dbchangehistory_id),
                  'old_dbchangehistory_id': json.dumps(old_dbchangehistory_id)
                  })
        if not serializer_record.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer_record.errors})
        serializer_record.save()

        # 3.发送企业消息
        user_list = [mydbchangeorder.submit_user]
        MessageObject.send(title='TMS 数据库审核', user_list=user_list,
                           msg=f"【修改并重新提交】{mydbchangeorder.title}",
                           forward=f"/database/audit/detail/{mydbchangeorder.id}",
                           send_mode=['users', 'leaders'])

        user_list = json.loads(mydbchangeorder.check_users)
        MessageObject.send(title='TMS 数据库审核', user_list=user_list,
                           msg=f"【修改并重新提交】{mydbchangeorder.title}",
                           forward=f"/database/audit/detail/{mydbchangeorder.id}",
                           send_mode=['users'])

        return Response({"status": True, "message": "成功", "data": serializer.data})

    def delete(self, request, id):
        """
        删除一个数据库变更内容
        """
        mydbchangeorder = DBChangeOrder.objects.get(id=id, delete=1)
        mydbchangeorder.delete = 0
        mydbchangeorder.save()

        return Response({"status": True, "message": "成功", "data": ""})


class DBChangeOrderAuditRecordObject(generics.GenericAPIView):
    """
    数据库变更单 审核记录
    """
    serializer_class = DBChangeAuditRecordSerializer

    @staticmethod
    def notice_bigdata(db_change_order_ids, step):
        big_data_need = [
            "数据库IP更换",
            "数据表字段类型变更",
            "数据表字段删除",
            "数据表字段用途变更(比如存放值的逻辑变动)",
        ]
        user_list = ['卢春洋', '程鹏', '吴绍杰']
        for db_change_order_id in db_change_order_ids:
            dbchangeorder = DBChangeOrder.objects.get(id=db_change_order_id)
            user_list = ['程俊杰', '程鹏', '丁金梁', '申俊伯', '王红卫', '吴绍杰']
            MessageObject.send(title='TMS 数据库变更通知', user_list=user_list,
                               msg=f"【{step}】{dbchangeorder.title}",
                               forward=f"/database/audit/detail/{db_change_order_id}",
                               send_mode=['users'])

    @staticmethod
    def analyse_sql(sql):
        tmpfile = f'temp/test{str(int(time.time() * 1000))}.txt'
        with open(tmpfile, 'w') as f:
            f.write(sql)

        if platform.system() == 'Windows':
            cmd = f"{settings.BASE_DIR}/databaseapp/soar/soar.windows-amd64 -query {tmpfile} -report-type ast"
        elif platform.system() == 'Linux':
            cmd = f"{settings.BASE_DIR}/databaseapp/soar/soar.linux-amd64 -query {tmpfile} -report-type ast"
        else:
            cmd = 'ls'
            print('其他')

        r = os.popen(cmd)
        text = r.read()
        r.close()

        tmpfile = f'temp/testa{str(int(time.time() * 1000))}.txt'
        with open(tmpfile, 'w') as f:
            f.write(text)
        return re.findall("Action:.*?\"(.*?)\".*?[\n]*.*?[\n]*.*?[\n]*.*?[\n]*.*?TableIdent{v:\"(.*?)\"}", text, re.I)

    def update_notice(self, dbchange_ids, id):
        analyse_result = []
        for iid in json.loads(dbchange_ids):
            change = DBChange.objects.get(id=iid)
            if change.type == 'MySQL':
                analyse_tmp = DBChangeOrderAuditRecordObject.analyse_sql(change.content)
                for tmp in analyse_tmp:
                    index = re.findall("_(\d+)$", tmp[1], re.I)
                    try:
                        index = str(int(index[0]))
                        table = '_'.join(tmp[1].split('_')[:-1]) + '_{x}'
                    except:
                        table = tmp[1]
                    if tmp[0] != 'insert':
                        tmp_result = {
                            "type": change.type,
                            "database": change.database,
                            "table": table,
                            "operation": tmp[0]
                        }
                    if tmp_result not in analyse_result:
                        analyse_result.append(tmp_result)
            else:
                tmp_result = {
                    "type": change.type,
                    "database": change.database,
                    "table": "请自行查看",
                    "operation": "请自行查看"
                }
                analyse_result.append(tmp_result)

        notice, created = DBChangeNotice.objects.get_or_create(dbchangeorder_id=id)
        notice.notice_date = datetime.datetime.now()
        notice.content = json.dumps(analyse_result)
        notice.save()

    def get(self, request, id):
        """
        查询一个变更单的所有审核记录
        """
        orderauditrecord = DBChangeAuditRecord.objects.filter(dbchangeorder_id=id, delete=1).order_by('id')
        serializer = DBChangeAuditRecordSerializer(orderauditrecord, many=True)
        return Response({"status": True, "message": "成功", "data": serializer.data})

    # def post(self, request, id):
    #     """
    #     对一个未生成审核记录的单子，手动执行
    #     """
    #     order = DBChangeOrder.objects.get(id=id)
    #     self.update_notice(order.dbchange_ids, id)
    #     return Response({"status": True, "message": "成功", "data": {}})

    def put(self, request, id):
        """
        修改一个变更单的所有审核记录
        """
        serializer_record = DBChangeAuditRecordSerializer(
            data={'dbchangeorder_id': id, 'content': request.data.get('content'), 'status': request.data.get('status'),
                  'username': request.session['user'].get('username'),
                  'realname': request.session['user'].get('realname'),
                  'new_dbchangehistory_id': '[]',
                  'old_dbchangehistory_id': '[]'
                  })
        if not serializer_record.is_valid():
            return Response({"status": False, "message": "数据格式不正确", "data": serializer_record.errors})
        serializer_record.save()

        if request.data.get('status') == '审核通过':
            status = '已通过'
        elif request.data.get('status') == '审核不通过':
            status = '不通过'
        elif request.data.get('status') == '已上线':
            status = '已上线'
        else:
            status = '未知'

        order = DBChangeOrder.objects.get(id=id)
        order.status = status
        order.save()

        if status == '已通过':
            # 异步处理分析sql
            threading.Thread(target=self.update_notice, args=(order.dbchange_ids, id,)).start()

        if status == '已上线':
            order.online_time = datetime.datetime.now()
            order.save()

        # 3.发送企业消息
        if order.status == '已通过':
            user_list = [order.submit_user]
            MessageObject.send(title='TMS 数据库审核', user_list=user_list,
                               msg=f"【{order.status}】{order.title}",
                               forward=f"/database/audit/detail/{order.id}",
                               send_mode=['users', 'leaders'])
            user_list = json.loads(order.cc_users)
            MessageObject.send(title='TMS 数据库审核', user_list=user_list,
                               msg=f"【{order.status}】{order.title}",
                               forward=f"/database/audit/detail/{order.id}",
                               send_mode=['users'])

        if order.status == '不通过':
            user_list = [order.submit_user]
            MessageObject.send(title='TMS 数据库审核', user_list=user_list,
                               msg=f"【{order.status}】{order.title}",
                               forward=f"/database/audit/detail/{order.id}",
                               send_mode=['users', 'leaders'])

        return Response({"status": True, "message": "成功", "data": serializer_record.data})


class DBChangeHistoryDetailObject(generics.GenericAPIView):
    """
    变更记录历史
    """
    serializer_class = DBChangeAuditRecordSerializer

    def get(self, request, ids):
        """
        查询一个变更单的记录历史
        """
        old_ids, new_ids = json.loads('[' + ids + ']')
        data = []
        for i in range(len(old_ids)):
            if old_ids[i] != 0:
                old = DBChangeHistory.objects.get(id=old_ids[i], delete=1)
                dbinfo = DBChange.objects.get(id=old.dbchange_id)
                old_content = old.content
            else:
                old_content = ""

            if new_ids[i] != 0:
                new = DBChangeHistory.objects.get(id=new_ids[i], delete=1)
                dbinfo = DBChange.objects.get(id=new.dbchange_id)
                new_content = new.content
            else:
                new_content = ""

            data.append({
                "old_content": old_content,
                "new_content": new_content,
                "database": dbinfo.database,
                "type": dbinfo.type,
            })
        return Response({"status": True, "message": "成功", "data": data})


class DBChangeNoticeObject(generics.GenericAPIView):
    """
    数据库变更通知
    """
    serializer_class = DBChangeAuditRecordSerializer

    def get(self, request):
        """
        查询所有数据库变更通知记录
        """
        data = {}
        for notice in DBChangeNotice.objects.all().order_by('-id'):
            if notice.notice_date.strftime('%Y-%m-%d') not in data:
                data[notice.notice_date.strftime('%Y-%m-%d')] = []
            data[notice.notice_date.strftime('%Y-%m-%d')].append({notice.dbchangeorder_id: json.loads(notice.content)})
        return Response({"status": True, "message": "成功", "data": data})


class DBExecuteObject(generics.GenericAPIView):
    serializer_class = DBExecuteRecordDetailSerializer

    def post(self, request):
        order_id = request.data.get('order_id')
        if order_id is None:
            return Response({"status": False, "message": "order_id是必传，请检查"})

        for env in json.loads(request.data.get('env')):
            for sql_id in json.loads(request.data.get('ids')):
                info = DBChange.objects.get(id=sql_id, delete=1)

                if info is not None:
                    # 根据;进行分割sql
                    sql_list = info.content.split(';\r\n')
                    # 数据库连接
                    try:
                        db = MySQLOperating(env, info.database)
                    except Exception:
                        return Response({"status": False, "message": env + "数据库连接失败"})

                    # 准备开始执行sqlsql_list，先在大的记录表中插入默认数据
                    # 获取执行者
                    executor = request.session['user'].get('realname')
                    execute = DBExecuteRecordSerializer(
                        data={'env': env, 'order_id': order_id, 'database': info.database,
                              'dbchangeorder_id': sql_id, 'result': 1, 'executor': executor
                              })
                    if not execute.is_valid():
                        return Response(
                            {"status": False, "message": "数据插入不正确", "data": execute.errors})
                    execute.save()
                    # 获取插入的id值
                    detail_id = execute.data.get('id')
                    # 遍历sql并开始执行
                    for sql_item in sql_list:
                        if sql_item != '' and sql_item is not None:
                            try:
                                db.execute(sql_item)
                                # 获取执行人
                                serializer_record = DBExecuteRecordDetailSerializer(
                                    data={'env': env, 'detail_id': detail_id, 'order_id': order_id,
                                          'database': info.database,
                                          'dbchangeorder_id': sql_id, 'result': 1,
                                          'sql_item': sql_item, 'error_info': '',
                                          'type': 'MYSQL'
                                          })
                                if not serializer_record.is_valid():
                                    return Response(
                                        {"status": False, "message": "数据插入不正确", "data": serializer_record.errors})
                                serializer_record.save()
                            except Exception as e:
                                serializer_record = DBExecuteRecordDetailSerializer(
                                    data={'env': env, 'detail_id': detail_id, 'order_id': order_id,
                                          'database': info.database,
                                          'dbchangeorder_id': sql_id, 'result': 0,
                                          'sql_item': sql_item, 'error_info': e.args[1],
                                          'type': 'MYSQL'
                                          })
                                if not serializer_record.is_valid():
                                    return Response(
                                        {"status": False, "message": "数据格式不正确", "data": serializer_record.errors})
                                serializer_record.save()
                                DBExecuteRecord.objects.filter(id=detail_id).update(result=0)
                                # 更新dbchangeorder的excute_status字段
                                DBExecuteObject.update_execute_status(order_id, env, "执行失败")
                                return Response({"status": False, "message": "sql执行失败"})
                    db.close()
            DBExecuteObject.update_execute_status(order_id, env, "执行成功")
        return Response({"status": True, "message": "成功"})

    @staticmethod
    def update_execute_status(order_id, env, result):
        order_info = DBChangeOrder.objects.get(id=order_id)
        execute_status = eval(order_info.execute_status)
        execute_status[env] = result
        DBChangeOrder.objects.filter(id=order_id).update(execute_status=json.dumps(execute_status, ensure_ascii=False))


class DBExecuteHistoryObject(generics.GenericAPIView):

    def get(self, request, id):
        env_info_list = []
        # 查询数据库提交信息
        info = DBExecuteRecord.objects.filter(order_id=id, env__in=envs).order_by('-id')
        for record in info:
            env_history = {}
            error_info = []
            env_history["date"] = record.create_time.strftime("%Y-%m-%d %H:%M:%S")
            env_history["result"] = record.result
            env_history["env"] = record.env
            env_history["executor"] = record.executor
            if record.result == '0':
                detail = DBExecuteRecordDetail.objects.filter(detail_id=record.id, result=0).order_by('-id')
                for detail_data in detail:
                    error_single = {"error_sql": detail_data.sql_item, "error_msg": detail_data.error_info,
                                    "database": detail_data.database}
                    error_info.append(error_single)
                env_history["error_info"] = error_info
            env_history["error_info"] = error_info
            env_info_list.append(env_history)
        return Response({"status": True, "message": "成功", "data": env_info_list})


# add by cc
class DBChangeUpdateType(generics.GenericAPIView):

    # 配合文档，显示请求参数
    # serializer_class = DBChangeOrderSerializer

    def get(self, request):
        """
        查询IDS的记录
        """

        dbchange_ids = request.query_params.get('dbchange_ids')
        print(dbchange_ids)
        rec = DBChange.objects.filter(id__in=json.loads(dbchange_ids))

        return Response({"status": True, "message": "成功", "data": DBChangeSerializer(rec, many=True).data})
