import logging
from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools import _

_logger = logging.getLogger(__name__)

class HelpdeskTodoStage(models.Model):
    _inherit = 'todo_app.todo_app' 

    helpdesk_ticket_id = fields.Many2one('helpdesk_systems.helpdesk_systems', string="Related Helpdesk Ticket")

    def action_send_to_completed(self):
        _logger.debug(">>> action_send_to_completed called for task: %s (ID: %s)", self.name, self.id)
        res = super(HelpdeskTodoStage, self).action_send_to_completed()

        completed_stage = self.env['todo_app.stage'].search([('name', '=', 'Completed')], limit=1)
        if not completed_stage:
            _logger.error(">>> ERROR: The 'Completed' stage does not exist in todo_app.stage")
            raise ValidationError(_("The 'Completed' stage does not exist in todo_app.stage."))
        self.sudo().write({'stage_id': completed_stage.id})
        _logger.info(">>> Todo task '%s' (ID: %s) moved to 'Completed' stage.", self.name, self.id)

        if self.helpdesk_ticket_id:
            completed_stage_helpdesk = self.env['helpdesk_system.stage'].search([('name', '=', 'Completed')], limit=1)
            if completed_stage_helpdesk:
                self.helpdesk_ticket_id.write({'stage_id': completed_stage_helpdesk.id})
                _logger.debug(f"Helpdesk ticket {self.helpdesk_ticket_id.id} updated to 'Completed'.")
            else:
                _logger.warning("Helpdesk 'Completed' stage not found!")
        else:
            _logger.debug(f"No associated Helpdesk ticket found for Todo task {self.id}")
        
        return res

    def action_send_to_assigned(self):
        _logger.debug(">>> action_send_to_assigned called for task: %s (ID: %s)", self.name, self.id)
        res = super(HelpdeskTodoStage, self).action_send_to_assigned()

        in_progress_stage = self.env['todo_app.stage'].search([('name', '=', 'In Progress')], limit=1)
        if not in_progress_stage:
            _logger.error(">>> ERROR: The 'In Progress' stage does not exist in todo_app.stage")
            raise ValidationError(_("The 'In Progress' stage does not exist in todo_app.stage."))
        self.sudo().write({'stage_id': in_progress_stage.id})
        _logger.info(">>> Todo task '%s' (ID: %s) moved to 'In Progress' stage.", self.name, self.id)

        # Synchronize with Helpdesk "In Progress" stage
        if self.helpdesk_ticket_id:
            in_progress_stage_helpdesk = self.env['helpdesk_system.stage'].search([('name', '=', 'In Progress')], limit=1)
            if in_progress_stage_helpdesk:
                self.helpdesk_ticket_id.write({'stage_id': in_progress_stage_helpdesk.id})
                _logger.debug(f"Helpdesk ticket {self.helpdesk_ticket_id.id} updated to 'In Progress'.")
            else:
                _logger.warning("Helpdesk 'In Progress' stage not found!")
        else:
            _logger.debug(f"No associated Helpdesk ticket found for Todo task {self.id}")

        return res

    def action_send_to_in_progress(self):
        _logger.debug(">>> action_send_to_in_progress called for task: %s (ID: %s)", self.name, self.id)
        res = super(HelpdeskTodoStage, self).action_send_to_in_progress()

        in_progress_stage = self.env['todo_app.stage'].search([('name', '=', 'In Progress')], limit=1)
        if not in_progress_stage:
            _logger.error(">>> ERROR: The 'In Progress' stage does not exist in todo_app.stage")
            raise ValidationError(_("The 'In Progress' stage does not exist in todo_app.stage."))
        self.sudo().write({'stage_id': in_progress_stage.id})
        _logger.info(">>> Todo task '%s' (ID: %s) moved to 'In Progress' stage.", self.name, self.id)

        # Synchronize with Helpdesk "In Progress" stage
        if self.helpdesk_ticket_id:
            in_progress_stage_helpdesk = self.env['helpdesk_system.stage'].search([('name', '=', 'In Progress')], limit=1)
            if in_progress_stage_helpdesk:
                self.helpdesk_ticket_id.write({'stage_id': in_progress_stage_helpdesk.id})
                _logger.debug(f"Helpdesk ticket {self.helpdesk_ticket_id.id} updated to 'In Progress'.")
            else:
                _logger.warning("Helpdesk 'In Progress' stage not found!")
        else:
            _logger.debug(f"No associated Helpdesk ticket found for Todo task {self.id}")

        return res
        