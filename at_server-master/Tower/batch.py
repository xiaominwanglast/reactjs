from apscheduler.schedulers.background import BackgroundScheduler
from flowapp.views_batch import *
from userapp.views import *
from baseapp.views_jenkins import *

sched = BackgroundScheduler()

# 上线完成后，针对昨天之前没有验收的单子进行提醒. 周一-周五，每天14点提醒
# 0周一 1周二 4周五 5周六 6周日
sched.add_job(CheckAndAcceptBatch().get, args=(None,),
              trigger='cron', day_of_week='0-4', hour=14, minute=0, second=0,
              id='CheckAndAcceptBatch', replace_existing=True)

# 每天晚上凌晨4点，对用户信息进行更新（对离职人员标记，更新部门信息等）
sched.add_job(UserSync().post, args=(None,),
              trigger='cron', day_of_week='0-6', hour=4, minute=0, second=0,
              id='UserSync', replace_existing=True)


# 每天晚上凌晨5点，对jenken上的job同步一下
sched.add_job(JenkinsServiceSyncObject().get, args=(None,),
              trigger='cron', day_of_week='0-6', hour=5, minute=0, second=0,
              id='JenkinsServiceSyncObject', replace_existing=True)

sched.start()