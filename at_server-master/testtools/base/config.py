dbInfo = {
        "T1":{
             "user": "test_dkw",
            "password": "test_dkw",
            "host": "172.17.0.32",
            "port": 3306
        },
        "T2":{
            "user": "test_dkw",
            "password": "test_dkw",
            "host": "172.16.0.142",
            "port": 3307
        },
        "T3":{
            "user": "test_dkw",
            "password": "test_dkw",
            "host": "172.17.0.30",
            "port": 3306
        },
        "P1":{
            "user": "test_dkw",
            "password": "test_dkw",
            "host": "172.17.0.34",
            "port": 3306
        },
        "D1":{
            "user": "test_dkw",
            "password": "test_dkw",
            "host": "172.17.0.120",
            "port": 3306
        },
        "D2":{
            "user": "test_dkw",
            "password": "test_dkw",
            "host": "172.17.0.121",
            "port": 3306
        },
}

tt = '注册'
productDict = {
    '立即贷':{
        'pid':'10002',
        'host':'',
    },
    '畅借款': {
        'pid': '109',
        'terminalId': '25',
        'host': 'http://env-wsdaikuan.2345.com/api/qlcenter',
        'interface': {
            '获取验证码': '/smsValidationCtrl/registerOrModifyLoginCode',
            '注册/登录': '/userCtrl/loginByCode',
            '获取人脸Provider': '/userAccountCtrl/getProviderType',
            '人脸': '/userAccountCtrl/uploadFaceVerifyResult',
            'ocr': '/userAccountCtrl/uploadOcrVerifyResult',
            '填写信息-基本信息': '/userAccountCtrl/basicInfo',
            '填写信息-联系人': '/userAccountCtrl/basicContacts',
            '更新运营商状态': '/creditCenterCtrl/updateDataCertification',
            '开户': '/userAccountCtrl/authAccount',
            '绑卡鉴权申请': '/smsValidationCtrl/addBankCard',
            '绑卡鉴权确认': '/userAccountCtrl/bankcard',
            '获取预借款信息': '/loanCtrl/prepare2Borrow',
            '获取借款状态': '/loanCtrl/getLoanStatus',
            '借款鉴权': '/smsValidationCtrl/gainDynamicValidateCode',
            '借款': '/loanCtrl/borrow4Vip',
            '借款结果查询':'/loanCtrl/borrowInfoQuery',
            '获取用户状态': '/userCtrl/userStatus',
            '还款': '/loanCtrl/getLoanStatus',
        },
        'period': 1,
        'bundleId': 'com.hj.greatloan.android',
        'version': '1.1.0',
        'type': '1',
        'purpose':'27',
        'fundId':'29',
    },
    '2345借款':{
        'pid':'108',
        'terminalId':'21',
        'host':'http://env-wsdaikuan.2345.com/api/jkcenter',
        'interface':{
            '获取验证码':'/smsValidationController/registerOrModifyLoginCode',
            '注册/登录':'/userController/loginByCode',
            '获取人脸Provider':'/userAccountController/getProviderType',
            '人脸':'/userAccountController/uploadFaceVerifyResult',
            'ocr':'/userAccountController/uploadOcrVerifyResult',
            '填写信息':'/userAccountController/userInfo',
            '更新运营商状态':'/creditCenterController/updateDataCertification',
            '开户':'/userAccountController/authAccount',
            '绑卡鉴权申请':'/smsValidationController/addBankCard',
            '绑卡鉴权确认':'/userAccountController/bankcard',
            '获取预借款信息':'/loanController/prepare2Borrow',
            '获取借款状态':'/loanController/getLoanStatus',
            '借款鉴权':'/smsValidationController/gainDynamicValidateCode',
            '借款':'/loanController/borrow4Vip',
            '借款结果查询':'/loanController/borrowInfoQuery',
            '获取用户状态':'/userController/userStatus',
            '还款':'/loanController/getLoanStatus',
        },
        'period':6,
        'bundleId':'com.hj.cardloan.android',
        'version':'2.0.0',
        'type':'1',
        'purpose': '22',
        'fundId': '27',
    },
    '黄金屋':{
        'pid':'111',
        'terminalId':'33',
        'host':'http://env-changloan.com/api/jyjcenter',
        'interface':{
            '获取验证码':'/smsValidationCtrlApi/registerOrModifyLoginCode',
            '注册/登录':'/userCtrlApi/loginByCode',
            '获取人脸Provider': '/userAccountCtrlApi/getProviderType',
            '人脸': '/userAccountCtrl/uploadFaceVerifyResult',
            'ocr': '/userAccountCtrl/uploadOcrVerifyResult',
            '填写信息-基本信息': '/userAccountCtrlApi/basicInfo',
            '填写信息-联系人': '/userAccountCtrlApi/basicContacts',
            '更新运营商状态': '/creditCenterCtrlApi/updateDataCertification',
            '开户': '/userAccountCtrlApi/authAccount',
            '绑卡鉴权申请': '/smsValidationCtrlApi/addBankCard',
            '绑卡鉴权确认': '/userAccountCtrlApi/bankcard',
            '获取预借款信息': '/loanCtrlApi/prepare2Borrow',
            '获取借款状态': '/loanCtrlApi/getLoanStatus',
            '借款鉴权': '/smsValidationCtrlApi/gainDynamicValidateCode',
            '借款': '/loanCtrlApi/borrow4Vip',
            '借款结果查询':'/loanCtrlApi/borrowInfoQuery',
            '获取用户状态': '/userCtrlApi/userStatus',
            '还款': '/loanCtrlApi/getLoanStatus',
        },
        'period':1,
        'bundleId':'com.hj.oneloan.android',
        'version':'1.0.0',
        'type':'5',
        'purpose': '33',
        'fundId': '34',
    },
    '好借款':{
        'pid':'110',
        'terminalId':'29',
        'host':'http://env-wsdaikuan.2345.com/api/hjkcenter',
        'interface':{
            '获取验证码':'/smsValidationCtrl/registerOrModifyLoginCode',
            '注册/登录':'/userCtrl/loginByCode',
            '获取人脸Provider': '/userAccountCtrl/getProviderType',
            '人脸': '/userAccountCtrl/uploadFaceVerifyResult',
            'ocr': '/userAccountCtrl/uploadOcrVerifyResult',
            '填写信息-基本信息': '/userAccountCtrl/basicInfo',
            '填写信息-联系人': '/userAccountCtrl/basicContacts',
            '更新运营商状态': '/creditCenterCtrl/updateDataCertification',
            '开户': '/userAccountCtrl/authAccount',
            '绑卡鉴权申请': '/smsValidationCtrl/addBankCard',
            '绑卡鉴权确认': '/userAccountCtrl/bankcard',
            '获取预借款信息': '/loanCtrl/prepare2Borrow',
            '获取借款状态': '/loanCtrl/getLoanStatus',
            '借款鉴权': '/smsValidationCtrl/gainDynamicValidateCode',
            '借款': '/loanCtrl/borrow4Vip',
            '借款结果查询':'/loanCtrl/borrowInfoQuery',
            '获取用户状态': '/userCtrl/userStatus',
            '还款': '/loanCtrl/getLoanStatus',
        },
        'period':1,
        'bundleId':'com.hj.greatloan.android',
        'version':'1.1.0',
        'type':'1',
        'purpose':'27',
        'fundId':'29',
    }
}

flow = {
    '注册/登录': 'registerAndLogin',
    '人脸OCR': 'saveFaceAndOcr',
    '填写资料': 'fullUserInfo',
    '信用卡': 'bankCardCredit',
    '运营商': 'authOperator',
    '开户': 'openAccount',
    '储蓄卡': 'bankCardDeposit',
    '借款': 'prepareBorrow',
}

step = [
    '注册',
    '登录',
    '人脸OCR',
    '填写资料',
    '绑定信用卡',
    '开户',
    '绑定储蓄卡',
    '借款',
    '还款',
]


flowStep = {
    '注册-人脸OCR':[1,2,3]
}

ss = [x for x in range(1,5)]
print(ss)