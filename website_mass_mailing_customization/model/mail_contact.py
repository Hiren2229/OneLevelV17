# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields


class MassMaillingContact(models.Model):
    _inherit = 'mailing.contact'

    x_aa_ol_language = fields.Many2one('res.lang', string='Language')
