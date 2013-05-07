# -*- coding: utf-8 -*-
'''
开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有

2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
2013    joshuajan                           (popkar77@gmail.com)
2013    mrshelly                            (mrshelly@hotmail.com)

'''

{
    'name': '开阖ERP基础模块',
    'version': '1.0',
    'category': 'Hidden/Dependency',
    'description': """
    开阖ERP基础模块，对base模块增强和修改
    """,
    'author': 'jeff@osbzr.com',
    'sequence': 1000,
    'depends': ['base','oecn_base_fonts'],
    'data': ['security/groups.xml',
             'security/ir.model.access.csv',
             'config.xml',
             'data.xml'],
    'installable': True,
    'auto_install': True,
    'images': [],
}
