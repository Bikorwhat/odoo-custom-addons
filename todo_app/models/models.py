# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_, Command
from datetime import timedelta

from random import randint

from odoo.tools.convert import datetime

class TodoApp(models.Model):
    _name = 'todo_app.todo_app'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'This is an app where you can manage your TODO list'
    _order = "sequence asc, id desc"
    
    # @api.model
    # def default_get(self, fields):
    #     result = super(TodoRemark, self).default_get(fields)
    #     print(self._context)
    #     return result

    sequence = fields.Integer("Sequence", default=1, help="Use to order the List",tracking=True)
    name = fields.Char(string="Name", required=True,tracking=True)
    description = fields.Text("Brief Description",tracking=True)
    description_html = fields.Html("Full Description",tracking=True)
    helpdesk_ticket_id = fields.Many2one(
        'helpdesk_systems.helpdesk_systems', 
        string="Related Helpdesk Ticket"
    )
    date_deadline = fields.Date("Deadline",tracking=True)
    active = fields.Boolean('Active', default=True)
    category_id = fields.Many2one("todo_app.todo_category", string="Category", ondelete="set null",tracking=True)
    is_complete = fields.Boolean("Is Complete", compute="_compute_is_complete", store=True)
    user_id = fields.Many2one('res.users', string="Assigned To" ,tracking=True)
    manager_id = fields.Many2one('res.users', string="Manager", tracking=True)
    task_ids = fields.One2many('todo_app.todo_task', 'todo_app_id', string="Tasks")
    progress = fields.Float(string="Progress (%)", compute="_compute_is_complete", store=True,tracking=True)
    stage_id = fields.Many2one('todo_app.stage', string='Stages', group_expand='_read_group_stage_id', tracking=True)
    template_id = fields.Many2one('todo_app.template',string='Templates')
    tag_ids = fields.Many2many(
        'todo_app.tag', 'todo_app_todo_todo_tag_rel' , column1='todo_id',column2='tag_id',string='Tags',tracking=True)
    total_tasks = fields.Integer(
        string="Total Tasks",
        compute="_compute_total_tasks",
        store=True,
    )
    short_description = fields.Char(
        string="Short Description",
        compute="_compute_short_description",
        store=True,
    )
    states = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled',"Cancelled")
    ], string="State", default='draft',tracking=True)
    
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Todo name already exists!"),
    ]
    @api.model
    def send_deadline_notifications(self):
        today = datetime.now().date()
        notification_days = int(
            self.env['ir.config_parameter'].sudo().get_param(
                'todo_app.notification_days_before_deadline', default=0
            )
        )
        if notification_days > 0:
            deadline_date = today + timedelta(days=notification_days)
            tasks = self.search([
                ('date_deadline', '=', deadline_date),
                ('states', '!=', 'completed')
            ])
            
            for task in tasks:
                if task.user_id and task.user_id.partner_id:
                    message = f"Task '{task.name}' is due in {notification_days} days."
                    task.message_post(
                        body=message,
                        partner_ids=[task.user_id.partner_id.id]  
                    )
    
    @api.depends('task_ids')
    def _compute_total_tasks(self):
        for rec in self:
            rec.total_tasks = len(rec.task_ids)

    @api.depends('task_ids', 'task_ids.is_completed')
    def _compute_is_complete(self):
        for rec in self:
            rec.is_complete = all(rec.task_ids.mapped("is_completed"))
            rec.progress = (len(rec.task_ids.filtered("is_completed")) / len(rec.task_ids) * 100) if len(rec.task_ids) > 0 else 0
     
    # def action_todo_completed(self):
    #     self.ensure_one()
    #     self.write({
    #          'states':'completed'
    #     })
         
            
    def action_send_to_assigned(self):
        self.write({
            'states':'assigned'  
        })
    def action_send_to_in_progress(self):
        self.write({
            'states':'in_progress'  
        })
    def action_send_to_completed(self):
        self.write({
            'states':'completed'  
        })
    def action_send_to_cancelled(self):
        self.write({
            'states':'cancelled'  
        })
    def action_send_to_draft(self):
        print(self._context)
        self.write({
            'states':'draft'  
        })
    @api.model
    def create(self,vals):
        return super(TodoApp,self).create(vals)
    
    def write(self,vals):
        # print("Updating a todo")
        # print('Write method....')
        # TodoTask = self.env['todo_app.todo.task']
        # tasks = TodoTask.search([])
        # print('Tasks, tasks:', tasks)
        # todo_category_sales = self.env.ref('todo_add.todo_category_1')
        return super(TodoApp,self).write(vals)
    
    def unlink(self):
        return super(TodoApp,self).unlink()
    
    @api.onchange('date_deadline')
    def onchange_date_deadline(self):
        today = fields.Date.today()
        if self.date_deadline and self.date_deadline < today:
            warning = {
                'title':'Validation Error',
                'message':"Date deadline cannot be in the past"
            }
            return {'warning':warning}
    
    @api.depends('description')
    def _compute_short_description(self):
        for rec in self:
            if rec.description:
                rec.short_description = str(rec.description)[0:30]
            else:
                rec.short_description = ""
                
    @api.onchange('template_id')
    def onchange_template(self):
        if not self.template_id:
            return
        
        self.task_ids = [Command.clear()]
        sequence = 1
        tasks = self.template_id.task_ids
        tasks_data = []
        for task in tasks:
            tasks_data.append(
                Command.create({
                        'sequence': sequence,
                        'name': task.name,
                        'description': task.description,
                        'date_deadline': fields.Date.today() + timedelta(days=task.due_days)
                })
            )
            sequence +=1
        self.task_ids = tasks_data
        

    
    @api.model
    def _read_group_stage_id(self, records, domain, order=None):
        return records.search([])
    
    def open_email_composer(self):  
        
        template_id = self.env.ref('todo_app.todo_app_template').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'view_id': False,
            'target': 'new',
            'context': {
                'default_model': 'todo_app.todo_app',
                'default_res_ids': self.ids,
                'default_template_id': template_id,
                'default_use_template': True,
                'default_composition_mode': 'comment',
                'custom_layout': 'mail.mail_notification_layout_with_responsible_signature',
            },
        }
    def action_send_email(self):
        template = self.env.ref('todo_app.todo_app_template')
        template.send_mail(self.id,force_send=True)               

    
