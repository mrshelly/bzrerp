# -*- coding: utf-8 -*-
###################################################################################
#
# 开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有
#
# 2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
# 2013    joshuajan                           (popkar77@gmail.com)
# 2013    mrshelly                            (mrshelly@hotmail.com)
###################################################################################


{
    'name': '财务会计 - 现金',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
    管理现金和银行存款等账目
""",
    'author': 'jeff@osbzr.com',
    'sequence': 2,
    'depends': [
        'bzr_fi_gl',
        'decimal_precision',
    ],
    'data': ['document.xml',
             'master.xml',
             'config.xml',
             'data.xml',
             'report/report.xml',
             'wizard/wizard.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'css': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
