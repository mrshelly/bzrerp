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
        'code':fields.char(u'编号',size=64,required=True),
        'name':fields.char(u'类型',size=64,required=True),
    }
    

