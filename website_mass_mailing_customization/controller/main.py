# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import tools, _
from odoo.http import route, request
from odoo.addons.website_mass_mailing.controllers.main import MassMailController


class MassMailController(MassMailController):

    # @route('/website_mass_mailing/subscribe', type='json', website=True, auth="public")
    # def subscribe(self, list_id, email, **post):
    @route('/website_mass_mailing/subscribe', type='json', website=True, auth='public')
    def subscribe(self, list_id, value, subscription_type, **post):
        # ovverride controller to make mail list according user website language
        ContactSubscription = request.env['mailing.subscription'].sudo()
        Contacts = request.env['mailing.contact'].sudo()
        # name, email = Contacts.get_name_email(email)
        if subscription_type == 'email':
            name, value = tools.parse_contact_from_email(value)
        elif subscription_type == 'mobile':
            name = value
        language = request.env['res.lang'].search([('code', '=', request.context.get('lang'))])
        mail_list_obj = request.env['mailing.list'].sudo().search(
            [('x_aa_ol_lang', '=', language.id)], limit=1)
        fname = self._get_fname(subscription_type)
        subscription = ContactSubscription.sudo().search(
            [('list_id', '=', mail_list_obj.id), (f'contact_id.{fname}', '=', value),
             ('contact_id.x_aa_ol_language', '=', language.id)])
        if mail_list_obj:
            if not subscription:
                contact_id = Contacts.search([(fname, '=', value)], limit=1)
                if not contact_id:
                    contact_id = Contacts.create({'name': name, fname: value, 'x_aa_ol_language': language.id})
                ContactSubscription.create({'contact_id': contact_id.id, 'list_id': mail_list_obj.id})
            elif subscription.opt_out:
                subscription.opt_out = False
            # add email to session
            request.session[f'mass_mailing_{fname}'] = value
            mass_mailing_list = request.env['mailing.list'].sudo().browse(mail_list_obj.id)
            return {
                'toast_type': 'success',
                # 'toast_content': mass_mailing_list.toast_content
                'toast_content': _("Thanks for subscribing!"),
            }
        return super().subscribe(list_id, value,subscription_type, **post)
