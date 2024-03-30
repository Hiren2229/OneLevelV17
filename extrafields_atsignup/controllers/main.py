# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import logging

import werkzeug

from odoo import http, _
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.base_vat.models.res_partner import _ref_vat
from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS


_logger = logging.getLogger(__name__)

custom_fields_set = {'vat', 'phone', 'company', 'street', 'door', 'zipcode'}
SIGN_UP_REQUEST_PARAMS |= custom_fields_set


class AddCountryData(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True,
                sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                User = request.env['res.users']
                user_sudo = User.sudo().search(
                    User._get_login_domain(qcontext.get('login')),
                    order=User._get_login_order(), limit=1)
                params = dict(request.params)
                country_id = False
                if params.get('country_id') and params.get('country_id').isdigit():
                    country_id = int(params.get('country_id'))
                partner_id = user_sudo.partner_id
                if partner_id:
                    partner_id.sudo().write({
                        'phone': params.get('phone', ''),
                        'company_name': params.get('company', ''),
                        'vat': params.get('vat', ''),
                        'street': params.get('street', ''),
                        'street2': params.get('door', ''),
                        'city': params.get('city', ''),
                        'zip': params.get('zipcode', ''),
                        'country_id': country_id,
                    })
                template = request.env.ref(
                    'auth_signup.mail_template_user_signup_account_created',
                    raise_if_not_found=False)
                if user_sudo and template:
                    template.sudo().send_mail(user_sudo.id,
                                            force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([
                    ("login", "=", qcontext.get("login"))]) or request.env["res.partner"].sudo().search([
                    ("email", "=", qcontext.get("login"))
                ]):
                    qcontext["error"] = _("Another user/ partner is already registered\
                        using this email address.")
                else:
                    msg = ''
                    vat_info = qcontext.get("vat")
                    partner_info = qcontext.get("name")
                    Country = request.env['res.country'].browse(
                        int(qcontext.get("country_id")))
                    country_code = Country.code.lower()
                    vat_no = "'CC##' (CC=Country Code, ##=VAT Number)"
                    vat_no = _ref_vat.get(country_code) or vat_no
                    if request.env.context.get('company_id'):
                        company = request.env['res.company'].browse(
                            request.env.context['company_id'])
                    else:
                        company = request.env.company
                    if company.vat_check_vies:
                        msg = _(
                            'The VAT Number [%(vat)s] for partner [%(name)s] either\
                            failed the VIES VAT validation check did not\
                            respect the expected format %(format)s.',
                            vat=vat_info,
                            name=partner_info,
                            format=vat_no)
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account." + msg)
        countries = request.env['res.country'].sudo().search([])
        qcontext['countries'] = countries
        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
