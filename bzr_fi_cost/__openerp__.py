# -*- coding: utf-8 -*-
{
    'name': '财务会计 - 辅助核算',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
    增加辅助核算项目和辅助核算凭证行
""",
    'author': 'bzrerp team',
    'sequence': 2,
    'depends': [
        'bzr_base','decimal_precision',
    ],
    'data': ['bzr_fi_cost_document.xml',
             'bzr_fi_cost_master.xml',
             'bzr_fi_cost_config.xml',
             'data/bzr_fi_cost_data.xml',
             'report/bzr_fi_cost_report.xml',
             'wizard/bzr_fi_cost_wizard.xml',
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
