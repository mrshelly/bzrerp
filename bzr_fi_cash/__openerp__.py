# -*- coding: utf-8 -*-
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
