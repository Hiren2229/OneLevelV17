# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController


class WebsiteSaleVariantControllerInh(WebsiteSaleVariantController):
    @http.route()
    def get_combination_info_website(
        self, product_template_id, product_id, combination, add_qty, parent_combination=None,
        **kwargs
    ):
        res = super().get_combination_info_website(product_template_id, product_id, combination, add_qty, parent_combination, **kwargs)
        if res.get('product_id'):
            # product_rec = request.env['product.product'].with_context(warehouse=request.env.company.warehouse_id.id).sudo().browse(res['product_id'])
            product_rec = request.env['product.product'].sudo().browse(res['product_id'])
            rel_product = product_rec.x_aa_ol_link_product_id
            if rel_product:
                main_product = rel_product.product_tmpl_id._get_combination_info()
                res.update({
                    'product_id': rel_product.id,
                    # 'virtual_available': rel_product.x_aa_ol_free_on_hand, // Un-Comment the line After migration of "sale_custom_fields"
                    # 'virtual_available_formatted': rel_product.x_aa_ol_free_on_hand,
                    'list_price' : main_product['list_price'],
                    'price' : main_product['price'],
                    'allow_out_of_stock_order': rel_product.allow_out_of_stock_order,
                    'out_of_stock_message': rel_product.out_of_stock_message or '',
                    'has_discounted_price': main_product['has_discounted_price'],
                    'price_extra': main_product['price_extra'],
                })
            # else:
            #     res.update({
            #         'virtual_available': product_rec.x_aa_ol_free_on_hand,
            #         'virtual_available_formatted': product_rec.x_aa_ol_free_on_hand,
            #     })
        return res