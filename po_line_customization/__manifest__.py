# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'PO Line Customization',
    'version': '17.0.1.0',
    'summary': 'Separate view for Purchase Order line',
    'description': """
        Separate view for Purchase Order line and
        new field for Quantity differnce and Difference price total
        and filter based on zero quantity difference.
    """,
    'category': 'Purchase',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'depends': [
                'purchase',
                ],
    'data': [
        'views/purchase_views.xml',
    ],
    'installable': True,
    'application': False,
}