# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import http
from odoo.http import request, route
# from odoo.addons.sale.controllers.variant import VariantController
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController

# class VariantControllerInh(VariantController):
class WebsiteSaleStockVariantControllerInh(WebsiteSaleVariantController):
    # WebsiteSaleVariantController
    @route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, parent_combination=None,
        **kwargs):
        res = super().get_combination_info_website(product_template_id=product_template_id, product_id=product_id, combination=combination,add_qty=add_qty, parent_combination=parent_combination, **kwargs)
        uom_price = res['price']
        website = request.env['website'].search([('id', '=', request.env.context.get('website_id'))])
        lang = request.env.context.get('lang')
        if 'linked_product' in res and res['linked_product']:
            res['uom_name'] = res['linked_product'].uom_id.name
        res['price'] = res['price'] * add_qty
        res.update({
            'website_currency': website.currency_id.symbol,
            'web_language': lang,
            'per_product_price': uom_price
        })
        if combination:
            tmpl = request.env['product.template'].browse(product_template_id)
            filtered_variant = tmpl.product_variant_ids.filtered(lambda x: x.product_template_attribute_value_ids and
                all(combo in x.product_template_attribute_value_ids.ids for combo in combination[:-1]))
            val_obj = request.env['product.template.attribute.value']
            values = val_obj.search([(
                'attribute_line_id.id', '=', val_obj.browse(combination[-1]).attribute_line_id.id)]).ids
            not_found_values = []
            for val in values:
                found = False
                for var in filtered_variant:
                    if val in var.product_template_attribute_value_ids.ids:
                        found = True
                        break
                if not found:
                    not_found_values.append(val)
            res.update({
                'remove_val': not_found_values
            })
        return res
    # @http.route(['/sale/get_combination_info'], type='json', auth="user", methods=['POST'])
    # def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
    #     res = super().get_combination_info(product_template_id, product_id, combination, add_qty, pricelist_id, **kw)
    #     uom_price = res['price']
    #     website = request.env['website'].search([('id', '=', request.env.context.get('website_id'))])
    #     lang = request.env.context.get('lang')
    #     if 'linked_product' in res and res['linked_product']:
    #         res['uom_name'] = res['linked_product'].uom_id.name
    #     res['price'] = res['price'] * add_qty
    #     res.update({
    #         'website_currency': website.currency_id.symbol,
    #         'web_language': lang,
    #         'per_product_price': uom_price
    #     })
    #     if combination:
    #         tmpl = request.env['product.template'].browse(product_template_id)
    #         filtered_variant = tmpl.product_variant_ids.filtered(lambda x: x.product_template_attribute_value_ids and
    #             all(combo in x.product_template_attribute_value_ids.ids for combo in combination[:-1]))
    #         val_obj = request.env['product.template.attribute.value']
    #         values = val_obj.search([(
    #             'attribute_line_id.id', '=', val_obj.browse(combination[-1]).attribute_line_id.id)]).ids
    #         not_found_values = []
    #         for val in values:
    #             found = False
    #             for var in filtered_variant:
    #                 if val in var.product_template_attribute_value_ids.ids:
    #                     found = True
    #                     break
    #             if not found:
    #                 not_found_values.append(val)
    #         res.update({
    #             'remove_val': not_found_values
    #         })
    #     return res
