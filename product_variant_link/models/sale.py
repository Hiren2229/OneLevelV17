# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
    #     '''replace product on sale order line'''
    #     print("our custom _cart_update called>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", product_id)
    #     product_obj = self.env['product.product'].browse(product_id)
    #     if product_obj.x_aa_ol_link_product_id:
    #         product_id = product_obj.x_aa_ol_link_product_id.id
    #     return super()._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
