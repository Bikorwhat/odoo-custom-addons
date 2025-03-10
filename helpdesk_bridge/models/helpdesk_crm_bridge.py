import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def write(self, values):
        """ Override the write method to synchronize the stage between CRM and Helpdesk """
        _logger.debug(f"Write method triggered for CRM Lead with values: {values}")

        result = super(CrmLead, self).write(values)

        for lead in self:
            new_stage = self.env['crm.stage'].browse(values.get('stage_id', False))
            is_lost = values.get('active', lead.active) == False  

            if new_stage and new_stage.exists():
                _logger.debug(f"CRM Lead {lead.id} new stage: {new_stage.name}")

            if (new_stage and new_stage.name == 'Won') or is_lost:
                status = 'Lost' if is_lost else new_stage.name
                _logger.debug(f"CRM Lead {lead.id} has stage {status}, synchronizing Helpdesk ticket...")

                helpdesk_ticket = self.env['helpdesk_systems.helpdesk_systems'].search([
                    ('crm_lead_id', '=', lead.id)
                ], limit=1)

                if helpdesk_ticket:
                    completed_stage = self.env['helpdesk_system.stage'].search([('name', '=', 'Completed')], limit=1)
                    if completed_stage:
                        helpdesk_ticket.write({'stage_id': completed_stage.id})
                        _logger.debug(f"Helpdesk ticket {helpdesk_ticket.id} updated to 'Completed'.")
                    else:
                        _logger.warning("Helpdesk 'Completed' stage not found!")
                else:
                    _logger.warning(f"No associated Helpdesk ticket found for CRM Lead {lead.id}")
            else:
                # If the CRM stage is neither 'Won' nor 'Lost', set Helpdesk ticket to 'In Progress'
                _logger.debug(f"CRM Lead {lead.id} is in an active stage, setting Helpdesk ticket to 'In Progress'.")

                helpdesk_ticket = self.env['helpdesk_systems.helpdesk_systems'].search([
                    ('crm_lead_id', '=', lead.id)
                ], limit=1)

                if helpdesk_ticket:
                    in_progress_stage = self.env['helpdesk_system.stage'].search([('name', '=', 'In Progress')], limit=1)
                    if in_progress_stage:
                        helpdesk_ticket.write({'stage_id': in_progress_stage.id})
                        _logger.debug(f"Helpdesk ticket {helpdesk_ticket.id} updated to 'In Progress'.")
                    else:
                        _logger.warning("Helpdesk 'In Progress' stage not found!")
                else:
                    _logger.warning(f"No associated Helpdesk ticket found for CRM Lead {lead.id}")
        return result
