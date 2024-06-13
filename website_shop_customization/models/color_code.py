# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models

class ColorCode(models.Model):
	_name = 'color.code'

	x_aa_ol_name = fields.Char('Name')
	x_aa_ol_color_group = fields.Selection([('no_charge', 'Group 1: No Charge'),
											('extra_charge', 'Group 2: 60€ Extra Charge'),
											('price_on_request', 'Group 3: Price On Request')
											], string="RAL Groups")
