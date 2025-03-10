from odoo import models, fields

class Category(models.Model):
    _name = 'helpdesk_systems.helpdesk_category'
    _description = 'Helpdesk Category'

    # Fields for the Helpdesk Category model
    name = fields.Char(string='Category Title', required=True)
    description = fields.Text(string='Description')
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Category already exists!"),
    ]