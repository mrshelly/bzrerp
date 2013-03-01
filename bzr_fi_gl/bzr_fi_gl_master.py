# -*- coding: utf-8 -*-

# 货币 fi.curr
# 会计科目 fi.acc
from openerp.osv import fields, osv
from openerp.addons.bzr_base import get_states
from openerp.tools.translate import _
from datetime import datetime
from dateutil.relativedelta import relativedelta
import openerp.addons.decimal_precision as dp

class fi_acc(osv.osv):
    _name='fi.acc'
    _description=u'会计科目'
    
    def __compute(self, cr, uid, ids, field_name, arg, context=None):
        result={}
        period=self.pool.get('fi.period').find(cr,uid,
                  fields.date.context_today(self._name,cr,uid),context)
        for acc in self.browse(cr, uid, ids, context=context):
            result[acc.id] = self.get_amount(cr,uid,acc.id,period,context)
        return result


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
        'report_id':fields.many2one('fi.report',u'报表行',domain=[('children_ids','=',None)]),
        'reverse':fields.boolean(u'余额取反'),
        'year_start':fields.function(__compute, digits_compute=dp.get_precision('Account'), 
                     string=u'年初余额',multi='balance'),             
        'year_debit':fields.function(__compute, digits_compute=dp.get_precision('Account'), 
                     string=u'本年借方',multi='balance'),             
        'year_credit':fields.function(__compute, digits_compute=dp.get_precision('Account'), 
                     string=u'本年贷方',multi='balance'),             
        'period_start':fields.function(__compute, digits_compute=dp.get_precision('Account'), 
                    string=u'期初余额',multi='balance'),             
        'period_debit':fields.function(__compute, digits_compute=dp.get_precision('Account'), 
                    string=u'本期借方',multi='balance'),                     
        'period_credit':fields.function(__compute, digits_compute=dp.get_precision('Account'), 
                    string=u'本期贷方',multi='balance'),             
        'period_end':fields.function(__compute, digits_compute=dp.get_precision('Account'), 
                    string=u'期末余额',multi='balance'), 
    }
    _defaults={
        'active': True,
    }
    def get_amount(self,cr,uid,id,period_id,context=None):
        ''' 返回科目的余额和发生额 '''
        result ={
        'year_start':0.00,       #年初余额
        'year_debit':0.00,       #本年借方
        'year_credit':0.00,      #本年贷方
        'period_start':0.00,     #期初余额             
        'period_debit':0.00,     #本期借方
        'period_credit':0.00,    #本期贷方
        'period_end':0.00,       #期末余额
        }
        obj_balance = self.pool.get('fi.acc.balance')
        obj_period = self.pool.get('fi.period')
        
        this_period = obj_period.browse(cr,uid,period_id,context)
        # 如期间已结账，从余额表取值并返回
        if this_period.state=='closed':
        
            b_id=obj_balance.search(cr,uid,[('account','=',id),('period','=',period_id)])
            balance=obj_balance.read(cr,uid,b_id)[0]
            
            result['year_start']=balance['year_start']
            result['year_debit']=balance['year_debit']
            result['year_credit']=balance['year_credit']
            result['period_start']=balance['period_start']
            result['period_debit']=balance['period_debit']
            result['period_credit']=balance['period_credit']
            result['period_end']=balance['period_end']
            
            return result
        
        # 计算本期借方和本期贷方 
        cr.execute('SELECT SUM(debit),SUM(credit) FROM fi_doc_line'
                   ' WHERE acc_id=%s AND period_id=%s'
                   ' GROUP BY acc_id', (id, period_id))
        data = cr.fetchone()      
        if data:
            result['period_debit']=data[0]
            result['period_credit']=data[1]
        
        last_period=None
        last_period_day = datetime.strptime(this_period.s_date, '%Y-%m-%d') + relativedelta(days=-1)
        try:
            last_period = obj_period.find(cr,uid,last_period_day.strftime('%Y-%m-%d'))
        except:
            pass
        
        # 如为本数据库第一个期间
        if last_period==None:
            result['period_start']=result['year_start']=0.00
            result['year_debit']=result['period_debit']
            result['year_credit']=result['period_credit']
        else:
            #取上期数据
            last_amount = self.get_amount(cr,uid,id,last_period,context)
                
            # 如本期为本年第一期间
            if this_period.s_date==this_period.year_id.s_date:
                # 年初余额 = 上期期末余额
                result['year_start']=last_amount['period_end']
            else:
                # 年初余额 = 上期年初余额
                result['year_start']=last_amount['year_start']
                
            # 期初余额 = 上期期末余额
            result['period_start']=last_amount['period_end']
            # 本年借方 = 上期本年借方 + 本期本期借方
            result['year_debit']=last_amount['year_debit']+result['period_debit']
            # 本年贷方 = 上期本年贷方 + 本期本期贷方 
            result['year_credit']=last_amount['year_credit']+result['period_credit']               
        
        if self.read(cr,uid,id,['reverse'],context=context)['reverse']:
            # 期末余额 = 期初余额 - 本期借方 + 本期贷方
            result['period_end']=result['period_start'] \
                - result['period_debit'] + result['period_credit']
                
            # 验证：期末余额 = 年初余额 - 本年借方 + 本年贷方，如验证失败报错
            if result['period_end'] !=  result['year_start'] \
                    - result['year_debit'] + result['year_credit']:
                raise osv.except_osv(_(u'错误'), \
                                _(u'余额计算出错'))
        else:
            # 期末余额 = 期初余额 + 本期借方 - 本期贷方
            result['period_end']=result['period_start'] \
                + result['period_debit'] - result['period_credit']
            # 验证：期末余额 = 年初余额 + 本年借方 - 本年贷方，如验证失败报错
            if result['period_end'] !=  result['year_start'] \
                    + result['year_debit'] - result['year_credit']:
                raise osv.except_osv(_(u'错误'), \
                                _(u'余额计算出错'))

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
        return result[0]
    
    def close(self, cr, uid, ids, context=None):
        obj_balance=self.pool.get('fi.acc.balance')
        obj_acc=self.pool.get('fi.acc')
        #写入余额表
        for id in ids:
            for acc in obj_acc.search(cr,uid,[]):
                data = obj_acc.get_amount(cr,uid,acc,id,context)
                data.setdefault('account',acc)
                data.setdefault('period',id)
                obj_balance.create(cr,uid,data,context)
            self.write(cr,uid,id,{'state':'closed'})
        return True
    