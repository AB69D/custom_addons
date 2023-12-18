from odoo import api, fields, models
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class IndoorGames(models.Model):
    _name = "indoor.tournament"
    _inherit = []
    _description = "Indoor Games Management System Tournament"
    _rec_name = "member_name"

    member_name = fields.Many2one("indoor.member", string="Tournament Master")
    member_email = fields.Char(string="Email")    
    member_type = fields.Char(string="Membership Type")
    membership_status = fields.Boolean(string="Membership Status")
    tournament_start_time = fields.Datetime(string="Start Time")
    tournament_duration = fields.Selection([('1', "1 Hour"), ('2', '2 Hour'), ('3', "3 Hour")], string="Duration")
    state = fields.Selection([('draft',"Draft"),('confirm',"Confirm"),('cancel',"Cancel")], string="Status", default='draft')

    tournament_end_time = fields.Datetime(string="End Time")

    record_line_ids = fields.One2many("indoor.event", "tournament_id", string="Tournament")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    subtotal = fields.Monetary(string="Subtotal", compute="_get_subtotal")
    discount = fields.Monetary(string="Discount", compute="_get_discount")
    participation_discount = fields.Monetary(string="Participation Discount", compute="_get_participation_discount")
    tax = fields.Monetary(string="Tax", compute="_get_tax")
    bill = fields.Monetary(string="Bill", compute="_get_bill")

    tournament_paid_amount = fields.Monetary(string="Paid", compute="_get_tournament_paid_amount")
    tournament_due_amount = fields.Monetary(string="Due", compute="_get_tournament_due_amount")
    tournament_transaction_cnt = fields.Integer(string="Transaction Count", compute="_get_tournament_transaction_cnt")


    def _get_subtotal(self):
        for rec in self:
            sum = 0
            for item in rec.record_line_ids:
                sum += item.subtotal
            rec.subtotal = sum
    def _get_discount(self):
        for item in self:
            # item.discount = 0
            for rec in item.record_line_ids:
                if item.member_name.member_type == "None":
                    item.discount += 0
                elif item.member_name.member_type == "Basic":
                    item.discount += (item.subtotal * rec.event_game.basic_partner_discount_percentage/100)   
                elif item.member_name.member_type == "Silver":
                    item.discount += (item.subtotal * rec.event_game.silver_partner_discount_percentage/100)  
                elif item.member_name.member_type == "Gold":
                    item.discount += (item.subtotal * rec.event_game.gold_partner_discount_percentage/100)
    def _get_participation_discount(self):
        for item in self:
            item.participation_discount = 0
    def _get_tax(self):
        for item in self:
            item.tax = item.subtotal * 2/100
            # item.tax = 0
    def _get_bill(self):
        for item in self:
            item.bill = item.subtotal - item.discount - item.participation_discount + item.tax
    def _get_tournament_paid_amount(self):
        for item in self:
            search_transaction_ids = item.env['indoor.transaction'].search([('event_id', '=', "tournament-"+str(item.id))])
            sum = 0
            # cnt = 0
            for rec in search_transaction_ids:
                sum += rec.paid_amount
                # cnt += 1
            item.tournament_paid_amount = sum
            # item.tournament_transaction_cnt = cnt
    def _get_tournament_transaction_cnt(self):
        for item in self:
            search_transaction_ids = item.env['indoor.transaction'].search([('event_id', '=', "tournament-"+str(item.id))])
            cnt = 0
            for rec in search_transaction_ids:
                cnt += 1
            item.tournament_transaction_cnt = cnt
    def _get_tournament_due_amount(self):
        for item in self:
            item.tournament_due_amount = item.bill - item.tournament_paid_amount

    def button_confirm(self):
        self.write({
           'state': "confirm"
        })
        for item in self:
            for rec in item.record_line_ids:
                rec.write({
                    'state': "confirm"
                })
        
    def button_cancel(self):
        self.write({
           'state': "cancel"
        })
        for item in self:
            for rec in item.record_line_ids:
                rec.write({
                    'state': "cancel"
                })
        
    def button_draft(self):
        self.write({
           'state': "draft"
        })
        for item in self:
            for rec in item.record_line_ids:
                rec.write({
                    'state': "draft"
                })
        
    def button_smart_paid(self):
        action = self.env.ref('indoor.action_indoor_transaction').read()[0]
        action['domain'] = [('event_id', '=', "tournament-"+str(self.id))]
        return action
        # return {'name' : 'Transaction',
        #     'type' : 'ir.actions.act_window',
        #     'res_model' : 'indoor.transaction',
        #     'view_mode' : 'tree',
        #     # 'target' : 'new',
        #     'target' : 'current',
        #     'domain' : [('event_id', '=', "tournament-"+str(self.id))]
        # }
    def button_make_payment(self):
        print("......id.....", self.id)
        return {'name' : 'Transaction',
            'type' : 'ir.actions.act_window',
            'res_model' : 'indoor.transaction',
            'view_mode' : 'form',
            'target' : 'new',
            # 'target' : 'current',
            # 'target' : 'main',
            'context' : {'member_name' : self.member_name.name, 
                         'event_id' : "tournament-"+str(self.id),
                        #  'event_game' : self.event_game.name, 
                        #  'event_game_id' : self.event_game_id,
                         'event_start_time' : self.tournament_start_time,
                         'event_duration' : self.tournament_duration,
                         'event_end_time' : self.tournament_end_time,
                         'subtotal' : self.subtotal,
                         'discount' : self.discount,
                         'participation_discount' : self.participation_discount,
                         'tax' : self.tax,
                         'bill' : self.bill
                        }
            # 'domain' : [('patient_id', '=', self.id)]
        }



    @api.onchange('member_name')
    def onchange_member_name(self,):
        for item in self:
            item.member_email = item.member_name.email
            item.member_type = item.member_name.member_type
            
            if item.member_name.membership_end_time == "None":
                item.membership_status = False
            else:
                if item.member_name.membership_end_time:
                    datetimeStart = item.member_name.membership_end_time +  " 12:00:00"
                    datetime1 = datetime.strptime(datetimeStart, "%Y-%m-%d %H:%M:%S")
                    today = date.today()

                    if today > datetime1.date():
                        item.membership_status = False
                    else:
                        self.membership_status = True

    @api.onchange('tournament_start_time','tournament_duration')
    def onchange_tournament_start_duration(self,):
        for item in self:
            if item.tournament_start_time and item.tournament_duration:
                item.tournament_end_time = item.tournament_start_time + timedelta(hours=int(item.tournament_duration))
    
    # @api.onchange('self.record_line_ids.event_start_time','self.record_line_ids.event_duration')
    # def onchange_tournament_start_duration(self,):
    #     for item in self:
    #         for rec in item.record_line_ids:

    #     if self.record_line_ids.event_start_time and self.record_line_ids.event_duration:
    #         self.record_line_ids.tournament_duration = item.event_start_time + timedelta(hours=int(item.event_duration))
    #     print("Type of timedelta: ", type(timedelta(hours=int(item.event_duration))))

