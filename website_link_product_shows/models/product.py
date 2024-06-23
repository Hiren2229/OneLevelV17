# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_first_possible_combination(self, parent_combination=None, necessary_values=None):
        """return related product if found with default code"""
        if self._context.get('search'):
            product = self.env['product.product'].search([
                ('x_aa_ol_link_product_id.default_code', '=', self._context['search'])], limit=1)
            if product:
                return product.product_template_attribute_value_ids
        return super(ProductTemplate, self)._get_first_possible_combination(
            parent_combination=parent_combination, necessary_values=necessary_values)
