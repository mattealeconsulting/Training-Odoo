from odoo import fields, models

class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name='real.estate',
        inverse_name='salesperson_id',
        string='Properties',
        domain=[('state', 'not in', ['sold', 'canceled'])]
    )