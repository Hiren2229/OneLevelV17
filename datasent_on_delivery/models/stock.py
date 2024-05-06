# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models

AVAILABLE_PRIORITIES = [
    ('0', 'No'),
    ('1', 'Yes')
]

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking'

    x_aa_ol_data_sent = fields.Selection(AVAILABLE_PRIORITIES, "Data Sent", default='0')