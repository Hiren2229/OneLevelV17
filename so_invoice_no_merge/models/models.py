# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api, _
from odoo.tools import float_compare


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    
    def _create_invoices(self, grouped=False, final=False, date=None):
        if self._context.get('flag_merge_invoices'):
            grouped = self._context.get('flag_merge_invoices')
        return super(SaleOrder, self)._create_invoices(grouped=grouped,final=final,date=date)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_aa_ol_not_merge_invoices = fields.Boolean("Not Merge Invoices")