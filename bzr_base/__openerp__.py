# -*- coding: utf-8 -*-
{
    'name': '开阖ERP基础模块',
    'version': '1.0',
    'category': 'Hidden/Dependency',
    'description': """
    开阖ERP基础模块，对base模块增强和修改
    """,
    'author': 'jeff@osbzr.com',
    'sequence': 1000,
    'depends': ['base'],
    'data': ['security/groups.xml',
             'security/ir.model.access.csv',
             'config.xml',
             'data.xml'],
    'installable': True,
    'auto_install': True,
    'images': [],
}
