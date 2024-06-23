# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Website Link Product Shows',
    'version': '17.0.0.0',
    'category': 'Website',
    'summary': 'Shows linked product varient based on reference',
    'description': """
    * Shows linked product varient based on reference
     """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'www.aardug.nl',
    'depends': ['product_variant_link', 'website_sale',
                'sale_management','theme_prime'],
    'data': [
        'views/template.xml'
    ],
    'installable': True,
    'auto_install': False,
}
