from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.tools.float_utils import float_is_zero, float_compare


class RealEstate(models.Model):
    _name = "real.estate"
    _description = "Property Listing"
    _order = "id desc"

    name = fields.Char(default="House")
    description = fields.Text()
    postcode = fields.Char()
    date_available = fields.Date(copy=False, default=lambda self: datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, default=0)
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
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
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

    def _default_property_type(self):
        type_ref = self.env.ref('real_estate.default_property_type', raise_if_not_found=False)
        return type_ref.id if type_ref else False

    property_type_id = fields.Many2one(
    comodel_name='real.estate.type',
    string='Property Type',
    required=True,
    default=lambda self: self._default_property_type()
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

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive!'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive!')
    ]
    
    @api.constrains('selling_price', 'expected_price')
    def _check_price_difference(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_digits=2) and 
                float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0):
                raise ValidationError(_("The selling price cannot be lower than 90% of the expected price!"))

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price'), default=0)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = "north"

    @api.onchange("date_available")
    def _onchange_date_available(self):
        if self.date_available and self.date_available < fields.Date.today():
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _("The date is in the past")
                }
            }
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_valid(self):
        for estate in self:
            if estate.state not in ['new', 'canceled']:
                raise UserError(_("You cannot delete a property that is not in 'New' or 'Canceled' state."))
                
    def action_sold(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError(_("Canceled properties cannot be sold."))
            
        accepted_offers = self.offer_ids.filtered(lambda o: o.status == 'accepted')
        if accepted_offers:
            highest_offer = max(accepted_offers, key=lambda o: o.price)
            self.buyer_id = highest_offer.partner_id
        elif not self.buyer_id:
            raise UserError(_("You cannot mark a property as sold without setting a buyer."))
            
        self.state = 'sold'
        return True
        
    def action_cancel(self):
        if self.state == 'sold':
            raise UserError(_("Sold properties cannot be canceled."))
        self.state = 'canceled'
        return True