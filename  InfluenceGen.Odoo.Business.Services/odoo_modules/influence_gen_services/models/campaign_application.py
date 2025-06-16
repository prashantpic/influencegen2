# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class InfluenceGenCampaignApplication(models.Model):
    _name = 'influence_gen.campaign_application'
    _description = "Campaign Application by Influencer"
    _order = 'submitted_at desc'

    campaign_id = fields.Many2one(
        'influence_gen.campaign', string="Campaign",
        required=True, ondelete='cascade', index=True
    )
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string="Influencer",
        required=True, ondelete='cascade', index=True
    )
    name = fields.Char(string="Application Reference", compute='_compute_name', store=True)
    proposal_text = fields.Text(string="Proposal / Expression of Interest")
    custom_questions_answers_json = fields.Text(string="Custom Questions & Answers (JSON)")
    status = fields.Selection([
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn_by_influencer', 'Withdrawn by Influencer')
    ], string="Application Status", default='submitted', required=True, tracking=True, index=True)
    submitted_at = fields.Datetime(
        string="Submitted At", default=fields.Datetime.now, readonly=True
    )
    reviewed_at = fields.Datetime(string="Reviewed At", readonly=True)
    reviewer_user_id = fields.Many2one(
        'res.users', string="Reviewed By", readonly=True, index=True
    )
    rejection_reason = fields.Text(string="Reason for Rejection")
    content_submission_ids = fields.One2many(
        'influence_gen.content_submission', 'campaign_application_id',
        string="Content Submissions"
    )

    _sql_constraints = [
        ('campaign_influencer_uniq',
         'unique(campaign_id, influencer_profile_id)',
         'An influencer can only apply to a specific campaign once.')
    ]

    @api.depends('campaign_id.name', 'influencer_profile_id.name')
    def _compute_name(self):
        for app in self:
            app.name = f"{app.campaign_id.name or 'N/A'} - {app.influencer_profile_id.name or 'N/A'}"

    def action_approve(self, reviewer_user_id):
        """Approves the application. Called by CampaignService. REQ-2-007."""
        self.ensure_one()
        if self.status not in ('submitted', 'under_review'):
            raise UserError(_("Only submitted or under review applications can be approved."))

        self.write({
            'status': 'approved',
            'reviewer_user_id': reviewer_user_id.id,
            'reviewed_at': fields.Datetime.now()
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_APPLICATION_APPROVED',
            actor_user_id=reviewer_user_id.id,
            action_performed='APPROVE_APPLICATION',
            target_object=self
        )
        # Trigger notification "Application Approved" to influencer
        try:
            self.env['influence_gen.infrastructure.integration.services'].send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                message_type='application_approved',
                subject=_("Your application for campaign '%s' has been approved!", self.campaign_id.name),
                body=_("Congratulations! Your application for the campaign '%s' has been approved.", self.campaign_id.name)
            )
        except Exception as e:
            _logger.error(f"Failed to send application approved notification for app {self.id}: {e}")
        return True

    def action_reject(self, reviewer_user_id, reason):
        """Rejects the application. REQ-2-007."""
        self.ensure_one()
        if self.status not in ('submitted', 'under_review'):
            raise UserError(_("Only submitted or under review applications can be rejected."))
        if not reason:
            raise UserError(_("A reason is required for rejecting an application."))

        self.write({
            'status': 'rejected',
            'reviewer_user_id': reviewer_user_id.id,
            'reviewed_at': fields.Datetime.now(),
            'rejection_reason': reason
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_APPLICATION_REJECTED',
            actor_user_id=reviewer_user_id.id,
            action_performed='REJECT_APPLICATION',
            target_object=self,
            details_dict={'reason': reason}
        )
        # Trigger notification "Application Rejected" to influencer
        try:
            self.env['influence_gen.infrastructure.integration.services'].send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                message_type='application_rejected',
                subject=_("Update on your application for campaign '%s'", self.campaign_id.name),
                body=_("Unfortunately, your application for the campaign '%s' has been rejected. Reason: %s", self.campaign_id.name, reason)
            )
        except Exception as e:
            _logger.error(f"Failed to send application rejected notification for app {self.id}: {e}")
        return True

    def action_withdraw(self):
        """Allows influencer to withdraw their application."""
        self.ensure_one()
        if self.status not in ('submitted', 'under_review'):
            raise UserError(_("Only submitted or under review applications can be withdrawn."))
        if self.env.user != self.influencer_profile_id.user_id and not self.env.user.has_group('influence_gen_services.group_influence_gen_admin'):
             raise UserError(_("You are not authorized to withdraw this application."))

        self.write({'status': 'withdrawn_by_influencer'})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_APPLICATION_WITHDRAWN',
            actor_user_id=self.env.user.id,
            action_performed='WITHDRAW_APPLICATION',
            target_object=self
        )
        return True