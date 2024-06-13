# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Website Shop Customization',
    'version': '17.0',
    'category': 'Website',
    'summary': 'Add fields on product and also show in website shop',
    'description': """
    * Add fields on product and also show in website shop
     """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'www.aardug.nl',
    'depends': ['base', 'website', 'website_sale', 'documents',
                'sale_management', 'theme_prime', 'droggol_theme_common', 'sale_custom_fields', 'sale_custom_report', 'order_line_quantity'],
    'data': [
        'security/ir.model.access.csv',
        'views/header_layout.xml',
        'views/color_code_view.xml',
        'views/product_template_inh.xml',
        'views/component_language_pricelist.xml',
        'views/product_view.xml',
        'views/template.xml',
        'views/layout.xml',
        'views/product_attribute_view.xml',
        'views/product_public_category_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_frontend': [
            '/website_shop_customization/static/src/js/add_color_code.js',
            '/website_shop_customization/static/src/js/add_colour_selection.js',
            '/website_shop_customization/static/src/js/pro_comb_notexist.js',
            '/website_shop_customization/static/src/js/add_accessory_product.js'
        ]
    },
}
