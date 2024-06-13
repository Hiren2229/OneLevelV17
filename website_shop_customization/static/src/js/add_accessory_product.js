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
VariantMixin._onChangeCombinationAccessory = function (ev, $parent, combination) {
    $(this.target).find('.oe_sku').text(combination.sku_code)
    var custom_accessory = $('.custom_accessory_product')

    var div_record = '<div class="owl-stage-outer">' +
                     '<div class="owl-stage" style="transform: translate3d(0px, 0px, 0px); transition: all 0s ease 0s; width: 249px; padding-left: 6px; padding-right: 6px;">' +
                     '</div>' +
                     '</div>';

    var div_disable_record = '<div class="owl-nav disabled">'
    var div_disable_record = div_disable_record + '<button type="button" role="presentation" class="owl-prev">'
    var div_disable_record = div_disable_record + '<span aria-label="Previous">' + '‹' + '</span>'
    var div_disable_record = div_disable_record + '</button>'
    var div_disable_record = div_disable_record + '<button type="button" role="presentation" class="owl-next">'
    var div_disable_record = div_disable_record + '<span aria-label="Next">' + '›' + '</span>'
    var div_disable_record = div_disable_record + '</button>'
    var div_disable_record = div_disable_record + '</div>'

    var accessory_product = custom_accessory.find('.owl-stage').html('');
    if (accessory_product.length === 0){
        var tp_cards = custom_accessory.find('.tp-suggested-products-cards').html('');
        tp_cards.append(div_record, div_disable_record);
        accessory_product = tp_cards.find('.owl-stage').html('');
    }
    var accessory_div = custom_accessory.find('.position-relative');
        jsonrpc("/product/accessory_product", {
            'product_id': combination.product_id,
        }).then(function(data) {
            if (!data || (data && data.length === 0)) {
                accessory_div[0].style='display: none;';
            }
            else {
                accessory_div[0].style='display: box;';
            }
            if (data){
                for (var rec of data){
                    var record = '<div class="owl-item active" style="width: 177.5px; margin-right: 15px;"><div class="card w-100">'
                    var record = record + '<a class="card-img-top" href=" '+rec.URL+' "><img loading="lazy" src="/web/image/product.template/'+rec.tempID+'/image_512" class="img img-fluid" alt=" '+rec.Name+' "></a>'
                    if (rec.label){
                        var record = record + '<span class="tp-product-label-style-1 tp-product-label-color-red">'
                        var record = record + '<span>'+rec.label+'</span>'
                        var record = record + '</span>'
                    }
                    var record = record + '<div class="card-body p-2">'
                    var record = record + '<div class="card-text"> <a class="text-decoration-none" href="/shop/category/'+rec.categID+'"> <small class="dr_category_lable"> '+rec.categname+' </small></a>'
                    var record = record + '<h6 class="text-truncate my-1" title="'+rec.Name+'"> <a class="tp-link-dark" href="'+rec.URL+'"> <span> '+rec.Name+' </span></a></h6>'
                    var record = record + '<div></div>'
                    var record = record + '</div>'
                    var record = record + '</div>'
                    var record = record + '</div>'
                    var record = record + '</div>'
                    accessory_product.append($(record));
                }
            }
         const $owlSlider = $('.owl-carousel');
         const responsiveParams = { 0: { items: 2 }, 576: { items: 2 }, 768: { items: 3 }, 992: { items: 4 }, 1200: { items: 5 } };
//        if (!this.$target.data('two-block')) {
            // _.extend(responsiveParams, { 768: { items: 3 }, 992: { items: 4 }, 1200: { items: 5 } });
//        }
        $owlSlider.removeClass('d-none');
        $owlSlider.owlCarousel({
            dots: false,
            margin: 15,
            stagePadding: 6,
            autoplay: true,
            autoplayTimeout: 3000,
            autoplayHoverPause: true,
            rewind: true,
            rtl: localization.direction === 'rtl',
            responsive: responsiveParams,
        });
        $('.tp-prev').click(function () {
            $owlSlider.trigger('prev.owl.carousel');
        });
        $('.tp-next').click(function () {
            $owlSlider.trigger('next.owl.carousel');
        });

        });
};

publicWidget.registry.WebsiteSale.include({
    /**
     * Adds the stock checking to the regular _onChangeCombination method
     * @override
     */
    _onChangeCombination: function () {
        this._super.apply(this, arguments);
        VariantMixin._onChangeCombinationAccessory.apply(this, arguments);
    }
});

export default VariantMixin;

// odoo.define('website_shop_customization.add_accessory_product', function (require) {
// 'use strict';

