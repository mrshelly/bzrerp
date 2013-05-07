# -*- coding: utf-8 -*-
'''
开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有

2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
2013    buke                                (wangbuke@gmail.com)        add lru cache for get_amount in menu open
2013    joshuajan                           (popkar77@gmail.com)
2013    mrshelly                            (mrshelly@hotmail.com)

'''

{
    'name': '财务会计 - 总账',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
    总账模块包含凭证、账簿、报表、月结等基本功能
""",
    'author': 'jeff@osbzr.com',
    'sequence': 2,
    'depends': [
        'bzr_base','decimal_precision','web',
    ],
    'data': ['security/groups.xml',
             'security/ir.model.access.csv',
             'document.xml',
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
    'js': ['static/js/*.js'],
    'css': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
