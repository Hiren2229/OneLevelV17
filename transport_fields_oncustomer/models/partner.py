# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_aa_ol_truck = fields.Boolean('Truck')
    x_aa_ol_train = fields.Boolean('Train')
    x_aa_ol_ship = fields.Boolean('Ship')
    x_aa_ol_plane = fields.Boolean('Plane')
    x_aa_ol_express = fields.Boolean('Express')
    x_aa_ol_truck_days = fields.Integer('Shipment Days Truck', help="Shipment Days Truck")
    x_aa_ol_train_days = fields.Integer('Shipment Days Train', help="Shipment Days Train")
    x_aa_ol_ship_days = fields.Integer('Shipment Days Ship', help="Shipment Days Ship")
    x_aa_ol_plane_days = fields.Integer('Shipment Days Plane', help="Shipment Days Plane")
    x_aa_ol_express_days = fields.Integer('Shipment Days Express', help="Shipment Days Express")
    x_aa_ol_default_transport_type = fields.Many2one('transport.type', string="Default Transport Type", domain="[('id', '=', False)]")


    @api.onchange('x_aa_ol_truck', 'x_aa_ol_train', 'x_aa_ol_ship', 'x_aa_ol_plane', 'x_aa_ol_express')
    def _onchange_transport_fields(self):
        transport_ids = []
        if self.x_aa_ol_truck:
            find_truck_id = self.env.ref('transport_fields_oncustomer.transport_one').id
            transport_ids.append(find_truck_id)
        if self.x_aa_ol_train:
            find_transport_id = self.env.ref('transport_fields_oncustomer.transport_two').id
            transport_ids.append(find_transport_id)
        if self.x_aa_ol_ship:
            find_ship_id = self.env.ref('transport_fields_oncustomer.transport_three').id
            transport_ids.append(find_ship_id)
        if self.x_aa_ol_plane:
            find_plane_id = self.env.ref('transport_fields_oncustomer.transport_four').id
            transport_ids.append(find_plane_id)
        if self.x_aa_ol_express:
            find_express_id = self.env.ref('transport_fields_oncustomer.transport_five').id
            transport_ids.append(find_express_id)
        return {"domain": {'x_aa_ol_default_transport_type' : [('id', 'in', transport_ids)]}}

class TransportType(models.Model):
    _name = 'transport.type'
    _description = 'Transport Type'

    name = fields.Char()
