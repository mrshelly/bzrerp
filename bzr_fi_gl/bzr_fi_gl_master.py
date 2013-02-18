# -*- coding: utf-8 -*-

# 货币 fi.curr
# 会计科目 fi.acc
from openerp.osv import fields, osv
from openerp.addons.bzr_base import get_states


class fi_acc(osv.osv):
    _name='fi.acc'
    _description=u'会计科目'
    _columns={
        'code':fields.char(u'编号',size=64),
        'name':fields.char(u'名称',size=64),
        'type':fields.many2one('fi.acc.type',u'类型',size=64),
    }
    
#会计期间 fi.period
class fi_period(osv.osv):
    _name='fi.period'
    _description=u'会计期间'
    _columns={
        'name':fields.char(u'会计期间',size=10,required=True),
        'year':fields.integer(u'年'),
        'month':fields.integer(u'月'),
        's_date':fields.date(u'开始日期',required=True),
        'e_date':fields.date(u'结束日期',required=True),
        'state':fields.selection(get_states('fi.period'),u'状态',
        required=True, readonly=True),
    }
    _defaults={
        'state':'draft',
    }

