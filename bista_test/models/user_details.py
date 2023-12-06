from odoo import models,fields,api
from datetime import datetime,date

class UserDetails(models.Model):
    _name = 'user.details'
    _description = " this table is for store the data of user"
    _inherit = 'mail.activity.mixin'
    
    name = fields.Char("Name", required=True)
    email = fields.Char("Email")
    phone = fields.Char("Phone")
    district = fields.Char("District")
            
        
    
    
