# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models, api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    x_aa_ol_customer_category = fields.Selection([('installer', 'Installer'), ('reseller_dealer', 'Reseller / Dealer'),
                                                  ('general_custruction', 'General construction company / contractor'),
                                                  ('architect_prescription', 'Architect / Prescription'),
                                                  ('other', 'Other')], string="Customer Category")
    x_aa_ol_customer_industry = fields.Selection(
        [('glasing', 'Glasing'), ('metal', 'Metal'), ('interiour_wood', 'Interiour / Wood'),
         ('facade_window', 'Facade / Window'), ('garden', 'Garden'), ('other', 'Other')], string="Customer Industry")
    x_aa_ol_customer_status = fields.Selection(
        [('client', 'Client'), ('cfd', 'CFD needs to be filled out'), ('prospect', 'Prospect'),
         ('suspect', 'Suspect'), ('supplier', 'Supplier'), ('competitor', 'Competitor'), ('bankruptcy', 'Banktrupty'),
         ('other', 'Other')], string="Customer Status")
    x_aa_ol_customer_abc = fields.Selection(
        [('A', 'A (High potential)'), ('B', 'B (Medium potential)'), ('C', 'C (Low potential)')], string="Customer ABC")

    @api.model
    def create(self, vals):
        res = super(ResPartnerInherit, self).create(vals)
        res['x_aa_ol_customer_category'] = res.parent_id.x_aa_ol_customer_category
        res['x_aa_ol_customer_industry'] = res.parent_id.x_aa_ol_customer_industry
        res['x_aa_ol_customer_status'] = res.parent_id.x_aa_ol_customer_status
        res['x_aa_ol_customer_abc'] = res.parent_id.x_aa_ol_customer_abc
        return res

    def write(self, vals):
        res = super(ResPartnerInherit, self).write(vals)
        for rec in self:
            if rec.is_company and (vals.get('x_aa_ol_customer_category') or vals.get('x_aa_ol_customer_industry') \
                                   or vals.get('x_aa_ol_customer_status') or vals.get('x_aa_ol_customer_abc')):
                child_ids = self.env['res.partner'].sudo().search([('parent_id', '=', rec.id)])
                if child_ids:
                    for child in child_ids:
                        child.write({
                            'x_aa_ol_customer_category': rec.x_aa_ol_customer_category,
                            'x_aa_ol_customer_industry': rec.x_aa_ol_customer_industry,
                            'x_aa_ol_customer_status': rec.x_aa_ol_customer_status,
                            'x_aa_ol_customer_abc': rec.x_aa_ol_customer_abc,
                        })
        return res

    def run_crm_cron(self):
        indi_partners = self.env['res.partner'].sudo().search([('is_company', '=', False), ('parent_id', '!=', False)])
        for record in indi_partners:
            record.write({
                'x_aa_ol_customer_category': record.parent_id.x_aa_ol_customer_category,
                'x_aa_ol_customer_industry': record.parent_id.x_aa_ol_customer_industry,
                'x_aa_ol_customer_status': record.parent_id.x_aa_ol_customer_status,
                'x_aa_ol_customer_abc': record.parent_id.x_aa_ol_customer_abc,
            })
