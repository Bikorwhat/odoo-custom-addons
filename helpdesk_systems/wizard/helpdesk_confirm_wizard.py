# from odoo import models, fields, api

# class HelpdeskConfirmWizard(models.TransientModel):
#     _name = 'helpdesk.confirm.wizard'
#     _description = 'Confirm Helpdesk Action'

#     helpdesk_ticket_id = fields.Many2one('helpdesk_systems.helpdesk_systems', string="Helpdesk Ticket")
    
#     def action_confirm(self):
#         """ Perform the original action after confirmation """
#         if self.helpdesk_ticket_id:
#             self.helpdesk_ticket_id.action_create_todo_from_ticket()