class TodoCategory(models.Model):
    _name = "todo_app.todo_category"
    _description = "Todo Category"
    _rec_name = "title"

    title = fields.Char("Title", required=True)
    description = fields.Text("Description")
    
    _sql_constraints = [
        ('name_uniq', 'unique (title)', "Category already exists!"),
    ]

class TodoTask(models.Model):
    _name = 'todo_app.todo_task'
    _description = 'This model stores individual tasks for a TodoApp'
    _order = "sequence asc, id desc"
    _rec_name = "name"

    sequence = fields.Integer("Sequence", default=1, help="Use to order the List")
    name = fields.Char(string="Task Name", required=True)
    description = fields.Text(string="Task Description")
    date_deadline = fields.Date("Task Deadline")
    is_completed = fields.Boolean("Task Complete")
    user_id = fields.Many2one('res.users', string="Assigned To", ondelete="set null")
    todo_app_id = fields.Many2one('todo_app.todo_app', string="Todo", ondelete='cascade')
    remarks = fields.Text("Remarks")
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Task  name already exists!"),
    ]

    def action_mark_completed(self,remarks=None):
        self.is_completed = True
        self.remarks = remarks
    
    from odoo import models, fields, api, _

class TodoTask(models.Model):
    _name = 'todo_app.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Todo Task"

    name = fields.Char("Task Name", required=True, tracking=True)
    is_completed = fields.Boolean("Completed", default=False, tracking=True)
    remarks = fields.Text("Remarks")
    assigned_to = fields.Many2one('res.users', string="Assigned To", tracking=True)
    date_deadline = fields.Date("Deadline", tracking=True)
    
    


class TodoAppTag(models.Model):
    _name = "todo_app.tag"
    _description = "Todo Tag"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color', default=_get_default_color)
    # color = fields.Integer('Color', default=lambda self: self.get_default_color())
    
    

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]
    
class TodoStage(models.Model):
    _name = 'todo_app.stage'
    _description = 'Task Stage'

    name = fields.Char(string="Stage Name", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    fold = fields.Boolean('Folded in Pipeline',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    
    @api.model_create_multi
    def create(self, valslist):
        res =  super(TodoStage, self).create(valslist)
        print("stage created",res)
        return res
    
    @api.model
    def create(self, vals):
        res = super(TodoStage, self).create(vals)
        # Check if the stage should be folded or not based on whether it has TODOs
        todo_apps = self.env['todo_app.todo_app'].search([('stage_id', '=', res.id)])
        if not todo_apps:
            res.fold = False  # Ensure that even empty stages are visible (not folded)
        return res
    
    
    
class Template(models.Model):
    _name = 'todo_app.template'
    _rec_name = 'name'
    _description = 'Task Task Template'
    _order = 'id desc'

    name = fields.Char(string="Stage Name", required=True)
    description = fields.Text('Description')
    task_ids = fields.One2many('todo_app.template_task', 'template_id', string="Tasks")
    
    
    
    
class TemplateTask(models.Model):
    _name = 'todo_app.template_task'
    _description = 'Todo Task Template Tasks'
    _rec_name = "name"
    _order = 'id desc'

    name = fields.Char(string="Task Name", required=True)
    description = fields.Text(string="Task Description")
    template_id = fields.Many2one('todo_app.template', string="Template", required=True)
    sequence = fields.Integer('Sequence',default=1)
    due_days = fields.Integer("Due in",defaullt=5) 
        