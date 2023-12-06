from odoo import api,fields,models
from odoo.exceptions import ValidationError

class ClassClass(models.Model):
    _name = "class.class"
    
    name = fields.Char("name")
    # students = fields.One2many('employee.employee','class_object_line',string="Students")
    
