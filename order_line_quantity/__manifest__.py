# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Order Line Quantity',
    'summary': 'Order Line Quantity',
    'description': """
Creates new variables to show quantities based on Unit of Measures.
Important to have 'uom' module installed, and enable it in settings.
    """,
    'version': '17.0.0.1.0',
    'category': 'Sales',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'depends': [
        'account',
        'product',
        'sale',
        'purchase',
    ],
    'data': [
        'views/view_sale_order_inherit.xml',
        'views/view_purchase_order_inherit.xml',
        'views/view_invoice_line_inherit.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
