# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Invoice Number Sequence',
    'summary': "Invoice Number Sequence",
    'description': """Change invoice and creditnote number sequence for sale and purchase""",
    "version": "17.0.0.1",
    'category': 'Account',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['account'],
    'data': [
        'data/account_data.xml',
        ],
    'installable': True,
}
