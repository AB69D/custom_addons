from datetime import timedelta
import re
from odoo import _,api,fields,models
from odoo.exceptions import UserError, ValidationError

class ProductForrent(models.Model):
    _name = "product.for.rent"
    _description = "product for rent"
    
    product_id = fields.Many2one('car.product', string='Product')
    rent_package = fields.Many2one('rent.package',string="Package",domain=[('active','=',True)])
    avilable_qty = fields.Integer(related='product_id.avilable_quantity')
    qty = fields.Integer(string="Quantity")
    rent_id = fields.Many2one('user.form.register', string="rent")
    done_qty = fields.Integer(string="Done", default=0, readonly=True)
    expected_delivery_qty = fields.Integer(string="Expected Delivery", compute='_compute_expected_delivery',
                                         default=0)
    currency_id = fields.Many2one(related='rent_package.currency_id', string='Currency', required=True,invisible=True)
    rent_amount = fields.Monetary(string='Rent', currency_field='currency_id',compute="_compute_rent_amount")
    
    @api.onchange('qty')
    def available(self):
            if self.qty > self.avilable_qty:
                raise ValidationError (" Product quentity is not avilable")
    
    @api.depends('rent_package','qty','rent_id.rent_day')
    def _compute_rent_amount(self):
        for rec in self:
            rec.rent_amount = rec.rent_package.rent_amount * rec.qty * rec.rent_id.rent_day

        
    @api.depends('qty', 'done_qty')
    def _compute_expected_delivery(self):
        for rec in self:
            rec.expected_delivery_qty = rec.qty - rec.done_qty
            
    @api.onchange('done_qty')
    def update_can_return(self):
        if self.done_qty == 0:
            self.rent_id.can_return = False
            
    # def count_done(self,done_qty,id):
    #     self.done_qty = done_qty
    #     print(done_qty,id)


