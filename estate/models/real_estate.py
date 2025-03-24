from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class RealEstate(models.Model):
    _name = "real.estate"
    _description = "Property Listing"

    name = fields.Char(default="House")
    description = fields.Text()
    postcode = fields.Char()
    date_available = fields.Date(copy=False, default=lambda self: datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
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
        copy=False,
        help="State of the real estate")
    
    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        copy=False
    )

    salesperson_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
        copy=False
    )

    property_type_id = fields.Many2one(
        comodel_name='real.estate.type',
        string='Property Type',
        required=True,
        default=lambda self: self.env['real.estate.type'].search([], limit=1).id
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

    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price')) if property.offer_ids else 0

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area = 0
                estate.garden_orientation = False
            else:
                estate.garden_area = 10
                estate.garden_orientation = "north"

    @api.onchange("date_available")
    def _onchange_date_available(self):
        for estate in self:
            if estate.date_available and estate.date_available < fields.Date.today():
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": _("The date is in the past")
                    }
                }
                
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("Canceled properties cannot be sold."))
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offer:
                record.buyer_id = accepted_offer[0].partner_id
                record.selling_price = accepted_offer[0].price
            elif not record.buyer_id:
                raise UserError(_("You cannot mark a property as sold without setting a buyer."))
                
            record.state = 'sold'
        return True
        
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold properties cannot be canceled."))
            record.state = 'canceled'
        return True