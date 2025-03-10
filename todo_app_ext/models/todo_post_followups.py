from datetime import timedelta

from odoo import api, fields, models, Command
from odoo.exceptions import UserError, ValidationError
from random import randint


class todo_post_followups(models.Model):
    _inherit = 'todo_app.todo_app'

    def action_send_to_completed(self):
        super(todo_post_followups,self).action_send_to_completed()
        action = self.env["ir.actions.actions"]._for_xml_id("todo_app_ext.action_todo_followup")

        action['context'] = self._prepare_opportunity_todo_context()
        
        return action
        
    
    def _prepare_opportunity_todo_context(self):

        todo_context = {
                'default_name': self.name,
                'default_date_deadline': self.date_deadline,
                'default_date_completed': fields.Date.today(),
                'default_assigned_to': self.env.user.id,
        }
        return todo_context
