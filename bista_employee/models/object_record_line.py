from odoo import api,fields,models

class ObjectRecordLine(models.Model):
    _name = 'object.record.line'
    _description = "this table store the details of the user"
    
    name =  fields.Char("Name")
    email = fields.Char("Email")
    phone = fields.Char("Phone")
    district = fields.Char("Description")
    default_value = fields.Char("Default Value",default="ok")
    tags = fields.Many2many('record.tag',string="Tags")
    tags_line = fields.Many2one('employee.employee',string="Supervisor")
    
    def get_context_value(self,context=None):
        return self.env.context.get('passing_value')
    context_value = fields.Char("Context",default=get_context_value)
    
    @api.model
    def default_get(self, fields_list):
        result = super(ObjectRecordLine,self).default_get(fields_list)
        
        result.update({
            'default_value':'asi default_get',
        })
        return result

    
    def show_male(self):
        ObjEmployee = self.env['employee.employee'].search([('gender','=','male')])# is this line i am filtering the model employee.employee by domain gender = male and get the ids by a object
        action = self.env.ref('bista_employee.action_employee_employee').read()[0] #in this line i am accesing all data of that model
        action['domain'] = [('id','in',ObjEmployee.ids)] #in this domain i am executing a for loop for executing the domain i mean 
        return action
    
    def show_female(self):
        ObjEmployee = self.env['employee.employee'].search([('gender','=','female')])
        action = self.env.ref('bista_employee.action_employee_employee').read()[0]
        action['domain'] = [('id','in',ObjEmployee.ids)]
        return action