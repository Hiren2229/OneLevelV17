        # -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.http_routing.models.ir_http import slug
from odoo.osv import expression


class WebsiteShowLinkProduct(WebsiteSale):


    def _get_search_domain(self, search, category, attrib_values, search_in_description=True, search_price=False):
        domains = [request.website.sale_product_domain()]
        if search:
            for srch in search.split(" "):
                subdomains = [
                    [('name', 'ilike', srch)],
                    [('product_variant_ids.default_code', 'ilike', srch)]
                ]
                if search_in_description:
                    subdomains.append([('description', 'ilike', srch)])
                    subdomains.append([('description_sale', 'ilike', srch)])
                    subdomains.append([('x_aa_ol_search_name', 'ilike', srch)])
                domains.append(expression.OR(subdomains))

        if category:
            domains.append([('public_categ_ids', 'child_of', int(category))])

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domains.append([('attribute_line_ids.value_ids', 'in', ids)])
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domains.append([('attribute_line_ids.value_ids', 'in', ids)])
        return expression.AND(domains)


    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        '''inherit because when search products need to open main products if searched products is
        linked with it '''
        response = super(WebsiteShowLinkProduct, self).shop(page, category, search, ppg, **post)
        if response.qcontext.get('search') and response.qcontext.get('products'):
            url = "/shop"
            Category = request.env['product.public.category']
            attrib_list = request.httprequest.args.getlist('attrib')
            attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
            attributes_ids = {v[0] for v in attrib_values}
            attrib_set = {v[1] for v in attrib_values}
            search_product = request.env['product.product'].search([
                ('x_aa_ol_link_product_id.product_tmpl_id','in',response.qcontext.get(
                    'products').ids)]).product_tmpl_id
            if search_product:
                website_domain = request.website.website_domain()
                categs_domain = [('parent_id', '=', False)] + website_domain
                if response.qcontext.get('search'):
                    search_categories = Category.search([
                        ('product_tmpl_ids', 'in', search_product.ids)
                        ] + website_domain).parents_and_self
                    categs_domain.append(('id', 'in', search_categories.ids))
                else:
                    search_categories = Category
                categs = Category.search(categs_domain)

                if response.qcontext.get('category'):
                    url = "/shop/category/%s" % slug(response.qcontext.get('category'))

                product_count = len(search_product)
                pager = request.website.pager(
                    url=url, total=product_count, page=page,
                    step=response.qcontext.get('ppg'), scope=7, url_args=post)
                offset = pager['offset']
                products = search_product[offset: offset + response.qcontext.get('ppg')]

                ProductAttribute = request.env['product.attribute']
                if products:
                    # get all products without limit
                    attributes = ProductAttribute.search([
                        ('product_tmpl_ids', 'in', search_product.ids)])
                else:
                    attributes = ProductAttribute.browse(attributes_ids)

                layout_mode = request.session.get('website_sale_shop_layout_mode')
                if not layout_mode:
                    if request.website.viewref('website_sale.products_list_view').active:
                        layout_mode = 'list'
                    else:
                        layout_mode = 'grid'
                bins = TableCompute().process(
                        products, response.qcontext.get('ppg'),
                        response.qcontext.get('ppr'))
                newbins = []
                for i in bins[0]:
                    newbins.append([i])
                response.qcontext.update({
                    'attrib_values': attrib_values,
                    'attrib_set': attrib_set,
                    'pager': pager,
                    'products': products,
                    'search_count': product_count,  # common for all searchbox
                    'bins': newbins,
                    'categories': categs,
                    'attributes': attributes,
                    'search_categories_ids': search_categories.ids,
                    'layout_mode': layout_mode,
                })
        return response


    @http.route('/shop/products/autocomplete', type='json', auth='public', website=True)
    def products_autocomplete(self, term, options={}, **kwargs):
        response = super(WebsiteShowLinkProduct, self).products_autocomplete(term, options={}, **kwargs)
        ProductTemplate = request.env['product.template']
        display_description = options.get('display_description', True)
        display_price = options.get('display_price', True)
        max_nb_chars = options.get('max_nb_chars', 999)
        category = options.get('category')
        attrib_values = options.get('attrib_values')
        domain = self._get_search_domain(term, category, attrib_values, 
            display_description)
        products_lst = []
        for product in response.get('products'):
            products_lst.append(product['id'])
        if response['products']:
            for prd_list in response['products']:
                products_links_variant = request.env['product.product'].search([
                    ('x_aa_ol_link_product_id.product_tmpl_id', '=', prd_list.get('id'))])
                if products_links_variant:
                    for productt in products_links_variant:
                        products = productt.product_tmpl_id
                        fields = ['id', 'name', 'website_url']
                        if display_description:
                            fields.append('description_sale')
                        prd_list.update({'website_url' : productt.website_url})
        for line in response.get('products'):
            if '<span class="oe_currency_value">0.00</span>' in line['price']:
                line['price'] = " "
        return response
