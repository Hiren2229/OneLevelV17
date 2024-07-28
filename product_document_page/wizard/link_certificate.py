# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class DocumentCertificateView1(models.Model):
    _inherit = 'document.flyers.view'

    def action_link_certificates(self):
        product_ids = self.env.context.get('product_ids')
        if not product_ids:
            raise UserError(_("Product ID is missing in the context."))
        product_model = self.env.context.get('product_model')
        products = self.env[product_model].search([('id', 'in', product_ids)])

        if not products:
            raise UserError(_("Product not found."))
        for document in self:
            for product in products:
                l1 = []
                if document.x_ad_ol_doc_id not in product.x_aa_ol_product_document_id.ids:
                    l1.append(document.x_ad_ol_doc_id)
                    l2 = product.x_aa_ol_product_document_id.ids
                    l2.extend(l1)
                    list_4 = list(set(l2))
                    product.x_aa_ol_product_document_id = list_4

    def action_un_link_certificates(self):
        product_ids = self.env.context.get('product_ids')
        if not product_ids:
            raise UserError(_("Product ID is missing in the context."))

        product_model = self.env.context.get('product_model')
        products = self.env[product_model].search([('id', 'in', product_ids)])

        if not products:
            raise UserError(_("Product not found."))
        for document in self:
            for product in products:
                l1 = []
                if document.x_ad_ol_doc_id in product.x_aa_ol_product_document_id.ids:
                    l1.append(document.x_ad_ol_doc_id)
                    l2 = product.x_aa_ol_product_document_id.ids
                    l2 = [x for x in l2 if x not in l1]
                    list_4 = list(set(l2))
                    product.x_aa_ol_product_document_id = list_4

