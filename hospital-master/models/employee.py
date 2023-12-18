from odoo import fields, models, api, _ 


class HrEmployee(models.Model):
    _inherit = "hr.employee"


    joining_date = fields.Date(string="Joining Date")
    county = fields.Char(string="County")
    bkash_account_no = fields.Char(string="Bkash")

    parent_emp = fields.Many2one("hr.department", string="hr_employee") # already exists so donot work
    
    # email = fields.Char(string="Email")
    # unit = fields.Char(string="Unit")
    # phone = fields.Char(string="Email")
