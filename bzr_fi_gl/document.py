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
    
    def name_get(self,cr,uid,ids,context=None):
        res = []
        for d in self.browse(cr, uid, ids, context):
            t = (d.id, d.period_id.name + d.type_id.name + d.number + '号')
            res.append(t)
        return res
    
    def _amount_compute(self, cr, uid, ids, name, args, context, where =''):
        if not ids: return {}
        cr.execute( 'SELECT doc_id, SUM(debit) '\
                    'FROM fi_doc_line '\
                    'WHERE doc_id IN %s '\
                    'GROUP BY doc_id', (tuple(ids),))
        result = dict(cr.fetchall())
        for id in ids:
            result.setdefault(id, 0.0)
        return result
    def _amount_big(self, cr, uid, ids, name, args, context, where =''):
        ''' 大写金额合计 '''
        pass
        
    def _search_amount(self, cr, uid, obj, name, args, context):
        ids = set()
        for cond in args:
            amount = cond[2]
            if isinstance(cond[2],(list,tuple)):
                if cond[1] in ['in','not in']:
                    amount = tuple(cond[2])
                else:
                    continue
            else:
                if cond[1] in ['=like', 'like', 'not like', \
                    'ilike', 'not ilike', 'in', 'not in', 'child_of']:
                    continue
    
            cr.execute('select doc_id from fi_doc_line group by doc_id ' \
                       'having sum(debit) %s %%s' % (cond[1]),(amount,))
            res_ids = set(id[0] for id in cr.fetchall())
            ids = ids and (ids & res_ids) or res_ids
        if ids:
            return [('id', 'in', tuple(ids))]
        return [('id', '=', '0')]
    
    _columns = {
        'company_id': fields.many2one('res.company', u'公司', 
                      required=True, select=1),
#凭证日期
        'date':fields.date(u'凭证日期',required=True,),
#会计期间
        'period_id':fields.many2one('fi.period',u'期间',required=True,
                    domain=[('state','!=','closed')]),        
#凭证字
        'type_id':fields.many2one('fi.doc.type','凭证字',required=True,
                  help=u'可在配置中自定义'),
#凭证号
        'number':fields.char(u'编号',size=64),
#附单据数
        'ref_count':fields.integer(u'附件数',help=u'凭证后附原始凭证的页数'),
#凭证行
        'line_ids':fields.one2many('fi.doc.line','doc_id',u'凭证行',
        states={'posted':[('readonly',True)]},help=u'过账后不可修改'),
#金额合计
        'amount': fields.function(_amount_compute, string=u'金额', 
                  digits_compute=dp.get_precision('Account'), 
                  type='float', fnct_search=_search_amount),
#大写金额
#        'big':fields.function(_amount_big, string=u'金额', type='char',size='128'),
#状态
        'state':fields.selection(get_states('fi.doc'),u'状态',required=True, 
        readonly=True,
        help=u'控制会计凭证工作流'),
#备注
        'note':fields.text(u'备注'),
#修正意见
        'needfix':fields.char(u'修正意见',size=128,
                  help=u'复核人发现的问题在这里描述，制单人修正后清空此字段'),
#制单
        'create_uid':fields.many2one('res.users',u'制单',
        help=u'凭证制单人'),
#复核
        'approve_uid':fields.many2one('res.users',u'复核',
        help=u'凭证复核人'),
#登账
        'post_uid':fields.many2one('res.users',u'记账',
        help=u'凭证登帐人'),
    }
    _defaults = {
        'type_id':1,
        'number': '/',
        'state': 'draft',
        'ref_count':1,
        'period_id': lambda self, cr, uid, c: \
            self.pool.get('fi.period').find(cr,uid),

        'date': fields.date.context_today,
        'company_id': lambda self, cr, uid, c: \
            self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
    }
# 审批按钮
    def button_approve(self, cursor, user, ids, context=None):
        return self.approve(cursor, user, ids, context=context)
