odoo.define('language_on_documents.DocumentsInspectors',[], function (require) {
'use strict';

    
    const DocumentsInspector = require('documents.DocumentsInspector');

    DocumentsInspector.include({
        init: function (parent, params) {
            this._super(...arguments);
        },
        _renderFields: function () {
            const options = {mode: 'edit'};
            const proms = [];
            if (this.records.length === 1) {
                proms.push(this._renderField('name', options));
                if (this.records[0].data.type === 'url') {
                    proms.push(this._renderField('url', options));
                }
                proms.push(this._renderField('partner_id', options));
            }
            if (this.records.length > 0) {
                proms.push(this._renderField('owner_id', options));
                proms.push(this._renderField('x_aa_ol_language_id', options));
                //                update 162 step3
                proms.push(this._renderField('x_ad_ol_document_group', options));
                proms.push(this._renderField('x_ad_ol_is_published', options));
                proms.push(this._renderField('x_ad_ol_online_name', options));

                if (this.records[0].data.x_ad_ol_is_certification_document === true){
                proms.push(this._renderField('x_ad_ol_certification_country', options));
                }
//                update 162 step3 end
                proms.push(this._renderField('folder_id', {
                    icon: 'fa fa-folder o_documents_folder_color',
                    mode: 'edit',
                }));
            }
            return Promise.all(proms);
        }
    });
});