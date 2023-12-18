from odoo import fields,api,models,_ 

class AmountLine(models.Model):
    _name = 'amount.line'
    _description = "Amount Line"
    
    
    payment_type = fields.Char("Payment Type")
    qty = fields.Char("Quantity")
    total_rent = fields.Monetary("Total Rent",currency_field='currency_id')
    customer_id = fields.Many2one('customer.invoice')
    down_payment = fields.Monetary("Paid Amount",currency_field='currency_id', default=0)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    

    
    
class CustomerInvoice(models.Model):
    _name ='customer.invoice'
    _description = "Customer invoice model"
    _rec_name = 'source_doc'
    _order = 'id desc'
    
    
    source_doc = fields.Many2one('user.form.register',string="Source")
    customer = fields.Many2one('hr.employee', string="Customer")
    invoice_date = fields.Date("Invoice Date")
    due_date = fields.Date("Due Date")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    total_rent = fields.Monetary("Total Rent",currency_field='currency_id')
    amount_line_ids = fields.One2many('amount.line','customer_id')
    state = fields.Selection([
        ('validation', 'Down Payment'),
        ('paid', 'paid'),
    ], string='Status', default='validation', readonly=True, copy=False, tracking=True)
    due_amount = fields.Monetary("Due Amount",currency_field='currency_id',compute="_compute_due_amount")
    
    def set_state_paid(self):
        self.state = "paid"
        
    
    @api.depends('total_rent', 'amount_line_ids.down_payment')
    def _compute_due_amount(self):
        for rec in self.amount_line_ids:
            total_ddue = 0.00  # Initialize total_ddue before the loop
            if rec.down_payment:
                total_ddue += rec.down_payment
        self.due_amount = self.total_rent - total_ddue


    def due_payment(self):
        return{
            'name':"process for payment",
            'res_model':'down.payment',
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'target':'new',
            'context':{
                'default_due_amount':self.due_amount,
                'id':self.id,
            }
        }
    
        
