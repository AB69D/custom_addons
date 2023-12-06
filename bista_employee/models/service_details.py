from odoo import api,_,models,fields

class DepartmentService(models.Model):
    _name = 'department.service'
    _description = "Department Service"
    
    name = fields.Char("Name")
    details = fields.Char("Details")