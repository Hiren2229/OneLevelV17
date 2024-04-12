# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models, api


class InvoiceInherit(models.Model):
    _inherit = "account.move.line"

    x_aa_ol_total_buom = fields.Float(string="Total BUoM", compute="_compute_total_buom", readonly=True)

    @api.depends('quantity', 'product_uom_id')
    def _compute_total_buom(self):
        for line in self:
            if line.product_uom_id.factor_inv:
                line.x_aa_ol_total_buom = line.quantity * line.product_uom_id.factor_inv
            else:
                line.x_aa_ol_total_buom = line.quantity

    def _get_real_number(self, qty):
        return (qty).is_integer()