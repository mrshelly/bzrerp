# -*- coding: utf-8 -*-
{
    'name': '财务会计 - 现金',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
    管理现金和银行存款等账目
""",
    'author': 'bzrerp team',
    'sequence': 2,
    'depends': [
        'bzr_base','decimal_precision',
    ],
    'data': ['bzr_fi_cash_document.xml',
             'bzr_fi_cash_master.xml',
             'bzr_fi_cash_config.xml',
             'data/bzr_fi_cash_data.xml',
             'report/bzr_fi_cash_report.xml',
             'wizard/bzr_fi_cash_wizard.xml',
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
