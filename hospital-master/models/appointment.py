from odoo import api, fields, models

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Management System'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(string="Patient", comodel_name='hospital.patient')
    gender = fields.Selection(related="patient_id.gender")
    appointment_date = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)

    age = fields.Integer(related="patient_id.age", string="AGE")

    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority")
    state = fields.Selection([('draft', 'Draft'), ('in_consultant', 'Inconsultant'), ('done', 'Done'), ('cancel', 'Cancel')], string="States")

    def get_context(self):
        return self.env.context.get('val')
    
    context = fields.Char(string="context", default=get_context)

    def object_test(self):
        print("button clicked...........")
        print(self.env.context)
        return {
            'effect' : {
                'fadeout' : 'slow',
                'message' : 'clicked successfully',
                'type' : 'rainbow_man'
            }
        }
