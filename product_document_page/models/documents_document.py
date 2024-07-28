# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


def get_folder_data(row_no):
    document_folder = [
        (0, 'folder_2d_pdf_id', 'Product/Download/2D Information/2D PDF/', '2D PDF', 'node'),
        (1, 'folder_2d_dwg_id', 'Product/Download/2D Information/2D DWG/', '2D DWG', 'node'),
        (2, 'folder_cut_drawings_id', 'Product/Download/Cut Drawings/', 'Cut Drawings', 'node'),
        (3, 'folder_bend_drawings_id', 'Product/Download/Bend Drawings/', 'Bend Drawings', 'node'),
        (4, 'folder_certification_id', 'Media/Certification/', 'Certification', 'parent'),
        (5, 'folder_mounting_instructions_id', 'Media/Printing/Mounting Instructions/', 'Mounting Instructions',
         'parent'),
        (6, 'folder_production_drawings_id', 'Product/Download/Production Drawings/', 'Production Drawings', 'both'),
        (7, 'folder_delivery_note_attachments_id', 'Product/Delivery Note Attachments/', 'Delivery Note Attachments',
         'node'),
    ]
    return document_folder[row_no]


class DocumentsDocumentInherit(models.Model):
    _inherit = 'documents.document'

    # return folders ids
    def _get_folder_ids_for_document_type(self, expected_type):
        folder_ids = []
        workspaces = self.env['documents.folder'].sudo().search([])
        for folder_id in workspaces:
            # test if folder matching
            folder_documents_type = folder_id.get_folder_documents_type()
            if folder_documents_type and folder_documents_type == expected_type:
                folder_ids.append(folder_id.id)
        return folder_ids

    # return folders records
    def find_folder_id_by_documents_type(self, documents_type):
        documents_type_folder_ids = self._get_folder_ids_for_document_type(documents_type)
        domain = [('id', 'in', documents_type_folder_ids)]
        folder_ids = self.env['documents.folder'].sudo().search(domain)
        if folder_ids:
            return folder_ids
        else:
            error_message = documents_type + ' Folder not exist in Folders'
            raise ValidationError(error_message)

    @api.model
    def create(self, vals_list):
        document_processed = True
        document_types = [get_folder_data(0)[3], get_folder_data(1)[3], get_folder_data(2)[3],
                          get_folder_data(3)[3], get_folder_data(4)[3], get_folder_data(5)[3], get_folder_data(6)[3]
                          ]
        # raise UserError(vals_list.keys())
        if 'folder_id' in vals_list:
            folder_id = self.env['documents.folder'].sudo().search([('id', '=', vals_list['folder_id'])], limit=1)
            # raise UserError(folder_id.name)
            if folder_id:
                uploaded_document_type = folder_id.get_folder_documents_type()
                if uploaded_document_type:
                    if uploaded_document_type in document_types:
                        existing_document = self.env['documents.document'].search(
                            [('folder_id', '=', folder_id.id), ('name', '=', vals_list['name']),
                             ('res_model', '=', 'documents.document'), ('type', '=', 'binary')], limit=1)

                        vals_list['partner_id'] = existing_document.partner_id.id

                        '''if document already exists then update it '''
                        if existing_document:
                            existing_document.write(vals_list)
                            document_processed = True
                            return existing_document
                        else:
                            '''document doesn't  exist then create one  '''
                            folder_2d_pdf_id = self._get_folder_ids_for_document_type(get_folder_data(0)[3])
                            folder_2d_dwg_id = self._get_folder_ids_for_document_type(get_folder_data(1)[3])
                            folder_cut_drawings_id = self._get_folder_ids_for_document_type(get_folder_data(2)[3])
                            folder_bend_drawings_id = self._get_folder_ids_for_document_type(get_folder_data(3)[3])
                            folder_certification_id = self._get_folder_ids_for_document_type(get_folder_data(4)[3])
                            folder_mounting_instructions_id = self._get_folder_ids_for_document_type(                    get_folder_data(5)[3])
                            folder_production_drawings_id = self._get_folder_ids_for_document_type(get_folder_data(6)[3])

                            lang_list = ['NL', 'DK', 'FR', 'DE', 'NO', 'ES', 'SE', 'RU', 'US', 'UK', 'EN']
                            lang_dict = {'NL': 'nl', 'DK': 'da_DK', 'FR': 'fr', 'DE': 'de', 'NO': 'nb_NO', 'ES': 'es',
                                         'SE': 'sv', 'RU': 'ru', 'US': 'en_GB', 'UK': 'en_GB', 'EN': 'en_GB', }

                            ''' if the uploading done in 2D PDF folder or in its subfolders'''
                            ''' folder_matching make sure if the uploading done in 2D PDF folder or in its sub folders'''
                            document_type = get_folder_data(0)[3]  # get_folder_data(0)[3] = 2D PDF

                            if folder_id.id in folder_2d_pdf_id:

                                '''prepare document group'''
                                group_id = self.env['documents.groups'].search([('name', '=', document_type)], limit=1)
                                vals_list['x_ad_ol_document_group'] = group_id.id
                                file_name = vals_list['name']

                                '''prepare document lang'''
                                pdf_lang = (file_name.split('-')[1].split('.')[0]).upper()
                                if pdf_lang in lang_list:
                                    lang_code = (lang_dict[pdf_lang])
                                    lang_id = self.env['res.lang'].search([('iso_code', '=', lang_code)], limit=1)
                                    vals_list['x_aa_ol_language_id'] = lang_id.id
                            '''create the new record'''
                            created_doc = super(DocumentsDocumentInherit, self).create(vals_list)

                            if created_doc and created_doc.folder_id.get_folder_documents_type() in document_types:
                                document_name_without_extension = created_doc.name.split('.')[0]
                                '''get the document name without language'''
                                if len(document_name_without_extension.split('-')) > 2:
                                    document_name_without_language = document_name_without_extension.split('-', 1)[0]
                                elif len(document_name_without_extension.split('-')) > 1 and \
                                        document_name_without_extension.split('-')[
                                            1] in lang_list:
                                    document_name_without_language = document_name_without_extension.split('-')[0]
                                else:
                                    document_name_without_language = document_name_without_extension

                                '''link all products having the with the new document created if it is have the same name and  
                                folder '''

                                if folder_id.id in folder_2d_pdf_id:
                                    products_with_drawing_name = self.env['product.template'].search(
                                        [('x_aa_ol_product_drawing_name', '=', document_name_without_language),
                                         ('x_aa_ol_product_drawing_name', '!=', False)])
                                    if products_with_drawing_name:
                                        for product in products_with_drawing_name:
                                            doc_written = False
                                            for doc in product.x_aa_ol_product_document_id:
                                                if doc.name == created_doc.name:
                                                    product.sudo().write(
                                                        {'x_aa_ol_product_document_id': [(3, doc.id),
                                                                                         (4, created_doc.id)]})
                                                    doc_written = True
                                            if not doc_written:
                                                product.sudo().write(
                                                    {'x_aa_ol_product_document_id': [(4, created_doc.id)]})

                                elif created_doc.folder_id.id in folder_2d_dwg_id:
                                    products_with_drawing_dwg_name = self.env['product.template'].search(
                                        [('x_ad_ol_product_drawing_dwg_name', '=', document_name_without_language),
                                         ('x_ad_ol_product_drawing_dwg_name', '!=', False)])
                                    if products_with_drawing_dwg_name:

                                        for product in products_with_drawing_dwg_name:
                                            doc_written = False
                                            for doc in product.x_aa_ol_product_document_id:
                                                if doc.name == created_doc.name:
                                                    product.sudo().write(
                                                        {'x_aa_ol_product_document_id': [(3, doc.id),
                                                                                         (4, created_doc.id)]})
                                                    doc_written = True
                                            if not doc_written:
                                                product.sudo().write(
                                                    {'x_aa_ol_product_document_id': [(4, created_doc.id)]})
                                # update 149 end
                                elif created_doc.folder_id.id in folder_cut_drawings_id:
                                    products_with_cut_drawing_name = self.env['product.template'].search(
                                        [('x_aa_ol_product_cut_drawing', '=', document_name_without_language),
                                         ('x_aa_ol_product_cut_drawing', '!=', False)])
                                    if products_with_cut_drawing_name:
                                        for product in products_with_cut_drawing_name:
                                            doc_written = False
                                            for doc in product.x_aa_ol_product_document_id:
                                                if doc.name == created_doc.name:
                                                    product.sudo().write(
                                                        {'x_aa_ol_product_document_id': [(3, doc.id),
                                                                                         (4, created_doc.id)]})
                                                    doc_written = True
                                            if not doc_written:
                                                product.sudo().write(
                                                    {'x_aa_ol_product_document_id': [(4, created_doc.id)]})
                                elif created_doc.folder_id.id in folder_bend_drawings_id:
                                    products_with_bend_drawing_name = self.env['product.template'].search(
                                        [('x_aa_ol_product_bend_drawing', '=', document_name_without_language),
                                         ('x_aa_ol_product_bend_drawing', '!=', False)])
                                    if products_with_bend_drawing_name:
                                        for product in products_with_bend_drawing_name:
                                            doc_written = False
                                            for doc in product.x_aa_ol_product_document_id:
                                                if doc.name == created_doc.name:
                                                    product.sudo().write(
                                                        {'x_aa_ol_product_document_id': [(3, doc.id),
                                                                                         (4, created_doc.id)]})
                                                    doc_written = True
                                            if not doc_written:
                                                product.sudo().write(
                                                    {'x_aa_ol_product_document_id': [(4, created_doc.id)]})

                                elif created_doc.folder_id.id in folder_mounting_instructions_id:
                                    products_with_manual_mounting = self.env['product.template'].search(
                                        [('x_ad_ol_product_mounting_manual_name', '=', document_name_without_language),
                                         ('x_ad_ol_product_mounting_manual_name', '!=', False)])
                                    if products_with_manual_mounting:
                                        for product in products_with_manual_mounting:
                                            doc_written = False
                                            for doc in product.x_aa_ol_product_document_id:
                                                if doc.name == created_doc.name:
                                                    product.sudo().write(
                                                        {'x_aa_ol_product_document_id': [(3, doc.id),
                                                                                         (4, created_doc.id)]})
                                                    doc_written = True
                                            if not doc_written:
                                                product.sudo().write(
                                                    {'x_aa_ol_product_document_id': [(4, created_doc.id)]})
                                elif created_doc.folder_id.id in folder_production_drawings_id:
                                    if '-rev' in created_doc.name.lower():
                                        document_production_name = created_doc.name.split('-rev')[0]
                                    else:
                                        document_production_name = created_doc.name.split('.')[0]
                                    products_with_production_drawings = self.env['product.template'].search(
                                        [('x_ad_ol_product_production_drawing_name', '=', document_production_name),
                                         ('x_ad_ol_product_production_drawing_name', '!=', False)])
                                    if products_with_production_drawings:
                                        for product in products_with_production_drawings:
                                            doc_written = False
                                            for doc in product.x_aa_ol_product_document_id:
                                                if doc.name == created_doc.name:
                                                    product.sudo().write(
                                                        {'x_aa_ol_product_document_id': [(3, doc.id),
                                                                                         (4, created_doc.id)]})
                                                    doc_written = True
                                            if not doc_written:
                                                product.sudo().write(
                                                    {'x_aa_ol_product_document_id': [(4, created_doc.id)]})
                            if created_doc:
                                return created_doc
                            else:
                                raise UserError(_('Error happening while uploading'))
                    else:
                        document_processed = False
                else:
                    document_processed = False
            else:
                document_processed = False
        else:
            document_processed = False
        if not document_processed:
            created_doc = super(DocumentsDocumentInherit, self).create(vals_list)
            return created_doc

    def find_folder_id_by_documents_type(self, documents_type):
        domain = [('x_ad_ol_folder_document_type', '=', documents_type)]
        folder_ids = self.env['documents.folder'].sudo().search(domain)
        if folder_ids:
            return folder_ids.ids
        else:
            error_message = documents_type + ' Folder not exist in Folders'
            raise ValidationError(error_message)

    def action_donwload_cloud_file(self):
        """
        The method to retrieve content from clouds

        Methods:
         * upload_attachment_from_cloud_ui of ir.attachment

        Returns:
         * action dict

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        return {
            "type": 'ir.actions.act_url',
            "target": 'new',
            "url": "web/content/{}?download=true".format(self.attachment_id.id),
        }

    # <!-- -------------------------updated by adaweyeh ------------------------- -->
    # <!-- -----------------------------22/09/2022 ------------------------------ -->
    # method to preview the document based on in its link stored in url field
    # update 150
    def download_file(self):
        for rec in self:
            if rec.attachment_id:
                url = "/web/content/?model=ir.attachment&id=" + str(
                    rec.attachment_id.id) + "&filename_field=name&field=datas&download=true&name=" + \
                      rec.attachment_id.name + "?download=true"
                return {
                    'type': 'ir.actions.act_url',
                    'target': 'new',
                    'url': url,
                }
            else:
                raise ValidationError("error in attachment")
    # update 150 end
