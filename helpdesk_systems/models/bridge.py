# from odoo import models, fields, api, _

# class HelpdeskTodoBridge(models.Model):
#     _name = 'helpdesk.todo.bridge'  # Define the model's technical name
#     _description = 'Helpdesk Todo Bridge'  # Optional: Add a description for the model
    
#     todo_task_id = fields.Many2one('todo_app.todo_app', string="Linked ToDo Task")

#     def action_create_todo_from_ticket(self):
#         for ticket in self:
#             if ticket.todo_task_id:
#                 continue  # Avoid duplicate task creation

#             # Fetch all existing tag names in ToDo App for efficiency
#             existing_tags = self.env['todo_app.tag'].search([]).mapped('name')

#             tag_ids = []
#             for tag in ticket.tags:
#                 if tag.name in existing_tags:
#                     todo_tag = self.env['todo_app.tag'].search([('name', '=', tag.name)], limit=1)
#                 else:
#                     todo_tag = self.env['todo_app.tag'].create({'name': tag.name})
#                     existing_tags.append(tag.name)  # Add to the list to avoid rechecking
                
#                 tag_ids.append(todo_tag.id)

#             # Format tag_ids for Many2many
#             tag_ids = [(6, 0, tag_ids)] if tag_ids else []

#             # Create ToDo Task
#             todo_task = self.env['todo_app.todo_app'].create({
#                 'name': ticket.name,
#                 'description': ticket.query or ticket.description,
#                 'helpdesk_ticket_id': ticket.id,
#                 'tags': tag_ids,  # Assign tags
#                 'assigned_user_id': ticket.assigned_user_id.id,
#                 'deadline': ticket.reported_date,
#             })

#             # Link created ToDo task to Helpdesk ticket
#             ticket.todo_task_id = todo_task.id
