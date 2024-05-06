# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order.line"

    x_aa_ol_total_buom = fields.Float(string="Total BUoM", compute="_compute_total_buom", readonly=True)

    @api.depends('product_uom_qty', 'product_uom')
    def _compute_total_buom(self):
        for line in self:
            if line.product_uom.factor_inv:
                line.x_aa_ol_total_buom = line.product_uom_qty * line.product_uom.factor_inv
            else:
                line.x_aa_ol_total_buom = line.product_uom_qty
