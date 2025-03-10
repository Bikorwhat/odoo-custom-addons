from odoo import models, fields

class HelpdeskStageWizard(models.TransientModel):
    _name = 'helpdesk_systems.stage_wizard'
    _description = 'Helpdesk Stage Wizard'

    helpdesk_ticket_id = fields.Many2one('helpdesk_systems.helpdesk_systems', string="Helpdesk Ticket", required=True)
    remarks = fields.Text("Remarks", required=True)
    document = fields.Binary("Upload Document", attachment=True)
    document_name = fields.Char("Document Name") 

    def action_update_stage(self):
        """ Updates the stage, adds remarks, and attaches a document to the helpdesk ticket """
        helpdesk_ticket = self.helpdesk_ticket_id
        new_stage = self.env.context.get('default_stage_id')

        # Create a new remark entry with document
        self.env['helpdesk.remarks'].create({
            'helpdesk_ticket_id': helpdesk_ticket.id,
            'remarks': self.remarks,
            'document': self.document,  # Save the uploaded document
        })

        # Update the ticket stage
        helpdesk_ticket.write({'stage_id': new_stage})

        return {'type': 'ir.actions.act_window_close'}
