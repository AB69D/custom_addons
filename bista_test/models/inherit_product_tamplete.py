from odoo import api,_,fields,models
from odoo.exceptions import ValidationError

class InheritProductTamplete(models.Model):
    _inherit = 'product.template'
    
    for_craitery_qty = fields.Integer("Range for Bonus")
    bonus_qty = fields.Integer("Bonus Quantity")
    

class InheritSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    bonus_qty = fields.Char("Bonus",readonly=True,compute="_compute_bonus_qty")
    
    @api.depends('product_uom_qty')
    def _compute_bonus_qty(self):
        for record in self:
            if (
                record.product_template_id
                and record.product_template_id.for_craitery_qty
                and record.product_uom_qty % record.product_template_id.for_craitery_qty == 0
            ):
                record.bonus_qty = (record.product_uom_qty // record.product_template_id.for_craitery_qty) * record.product_template_id.bonus_qty
            else:
                record.bonus_qty = 0

class InheritStockPicking(models.Model):
    _inherit = 'stock.move'
    
    bonus_demand = fields.Char("Bonus Demand")
    
    
    
    
class InheritStockPicking(models.Model):
    _inherit = 'account.move.line'
    
    bonus_qty = fields.Char("Bonus Quentity")
    
    
    
class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = "inherit sale order"
    
    def action_confirm(self):
        for rec in self:
            for roc in rec.order_line:
                if roc.product_uom_qty < roc.product_template_id.qty_available:
                    continue
                else:
                    raise ValidationError("No Enough Product on hand")
        print("action_confirm..........................!")
        return super(InheritSaleOrder,self).action_confirm()
    