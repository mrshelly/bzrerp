# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.addons.bzr_base import get_states

#年度     fi.year
#TODO 我们真的需要会计年度么？

#凭证类型 fi.doc.type
    
class fi_doc_type(osv.osv):
    _name='fi.doc.type'
    _description='凭证字'
    _columns={
        'name':fields.char('凭证字',size=10,required=True),
    }
