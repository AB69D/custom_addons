from odoo import _,api,fields,models
from odoo.exceptions import UserError

class ProductForrent(models.Model):
    _name = "car.product"
    _description = " car product for rent"
    
    name =  fields.Char("Name")
    image = fields.Image("Image")
    cost_price =fields.Float("Cost Price")
    sale_price =fields.Float("Sale Price")
    
    brand = fields.Many2one('car.brand',string="Brand")
    color_tag = fields.Many2many(related='brand.color_tag', string="Color Tag")
    avilable_quantity = fields.Integer("Avilable Quantity", default=0)
    transfer_history_count = fields.Integer(compute='_compute_transfer_history_count',
                                             string='Transfer History Count', store=False)
    
    def _compute_transfer_history_count(self):
        for record in self:
            transfer_count = self.env['rent.history'].search_count([
                ('product_details_lines.product_id.id', '=', self.id),
            ])
            record.transfer_history_count = transfer_count
            
    @api.onchange('brand')
    def color_filter(self):
        if self.brand:
            brand_colors = self.env['car.brand'].search([]).color_tag.ids
            print(f"Brand colors: {brand_colors}")
            domain = [('id', 'in', brand_colors)]
            print(f"Domain: {domain}")
            return {'color_tag': {'domain': domain}}
            
        else:
            self.color_tag = False
            return {
                'color_tag': {
                    'domain':[]
                }
            }
    
    def action_total_rent_history(self):
        histories = self.env['rent.history'].search([('product_details_lines.product_id.id', '=', self.id)])
        action = self.env.ref('bista_car_rent_service.action_rent_history').read()[0]
        action['domain'] = [('id', 'in', histories.ids)]

        return action
    
    def reserve_increase(self ,qty):
        self.avilable_quantity += qty
        
    def reserve_dicrease(self ,qty):
        self.avilable_quantity -= qty