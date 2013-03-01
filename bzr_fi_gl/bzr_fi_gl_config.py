# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
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
    def __compute(self, cr, uid, ids, field_name, arg, context=None):
        result={}
        for report in self.browse(cr, uid, ids, context=context):
            result[report.id] = self.get_amount(cr,uid,report.id,None,context)
        return result

    
    _columns={
        'name':fields.char(u'文本',size=128,required=True,translate=True),
        'sequence':fields.integer(u'行号'),
        'parent_id':fields.many2one('fi.report', u'上级'),
        'account_ids':fields.one2many('fi.acc','report_id',u'科目'),
        'children_ids':fields.one2many('fi.report','parent_id',u'下级'), 
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

    
    def get_amount(self,cr,uid,id,period_id=None,context=None):
        '''报表行的金额'''
        result ={
#        'report':id,             #报表行
#        'period':period_id,      #期间
        'year_start':0.00,       #年初余额
        'year_debit':0.00,       #本年借方
        'year_credit':0.00,      #本年贷方
        'period_start':0.00,     #期初余额             
        'period_debit':0.00,     #本期借方
        'period_credit':0.00,    #本期贷方
        'period_end':0.00,       #期末余额
        }
        
        obj_period = self.pool.get('fi.period')
        obj_acc = self.pool.get('fi.acc')
        
        # 如未输入期间，取当前期间
        if period_id==None:
            period_id=obj_period.find(cr,uid,fields.date.context_today(self._name,cr,uid),context)
        
        this_report = self.read(cr,uid,id,['children_ids',
                     'account_ids','reverse'],context=context)
        
        # 如有下级表行，汇总下级表行金额
        for child in this_report['children_ids']:
            l = self.get_amount(cr,uid,child,period_id,context)
            result['year_start']+=l['year_start']
            result['year_debit']+=l['year_debit']
            result['year_credit']+=l['year_credit']
            result['period_start']+=l['period_start']
            result['period_debit']+=l['period_debit']
            result['period_credit']+=l['period_credit']
            result['period_end']+=l['period_end']
            
        # 取得表行科目
        for acc in this_report['account_ids']:
            l = obj_acc.get_amount(cr,uid,acc,period_id,context)
            result['year_start']+=l['year_start']
            result['year_debit']+=l['year_debit']
            result['year_credit']+=l['year_credit']
            result['period_start']+=l['period_start']
            result['period_debit']+=l['period_debit']
            result['period_credit']+=l['period_credit']
            result['period_end']+=l['period_end']

        return result
