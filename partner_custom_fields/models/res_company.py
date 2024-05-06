# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models, _


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    x_aa_ol_custom_domain = fields.Char(string='Domain')