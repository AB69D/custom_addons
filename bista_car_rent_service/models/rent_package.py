from odoo import fields,api,models,_ 

class RentPackage(models.Model):
    _name = 'rent.package'
    _description = " PAckage details for rent"
    
    name =  fields.Char("Name")
    day = fields.Integer("Number of Day")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    rent_amount = fields.Monetary(string='Rent', currency_field='currency_id', required=True)

    active = fields.Boolean("active")