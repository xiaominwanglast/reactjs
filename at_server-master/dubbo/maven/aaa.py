from jpype import *
cpopt="-Djava.class.path=%s" % ("E:\\Workspace\\Tower\\dubbo\\maven\\henxin-dubbo-test-1.0-SNAPSHOT.jar")
startJVM(getDefaultJVMPath(),"-ea",cpopt)
java.lang.System.out.println("Hello World!!")
Test = JClass('com.test.Start2')
Test.getSeriveInfo("hi")
shutdownJVM()