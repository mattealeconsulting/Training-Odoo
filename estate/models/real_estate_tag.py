from odoo import models, fields

class PropertyTag(models.Model):
    _name = "real.estate.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)
    
