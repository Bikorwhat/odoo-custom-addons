from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime

class SaleApprovelRemarkWizard(models.TransientModel):
    _name = 'sale_ext.remark.wizard'
    _description = 'Remark for Sale Order'

    sale_id = fields.Many2one('sale.order', string='Sale Order')
    reason = fields.Text(string="Remark", required=True)
    state = fields.Char('State')
    remark_date = fields.Datetime(string="Remark Date", default=fields.Datetime.now, readonly=True)  # Auto date
    attachment = fields.Binary(string="Attachment")  # Binary field for file upload

    def action_confirm(self):
        """Add a remark to the Sale Order and notify the assigned user."""
        self.ensure_one()
        if not self.sale_id:
            raise UserError('Sale ID is not selected')

        # Create a remark record
        self.env['sale_extend.remark'].create({
            'sale_id': self.sale_id.id,
            'remark': self.reason,
            'state': self.state,
            'remark_date': self.remark_date,  # Save the date
            'attachment': self.attachment,  # Save the attachment
        })

        # Update the sale order state
        self.sale_id.write({
            'state': self.state,
        })

        # Send message to the assigned user (user_id)
        if self.sale_id.user_id:
            self.sale_id.message_post(
                body=f"Your sale order has been {self.state}. Remark: {self.reason}",
                subject="Sale Order Status Update",
                message_type="notification",
                subtype_xmlid="mail.mt_comment",
                partner_ids=[self.sale_id.user_id.partner_id.id],  # Send message to the salesperson
            )

        return {'type': 'ir.actions.act_window_close'}
