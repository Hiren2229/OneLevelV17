# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models
import time
from datetime import datetime, date, timedelta


class AccountMove(models.Model):
    _inherit = 'account.move'


    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountMove, self).create(vals_list)
        for moves in res:
            if moves.move_type == 'out_invoice':
                moves.name = self.env['ir.sequence'].next_by_code('account.invoice')
            if moves.move_type == 'in_invoice':
                moves.name = self.env['ir.sequence'].next_by_code('account.bill')
            if moves.move_type == 'out_refund':
                moves.name = self.env['ir.sequence'].next_by_code('account.creditnote')
            if moves.move_type == 'in_refund':
                moves.name = self.env['ir.sequence'].next_by_code('account.refunds')
        return res