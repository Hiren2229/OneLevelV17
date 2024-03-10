# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    x_aa_ol_default_sales_contact = fields.Many2one('res.partner', string='Default Sales Contact',
                                                    domain="['&', ('type', '=', 'contact'), ('id', 'in', child_ids),]")

    def name_get(self):
        res = []
        for partner in self:
            name = partner._get_name()
            res.append((partner.id, name))
        res.sort(key=lambda a: a[1])
        return res

    def _get_name(self):
        name = super(ResPartnerInh, self)._get_name()
        if self.env.context.get('contact'):
            name = self.name
        return name
