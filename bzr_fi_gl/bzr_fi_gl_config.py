# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

#凭证类型 fi.doc.type
    
class fi_doc_type(osv.osv):
    _name='fi.doc.type'
    _description=u'凭证字'
    _columns={
        'name':fields.char(u'凭证字',size=10,required=True),
    }
class fi_acc_type(osv.osv):
    _name='fi.acc.type'
    _description=u'科目类型'
    _columns={
        'name':fields.char(u'类型',size=64,required=True),
    }

class fi_report(osv.osv):
    _name='fi.report'
    _description=u'报表行'
    _order='sequence'
    _columns={
        'name':fields.char(u'文本',size=128,required=True,translate=True),
        'sequence':fields.integer(u'行号'),
        'parent_id':fields.many2one('fi.report', u'上级'),
        'children_ids':fields.one2many('fi.report','parent_id',u'下级'),        
        'reverse':fields.boolean(u'金额取反'),
    }
    

