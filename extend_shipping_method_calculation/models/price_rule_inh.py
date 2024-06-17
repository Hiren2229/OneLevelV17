# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api, tools, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


class PriceRuleInherit(models.Model):
    _inherit = 'delivery.price.rule'

    variable = fields.Selection(selection_add=[('length', 'Length')], ondelete={'length': 'cascade'})
    variable_factor = fields.Selection(selection_add=[('length', 'Length')], ondelete={'length': 'cascade'})
    x_aa_ol_variable = fields.Selection([
        ('weight', 'Weight'),
        ('volume', 'Volume'),
        ('wv', 'Weight * Volume'),
        ('price', 'Price'),
        ('quantity', 'Quantity'),
        ('length', 'Length')
    ])
    x_aa_ol_operator = fields.Selection([
        ('==', '='),
        ('<=', '<='),
        ('<', '<'),
        ('>=', '>='),
        ('>', '>')], default='<=')
    x_aa_ol_max_value = fields.Float('Maximum Value')


    @api.depends('x_aa_ol_variable', 'x_aa_ol_operator', 'x_aa_ol_max_value', 'list_base_price', 'list_price',
                 'variable_factor','variable', 'operator', 'max_value',)
    def _compute_name(self):
        for rule in self:
            if rule.variable and rule.x_aa_ol_variable:
                name = 'if %s %s %.02f and %s %s %.02f then' % (rule.variable, rule.operator, rule.max_value, rule.x_aa_ol_variable, rule.x_aa_ol_operator, rule.x_aa_ol_max_value)
            if rule.variable and not rule.x_aa_ol_variable:
                name = 'if %s %s %.02f then' % (rule.variable, rule.operator, rule.max_value)
            if rule.list_base_price and not rule.list_price:
                name = '%s fixed price %.02f' % (name, rule.list_base_price)
            elif rule.list_price and not rule.list_base_price:
                name = '%s %.02f times %s' % (name, rule.list_price, rule.variable_factor)
            else:
                name = '%s fixed price %.02f plus %.02f times %s' % (
                    name, rule.list_base_price, rule.list_price, rule.variable_factor)
            rule.name = name


class ProviderGridInherit(models.Model):
    _inherit = 'delivery.carrier'

    def _get_price_available(self, order):
        self.ensure_one()
        self = self.sudo()
        order = order.sudo()
        total = weight = volume = quantity = length = 0
        total_delivery = 0.0
        for line in order.order_line:
            if line.state == 'cancel':
                continue
            if line.is_delivery:
                total_delivery += line.price_total
            if not line.product_id or line.is_delivery:
                continue
            if line.product_id.type == "service":
                continue
            qty = line.product_uom._compute_quantity(line.product_uom_qty, line.product_id.uom_id)
            weight += (line.product_id.gross_weight or 0.0) * qty
            volume += (line.product_id.volume or 0.0) * qty
            if line.product_id.x_aa_ol_transport_length and line.product_id.x_aa_ol_transport_length > length:
                length = line.product_id.x_aa_ol_transport_length
            quantity += qty
        total = (order.amount_total or 0.0) - total_delivery

        total = self._compute_currency(order, total, 'pricelist_to_company')
        # weight is either,
        # 1- weight chosen by user in choose.delivery.carrier wizard passed by context
        # 2- saved weight to use on sale order
        # 3- total order line weight as fallback
        weight = self.env.context.get('order_weight') or order.shipping_weight or weight
        return self._get_price_from_picking(total, weight, volume, quantity, length)

    def _get_price_dict(self, total, weight, volume, quantity, length=False):
        res = super(ProviderGridInherit, self)._get_price_dict(total, weight, volume, quantity)
        res['length'] = length
        return res

    def _get_price_from_picking(self, total, weight, volume, quantity, length):
        price = 0.0
        criteria_found = False
        price_dict = self._get_price_dict(total, weight, volume, quantity, length)
        if self.free_over and total >= self.amount:
            return 0
        for line in self.price_rule_ids:
            test = safe_eval(line.variable + line.operator + str(line.max_value), price_dict)
            test1 = safe_eval(line.x_aa_ol_variable + line.x_aa_ol_operator + str(line.x_aa_ol_max_value), price_dict)
            if test and test1:
                price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                criteria_found = True
                break
        if not criteria_found:
            raise UserError(_("Not available for current order"))
        return price

