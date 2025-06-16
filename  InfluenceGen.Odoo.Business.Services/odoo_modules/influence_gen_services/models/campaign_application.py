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
        ondelete='cascade', # If influencer profile deleted, application is removed
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
        ('campaign_influencer_uniq',
         'unique(campaign_id, influencer_profile_id)',
         'An influencer can only apply to a specific campaign once.')
    ]

    @api.depends('campaign_id.name', 'influencer_profile_id.name')
    def _compute_name(self) -> None:
        for app in self:
            app.name = f"{app.campaign_id.name or 'N/A'} - {app.influencer_profile_id.name or 'N/A'}"

    def action_approve(self, reviewer_user_id: int) -> None:
        """
        Approves the application. Called by CampaignService. REQ-2-007.
        """
        self.ensure_one()
        if self.status not in ['submitted', 'under_review']:
            raise UserError(_("Application can only be approved if it's 'Submitted' or 'Under Review'."))

        self.write({
            'status': 'approved',
            'reviewer_user_id': reviewer_user_id,
            'reviewed_at': fields.Datetime.now()
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_APPLICATION_APPROVED',
            actor_user_id=reviewer_user_id,
            action_performed='APPROVE_APPLICATION',
            target_object=self
        )
        # Trigger notification "Application Approved" to influencer
        self.env['influence_gen_integration.notification_service'].send_notification(
            user_id=self.influencer_profile_id.user_id.id,
            message_type='application_approved',
            title=_("Application Approved for %s", self.campaign_id.name),
            message_body=_("Congratulations! Your application for the campaign '%s' has been approved.", self.campaign_id.name)
        )

    def action_reject(self, reviewer_user_id: int, reason: str) -> None:
        """
        Rejects the application. REQ-2-007.
        """
        self.ensure_one()
        if not reason:
            raise UserError(_("A reason is required for rejecting an application."))
        if self.status not in ['submitted', 'under_review']:
            raise UserError(_("Application can only be rejected if it's 'Submitted' or 'Under Review'."))

        self.write({
            'status': 'rejected',
            'reviewer_user_id': reviewer_user_id,
            'reviewed_at': fields.Datetime.now(),
            'rejection_reason': reason
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_APPLICATION_REJECTED',
            actor_user_id=reviewer_user_id,
            action_performed='REJECT_APPLICATION',
            target_object=self,
            details_dict={'reason': reason}
        )
        # Trigger notification "Application Rejected" to influencer
        self.env['influence_gen_integration.notification_service'].send_notification(
            user_id=self.influencer_profile_id.user_id.id,
            message_type='application_rejected',
            title=_("Application Update for %s", self.campaign_id.name),
            message_body=_("Regarding your application for campaign '%s': %s", self.campaign_id.name, reason)
        )

    def action_withdraw(self) -> None:
        """
        Allows influencer to withdraw their application.
        Called by influencer via portal (through a controller that calls this method).
        """
        self.ensure_one()
        if self.status not in ['submitted', 'under_review', 'approved']: # Can withdraw even if approved, if campaign hasn't started or no content submitted
            raise UserError(_("Application cannot be withdrawn as it is in status '%s'.", self.status))
        
        # Check if user is the influencer themselves
        if self.env.user != self.influencer_profile_id.user_id and not self.env.user.has_group('influence_gen_services.group_influence_gen_admin'):
            raise UserError(_("You do not have permission to withdraw this application."))

        self.write({'status': 'withdrawn_by_influencer'})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_APPLICATION_WITHDRAWN',
            actor_user_id=self.env.user.id, # Should be influencer's user ID
            action_performed='WITHDRAW_APPLICATION',
            target_object=self
        )
        # Notify admin/campaign manager
        # self.env['influence_gen_integration.notification_service'].send_notification(...)