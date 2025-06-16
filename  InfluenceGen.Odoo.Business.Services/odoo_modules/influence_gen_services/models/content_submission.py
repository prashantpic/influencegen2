# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class InfluenceGenContentSubmission(models.Model):
    _name = 'influence_gen.content_submission'
    _description = "Campaign Content Submission"
    _order = 'submission_date desc'

    campaign_application_id = fields.Many2one(
        'influence_gen.campaign_application', string="Campaign Application",
        required=True, ondelete='cascade', index=True
    )
    campaign_id = fields.Many2one(
        related='campaign_application_id.campaign_id', string="Campaign",
        store=True, readonly=True, index=True
    )
    influencer_profile_id = fields.Many2one(
        related='campaign_application_id.influencer_profile_id', string="Influencer",
        store=True, readonly=True, index=True
    )
    name = fields.Char(string="Submission Title/Reference", compute='_compute_name', store=True)
    content_attachment_ids = fields.Many2many('ir.attachment', string="Content Files")
    content_link = fields.Char(string="Link to Content (e.g., social media post)")
    content_text_caption = fields.Text(string="Text/Caption")
    generated_image_id = fields.Many2one(
        'influence_gen.generated_image', string="Associated AI Generated Image",
        ondelete='set null'
    )
    submission_date = fields.Datetime(
        string="Submission Date", default=fields.Datetime.now, readonly=True
    )
    review_status = fields.Selection([
        ('pending_review', 'Pending Review'),
        ('revision_requested', 'Revision Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Review Status", default='pending_review', required=True, tracking=True, index=True)
    reviewed_by_user_id = fields.Many2one(
        'res.users', string="Reviewed By", readonly=True, index=True
    )
    reviewed_at = fields.Datetime(string="Reviewed At", readonly=True)
    version = fields.Integer(string="Version", default=1, readonly=True)
    feedback_history_ids = fields.One2many(
        'influence_gen.content_feedback', 'content_submission_id',
        string="Feedback History"
    )
    is_final_submission = fields.Boolean(string="Is Final Submission?", default=False)

    @api.depends('campaign_id.name', 'influencer_profile_id.name', 'submission_date')
    def _compute_name(self):
        for sub in self:
            date_str = fields.Datetime.to_string(sub.submission_date) if sub.submission_date else 'N/A'
            sub.name = f"{sub.campaign_id.name or 'N/A'} - {sub.influencer_profile_id.name or 'N/A'} - Submission {date_str}"

    def _notify_influencer(self, message_type, subject, body_template, **kwargs):
        try:
            self.env['influence_gen.infrastructure.integration.services'].send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                message_type=message_type,
                subject=subject,
                body=_(body_template, **kwargs)
            )
        except Exception as e:
            _logger.error(f"Failed to send {message_type} notification for submission {self.id}: {e}")

    def action_approve(self, reviewer_user_id):
        """Approves content. Called by CampaignService. REQ-2-010."""
        self.ensure_one()
        if self.review_status not in ('pending_review', 'revision_requested'):
             raise UserError(_("Only content pending review or with revision requested can be approved."))

        self.write({
            'review_status': 'approved',
            'reviewed_by_user_id': reviewer_user_id.id,
            'reviewed_at': fields.Datetime.now(),
            'is_final_submission': True # Or based on campaign rules, e.g., if campaign requires multiple approved submissions
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_APPROVED',
            actor_user_id=reviewer_user_id.id,
            action_performed='APPROVE_CONTENT',
            target_object=self
        )
        self._notify_influencer(
            'content_approved',
            _("Your content for campaign '%s' has been approved!", self.campaign_id.name),
            "Congratulations! Your content submission for campaign '%s' has been approved." , campaign_name=self.campaign_id.name
        )

        # Potentially trigger payment record creation via PaymentService if is_final_submission
        if self.is_final_submission:
            # This is a conceptual call; PaymentService might have more complex logic
            # self.env['influence_gen.payment_service'].create_payment_for_approved_content(self.id)
            _logger.info("Content submission %s approved and marked final. Payment processing can be triggered.", self.id)
        return True

    def action_reject(self, reviewer_user_id, feedback_text):
        """Rejects content. REQ-2-010."""
        self.ensure_one()
        if self.review_status not in ('pending_review', 'revision_requested'):
             raise UserError(_("Only content pending review or with revision requested can be rejected."))
        if not feedback_text:
            raise UserError(_("Feedback is required when rejecting content."))

        self.write({
            'review_status': 'rejected',
            'reviewed_by_user_id': reviewer_user_id.id,
            'reviewed_at': fields.Datetime.now()
        })
        self.env['influence_gen.content_feedback'].create({
            'content_submission_id': self.id,
            'reviewer_user_id': reviewer_user_id.id,
            'feedback_text': feedback_text
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_REJECTED',
            actor_user_id=reviewer_user_id.id,
            action_performed='REJECT_CONTENT',
            target_object=self,
            details_dict={'feedback': feedback_text}
        )
        self._notify_influencer(
            'content_rejected',
            _("Feedback on your content for campaign '%s'", self.campaign_id.name),
            "Your content submission for campaign '%s' has been rejected. Feedback: %s", campaign_name=self.campaign_id.name, feedback=feedback_text
        )
        return True

    def action_request_revision(self, reviewer_user_id, feedback_text):
        """Requests revision. REQ-2-010."""
        self.ensure_one()
        if self.review_status not in ('pending_review', 'revision_requested'):
             raise UserError(_("Revision can only be requested for content that is pending review or already has a revision requested."))
        if not feedback_text:
            raise UserError(_("Feedback is required when requesting a revision."))

        self.write({
            'review_status': 'revision_requested',
            'reviewed_by_user_id': reviewer_user_id.id,
            'reviewed_at': fields.Datetime.now(),
            'is_final_submission': False # Not final if revision requested
        })
        self.env['influence_gen.content_feedback'].create({
            'content_submission_id': self.id,
            'reviewer_user_id': reviewer_user_id.id,
            'feedback_text': feedback_text
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_REVISION_REQUESTED',
            actor_user_id=reviewer_user_id.id,
            action_performed='REQUEST_REVISION',
            target_object=self,
            details_dict={'feedback': feedback_text}
        )
        self._notify_influencer(
            'content_revision_requested',
            _("Revision requested for your content on campaign '%s'", self.campaign_id.name),
            "A revision has been requested for your content submission for campaign '%s'. Feedback: %s", campaign_name=self.campaign_id.name, feedback=feedback_text
        )
        return True

    def create_new_version_for_revision(self, new_content_data):
        """Creates a new submission record for a revision."""
        self.ensure_one()
        if self.review_status != 'revision_requested':
            raise UserError(_("A new version can only be submitted if a revision was requested."))

        # Mark current submission as superseded or keep for history
        # For simplicity, we create a new one, the old one remains 'revision_requested'
        
        new_submission_vals = {
            'campaign_application_id': self.campaign_application_id.id,
            'version': self.version + 1,
            'submission_date': fields.Datetime.now(),
            'review_status': 'pending_review',
            'content_text_caption': new_content_data.get('content_text_caption'),
            'content_link': new_content_data.get('content_link'),
            'generated_image_id': new_content_data.get('generated_image_id'),
            # attachments handled by service layer if direct file upload
        }
        
        # Handle attachments - this might be done in the service layer
        # if new_content_data.get('content_attachment_ids'):
        #    new_submission_vals['content_attachment_ids'] = [(6, 0, new_content_data.get('content_attachment_ids'))]

        new_submission = self.create(new_submission_vals)
        
        # If new_content_data contains attachment data (e.g., list of attachment IDs to link)
        if 'content_attachment_ids_to_link' in new_content_data:
            new_submission.write({'content_attachment_ids': [(6, 0, new_content_data['content_attachment_ids_to_link'])]})

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_NEW_VERSION',
            actor_user_id=self.influencer_profile_id.user_id.id, # Action by influencer
            action_performed='CREATE_NEW_VERSION',
            target_object=new_submission,
            details_dict={'previous_version_id': self.id}
        )
        return new_submission