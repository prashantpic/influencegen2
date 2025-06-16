# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError

# REQ-2-007, REQ-2-008, REQ-2-010: Campaign Management Wizards
class CampaignApplicationRejectionWizard(models.TransientModel):
    _name = 'influence_gen.campaign_app_rejection_wizard'
    _description = 'Campaign Application Rejection Wizard'

    application_id = fields.Many2one(
        'influence_gen.campaign_application',
        string='Campaign Application',
        required=True,
        readonly=True,
        ondelete='cascade'
    )
    rejection_reason = fields.Text(string='Rejection Reason', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super(CampaignApplicationRejectionWizard, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'influence_gen.campaign_application' and self.env.context.get('active_id'):
            res['application_id'] = self.env.context.get('active_id')
        return res

    def action_confirm_application_rejection(self):
        # REQ-2-007, REQ-16-004 (Notification via Business Service)
        self.ensure_one()
        if not self.application_id:
            raise UserError(_("No Campaign Application linked to this wizard."))

        # Call the business service layer
        try:
            self.application_id.sudo()._service_reject_application(self.rejection_reason)
        except Exception as e:
            raise UserError(_("Failed to reject campaign application: %s") % str(e))
            
        return {'type': 'ir.actions.act_window_close'}


class ContentRevisionWizard(models.TransientModel):
    _name = 'influence_gen.content_revision_wizard'
    _description = 'Content Revision Request Wizard'

    submission_id = fields.Many2one(
        'influence_gen.content_submission',
        string='Content Submission',
        required=True,
        readonly=True,
        ondelete='cascade'
    )
    revision_feedback = fields.Text(string='Revision Feedback', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super(ContentRevisionWizard, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'influence_gen.content_submission' and self.env.context.get('active_id'):
            res['submission_id'] = self.env.context.get('active_id')
        return res

    def action_request_content_revision(self):
        # REQ-2-010, REQ-16-005 (Notification via Business Service)
        self.ensure_one()
        if not self.submission_id:
            raise UserError(_("No Content Submission linked to this wizard."))

        # Call the business service layer
        try:
            self.submission_id.sudo()._service_request_revision(self.revision_feedback)
        except Exception as e:
            raise UserError(_("Failed to request content revision: %s") % str(e))

        return {'type': 'ir.actions.act_window_close'}