# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_aa_gp_short_description = fields.Html('Short Description', translate=True)
    x_aa_gp_long_description = fields.Html('Long Description', translate=True)
    x_aa_gp_is_color_code = fields.Boolean('Is Color Code')
