from odoo import fields, models, api, _ 
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    # _inherit = "sale.order,sale.order.line"
    _inherit = "product.template"

    buy_qty = fields.Char(string="Buy Quantity")
    bonus_qty = fields.Char(string="Bonus Quantity")
