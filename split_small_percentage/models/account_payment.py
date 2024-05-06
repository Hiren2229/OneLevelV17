# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from datetime import datetime
from odoo import models, api, fields


class AccountPayment(models.Model):
    _inherit = "account.payment"

    x_aa_ol_discount_amount = fields.Float('Discount Amount')
    x_aa_ol_early_payment = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='yes',
                                             string='Early Payment Discount')
    x_aa_ol_is_discount_applied = fields.Boolean('Is Discount Applied')
    x_aa_ol_payment_difference = fields.Monetary(readonly=True)
    x_aa_ol_payment_difference_handling = fields.Selection(
        [('open', 'Keep open'), ('reconcile', 'Mark invoice as fully paid')], default='open',
        string="Payment Difference Handling", copy=False)
    x_aa_ol_writeoff_account_id = fields.Many2one('account.account', string="Difference Account",
                                                  domain="[('deprecated', '=', False), ('company_id', '=', company_id)]",
                                                  copy=False)
    x_aa_ol_writeoff_label = fields.Char(
        string='Journal Item Label',
        help='Change label of the counterpart that will hold the payment difference',
        default='Write-Off')

    '''select/change currency and early payment discount is yes then 
        discount amount is minus from amount'''
    @api.onchange('currency_id')
    def _onchange_currency(self):
        if self.x_aa_ol_early_payment != 'no':
            self.amount = self.amount - self.x_aa_ol_discount_amount

    '''If select/change early payment then update payment difference handling, difference
       account, journal item label and payment difference'''
    @api.onchange('x_aa_ol_early_payment')
    def _onchange_x_aa_ol_early_payment(self):
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        invoices = self.env['account.move'].browse(active_ids).filtered(
            lambda move: move.is_invoice(include_receipts=True))
        for invoice in invoices:
            if self.x_aa_ol_early_payment == 'no' and self.x_aa_ol_discount_amount:
                self.amount = invoice.amount_residual
                self.x_aa_ol_writeoff_account_id = False
                self.x_aa_ol_payment_difference_handling = 'open'
                self.x_aa_ol_payment_difference = 0.0
            else:
                write_off_account_id = self.env['account.account'].search([
                    ('code', '=', '706500')]).id or False
                self.amount = invoice.amount_residual - self.x_aa_ol_discount_amount
                self.x_aa_ol_payment_difference_handling = 'reconcile'
                self.x_aa_ol_writeoff_account_id = write_off_account_id or False


class PaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

#     '''Update payment values by decrease discount amount.'''
    def _create_payment_vals_from_wizard(self,batch_result):
        res = super(PaymentRegister, self)._create_payment_vals_from_wizard(batch_result)
        write_off_account_id = self.env['ir.config_parameter'].sudo().get_param('write_off_account_id') or False
        amount = res.get('amount')
        active_ids = self._context.get('active_id')
        invoices = self.env['account.move'].browse(active_ids)
        if (invoices.partner_id and invoices.partner_id.x_aa_ol_discount_percentage and invoices.x_aa_ol_discount_date and invoices.x_aa_ol_discount_date >= datetime.today().date() and invoices.move_type in ('in_invoice') or invoices.move_type in ('in_refund')):
            discountAmount = (invoices.amount_untaxed * invoices.partner_id.x_aa_ol_discount_percentage) / 100 or 0.0
            if not write_off_account_id:
                write_off = self.env['account.account'].search([
                    ('code', '=', '706500')])
                if write_off:
                    write_off_account_id = write_off.id
                else:
                    write_off_account_id = self.env['account.account'].create({
                        'code': '706500',
                        'name': 'Payment discount creditors',
                        'account_type':'expense_direct_cost'                                                
                    }).id
                        # 'user_type_id': self.env['account.account.type'].search([('name', '=', 'Cost of Revenue')],limit=1).id
            res.update({
                'amount': abs(amount) - discountAmount or 0.0,
                'x_aa_ol_payment_difference_handling': 'reconcile',
                'x_aa_ol_writeoff_account_id': int(write_off_account_id),
                'x_aa_ol_writeoff_label': 'Write-Off',
                'x_aa_ol_payment_difference': -discountAmount or 0.0,
            })
        return res
