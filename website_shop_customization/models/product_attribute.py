# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    x_aa_ol_is_ral_color = fields.Boolean('Is RAL Color Options', default=False)


    @api.constrains('x_aa_ol_is_ral_color')
    def check_ral_color_option(self):
        check_rec = self.search([('x_aa_ol_is_ral_color','=',True)])
        for record in self:
            if check_rec and record.x_aa_ol_is_ral_color:
                raise ValidationError(_('Only Surface has this value'))

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    x_aa_ol_is_color = fields.Boolean(string="Color", default=False)
