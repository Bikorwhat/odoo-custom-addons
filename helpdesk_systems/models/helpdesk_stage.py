from odoo import SUPERUSER_ID, api, models, fields
from odoo.exceptions import ValidationError
from odoo.osv.expression import date

class HelpdeskStage(models.Model):
    _name = 'helpdesk_system.stage'
    _description = 'Helpdesk Stage'
    
    name = fields.Char("Stage Name", required=True)
    sequence = fields.Integer("Sequence", default=1)
    _sql_constraints=[
        ('name_unique' , 'unique(name)', 'Stage Name must be unique'),
    ]
    