import logging
from odoo import exceptions, models, fields, api

class HelpdeskBridge(models.Model):
    _inherit = ['helpdesk_systems.helpdesk_systems',]
    crm_lead_id = fields.Many2one('crm.lead', string="CRM Lead")
    todo_id = fields.Many2one('todo_app.todo_app', string="Todo App id")
    
    def action_create_crm_lead(self):
        """ Open the CRM wizard to create a lead """
        self.ensure_one()  # Ensure only one record is processed
        return {
            'name': 'Create CRM Lead',
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk_bridge.crm_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': self.name,
                'default_email': self.email,
                'default_phone': self.number,
                'default_ticket_id': self.id,  # Pass the ticket ID to the wizard
            },
        }

    def action_create_todo_from_ticket(self):
        for ticket in self:
          
            tag_ids = []
            for tag in ticket.tags:
               
                todo_tag = self.env['todo_app.tag'].search([('name', '=', tag.name)], limit=1)
                
                # If tag does not exist, create it
                if not todo_tag:
                    todo_tag = self.env['todo_app.tag'].create({'name': tag.name})
                
                tag_ids.append(todo_tag.id)

          
            # tag_ids = [(6, 0, tag_ids)] if tag_ids else []

            # Ensure the category exists in the todo_app.todo_category model
            todo_category = self.env['todo_app.todo_category'].search([('title', '=', ticket.category_id.name)], limit=1)
            
            # If category does not exist, create it
            if not todo_category and ticket.category_id:
                todo_category = self.env['todo_app.todo_category'].create({
                    'title': ticket.category_id.name,
                    'description': ticket.category_id.description or '',  # Copy description if needed
                })

            team_leader_id = ticket.team_id.leader_id.id
          
            return {
            'name': 'Confirm Todo',
            'type': 'ir.actions.act_window',
            'res_model': 'todo.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': ticket.name,
                'default_description': ticket.query,
                'default_description_html': ticket.description,
                # 'default_user_id': team_leader_id,
                'default_user_id': ticket.assigned_user_id.id if ticket.assigned_user_id else False,

                'default_category_id': todo_category.id if todo_category else False,
                'default_tag_ids': [(6, 0, tag_ids)],
                'default_helpdesk_ticket_id': ticket.id,
            }
        }