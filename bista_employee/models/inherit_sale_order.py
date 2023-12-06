from odoo import api,models,_,fields
from odoo.exceptions import ValidationError

class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = "inherit sale order"
    
    phone = fields.Char(string="Phone")
    
    @api.onchange('partner_id')
    def get_phone(self):
        self.phone = self.partner_id.phone
        
    @api.onchange('phone')
    def get_user(self):
        if self.phone:
            user = self.env['res.partner'].search([('phone', '=', self.phone)], limit=1)
            if user:
                self.partner_id = user.id
                print(user.phone)
            else:
                self.partner_id = False
    
    email = fields.Char(related='partner_id.email',string="Email")
    def action_confirm(self):
        for rec in self:
            if rec.partner_id.phone:
                for roc in rec.order_line:
                    if roc.product_id.package_count % roc.product_uom_qty  == 0:
                        raise ValidationError("Must need to fullfill the conditon of package counter")
                    list_price = roc.product_id.list_price
                    print(list_price)
                    if list_price > roc.price_unit:
                        raise ValidationError("you can not sell this product with this price ")
            else:
                raise ValidationError("Customer should have his/her phone number")
        print("action_confirm..........................!")
        return super(InheritSaleOrder,self).action_confirm()
    