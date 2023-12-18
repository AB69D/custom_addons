from odoo import fields,_,api,models
from odoo.exceptions import ValidationError

class PaymentConfirmation(models.TransientModel):
    _name = 'payment.confirmation'
    _description = "payment confirmation"
    
    def default_sourch(self):
        return self.env['user.form.register'].search([('id','=',self.env.context.get('id'))]).id
        
    sourch_doc = fields.Many2one('user.form.register',string="Sourch ",default=default_sourch)
    full_payment = fields.Boolean("Full Payment")
    down_payment = fields.Boolean("Down Payment")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    total_amount = fields.Monetary("Amount",currency_field='currency_id')
    
    def get_paid(self):
        id = self.env.context.get('id')
        self.env['user.form.register'].search([('id','=',id)]).get_paid()
        self.env['rent.history'].search([('source_doc.id','=',id)]).get_payment()
        if self.full_payment:
            str = "Full Payment"
            self.env['user.form.register'].search([('id','=',id)]).create_invoice_amount(str,self.total_amount)
            self.env['customer.invoice'].search([('source_doc','=',self.sourch_doc.id)]).set_state_paid()
        else:
            str = "Down Payment"
            self.env['user.form.register'].search([('id','=',id)]).create_invoice_amount(str,self.total_amount)
        
            
        # if self.down_payment:
        #     due = self.env.context.get('default_total_amount') - self.total_amount
        
        # data = {
        #     'source_doc': self.sourch_doc,
        #     'expected_payment': self.total_amount,
        #     'due': due,
        #     'paid': self.full_payment,
        # }
        # self.env['payment.history'].create(data)

    