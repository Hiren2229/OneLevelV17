# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Pricelist items on Product',
    'summary': "Show extra prices as list view",
    'description': """ Pricelist items on Product

    Adds a list of pricelist prices per product to the product template sale view
    """,
    "version": "17.0.0.0.0",
    'category': 'Product',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['product', 'sale'],
    'data': [
        'views/product_template_views.xml'
    ],
    'installable': True,
}
