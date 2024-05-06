# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Product Cost Price Security',
    'summary': "Only Responsible Person access cost price",
    'description': """This Module allows to give edit product cost price access rights
    1. Only Users that has this rights can edit the product cost price other can only see. """,
    "version": "17.0.0.1.0",
    'category': 'product',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['product'],
    "application": True,
    'data': [
        'security/product_field_security.xml',
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
