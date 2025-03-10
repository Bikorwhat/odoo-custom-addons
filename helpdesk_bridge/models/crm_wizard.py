import logging
from odoo import models, fields, api

class CrmWizard(models.TransientModel):
    _name = 'helpdesk_bridge.crm_wizard'
    _description = 'CRM Lead Creation Wizard'

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone", required=True)
    ticket_id = fields.Many2one('helpdesk_systems.helpdesk_systems', string="Ticket")  # Add ticket_id field

    def action_confirm_crm_lead(self):
        """ Create a CRM lead from the wizard and link it to the ticket """
        self.ensure_one()  # Ensure only one record is processed
        _logger = logging.getLogger(__name__)

        # Prepare CRM lead values
        crm_vals = {
            'name': self.name,
            'email_from': self.email,
            'phone': self.phone,
        }

        # Search for an existing partner
        existing_partner = self.env['res.partner'].search([
            ('email', '=', self.email),
            '|',
            ('phone', '=', self.phone), 
            ('mobile', '=', self.phone)
        ], limit=1)

        if existing_partner:
            crm_vals['contact_name'] = existing_partner.name
            crm_vals['email_from'] = existing_partner.email
            crm_vals['phone'] = existing_partner.phone  # Set the phone field if available
            crm_vals['mobile'] = existing_partner.mobile  # Set the mobile field if available
            _logger.info(f"Existing partner found: {existing_partner.name}")
        else:
            _logger.info(f"No existing partner found, using wizard info")
            

        # Create the CRM lead
        _logger.info(f"CRM Values: {crm_vals}")
        crm_lead = self.env['crm.lead'].sudo().create(crm_vals)
        _logger.info(f"CRM Lead created successfully.")

        # Link the CRM lead to the ticket
        if self.ticket_id:
            self.ticket_id.crm_lead_id = crm_lead.id
            _logger.info(f"Linked CRM Lead ID: {crm_lead.id} to Ticket ID: {self.ticket_id.id}")

        return {
             'type': 'ir.actions.act_window_close', 
        }