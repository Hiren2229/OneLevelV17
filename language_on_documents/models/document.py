# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import logging

logger = logging.getLogger(__name__)


# update 268 step1
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


# update 268 step1 end

class Document(models.Model):
    _inherit = 'documents.document'
    _description = 'Document'

    x_aa_ol_language_id = fields.Many2one('res.lang', string="Language")
    # update 162 step1
    x_ad_ol_document_group = fields.Many2one('documents.groups', string='Group')
    # update 162 step1 end
    # update 162 step3
    x_ad_ol_online_name = fields.Char('Online Name', translate=True)
    x_ad_ol_certification_country = fields.Many2one('res.country', string='Certif. Country')
    x_ad_ol_is_published = fields.Boolean('Published')
    x_ad_ol_is_certification_document = fields.Boolean(compute='_compute_x_ad_ol_is_certification_document',
                                                       default=False)

    # update 248 step1
    x_ad_ol_folder_full_path = fields.Char('Path Name', related='folder_id.x_ad_ol_folder_full_path')

    # fix issue mail_template
    def correct_document_resource_model(self):
        for rec in self:
            if rec.res_model == 'mail.template':
                try:
                    if rec.attachment_id:
                        rec.attachment_id.write({'res_model': 'documents.document', 'res_id': rec.id})
                        logger.info(f"Updated attachment {rec.attachment_id.name} for template {rec.name}")
                    else:
                        logger.warning(f"No attachment found for template {rec.name}")
                except Exception as e:
                    logger.error(f"Error updating attachment for template {rec.name}: {e}")

    # fix issue mail_template end

    # update 248 step1 end

    def _compute_x_ad_ol_is_certification_document(self):
        certification_code = get_folder_data(4)[3]
        for rec in self:
            folder_documents_type = rec.folder_id.get_folder_documents_type()
            if folder_documents_type and folder_documents_type == certification_code:
                rec.x_ad_ol_is_certification_document = True
            else:
                rec.x_ad_ol_is_certification_document = False

    # update 162 step3 end


# update  162 step1
class DocumentGroups(models.Model):
    _name = 'documents.groups'
    _description = 'Documents groups'

    sequence = fields.Integer(string="Sequence")
    name = fields.Char('Group Name', required=True, translate=True)
    x_ad_ol_documents_line_ids = fields.One2many(comodel_name="documents.document",
                                                 inverse_name="x_ad_ol_document_group",
                                                 string="Group Document Line Ids")
    x_ad_ol_document_group_logo = fields.Image("Logo", max_width=128, max_height=128)
    x_ad_ol_document_group_logo_exits = fields.Boolean('logo_filled',
                                                       compute='_compute_x_ad_ol_document_group_logo_exits')

    def _compute_x_ad_ol_document_group_logo_exits(self):
        for rec in self:
            has_image = False
            if rec.x_ad_ol_document_group_logo:
                has_image = True
            rec.x_ad_ol_document_group_logo_exits = has_image


# update  162 end step1

class ir_attachment(models.Model):
    _inherit = "ir.attachment"

    document_ids = fields.One2many(
        "documents.document",
        "attachment_id",
        string="Related documents"
    )

    @api.depends("document_ids", "document_ids.folder_id")
    def _compute_folder_id(self):
        """
        Compute method for folder_id
        """
        for attachment in self:
            folder_id = False
            handler = False
            if attachment.document_ids:
                folder_id = attachment.document_ids[0].folder_id
                if hasattr(attachment.document_ids, "handler"):
                    handler = attachment.document_ids[0].handler
            attachment.folder_id = folder_id
            attachment.handler = handler

    folder_id = fields.Many2one(
        "documents.folder",
        compute=_compute_folder_id,
        compute_sudo=True,
        store=True,
    )
    handler = fields.Char(
        compute=_compute_folder_id,
        compute_sudo=True,
        store=True,
    )

    # update 162 step3
    @api.depends("document_ids", "document_ids.x_ad_ol_document_group")
    def _compute_document_group(self):
        """
        Compute method for document_group
        """
        for attachment in self:
            document_group = False
            if attachment.document_ids:
                document_group = attachment.document_ids[0].x_ad_ol_document_group
            attachment.x_ad_ol_document_group = document_group

    x_ad_ol_document_group = fields.Many2one(
        "documents.groups",
        compute=_compute_document_group,
        compute_sudo=True,
        store=True,
    )


# Update 162 step3 end

# update 248 step1

class DocumentsFolder(models.Model):
    _inherit = "documents.folder"

    # update 268 step1
    x_ad_ol_folder_document_type = fields.Selection([('2D PDF', '2D PDF'),
                                                     ('2D DWG', '2D DWG'),
                                                     ('Cut Drawings', 'Cut Drawings'),
                                                     ('Bend Drawings', 'Bend Drawings'),
                                                     ('Certification', 'Certification'),
                                                     ('Mounting Instructions', 'Mounting Instructions'),
                                                     ('Production Drawings', 'Production Drawings'),
                                                     ('Flyers', 'Flyers'),
                                                     ('Catalogs', 'Catalogs'),
                                                     ('Delivery Note Attachments', 'Delivery Note Attachments')
                                                     ], string='Folder Documents Type')
    # update 268 step1 end
    x_ad_ol_folder_full_path = fields.Char('Path Name', compute='_compute_x_ad_ol_folder_full_path')

    def _compute_x_ad_ol_folder_full_path(self):
        for workspace in self:
            if workspace.parent_folder_id:
                folder_list = [workspace.name.lstrip().rstrip()]
                folder_id = workspace.parent_folder_id
                while folder_id:
                    node = folder_id.name_get()[0][1]
                    if '/' in node:
                        node = node.split('/')[1]
                    folder_list.append(node.lstrip().rstrip())
                    folder_id = folder_id.parent_folder_id
                full_path = ''
                folder_list.reverse()
                for folder in folder_list:
                    full_path = full_path + folder.lstrip().rstrip() + '/'
                workspace.x_ad_ol_folder_full_path = full_path
            else:
                # Handle cases where workspace has no parent (root level)
                full_path = workspace.name
                workspace.x_ad_ol_folder_full_path = full_path

    def get_folder_documents_type(self):
        self.ensure_one()
        folder_document_type = False
        for rec in self:
            folder_id = rec
            while folder_id:
                folder_document_type = folder_id.x_ad_ol_folder_document_type
                if folder_document_type:
                    return folder_document_type
                folder_id = folder_id.parent_folder_id
        return folder_document_type

    def folder_matching(self, expected_type):
        self.ensure_one()
        matching = False
        if expected_type:
            for rec in self:
                if rec.get_folder_documents_type():
                    if rec.get_folder_documents_type() == expected_type:
                        matching = True
        else:
            raise ValidationError('folder_matching method need expected_type')
        return matching
# update 248 step1 end
