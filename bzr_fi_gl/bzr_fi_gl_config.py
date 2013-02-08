# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.addons.bzr_base import get_states

#年度     fi.year
#TODO 我们真的需要会计年度么？
#会计期间 fi.period
#凭证类型 fi.doc.type

class fi_period(osv.osv):
    _name='fi.period'
    _description='会计期间'
    _columns={
        'name':fields.char('会计期间',size=10,required=True),
        's_date':fields.date('开始日期',required=True),
        'e_date':fields.date('结束日期',required=True),
    }
    
class fi_doc_type(osv.osv):
    _name='fi.doc.type'
    _description='凭证字'
    _columns={
    'name':fields.char('会计期间',size=10,required=True),
    's_date':fields.date('开始日期',required=True),
    'e_date':fields.date('结束日期',required=True),
    'state':fields.selection(get_states('fi.doc.type'),'状态'),
    }
