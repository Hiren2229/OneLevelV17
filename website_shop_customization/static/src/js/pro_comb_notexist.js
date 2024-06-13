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
    _getCombinationInfo: function (ev) {
        var self = this;

        if ($(ev.target).hasClass('variant_custom_value')) {
            return Promise.resolve();
        }

        var $parent = $(ev.target).closest('.js_product');
        var qty = $parent.find('input[name="add_qty"]').val();
        var combination = this.getSelectedVariantValues($parent);
        var parentCombination = $parent.find('ul[data-attribute_exclusions]').data('attribute_exclusions').parent_combination;
        var productTemplateId = parseInt($parent.find('.product_template_id').val());
        self._checkExclusions($parent, combination);

        return jsonrpc(this._getUri('/website_sale/get_combination_info'), {
            'product_template_id': productTemplateId,
            'product_id': this._getProductId($parent),
            'combination': combination,
            'add_qty': parseInt(qty),
            'pricelist_id': this.pricelistId || false,
            'parent_combination': parentCombination,
        }).then(function (combinationData) {
            console.log("combinationData",combinationData)
            if (combinationData.remove_val && combinationData.remove_val.length > 0) {
                $.each($parent[0].querySelectorAll('.js_variant_change'), function (val) {
                    if (combinationData.remove_val.includes(parseInt($parent[0].querySelectorAll('.js_variant_change')[val].getAttribute('value')))) {
                            $parent[0].querySelectorAll('.js_variant_change')[val].parentElement.parentElement.style.display = 'none';
                      }
                });
                $.each($parent[0].querySelectorAll('option'), function (val) {
                    if (combinationData.remove_val.includes(parseInt($parent[0].querySelectorAll('option')[val].getAttribute('value')))) {
                            $parent[0].querySelectorAll('option')[val].style.display = 'none';
                      }
                });
            } else {
                $.each($parent[0].querySelectorAll('.js_attribute_value'), function (val) {
                    console.log("js_attribute_value val",$parent[0].querySelectorAll('.js_attribute_value')[val])
                    $parent[0].querySelectorAll('.js_attribute_value')[val].style.display = null;
                });
                $.each($parent[0].querySelectorAll('option'), function (val) {
                    console.log("option val",$parent[0].querySelectorAll('option')[val])
                    $parent[0].querySelectorAll('option')[val].style.display = null;
                });
                $.each($parent[0].querySelectorAll('.js_variant_change'), function (val) {
                    console.log("js_variant_change val",val)
                    $parent[0].querySelectorAll('.js_variant_change')[val].parentElement.parentElement.style.display = null;
                });
            }
            $.each($parent[0].querySelectorAll('.js_variant_change'), function (val) {
                var uomName = document.getElementById("uom_name")
                uomName.innerHTML = combinationData.uom_name;
                var uomPrice = document.getElementById("uom_unit_price")
                var webLanguage = combinationData.web_language || 'en-US'
                webLanguage = webLanguage.replace('_', '-');
                var formattedPrice = combinationData.per_product_price;
                formattedPrice = formattedPrice.toLocaleString(webLanguage, {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                });
                uomPrice.innerHTML = formattedPrice + '  ' + combinationData.website_currency;
            });
            self._onChangeCombination(ev, $parent, combinationData);
        });
    },
});
// odoo.define("website_shop_customization.pro_comb_notexist", function (require) {
//     "use strict";
// var publicWidget = require('web.public.widget');
// var ajax = require('web.ajax');


// publicWidget.registry.WebsiteSale.include({
//     /**
//      * to check product combination that exist or not if not hide the varinats attributes value
//      * @override
//      */
//     _getCombinationInfo: function (ev) {
//         var self = this;

//         if ($(ev.target).hasClass('variant_custom_value')) {
//             return Promise.resolve();
//         }

//         var $parent = $(ev.target).closest('.js_product');
//         var qty = $parent.find('input[name="add_qty"]').val();
//         var combination = this.getSelectedVariantValues($parent);
//         var parentCombination = $parent.find('ul[data-attribute_exclusions]').data('attribute_exclusions').parent_combination;
//         var productTemplateId = parseInt($parent.find('.product_template_id').val());
//         self._checkExclusions($parent, combination);

//         return ajax.jsonRpc(this._getUri('/sale/get_combination_info'), 'call', {
//             'product_template_id': productTemplateId,
//             'product_id': this._getProductId($parent),
//             'combination': combination,
//             'add_qty': parseInt(qty),
//             'pricelist_id': this.pricelistId || false,
//             'parent_combination': parentCombination,
//         }).then(function (combinationData) {
//             if (combinationData.remove_val && combinationData.remove_val.length > 0) {
//                 _.each($parent[0].querySelectorAll('.js_variant_change'), function (val) {
//                     if (combinationData.remove_val.includes(parseInt(val.getAttribute('value')))) {
//                             val.parentElement.parentElement.style.display = 'none';
//                       }
//                 });
//                 _.each($parent[0].querySelectorAll('option'), function (val) {
//                     if (combinationData.remove_val.includes(parseInt(val.getAttribute('value')))) {
//                             val.style.display = 'none';
//                       }
//                 });
//             } else {
//                 _.each($parent[0].querySelectorAll('.js_attribute_value'), function (val) {
//                             val.style.display = null;
//                 });
//                 _.each($parent[0].querySelectorAll('option'), function (val) {
//                             val.style.display = null;
//                 });
//                 _.each($parent[0].querySelectorAll('.js_variant_change'), function (val) {
//                             val.parentElement.parentElement.style.display = null;
//                 });
//             }
//             _.each($parent[0].querySelectorAll('.js_variant_change'), function (val) {
//                         var uomName = document.getElementById("uom_name")
//                         uomName.innerHTML = combinationData.uom_name;
//                         var uomPrice = document.getElementById("uom_unit_price")
//                         var webLanguage = combinationData.web_language || 'en-US'
//                         webLanguage = webLanguage.replace('_', '-');
//                         var formattedPrice = combinationData.per_product_price;
//                         formattedPrice = formattedPrice.toLocaleString(webLanguage, {
//                             minimumFractionDigits: 2,
//                             maximumFractionDigits: 2,
//                         });
//                         uomPrice.innerHTML = formattedPrice + '  ' + combinationData.website_currency;
//                 });
//             self._onChangeCombination(ev, $parent, combinationData);
//         });
//     },
// });

// });
