from odoo import _,api,fields,models
from odoo.exceptions import UserError

class ProductForrent(models.Model):
    _name = "car.brand"
    _description = " car type brand"
    
    name = fields.Char("Name")
    color_tag = fields.Many2many('color.tag',string="Colors")