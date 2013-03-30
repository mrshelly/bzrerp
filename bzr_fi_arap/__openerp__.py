# -*- coding: utf-8 -*-

{
    'name': '财务会计 - 往来',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
    往来模块包含应收、应付、个人往来等辅助核算管理
    可以打印往来明细账和账龄分析表
""",
    'author': 'jeff@osbzr.com',
    'sequence': 3,
    'depends': [
        'bzr_base','decimal_precision',
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