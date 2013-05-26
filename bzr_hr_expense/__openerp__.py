# -*- coding: utf-8 -*-
###################################################################################
#
# 开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有
#
# 2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
# 2013    mrshelly                            (mrshelly@hotmail.com)
#
###################################################################################


{
    'name': '人力资源 - 报销',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

""",
    'author': 'mrshelly@hotmail.com',
    'sequence': 100,
    'depends': [
        'bzr_base',
        'bzr_hr_base',
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
