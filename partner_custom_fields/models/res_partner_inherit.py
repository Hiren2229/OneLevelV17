# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import werkzeug.urls


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    x_aa_ol_default_delivery_address = fields.Many2one('res.partner', string="Default Delivery Address")

    property_product_pricelist = fields.Many2one(
        search="_search_property_product_pricelist"
    )

    def _get_signup_url_for_action(self, url=None, action=None, view_type=None, menu_id=None, res_id=None, model=None):
        """ generate a signup url for the given partner ids and action, possibly overriding
            the url state components (menu_id, id, view_type) """

        res = dict.fromkeys(self.ids, False)
        for partner in self:
            base_url = partner.get_base_url()
            if partner.company_id and partner.company_id.x_aa_ol_custom_domain:
                base_url = partner.company_id.x_aa_ol_custom_domain
            # when required, make sure the partner has a valid signup token
            if self.env.context.get('signup_valid') and not partner.user_ids:
                partner.sudo().signup_prepare()

            route = 'login'
            # the parameters to encode for the query
            query = dict(db=self.env.cr.dbname)
            signup_type = self.env.context.get('signup_force_type_in_url', partner.sudo().signup_type or '')
            if signup_type:
                route = 'reset_password' if signup_type == 'reset' else signup_type

            if partner.sudo().signup_token and signup_type:
                query['token'] = partner.sudo().signup_token
            elif partner.user_ids:
                query['login'] = partner.user_ids[0].login
            else:
                continue        # no signup token, no user, thus no signup url!

            if url:
                query['redirect'] = url
            else:
                fragment = dict()
                base = '/web#'
                if action == '/mail/view':
                    base = '/mail/view?'
                elif action:
                    fragment['action'] = action
                if view_type:
                    fragment['view_type'] = view_type
                if menu_id:
                    fragment['menu_id'] = menu_id
                if model:
                    fragment['model'] = model
                if res_id:
                    fragment['res_id'] = res_id

                if fragment:
                    query['redirect'] = base + werkzeug.urls.url_encode(fragment)

            signup_url = "/web/%s?%s" % (route, werkzeug.urls.url_encode(query))
            if not self.env.context.get('relative_url'):
                signup_url = werkzeug.urls.url_join(base_url, signup_url)
            res[partner.id] = signup_url

        return res

    @api.model
    def _search_property_product_pricelist(self, operator, value):
        if operator == "=":

            def filter_func(partner):
                return partner.property_product_pricelist.name == value

        elif operator == "!=":

            def filter_func(partner):
                return partner.property_product_pricelist.name != value

        elif operator == "in":

            def filter_func(partner):
                return partner.property_product_pricelist.name in value

        elif operator == "not in":

            def filter_func(partner):
                return partner.property_product_pricelist.name not in value

        elif operator == "not ilike":

            def filter_func(partner):
                return value.lower() not in partner.property_product_pricelist.name.lower()

        elif operator == "ilike":

            def filter_func(partner):
                return value.lower() in partner.property_product_pricelist.name.lower()

        else:
            raise UserError(
                _("Pricelist field do not support search with the operator '%s'.")
                % operator
            )
        partners = self.with_context(prefetch_fields=False).search([])
        return [("id", "in", partners.filtered(filter_func).ids)]
