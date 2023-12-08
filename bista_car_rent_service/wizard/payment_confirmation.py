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
    total_amount = fields.Float("Amount")
    
    def get_paid(self):
        id = self.env.context.get('id')
        self.env['user.form.register'].search([('id','=',id)]).get_paid()
        self.env['rent.history'].search([('source_doc.id','=',id)]).get_payment()
        print(id)

    