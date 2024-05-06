# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models
import base64

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking'

    
    x_aa_ol_packaging_line = fields.One2many('packaging.details', 'x_aa_ol_package_id', string='Packaging details', copy=True, auto_join=True)


# create below class for a packaging details on delivery orders like length, width and height.
class PackagingDetails(models.Model):
    _name = 'packaging.details'
    _description = 'Details of Packaging of delivery orders'
    _order = 'x_aa_ol_package_id'


    x_aa_ol_package_id = fields.Many2one('stock.picking', string='Picking Reference', required=True, ondelete='cascade', index=True, copy=False)
    x_aa_ol_colli = fields.Integer('Colli')
    x_aa_ol_length = fields.Char('Length')
    x_aa_ol_width = fields.Char('Width')
    x_aa_ol_height = fields.Char('Height')
    x_aa_ol_weight = fields.Char('Weight')