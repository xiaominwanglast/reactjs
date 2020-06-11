from . import createuser,sql_deal,endecryption,create_overdue
from django.urls import path, include

urlpatterns = [
    # 文件上传、下载
    path('adduser/', createuser.CreateUser.as_view()),
    path('getstep/', createuser.GetStep.as_view()),
    path('getcurrentstep/', createuser.GetCurrentStepAndStatus.as_view()),
    path('change/', sql_deal.ChangeOperator.as_view()),
    path('operate/', sql_deal.GetOperateCode.as_view()),
    path('getmongocode/', sql_deal.GetJkMongo.as_view()),
    path('getcollections/', sql_deal.GetCollections.as_view()),
    path('accountoperate/', createuser.GetAccountOperateCode.as_view()),
    path('getuserinfo/', createuser.GetUserInfo.as_view()),
    path('getuserinfocode/', createuser.GetUserInfoCode.as_view()),
    path('decrypt/', endecryption.Decryption.as_view()),
    path('endecrypt/', endecryption.Endecryption.as_view()),
    path('bankbin/', createuser.GetBankBinInfo.as_view()),
    path('overdue/', create_overdue.OverDue.as_view()),
    path('clearredis/', sql_deal.ClearRedisInfo.as_view()),
]