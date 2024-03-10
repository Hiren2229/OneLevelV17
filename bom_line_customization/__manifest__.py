# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'BOM Line Customization',
    "version": "17.0.0.0.0",
    'summary': 'Select Multiple Products at BOM Components',
    'description': """
        Here add Domain on product that we can select products
        which has no company or a selected company on a BOM Components.
    """,
    'category': 'MRP',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'depends': [
                'mrp',
                ],
    'data': [
        'views/bom_line_view.xml',
    ],
    'installable': True,
    'application': False,
}