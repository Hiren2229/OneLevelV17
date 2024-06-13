# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
import binascii

from odoo import fields, models, api
import base64
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # @api.constrains('order_line', 'amount_untaxed')
    # def add_extra_product(self):
    #     if self.order_line:
    #         extra_charge_product = self.env['product.product'].search([('default_code', '=', '95000000901')], limit=1)
    #         existing_extra_charge_line = self.order_line.filtered(lambda x: x.product_id == extra_charge_product)
    #         total = 0
    #         for record in self.order_line:
    #             if record.product_template_id:
    #                 link_product = self.env['product.product'].search(
    #                     [('x_aa_ol_link_product_id', '=', record.product_id.id)], limit=1) or record.product_id
    #                 if link_product and link_product.valid_product_template_attribute_line_ids.filtered(
    #                         lambda ptal: ptal.attribute_id.x_aa_ol_is_ral_color):
    #                     total += (record.price_unit * record.product_uom_qty)
    #         if total < 250 and not existing_extra_charge_line:
    #             self.env['sale.order.line'].create({
    #                 'product_id': extra_charge_product.id,
    #                 'order_id': self.id
    #             })
    #
    #         if total > 250 and existing_extra_charge_line:
    #             existing_extra_charge_line.unlink()

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        '''update color code on sale order line'''
        res = super()._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
        if res['line_id'] and add_qty != None and res['quantity'] > 0:
            line = self.env['sale.order.line'].browse(res.get('line_id'))
            if kwargs.get('color_code') and kwargs.get('color_code') != 'undefined':
                color_code = self.env['color.code'].search([('id', '=', kwargs.get('color_code'))])
                line.x_aa_gp_color_code = color_code.x_aa_ol_name
                line.name = line.name + ' - ' + color_code.x_aa_ol_name
            else:
                if line and line.x_aa_gp_color_code:
                    line.name = line.name + ' - ' + line.x_aa_gp_color_code
            configuration_id = False
            if 'configuration_id' in kwargs and kwargs.get('configuration_id'):
                line.x_es_ol_configuration_id = configuration_id = kwargs.get('configuration_id')
            if 'pdf_name' in kwargs and 'pdf_content' in kwargs and kwargs.get('pdf_name') and kwargs.get(
                    'pdf_content'):
                try:
                    base64.b64decode(kwargs.get('pdf_content'))
                    attachment = self.env['ir.attachment'].sudo().create({
                        'name': kwargs.get('pdf_name'),
                        'datas': kwargs.get('pdf_content'),
                        'res_model': 'sale.order',
                        'res_id': line.order_id.id,
                    })
                    workspace = self.env['documents.folder'].sudo().search([('name', '=', 'Online Configurator Drawings')],
                                                                    limit=1)
                    if not workspace:
                        _logger.info('Workspace Online Configurator Drawings not found')
                    else:
                        document_values = {
                            'name': attachment.name,
                            'attachment_id': attachment.id,
                            'folder_id': workspace.id,
                            # Replace with the ID of the folder where you want to store the document
                            'file_size': attachment.file_size,
                            'mimetype': attachment.mimetype,
                            'description': attachment.description,
                            'datas': attachment.datas,
                            'x_aa_ol_configuration_id': configuration_id
                        }

                        document = self.env['documents.document'].sudo().create(document_values)

                except (binascii.Error, UnicodeDecodeError):
                    _logger.info('Decode of pdf failed')
        # if self.order_line:
        #     ral_color_lines = self.order_line.filtered(lambda color: color.x_aa_gp_color_code)
        #     extra_charge_product = self.env['product.product'].search([('default_code', '=', '95000000901')], limit=1)
        #     existing_extra_charge_line = self.order_line.filtered(
        #         lambda x: x.product_id == extra_charge_product)
        #
        #     if not existing_extra_charge_line and ral_color_lines and sum(
        #             (x.price_unit * x.product_uom_qty) for x in ral_color_lines
        #     ) < 250:
        #         self.env['sale.order.line'].create({
        #             'product_id': extra_charge_product.id,
        #             'order_id': self.id
        #         })
        #     if ral_color_lines and sum(
        #             (x.price_unit * x.product_uom_qty) for x in ral_color_lines
        #     ) > 250:
        #         self.order_line.filtered(lambda x: x.product_id == extra_charge_product).unlink()
        return res


class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    x_aa_gp_color_code = fields.Char(string='Color code')
