from odoo import models, fields, api

class TodoWizard(models.TransientModel):
    _name = 'todo.wizard'
    _description = 'Confirm and Send Todo'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    description_html = fields.Html(string="Detailed Description")
    category_id = fields.Many2one('todo_app.todo_category', string="Category")
    tag_ids = fields.Many2many('todo_app.tag', string="Tags")
    user_id = fields.Many2one('res.users', string="Assigned User")
    leader_id = fields.Many2one('res.users', string="Leader" ,tracking=True)
    helpdesk_ticket_id = fields.Many2one('helpdesk_systems.helpdesk_systems', string="Related Helpdesk Ticket")
    todo_id = fields.Many2one('todo_app.todo_app', string="Linked To-Do Task")
    
    @api.model
    def create(self, vals):
        record = super(TodoWizard, self).create(vals)
        
        if record.leader_id:
            record._assign_todo_manager_role(record.leader_id)
        if record.user_id:
            record._assign_todo_user_role(record.user_id)
            
        return record

    def write(self, vals):
        res = super(TodoWizard, self).write(vals)
        
        if 'leader_id' in vals:
            for wizard in self:
                wizard._assign_todo_manager_role(wizard.leader_id)
        if 'user_id' in vals:
            for wizard in self:
                wizard._assign_todo_user_role(wizard.user_id)        

        return res

    def _assign_todo_manager_role(self, user):
        if user:
            todo_manager_group = self.env.ref('todo_app.group_todo_manager', raise_if_not_found=False)
            if todo_manager_group:
                user.write({
                    'groups_id': [(4, todo_manager_group.id)]
                })
    def _assign_todo_user_role(self, user):
        if user:
            todo_user_group = self.env.ref('todo_app.group_todo_user', raise_if_not_found=False)
            if todo_user_group:
                user.write({
                    'groups_id': [(4, todo_user_group.id)]
                })
    def action_confirm_create_todo(self):
        """ Create Todo in todo_app.todo_app when the wizard is confirmed """
        self.env['todo_app.todo_app'].create({
            'name': self.name,
            'description': self.description,
            'description_html': self.description_html,
            'user_id': self.user_id.id,
            'category_id': self.category_id.id if self.category_id else False,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
            'stage_id': 1,
            'helpdesk_ticket_id': self.helpdesk_ticket_id.id,
        })
