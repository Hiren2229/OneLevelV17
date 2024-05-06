# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrderInherit, self).onchange_partner_id()
        if self.partner_id.x_aa_ol_default_delivery_address:
            values = {
                'partner_shipping_id': self.partner_id.x_aa_ol_default_delivery_address,
            }
            self.update(values)
