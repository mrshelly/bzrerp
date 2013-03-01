# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

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
