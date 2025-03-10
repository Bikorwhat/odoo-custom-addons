from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import logging

class HelpdeskCustomerPortal(CustomerPortal):

    @http.route(['/helpdesk/submit'], type='http', auth="public", website=True)
    def helpdesk_submit_ticket(self, **post):
        """Render the submit ticket form"""
        return request.render("helpdesk_systems.portal_submit_ticket", {})

    @http.route(['/helpdesk/submit/process'], type='http', auth="public", website=True, methods=['POST'], csrf=True)
    def helpdesk_submit_process(self, **post):
        """Process the ticket submission"""
    
        vals = {
            'name': post.get('name', ''),
            'query': post.get('query', ''),
            'email':post.get('email', ''),
            'number': post.get('number', ''),
            'type': post.get('type', 'external'),
            'description': post.get('description', ''),
            'type': post.get('type', 'external'),
  # Use user ID or False if no match
        }
      

        # Create the helpdesk ticket
        ticket = request.env['helpdesk_systems.helpdesk_systems'].sudo().create(vals)

        # Render a success page with a message
        return request.render("helpdesk_systems.ticket_submission_success", {
            'message': "Your ticket has been submitted successfully!",
            'ticket_id': ticket.id
        })
