from odoo import models, fields

class RealEstateOffer(models.Model):
    _name = "real.estate.offer"
    _description = "Real Estate Offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        string='Status',
        selection=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')],
        default='pending',
        required=True,
        copy = False
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True
    )
    property_id = fields.Many2one(
        comodel_name='real.estate',
        string='Property',
        required=True
    )