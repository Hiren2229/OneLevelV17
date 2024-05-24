# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    payment_term_id = fields.Many2one(
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id), ('x_aa_ol_is_purchase_payment_term', '=', True)]")

