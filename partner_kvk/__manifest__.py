# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name' : 'Add KvK (Chamber of Commerce Registration Number) field to partner',
    'version' : '17.0.1.0',
    'category' : 'Customer Relationship Management',
    'description': """
        Add KvK (Chamber of Commerce Registration Number) field to partner form.
    """,
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'depends' : ['account', 'base', 'contacts', 'product'],
    'data' : [
        'views/partner_view.xml',
        'views/product_view.xml',
    ],
    'installable' : True,
    'auto_install' : False,
}
