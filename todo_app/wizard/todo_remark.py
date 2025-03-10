# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo .exceptions import UserError

class TodoRemark(models.TransientModel):
    _name = 'todo_remark.wizard'
    _description = 'Give remark for the completed task'

    
    # @api.model
    # def default_get(self, fields):
    #     result = super(TodoRemark, self).default_get(fields)
    #     task_id = self._context.get('active_id')
    #     task_model = self._context.get('active_model')
    #     task = self.env[task_model].browse(task_id)
    #     if not task:
    #         raise UserError('Task is not selected')
    #     result['task_id'] = task_id
    #     return result
    
    user_id = fields.Many2one('res.users','Responsible')
    task_id = fields.Many2one('todo_app.todo_task', string="Todo Task", required=True )
    remarks = fields.Text("Remarks" , required=True)


    def action_confirm(self):
        """Mark task as complete"""
        self.ensure_one()
        if not self.task_id:
            raise UserError('Task is not selected')
        self.task_id.action_mark_completed(remarks=self.remarks)
        return True


