# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################-

from odoo import models, fields, api
from collections import defaultdict
from odoo.exceptions import AccessError, ValidationError, MissingError, UserError
from odoo.http import request

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty,
            parent_combination=parent_combination, only_template=only_template)
        if combination_info['product_id']:
            product = self.env['product.product'].sudo().browse(combination_info['product_id'])
            lists = []
            user_context = request.session.context if request.session.uid else {}
            if product.x_aa_ol_link_product_id:
                lists = [[irow.type, irow.attachment_id.id, irow.name, irow.x_aa_ol_language_id.id, irow.x_aa_ol_language_id.name, irow.mimetype, irow.url] for irow in product.x_aa_ol_link_product_id.x_aa_ol_product_document_id.filtered(lambda lang: lang.x_aa_ol_language_id.code == user_context.get('lang') or not lang.x_aa_ol_language_id)]
            else:
                lists = [[irow.type, irow.attachment_id.id, irow.name, irow.x_aa_ol_language_id.id, irow.x_aa_ol_language_id.name, irow.mimetype, irow.url] for irow in product.x_aa_ol_product_document_id.filtered(lambda lang: lang.x_aa_ol_language_id.code == user_context.get('lang') or not lang.x_aa_ol_language_id)]
            combination_info.update({
                'sku_code': product.x_aa_ol_link_product_id.x_aa_ol_search_name if product.x_aa_ol_link_product_id else product.x_aa_ol_search_name,
                'linked_product' : product.x_aa_ol_link_product_id if product.x_aa_ol_link_product_id else product,
                'document_ids':  lists
            })
            print("\n\n\n lists",lists)
        return combination_info
