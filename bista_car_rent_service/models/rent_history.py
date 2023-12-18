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
    _order = 'id desc'
    
    ref = fields.Char("ref" ,readonly=True)
    res_user = fields.Many2one('hr.employee',string="User")
    rent_date = fields.Date(string="Rent Date")
    return_date = fields.Date(string="Return Date")
    source_doc = fields.Many2one('user.form.register',string="Source")
    product_details_lines = fields.One2many('line.history.rent', 'rent_id', string="Car Details")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('payment', 'Pending Return'),
        ('paid', 'Returned'),

    ], string='Status', default='draft', readonly=True, copy=False, tracking=True)
    
    def check_for_reserve(self):
        for rec in self.product_details_lines:
            reserve_qty = self.env["car.product"].search([('id','=',rec.product_id.id)]).avilable_quantity
            rec.reserve_qty = reserve_qty
    
    def reserve_maintain(self,qty):
        for rec in self.product_details_lines:
            self.env['car.product'].search([('id','=',rec.product_id.id)]).reserve_dicrease(qty)

        
    def get_paid(self):
        for rec in self:
            for line in rec.product_details_lines:
                if line.reserve_qty >= line.qty:
                    self.state = "payment"
                    line.done_qty = line.qty
                    self.env['user.form.register'].search([('ref','=',rec.source_doc.ref)]).count_done(line.done_qty,line.product_id)
                    # self.reserve_maintain(line.done_qty)
                    self.env['car.product'].search([('id','=',line.product_id.id)]).reserve_dicrease(line.done_qty)
                    line.done_qty = line.qty
                    self.env['user.form.register'].search([('ref','=',rec.source_doc.ref)]).charge_state_deliver()
                else:
                    raise ValidationError("Don't have enough reserve for rent")
        
    @api.model
    def create(self, vls):
        vls['ref'] = self.env['ir.sequence'].next_by_code('rent.history')
        res = super(RentHistory, self).create(vls)
        return res
    
    def get_payment(self):
        self.state = 'paid'
        
        
