# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Extend Shipping Method Calculation',
    'summary': "Extend Shipping Method Calculation",
    'description': """ 
    Adds Length option to shipping method calculations and make shipping method
    Calculation based on Products Groos Weight instead of weight.
    """,
    "version": "17.0.0.0",
    'category': 'Sales',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': [
        'product', 'delivery', 'partner_kvk'
    ],
    'data': [
        'views/product_view.xml',
        'views/delivery_rule_view.xml',
    ],
    'installable': True,
}
