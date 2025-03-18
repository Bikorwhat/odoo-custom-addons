from odoo import api, fields, models

class SettingNotify(models.TransientModel):
    _inherit = 'res.config.settings'

    notification_days_before_deadline = fields.Integer(
        string="Notification Days Before Deadline",
        default=0,
        config_parameter='todo_app.notification_days_before_deadline'
    )
