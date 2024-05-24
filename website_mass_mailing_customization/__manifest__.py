# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Website Mass Mailing Customization',
    'version': '17.0',
    'category': 'Website',
    'summary': 'Create Mail List According to the User language',
    'description': """
    * Create Mail List According to the User language
     """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'www.aardug.nl',
    'depends': ['website_mass_mailing', 'mass_mailing'],
    'data': [
        'views/mailing_list_view.xml',
        'views/mail_contact_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
