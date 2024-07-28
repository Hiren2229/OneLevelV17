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
VariantMixin._onChangeCombinationSkuCode = function (ev, $parent, combination) {
    console.log("combination.sku_code",combination.sku_code)
    $(this.target).find('.oe_sku').text(combination.sku_code)
    var long_description = $('.variant_long_description').html('')
    jsonrpc("/product/long_description", {
        'product_id': combination.product_id,
    }).then(function(data) {
       long_description.append(data)
    });
    $('.oe_linked').text(combination.document_ids)
    var documents = $('#dynamic_download_id').html('');
    $.each(combination.document_ids, function(x) {
        if (combination.document_ids[x][0] === 'binary')
        {
        var record = '<a class="list-group-item list-group-item-action d-flex align-items-center oe_attachments py-1 px-2" target="_blank" href="/web/content/'+combination.document_ids[x][1]+'?&amp;download=true">\
            <div class="oe_attachment_embedded o_image o_image_small mr-2 mr-lg-3" title="'+combination.document_ids[x][2]+'" data-mimetype="'+combination.document_ids[x][5]+'"></div>\
            <div class="oe_attachment_name text-truncate">'+combination.document_ids[x][2]
            if (combination.document_ids[x][4]){
             record = record+'('+ combination.document_ids[x][4] +')'
            }
            record = record + '</div></a>'
            documents.append($(record));
        }
        if (combination.document_ids[x][0] === 'url')
        {
        var record = '<a class="list-group-item list-group-item-action d-flex align-items-center oe_attachments py-1 px-2" target="_blank" href="'+combination.document_ids[x][6]+'">\
            <div class="oe_attachment_embedded o_image o_image_small mr-2 mr-lg-3" title="'+combination.document_ids[x][2]+'" data-mimetype="'+combination.document_ids[x][5]+'"></div>\
            <div class="oe_attachment_name text-truncate">'+combination.document_ids[x][2]
            if (combination.document_ids[x][4]){
             record = record+'('+ combination.document_ids[x][4] +')'
            }
            record = record + '</div></a>'
            documents.append($(record));
        }
    });
};

publicWidget.registry.WebsiteSale.include({
    /**
     * Adds the stock checking to the regular _onChangeCombination method
     * @override
     */
    _onChangeCombination: function () {
        this._super.apply(this, arguments);
        VariantMixin._onChangeCombinationSkuCode.apply(this, arguments);
    }
});
// odoo.define('downloads_on_website.skucode', function (require) {
// 'use strict';

// require('website_sale.website_sale');

// const publicWidget = require('web.public.widget');
// const {_t} = require('web.core');

// publicWidget.registry.WebsiteSale.include({
//     _onChangeCombination: function (ev, $parent, combination) {
//         this._super.apply(this, arguments);
//         $(this.target).find('.oe_sku').text(combination.sku_code)

//         var ajax = require('web.ajax');
//         var long_description = $('.variant_long_description').html('')
//         ajax.jsonRpc("/product/long_description", 'call', {
//             'product_id': combination.product_id,
//         }).then(function(data) {
//            long_description.append(data)
//         });
//         $('.oe_linked').text(combination.document_ids)
//         var documents = $('#dynamic_download_id').html('');
//         _.each(combination.document_ids, function(x) {
//             if (x[0] === 'binary')
//             {
//             var record = '<a class="list-group-item list-group-item-action d-flex align-items-center oe_attachments py-1 px-2" target="_blank" href="/web/content/'+x[1]+'?&amp;download=true">\
//                 <div class="oe_attachment_embedded o_image o_image_small mr-2 mr-lg-3" title="'+x[2]+'" data-mimetype="'+x[5]+'"></div>\
//                 <div class="oe_attachment_name text-truncate">'+x[2]
//                 if (x[4]){
//                  record = record+'('+ x[4] +')'
//                 }
//                 record = record + '</div></a>'
//                 documents.append($(record));
//             }
//             if (x[0] === 'url')
//             {
//             var record = '<a class="list-group-item list-group-item-action d-flex align-items-center oe_attachments py-1 px-2" target="_blank" href="'+x[6]+'">\
//                 <div class="oe_attachment_embedded o_image o_image_small mr-2 mr-lg-3" title="'+x[2]+'" data-mimetype="'+x[5]+'"></div>\
//                 <div class="oe_attachment_name text-truncate">'+x[2]
//                 if (x[4]){
//                  record = record+'('+ x[4] +')'
//                 }
//                 record = record + '</div></a>'
//                 documents.append($(record));
//             }
//             });
//     },
// });

// });
