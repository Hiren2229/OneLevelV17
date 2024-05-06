# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Base Contact Individual Filter',
    'summary': "Base contact individual filter domain change.",
    'description': """ Base contact individual filter domain change. hide 
        contacts which type invoice/delivery
        and Added individual Filter for invoice/Delivery address's.
     """,
    "version": "17.0.1.1.0",
    'category': 'Sales/CRM',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['base', 'contacts'],
    'data': [
        'views/contact.xml',    
    ],
    'installable': True,
    'auto_install': True,
}
