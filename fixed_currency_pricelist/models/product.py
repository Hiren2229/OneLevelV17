# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api, tools, _


class InheritProduct(models.Model):
    _inherit = ['product.template']

    x_aa_ol_sale_price_country_currency = fields.Many2one('res.currency', required=True, compute='_compute_sale_price')
    x_aa_ol_sale_price_country = fields.Float(string='Sale Price Valuta', compute='_compute_sale_price')
    x_aa_ol_exists_in_pricelist = fields.Boolean(string='Exists in Pricelist', compute='_compute_sale_price')

    @api.depends('list_price', 'pricelist_item_count')
    def _compute_sale_price(self):
        for product in self:
            product.x_aa_ol_sale_price_country_currency = product.currency_id
            if product.pricelist_item_count == 0:
                product.x_aa_ol_sale_price_country = product.list_price
                product.x_aa_ol_exists_in_pricelist = False
            else:
                pricelist_item = self.env['product.pricelist.item'].search([('product_tmpl_id', '=', product.id), (
                    'currency_id', '=', self.env.company.currency_id.id)], limit=1)
                if pricelist_item:
                    product.x_aa_ol_sale_price_country = pricelist_item[0].fixed_price
                    product.x_aa_ol_sale_price_country_currency = pricelist_item[0].currency_id
                    if pricelist_item[0].pricelist_id.name == 'OnLevel DKK':
                        product.x_aa_ol_exists_in_pricelist = True
                    else:
                        product.x_aa_ol_exists_in_pricelist = False
                        product.x_aa_ol_sale_price_country = product.list_price
                else:
                    product.x_aa_ol_sale_price_country = product.list_price
                    product.x_aa_ol_exists_in_pricelist = False
