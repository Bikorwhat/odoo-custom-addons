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
    helpdesk_ticket_id = fields.Many2one('helpdesk_systems.helpdesk_systems', string="Related Helpdesk Ticket")

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
