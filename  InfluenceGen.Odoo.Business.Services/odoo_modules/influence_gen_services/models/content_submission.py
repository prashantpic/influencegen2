from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InfluenceGenContentSubmission(models.Model):
    _name = 'influence_gen.content_submission'
    _description = "Campaign Content Submission"
    _order = 'submission_date desc'

    campaign_application_id = fields.Many2one(
        'influence_gen.campaign_application',
        string="Campaign Application",
        required=True,
        ondelete='cascade',
        index=True
    )
    campaign_id = fields.Many2one(
        related='campaign_application_id.campaign_id',
        string="Campaign",
        store=True,
        readonly=True,
        index=True
    )
    influencer_profile_id = fields.Many2one(
        related='campaign_application_id.influencer_profile_id',
        string="Influencer",
        store=True,
        readonly=True,
        index=True
    )
    name = fields.Char(string="Submission Title/Reference", compute='_compute_name', store=True)
    content_attachment_ids = fields.Many2many('ir.attachment', string="Content Files")
    content_link = fields.Char(string="Link to Content (e.g., social media post)")
    content_text_caption = fields.Text(string="Text/Caption")
    generated_image_id = fields.Many2one('influence_gen.generated_image', string="Associated AI Generated Image", ondelete='set null')
    submission_date = fields.Datetime(string="Submission Date", default=fields.Datetime.now, readonly=True)
    review_status = fields.Selection([
        ('pending_review', 'Pending Review'),
        ('revision_requested', 'Revision Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Review Status", default='pending_review', required=True, tracking=True, index=True)
    reviewed_by_user_id = fields.Many2one('res.users', string="Reviewed By", readonly=True, index=True)
    reviewed_at = fields.Datetime(string="Reviewed At", readonly=True)
    version = fields.Integer(string="Version", default=1, readonly=True)
    feedback_history_ids = fields.One2many('influence_gen.content_feedback', 'content_submission_id', string="Feedback History")
    is_final_submission = fields.Boolean(string="Is Final Submission?", default=False)

    @api.depends('campaign_id.name', 'influencer_profile_id.name', 'submission_date', 'version')
    def _compute_name(self):
        for sub in self:
            date_str = fields.Datetime. Kontextualize_datetime(sub.submission_date, self.env.user.tz).strftime('%Y-%m-%d') if sub.submission_date else 'N/A'
            sub.name = f"{sub.campaign_id.name or 'N/A'} - {sub.influencer_profile_id.name or 'N/A'} - V{sub.version} ({date_str})"

    def _log_review_action(self, action_type, reviewer_user_id, feedback_text=None):
        self.ensure_one()
        details = {
            'submission_id': self.id,
            'action': action_type,
            'reviewer': reviewer_user_id.name if reviewer_user_id else self.env.user.name,
            'campaign': self.campaign_id.name,
            'influencer': self.influencer_profile_id.name,
        }
        if feedback_text:
            details['feedback'] = feedback_text

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_REVIEWED',
            actor_user_id=reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict=details
        )

    def action_approve(self, reviewer_user_id):
        self.ensure_one()
        if self.review_status not in ('pending_review', 'revision_requested'):
             raise UserError(_("Content can only be approved if 'Pending Review' or 'Revision Requested'."))

        vals = {
            'review_status': 'approved',
            'reviewed_by_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'is_final_submission': True # Default assumption, could be based on campaign rules
        }
        self.write(vals)
        self._log_review_action('approved', vals.get('reviewed_by_user_id'))

        # Trigger notification "Content Approved" to influencer
        # self.env['influence_gen.infrastructure.integration.service'].send_notification(
        #     user_id=self.influencer_profile_id.user_id.id,
        #     message_type='content_submission_approved',
        #     message_params={'campaign_name': self.campaign_id.name, 'submission_name': self.name}
        # )
        self.message_post(body=_("Content submission approved by %s.", self.reviewed_by_user_id.name))

        # Potentially trigger payment record creation via PaymentService if is_final_submission
        if self.is_final_submission:
            # This logic is typically handled by PaymentService based on approved content
            # self.env['influence_gen.service.payment'].create_payment_for_submission(self.id)
            pass
        return True

    def action_reject(self, reviewer_user_id, feedback_text):
        self.ensure_one()
        if self.review_status not in ('pending_review', 'revision_requested'):
             raise UserError(_("Content can only be rejected if 'Pending Review' or 'Revision Requested'."))
        if not feedback_text:
            raise UserError(_("Feedback is required when rejecting content."))

        vals = {
            'review_status': 'rejected',
            'reviewed_by_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now()
        }
        self.write(vals)
        self.env['influence_gen.content_feedback'].create({
            'content_submission_id': self.id,
            'reviewer_user_id': vals.get('reviewed_by_user_id'),
            'feedback_text': feedback_text,
        })
        self._log_review_action('rejected', vals.get('reviewed_by_user_id'), feedback_text)

        # Trigger notification "Content Rejected" to influencer
        # self.env['influence_gen.infrastructure.integration.service'].send_notification(
        #     user_id=self.influencer_profile_id.user_id.id,
        #     message_type='content_submission_rejected',
        #     message_params={'campaign_name': self.campaign_id.name, 'submission_name': self.name, 'feedback': feedback_text}
        # )
        self.message_post(body=_("Content submission rejected by %s. Feedback: %s", self.reviewed_by_user_id.name, feedback_text))
        return True

    def action_request_revision(self, reviewer_user_id, feedback_text):
        self.ensure_one()
        if self.review_status not in ('pending_review', 'revision_requested'):
             raise UserError(_("Revision can only be requested if 'Pending Review' or 'Revision Requested'."))
        if not feedback_text:
            raise UserError(_("Feedback is required when requesting revision."))

        vals = {
            'review_status': 'revision_requested',
            'reviewed_by_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'is_final_submission': False # No longer final if revision requested
        }
        self.write(vals)
        self.env['influence_gen.content_feedback'].create({
            'content_submission_id': self.id,
            'reviewer_user_id': vals.get('reviewed_by_user_id'),
            'feedback_text': feedback_text,
        })
        self._log_review_action('revision_requested', vals.get('reviewed_by_user_id'), feedback_text)

        # Trigger notification "Revision Requested" to influencer
        # self.env['influence_gen.infrastructure.integration.service'].send_notification(
        #     user_id=self.influencer_profile_id.user_id.id,
        #     message_type='content_submission_revision_requested',
        #     message_params={'campaign_name': self.campaign_id.name, 'submission_name': self.name, 'feedback': feedback_text}
        # )
        self.message_post(body=_("Content submission revision requested by %s. Feedback: %s", self.reviewed_by_user_id.name, feedback_text))
        return True

    def create_new_version_for_revision(self, new_content_data):
        self.ensure_one()
        if self.review_status != 'revision_requested':
            raise UserError(_("A new version can only be created for submissions awaiting revision."))

        default_vals = {
            'campaign_application_id': self.campaign_application_id.id,
            'version': self.version + 1,
            'submission_date': fields.Datetime.now(),
            'review_status': 'pending_review',
            'is_final_submission': False,
            # Copy other relevant fields if needed, or expect them in new_content_data
        }
        if 'content_attachment_ids' in new_content_data: # M2M field
            default_vals['content_attachment_ids'] = [(6, 0, new_content_data.pop('content_attachment_ids'))]

        default_vals.update(new_content_data)
        new_submission = self.copy(default=default_vals)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_NEW_VERSION',
            actor_user_id=self.env.user.id, # Assumes submitted by current user (influencer)
            action_performed='CREATE',
            target_object=new_submission,
            details_dict={
                'new_submission_id': new_submission.id,
                'previous_submission_id': self.id,
                'version': new_submission.version
            }
        )
        # Mark old one as superseded or link them if needed. For now, just create new.
        # self.write({'review_status': 'superseded_by_revision'}) # Example
        return new_submission