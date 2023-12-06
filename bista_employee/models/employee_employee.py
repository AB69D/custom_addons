from odoo import api, fields, _, models
from datetime import date
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _name = 'employee.employee'
    _description = "This model is for store the information of the employee"

    def get_height(self):
        return float(5.5)
    
    name = fields.Char("Name", required=True)
    email = fields.Char("Email")
    work_mail = fields.Char("Work Mail")
    work_phone = fields.Char("Work Phone")

    refer = fields.Boolean("Refer from Linkdin", required=True)
    height = fields.Float("Height", default=get_height)
    age = fields.Integer("Age", compute="_compute_age", readonly=True, store=True)
    note = fields.Html("Note", help="Enter your html content")
    image = fields.Image("Image")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    monetary_field = fields.Monetary(string='Salary', currency_field='currency_id', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], required=True)
    birthday = fields.Date("Date of birth", required=True)
    refer_employe = fields.Many2many("object.record.line", string="Refer Employee")
    id_for_tag = fields.Integer("ID")

    work_address = fields.Text("Work Address")
    work_location = fields.Char("Work Locatiom")
    work_hours = fields.Selection([('40', 'Standard 40 hours/week'), ('20', '20 hours/week')])

    private_address = fields.Text('Address')
    private_email = fields.Char('Private Email')
    personal_phone = fields.Char("Personal Phone")
    marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried')])

    cv = fields.Binary("Resume")
    supervice = fields.One2many('object.record.line', inverse_name="tags_line", string="supervicing")

    def test_for_add_item(self):
        self.refer_employe = [(0,0,{'name':"Abid",
                                    'email':'abid@gmail.com'})]
        
    def test_for_remove_all_item(self):
        self.refer_employe = [(5,)]
        
    def remove_all_and_replace(self):
        self.refer_employe = [(6,0,[self.id_for_tag,])]
    
    def add_one_element(self):
        self.refer_employe = [(4,self.id_for_tag)]
    
    def single_remove(self):
        self.refer_employe = [(3, self.id_for_tag)]
    
    def single_remove_and_delete(self):
        self.refer_employe = [(2,self.id_for_tag)]
        
    @api.onchange('gender')
    def gender_mention(self):
        if self.name and isinstance(self.name, str):
            if self.gender:
                spit_name = self.name.split('(')
                self.name = spit_name[0]
            if self.gender == 'male':
                self.name += '(M)'
            if self.gender == 'female':
                self.name += '(F)'

    @api.depends('birthday')
    def _compute_age(self):
        for rec in self:
            for record in rec:
                if rec.birthday:
                    today = date.today()
                    record.age = today.year - record.birthday.year
                else:
                    record.age = 0

    @api.model
    def create(self, vals):
        print("Here i am ...! Create Method ")
        print(vals)
        record = super(Employee, self).create(vals)
        return record

    def write(self, vals):
        print("Here i am ...! Write Method")
        print(vals)
        if self.create_uid.id == self.env.user.id:
            record = super(Employee, self).write(vals)
            return record
        else:
            raise ValidationError("You dont have the access to update this record")
            

    def unlink(self):
        print("Here i am ...! Unlink Method ")
        res = super(Employee, self).unlink()
        return res

    @api.constrains('age')
    def _constraint_age(self):
        for record in self:
            if record.age < 18:
                raise ValidationError("Less then 18 Years Old")

    @api.constrains('name')
    def _constraint_name(self):
        count = self.env['employee.employee'].search_count([('name', '=', self.name)])
        if count > 1:
            raise ValidationError("You already registered...!")

    def show_all_tags(self):
        ObjTag = self.env['record.tag'].search([])
        action = self.env.ref('bista_employee.action_record_tag').read()[0]
        action['domain'] = [('id', 'in', ObjTag.ids)]

        return action

    def show_all_record(self):
        ObjRecord = self.env['object.record.line'].search([])
        action = self.env.ref('bista_employee.action_object_record_line').read()[0]
        action['domain'] = [('id', 'in', ObjRecord.ids)]

        return action

    def create_tag(self):
        return {
            'name': 'python action for create new tag',
            'res_model': 'record.tag',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

    def create_record(self):
        return {
            'name': 'python action for create Record',
            'res_model': 'object.record.line',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_tags_line': self.id,
                'passing_value':'ami context e asi',
            },
        }

    def show_records(self):
        domain = [('tags_line.id', '=', self.id)]
        return {
            'name': 'show the record of this user',
            'res_model': 'object.record.line',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'target': 'new'

        }
        
    def show_service_product(self):
        domain = [('type','=','service')]
        return {
            'name': 'All Products',
            'res_model':'product.product',
            'view_mode' : 'tree',
            'type': 'ir.actions.act_window',
            'target':'new',
            'domain':domain
            
        }
    def all_jobs(self):
        return {
            'name':'All jobs',
            'res_model':'hr.job',
            'view_mode':'tree',
            'type':'ir.actions.act_window',
            'target':'new'
        }
    def create_recuirment_professional_service_traine(self):
        return{
            'name': 'Traine fro Professional Service',
            'res_model': 'hr.job',
            'view_mode': 'form',
            'type':'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_department_id':'7',
                'default_name':'traine',
                'default_user_id': self.env.uid,
            }
        }

