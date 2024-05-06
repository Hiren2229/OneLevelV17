# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import email_split



class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.constrains('login')
    def _check_login_partner(self):
        """ Do not allow two users or partner with the same login"""
        if not self.env.context.get('active_model') == 'res.partner':
            for record in self:
                partners = self.env['res.partner'].search([('id', '!=', record.partner_id.id)])
                for partner in partners:
                    if (record.login == partner.email):
                        raise ValidationError('You cannot have two users/partners with the same login/email!')
