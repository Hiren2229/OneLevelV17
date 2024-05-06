    # -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################


from odoo import fields, models,api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_aa_ol_qty_diff = fields.Float(
        string='Quantity difference',
        compute='_compute_qty_diff'
    )
    x_aa_ol_price_unit_diff = fields.Float(
        string='Price Total Difference',
        compute='_compute_price_unit_diff',
        store = True
    )
    x_aa_ol_default_code = fields.Char(related='product_id.product_tmpl_id.default_code')

    @api.depends('qty_invoiced', 'qty_received')
    def _compute_qty_diff(self):
        for line in self:
            line.x_aa_ol_qty_diff = line.qty_received - line.qty_invoiced

    @api.depends('x_aa_ol_qty_diff', 'price_unit')
    def _compute_price_unit_diff(self):
        for line in self:
            line.x_aa_ol_price_unit_diff = line.x_aa_ol_qty_diff*line.price_unit

    def _get_product_purchase_description(self, product_lang):
        super(PurchaseOrderLine, self)._get_product_purchase_description(product_lang)
        name = product_lang.name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase

        return name

    # updated by adaweyeh
    # 05-04-2023
    # Update 80
    x_ad_ol_backorder_qty = fields.Float("BackOrder Qty", compute='_compute_x_ad_ol_backorder_qty' ,search='_x_ad_ol_backorder_qty_search')

    def _x_ad_ol_backorder_qty_search(self, operator, value):
        recs = self.search([]).filtered_domain([('x_ad_ol_backorder_qty', '!=', False)])
        recs = recs.filtered_domain([('x_ad_ol_backorder_qty', operator, value)])
        if recs:
            return [('id', 'in', [x.id for x in recs])]
    # Update 80 **** end ****
    def _compute_x_ad_ol_backorder_qty(self):
        '''calculate actual backorder qty for PO Lines'''
        for rec in self:
            find_move = self.env['stock.move'].search([('purchase_line_id', '=', rec.id)])
            if find_move:
                for move in find_move:
                    if move.picking_id.backorder_id:
                        for line in move.picking_id.move_ids_without_package:
                            if line.product_uom_qty and line.product_id == rec.product_id and \
                                line.quantity_done == 0 and line.state != 'cancel':
                                rec.x_ad_ol_backorder_qty += line.product_uom_qty
                            else:
                                rec.x_ad_ol_backorder_qty = 0.0
                    else:
                        rec.x_ad_ol_backorder_qty = 0.0
            else:
                rec.x_ad_ol_backorder_qty = 0.0
