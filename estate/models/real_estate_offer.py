from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import timedelta

class RealEstateOffer(models.Model):
    _name = "real.estate.offer"
    _description = "Real Estate Offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        string='Status',
        selection=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')],
        default='pending',
        required=True,
        copy=False
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True
    )
    property_id = fields.Many2one(
        comodel_name='real.estate',
        string='Property',
        required=True,
        ondelete='cascade'
    )
    type_id = fields.Many2one(related="property_id.property_type_id")

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date_ref = offer.create_date or fields.Datetime.now()
            date_ref_date = fields.Date.to_date(date_ref)
            offer.date_deadline = date_ref_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date_ref = offer.create_date or fields.Datetime.now()
            date_ref_date = fields.Date.to_date(date_ref)
            if offer.date_deadline:
                delta = offer.date_deadline - date_ref_date
                offer.validity = delta.days

    def action_accept(self):
        self.ensure_one()
        
        # Check if there's already an accepted offer for this property
        if self.property_id and "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("An offer has already been accepted for this property."))
        
        # Check if property exists
        if not self.property_id:
            raise UserError(_("Cannot accept an offer without a property."))
            
        # Set this offer as accepted
        self.write({
            'status': 'accepted'
        })
        
        # Update the property with buyer and selling price
        self.property_id.write({
            'state': 'offer_accepted',
            'selling_price': self.price,
            'buyer_id': self.partner_id.id,
        })
        
        # Refuse all other offers
        other_offers = self.property_id.offer_ids.filtered(lambda r: r.id != self.id)
        other_offers.write({'status': 'refused'})
        
        return True
        
    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True