from odoo import fields,_,api,models
from odoo.exceptions import ValidationError

class DownPayment(models.TransientModel):
    _name = 'down.payment'
    _description = "downpayment"
    
    def default_sourch(self):
        return self.env['user.form.register'].search([('id','=',self.env.context.get('id'))]).id
        
    sourch_doc = fields.Many2one('user.form.register',string="Sourch ",default=default_sourch)
    down_payment = fields.Boolean("Down Payment",default=True,readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    due_amount = fields.Monetary("Amount",currency_field='currency_id',readonly=True)
    
    def get_paid(self):
        customer_invoice = self.env['customer.invoice'].browse(self.env.context.get('id'))

        for line in customer_invoice.amount_line_ids:
            move_data = {
                'payment_type': "Down Payment",
                'qty': line.qty,
                'customer_id': line.customer_id.id,
                'total_rent': line.total_rent,
                'down_payment': self.due_amount,
            }
            self.env['amount.line'].create(move_data)

        # Update the state of the customer invoice to 'paid'
        customer_invoice.set_state_paid()

        # Close the wizard
        return {'type': 'ir.actions.act_window_close'}

    