# -*- coding: utf-8 -*-
###################################################################################
#
#  开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有
#
# 2013    开阖软件 Jeff Wang,OpenERPJeff        (jeff@osbzr.com)            初始版本
# 2013    mrshelly                              (mrshelly@hotmail.com)
#
#
###################################################################################


from openerp.osv import fields, osv
from openerp.addons.bzr_base import get_states

class bzr_hr_expense(osv.osv):
    """
        费用 bzr.hr.expense
    """
    _name='bzr.hr.expense'
    _description=u'费用单'

    _columns = {
        'name': fields.char(u'费用摘要', size=200, required=True),
        'type_id': fields.many2one('bzr.hr.expense.type', u'费用类型', required=True),
        'company_id': fields.many2one('res.company', u'归属公司', required=False),
        'department_id': fields.many2one('bzr.hr.department', u'归属部门', required=True),
        'date': fields.date(u'费用日期', required=True),
        'line_ids': fields.one2many('bzr.hr.expense.line', 'order_id', u'费用明细'),
        'employee_id': fields.many2one('bzr.hr.employee', u'经办人'),
        'state':fields.selection(get_states('bzr_hr_expense.bzr.hr.expense'),u'状态', required=True, readonly=True),
        #'workflow_ids': #TODO 这里需要一个通用的工作流信息记录 整个工作流 时间 操作人
    }

    _defaults={
        'state':'draft',
    }

class bzr_hr_expense_line(osv.osv):
    """
        费用明细 bzr.hr.expense.line
    """
    _name='bzr.hr.expense.line'
    _description=u'费用明细'

    _columns = {
        'name': fields.char(u'说明', size=200, required=True),
        'order_id': fields.many2one('bzr.hr.expense', u'费用单', required=True, ondelete='cascade'),
        'amount': fields.float(u'金额', digits=(16,2), required=True),
    }
