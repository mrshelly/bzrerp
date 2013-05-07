# -*- coding: utf-8 -*-
'''
开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有

2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
2013    buke                                (wangbuke@gmail.com)        add lru cache for get_amount in menu open
2013    mrshelly                            (mrshelly@hotmail.com)


'''
from openerp.osv import fields, osv
from operator import itemgetter
from openerp.tools import ormcache

# LRU CACHE
class bzrcache(ormcache):
    def lookup(self, self2, cr, *args):
        d = self.lru(self2)
        key = args[self.skiparg-2:]
        key = str(key) # to load context
        try:
           r = d[key]
           self.stat_hit += 1
           return r
        except KeyError:
           self.stat_miss += 1
           value = d[key] = self.method(self2, cr, *args)
           return value
        except TypeError:
           self.stat_err += 1
           return self.method(self2, cr, *args)


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

