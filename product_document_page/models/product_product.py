# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
import base64
import io
import zipfile
from odoo import http
from odoo.http import request


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


def compare_strings_dwg(str1, str2):
    # remove extension
    string1 = str1.split('.')[0].lower()
    string2 = str2.split('.')[0].lower()
    # If the lengths of the strings are not equal, return False
    if len(string1) != len(string2):
        return False

    # Iterate over each character in the strings
    for c1, c2 in zip(string1, string2):
        # If the characters are equal or one of them is 'x', continue to the next character
        if c1 == c2 or c1 == 'x' or c2 == 'x':
            continue
        else:
            # If characters are not equal and none of them are 'x', return False
            return False

    # If all characters are either equal or one of them is 'x', return True
    return True


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

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

    def download_document_file(self, document_type, document_name):
        self.ensure_one()
        document_to_download = False
        folder_ids = self._get_folder_ids_for_document_type(document_type)
        if folder_ids:
            for document in self.x_aa_ol_product_document_id:
                folder_matching = document.folder_id.id in folder_ids
                if document_type == '2D DWG':
                    name_matching = compare_strings_dwg(document_name, document.name)
                else:
                    name_matching = document_name in document.name
                if name_matching and folder_matching:
                    ext = document.name.lower().split('.')[1]
                    if document_type == '2D PDF':
                        if self.check_lang(document.name):
                            document_to_download = document
                            break
                    elif document_type == '2D DWG':
                        if ext == 'dwg':
                            document_to_download = document
                            break
                    elif document_type in ['Cut Drawings', 'Bend Drawings']:
                        if ext == 'pdf':
                            document_to_download = document
                            break
                    elif document_type in ['Mounting Instructions']:
                        document_to_download = document
                        break
            if document_to_download:
                return document_to_download.action_donwload_cloud_file()

    @api.depends('product_tmpl_id')
    def download_drawing_file(self):
        row = get_folder_data(0)
        res = self.download_document_file(row[3], self.x_aa_ol_product_drawing_name)
        return res

    @api.depends('product_tmpl_id')
    def download_drawing_dwg_file(self):
        row = get_folder_data(1)
        res = self.download_document_file(row[3], self.x_ad_ol_product_drawing_dwg_name)
        return res

    @api.depends('product_tmpl_id')
    def download_cut_drawing_file(self):
        row = get_folder_data(2)
        res = self.download_document_file(row[3], self.x_aa_ol_product_cut_drawing)
        return res

    @api.depends('product_tmpl_id')
    def download_bend_drawing_file(self):
        row = get_folder_data(3)
        res = self.download_document_file(row[3], self.x_aa_ol_product_bend_drawing)
        return res

    @api.depends('product_tmpl_id')
    def download_certification_file(self):
        self.ensure_one()
        document_type = get_folder_data(4)[3]
        folder_ids = self._get_folder_ids_for_document_type(document_type)
        list_ids = []
        document_to_download = False
        if self.x_aa_ol_product_document_id:
            for document in self.x_aa_ol_product_document_id:
                if folder_ids:
                    if document.folder_id.id in folder_ids:
                        list_ids.append(document.id)
                        document_to_download = document

        if len(list_ids) == 1:
            if document_to_download:
                return document_to_download.action_donwload_cloud_file()
            else:
                raise UserError('no Documents found to download')
        elif len(list_ids) > 0:
            url = '/product_product/download_documents?res_id={}&list_ids={}&document_type={}' \
                .format(self.id, list_ids, document_type)
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }
        else:
            raise ValidationError('No Production Drawings Documents had been linked ')

    @api.depends('product_tmpl_id')
    def download_mounting_manual_file(self):
        row = get_folder_data(5)
        res = self.download_document_file(row[3], self.x_ad_ol_product_mounting_manual_name)
        return res

    @api.depends('product_tmpl_id')
    def download_production_drawing_file(self):
        self.ensure_one()
        document_type = get_folder_data(6)[3]
        folder_ids = self._get_folder_ids_for_document_type(document_type)
        list_ids = []
        document_to_download = False
        if self.x_aa_ol_product_document_id:
            for document in self.x_aa_ol_product_document_id:
                if folder_ids:
                    if document.folder_id.id in folder_ids:
                        name_matching = self.x_ad_ol_product_production_drawing_name in document.name
                        if name_matching:
                            list_ids.append(document.id)
                            document_to_download = document

        if len(list_ids) == 1:
            if document_to_download:
                return document_to_download.action_donwload_cloud_file()
            else:
                raise UserError('no Documents found to download')

        elif len(list_ids) > 0:
            url = '/product_product/download_documents?res_id={}&list_ids={}&document_type={}' \
                .format(self.id, list_ids, document_type)
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }
        else:
            raise ValidationError('No Production Drawings Documents had been linked ')

    def check_lang(self, document_name):
        flag = False
        lang = self._context.get("lang") or self.env.user.lang
        active_langs = ['en_GB', 'en_US', 'nl_NL', 'da_DK', 'fr_FR', 'de_DE', 'nb_NO', 'es_ES', 'sv_SE']
        if lang in ['en_GB', 'en_US']:
            lang_code = 'en'
        else:
            lang_code = lang.split('_')[0]
        if lang in active_langs and lang_code.lower() in document_name.lower():
            flag = True
        return flag

    def button_un_link_drawing(self):
        row = get_folder_data(0)
        for rec in self:
            if rec.x_aa_ol_product_drawing_name:
                rec.unlink_document(rec.x_aa_ol_product_drawing_name, 'pdf', row[3])

    def button_un_link_drawing_dwg(self):
        row = get_folder_data(1)
        for rec in self:
            if rec.x_ad_ol_product_drawing_dwg_name:
                rec.unlink_document(rec.x_ad_ol_product_drawing_dwg_name, 'dwg', row[3])

    def button_un_link_cut(self):
        row = get_folder_data(2)
        for rec in self:
            if rec.x_aa_ol_product_cut_drawing:
                rec.unlink_document(rec.x_aa_ol_product_cut_drawing, 'pdf', row[3])

    def button_un_link_bend(self):
        row = get_folder_data(3)
        for rec in self:
            if rec.x_aa_ol_product_bend_drawing:
                rec.unlink_document(rec.x_aa_ol_product_bend_drawing, 'pdf', row[3])

    def button_link_certification(self):
        self.ensure_one()
        document_type = get_folder_data(4)[3]
        certification_folders_ids = self._get_folder_ids_for_document_type(document_type)
        items = []
        if certification_folders_ids and len(certification_folders_ids) > 0:
            items = self.env['documents.document'].search(
                [('folder_id', 'in', certification_folders_ids)]).ids
        if items and len(items) > 0:
            for rec in self:
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Documents'),
                    'view_mode': 'tree',
                    'res_model': 'document.flyers.view',
                    'views': [(False, 'tree')],
                    'view_id': False,
                    'target': 'new',
                    'domain': [('x_ad_ol_doc_id', 'in', items)],
                    'context': {'called_context': self.env.context,
                                'product_ids': [rec.id],
                                'items': items,
                                'hide_button_link_certification': False,
                                'hide_button_un_link_certification': True,
                                'hide_button_attach_flyers': True,
                                'product_model':'product.product'
                                }
                }

    def link_products_certificate_wizard(self, vals):
        if vals:
            document_type = get_folder_data(4)[3]
            certification_folders_ids = self._get_folder_ids_for_document_type(document_type)
            items = []
            if certification_folders_ids and len(certification_folders_ids) > 0:
                items = self.env['documents.document'].search(
                    [('folder_id', 'in', certification_folders_ids)]).ids
            if items and len(items) > 0:
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Certificates'),
                    'view_mode': 'tree',
                    'res_model': 'document.flyers.view',
                    'views': [(False, 'tree')],
                    'view_id': False,
                    'target': 'new',
                    'domain': [('x_ad_ol_doc_id', 'in', items)],
                    'context': {'called_context': self.env.context,
                                'product_ids': vals.ids,
                                'items': items,
                                'hide_button_link_certification': False,
                                'hide_button_un_link_certification': True,
                                'hide_button_attach_flyers': True,
                                'product_model':'product.product'}
                }
        else:
            raise UserError(_("No records selected in the tree view."))
    def button_un_link_mounting_manual(self):
        row = get_folder_data(5)
        for rec in self:
            if rec.x_ad_ol_product_mounting_manual_name:
                rec.unlink_document(rec.x_ad_ol_product_mounting_manual_name, 'pdf', row[3])

    def button_un_link_production_drawing(self):
        row = get_folder_data(6)
        for rec in self:
            if rec.x_ad_ol_product_production_drawing_name:
                rec.unlink_document(rec.x_ad_ol_product_production_drawing_name, 'pdf', row[3])
    def button_un_link_certification(self):
        self.ensure_one()
        document_type = get_folder_data(4)[3]
        folder_ids = self.env['documents.folder'].sudo().search([])
        certification_folders = []
        for folder_id in folder_ids:
            if folder_id.folder_matching(document_type):
                certification_folders.append(folder_id.id)
        if certification_folders and len(certification_folders) > 0:
            items = self.env['documents.document'].search(
                [('folder_id', 'in', certification_folders)]).ids
            selected_items = self.env['documents.document'].search(
                [('folder_id', 'in', certification_folders),
                 ('id', 'in', self.x_aa_ol_product_document_id.ids)
                 ]).ids
            return {
                'type': 'ir.actions.act_window',
                'name': _('Certificates'),
                'view_mode': 'tree',
                'res_model': 'document.flyers.view',
                'views': [(False, 'tree')],
                'view_id': False,
                'target': 'new',
                'domain': [('x_ad_ol_doc_id', 'in', selected_items)],
                'context': {'called_context': self.env.context,
                            'product_ids': [self.id],
                            'items': items,
                            'hide_button_link_certification': True,
                            'hide_button_un_link_certification': False,
                            'hide_button_attach_flyers': True,
                            'product_model':'product.product'
                            }
            }
    def button_link_drawing(self):
        row = get_folder_data(0)
        for rec in self:
            if not rec.x_aa_ol_product_drawing_name:
                rec.x_aa_ol_product_drawing_name = rec._compute_document_field_value_ol()
                if rec.x_aa_ol_product_drawing_name:
                    rec.link_document(rec.x_aa_ol_product_drawing_name, 'pdf', row[3])
                else:
                    raise UserError(_('You have to fill Customer Drawing Name'))
            else:
                rec.link_document(rec.x_aa_ol_product_drawing_name, 'pdf', row[3])


    def button_link_drawing_dwg(self):
        row = get_folder_data(1)
        for rec in self:
            if not rec.x_ad_ol_product_drawing_dwg_name:
                rec.x_ad_ol_product_drawing_dwg_name = rec._compute_document_field_value_ol()
                if rec.x_ad_ol_product_drawing_dwg_name:
                    rec.link_document(rec.x_ad_ol_product_drawing_dwg_name, 'dwg', row[3])
                else:
                    raise UserError(_('You have to fill Customer DWG Name'))
            else:
                rec.link_document(rec.x_ad_ol_product_drawing_dwg_name, 'dwg', row[3])
    def button_link_cut(self):
        row = get_folder_data(2)
        for rec in self:
            if not rec.x_aa_ol_product_cut_drawing:
                rec.x_aa_ol_product_cut_drawing = rec._compute_document_field_value_ol()
                if rec.x_aa_ol_product_cut_drawing:
                    rec.link_document(rec.x_aa_ol_product_cut_drawing, 'pdf', row[3])
                else:
                    raise UserError(_('You have to fill Cut Drawing Name'))
            else:
                rec.link_document(rec.x_ad_ol_product_drawing_dwg_name, 'dwg', row[3])

    def button_link_bend(self):
        row = get_folder_data(3)
        for rec in self:
            if not rec.x_aa_ol_product_bend_drawing:
                rec.x_aa_ol_product_bend_drawing = rec._compute_document_field_value_ol()
                if rec.x_aa_ol_product_bend_drawing:
                    rec.link_document(rec.x_aa_ol_product_bend_drawing, 'pdf', row[3])
                else:
                    raise UserError(_('You have to fill Bend Drawing Name'))
            else:
                rec.link_document(rec.x_aa_ol_product_bend_drawing, 'pdf', row[3])

    def button_link_mounting_manual(self):
        row = get_folder_data(5)
        for rec in self:
            if rec.x_ad_ol_product_mounting_manual_name:
                rec.link_document(rec.x_ad_ol_product_mounting_manual_name, 'pdf', row[3])

    def button_link_production_drawing(self):
        row = get_folder_data(6)
        for rec in self:
            if rec.x_ad_ol_product_production_drawing_name:
                rec.link_document(rec.x_ad_ol_product_production_drawing_name, 'pdf', row[3])

    def button_link_all_documents(self):
        for rec in self:
            rec.button_link_mounting_manual()
            rec.button_link_certification()
            rec.button_link_bend()
            rec.button_link_cut()
            rec.button_link_drawing()
            rec.button_link_drawing_dwg()
            rec.button_link_production_drawing()

    def button_un_link_all_documents(self):
        l1 = []
        for i in range(7):
            row = get_folder_data(i)
            document_type = row[3]
            folder_ids = self._get_folder_ids_for_document_type(document_type)
            l1.extend(folder_ids)
        for rec in self:
            l2 = rec.x_aa_ol_product_document_id.filtered(lambda document: document.folder_id.id not in l1).ids
            rec.x_aa_ol_product_document_id = l2

    def unlink_document(self, file_name, ext, document_type):
        active_lang_codes = ["-NL", "-DK", "-FR", "-DE", "-NO", "-ES", "-SE", "-RU", "-EN", "-US",
                             "-nl", "-dk", "-fr", "-de", "-no", "-es", "-se", "-ru", "-en", "-us"]
        folder_ids = self._get_folder_ids_for_document_type(document_type)
        for rec in self:
            l1 = []
            for document in rec.x_aa_ol_product_document_id:
                folder_matching = document.folder_id.id in folder_ids

                if document_type in [get_folder_data(0)[3]]:
                    lang_matching = any([x in document.name for x in active_lang_codes])
                else:
                    lang_matching = True
                if document_type in [get_folder_data(6)[3]]:
                    ext_matching = True
                else:
                    ext_matching = ext.lower() in document.name.lower()
                if ext == 'dwg':
                    name_matching = compare_strings_dwg(file_name, document.name)
                else:
                    name_matching = file_name in document.name
                if not (folder_matching and lang_matching and ext_matching and name_matching):
                    l1.append(document.id)
                if len(l1) == 0:
                    rec.x_aa_ol_product_document_id = False
                else:
                    rec.x_aa_ol_product_document_id = l1

    def link_document(self, file_name, ext, document_type):

        active_lang_codes = ["-NL", "-DK", "-FR", "-DE", "-NO", "-ES", "-SE", "-RU", "-EN", "-US",
                             "-nl", "-dk", "-fr", "-de", "-no", "-es", "-se", "-ru", "-en", "-us"]
        for rec in self:
            folder_ids = self._get_folder_ids_for_document_type(document_type)
            if document_type == '2D DWG':
                documents = self.env['documents.document'].search(
                    [('folder_id', 'in', folder_ids), ('res_model', '=', 'documents.document')
                     ])
                l1 = []
                for document in documents:
                    if compare_strings_dwg(document.name, file_name):
                        if ext.lower() in document.name.lower():
                            l1.append(document.id)
                l2 = rec.x_aa_ol_product_document_id.ids
                l2.extend(l1)
                list_4 = list(set(l2))
                rec.x_aa_ol_product_document_id = list_4
            else:
                documents = self.env['documents.document'].search(
                    [('name', 'like', file_name), ('res_model', '=', 'documents.document'),
                     ('folder_id', 'in', folder_ids)])
                l1 = []

                for document in documents:
                    # folder_matching = document.folder_id.folder_matching(document_type)

                    if document_type in [get_folder_data(0)[3]]:
                        lang_matching = any([x in document.name for x in active_lang_codes])
                    else:
                        lang_matching = True

                    if document_type in [get_folder_data(6)[3]]:
                        ext_matching = True
                    else:
                        ext_matching = ext.lower() in document.name.lower()

                    name_matching = file_name.lower() in document.name.lower()
                    if lang_matching and ext_matching and name_matching:
                        l1.append(document.id)
                    l2 = rec.x_aa_ol_product_document_id.ids
                    l2.extend(l1)
                    list_4 = list(set(l2))
                    rec.x_aa_ol_product_document_id = list_4


