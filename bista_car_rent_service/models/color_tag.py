from odoo import _,api,fields,models
from odoo.exceptions import UserError

class ProductForrent(models.Model):
    _name = "color.tag"
    _description = "Color Tags"
    
    name =  fields.Char("Name")
    # brand_tag_line = fields.One2many('car.brand',inverse_name=)