# 登账按钮
    def button_post(self, cursor, user, ids, context=None):
        return self.post(cursor, user, ids, context=context)
# 审批拒绝
    def button_redo(self, cursor, user, ids, context=None):
        return self.redo(cursor, user, ids, context=context)
# 批量登帐            
    def post(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr,uid,ids,{'post_uid':uid,'state':'posted'})
        return True

    def approve(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr,uid,ids,{'approve_uid':uid,'state':'approved'})
        return True
    def redo(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr,uid,ids,{'state':'draft','approve_uid':None,'post_uid':None})
        return True 
    def copy(self, cr, uid, id, default=None, context=None):
        default = {} if default is None else default.copy()
        context = {} if context is None else context.copy()
        default.update({
            'state':'draft',
            'name':'/',
        })
        context.update({
            'copy':True
        })
        return super(fi_doc, self).copy(cr, uid, id, default, context)
            
class fi_doc_line(osv.osv):
    _name = 'fi.doc.line'
    _description = u'会计凭证行'
    _columns = {
#会计凭证
        'doc_id':fields.many2one('fi.doc',u'会计凭证',required=True, ondelete='cascade'),
#摘要
        'text':fields.char(u'摘要',size=64,help=u'凭证行的摘要',required=True),
#会计科目
        'acc_id':fields.many2one('fi.acc',u'会计科目',help=u'只能选择末级科目',required=True,domain=[('child_ids','=',False)]),
#借方
#TODO 这里这个'Account'能否使用当前class的name？
        'debit': fields.float(u'借方',help=u'以公司本位币计的金额', 
        digits_compute=dp.get_precision('Account')),
#贷方
        'credit': fields.float(u'贷方',help=u'以公司本位币计的金额',
        digits_compute=dp.get_precision('Account')),        

#辅助核算行
        'cost_ids':fields.one2many('fi.doc.line.cost','line_id',u'辅助核算行'),

# 从凭证上复制一些字段过来
#TODO 复制凭证时这个字段的值会带入新凭证，即使新凭证的期间值改了也不更新这里，注意
        'period_id':fields.related('doc_id','period_id',type='many2one', 
          relation='fi.period', string='期间', store=True, readonly=True),
    }


class fi_doc_line_cost(osv.osv):
    def _get_co(self,cr,uid,context=None):
        return [('res.partner','往来')]
    _name = 'fi.doc.line.cost'
    _description = u'辅助核算行'
    _columns = {
#凭证行编号
        'line_id':fields.many2one('fi.doc.line',u'凭证行'),
#类别
        'type':fields.char(u'辅助核算类别',size=64),
#辅助核算项目
        'co_obj':fields.reference(u'辅助核算项目',selection=_get_co,size=128),
#借方
#TODO 这里这个'Account'能否使用当前class的name？
        'debit': fields.float(u'借方',help=u'以公司本位币计的金额', 
        digits_compute=dp.get_precision('Account')),
#贷方
        'credit': fields.float(u'贷方',help=u'以公司本位币计的金额',
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
        
        'period_id':fields.related('line_id','period_id',type='many2one', 
          relation='fi.period', string='期间', store=True),
        'acc_id':fields.related('line_id','acc_id',type='many2one',
          relation='fi.acc',string='科目',store=True)
    }
    def create(self, cr, uid, data, context=None):
        '''在创建记录时，凭证行还未保存，无法获取related的字段值（两级related可以，三级就不行了）
                             暂时在创建时写入，但问题是凭证的科目和期间变化不会写入成本行
        '''
        #FIXME: 改成function字段并在修改时更新
        obj_line=self.pool.get('fi.doc.line')
        line = obj_line.browse(cr,uid,data['line_id'],context)
        data['period_id'] = line.doc_id.period_id.id
        data['acc_id'] = line.acc_id.id
        line_cost_id = super(fi_doc_line_cost, self).create(cr, uid, data, context=context)
        return line_cost_id
