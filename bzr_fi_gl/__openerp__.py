# -*- coding: utf-8 -*-

{
    'name': '财务会计 - 总账',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
    总账模块包含凭证、账簿、报表、月结等基本功能
""",
    'author': 'bzrerp team',
    'sequence': 2,
    'depends': [
        'bzr_base','decimal_precision',
    ],
    'data': ['bzr_fi_gl_document.xml',
             'bzr_fi_gl_master.xml',
             'bzr_fi_gl_config.xml',
             'data/bzr_fi_gl_data.xml',
             'report/bzr_fi_gl_report.xml',
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
