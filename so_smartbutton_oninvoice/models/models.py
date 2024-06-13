# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _ 


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_aa_ol_sale_count = fields.Integer(string='Sale Count', compute='_get_sales', readonly=True)
    x_aa_ol_sale_ids = fields.Many2many("sale.order", string='Sales', compute="_get_sales", readonly=True, copy=False)

    # Get Sale order details on Invoice based on Origin
    @api.depends('invoice_origin')
    def _get_sales(self):
        for invoice in self:
            sales_order = self.env['sale.order'].search([('name', '=', invoice.invoice_origin)])
            invoice.x_aa_ol_sale_ids = sales_order
            invoice.x_aa_ol_sale_count = len(sales_order)

    # Display Sale Orders from Invoice Form.
    def action_view_sale(self):
        sales = self.mapped('x_aa_ol_sale_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations")
        form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = sales.id
        return action