# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InfluenceGenCampaignApplication(models.Model):
    _name = 'influence_gen.campaign_application'
    _description = "Campaign Application by Influencer"
    _order = 'submitted_at desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    campaign_id = fields.Many2one(
        'influence_gen.campaign',
        string="Campaign",
        required=True,
        ondelete='cascade',
        index=True
    )
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Influencer",
        required=True,
        ondelete='cascade',
        index=True
    )
    name = fields.Char(string="Application Reference", compute='_compute_name', store=True, readonly=True)
    proposal_text = fields.Text(string="Proposal / Expression of Interest")
    custom_questions_answers_json = fields.Text(string="Custom Questions & Answers (JSON)")
    status = fields.Selection([
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn_by_influencer', 'Withdrawn by Influencer')
    ], string="Application Status", default='submitted', required=True, tracking=True, index=True)
    submitted_at = fields.Datetime(string="Submitted At", default=fields.Datetime.now, readonly=True)
    reviewed_at = fields.Datetime(string="Reviewed At", readonly=True)
    reviewer_user_id = fields.Many2one('res.users', string="Reviewed By", readonly=True, index=True)
    rejection_reason = fields.Text(string="Reason for Rejection")
    content_submission_ids = fields.One2many(
        'influence_gen.content_submission',
        'campaign_application_id',
        string="Content Submissions"
    )

    _sql_constraints = [
        (
            'campaign_influencer_uniq',
            'unique(campaign_id, influencer_profile_id)',
            'An influencer can only apply to a specific campaign once.'
        )
    ]

    @api.depends('campaign_id.name', 'influencer_profile_id.name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.campaign_id.name or 'N/A'} - {record.influencer_profile_id.name or 'N/A'}"

    def _log_status_change(self, new_status, details=None):
        self.ensure_one()
        log_details = {'old_status': self._origin.status if self._origin else 'N/A', 'new_status': new_status}
        if details:
            log_details.update(details)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_APPLICATION_STATUS_CHANGED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict=log_details
        )

    def action_approve(self, reviewer_user_id):
        """Approves the application. Called by CampaignService. REQ-2-007."""
        self.ensure_one()
        if self.status not in ['submitted', 'under_review']:
            raise UserError(_("Application can only be approved if 'Submitted' or 'Under Review'."))

        self.write({
            'status': 'approved',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now()
        })
        self._log_status_change('approved')

        # Trigger notification "Application Approved" to influencer
        notification_service = self.env['influence_gen.infrastructure.integration.services'].sudo()
        if hasattr(notification_service, 'send_notification') and self.influencer_profile_id.user_id:
             notification_service.send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                notification_type='campaign_application_approved',
                title=_("Campaign Application Approved!"),
                message=_("Your application for campaign '%s' has been approved.", self.campaign_id.name),
                target_model=self._name,
                target_res_id=self.id
            )
        return True

    def action_reject(self, reviewer_user_id, reason):
        """Rejects the application. REQ-2-007."""
        self.ensure_one()
        if self.status not in ['submitted', 'under_review']:
            raise UserError(_("Application can only be rejected if 'Submitted' or 'Under Review'."))
        if not reason:
            raise UserError(_("A reason is required for rejecting an application."))

        self.write({
            'status': 'rejected',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'rejection_reason': reason
        })
        self._log_status_change('rejected', details={'reason': reason})

        # Trigger notification "Application Rejected" to influencer
        notification_service = self.env['influence_gen.infrastructure.integration.services'].sudo()
        if hasattr(notification_service, 'send_notification') and self.influencer_profile_id.user_id:
            notification_service.send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                notification_type='campaign_application_rejected',
                title=_("Campaign Application Update"),
                message=_("Your application for campaign '%s' has been rejected. Reason: %s", self.campaign_id.name, reason),
                target_model=self._name,
                target_res_id=self.id
            )
        return True

    def action_withdraw(self):
        """Allows influencer to withdraw their application."""
        self.ensure_one()
        # Check if the current user is the influencer or an admin
        if self.env.user != self.influencer_profile_id.user_id and not self.env.user.has_group('influence_gen_services.group_influence_gen_admin'): # Assuming admin group
            raise UserError(_("You are not authorized to withdraw this application."))

        if self.status not in ['submitted', 'under_review', 'approved']: # Can withdraw even if approved if no content submitted yet
            raise UserError(_("Application cannot be withdrawn as it is in status '%s'.") % self.status)

        self.write({'status': 'withdrawn_by_influencer'})
        self._log_status_change('withdrawn_by_influencer')
        return True