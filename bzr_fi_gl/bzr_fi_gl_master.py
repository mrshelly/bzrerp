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
    
#会计期间 fi.period
class fi_period(osv.osv):
    _name='fi.period'
    _description='会计期间'
    _columns={
        'name':fields.char('会计期间',size=10,required=True),
        'year':fields.integer('年'),
        'month':fields.integer('月'),
        's_date':fields.date('开始日期',required=True),
        'e_date':fields.date('结束日期',required=True),
    }

