from odoo import models, fields

class HelpdeskTag(models.Model):
    _name = 'helpdesk_systems.tag'
    _description = 'Helpdesk Tag'
    _order = 'name'

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color Index")  # Used for color picker
