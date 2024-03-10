# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    x_aa_ol_default_sales_contact = fields.Many2one('res.partner', string='Contact Person')

    @api.onchange('partner_id')
    def _onchange_partner_sales_contact(self):
        if self.partner_id:
            if self.partner_id.x_aa_ol_default_sales_contact:
                self.x_aa_ol_default_sales_contact = self.partner_id.x_aa_ol_default_sales_contact
            elif self.partner_id.child_ids:
                for rec in self.partner_id.child_ids:
                    if rec.type == 'contact':
                        self.x_aa_ol_default_sales_contact = rec
                        break
            else:
                self.x_aa_ol_default_sales_contact = self.partner_id
