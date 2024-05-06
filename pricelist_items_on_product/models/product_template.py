# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    x_aa_ol_pricelist_items = fields.One2many(
        comodel_name="product.pricelist.item",
        inverse_name="product_tmpl_id",
        string="Pricelist Prices")
