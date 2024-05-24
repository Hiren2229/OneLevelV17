# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo.osv import expression 
from odoo import fields, models, api


class PaymentTermsInherit(models.Model):
    _inherit = 'account.payment.term'

    x_aa_ol_is_sale_payment_term = fields.Boolean(string='Sales', default=True)
    x_aa_ol_is_purchase_payment_term = fields.Boolean(string='Purchase', default=True)

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        domain = domain or []
        transport_ids = []
        name_domain = []
        if self._context.get("x_aa_vendor_bill"):
            name_domain = [('x_aa_ol_is_purchase_payment_term', "=", True)]
        if self._context.get("x_aa_invoice_bill"):
            name_domain = [('x_aa_ol_is_sale_payment_term', "=", True)]
        domain = expression.AND([name_domain, domain])
        return self._search(domain, limit=10, order=order)

    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        domain = domain or []
        transport_ids = []
        name_domain = []
        if self._context.get("x_aa_vendor_bill"):
            name_domain = [('x_aa_ol_is_purchase_payment_term', "=", True)]
        if self._context.get("x_aa_invoice_bill"):
            name_domain = [('x_aa_ol_is_sale_payment_term', "=", True)]
        domain = expression.AND([name_domain, domain])
        return super().search_fetch(domain, field_names, offset, limit, order)