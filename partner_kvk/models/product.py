# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    gross_weight = fields.Float(string='Gross weight', digits='Stock Weight')
    net_weight = fields.Float(string='Net weight', digits='Stock Weight')
