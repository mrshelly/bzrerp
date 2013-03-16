# -*- coding: utf-8 -*-
{
    'name': '财务会计 - 存货',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
    材料账
""",
    'author': 'bzrerp team',
    'sequence': 2,
    'depends': [
        'bzr_base','decimal_precision',
    ],
    'data': ['bzr_fi_stock_document.xml',
             'bzr_fi_stock_master.xml',
             'bzr_fi_stock_config.xml',
             'data/bzr_fi_stock_data.xml',
             'report/bzr_fi_stock_report.xml',
             'wizard/bzr_fi_stock_wizard.xml',
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
