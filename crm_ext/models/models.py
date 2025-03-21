# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    is_visible = fields.Boolean(compute='_compute_hide_restore_button')
    prev_stage_id = fields.Many2one('crm.stage', string='Old Stage')

    @api.depends('stage_id')
    def _compute_hide_restore_button(self):
        lost_id = self.env.ref('crm_ext.stage_lead5')
        for rec in self:
            if rec.stage_id == lost_id:
                rec.is_visible = False
            else:
                rec.is_visible = True

    def action_custom_convert_to_opportunity(self):
        self.partner_id = False
        return super(CRMLead, self).convert_opportunity(None)
    

    def action_set_lost(self,**addtional_values):
        res = super(CRMLead, self).action_set_lost(**addtional_values)
        lost_stage_id = self.env.ref('crm_ext.stage_lead5').id
        self.prev_stage_id = self.stage_id
        self.write({
            'stage_id': lost_stage_id,
            'active': True,
        })
        return res

    def action_restore(self):
        if self.prev_stage_id:
         self.write({
            'stage_id': self.prev_stage_id.id,
        })

    def action_set_won(self):
        res = super(CRMLead, self).action_set_won()
        for lead in self:
            if not lead.partner_id:  # Only proceed if no customer is linked
                partner = lead._find_partner()
                if not partner:
                    partner = lead._create_customer()
                lead.partner_id = partner.id  # Link the found or created partner
        return res

    def _find_partner(self):
        """ Find a matching partner in res.partner using email and name, then fallback to email-only, then name-only. """
        self.ensure_one()
        Partner = self.env['res.partner']
        
        if self.email_from and self.contact_name:
            partner = Partner.search([('email', '=', self.email_from), ('name', 'ilike', self.contact_name)], limit=1)
            if partner:
                return partner
        if self.email_from:
            partner = Partner.search([('email', '=', self.email_from)], limit=1)
            if partner:
                return partner
        if self.contact_name:
            partner = Partner.search([('name', 'ilike', self.contact_name)], limit=1)
            if partner:
                return partner
        return None  

    def _create_customer(self):
        """ Create a new customer and return the partner record. """
        Partner = self.env['res.partner']
        contact_name = self.contact_name or self.partner_name or self.name

        partner_vals = self._prepare_customer_values(contact_name, is_company=False)
        partner = Partner.create(partner_vals)
        return partner