from odoo import fields,api,models

class RecordTag(models.Model):
    _name = 'record.tag'
    _description = "Information of some tags"
    
    name = fields.Char("Name")
    description = fields.Char("Description")
    select_model = fields.Many2one('ir.model',string="Models")
    
    def show_data(self):
        return {
            'name' : 'All Records of the model',
            'res_model' : self.select_model.model,
            'view_mode' : 'tree',
            'type': 'ir.actions.act_window',
            'target':'new'
        }