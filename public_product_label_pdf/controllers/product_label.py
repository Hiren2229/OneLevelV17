# -*- coding: utf-8 -*-
import xmlrpc.client

from odoo.http import Controller, request, route

from werkzeug.exceptions import BadRequest
import logging

_logger = logging.getLogger(__name__)


class SaleRestApi(Controller):

    @route(['/print/productlabel/<string:internal_ref>',
            '/print/productlabel/<string:internal_ref>/<string:ral_code>',
            '/print/productlabel/<string:internal_ref>/<string:ral_code>/<string:size>'], type='http', methods=['GET'], auth='public', csrf=False)
    def print_productlabel(self, internal_ref, ral_code=None, size=None):
        product_ids = request.env['product.template'].sudo().search([('default_code', '=', internal_ref)], limit=1)
        if product_ids:
            # {'context': {'lang': 'en_US', 'tz': 'Asia/Calcutta', 'uid': 2, 'allowed_company_ids': [1], 'active_model': 'product.template', 'active_id': 15, 'active_ids': [15], 'default_product_tmpl_ids': [15]}, 'active_model': 'product.template', 'quantity_by_product': {'15': 1}, 'layout_wizard': 2, 'price_included': False, 'report_type': 'pdf'}
            pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf('public_product_label_pdf.report_product_template_label_own', product_ids.ids[0],
                {'active_model': 'product.template',
                 'quantity_by_product': {str(product_ids.ids[0]): 1},
                  'layout_wizard': 2, 
                  'price_included': False, 
                  'report_type': 'pdf',
                  'ral_code': ral_code or '',
                  'size': size or ''})[0]
            response = request.make_response(pdf, headers=[('Content-Type', 'application/pdf')])

            return response
        return BadRequest('Product not found')
