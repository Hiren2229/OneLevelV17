# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name' : 'Partner Salutation',
    'version': '17.0',
    'summary': 'Formal And Informal Name For Partner',
    'category': 'Partner',
    'description': """ Generate Formal And Informal Name For Partner,
        Based On Partner First Name And Last Name.
        Below are the functionality of this Module.

        1. Update Partner's Salutation Value based on Opportunity
        2. Set Partner Salutation Based on Partner's Salutation on Sale order. 
    """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'depends': ['contacts'],
    'data': ['views/views.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
