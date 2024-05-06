# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields

class resPartner(models.Model):
    _inherit = 'res.partner'

    kvk = fields.Char('CoC')
