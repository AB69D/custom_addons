from odoo import api, fields, models
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class IndoorGames(models.Model):
    _name = "indoor.transaction"
    _inherit = []
    _description = "Indoor Games Management System Event"
    _rec_name = "transaction_id"


    def _get_member_name(self):
        # print(".............self.env.context", self.env.context)
        return self.env.context.get('member_name')
    member_name = fields.Char(string="Event Master", default=_get_member_name)

    def _get_event_id(self):
        return self.env.context.get("event_id")
    event_id = fields.Char(string="Event ID", default=_get_event_id)

    def _get_event_name(self):
        return self.env.context.get('event_game')
    event_game = fields.Char(string="Event Game", default=_get_event_name)

    def _get_event_game_id(self):
        return self.env.context.get('event_game_id')
    event_game_id = fields.Char(string="Event Game ID", default=_get_event_game_id)

    # event_players = fields.One2many("indoor.member", "parent_o2m_players", string="Players")

    def _get_event_start_time(self):
        return self.env.context.get('event_start_time')
    event_start_time = fields.Datetime(string="Start Time", default=_get_event_start_time)

    def _get_event_duration(self):
        return self.env.context.get('event_duration')
    event_duration = fields.Char(string="Duration", default=_get_event_duration)

    def _get_event_end_time(self):
        return self.env.context.get('event_end_time')
    event_end_time = fields.Datetime(string="End Time", default=_get_event_end_time)
    # state = fields.Selection([('draft',"Draft"),('confirm',"Confirm"),('cancel',"Cancel")], string="Status")

    # delay_hour = fields.Integer(string="Delay Hour", default=0)

    def _get_subtotal(self):
        return self.env.context.get('subtotal')
    subtotal = fields.Integer(string="Subtotal", default=_get_subtotal)

    def _get_discount(self):
        return self.env.context.get('discount')
    discount = fields.Integer(string="Discount", default=_get_discount)

    def _get_participation_discount(self):
        return self.env.context.get('participation_discount')
    participation_discount = fields.Integer(string="Participation Discount", default=_get_participation_discount)
    # delay_charge = fields.Integer(string="Delay Charge", default=0, readonly=1)

    def _get_tax(self):
        return self.env.context.get('tax')
    tax = fields.Integer(string="Tax", default=_get_tax)

    def _get_bill(self):
        return self.env.context.get('bill')
    bill = fields.Integer(string="Bill", default=_get_bill)


    def _get_transaction_id(self):
        # for item in self:
        #     return         
        print("........................self.id", self.id)
        # return "ev-" + str(self.id)
        # self.env.uid
        now = datetime.now()
        # current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        current_datetime = now.strftime("%Y%m%d%H%M%S%f")
        print("...........type", type(current_datetime))
        return current_datetime
    transaction_id = fields.Char(string="Transaction ID", default=_get_transaction_id) 
    payment_method = fields.Selection([('cash', "Cash"), ('bkash', "bKash")], string="Payment Method")
    payment_status = fields.Boolean(string="Payment Status")

    paid_amount = fields.Integer(string="Paid Amount")
    due_amount = fields.Integer(string="Due Amount", compute="_get_due_amount")
    def _get_due_amount(self):
        # for item in self:
            # item.due_amount = item.bill - item.paid_amount
        pass

