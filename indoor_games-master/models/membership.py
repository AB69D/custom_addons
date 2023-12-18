from odoo import api, fields, models
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta


class IndoorGames(models.Model):
    _name = "indoor.membership"
    _inherit = []
    _description = "Indoor Games Management System Membership"
    _rec_name = "member_name"

    # member_name = fields.Char(string="Name") # Many2one with indoor.member
    member_name = fields.Many2one("indoor.member", string="Name", domain=[('member_type', '=', 'None')])

    partner_type = fields.Selection([('100', "Basic"), ('200', 'Silver'), ('300', "Gold")], string="Membership Type")
    partner_type_member_update = fields.Char(string="Member Update", compute="_get_type")

    # membership_products = fields.One2many()
    game_ids = fields.One2many("indoor.game","parent_id", string="Games")

    membership_duration = fields.Selection([('1', "1 Month"), ('2', '2 Month'), ('3', "3 Month")], string="Duration")
    # membership_start_time = fields.Date(string="Start Time") --> cancel

    membership_end_time = fields.Char(string="End Time", compute="_get_end_date") # onchange: auto calculate from duration
    
    # membership_staus = active/expired --> depends--> onchange: membership_end_time
    membership_status = fields.Boolean(string="Membership Status", compute="_get_status")

    membership_fees = fields.Integer(string="Fees", compute="_get_fees", readonly=1) # onchange: basic-->100, silver-->200, gold-->300 times(*) 1 for 1 month, 2 for 2 month

    @api.depends('partner_type', 'membership_duration')
    def _get_fees(self):
        print("******=====calling compute function=====******")
        for item in self:
            item.membership_fees = int(item.partner_type) * int(item.membership_duration)
    @api.depends('membership_duration')
    def _get_end_date(self):
        today = date.today()
        for item in self:
            item.membership_end_time = today + relativedelta(months=int(item.membership_duration))

    # https://stackoverflow.com/questions/29867945/python-find-date-beginning-two-months-prior-to-today-and-start-on-a-monday

    @api.depends('membership_end_time')
    def _get_status(self):
        datetimeStart = self.membership_end_time +  " 12:00:00"
        datetime1 = datetime.strptime(datetimeStart, "%Y-%m-%d %H:%M:%S")
        today = date.today()

        if today > datetime1.date():
            self.membership_status = False
            self.member_name.member_type = None
        else:
            self.membership_status = True

        # _get_type()
        for item in self:
            print("Member type updated called................")
            item.partner_type_member_update = item.partner_type # jekhan theke call deoya hoyeche sekhaner value na deoyay error
            # item.member_name.member_type = item.partner_type
            item.member_name.membership_end_time = item.membership_end_time
            if item.partner_type == '100':
                item.member_name.member_type = 'Basic'
            elif item.partner_type == '200':
                item.member_name.member_type = 'Silver'
            elif item.partner_type == '300':
                item.member_name.member_type = 'Gold'
        # return True --> not return, something self..........
        # self.membership_status = True
    # https://stackoverflow.com/questions/32287708/python-compare-the-date-in-the-string-with-todays-date

    def _get_type(self):
        for item in self:
            print("Member type updated called................")
            item.partner_type_member_update = item.partner_type # jekhan theke call deoya hoyeche sekhaner value na deoyay error
            # item.member_name.member_type = item.partner_type
            item.member_name.membership_end_time = item.membership_end_time
            if item.partner_type == '100':
                item.member_name.member_type = 'Basic'
            elif item.partner_type == '200':
                item.member_name.member_type = 'Silver'
            elif item.partner_type == '300':
                item.member_name.member_type = 'Gold'
            

            # print("member name................", item.member_name.member_type)
            # print("member type................", item.partner_type)
            