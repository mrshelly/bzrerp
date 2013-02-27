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
    
    def get_amount(self,cr,uid,id,period_id,context=None):
        '''报表行的金额'''
        result ={
        'report':id,            #科目
        'period':period_id,      #期间
        'year_start':0.00,       #年初余额
        'year_debit':0.00,       #本年借方
        'year_credit':0.00,      #本年贷方
        'period_start':0.00,     #期初余额             
        'period_debit':0.00,     #本期借方
        'period_credit':0.00,    #本期贷方
        'period_end':0.00,       #期末余额
        }
        
        # 如有下级表行，汇总下级表行金额
        return result
        # 如无下级表行，取得表行科目
        # 遍历科目并调用get_amount方法，汇总
        # 如表行需取反，结果乘以 -1
        return result
