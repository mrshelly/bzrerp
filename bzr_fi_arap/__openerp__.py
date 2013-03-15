# -*- coding: utf-8 -*-

{
    'name': '财务会计 - 往来',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
    往来模块包含应收、应付、个人往来等辅助核算管理
    可以打印往来明细账和账龄分析表
""",
    'author': 'bzrerp team',
    'sequence': 3,
    'depends': [
        'bzr_base','decimal_precision',
    ],
    'data': ['bzr_fi_arap_document.xml',
             'bzr_fi_arap_master.xml',
             'bzr_fi_arap_config.xml',
             'data/bzr_fi_arap_data.xml',
             'report/bzr_fi_arap_report.xml',
             'wizard/bzr_fi_arap_wizard.xml',
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