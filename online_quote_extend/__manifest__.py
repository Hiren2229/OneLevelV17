# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Customer Reference At quote',
    'summary': "Show Customer Reference at online web quote",
    'description': """This Module allows to show customer reference
    at online web quotation.""",
    "version": "17.0.0.1.0",
    'category': 'Hidden/Tools',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['sale_stock'],
    'data': [
        'views/sale_portal_template.xml',
    ],
    'installable': True,
    'auto_install': False,
}
