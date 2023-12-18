from odoo import api,_,fields,models
from odoo.exceptions import UserError, ValidationError

class InheritPartner(models.Model):
    _inherit = 'res.partner'
    _description = "partner model"
    
    credit_limit = fields.Float("Credit Limit" , default= 0.00)
    
    @api.model
    def create(self,vals):
        if vals.get('credit_limit') > 0:
            if self.env.user.has_group('bista_test.acess_customer_credit_allow'):
               record = super(InheritPartner,self).create(vals)
               return record
            else:
                raise UserError('Access Denied to edit credit limit')
                 
        else:
            record = super(InheritPartner,self).create(vals)
            return record
               
            
    def write(self,vals):
        if vals.get('credit_limit'):

            has_group_access = self.env.user.has_group('bista_test.acess_customer_credit_allow')

            if not has_group_access:
                raise UserError('Access Denied to edit credit limit')

        return super(InheritPartner, self).write(vals)

    
class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = "inherit sale order"
    
    def has_power(self):
        if self.amount_total > 1000:
            return True
        # return self.env.user.has_group('bista_test.acess_customer_credit_allow')
    approve = fields.Boolean("Approve" , compute="_compute_has_power")
    now_confirm = fields.Boolean("now confirm",default=False)
    total_due = fields.Char("Total Due", compute="_compute_get_total_due_amount")
    
    @api.depends('partner_id')
    def _compute_get_total_due_amount(self):
        invoices = self.env['account.move'].search([('partner_id', '=', self.partner_id.id), ('payment_state', '=', 'not_paid')])
        total_due_amount = sum(invoice.amount_residual for invoice in invoices)
        print(total_due_amount)
        self.total_due = total_due_amount
        print("------------------------------")
    
    
    @api.depends('amount_total')
    def _compute_has_power(self):
        if self.env.user.has_group('bista_test.acess_customer_credit_allow'):
            self.approve = True
        else:
            self.approve = False
    
    def action_approve(self):
        self.now_confirm = True
    
    
    def action_confirm(self):
        if self.amount_total > 1000 or (self.amount_total+self.total_due) > self.partner_id.credit_limit:
            if self.now_confirm == False:
                raise ValidationError("You need approval")
        for rec in self:
            for roc in rec.order_line:
                if roc.product_uom_qty < roc.product_template_id.qty_available:
                    continue
                else:
                    raise ValidationError("No Enough Product on hand")
        print("action_confirm..........................!")
        return super(InheritSaleOrder,self).action_confirm()