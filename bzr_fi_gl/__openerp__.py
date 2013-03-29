# -*- coding: utf-8 -*-

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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
