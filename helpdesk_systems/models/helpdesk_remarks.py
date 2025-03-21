from odoo import SUPERUSER_ID, api, models, fields
from odoo.exceptions import ValidationError
from odoo.osv.expression import date

class HelpdeskRemarks(models.Model):
    _name = 'helpdesk.remarks'
    _description = 'Helpdesk Remarks'

    helpdesk_ticket_id = fields.Many2one('helpdesk_systems.helpdesk_systems', string="Helpdesk Ticket", ondelete='cascade')
    name = fields.Char("Ticket Name")
    team_id = fields.Many2one('helpdesk.team', string="Assigned Team")
    remarks = fields.Text("Remarks")
    document = fields.Binary("Upload Document")
    