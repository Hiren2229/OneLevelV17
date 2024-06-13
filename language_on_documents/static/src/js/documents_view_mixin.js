odoo.define('language_on_documents.viewMixins', [], function (require) {
'use strict';

    var DocumentsViewMixin = require('documents.viewMixin').inspectorFields;
    
    DocumentsViewMixin.push('x_aa_ol_language_id');
        //    update 162 step3
    DocumentsViewMixin.push('x_ad_ol_document_group');
    DocumentsViewMixin.push('x_ad_ol_is_published');
    DocumentsViewMixin.push('x_ad_ol_online_name');

    if (this.records[0].data.x_ad_ol_is_certification_document === true){DocumentsViewMixin.push('x_ad_ol_certification_country');}
//    update 162 step3 end

    return DocumentsViewMixin
});