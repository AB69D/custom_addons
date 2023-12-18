from odoo import fields, models, api, _ 


class StockMove(models.Model):
    _inherit = "account.move.line"

    bonus_qty = fields.Char(string="Bonus Quantity")
