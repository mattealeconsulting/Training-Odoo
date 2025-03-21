from odoo import fields, models
from datetime import datetime, timedelta

class RealEstate(models.Model):
    _name = "real.estate"
    _description = "Test model"

    name = fields.Char(default="House",required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_available = fields.Date(copy=False, default=lambda self: datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('sold', 'Sold'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('canceled', 'Canceled')],
        default='new',
        required = True,
        copy = False,
        help="State of the real estate")

    property_type_id = fields.Many2one(
        comodel_name='real.estate.type',
        string='Property Type',
        required=True
    )
    offer_ids = fields.One2many(
        comodel_name='real.estate.offer',
        inverse_name='property_id',
        string='Offers'
    )

    tag_ids = fields.Many2many(
        comodel_name='real.estate.tag',
        string='Tags'
    )

