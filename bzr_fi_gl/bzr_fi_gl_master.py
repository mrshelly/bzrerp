# -*- coding: utf-8 -*-

# 货币 fi.curr
# 会计科目 fi.acc
from openerp.osv import fields, osv
from openerp.addons.bzr_base import get_states
from openerp.tools.translate import _

class fi_acc(osv.osv):
    _name='fi.acc'
    _description=u'会计科目'
    _columns={
        'company_id': fields.many2one('res.company', 'Company', 
                      required=True, select=1),
        'code':fields.char(u'编号',size=64),
        'name':fields.char(u'名称',size=64),
        'type':fields.many2one('fi.acc.type',u'类型',size=64),
        'parent_id': fields.many2one('fi.acc',u'上级科目',ondelete='cascade'),
        'child_ids': fields.one2many('fi.acc','parent_id',u'下级科目'),
        'note': fields.text(u'备注'),  
        'active': fields.boolean(u'启用'),
        'report_id':fields.many2one('fi.report',u'报表行'),      
    }
    _defaults={
        'active': True,
    }

class fi_year(osv.osv):
    _name='fi.year'
    _description=u'会计年度'
    _columns = {
        'name':fields.char(u'会计年度',size=64,required=True),
        'company_id':fields.many2one('res.company',u'公司'),
        's_date':fields.date('开始日期',required=True),
        'e_date':fields.date(u'结束日期',required=True),
        'period_ids':fields.one2many('fi.period','year_id','期间'),
    }
    _order = 's_date'

#会计期间 fi.period
class fi_period(osv.osv):
    _name='fi.period'
    _description=u'会计期间'
    _columns={
        'name':fields.char(u'会计期间',size=10,required=True),
        'company_id': fields.many2one('res.company', u'公司', 
              required=True, select=1),
        'year_id':fields.many2one('fi.year',u'年度'),
        'month':fields.integer(u'月'),
        's_date':fields.date(u'开始日期',required=True),
        'e_date':fields.date(u'结束日期',required=True),
        'state':fields.selection(get_states('fi.period'),u'状态',
                required=True, readonly=True),
    }
    _defaults={
        'state':'draft',
    }
    _order = 's_date'
    def find(self, cr, uid, dt=None, context=None):
        if context is None: context = {}
        if not dt:
            dt = fields.date.context_today(self,cr,uid,context=context)
        args = [('s_date', '<=' ,dt), ('e_date', '>=', dt)]
        if context.get('company_id', False):
            args.append(('company_id', '=', context['company_id']))
        else:
            company_id = self.pool.get('res.users').browse(cr, uid, uid, \
                         context=context).company_id.id
            args.append(('company_id', '=', company_id))
        result = self.search(cr, uid, args, context=context)
        if not result:
            raise osv.except_osv(_(u'错误'), \
                                 _(u'无法根据输入的日期 %s 找到期间')%dt)
        return result
