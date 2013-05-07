# -*- coding: utf-8 -*-
'''
开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有

2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
2013    joshuajan                           (popkar77@gmail.com)
2013    mrshelly                            (mrshelly@hotmail.com)

'''

{
    'name': '财务会计 - 辅助核算',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
    增加辅助核算项目和辅助核算凭证行
""",
    'author': 'jeff@osbzr.com',
    'sequence': 2,
    'depends': [
        'bzr_base','decimal_precision','bzr_fi_gl',
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
