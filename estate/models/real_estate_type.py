from odoo import fields, models

class PropertyType(models.Model):
    _name = "real.estate.type"
    _description = "Property Type"

    name = fields.Char(string="Name", required=True)
    description = fields.Text()
    
    # Add the back-reference to properties
    property_ids = fields.One2many(
        comodel_name='real.estate',
        inverse_name='property_type_id',
        string='Properties'
    )