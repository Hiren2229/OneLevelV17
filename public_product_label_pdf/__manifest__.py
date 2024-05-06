# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Public Product Label PDF',
    'summary': "Public Available Product Label Download",
    'description': """ Public Product Label PDF
    
    Opens a public link in order to be able to download product labels.
    """,
    "version": "17.0",
    'category': 'Product',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['product','event'],
    'data': [
        'security/ir.model.access.csv',
        'report/product_label_action.xml'
    ],
    'installable': True,
    'auto_install': False,
}
