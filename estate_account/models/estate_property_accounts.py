from odoo import api, Command, fields, models, _
from odoo.exceptions import UserError
import logging

class RealEstate(models.Model):
    _inherit = "real.estate"
    
    def action_sold(self):
        result = super().action_sold()
        
        self._create_invoice()
        
        return result
    
    def _create_invoice(self):
        for property in self:
            if property.selling_price <= 0:
                continue
                
            if not property.buyer_id:
                continue
                
            try:
                journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
                
                if not journal:
                    raise UserError(_("No sales journal found. Please configure one."))
                invoice_vals = {
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice', 
                    'journal_id': journal.id,
                    'invoice_origin': property.name, 
                    'invoice_line_ids': [
                        Command.create({
                            'name': f'Commission for {property.name}',
                            'quantity': 1.0,
                            'price_unit': property.selling_price * 0.06,
                    }),
                        Command.create({
                            'name': 'Administrative fees',
                            'quantity': 1.0,
                            'price_unit': 100.00,
                    }),
                    ],
                    'narration': f"""
                        Property: {property.name}
                        Expected Price: {property.expected_price}
                        Selling Price: {property.selling_price}
                    """,
                }
                
                invoice = self.env['account.move'].with_context(default_move_type='out_invoice').create(invoice_vals)
                invoice.action_post()
                
            except Exception as e:
                _logger = logging.getLogger(__name__)
                _logger.error(f"Error creating invoice for property {property.name}: {str(e)}")