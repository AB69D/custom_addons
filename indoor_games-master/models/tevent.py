from odoo import api, fields, models
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class IndoorGames(models.TransientModel):
    _name = "indoor.tevent"
    _description = "Indoor Games Management System tevent"

    member_id = fields.Many2one("indoor.member", string="Event Master")
    game_id = fields.Many2one("indoor.game",string="Event Game")

    start_time = fields.Datetime(string="Start Time")
    duration = fields.Char(string="Duration")
    end_time = fields.Datetime(string="End Time")

    event_game_id = fields.Char(string="Event Game ID")

    