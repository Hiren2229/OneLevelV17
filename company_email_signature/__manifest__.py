# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Company Email Signature',
    'version': '17.0.0.0.0',
    'summary': 'Company Email Signature',
    'description': """
    Adds an email signature field to res company, which can be printed on the email templates.
    """,
    'category': 'Base',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'depends': [
        'base'
    ],
    'data': [
        'views/res_company_view_inh.xml'
    ],
    'installable': True,
    'application': False,
}
