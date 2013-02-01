# -*- coding: utf-8 -*-
#状态
from openerp.osv import fields, osv

class bzr_state(osv.osv):
    _name='bzr.state'
    _description='状态'
    _columns={
        'object':fields.char('对象',size=64),
        'seq':fields.integer('序号'),
        'key':fields.char('值',size=64),
        'name':fields.char('文本',size=64),
    }
    def get_states(self,cr,uid,object):
        """
        取得该对象state字段的可选值，并按seq字段排序
        """
                
