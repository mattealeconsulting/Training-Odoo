from odoo import api, fields, models

class PropertyType(models.Model):
    _name = "real.estate.type"
    _description = "Property Type"
    _order = "sequence, name"

    sequence = fields.Integer(default=10)
    name = fields.Char(string="Name", required=True)
    description = fields.Text()
    
    # Add the back-reference to properties
    property_ids = fields.One2many(
        comodel_name='real.estate',
        inverse_name='property_type_id',
        string='Properties'
    )
    offer_ids = fields.One2many('real.estate.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type must be unique')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

