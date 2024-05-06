# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name' : 'Split Small Percentage',
    'version': '17.0',
    'summary': 'Split Percentage amount',
    'category': 'Account',
    'description': """ Split Percentage amount to write off account
    1. Add new fields payment_difference , Payment Difference Handling, Difference Account, Journal Item Label, Payment Discount and Discount Amount on Payment Amount. 
    2. Modify _create_payment_vals_from_wizard method.
    3. Remove Onchange Amount Method. 
    4. Remove default Get method from Account Payment because The Same Functionality Is Provided By _create_payment_vals_from_wizard method in Account Payment Register.""",
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'depends': ['account'],
    'data': [
        'views/res_partner_view.xml',
        'views/account_move_view.xml',
        'views/account_payment.xml'
    ],
    'installable' : True
}
