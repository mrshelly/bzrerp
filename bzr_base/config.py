# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from operator import itemgetter

#状态
class bzr_state(osv.osv):
    _name='bzr.state'
    _description=u'状态'
    _columns={
        'object':fields.char(u'对象',size=64),
        'seq':fields.integer(u'序号'),
        'key':fields.char(u'值',size=64),
        'name':fields.char(u'文本',size=64),
    }

def get_states(object):
    """
    取得该对象state字段的可选值，并按seq字段排序
    """
    def states_list(self,cr,uid,context=None):
        if context==None:
            context={}
        #TODO remove this SQL
        psql='select key, name from bzr_state where object=%s order by seq'
        cr.execute(psql, (object,))
        res=cr.fetchall()
        return res
    return states_list

def check_cycle(self, cr, uid, ids, context=None):
    """ 从当前记录开始查找上级记录看是否会形成闭环，造成逻辑错误
    所以上级字段名需固定为 parent_id
    如级数少于100返回True，级数大于100返回False
    """
    level = 100
    while len(ids):
        cr.execute('SELECT DISTINCT parent_id '\
                    'FROM '+self._table+' '\
                    'WHERE id IN %s '\
                    'AND parent_id IS NOT NULL',(tuple(ids),))
        ids = map(itemgetter(0), cr.fetchall())
        if not level:
            return False
        level -= 1
    return True

