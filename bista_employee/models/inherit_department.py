from odoo import fields,api,_,models

class DepartmentInherit(models.Model):
    _inherit = 'hr.department'
    
    manager_email = fields.Char(related='manager_id.private_email', string='Manager Email', readonly=True)
    manager_phone = fields.Char(related='manager_id.mobile_phone', string='Manager Phone', readonly=True)
    service = fields.Many2many('department.service',string="Services")
    manager_unit = fields.Selection([
        ('canada', 'Canada'),
        ('usa', 'USA'),
        ('other', 'Other')
    ], string="Manager Unit")
    
    # @api.onchange('manager_id')
    # def on_change_manager_id(self):
    #     if self.manager_id:
    #         manager_email = self.env['hr.employee'].search([('id', '=', self.manager_id.id)]).private_email
    #         self.manager_email = manager_email
            
    #     if self.manager_id:
    #         manager_phone = self.env['hr.employee'].search([('id', '=', self.manager_id.id)]).phone
    #         self.manager_phone = manager_phone

    #     else:
    #         self.manager_email = None
    #         self.manager_phone = None
