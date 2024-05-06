# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _ 


class PartnerSalutation(models.Model):
    _inherit = 'res.partner'

    xaa_aa_firstname = fields.Char("First name")
    xaa_aa_lastname = fields.Char("Last name")
    xaa_aa_informal_salutation = fields.Selection([('hello','Hello'),('best','Best')],string='Informal Salutation', default='hello')
    xaa_aa_formal_salutation = fields.Selection([('dear','Dear')], string='Formal Salutation', default='dear')
    xaa_aa_formal_partner_salutation = fields.Char(string='Formal Partner Salutation', translate=True)
    xaa_aa_informal_partner_salutation = fields.Char(string='Informal Partner Salutation', translate=True)

    # update 263
    x_ad_ol_is_private_person = fields.Boolean('Attention! Private person')
    x_ad_ol_is_delivery_phone_call_required = fields.Boolean('Call Customer Before Delivery')
    x_ad_ol_is_forklift_delivery = fields.Boolean('Forklift for delivery')
    # update 263 end

    @api.onchange('xaa_aa_informal_salutation', 'xaa_aa_firstname')
    def _onchange_partner_salutation(self):
        ''' Set  Informal Partner Salutation based on first name and informal salutation type'''
        if self.xaa_aa_firstname and self.xaa_aa_informal_salutation:
            xaa_aa_informal_salutation = dict(self._fields['xaa_aa_informal_salutation'].selection).get(self.xaa_aa_informal_salutation)
            self.xaa_aa_informal_partner_salutation = _(xaa_aa_informal_salutation)+ ' ' + self.xaa_aa_firstname
        else:
            self.xaa_aa_informal_partner_salutation = False

    @api.onchange('xaa_aa_formal_salutation', 'title', 'xaa_aa_lastname')
    def _onchange_par_formal_salutation(self):
        ''' Set Formal Partner Salutation based on title, lastname and formal salutaion type'''
        if self.xaa_aa_lastname and self.xaa_aa_formal_salutation:
            nameContent = []
            xaa_aa_formal_salutation = dict(self._fields['xaa_aa_formal_salutation'].selection).get(self.xaa_aa_formal_salutation)
            nameContent.append(_(xaa_aa_formal_salutation))
            nameContent.append(self.title and self.title.name or '')
            nameContent.append(self.xaa_aa_lastname or '')
            title = ' '.join([x for x in nameContent if x])
            self.xaa_aa_formal_partner_salutation = title
        else:
            self.xaa_aa_formal_partner_salutation = False

    @api.onchange('xaa_aa_lastname', 'xaa_aa_firstname')
    def _onchange_first_last_salutation(self):
        ''' Set  Name of Partner based on first name and last name'''
        sequence = ()
        if self.xaa_aa_firstname and self.xaa_aa_lastname:
            sequence = (self.xaa_aa_firstname,self.xaa_aa_lastname)
        elif self.xaa_aa_firstname:
            sequence = (self.xaa_aa_firstname,'')
        elif self.xaa_aa_lastname:
            sequence = (self.xaa_aa_lastname,'')
        else:
            self.name = ''

        self.name = " ".join(sequence)

    @api.model_create_multi
    def create(self,vals_list):
        ''' create first & last name based on name field '''
        res = super(PartnerSalutation,self).create(vals_list)
        if res.xaa_aa_firstname and res.xaa_aa_informal_salutation:
            xaa_aa_informal_salutation = dict(res._fields['xaa_aa_informal_salutation'].selection).get(res.xaa_aa_informal_salutation)
            res.xaa_aa_informal_partner_salutation = _(xaa_aa_informal_salutation)+ ' ' + res.xaa_aa_firstname
        else:
            res.xaa_aa_informal_partner_salutation = False

        if res.xaa_aa_lastname and res.xaa_aa_formal_salutation:
            nameContent = []
            xaa_aa_formal_salutation = dict(res._fields['xaa_aa_formal_salutation'].selection).get(res.xaa_aa_formal_salutation)
            nameContent.append(_(xaa_aa_formal_salutation))
            nameContent.append(res.title and res.title.name or '')
            nameContent.append(res.xaa_aa_lastname or '')
            title = ' '.join([x for x in nameContent if x])
            res.xaa_aa_formal_partner_salutation = title
        else:
            res.xaa_aa_formal_partner_salutation = False
        return res


