# -*- coding: utf-8 -*-
'''
开阖ERP采用AGPL-3协议，版权(CopyRight)归以下代码提交者所有

2013    开阖软件 Jeff Wang,OpenERPJeff      (jeff@osbzr.com)            初始版本
2013    joshuajan                           (popkar77@gmail.com)

'''

from openerp.osv import fields, osv
from openerp.addons.bzr_base import check_cycle

class bzr_hr_department(osv.osv):
    """
        员工 bzr.hr.department
    """
    _name='bzr.hr.department'
    _description=u'部门'
    _columns = {
        'name': fields.char(u'名称', size=64, required=True),
        'company_id': fields.many2one('res.company', u'直属公司', required=False),
        'parent_id': fields.many2one('bzr.hr.department', u'上级部门'),
        'child_ids': fields.one2many('bzr.hr.department', 'parent_id', u'下属部门'),
        'manager_id': fields.many2one('bzr.hr.employee', u'部门主管'),
        'member_ids': fields.many2many('bzr.hr.employee', 'rel_employee_2_department', 'department_id', 'employee_id', u'员工'),
    }
    _constraints = [
        (check_cycle,u'不能创建循环的层级关系',['parent_id']),
                   ]

class bzr_hr_employee(osv.osv):
    """
        员工 bzr.hr.employee
    """
    _name='bzr.hr.employee'
    _description=u'员工'
    _columns={
        'name':fields.char(u'姓名',size=50,required=True),
        'code': fields.char(u'编号', size=16),
        'active' : fields.boolean('有效'),
        'company_id' : fields.many2one('res.company', u'直属公司'),
        'user_id' : fields.many2one('res.users', u'公司帐户'),
        'birthday': fields.date(u'生日'),
        'sinid': fields.char(u'社保卡号', size=50),
        'identity_id': fields.char(u'身份证号', size=32),
        'gender': fields.selection([(u'男', u'男'),(u'女', u'女'),(u'未知', u'未知')], u'性别'),
        'department_id':fields.many2one('bzr.hr.department', u'直属部门'),
        'work_phone': fields.char(u'办公电话', size=32, readonly=False),
        'mobile_phone': fields.char(u'手机', size=32, readonly=False),
        'work_email': fields.char(u'公司邮箱', size=240),
        'notes': fields.text('备注'),
        'manager_id': fields.related('department_id', 'manager_id', type='many2one', relation='bzr.hr.employee', string='直接上司', readonly=1),
        'type_ids': fields.many2many('bzr.hr.employee.type', 'rel_employee_2_employee_type', 'employee_id', 'type_id', u'员工类型'),
        'child_ids': fields.one2many('bzr.hr.employee', 'manager_id', '直接下属'),
        'photo': fields.binary(u'证件照片'),
        'login': fields.related('user_id', 'login', type='char', string='用户名', readonly=1),
    }

    _defaults = {
        'active': '1',
        'gender': u'未知',
    }


