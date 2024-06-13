from odoo import api, models
from odoo.addons.http_routing.models.ir_http import slugify


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    @api.model
    def _prepare_qcontext(self):
        qcontext = super(IrUiView, self)._prepare_qcontext()
        qcontext['slugify'] = slugify
        return qcontext
