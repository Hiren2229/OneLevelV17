# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Fixed Currency Pricelists',
    'summary': "Fixed Currency Pricelists",
    'description': """ Module for adding a fixed product price field, based on a currency selected in res.company settings.
    1. Select a Fixed Currency in Company info (res.company)
    2. The new price should be displayed at product form.
    If you make use of pricelists, the unit price will also be rounded 
    """,
    "version": "17.0.0.0.0",
    'category': 'Sales',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': [
        'product'
    ],
    'data': [
        'views/product_inherit.xml',
    ],
    'installable': True,
}
