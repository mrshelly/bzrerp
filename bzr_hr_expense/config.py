# -*- coding: utf-8 -*-
###################################################################################
#
#  开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有
#
# 2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
# 2013    mrshelly                            (mrshelly@hotmail.com)
#
###################################################################################


from openerp.osv import fields, osv

class bzr_hr_expense_type(osv.osv):
    """
        费用类型 bzr.hr.expense.type
    """
    _name='bzr.hr.expense.type'
    _description=u'费用类型'
    _columns={
        'name':fields.char(u'类型',size=60,required=True),
    }