// require('website_sale.website_sale');

// const publicWidget = require('web.public.widget');
// const {_t} = require('web.core');


// publicWidget.registry.WebsiteSale.include({ 
//     _onChangeCombination: function (ev, $parent, combination) {
//         this._super.apply(this, arguments);
//         $(this.target).find('.oe_sku').text(combination.sku_code)
//         var custom_accessory = $('.custom_accessory_product')

//         var div_record = '<div class="owl-stage-outer">' +
//                          '<div class="owl-stage" style="transform: translate3d(0px, 0px, 0px); transition: all 0s ease 0s; width: 249px; padding-left: 6px; padding-right: 6px;">' +
//                          '</div>' +
//                          '</div>';

//         var div_disable_record = '<div class="owl-nav disabled">'
//         var div_disable_record = div_disable_record + '<button type="button" role="presentation" class="owl-prev">'
//         var div_disable_record = div_disable_record + '<span aria-label="Previous">' + '‹' + '</span>'
//         var div_disable_record = div_disable_record + '</button>'
//         var div_disable_record = div_disable_record + '<button type="button" role="presentation" class="owl-next">'
//         var div_disable_record = div_disable_record + '<span aria-label="Next">' + '›' + '</span>'
//         var div_disable_record = div_disable_record + '</button>'
//         var div_disable_record = div_disable_record + '</div>'

//         var accessory_product = custom_accessory.find('.owl-stage').html('');
//         if (accessory_product.length === 0){
//             var tp_cards = custom_accessory.find('.tp-suggested-products-cards').html('');
//             tp_cards.append(div_record, div_disable_record);
//             accessory_product = tp_cards.find('.owl-stage').html('');
//         }
//         var accessory_div = custom_accessory.find('.position-relative')
//         var ajax = require('web.ajax');
//         ajax.jsonRpc("v                xc                        ,li", 'call', {
//             'product_id': combination.product_id,
//         }).then(function(data) {
//             if (!data || (data && data.length === 0)) {
//                 accessory_div[0].style='display: none;';
//             }
//             else {
//                 accessory_div[0].style='display: box;';
//             }
//             if (data){
//                 for (var rec of data){
//                     var record = '<div class="owl-item active" style="width: 177.5px; margin-right: 15px;"><div class="card w-100">'
//                     var record = record + '<a class="card-img-top" href=" '+rec.URL+' "><img loading="lazy" src="/web/image/product.template/'+rec.tempID+'/image_512" class="img img-fluid" alt=" '+rec.Name+' "></a>'
//                     if (rec.label){
//                         var record = record + '<span class="tp-product-label-style-1 tp-product-label-color-red">'
//                         var record = record + '<span>'+rec.label+'</span>'
//                         var record = record + '</span>'
//                     }
//                     var record = record + '<div class="card-body p-2">'
//                     var record = record + '<div class="card-text"> <a class="text-decoration-none" href="/shop/category/'+rec.categID+'"> <small class="dr_category_lable"> '+rec.categname+' </small></a>'
//                     var record = record + '<h6 class="text-truncate my-1" title="'+rec.Name+'"> <a class="tp-link-dark" href="'+rec.URL+'"> <span> '+rec.Name+' </span></a></h6>'
//                     var record = record + '<div></div>'
//                     var record = record + '</div>'
//                     var record = record + '</div>'
//                     var record = record + '</div>'
//                     var record = record + '</div>'
//                     accessory_product.append($(record));
//                 }
//             }
//          const $owlSlider = $('.owl-carousel');
//          const responsiveParams = { 0: { items: 2 }, 576: { items: 2 }, 768: { items: 2 }, 992: { items: 2 }, 1200: { items: 3 } };
// //        if (!this.$target.data('two-block')) {
//             _.extend(responsiveParams, { 768: { items: 3 }, 992: { items: 4 }, 1200: { items: 5 } });
// //        }
//         $owlSlider.removeClass('d-none');
//         $owlSlider.owlCarousel({
//             dots: false,
//             margin: 15,
//             stagePadding: 6,
//             autoplay: true,
//             autoplayTimeout: 3000,
//             autoplayHoverPause: true,
//             rewind: true,
//             rtl: _t.database.parameters.direction === 'rtl',
//             responsive: responsiveParams,
//         });
//         $('.tp-prev').click(function () {
//             $owlSlider.trigger('prev.owl.carousel');
//         });
//         $('.tp-next').click(function () {
//             $owlSlider.trigger('next.owl.carousel');
//         });

//         });

// //         debugger;
//     },
// });

// });
