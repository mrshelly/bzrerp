# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.addons.bzr_base import get_states
import openerp.addons.decimal_precision as dp
#会计凭证   fi.doc
#会计凭证行 fi.doc.line
#辅助核算行 fi.doc.line.cost

class fi_doc(osv.osv):
    _name = 'fi.doc'
    _description = u'会计凭证'
    _columns = {
#凭证日期
        'date':fields.date(u'凭证日期'),
#会计期间
        'period_id':fields.many2one('fi.period',u'期间',required=True,
        states={'posted':[('readonly',True)]},help=u'过账后不可修改'),        
#凭证字
        'type_id':fields.many2one('fi.doc.type','凭证字',required=True,
        help=u'可在配置中自定义'),
#凭证号
        'number':fields.char(u'凭证编号',size=64,
        help=u'由系统自动生成，结帐前可重排'),
#附单据数
        'ref_count':fields.integer(u'附单据数',help=u'凭证后附原始凭证的页数'),
#凭证行
        'line_ids':fields.one2many('fi.doc.line','doc_id',u'凭证行',
        states={'posted':[('readonly',True)]},help=u'过账后不可修改'),
#状态
        'state':fields.selection(get_states('fi.doc'),u'状态',required=True, 
        readonly=True,
        help=u'控制会计凭证工作流'),
#制单
        'create_uid':fields.many2one('res.users',u'制单',
        help=u'凭证制单人'),
#审核
        'approve_uid':fields.many2one('res.users',u'审核',
        help=u'凭证审核人'),
#登账
        'post_uid':fields.many2one('res.users',u'记账',
        help=u'凭证登帐人'),
    }
    _defaults={
        'state':'draft',
    }

class fi_doc_line(osv.osv):
    _name = 'fi.doc.line'
    _description = u'会计凭证行'
    _columns = {
#会计凭证
        'doc_id':fields.many2one('fi.doc',u'会计凭证',required=True),
#摘要
        'text':fields.char(u'摘要',size=64,help=u'凭证行的摘要',required=True),
#会计科目
        'acc_id':fields.many2one('fi.acc',u'会计科目',help=u'只能选择末级科目',required=True),
#借方
#TODO 这里这个'Account'能否使用当前class的name？
        'debit': fields.float(u'借方',help=u'以公司本位币计的金额', 
        digits_compute=dp.get_precision('Account')),
#贷方
        'credit': fields.float(u'贷方',help=u'以公司本位币计的金额',
        digits_compute=dp.get_precision('Account')),        

#辅助核算行
        'cost_ids':fields.one2many('fi.doc.line.cost','line_id',u'辅助核算行'),   
    }


class fi_doc_line_cost(osv.osv):
    def _get_co(self,cr,uid,context=None):
        return 'res.partner'
    _name = 'fi.doc.line.cost'
    _description = u'辅助核算行'
    _columns = {
#凭证行编号
        'line_id':fields.many2one('fi.doc.line',u'凭证行'),
#类别
        'type':fields.char(u'辅助核算类别',size=64),
#辅助核算项目
        'co_obj':fields.reference(u'辅助核算项目',selection=_get_co,size=128),
#金额
        'amount':fields.float(u'金额',
        digits_compute=dp.get_precision('Account')),
#产品相关
#数量
        'quantity':fields.float(u'数量',
        digits_compute=dp.get_precision('Account')),
#单价
        'price':fields.float(u'单价',
        digits_compute=dp.get_precision('Account')),
#业务伙伴相关
#到期日
        'due':fields.date(u'到期日',help=u'往来欠款到期日，用于计算账龄'),
    }
