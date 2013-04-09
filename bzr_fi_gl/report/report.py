# -*- coding: utf-8 -*-
from openerp.report import report_sxw
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
import time
from tools.translate import _

class fi_acc_balance(osv.osv):
    _name='fi.acc.balance'
    _description='科目余额表'
    _columns={
    'account':fields.many2one('fi.acc',u'科目'),
    'period':fields.many2one('fi.period',u'期间'),
    'year_start':fields.float(u'年初余额', 
                 digits_compute=dp.get_precision('Account')),
    'year_debit':fields.float(u'本年借方', 
                 digits_compute=dp.get_precision('Account')),
    'year_credit':fields.float(u'本年贷方', 
                 digits_compute=dp.get_precision('Account')),
    'period_start':fields.float(u'期初余额', 
                 digits_compute=dp.get_precision('Account')),
    'period_debit':fields.float(u'本期借方', 
                 digits_compute=dp.get_precision('Account')),
    'period_credit':fields.float(u'本期贷方', 
                 digits_compute=dp.get_precision('Account')),
    'period_end':fields.float(u'期末余额', 
                 digits_compute=dp.get_precision('Account')),
    }    

class ledger_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(ledger_parser, self).__init__(cr, uid, name, context)

        self.localcontext.update( { 
            '''
            注册报表模板里可以访问的函数
            '''
            'time': time,
            'periods':self._get_periods,
            'balance':self._get_period_balance,
            'lines': self._get_period_lines,
            'conterparty':self._get_conterparty,
            'direction':self._get_direction,
        })
        self.context = context
    
    def set_context(self, objects, data, ids, report_type = None):
        """
        设置 OE context
        """
        self.data = data
        obj_period = self.pool.get('fi.period')
        data['period_from']=obj_period.browse(self.cr,self.uid,self.data['period_from'],self.context)
        data['period_to']=obj_period.browse(self.cr,self.uid,self.data['period_to'],self.context)
        super(ledger_parser, self).set_context(objects, data, ids, report_type)    

    def _get_periods(self,context=None):
        '''
        获取期间列表
        '''
        obj_period = self.pool.get('fi.period')
        
        period_ids = obj_period.search(self.cr, self.uid, 
                          [('s_date','>=',self.data['period_from'].s_date),
                           ('e_date','<=',self.data['period_to'].e_date)], 
                           order='s_date')
        periods = obj_period.browse(self.cr, self.uid, period_ids)
        return periods

    def _get_conterparty(self, ids, context=None):
        """
        计算"对方科目"，返回字符串
        """
        result = {}

        for doc_line in self.pool.get('fi.doc.line').browse(self.cr, self.uid, ids, context):
            result[doc_line.id] = ' '

            self.cr.execute('SELECT distinct(acc.name) as name_rest from fi_acc AS acc, fi_doc_line line\
                    where acc.id = line.acc_id and line.doc_id = ' + str(doc_line.doc_id.id) +' and line.acc_id <> ' + str(doc_line.acc_id.id) )
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
                result[doc_line.id] = concat
        return result

    def _get_period_lines(self, acc_id, period_id, context=None):
        '''
        取某科目某期间的凭证行，用于输出明细账
        '''
        lines = []
        obj_acc = self.pool.get('fi.acc')
        obj_line = self.pool.get('fi.doc.line')
        line_ids = obj_line.search(self.cr, self.uid, [('acc_id','=',acc_id),('period_id','=',period_id)],order='date,doc_id')
        for line in obj_line.browse(self.cr, self.uid, line_ids):
            lines.append(line)

        return lines

    def _get_period_balance(self, acc_id, period_id):
        '''
        获取科目的余额数据
        '''
        return self.pool.get('fi.acc').get_amount(self.cr, self.uid, acc_id, period_id,context=self.context)

    def _get_direction(self, balance):

        dir_str = ''
        if balance == 0:
            dir_str = u'平'
        elif balance > 0:
            dir_str = u'借'
        else:
            dir_str = u'贷'
        return dir_str
    
class report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(report_parser, self).__init__(cr, uid, name, context)

        self.localcontext.update( { 
            '''
            注册报表模板里可以访问的函数
            '''
            'time': time,
            'lines':self._get_lines,
            'period_name':self._priod_name,
        })
        self.context = context
    
    def set_context(self, objects, data, ids, report_type = None):
        """
        设置 OE context
        """
        self.data = data
        super(report_parser, self).set_context(objects, data, ids, report_type)    
        
    def _priod_name(self):
        obj_period = self.pool.get('fi.period')
        res = obj_period.browse(self.cr,self.uid,self.data['period_to'],self.context).name
        return res
    def _get_lines(self,block='1',context=None):

        lines = []    
        obj_report = self.pool.get('fi.report')

        line_ids = obj_report.search(self.cr, self.uid, [('type','=',block)])
        for line in obj_report.browse(self.cr, self.uid, line_ids):
            lines.append(line)
        return lines
#注册报表类

#总帐
report_sxw.report_sxw('report.fi.general.ledger', 'fi.acc', 
                      'addons/bzr_fi_gl/report/general_ledger.rml', 
                      parser=ledger_parser, header=False)

#明细帐
report_sxw.report_sxw('report.fi.detail.ledger', 'fi.acc', 
                      'addons/bzr_fi_gl/report/detail_ledger.rml', 
                      parser=ledger_parser, header=False)

#资产负债表
report_sxw.report_sxw('report.balance.sheet', 'fi.period', 
                      'addons/bzr_fi_gl/report/balance_sheet.rml', 
                      parser=report_parser, header=False)

#利润表
report_sxw.report_sxw('report.profit.loss', 'fi.period', 
                      'addons/bzr_fi_gl/report/profit_loss.rml', 
                      parser=report_parser, header=False)
