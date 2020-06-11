import queue
import threading, jpype, os, json, time
import time
import random
from multiprocessing import Process, Queue, Lock

L = [1, 2, 3]


def add(q, lock, a, b):
    lock.acquire()  # 加锁避免写入时出现不可预知的错误

    jarpath = os.path.join(os.path.abspath('.'), 'D:/')
    jvmPath = jpype.getDefaultJVMPath()

    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s;%s;%s;%s;%s" % (
            jarpath + 'henxin-dubbo-test-1.0-SNAPSHOT.jar',
            'E:/Workspace/Tower/dubbo/maven/dependency/galaxy-domain-1.3.13-SNAPSHOT.jar',
            'E:/Workspace/Tower/dubbo/maven/dependency/galaxy-facade-1.3.13-SNAPSHOT.jar',
            'E:/Workspace/Tower/dubbo/maven/dependency/business-service-api-0.0.4-SNAPSHOT.jar',
            'E:/Workspace/Tower/dubbo/maven/dependency/base-common-1.0.1.jar'))

    jd = jpype.JPackage("com.test").Start2()
    java_return = json.loads(str(jd.getSeriveInfo("com.loanking.galaxy.facade.MxCarrierFacade")))
    jpype.shutdownJVM()

    lock.release()
    q.put([342])


if __name__ == '__main__':
    q = Queue()
    lock = Lock()
    p1 = Process(target=add, args=(q, lock, 20, 30))
    p2 = Process(target=add, args=(q, lock, 30, 40))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    L += q.get() + q.get()
    print(L)



    # jarpath = os.path.join(os.path.abspath('.'), 'D:/')
    # jvmPath = jpype.getDefaultJVMPath()
    #
    # if not jpype.isJVMStarted():
    #     jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s;%s;%s;%s;%s" % (
    #         jarpath + 'henxin-dubbo-test-1.0-SNAPSHOT.jar',
    #         'E:/Workspace/Tower/dubbo/maven/dependency/galaxy-domain-1.3.13-SNAPSHOT.jar',
    #         'E:/Workspace/Tower/dubbo/maven/dependency/galaxy-facade-1.3.13-SNAPSHOT.jar',
    #         'E:/Workspace/Tower/dubbo/maven/dependency/business-service-api-0.0.4-SNAPSHOT.jar',
    #         'E:/Workspace/Tower/dubbo/maven/dependency/base-common-1.0.1.jar'))
    #
    # jd = jpype.JPackage("com.test").Start2()
    # java_return = json.loads(str(jd.getSeriveInfo("com.loanking.galaxy.facade.MxCarrierFacade")))
    # q.put([42, None, json.dumps(java_return)])
    #
    # jpype.shutdownJVM()
