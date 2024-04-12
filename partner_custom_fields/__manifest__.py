# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
{
    'name': 'Partner Custom Fields',
    'summary': "Customizations to contact card",
    'description': """  Contacts
    1. Default delivery date
    """,
    "version": "17.0.1.0.0",
    'category': 'Contacts',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': [
        'base',
        'contacts',
        'sale'
    ],
    'data': [
        'views/res_partner_inherit_view.xml',
        'views/res_company_view.xml',
    ],
    'installable': True,
}