class UserForm(models.Model):
    _name = 'user.form.register'
    _description = "User registration form for executive"
    _inherit = ['product.for.rent']
    _rec_name = 'ref'
    _order = 'id desc'


    ref = fields.Char(string="Reference ",readonly=True)
    rent_for = fields.Many2one('hr.employee', string="Rent for",required=True)
    rent_purpose = fields.Char(string="Purpose Note")
    phone = fields.Char("Phone",required=True)
    email = fields.Char("Email",required=True)
    rent_date = fields.Date(string="Date of rent", default=fields.Date.context_today)
    return_date = fields.Date(string="Date of return", compute="_compute_day_of_rant")
    rent_day = fields.Integer(string="Rent Duration",default=1)
    product_details_lines = fields.One2many('product.for.rent', 'rent_id', string="Car Details")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validation', 'Pending for delivery'),
        ('deliveried','Deliveried'),
        ('cancel', 'Cancel'),
        ('return', 'Returned'),

    ], string='Status', default='draft', readonly=True, copy=False, tracking=True)
    nid_number =  fields.Char("Nid Number")
    nid =  fields.Binary("NID")
    responsible_person_internal = fields.Many2one('hr.employee', string="Responsible person")
    driving_licence = fields.Char("Driving Lience")
    transfer_delivery_count = fields.Integer(compute='_compute_transfer_delivery_count',
                                             string='Transfer Delivery Count', store=False)
    can_return = fields.Boolean("Can Return",default=False)
    # 
    terms_and_conditions = fields.Text(string="Terms and Conditions Agreement", translate=True,
                                                help="Specify the terms and conditions of the rental agreement",)
    # 
    invoice_count = fields.Integer(compute='_compute_invoice_count',
                                             string='Invoice Count', store=False)
    total_rent = fields.Monetary(string='Rent', currency_field='currency_id',compute="_compute_total_rent")
    
    total_done_qty = fields.Integer("Done",compute="_compute_done_quantity")
    
    due_amount =  fields.Monetary(string='Due Amount', currency_field='currency_id',compute="_compute_due_amount")
    
    def charge_state_deliver(self):
        self.state = "deliveried"
    
    def _compute_due_amount(self):
        for record in self:
            invoices = self.env['customer.invoice'].search([('source_doc', '=', record.ref)])
            record.due_amount = sum(invoices.mapped('due_amount'))
            
    def _compute_done_quantity(self):
        for rec in self.product_details_lines:
            self.total_done_qty += rec.done_qty
    
    def _compute_total_rent(self):
        for rec in self.product_details_lines:
            self.total_rent += rec.rent_amount
    
    def action_view_customer_invoice(self):
        histories = self.env['customer.invoice'].search([('source_doc', '=', self.ref)])
        action = self.env.ref('bista_car_rent_service.action_customer_invoice').read()[0]
        action['domain'] = [('id', 'in', histories.ids)]

        return action
    
    # @api.onchange('phone')
    # def onchange_phone(self,):
    #     for item in self:
    #         pattern = re.compile(r"^\+8801[13456789]\d{8}$")
    #         if pattern.match(item.phone) == None:
    #             raise UserError("Phone Number is not valid")
            
    # @api.onchange('email')
    # def on_change_email(self,):
    #     for item in self:
    #         pattern = re.compile(r"^[a-zA-Z0-9_-]+@[a-z]+\.[a-z]{1,3}$")
    #         if pattern.match(item.email) == None:
    #             raise UserError("Email is not valid")
    
    
    def count_done(self,done_qty,id):
        for rec in self.product_details_lines:
            if id == rec.product_id:
                rec.done_qty = done_qty
            print(rec.done_qty,id)
    
    def _compute_invoice_count(self):
        for record in self:
            invoice_count = self.env['customer.invoice'].search_count([
                ('source_doc', '=', self.ref),
            ])
            record.invoice_count = invoice_count
        
    def _compute_transfer_delivery_count(self):
        for record in self:
            transfer_count = self.env['rent.history'].search_count([
                ('source_doc', '=', self.ref),
            ])
            record.transfer_delivery_count = transfer_count
    
    def action_view_history(self):
        histories = self.env['rent.history'].search([('source_doc', '=', self.ref)])
        action = self.env.ref('bista_car_rent_service.action_rent_history').read()[0]
        action['domain'] = [('id', 'in', histories.ids)]

        return action
    
    @api.model
    def create(self, vls):
        vls['ref'] = self.env['ir.sequence'].next_by_code('user.form.register')
        res = super(UserForm, self).create(vls)
        return res
    
    @api.depends('rent_day')
    def _compute_day_of_rant(self):
        self.return_date = self.rent_date + timedelta(days=self.rent_day)
    
    def get_paid(self):
        self.state = "return"
        for line in self.product_details_lines:
            self.env['car.product'].search([('id','=',line.product_id.id)]).reserve_increase(line.done_qty)
    
    def submit_for_validation(self):
        self.state = "validation"
        self.create_rent_history()
    
    def submit_for_cancel(self):
        self.state = "cancel"
    
    # if self.env.user.has_group('bista_car_rent_service.access_category_car_rent_admin'):
        
    def submit_for_return(self):
        return{
            'name':"process for payment",
            'res_model':'payment.confirmation',
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'target':'new',
            'context':{
                'default_total_amount':self.total_rent,
                'id':self.id,
            }
        }
    
    def submit_for_create_delivery(self):
        self.create_rent_history()
        
    @api.model  
    def create_rent_history(self):
    
        for line in self.product_details_lines:
            if line.expected_delivery_qty == 0:
                raise UserError(_("You do not have enough product quantity for create a delivery."))
            else:
                car_data = {
                    'source_doc': self.id,
                    'res_user': self.rent_for.id,
                    'return_date': self.return_date,
                    'rent_date': self.rent_date
                }
                rent_history = self.env['rent.history'].create(car_data)
                product_ids_to_transfer = [line.product_id.id for line in self.product_details_lines]

                for line in self.product_details_lines: 
                    move_data = {
                        'product_id': line.product_id.id,
                        'qty': line.expected_delivery_qty,
                        'rent_id': rent_history.id,
                    }
                    move = self.env['line.history.rent'].create(move_data)

                return rent_history
            
    
    def create_invoice_amount(self,val,amount):
        self.create_invoice(val,amount)      
        
    @api.model  
    def create_invoice(self,val,amount):
        user_data = {
            'source_doc': self.id,
            'customer': self.rent_for.id,
            'invoice_date': self.rent_date,
            'due_date': self.return_date,
            'total_rent':self.total_rent
        }
        invoice = self.env['customer.invoice'].create(user_data)

        move_data = {
            'payment_type': val,
            'qty': self.total_done_qty,
            'customer_id': invoice.id,
            'total_rent': self.total_rent,
            'down_payment': amount,
        }
        move = self.env['amount.line'].create(move_data)

        return invoice