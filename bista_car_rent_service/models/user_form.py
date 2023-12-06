from datetime import timedelta
from odoo import _,api,fields,models
from odoo.exceptions import UserError

class ProductForrent(models.Model):
    _name = "product.for.rent"
    _description = "product for rent"
    
    product_id = fields.Many2one('car.product', string='Product')
    qty = fields.Integer(string="Quantity", default=1)
    rent_id = fields.Many2one('user.form.register', string="rent")
    done_qty = fields.Integer(string="Done", default=0, readonly=True)
    expected_delivery_qty = fields.Integer(string="Expected Delivery", compute='_compute_expected_delivery',
                                         default=0)
    # tax_ids = fields.Many2many('account.tax',string="Tax")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,invisible=True)
    rent_amount = fields.Monetary(string='Rent', currency_field='currency_id', required=True)
    
    @api.onchange('product_id','qty')
    def get_rent_amount(self):
        self.currency_id = self.rent_id.rent_package.currency_id.id
        self.rent_amount = self.rent_id.rent_package.rent_amount * self.qty
        
    @api.depends('qty', 'done_qty')
    def _compute_expected_delivery(self):
        for rec in self:
            rec.expected_delivery_qty = rec.qty - rec.done_qty
            
    @api.onchange('done_qty')
    def update_can_return(self):
        if self.done_qty == 0:
            self.rent_id.can_return = False


class UserForm(models.Model):
    _name = 'user.form.register'
    _description = "User registration form for executive"
    _inherit = ['product.for.rent']
    _rec_name = 'ref'
    _order = 'id desc'


    ref = fields.Char(string="Reference ",readonly=True)
    rent_for = fields.Many2one('hr.employee', string="rent for")
    rent_purpose = fields.Char(string="Purpose Note")
    rent_date = fields.Date(string="Date of rent", default=fields.Date.context_today)
    return_date = fields.Date(string="Date of return", compute="_compute_day_of_rant")
    rent_day = fields.Integer(string="rent Day", compute="_compute_day_of_rant")
    responsible_person_internal = fields.Many2one('hr.employee', string="Responsible person")
    product_details_lines = fields.One2many('product.for.rent', 'rent_id', string="Car Details")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validation', 'Pending for delivery'),
        ('cancel', 'Cancel'),
        ('return', 'Return'),

    ], string='Status', default='draft', readonly=True, copy=False, tracking=True)
    rent_package = fields.Many2one('rent.package',string="Package",domain=[('active','=',True)])

    nid_number =  fields.Char("Nid Number")
    nid =  fields.Binary("NID")
    driving_licence = fields.Char("Driving Lience")
    transfer_delivery_count = fields.Integer(compute='_compute_transfer_delivery_count',
                                             string='Transfer Delivery Count', store=False)
    can_return = fields.Boolean("Can Return",default=False)
    def count_done(self,done_qty):
        self.product_details_lines.done_qty = done_qty
        
        
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
    
    @api.depends('rent_package')
    def _compute_day_of_rant(self):
        self.rent_day = self.rent_package.day
        self.return_date = self.rent_date + timedelta(days=self.rent_day)
    
    
    def submit_for_validation(self):
        self.state = "validation"
        self.create_rent_history()
    
    def submit_for_cancel(self):
        self.state = "cancel"
    
    def submit_for_return(self):
        self.state = "return"
        self.env['car.product'].search([('id','=',self.product_details_lines.product_id.id)]).reserve_increase(self.product_details_lines.done_qty)
    
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
                    'res_user': self.responsible_person_internal.id,
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