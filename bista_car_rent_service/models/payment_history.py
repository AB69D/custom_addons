from odoo import fields,_,api,models

class PaymentHistory(models.Model):
    _name = 'payment.history'
    _description = "payment history table"
    
    source_doc = fields.Many2one('user.form.register',string="Source Doc")
    paid = fields.Boolean("Paid")
    expected_payment = fields.Char("Expected Payment")
    due = fields.Char("Due Amount")