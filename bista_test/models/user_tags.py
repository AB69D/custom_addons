from odoo import models,fields,api
from datetime import datetime,date

class UserDetails(models.Model):
    _name = 'user.tags'
    _description = " this table is for store tag "
    