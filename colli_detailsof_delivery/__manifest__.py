# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################


{
    'name': 'Colli Details of Delivery',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'sequence': 1,
    'summary': '',
    'description':
        """
        Features:
            1. This module allows to enter details of colli
            on Delivery Orders with details like Length, Width,
            and Heigth of Packages(colli).
        """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['stock'],
    'data': [
    'security/ir.model.access.csv',
    'views/delivery_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}