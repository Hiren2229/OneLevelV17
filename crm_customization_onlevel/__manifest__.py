# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'CRM Customization Onlevel',
    'version': '17.0.1.0.0',
    'summary': 'CRM Customization Onlevel',
    'description': """
    Adds some fields to the contact form view.
    """,
    'category': 'CRM',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'depends': [
                'base', 'contacts'
                ],
    'data': [
        'views/res_partner_view_inherit.xml',
        'data/crm_custom_parent_cron.xml'
    ],
    'installable': True,
    'application': False,
}
