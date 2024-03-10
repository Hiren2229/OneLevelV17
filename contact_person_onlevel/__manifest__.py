# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Contact Person OnLevel',
    'summary': "Adds contact person selection to contact application and sale order",
    'description': """
    Select a default sales contact person under a company.
    This contact will be automatically filled in under a sale order, and can be used in the email template to send the
    email to.
    """,
    "version": "17.0.1.0.0",
    'category': 'Sales',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': [
        'base', 'contacts', 'sale'
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
