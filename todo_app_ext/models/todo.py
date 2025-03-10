from odoo import models, fields, api, _
from datetime import date

class Todo(models.Model):
    _name = 'todo_app_ext.todo.followups'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Todo Follow-ups"
    _order = "sequence asc, id desc"

    sequence = fields.Integer("Sequence", default=1, help="Use to order the List", tracking=True)
    name = fields.Char(string="Name", required=True, tracking=True)
    date_deadline = fields.Date("Deadline", tracking=True)
    date_completed = fields.Date('Date Completed', default=fields.Date.context_today)
    assigned_to = fields.Many2one('res.users', string="Assigned To", tracking=True)

    # # Method to open a new form pre-filled without saving
    # def action_open_form_pre_filled(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': "New Todo Follow-up",
    #         'res_model': 'todo_app_ext.todo.followups',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'target': 'new',  # Opens in the same window
    #         'context': {
    #             'default_name': 'New Task',
    #             'default_date_deadline': fields.Date.context_today(self),
    #             'default_assigned_to': self.env.user.id,  # Assign current user by default
    #         }
    #     }

    # # Method to create a record and redirect to its form view
    # def action_create_and_open(self):
    #     new_record = self.create({
    #         'name': 'New Task',
    #         'date_deadline': fields.Date.context_today(self),
    #         'assigned_to': self.env.user.id
    #     })

    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': "Todo Follow-up",
    #         'res_model': 'todo_app_ext.todo.followups',
    #         'res_id': new_record.id, 
    #         'view_mode': 'form',
    #         'target': 'current',
    #     }
