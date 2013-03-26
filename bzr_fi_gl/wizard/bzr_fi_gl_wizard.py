# -*- encoding: utf-8 -*-

from  osv import osv, fields
from tools.translate import _
from datetime import date


class detail_ledger(osv.osv_memory):
    '''
    根据输入的科目和期间、辅助核算项目输出《明细账》
    现金日记账，现金外币账，数量金额明细账，三栏帐，外币往来帐
    '''
    def _get_co(self,cr,uid,context=None):
        return [('res.partner','往来')]
    
    _name = 'detail.ledger'
    _descript = u'明细账'
    _columns = {
        'acc_id':fields.many2one('fi.acc', u'会计科目', required=True),
        'period_from':fields.many2one('fi.period', u'开始期间', required=True),
        'period_to':fields.many2one('fi.period', u'截至期间', required=True),
        'co_obj':fields.reference(u'辅助核算项目',selection=_get_co,size=128),
    }

    
    def default_get(self, cr, uid, fields, context=None):
        return {'acc_id': context.get('active_id', None),
                'period_to': self.pool.get('fi.period').find(cr, uid, context=context),
                'period_from': self.pool.get('fi.period').find(cr, uid, context=context),
        }

    def print_report(self, cr, uid, ids, context=None):
        datas = {}
        res = self.read(cr, uid, ids[0], ['acc_id','period_from','period_to','co_obj'], context=context)
        acc = self.pool.get('fi.acc').browse(cr, uid, res['acc_id'][0], context=context)
        datas['ids']=[res['acc_id'][0],]
        datas['period_to'] = res['period_to'][0]
        datas['period_from'] = res['period_from'][0]
        return {
                'type':'ir.actions.report.xml',
                'report_name':acc.format,
                'datas':datas
        }

class general_ledger(osv.osv_memory):
    '''
    根据输入的科目和期间输出 《总帐》
    每个科目一页，第一行输出年初余额，第二行起输出本期合计，本年累计，期末余额
    '''
    _name = 'general.ledger'
    _description = u'总帐'
    _columns = {
        'acc_id':fields.many2one('fi.acc',u'会计科目', required=True),
        'period_to':fields.many2one('fi.period', u'截至期间', required=True),
    }

    def print_report(self, cr, uid, ids, context=None):
        datas = {}
        res = self.read(cr, uid, ids[0], ['acc_id','period_to'], context=context)
        obj_period = self.pool.get('fi.period')
        period_to = obj_period.browse(cr,uid,res['period_to'][0],context=context)
        period_from_id =obj_period.find(cr,uid,dt=period_to.year_id.s_date,context=context)
        datas['ids']=[res['acc_id'][0],]
        datas['period_to'] = res['period_to'][0]
        datas['period_from'] = period_from_id
        return {
            'type':'ir.actions.report.xml',
            'report_name':'fi.general.ledger',
            'datas':datas,
        }
    def default_get(self, cr, uid, fields, context=None):
        return {'acc_id': context.get('active_id', None),
                'period_to':self.pool.get('fi.period').find(cr, uid, context=context),
                }   

class period_report(osv.osv_memory):
    '''
    根据期间输出 《资产负债表》《利润表》，现金流量表在bzr_fi_cash模块实现
    每个期间一页，资产负债表输出年初余额和期末余额，利润表输出本期合计和本年累积
    '''
    _name = 'period.report'
    _description = u'期末报表'
    _columns = {
        'period_to':fields.many2one('fi.period', u'截至期间', required=True),
        'report':fields.selection([('balance.sheet',u'资产负债表'),('profit.loss',u'利润表')],u'报表格式',required=True),
    }

    def print_report(self, cr, uid, ids, context=None):
        datas = {}
        res = self.read(cr, uid, ids[0], ['report','period_to'], context=context)
        datas['period_to'] = res['period_to'][0]
        return {
            'type':'ir.actions.report.xml',
            'report_name':res['report'],
            'datas':datas,
        }
    def default_get(self, cr, uid, fields, context=None):
        return {
                'period_to':self.pool.get('fi.period').find(cr, uid, context=context),
                'report':'balance.sheet',
                } 