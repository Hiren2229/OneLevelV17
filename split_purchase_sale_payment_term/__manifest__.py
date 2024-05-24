# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Split Purchase Sale Payment Terms',
    'summary': "Split Purchase Sale Payment Terms",
    'description': """
    Splits the payment terms up into two different options (can select both): Sale and purchase
    """,
    "version": "17.0",
    'category': 'Sales',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['base', 'account', 'sale', 'purchase'],
    'data': [
        'views/account_move_view.xml',
        'views/payment_terms_inherit.xml',
    ],
    'installable': True,
}
