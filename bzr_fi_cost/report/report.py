# -*- coding: utf-8 -*-
###################################################################################
#
#  开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有
#
# 2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
# 2013    joshuajan                           (popkar77@gmail.com)
#
#
###################################################################################

from openerp.report import report_sxw
from openerp.addons.bzr_fi_gl import ledger_parser
import time

class cost_ledger(ledger_parser):
    def __init__(self, cr, uid, name, context):
        super(cost_ledger, self).__init__(cr, uid, name, context)

        self.localcontext.update( { 
            '''
            注册报表模板里可以访问的函数
            '''
            'time': time,
            'periods':self._get_periods,
            'balance':self._get_period_cost_balance,
            'lines': self._get_period_cost_lines,
            'conterparty':self._get_cost_conterparty,
            'direction':self._get_direction,
        })
        self.context = context
        
    def _get_cost_conterparty(self, ids, context=None):
        """
        计算"对方科目"，返回字符串
        """
        result = {}

        for doc_line_cost in self.pool.get('fi.doc.line.cost').browse(self.cr, self.uid, ids, context):
            result[doc_line_cost.id] = ' '

            self.cr.execute('SELECT distinct(acc.name) as name_rest from fi_acc AS acc, fi_doc_line line\
                    where acc.id = line.acc_id and line.doc_id = ' + str(doc_line_cost.line_id.doc_id.id) \
                    +' and line.acc_id <> ' + str(doc_line_cost.line_id.acc_id.id) )
            res = self.cr.dictfetchall()

            if res:
                concat = ''
                run_id = 0
                for line_rest in res:
                    concat = concat + line_rest['name_rest'] + u' '
                    if run_id > 3:
                        # 最多输出3个对方科目，多于3个的时候在后面输出省略号
                        concat += '...'
                        break
                    run_id+=1
                result[doc_line_cost.id] = concat
        return result
    
    def _get_period_cost_lines(self,cost_id,acc_id,period_id,context=None):
        '''取得某一期间的成本行'''
        obj_cost = self.pool.get('fi.doc.line.cost')
        cost_ids = obj_cost.search(self.cr,self.uid,[('co_obj','=',cost_id),('acc_id','=',acc_id),('period_id','=',period_id)],context)
        res = obj_cost.browse(self.cr,self.uid,cost_ids,context)
        return res
    
    def _get_period_cost_balance(self,cost_id,acc_id,period_id,context=None):
        '''取得某一期间的余额'''
        per_start = per_credit = per_debit = per_end = 0.0
        obj_period = self.pool.get('fi.period')
        last_per = obj_period.last(self.cr,self.uid,period_id,context)
        last_balance = {}
        if last_per:
            last_balance = self._get_period_cost_balance(cost_id,acc_id,last_per,context)
        if last_balance:
            per_start = last_balance['period_end']
            
        per_lines = self._get_period_cost_lines(cost_id, acc_id, period_id, context)
        
        if per_lines:
            for l in per_lines:
                per_debit += l.debit
                per_credit += l.credit

        per_end =  per_start + per_debit - per_credit
        
        res = {
               'period_start':per_start,
               'period_debit':per_debit,
               'period_credit':per_credit,
               'period_end':per_end,
               }
        return res
    
report_sxw.report_sxw('report.fi.cost.ledger', 'fi.acc', 
                      'addons/bzr_fi_cost/report/cost_ledger.rml', 
                      parser=cost_ledger, header=False)            