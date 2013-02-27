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
    def get_amount(self,cr,uid,id,period_id,context=None):
        ''' 返回科目的余额和发生额 '''
        result ={
        'account':id,            #科目
        'period':period_id,      #期间
        'year_start':0.00,       #年初余额
        'year_debit':0.00,       #本年借方
        'year_credit':0.00,      #本年贷方
        'period_start':0.00,     #期初余额             
        'period_debit':0.00,     #本期借方
        'period_credit':0.00,    #本期贷方
        'period_end':0.00,       #期末余额
        }
        
        # 如期间已结账，从余额表取值并返回
        
        return result
        
        # 计算本期借方和本期贷方 
        
        #取上期数据 (find方法取s_date之前一天所在期间即为上一期间)
        last_period = 1
        last_amount = self.get_amount(cr,uid,id,last_period,context=None):
        # 如本期为本年第一期间 开始日期相同
            # 年初余额 = 上期期末余额
        # 否则
            # 年初余额 = 上期年初余额
        # 期初余额 = 上期期末余额
        # 本年借方 = 上期本年借方 + 本期本期借方
        # 本年贷方 = 上期本年贷方 + 本期本期贷方        
        # 期末余额 = 期初余额 + 本期借方 - 本期贷方
        
        # 验证：期末余额 = 年初余额 + 本年借方 - 本年贷方，如验证失败报错
        
        return result
        
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
    
    def close(self, cr, uid, ids, context=None):
        #写入余额表 pool.get('fi.acc').get_amount
        return True
    