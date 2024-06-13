# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Language On Documents',
    'version': '17.0',
    'category': 'Documents',
    'sequence': 1,
    'summary': 'add Language field on Documents',
    'description':
        """
        Features:
            1. This module allows to Select Language of Documents.
        """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'depends': ['documents'],
    'data': [
        'security/ir.model.access.csv',
        'views/documents_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
    'assets': {
        'web.assets_backend': [
            'language_on_documents/static/src/js/document_languaue.js',
            'language_on_documents/static/src/xml/document_model_fields.xml'
            # 'language_on_documents/static/src/js/documents_inspector.js',
            # 'language_on_documents/static/src/js/documents_view_mixin.js',
        ]
    }
}
