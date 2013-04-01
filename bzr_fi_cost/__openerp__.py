# -*- coding: utf-8 -*-
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
