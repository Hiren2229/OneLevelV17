# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from datetime import timedelta, datetime
from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Variant'

    x_aa_ol_link_product_tmpl_id = fields.Many2one('product.template', 'Link Product Template')
    x_aa_ol_link_product_id = fields.Many2one('product.product', 'Link Product')
    x_aa_ol_available_qty_linked_product = fields.Float(related='x_aa_ol_link_product_id.qty_available', string='Linked Products Quantity On Hand')

    def write(self,vals):
        res = super(ProductProduct, self).write(vals)
        for product in self:
            if 'x_aa_ol_link_product_tmpl_id' in vals:
                product_template_id = self.env['product.template'].browse(vals['x_aa_ol_link_product_tmpl_id'])
                if product_template_id:
                    product.write(
                        {'x_aa_ol_link_product_id': product_template_id.product_variant_id.id, 
                        'lst_price' : product_template_id.product_variant_id.lst_price, 
                        'standard_price' : product_template_id.product_variant_id.standard_price, 
                        'image_1920': product_template_id.product_variant_id.image_1920})
        return res


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    def write(self,vals):
        res = super(ProductTemplate, self).write(vals)
        for product in self:
            if 'image_1920' or 'list_price' or 'standard_price' in vals:
                find_linked_variant_id = self.env['product.product'].search([('x_aa_ol_link_product_tmpl_id', '=', product.id)])
                if find_linked_variant_id:
                    find_linked_variant_id.write(
                        {'lst_price' : product.list_price, 
                        'standard_price' : product.standard_price, 
                        'image_1920' : product.image_1920})
        return res
