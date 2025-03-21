from odoo import SUPERUSER_ID, api, models, fields
from odoo.exceptions import ValidationError
from odoo.osv.expression import date
from odoo.tools import _
    
class HelpdeskSystems(models.Model):
    _name = 'helpdesk_systems.helpdesk_systems'
    _description = 'Helpdesk System'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # name = fields.Char(string="Name", required=True, tracking=True)
    name = fields.Char(
        string="Name",
        required=True, copy=False, readonly=False,
        index='trigram',
        default=lambda self: ('New'))
    # company_id = fields.Many2one(
    #     comodel_name='res.company',
    #     required=True, index=True,
    #     default=lambda self: self.env.company)
    
   


    email = fields.Char(string="Email", tracking=True)
    number = fields.Char(string="Number", tracking=True)
    query = fields.Text("Query", tracking=True,required=True)
    description = fields.Text("Brief Description", tracking=True)
    reported_date = fields.Date("Reported Date", tracking=True)
    @api.constrains('reported_date')
    def _limitDate(self):
        for record in self:
            if record.reported_date and record.reported_date > fields.Date.today():
                raise ValidationError("Date can't be set in the future.")
   
    type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External')],
         string="Type", tracking=True,required=True)
    reported_by = fields.Many2one(
    'res.users', 
    string="Reported By", 
    tracking=True, 
    required=True, 
    default=lambda self: self.env.user
)
    
    team_id = fields.Many2one('helpdesk.team', string="Assigned Team", tracking=True)
      # Add the Many2one field for category
    category_id = fields.Many2one(
        'helpdesk_systems.helpdesk_category', 
        string="Category", 
        tracking=True
    )
    tags = fields.Many2many(
        'helpdesk_systems.tag', 
        'helpdesk_systems_helpdesk_systems_tag_rel', 
        'helpdesk_system_id', 
        'tag_id', 
        string='Tags'
    )
    assigned_team_leader = fields.Many2one('res.users', string="Assigned Team Leader")
     
    assigned_user_id = fields.Many2one(
        'res.users', string="Assigned To", tracking=True,
        domain="[('id', 'in', available_members)]"
    )
  
    available_members = fields.Many2many(
        'res.users', compute="_compute_available_members", store=False
    )

    @api.depends('team_id')
    def _compute_available_members(self):
        for ticket in self:
            if ticket.team_id:
                ticket.available_members = ticket.team_id.member_ids
            else:
                ticket.available_members = self.env['res.users'].search([])
    @api.onchange('team_id')
    def _onchange_team_id(self):
        for ticket in self:
            if ticket.team_id:
                # Update the team leader
                ticket.assigned_team_leader = ticket.team_id.leader_id
                # Only reset assigned_user_id if the current user is not in the new team's members
                if ticket.assigned_user_id and ticket.assigned_user_id not in ticket.team_id.member_ids:
                    ticket.assigned_user_id = False
            else:
                ticket.assigned_team_leader = False
                
    @api.onchange('assigned_user_id')
    def _onchange_assigned_user_id(self):
     for ticket in self:
        if ticket.assigned_user_id:
            # Find all teams the selected member belongs to
            teams = self.env['helpdesk.team'].search([('member_ids', 'in', ticket.assigned_user_id.ids)])
            
            if teams:
                # If no team is selected, assign the first team
                if not ticket.team_id or ticket.team_id not in teams:
                    ticket.team_id = teams[0]

                # Update the team leader based on the assigned team
                ticket.assigned_team_leader = ticket.team_id.leader_id


    @api.onchange('type')
    def _onchange_type(self):
      if self.type == 'internal':
        if not self.assigned_user_id:
            # If type is internal and no user is assigned, prompt user to assign a member
            raise ValidationError(_("Please assign a team member to this internal ticket."))
        
        if not self.team_id:
            # If type is internal and no team is assigned, prompt user to assign a team
            raise ValidationError(_("Please assign a team to this internal ticket."))

    # Define binary field for document upload
    document = fields.Binary("Upload Document")
    document_name = fields.Char("Document Name")
   
    
    stage_id = fields.Many2one(
    'helpdesk_system.stage', string="Stage",group_expand='_read_group_stage_id', tracking=True,
    default=lambda self: self.env['helpdesk_system.stage'].search([], order="sequence asc", limit=1))
    is_cancelled = fields.Boolean(string='Is Cancelled Stage', compute='_compute_is_cancelled')
    is_progress = fields.Boolean(string='Is In Progress Stage', compute='_compute_is_progress')
    is_draft = fields.Boolean(string='Is Draft Stage', compute='_compute_is_draft')
    stages_name = fields.Char(related="stage_id.name", store=True, string="Stage Name")

    @api.depends('stage_id')
    def _compute_is_cancelled(self):
     for rec in self:
        rec.is_cancelled = rec.stage_id == self.env.ref('helpdesk_systems.stage_cancelled')  # Correct ref for 'Cancelled'

    @api.depends('stage_id')
    def _compute_is_progress(self):
     for rec in self:
        rec.is_progress = rec.stage_id == self.env.ref('helpdesk_systems.stage_in_progress')  # Correct ref for 'In Progress'

    @api.depends('stage_id')
    def _compute_is_draft(self):
     for rec in self:
        rec.is_draft = rec.stage_id == self.env.ref('helpdesk_systems.stage_draft')  # Correct ref for 'Draft'

   
         
    
    @api.model
    def _read_group_stage_id(self, records, domain, order=None):
        return records.search([])
    remarks_ids = fields.One2many('helpdesk.remarks', 'helpdesk_ticket_id', string="Remarks")
    # @api.model
    # def _read_group_stage_ids(self, stages, domain, order):
    #     """Read all the stages and display them in the kanban view,
    #     even if they are empty"""
    #     stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
    #     return stages.browse(stage_ids)

    def action_open_stage_wizard(self):
        """ Opens the wizard to change the stage and add remarks """
        new_stage = self.stage_id  # Get the current stage of the helpdesk ticket

        next_stage = self.env['helpdesk_system.stage'].search([
            ('sequence', '>', new_stage.sequence)
        ], order="sequence asc", limit=1)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk_systems.stage_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_helpdesk_ticket_id': self.id,
                'default_stage_id': next_stage.id if next_stage else new_stage.id,
            }
        }


    def action_send_to_cancel(self):
        """ Set stage to 'Cancelled' """
        cancelled_stage = self.env['helpdesk_system.stage'].search([('name', '=', 'Cancelled')], limit=1)
        if cancelled_stage:
            self.stage_id = cancelled_stage
    
    def action_send_to_in_progress(self):
     """ Set stage to 'In Progress' """
     in_progress_stage = self.env['helpdesk_system.stage'].search([('name', '=', 'In Progress')], limit=1)
     if in_progress_stage:
        self.stage_id = in_progress_stage

    def action_send_to_completed(self):
     """ Set stage to 'Completed' """
     completed_stage = self.env['helpdesk_system.stage'].search([('name', '=', 'Completed')], limit=1)
     if completed_stage:
        self.stage_id = completed_stage

    def action_restore_ticket(self):
        """ Restores a cancelled ticket back to draft """
        draft_stage = self.env['helpdesk_system.stage'].search([('name', '=', 'Draft')], limit=1)
        if self.stage_id and self.stage_id.name == 'Cancelled' and draft_stage:
            self.stage_id = draft_stage
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', "New") == "New":
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'helpdesk_systems.helpdesk_systems') or ("New")
        """ Override create to send notification when ticket is created """
        ticket = super(HelpdeskSystems, self).create(vals_list)
         # Debugging: Print team leader ID when a team is assigned
        if ticket.team_id:
         print("Assigned Team Leader ID: ", ticket.team_id.leader_id.name)
       
        ticket._send_creation_notifications()

        ticket._send_assignment_notifications()
        return ticket

    def write(self, values):
        """ Override write to send notification when ticket is updated """
        result = super(HelpdeskSystems, self).write(values)
        if 'team_id' in values and self.team_id:
         print("Assigned Team Leader ID: ", self.team_id.leader_id.name)
    
        if 'assigned_user_id' in values:  # Check if assigned user was updated
            self._send_assignment_notifications()
        return result
    def _send_creation_notifications(self):
        """ Sends notifications to all team leaders and admins when a ticket is created """
        # Notify all team leaders
        team_leader_group = self.env.ref('helpdesk_systems.group_helpdesk_leader').sudo()  # Team leader group
        team_leaders = team_leader_group.users.sudo()
        team_leader_partner_ids = []

        # Check if the ticket is from a contact or non-contact user
        # Collect partner IDs of team leaders
        for leader in team_leaders:
            if leader.partner_id:
                team_leader_partner_ids.append(leader.partner_id.id)

        # Notify team leaders
        if team_leader_partner_ids:
            self.message_post(
                body=f"A new Help Desk ticket has been created from the portal: {self.name}",
                partner_ids=team_leader_partner_ids,
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

        # Notify admins (users in the 'Administrator' group)
        admin_group = self.env.ref('helpdesk_systems.group_helpdesk_admin').sudo()  # Admin group
        admins = admin_group.users.sudo()
        admin_partner_ids = []

        # Collect partner IDs of admins
        for admin in admins:
            if admin.partner_id:
                admin_partner_ids.append(admin.partner_id.id)

        # Notify admins
        if admin_partner_ids:
            self.message_post(
                body=f"A new Help Desk ticket has been created from the portal: {self.name}",
                partner_ids=admin_partner_ids,
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

    def _send_assignment_notifications(self):
        """ Sends notifications to assigned user and team leader """
        if not self.assigned_user_id:
            return  # If no assigned user, do nothing

        # Notify the assigned user
        self.message_post(
            body=_("%s, you have been assigned a new helpdesk ticket: %s") % (self.assigned_user_id.name, self.name),
            partner_ids=[self.assigned_user_id.partner_id.id]
        )

       # Notify the team leader
        if self.team_id and self.team_id.leader_id:
         leader_name = self.team_id.leader_id.name  # Get the team leader's name
        self.message_post(
            body=_("%s, your team has been assigned a new helpdesk ticket: %s" % (
                leader_name, self.name
            )),
            partner_ids=[self.team_id.leader_id.partner_id.id]
        )
     
class ResUsers(models.Model):
    _inherit = 'res.users'

    # Computed field to get the teams the user belongs to
    team_ids = fields.Many2many(
        'helpdesk.team',
        string="Teams",
        compute="_compute_team_ids",
        store=True,
    )

    @api.depends('groups_id')
    def _compute_team_ids(self):
        for user in self:
            # Find all teams where the user is either a leader or a member
            teams = self.env['helpdesk.team'].search([
                '|',
                ('leader_id', '=', user.id),
                ('member_ids', 'in', user.ids),
            ])
            user.team_ids = teams