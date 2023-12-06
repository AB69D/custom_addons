from odoo import fields,api,models,_ 

class ProductForbuy(models.Model):
    _name = "product.for.buy"
    _description = "product for buy"
    _inherit = "car.product"
    
    product_id = fields.Many2one('car.product', string='Product')
    qty = fields.Integer(string="Quantity", default=1)
    buy_id = fields.Many2one('purchase.car',string="buy_id")
    cost_price = fields.Char(related='product_id.cost_price',string="Price")



class PurchaseCar(models.Model):
    _name = 'purchase.car'
    _description = "purchase  new car"
    _inherit = ['product.for.buy']
    
    vendor = fields.Many2one('res.partner',string="Vendor")
    confirmation_date =  fields.Date("Confirmation Date")
    product_details_lines = fields.One2many('product.for.buy', 'buy_id', string="Car Details") 