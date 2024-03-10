# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Transport Type',
    'version': '17.0.0.0.0',
    'summary': 'Customers Transport Type Fields',
    'description': """
    """,
    'category': 'Purchase',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'depends': [
                'purchase',
                ],
    'data': [
        'data/transport_types.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
}