# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    x_aa_ol_company_signature = fields.Html(string='Company Email Signature')
