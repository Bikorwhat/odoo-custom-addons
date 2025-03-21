from odoo import api, models, fields

class HelpdeskTeam(models.Model):
    _name = 'helpdesk.team' 
    _description = 'Helpdesk Team'

    name = fields.Char("Team Name", required=True)
    leader_id = fields.Many2one('res.users', string="Team Leader", required=True)
    member_ids = fields.Many2many('res.users', string="Team Members")
    
    @api.constrains('leader_id')
    def _check_leader_is_member(self):
        for team in self:
            if team.leader_id and team.leader_id not in team.member_ids:
                raise models.ValidationError("The team leader must be a member of the team.")
    @api.model
    def create(self, values):
        # Create the team first
        team = super(HelpdeskTeam, self).create(values)

        # Ensure the leader and members are added to the group
        self._add_users_to_group(team)

        return team

    def _add_users_to_group(self, team):
        # Define the groups (or create new ones if needed)
        team_leader_group = self.env.ref('helpdesk_systems.group_helpdesk_leader', raise_if_not_found=False)
        team_member_group = self.env.ref('helpdesk_systems.group_helpdesk_member', raise_if_not_found=False)

        if team_leader_group:
            team_leader_group.users = [(4, team.leader_id.id)]  # Add the team leader to the leader group

        if team_member_group:
            for member in team.member_ids:
                team_member_group.users = [(4, member.id)]  # Add each team member to the member group
