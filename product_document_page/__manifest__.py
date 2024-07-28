# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Product Document Page',
    'summary': 'Add Document page on product form view',
    'description': '''
        Add Document page on product form view.
    ''',
    'version': '17.0', 
    "license": "LGPL-3",
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'depends': ['product', 'documents_product', 'documents', 'sale_custom_report'],
    'data': [
        'views/product_template_view.xml',
        'wizard/link_products_documents.xml',
        'wizard/link_certificate.xml',
        'security/ir.model.access.csv',
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
