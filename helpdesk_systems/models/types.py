from odoo import models, fields

class HelpdeskTypes(models.Model):
    _name = 'helpdesk_systems.helpdesk_types'
    _description = 'Helpdesk Types'

    # Fields for Helpdesk Types model
    name = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External'),
    ], string='Type', required=True)
    
    description = fields.Text(string='Description')
