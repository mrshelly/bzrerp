# -*- coding: utf-8 -*-
{
    'name': '人力资源 - 基本数据',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

""",
    'author': 'mrshelly@gmail.com',
    'sequence': 100,
    'depends': [
        'bzr_base',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'config.xml',
        'document.xml',
        'master.xml',
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
