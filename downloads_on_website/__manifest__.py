# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Download Option on Website',
    'version': '17.0',
    'category': 'Website',
    'sequence': 1,
    'summary': '',
    'description':
        """
        Features:
            1. This module allows to see and Download the Documents of Product
            on Website to users based on their language.
        """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['theme_prime', 'product_document_page', 'product_variant_link', 'sale_custom_fields'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/download_share.xml',
        'views/layout_view.xml',
        # 'views/assets.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
    'assets': {
        'web.assets_frontend': [
            '/downloads_on_website/static/src/js/skucode.js'
        ]
    },
}
