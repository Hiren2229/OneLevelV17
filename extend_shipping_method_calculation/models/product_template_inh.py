# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    x_aa_ol_transport_length = fields.Float(string='Transport Length')
