/** @odoo-module **/

import VariantMixin from "@website_sale/js/sale_variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToFragment } from "@web/core/utils/render";
import { localization } from "@web/core/l10n/localization";
import "@website_sale/js/website_sale";
import { jsonrpc } from "@web/core/network/rpc_service";
import { markup } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
publicWidget.registry.WebsiteSale.include({
    /**
     * Adds the stock checking to the regular _onChangeCombination method
     * @override
     */
    onClickAdd: function (ev) {
        this._super.apply(this, arguments);
        var color_code = $("select[name='color_id']")
        if (color_code.val() == '' && !color_code.hasClass('d-none')){
            $("#colorcode_show").show();
            color_code.addClass('is-invalid');
        }
        else{
            $("#colorcode_show").hide();
            color_code.removeClass('is-invalid');
            return this._handleAdd($(ev.currentTarget).closest('form'));
        }
    },
    _updateRootProduct($form, productId) {
        this.rootProduct = {
            product_id: productId,
            quantity: parseFloat($form.find('input[name="add_qty"]').val() || 1),
            product_custom_attribute_values: this.getCustomVariantValues($form.find('.js_product')),
            variant_values: this.getSelectedVariantValues($form.find('.js_product')),
            no_variant_attribute_values: this.getNoVariantAttributeValues($form.find('.js_product')),
            color_code: $("input[name='color_code']").val(),
            color_id: $("select[name='color_id']").val()
        };
    },
});
// odoo.define('website_shop_customization.website_sale', function (require) {
// 'use strict';

// var publicWidget = require('web.public.widget');

// publicWidget.registry.WebsiteSale.include({
//     _handleAdd: function ($form) {
//         var self = this;
//         this.$form = $form;

//         var productSelector = [
//             'input[type="hidden"][name="product_id"]',
//             'input[type="radio"][name="product_id"]:checked'
//         ];

//         var productReady = this.selectOrCreateProduct(
//             $form,
//             parseInt($form.find(productSelector.join(', ')).first().val(), 10),
//             $form.find('.product_template_id').val(),
//             false
//         );

//         return productReady.then(function (productId) {
//             $form.find(productSelector.join(', ')).val(productId);

//             self.rootProduct = {
//                 product_id: productId,
//                 quantity: parseFloat($form.find('input[name="add_qty"]').val() || 1),
//                 product_custom_attribute_values: self.getCustomVariantValues($form.find('.js_product')),
//                 variant_values: self.getSelectedVariantValues($form.find('.js_product')),
//                 no_variant_attribute_values: self.getNoVariantAttributeValues($form.find('.js_product')),
//                 color_code: $("input[name='color_code']").val(),
//                 color_id: $("select[name='color_id']").val()
//             };

//             return self._onProductReady();
//         });
//     },
//     _onClickAdd: function (ev) {
//         ev.preventDefault();
//         this.isBuyNow = $(ev.currentTarget).attr('id') === 'buy_now';
//         var color_code = $("select[name='color_id']")
//         if (color_code.val() == '' && !color_code.hasClass('d-none')){
//                 $("#colorcode_show").show();
//                 color_code.addClass('is-invalid');
//             }
//         else{
//                 $("#colorcode_show").hide();
//                 color_code.removeClass('is-invalid');
//                 return this._handleAdd($(ev.currentTarget).closest('form'));

//             }
//     },

// });


// });
