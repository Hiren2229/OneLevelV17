# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Product Category Archivable',
    'summary': "Product Category Archivable",
    'description': """ Product Category Archivable
    
    Makes the Product Category model's records archivable.
    """,
    "version": "14.0.0",
    'category': 'Product',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['product'],
    'data': [
        'views/product_category_view.xml'
    ],
    'installable': True,
}