class DownloadDocuments(http.Controller):
    @http.route('/product_product/download_documents', type='http', auth='user')
    def download_documents(self, **kwargs):
        # Identify documents based on your model and criteria
        product = request.env['product.product'].search(
            [('id', '=', kwargs.get('res_id'))])
        '''get the documents linked to product in order to searched'''
        if 'list_ids' in kwargs:
            list_ids = kwargs.get('list_ids')
        else:
            raise ValidationError("Missing list_ids parameter")

        if 'document_type' in kwargs:
            document_type = kwargs.get('document_type')
        else:
            raise ValidationError("Missing document_type parameter")
        documents = product.x_aa_ol_product_document_id
        if not documents:
            raise ValidationError("No documents found for this product and download type!")
        else:
            # Create the ZIP file in memory
            memory_file = io.BytesIO()
            count = 0
            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for document in documents:
                    if str(document.id) in list_ids:
                        attachment = document.attachment_id
                        file_data = base64.b64decode(attachment.datas)
                        filename = document.name
                        zip_file.writestr(filename, file_data)
                        count += 1

            # Prepare the HTTP response

            if count > 0:
                if document_type == 'Production Drawings':
                    response = request.make_response(memory_file.getvalue(),
                                                     headers=[('Content-Type', 'application/zip'),
                                                              ('Content-Disposition', 'attachment; '
                                                                                      'filename="production_drawing'
                                                                                      '.zip"')])
                elif document_type == 'Certification':

                    response = request.make_response(memory_file.getvalue(),
                                                     headers=[('Content-Type', 'application/zip'),
                                                              ('Content-Disposition', 'attachment; '
                                                                                      'filename="certifications.zip"')])
                else:
                    response = request.make_response(memory_file.getvalue(),
                                                     headers=[('Content-Type', 'application/zip'),
                                                              ('Content-Disposition', 'attachment; '
                                                                                      'filename="documents.zip"')])

                return response
            else:
                raise ValidationError("No documents found for this product and download type!")
