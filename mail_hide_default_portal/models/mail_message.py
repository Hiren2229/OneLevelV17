# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models, api


class MessageInherit(models.Model):
    _inherit = 'mail.message'

    is_internal = fields.Boolean('Employee Only',
                                 help='Hide to public / portal users, independently from subtype configuration.',
                                 default=True)
