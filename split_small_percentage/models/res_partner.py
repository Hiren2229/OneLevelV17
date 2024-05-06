# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    x_aa_ol_payment_day = fields.Integer('Payment in Days')
    x_aa_ol_discount_percentage = fields.Float('Discount Percentage')
    # update 92-contact
    x_ad_ol_purchase_transport_days = fields.Integer(string="Purchase Transport Days")
    # update 92-contact *** end ***