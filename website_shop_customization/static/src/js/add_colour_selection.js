/** @odoo-module **/

import VariantMixin from "@website_sale/js/sale_variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToFragment } from "@web/core/utils/render";
import { localization } from "@web/core/l10n/localization";
import "@website_sale/js/website_sale";
import { jsonrpc } from "@web/core/network/rpc_service";
import { markup } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
/**
 * Addition to the variant_mixin._onChangeCombination
 *
 * This will prevent the user from selecting a quantity that is not available in the
 * stock for that product.
 *
 * It will also display various info/warning messages regarding the select product's stock.
 *
 * This behavior is only applied for the web shop (and not on the SO form)
 * and only for the main product.
 *
 * @param {MouseEvent} ev
 * @param {$.Element} $parent
 * @param {Array} combination
 */
VariantMixin.handleCustomValuesRender = function ($target) {
    var $variantContainer;
    var $customInput = false;
    if ($target.is('select') && $target.data('is_ral_color')) {
        $variantContainer = $target.closest('li');
        $customInput = $target
            .find('option[value="' + $target.val() + '"]');
    }
    if ($variantContainer && $variantContainer.data('is_ral_color')) {
        if ($customInput && $customInput.data('is_color') === 'True') {
            this.$el.find('#color_id').removeClass('d-none')
        }
        else{
            this.$el.find('#color_id').addClass('d-none')
            this.$el.find('#colorcode_show').hide()
        }
    }
    this._super.apply(this, arguments);
}

publicWidget.registry.WebsiteSale.include({
    /**
     * Adds the stock checking to the regular _onChangeCombination method
     * @override
     */
    handleCustomValues: function () {
        this._super.apply(this, arguments);
        VariantMixin.handleCustomValuesRender.apply(this, arguments);
    }
});

export default VariantMixin;

// odoo.define("website_shop_customization.add_colour_selection", function (require) {
//     "use strict";
// var publicWidget = require('web.public.widget');
// var VariantMixin = require('sale.VariantMixin');


// VariantMixin.handleCustomValuesRender = function ($target) {
//         var $variantContainer;
//         var $customInput = false;
//         if ($target.is('select') && $target.data('is_ral_color')) {
//             $variantContainer = $target.closest('li');
//             $customInput = $target
//                 .find('option[value="' + $target.val() + '"]');
//         }
//         if ($variantContainer && $variantContainer.data('is_ral_color')) {
//             if ($customInput && $customInput.data('is_color') === 'True') {
//                 this.$el.find('#color_id').removeClass('d-none')
//             }
//             else{
//                 this.$el.find('#color_id').addClass('d-none')
//                 this.$el.find('#colorcode_show').hide()
//             }
//         }
//         this._super.apply(this, arguments);
//     }


// publicWidget.registry.WebsiteSale.include({
//     /**
//      * Adds the RAL Color Options checking to the regular _onChangeCombination method
//      * @override
//      */
//     handleCustomValues: function (){
//         this._super.apply(this, arguments);
//         VariantMixin.handleCustomValuesRender.apply(this, arguments);
//     },
// });

// return VariantMixin;
// });
