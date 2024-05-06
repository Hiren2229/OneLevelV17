# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from datetime import timedelta, datetime
from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    x_aa_ol_discount_date = fields.Date('Discount Date')
    x_aa_ol_day_till_discount_date = fields.Integer('Days Till Discount Date', compute='_compute_x_aa_ol_day_till_discount_date')

    '''If select/change partner then update discount date'''
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        if (self.partner_id and self.partner_id.x_aa_ol_payment_day
            and self.partner_id.x_aa_ol_discount_percentage and self.move_type == 'in_invoice'):
            self.x_aa_ol_discount_date = self.date + timedelta(days=self.partner_id.x_aa_ol_payment_day)
        else:
            self.x_aa_ol_discount_date = False
        if res:
            return res

    @api.onchange('invoice_payment_term_id')
    def onchange_payment_term(self):
        if len(self.invoice_payment_term_id.line_ids) > 1 and self.invoice_date:
            num_days = self.invoice_payment_term_id.line_ids[0].days
            bill_date = self.invoice_date
            self.x_aa_ol_discount_date = bill_date + timedelta(days=num_days)
        else:
            self.x_aa_ol_discount_date = False

    '''Calculate the discount days'''
    def _compute_x_aa_ol_day_till_discount_date(self):
        for rec in self:
            rec.x_aa_ol_day_till_discount_date = 0
            if rec.x_aa_ol_discount_date:
                rec.x_aa_ol_day_till_discount_date = (rec.x_aa_ol_discount_date - datetime.today().date()).days

