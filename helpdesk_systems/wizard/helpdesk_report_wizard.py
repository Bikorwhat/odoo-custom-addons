from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HelpdeskReportWizard(models.TransientModel):
    _name = 'helpdesk.report.wizard'
    _description = 'Helpdesk Report Wizard'

    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    
    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        if self.date_from > self.date_to:
            raise ValidationError("Date From cannot be greater than Date To")
    
    report_type = fields.Selection([
        ('brief_data', 'Brief Data'),
        ('team_progress', 'Team Progress Data')
    ], string="Report Type", required=True, default='brief_data')

    def get_helpdesk_data(self):
        """Fetch helpdesk tickets within the selected date range."""
        return self.env['helpdesk_systems.helpdesk_systems'].search([
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to)
        ])

    def generate_report(self):
        """Generates the PDF Report with selected date range"""
        if self.report_type == 'brief_data':
            return self.env.ref('helpdesk_systems.action_helpdesk_report_pdf').report_action(self)
        elif self.report_type == 'team_progress':
            return self.env.ref('helpdesk_systems.action_helpdesk_team_progress_report_pdf').report_action(self)
    
    def get_team_progress_data(self):
     teams = self.env['helpdesk.team'].search([])  
     team_data = []
     for team in teams:
        tickets = self.env['helpdesk_systems.helpdesk_systems'].search([
            ('team_id', '=', team.id),
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to)
        ])
        team_data.append({
            'name': team.name,
            'leader_id': team.leader_id,
            'total_tickets': len(tickets),
             'draft_tickets': len(tickets.filtered(lambda t: t.stage_id.name == 'Draft')),
            'completed_tickets': len(tickets.filtered(lambda t: t.stage_id.name == 'Completed')),
            'in_progress_tickets': len(tickets.filtered(lambda t: t.stage_id.name == 'In Progress')),
            'cancelled_tickets': len(tickets.filtered(lambda t: t.stage_id.name == 'Cancelled')),
        })
     return team_data