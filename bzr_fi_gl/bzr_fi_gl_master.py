# -*- coding: utf-8 -*-

# 货币 fi.curr
# 会计科目 fi.acc
from openerp.osv import fields, osv

class fi_acc(osv.osv):
    _name='fi.acc'
    _description='会计科目'
    _columns={
        'name':fields.char('名称',size=64),
    }
