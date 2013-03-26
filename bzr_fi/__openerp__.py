# -*- encoding: utf-8 -*-
{
    'name': '财务会计 ',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
        此模块作为bzrerp中财务模块的集成包，逐渐把可用的模块加入这个包
  现在总账是可运行的，正在开发辅助核算    
""",
    'author': 'bzrerp team',
    'sequence': 3,
    'depends': [
        'bzr_fi_gl',
#        'bzr_fi_cost',
#        'bzr_fi_arap',
#        'bzr_fi_cash',
#        'bzr_fi_stock',
    ],
    'data': [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}