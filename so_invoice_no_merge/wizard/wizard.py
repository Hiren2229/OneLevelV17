# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api, exceptions
from odoo.tools import groupby as groupbyelem
from operator import itemgetter

class SaleAdvancePaymentInvInherit(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        sale_orders_by_partners = [self.env['sale.order'].concat(*g) for k, g in groupbyelem(sale_orders, itemgetter('partner_id'))]
        inv_ids = []
        for so_by_partner in sale_orders_by_partners:
            if so_by_partner[0].partner_id.x_aa_ol_not_merge_invoices:
                res = super(SaleAdvancePaymentInvInherit, self.with_context(flag_merge_invoices=True,active_ids=so_by_partner.ids)).create_invoices()
                if res.get('domain') and res.get('domain')[0] and len(res.get('domain')[0]) > 2:
                    inv_ids.extend(res.get('domain')[0][2])
            else:
                res = super(SaleAdvancePaymentInvInherit, self.with_context(active_ids=so_by_partner.ids)).create_invoices()
                if res.get('res_id'):
                    inv_ids.extend([res.get('res_id')])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action['domain'] = [('id', 'in', inv_ids)]
        return action