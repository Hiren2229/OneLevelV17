# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Data Sent Of Delivery',
    'version': '17.0.1.0.0',
    'category': 'Stock',
    'sequence': 1,
    'summary': 'add field data sent on delivery orders only',
    'description':
        """
        Features:
            1. This module allows to enter details of data sent.
        """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['stock'],
    'data': [
    'views/delivery_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}
