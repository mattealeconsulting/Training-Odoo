from odoo import fields, models

class PropertyTag(models.Model):
    _name = "real.estate.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char()
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique')
    ]
    
