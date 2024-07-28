# -*- coding: utf-8 -*-

from lxml import html
from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal


class SaleShop(CustomerPortal):

    @http.route("/product/long_description", type='json', auth="public", methods=['POST'], website=True)
    def product_long_description(self, product_id, **kwargs):
        if product_id:
            linked_obj_id = request.env['product.product'].sudo().browse(int(product_id))
            str_desc = html.fromstring(linked_obj_id.x_aa_gp_long_description or '<br>')
            if str_desc.text_content().strip() != '':
                long_desc = str(linked_obj_id.x_aa_gp_long_description)
            else:
                product = request.env['product.product'].sudo().search([('x_aa_ol_link_product_id','=',product_id)], limit=1)
                str_desc = html.fromstring(product.x_aa_gp_long_description or '<br>')
                if str_desc.text_content().strip() != '':
                    long_desc = str(product.x_aa_gp_long_description)
                else:
                    long_desc = str(product.product_tmpl_id.x_aa_gp_long_description)
            return long_desc
