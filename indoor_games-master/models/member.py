from odoo import api, fields, models
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import re



class IndoorGames(models.Model):
    _name = "indoor.member"
    _inherit = []
    _description = "Indoor Games Management System Members"

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    image = fields.Image(string="Image")
    website = fields.Char(string='Website')
    occupation = fields.Char(string='Occupation')
    language = fields.Char(string='Language')
    gender = fields.Selection([('male', "Male"), ('female', 'Female')], string="Gender")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age")

    height = fields.Float(string="Height")
    weight = fields.Float(string="Weight")
    bmi = fields.Float(string="BMI")
    bmr = fields.Float(string="BMR")
    injury_point = fields.Selection([('head', "Head"), ('face', "Face"), ('neck', "Neck")], string="Injury Point")
    injury_type = fields.Selection([('fractures', "Fractures"), ('burns', "Burns"), ('concussion', "Concussion"), ('sprains', "Sprains"), ('catastrophic_injury', "Catastrophic Injury"), ('pulled_muscle', "Pulled Muscle"), ('strains', "Strains"), ('animal_bites', "Animal Bites"), ('blunt_trauma', "Blunt Trauma"), ('dislocation', "Dislocation"),('tendinitis', "Tendinitis")], string="Injury Type")
    injury_level = fields.Selection([('minor', "Minor"), ('moderate', "Moderate"), ('serious', "Serious"), ('severe', "Severe"), ('critical', "Critical"), ('maximal', "Maximal")], string="Injury Level")
    neck = fields.Integer(string="Neck")
    chest = fields.Integer(string="Chest")
    right_arm = fields.Integer(string="Right Arm")
    left_arm = fields.Integer(string="Left Arm")
    waist = fields.Integer(string="Waist")
    hips = fields.Integer(string="Hips")
    right_thigh = fields.Integer(string="Right Thigh")
    left_thigh = fields.Integer(string="Left Thigh")
    right_calf = fields.Integer(string="Right Calf")
    left_calf = fields.Integer(string="Left Calf")



    member_type = fields.Char(string='Member Type', default="None", readonly=1)
    membership_end_time = fields.Char(string="Membership Expirity Time", default="None", readonly=1)
    membership_status = fields.Boolean(string="Membership Status", compute="_get_status")
    # member_type = fields.Char(string='Member Type', default="None", readonly=1, compute="_get_mem_status")

    parent_o2m_players = fields.Many2one("indoor.event", string="Parent m2m players", invisible=1)

    member_transaction_cnt = fields.Integer(string="Member Transaction cnt", compute="_get_member_transaction_cnt")

    def _get_mem_status(self):
        pass
    def validate_phone(self):
        pattern = re.compile(r"^\+8801[13456789]\d{8}$")
        # pattern = re.compile(r"^+8801")
        # pattern = re.compile(r"^[13456789]\d{8}$")
        # str = "+8801719342241"
        if pattern.match(self.phone):
            print("Yes")
        else:
            print("No")
        # pattern = re.compile(r'^[789]\d{9}$')
        # n = int(input())
        # for i in range(n):
        #     x = input()
        #     if pattern.match(x):
        #         print("YES")
        #     else:
        #         print("NO")
    @api.onchange('phone')
    def onchange_phone(self,):
        for item in self:
            if item.phone:
                pattern = re.compile(r"^\+8801[13456789]\d{8}$")
                if pattern.match(item.phone) == None:
                    raise UserError("Phone Number is not valid")
    @api.onchange('email')
    def onchange_email(self,):
        for item in self:
            if item.email:
                # pattern = re.compile(r"^[a-zA-Z0-9'*()_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$")
                pattern = re.compile(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$")
                if pattern.match(item.email) == None:
                    raise UserError("Email is not valid")



    @api.depends('membership_end_time')
    def _get_status(self):
        if self.membership_end_time == "None":
            self.membership_status = False
        else:
            datetimeStart = self.membership_end_time +  " 12:00:00"
            datetime1 = datetime.strptime(datetimeStart, "%Y-%m-%d %H:%M:%S")
            today = date.today()

            if today > datetime1.date():
                self.membership_status = False
                self.member_name.member_type = "None"
            else:
                self.membership_status = True
    

    def _get_member_transaction_cnt(self):
        for item in self:
            search_transaction_ids = item.env['indoor.transaction'].search([('member_name', '=', self.name)])
            cnt = 0
            for rec in search_transaction_ids:
                cnt += 1
            item.member_transaction_cnt = cnt
    def button_smart_paid(self):
        return {'name' : 'Transaction',
            'type' : 'ir.actions.act_window',
            'res_model' : 'indoor.transaction',
            'view_mode' : 'tree',
            # 'target' : 'new',
            'target' : 'current',
            'domain' : [('member_name', '=', self.name)]
        }
