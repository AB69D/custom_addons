from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Management System'

    name = fields.Char(string='Name', tracking=True)
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string='Age', tracking=True)
    age_comp = fields.Integer(string='Age Calculated', compute="_compute_age")
    gender = fields.Selection([('male', "Male"), ('female', 'Female')], string='Gender', tracking=True)
    active = fields.Boolean(string="Archive", default=True)

    # own 
    bill = fields.Float(string="Bill")
    paid = fields.Boolean(string="Paid")
    
    # image = fields.Binary(string="Patient Image")
    documents = fields.Binary(string="Documents")
    
    document_name = fields.Char(string="File Name")
    image = fields.Image(string="Patient Image")
    prescription = fields.Html(string="Prescription")
    comments = fields.Text(string="Comments")

    currency_id = fields.Many2one("res.currency", string="Currency")
    ticket_fees = fields.Monetary(string="Ticket fees")
    other_cost = fields.Float(string="Other Cost")

    appointment_time = fields.Datetime(string="Appointment Time")
    booking_time = fields.Date(string="Booking Date")

    model_name = fields.Char(string="Model name")
    email = fields.Char(string="Email")

    state = fields.Selection([('step1',"Step 1"),('step2',"Step 2"),('step3',"Step 3")], string="Status")

    # with_context
    # def get_address(): # parent class e
        # print(self_context[email])
        # self.env.context
    # def get_info(): # child class e
        # address = context.get_address()
        # context.with_context({'email' : '123'}).get_address()

    # with_context


    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age_comp = today.year - rec.dob.year
            else:
                rec.age_comp = 0








    def action_create(self):
        emp_id = self.env['hospital.patient'].create({'name' : '1', 'age' : 30})
        emp_id.write({'name' : '12345', 'age' : 35})
    
    def pre_obj_res(self):
        return self.with_context(abc='def').obj_res()

    
    def obj_res(self):
        print("new contxt===",self.env.context)
        return {'name' : 'Patient',
                'type' : 'ir.actions.act_window',
                'res_model' : 'hospital.appointment',
                'view_mode' : 'tree,form',
                'target' : 'new',
                # 'target' : 'current',
                # 'target' : 'main',
                'context' : {'default_email' : 'example@gmail.com', 'val' : 'context value'},
                'domain' : [('patient_id', '=', self.id)]
        }

    def action_test(self):
        print("hello...........................")
        print("Browse..........................")
        hos_patient_id = self.env['hospital.appointment'].browse(1)
        print("Patient ID: ", hos_patient_id.patient_id)
        print("Patient Name: ", hos_patient_id.patient_id.name)
        print("Patient Age: ", hos_patient_id.patient_id.age)
        print("Patient Gender: ", hos_patient_id.patient_id.gender)
        print("Appointment Date & time: ", hos_patient_id.appointment_date)
        print("Booking Date: ", hos_patient_id.booking_date)


        search_patient_ids = self.env['hospital.patient'].search([('age', '=', 30),('gender', '=', 'male')])
        # print("Search Patient ID: ", search_patient_id)
        print("..................Search Resluts self model(Male)..................")
        for item in search_patient_ids:
            print("Name: ", item.name, "Age: ", item.age, "Gender:", item.gender)
        print("...................................................................")
        
        # EmpOBJ = self.env['hospital.appointment']
        # search_patient_id_2 = EmpOBJ.search([('booking_date', '=', '11/08/2023')]) # maybe error
        # print("class stored......diff model")
        # for item in search_patient_id_2:
        #     print("1")
        #     print("ID: ", item.patient_id.name, "Datetime: ", item.appointment_date, "Date:", item.booking_date)

        EmpOBJ = self.env['hospital.patient']
        search_patient_ids2 = EmpOBJ.search(['&', '&', '|', ('age', '=', 25), ('age', '=', 30), ('gender', '=', 'female'), '&', ('paid', '=', True), ('bill', '>', 10000)])
        print("......................Search Result for female.....................")
        for item in search_patient_ids2:
            print("Name: ", item.name, "Age: ", item.age, "Gender:", item.gender)
        print("...................................................................")

        abc = search_patient_ids.mapped('name')
        print("abc...list of all name value", abc)

        # raise UserWarning()
        # raise UserError("Hello")
        # raise UserError(abc)                  # Mr. Abul,Mr. Babul (Odoo),Mr. Kabul
        # raise UserError(search_patient_ids)   # hospital.patient(1, 2, 3)
        # raise UserError(search_patient_ids2)    # hospital.patient(8, 9)


        # ASC DESC order limit, 2nd highest, 3rd highest
        # search_read, search_count - similar to browse, search
        # search_read kono object return kore na. list of dictionary return kore. each dict ekekta record ke represent korbe. json structure e sajano thakbe.
        # view chara object create kora - create ke call dile(dict pass kore) object return korbe. ei object ke diye write function call dite hobe.
        # exception(raise UserError) --> obj create korechilam age but db te paoya jabe na cz rollback hoye jabe.
        # create action in python file --> xml er record id hocche xml er id. python file e action er kono id thakbe na. action ta je class er sei class er id.
        # dynamic action --> view e button e click korle button er function e jodi action define kora thake tahole click korlei oi action e chole jabe
        # form e ekta field e model_name user input dibe then button e click korbe. py file e model_name e self.field_name e model_name ta paoya jabe. eta py file e action e bosiye dibo model_name er value hisebe.
        # res_id --> ekta result chacchi so tree view er drkr nai. only form view dekhabe.
        # default --> model e default value rakhle form load korar time e default value auto fill up hoye thakbe but py file theke object create korte chaile ekhane kono default value thakbe na.
        # context e dictionary jabe(both py and xml) --> context er vitore dictionary thakbe. tar vitore default_fieldname variable e default value dite hobe.
        # context is used --> temporary purpose e value passing er jonne



        search_patient_filter_ids = self.env['hospital.patient'].search([('age', '=', 30),('gender', '=', 'male')], limit=2, order='name') # ASC, DESC
        print("..................Search Resluts self model(Male) with filter..................")
        for item in search_patient_filter_ids:
            print("Name: ", item.name, "Age: ", item.age, "Gender:", item.gender)
        print("...................................................................")

        search_read_dicts = EmpOBJ.search_read([('age', '=', 30),('gender', '=', 'male')])
        print("......................Search Result for Search Read.....................")
        for item in search_read_dicts:
            print(item)
        # print(search_read_dicts[0])
        print("...................................................................")

        search_count = EmpOBJ.search_count([('age', '=', 30),('gender', '=', 'male')])
        print("......................Search Result for Search Count.....................")
        print(search_count)
        print("...................................................................")

        # emp_id = self.env['hospital.patient'].create({'name' : '1', 'age' : 30})
        # emp_id.write({'name' : '12345', 'age' : 35})

        # return {'name' : 'Patient',
        #         'type' : 'ir.actions.act_window',
        #         'res_model' : 'hospital.patient',
        #         'view_mode' : 'tree,form'
        # }
        return {'name' : 'Patient',
                'type' : 'ir.actions.act_window',
                'res_model' : self.model_name,
                'view_mode' : 'tree,form',
                # 'target' : 'new',
                'target' : 'current',
                # 'target' : 'main',
                'context' : {'default_email' : 'example@gmail.com', 'val' : 'context value'},
                'domain' : [('gender', '=', 'female')]
        }
        #     <record id="action_hospital_patient" model="ir.actions.act_window">
        #     <field name="name">Patient</field>
        #     <field name="type">ir.actions.act_window</field>
        #     <field name="res_model">hospital.patient</field>
        #     <!-- <field name="view_mode">tree,kanban,form,calendar,pivot,graph,activity</field> -->
        #     <field name="view_mode">tree,form</field>
        #     <field name="context">{}</field>
        #     <field name="help" type="html">
        #         <p class="o_view_nocontent_smiling_face">
        #             Create a patient details
        #         </p>
        #     </field>
        # </record>