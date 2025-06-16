from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InfluenceGenCampaignApplication(models.Model):
    _name = 'influence_gen.campaign_application'
    _description = "Campaign Application by Influencer"
    _order = 'submitted_at desc'

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
    submitted_at = fields.Datetime(string="Submitted At", default=fields.Datetime.now, readonly=True)
    reviewed_at = fields.Datetime(string="Reviewed At", readonly=True)
    reviewer_user_id = fields.Many2one('res.users', string="Reviewed By", readonly=True, index=True)
    rejection_reason = fields.Text(string="Reason for Rejection")
    content_submission_ids = fields.One2many('influence_gen.content_submission', 'campaign_application_id', string="Content Submissions")

    _sql_constraints = [
        ('campaign_influencer_uniq',
         'unique(campaign_id, influencer_profile_id)',
         'An influencer can only apply to a specific campaign once.')
    ]

    @api.depends('campaign_id.name', 'influencer_profile_id.name')
    def _compute_name(self):
        for app in self:
            app.name = f"{app.campaign_id.name or 'N/A'} - {app.influencer_profile_id.name or 'N/A'}"

    def _log_status_change(self, old_status, new_status, details=None):
        self.ensure_one()
        log_details = {
            'application_id': self.id,
            'old_status': old_status,
            'new_status': new_status,
            'campaign': self.campaign_id.name,
            'influencer': self.influencer_profile_id.name,
        }
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
        self.ensure_one()
        if self.status not in ('submitted', 'under_review'):
            raise UserError(_("Application can only be approved if 'Submitted' or 'Under Review'."))
        
        old_status = self.status
        self.write({
            'status': 'approved',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now()
        })
        self._log_status_change(old_status, 'approved', {'reviewer': self.reviewer_user_id.name})

        # Trigger notification "Application Approved" to influencer
        # self.env['influence_gen.infrastructure.integration.service'].send_notification(
        #     user_id=self.influencer_profile_id.user_id.id,
        #     message_type='campaign_application_approved',
        #     message_params={'campaign_name': self.campaign_id.name}
        # )
        self.message_post(body=_("Application approved by %s.", self.reviewer_user_id.name))
        return True

    def action_reject(self, reviewer_user_id, reason):
        self.ensure_one()
        if self.status not in ('submitted', 'under_review'):
            raise UserError(_("Application can only be rejected if 'Submitted' or 'Under Review'."))
        if not reason:
            raise UserError(_("A reason for rejection is required."))

        old_status = self.status
        self.write({
            'status': 'rejected',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'rejection_reason': reason
        })
        self._log_status_change(old_status, 'rejected', {'reviewer': self.reviewer_user_id.name, 'reason': reason})

        # Trigger notification "Application Rejected" to influencer
        # self.env['influence_gen.infrastructure.integration.service'].send_notification(
        #     user_id=self.influencer_profile_id.user_id.id,
        #     message_type='campaign_application_rejected',
        #     message_params={'campaign_name': self.campaign_id.name, 'reason': reason}
        # )
        self.message_post(body=_("Application rejected by %s. Reason: %s", self.reviewer_user_id.name, reason))
        return True

    def action_withdraw(self):
        self.ensure_one()
        # Potentially add constraints, e.g., cannot withdraw if already approved and content submitted
        if self.status not in ('submitted', 'under_review'):
            raise UserError(_("Application can only be withdrawn if 'Submitted' or 'Under Review'."))

        old_status = self.status
        self.write({'status': 'withdrawn_by_influencer'})
        self._log_status_change(old_status, 'withdrawn_by_influencer')
        # Notify admin/campaign manager
        # self.env['influence_gen.infrastructure.integration.service'].send_notification_to_group(...)
        self.message_post(body=_("Application withdrawn by influencer."))
        return True