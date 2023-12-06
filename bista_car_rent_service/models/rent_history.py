from odoo import fields,api,models,_
from odoo.exceptions import ValidationError

class ProductForrent(models.Model):
    _name = 'line.history.rent'
    _description = "product list"
    
    product_id = fields.Many2one('car.product', string='Product')
    qty = fields.Integer(string="Quantity", default=1)
    rent_id = fields.Many2one('user.form.register', string="rent")
    done_qty = fields.Integer(string="Done", default=0, readonly=True)
    reserve_qty = fields.Integer(string="Reserve", default=0, readonly=True)
    demand_qty = fields.Integer(string="Demand", compute='_compute_demand',
                                           readonly=True, default=0)

    @api.depends('qty', 'done_qty')
    def _compute_demand(self):
        for rec in self:
            rec.demand_qty = rec.qty - rec.done_qty

class RentHistory(models.Model):
    _name = 'rent.history'
    _description = "all frecord of rent history"
    _rec_name = 'ref'
    
    ref = fields.Char("ref" ,readonly=True)
    res_user = fields.Many2one('hr.employee',string="User")
    rent_date = fields.Date(string="Rent Date")
    return_date = fields.Date(string="Return Date")
    source_doc = fields.Many2one('user.form.register',string="Source")
    product_details_lines = fields.One2many('line.history.rent', 'rent_id', string="Car Details")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('payment', 'Pending for payment'),
        ('paid', 'paid'),

    ], string='Status', default='draft', readonly=True, copy=False, tracking=True)
    
    def check_for_reserve(self):
        reserve_qty = self.env["car.product"].search([('id','=',self.product_details_lines.product_id.id)]).avilable_quantity
        self.product_details_lines.reserve_qty = reserve_qty
    
    def reserve_maintain(self,qty):
        self.env['car.product'].search([('id','=',self.product_details_lines.product_id.id)]).reserve_dicrease(qty)

        
    def get_paid(self):
        if self.product_details_lines.reserve_qty > self.product_details_lines.qty:
            self.state = "payment"
            self.product_details_lines.done_qty = self.product_details_lines.qty
            self.env['user.form.register'].search([('ref','=',self.source_doc.ref)]).count_done(self.product_details_lines.done_qty)
            self.reserve_maintain(self.product_details_lines.done_qty)
        else:
            raise ValidationError("Don't have enough reserve for rent")
        
    @api.model
    def create(self, vls):
        vls['ref'] = self.env['ir.sequence'].next_by_code('rent.history')
        res = super(RentHistory, self).create(vls)
        return res
    
    def get_payment(self):
        self.state = 'paid'