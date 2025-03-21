from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.tools import _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    has_lower_price = fields.Boolean(string="Has Lower Price", compute="_compute_has_lower_price")
    is_field_read = fields.Boolean(string="read only field", compute="_compute_has_read_only")
    
    state_extend = fields.Char(string='Extended State')
    remark = fields.One2many(
        'sale_extend.remark',  # Related model
        'sale_id',  # Inverse field in the related model
        string='Remarks',
    )

    state = fields.Selection(
        selection_add=[
            ('sent_for_approval', 'Sent for Approval'),
            ('approved', 'Approved'),
            ('sent',)
        ]
    )

    @api.depends('order_line.price_unit', 'order_line.product_id.list_price')
    def _compute_has_lower_price(self):
        for order in self:
            order.has_lower_price = any(
                line.price_unit < line.product_id.list_price for line in order.order_line
            )
    @api.depends('state')
    def _compute_has_read_only(self):
        for rec in self:
            if rec.state in ['approved','sent'] and self.env.user.id not in self.env.ref('sales_team.group_sale_manager').users.mapped('id') :
                rec.is_field_read = True
            else:
                rec.is_field_read = False
    def action_sent_for_approval(self):
     for order in self:
        for line in order.order_line:
            if line.price_unit < line.product_id.list_price:
                order.write({'state': 'sent_for_approval'})
                return
    # If no line requires approval, continue normal flow
     order.write({'state': 'draft'})

    
    def action_open_approve_wizard(self):
        return self._open_remark_wizard('approved')

    def action_open_reject_wizard(self):
        return self._open_remark_wizard('draft')

    def _open_remark_wizard(self, state):
        return {
            'name': 'Add Remark',
            'type': 'ir.actions.act_window',
            'res_model': 'sale_ext.remark.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sales_ext.view_sale_remark_form').id,
            'target': 'new',
            'context': {
                'default_sale_id': self.id,
                'default_state': state,
            },
        }
        
    def _confirmation_error_message(self):
        """Override to only allow confirmation in the 'approved' state."""
        self.ensure_one()
        # Call the original method to get the error message for other checks (e.g., missing products)
        if self.state not in  ('draft','approved','sent'):
            return _("You can only confirm orders in the 'draft','approved','sent' state.")
        error_msg = super()._confirmation_error_message()
        if error_msg:
            return error_msg

        return False

    def action_confirm(self):
        for order in self:
            if order.state not in ('draft','approved','sent'):
                raise UserError(_("You can only confirm orders in the 'draft','approved','sent' state."))
        return super(SaleOrder, self).action_confirm()
    
    def action_quotation_send(self):
     for order in self:
        result = super(SaleOrder, order).action_quotation_send()
        # Update the state to 'sent' only if it's in draft or approved state
        if order.state in ['draft', 'approved']:
            order.write({'state': 'sent'})
     return result

class SaleRemark(models.Model):
    _name = 'sale_extend.remark'
    _description = 'Sale Approval Remark'

    sale_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    remark = fields.Text(string='Remark', required=True)
    state = fields.Char(string='State')
    remark_date = fields.Datetime(string="Remark Date", default=fields.Datetime.now, readonly=True)  # Auto date
    attachment = fields.Binary(string="Attachment")  # Binary field for file upload

    @api.model
    def create(self, vals):
        """Override create method to update Sale Order state when a remark is added."""
        remark = super(SaleRemark, self).create(vals)
        if remark.sale_id:
            remark.sale_id.write({'state': remark.state})
        return remark
