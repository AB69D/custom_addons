from odoo import api,fields,_,models

class InheritProductProduct(models.Model):
    _inherit = 'product.template'
    _description = "inherit product templete"
    
    package_count = fields.Integer("Package Count",default=1)