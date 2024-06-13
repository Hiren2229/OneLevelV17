# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class DocumentsDocument(models.Model):
    _inherit = 'documents.document'

    x_aa_ol_configuration_id = fields.Char(string='Configuration id')
