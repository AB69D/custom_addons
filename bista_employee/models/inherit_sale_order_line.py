from odoo import fields,_,api,models

class InheritSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description  = "sale order line"
    
    product_package = fields.Integer(related='product_template_id.package_count',string="Package Count")