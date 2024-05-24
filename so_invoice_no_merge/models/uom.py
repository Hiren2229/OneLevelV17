# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, api

class UoM(models.Model):
    _inherit = 'uom.uom'
    _description = 'Product Unit of Measure'

    @api.depends('factor')
    def _compute_factor_inv(self):
        ''' update factor value by 1 doing this as client want for some uom'''
        for uom in self:
            if uom.id in [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 86]:
                uom.factor_inv = 1
            else:
                uom.factor_inv = uom.factor and (1.0 / uom.factor) or 0.0