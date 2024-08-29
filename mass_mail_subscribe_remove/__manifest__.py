# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Mass Mailing Subscribe Remove',
    'version': '17.0.0.0',
    'category': 'Marketing/Email Marketing',
    'summary': 'Remove unsubscribe template from emails.',
    'description': """
    * Remove unsubscribe template from emails
    * Remove odoo branding from emails
     """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'www.aardug.nl',
    'depends': ['mass_mailing'],
    'data': [
        'views/template.xml',
    ],
    'installable': True,
    'auto_install': False,
}
