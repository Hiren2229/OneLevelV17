# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields


class MailingList(models.Model):
    _inherit = 'mailing.list'

    x_aa_ol_lang = fields.Many2many('res.lang', string='Language')
