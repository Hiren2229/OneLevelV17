# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.depends('move_type')
    def _get_payment_term_domain(self):
        print("\n\n self",self)
        print("\n\n self._context",self._context)
        move_type = self._context.get('default_move_type', 'entry')
        print("\n\n move_type",move_type)
        print("\n\n self.get_purchase_types(include_receipts=True)",self.get_purchase_types(include_receipts=True))
        print("\n\n self.get_sale_types(include_receipts=True)",self.get_sale_types(include_receipts=True))
        if move_type in self.get_sale_types(include_receipts=True):
            return "[('x_aa_ol_is_sale_payment_term', '=', True)]"
        elif move_type in self.get_purchase_types(include_receipts=True):
            return "[('x_aa_ol_is_purchase_payment_term', '=', True)]"
        else:
            return "[]"

    @api.onchange('invoice_payment_term_id')
    def onchange_truck_field(self):
        print("self.move_type",self.move_type)
        if self.move_type in self.get_sale_types(include_receipts=True):
            return {"domain": {'invoice_payment_term_id' : [('x_aa_ol_is_sale_payment_term', '=', True)]}}

    invoice_payment_term_id = fields.Many2one(domain=_get_payment_term_domain)
