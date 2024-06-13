# -*- coding: utf-8 -*-

from lxml import html
from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal


class SaleShop(CustomerPortal):

    @http.route("/product/accessory_product", type='json', auth="public", methods=['POST'], website=True)
    def accessory_product(self, product_id, **kwargs):
        data = []
        # accessory_product_lst = []
        if product_id:
            product_id = request.env['product.product'].sudo().browse(product_id)
            is_a_linked_product = request.env['product.product'].sudo().search([('x_aa_ol_link_product_id', '=', product_id.id)],limit=1)
            if not product_id.accessory_product_ids and is_a_linked_product:
                accessory_product = is_a_linked_product.accessory_product_ids
            else:
                accessory_product = product_id.accessory_product_ids
            for rec in accessory_product:
                data.append({'ID': rec.id,
                    'Name': rec.name,
                    'URL': rec.website_url,
                    'tempID': rec.product_tmpl_id.id,
                    'categID': rec.public_categ_ids[0].id if rec.public_categ_ids else '',
                    'categname': rec.public_categ_ids[0].name if rec.public_categ_ids else '',
                    'label' : rec.dr_label_id.name
                })
            return data
