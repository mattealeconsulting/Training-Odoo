from odoo import fields, models

class PropertyType(models.Model):
    _name = "real.estate.type"
    _description = "Property Type"

    name = fields.Char(string="Name", required=True)
    description = fields.Text()