# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models


class ProductCategoryInherit(models.Model):
    _inherit = 'product.category'

    active = fields.Boolean(default=True)
    name = fields.Char('Name', index=True, required=True, translate=True)
