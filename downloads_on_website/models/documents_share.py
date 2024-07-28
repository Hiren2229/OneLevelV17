# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################-

from odoo import models, fields, api


class DocumentsShare(models.Model):
    _inherit = 'documents.share'

    x_aa_ol_download_link = fields.Char(string='Download Link', compute='_compute_download_link')

    @api.depends('access_token', 'document_ids')
    def _compute_download_link(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for rec in self:
            if rec.id and rec.access_token and rec.document_ids and len(rec.document_ids) == 1:
                rec.x_aa_ol_download_link = "%s/document/download/%s/%s/%s" % (
                    base_url, rec.id, rec.access_token, rec.document_ids[0].id)
            else:
                rec.x_aa_ol_download_link = False
