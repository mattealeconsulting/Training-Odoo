from odoo import fields, models

class PropertyTag(models.Model):
    _name = "real.estate.tag"
    _description = "Property Tag"

    name = fields.Char()
    
