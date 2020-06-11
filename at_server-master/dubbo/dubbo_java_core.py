# -*- coding: utf-8 -*-

import json
import jpype
import os
from multiprocessing import Process, Queue, Lock
from django.conf import settings
import time
import shutil


class DubboJava:

    @staticmethod
    def update_dependency_jar_by_maven():
        cmd = []
        current_timestamp = str(int(time.time() * 1000))
        maven_dir = os.path.join(settings.BASE_DIR, 'dubbo', 'maven')
        dependency_dir_tmp = os.path.join(settings.BASE_DIR, 'dubbo', 'maven', f'dependency{current_timestamp}')
        dependency_dir = os.path.join(settings.BASE_DIR, 'dubbo', 'maven', 'dependency')

        cmd.append(f'cd {maven_dir}')
        cmd.append(
            f'mvn dependency:copy-dependencies -DoverWriteIfNewer=true -DoverWriteReleases=true -DoverWriteSnapshots=true -DoutputDirectory={dependency_dir_tmp}')

        if os.system(' && '.join(cmd)) == 0:
            try:
                shutil.rmtree(dependency_dir)
            except:
                pass
            try:
                shutil.move(dependency_dir_tmp, dependency_dir)
            except:
                pass
            return True
        else:
            return False

    @staticmethod
    def get_jarpath():
        jar_list = []
        dependency_dir = os.path.join(settings.BASE_DIR, 'dubbo', 'maven', 'dependency')
        for parent, dirnames, filenames in os.walk(dependency_dir):
            for filename in filenames:
                jar_list.append(os.path.join(parent, filename))
        jar_list.append(os.path.join(settings.BASE_DIR, 'dubbo', 'maven', 'henxin-dubbo-test-1.0-SNAPSHOT.jar'))
        jarpsth = ';'.join(jar_list)
        return jarpsth

    @staticmethod
    def get_function_params_from_java_multiprocessing(queue, lock, env, service_name, function_name):

        lock.acquire()  # 加锁避免写入时出现不可预知的错误
        jvmPath = jpype.getDefaultJVMPath()
        if not jpype.isJVMStarted():
            jpype.startJVM(jvmPath, "-ea", "-Djava.class.path={0}".format(DubboJava.get_jarpath()))
        jd = jpype.JPackage("com.test").Start2()
        try:
            java_return = json.loads(str(jd.getSeriveInfo(service_name)))
        except:
            java_return = {}

        jpype.shutdownJVM()
        lock.release()
        queue.put(java_return.get(function_name, "error"))

    @staticmethod
    def create_params(**kwargs):
        arg_template = {
            "name": "参数",
            "type": "arg",
            "require": True,
            "example": "",
            "desc": "",
            "note": "",
            "children": []
        }
        arg_template.update(kwargs)
        return arg_template

    @staticmethod
    def change_param_type(value):
        type_dict = {
            "arg": "arg",
            "class": "class",
            "class java.util.Date": "Date",
            "list": "list",
            "class java.lang.Integer": "Integer",
            "class java.lang.String": "String",
            "object": "object",
            "class java.math.BigDecimal": "BigDecimal",
            "class java.lang.Boolean": "Boolean",
            "java.lang.String": "String",
            "java.util.Date": "Date",
            "java.lang.Integer": "Integer",
            "java.math.BigDecimal": "BigDecimal",
            "java.lang.Boolean": "Boolean",
            "class java.lang.Long": "Long",
            "java.lang.Long": "Long",

        }

        return type_dict.get(value, value)

    # todo 转换类型


    @staticmethod
    def format_object(object):
        ret_list = []

        for name, value in object.items():
            if isinstance(value, str):
                if name == 'serialVersionUID':
                    continue
                if value == 'class java.util.Date':
                    ret_list.append(DubboJava.create_params(name=name, type=DubboJava.change_param_type(value),
                                                            example='2018-06-06 06:06:06'))
                elif name == 'class':
                    ret_list.append(DubboJava.create_params(name=name, type='class', example=value))
                else:
                    ret_list.append(DubboJava.create_params(name=name, type=DubboJava.change_param_type(value)))
            else:
                if isinstance(value, list):
                    if isinstance(value[0],dict):
                        ret_list.append(
                            DubboJava.create_params(name=name, type='list', children=DubboJava.format_object(value[0])))
                    elif isinstance(value[0],str):
                        ret_list.append(
                            DubboJava.create_params(name=name, type='list', children=[]))
                else:
                    ret_list.append(
                        DubboJava.create_params(name=name, type='object', children=DubboJava.format_object(value)))
        return ret_list

    @staticmethod
    def sort_class(object):
        if isinstance(object.get('children'), list):
            for i in range(len(object.get('children'))):
                if object.get('children')[i].get('name') == 'class':
                    object.get('children').insert(0, object.get('children')[i])
                    del object.get('children')[i + 1]

                if object.get('children')[i].get('type') in ['object', 'list']:
                    object.get('children').append(object.get('children')[i])
                    del object.get('children')[i]

                if isinstance(object.get('children')[i].get('children'), list):
                    DubboJava.sort_class(object.get('children')[i])
        return object

    @staticmethod
    def format_resopnse_json_to_table_data(object):
        ret_list = []

        for name, value in object.items():

            if isinstance(value, list):
                ret_list.append(
                    DubboJava.create_params(name=name, type='list',
                                            children=DubboJava.format_resopnse_json_to_table_data(value[0])))
            elif isinstance(value, dict):
                ret_list.append(
                    DubboJava.create_params(name=name, type='object',
                                            children=DubboJava.format_resopnse_json_to_table_data(value)))
            elif isinstance(value, bool):
                ret_list.append(DubboJava.create_params(name=name, type="bool", example=str(value)))
            elif isinstance(value, int):
                ret_list.append(DubboJava.create_params(name=name, type="Integer", example=str(value)))
            elif isinstance(value, float):
                ret_list.append(DubboJava.create_params(name=name, type="Float", example=str(value)))
            else:
                ret_list.append(DubboJava.create_params(name=name, type="String", example=str(value)))

        return ret_list

    def get_function_params(self, env, service_name, function_name):

        queue = Queue()
        lock = Lock()
        process = Process(target=DubboJava.get_function_params_from_java_multiprocessing,
                          args=(queue, lock, env, service_name, function_name,))
        process.start()
        process.join()
        args = queue.get()

        if args == 'error':
            return args
        print(json.dumps(args))
        params = []
        i = 0
        for arg in args:
            if isinstance(arg, str):
                param = DubboJava.create_params(name=f'参数{i}', children=[
                    DubboJava.create_params(name="arg", type=DubboJava.change_param_type(arg))])
            elif isinstance(arg, list):
                param = DubboJava.create_params(name=f'参数{i}', children=DubboJava.format_object(arg[0]),type='list')
                param = DubboJava.sort_class(param)
            else:
                param = DubboJava.create_params(name=f'参数{i}', children=DubboJava.format_object(arg))
                param = DubboJava.sort_class(param)
            params.append(param)
            i += 1
        print(json.dumps(params, ensure_ascii=False))
        return params


if __name__ == '__main__':
    DJ = DubboJava()
    arg = {
        "reqId": "string",
        "strategyId": "int",
        "serialNo": "string"
    }
    param = DubboJava.create_params(name=f'参数0', children=DubboJava.format_object(arg))
    print(json.dumps(param, ensure_ascii=False))
    # DJ.get_function_params('T1', "com.daikuan.product.customercenter.api.UserService", 'setPassword')
    # DJ.get_function_params('T1', "com.daikuan.product.customercenter.api.UserService", 'login')
    # DJ.get_function_params('T1', "com.daikuan.product.customercenter.api.UserService", 'forgetPassword')
    # DJ.get_function_params('T1', "com.hexin.member.center.api.BankCardManagerApi", 'changeBankCard')
