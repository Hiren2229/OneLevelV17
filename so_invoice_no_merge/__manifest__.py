# -*- coding: utf-8 -*-
{
    'name': "SO Invoicing No Merge",

    'summary': """
        This Module Used to Restrict the invoice to be merged for a specific customer
        """,

    'description': """
        This module Gives one options on Customer Form To Check Whether For Customer 
        Invoices Needs to Merged or Not.
    """,
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Accounting',
    'version': '17.0',
    'depends': ['base', 'sale', 'product'],
    'data': [
        'views/view_partner_property_form.xml',
    ],
}
