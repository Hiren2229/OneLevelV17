# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Extra Fields At Signup',
    'summary': "Add Extra Fields At Signup",
    'description': """This Module allows to Add Extra Fields At Signup.""",
    "version": "17.0.0.1.0",
    'category': 'Hidden/Tools',
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['auth_signup', 'portal'],
    'data': [
        'views/signup_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
