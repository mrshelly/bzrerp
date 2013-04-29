# -*- coding: utf-8 -*-
'''
开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有

2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
2013    joshuajan                           (popkar77@gmail.com)
2013    mrshelly                            (mrshelly@hotmail.com)

'''

{
    'name': '人力资源 - 基本数据',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

""",
    'author': 'mrshelly@gmail.com',
    'sequence': 100,
    'depends': [
        'bzr_base',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'config.xml',
        'document.xml',
        'master.xml',
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
