# -*- coding: utf-8 -*-

from odoo import api, fields, models, api, _
from odoo.exceptions import UserError, ValidationError

# update 222
class LinkProductsDocuments(models.TransientModel):
    _name = 'link.products.documents'
    _description = 'Link Products Documents'

    x_ad_ol_product_ids = fields.Many2many('product.template', string='Products')
    drawing_name_option = fields.Boolean('Drawing Name', default=True)
    drawing_name_dwg_option = fields.Boolean('Drawing DWG', default=True)
    cut_drawing_name_option = fields.Boolean('Cut Drawing', default=True)
    bend_drawing_name_option = fields.Boolean('Bend Drawing', default=True)
    certification_name_option = fields.Boolean('Certification ', default=True)
    mounting_manual_option = fields.Boolean('Mounting Manual Name', default=True)
    production_drawing_name_option = fields.Boolean('Production Drawing Name', default=True)

    def options_select_all(self):
        self.drawing_name_option = True
        self.drawing_name_dwg_option = True
        self.cut_drawing_name_option = True
        self.bend_drawing_name_option = True
        self.certification_name_option = True
        self.mounting_manual_option = True
        self.production_drawing_name_option = True
        return {
            'view_mode': 'form',
            'name': _('Link Product Documents'),
            'view_id': False,
            'res_model': self._name,
            'domain': [],
            'context': dict(self._context, active_ids=self.ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

    def options_deselect_all (self):
        self.drawing_name_option = False
        self.drawing_name_dwg_option = False
        self.cut_drawing_name_option = False
        self.bend_drawing_name_option = False
        self.certification_name_option = False
        self.mounting_manual_option = False
        self.production_drawing_name_option = False

        return {
            'view_mode': 'form',
            'name': _('Link Product Documents'),
            'view_id': False,
            'res_model': self._name,
            'domain': [],
            'context': dict(self._context, active_ids=self.ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

    def link_products_to_documents(self):
        for rec in self:
            for product in rec.x_ad_ol_product_ids:
                if rec.drawing_name_option:
                    product.button_link_drawing()
                if rec.drawing_name_dwg_option:
                    product.button_link_drawing_dwg()
                if rec.cut_drawing_name_option:
                    product.button_link_cut()
                if rec.bend_drawing_name_option:
                    product.button_link_bend()
                if rec.certification_name_option:
                    product.button_link_certification()
                if rec.mounting_manual_option:
                    product.button_link_mounting_manual()
                if rec.production_drawing_name_option:
                    product.button_link_production_drawing()

