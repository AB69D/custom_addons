from odoo import fields, models, api, _ 


class StockMove(models.Model):
    _inherit = "stock.move"

    act_qty = fields.Char(string="Actual Quantity")
    bonus_qty = fields.Char(string="Bonus Quantity")
