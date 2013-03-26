# -*- coding: utf-8 -*-
{
    'name': '人力资源 - 基本数据',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

""",
    'author': 'bzrerp team',
    'sequence': 100,
    'depends': [
        'bzr_base',
    ],
    'data': [
        'bzr_hr_config.xml',
        'bzr_hr_document.xml',
        'bzr_hr_master.xml',
        'data/bzr_hr_data.xml',
        'report/bzr_hr_report.xml',
        'wizard/bzr_hr_wizard.xml',
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
