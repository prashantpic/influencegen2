# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InfluenceGenContentSubmission(models.Model):
    _name = 'influence_gen.content_submission'
    _description = "Campaign Content Submission"
    _order = 'submission_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
    name = fields.Char(string="Submission Title/Reference", compute='_compute_name', store=True, readonly=True)
    content_attachment_ids = fields.Many2many(
        'ir.attachment',
        'content_submission_ir_attachments_rel',
        'content_submission_id', 'attachment_id', # Explicit relation table name and column names
        string="Content Files"
    )
    content_link = fields.Char(string="Link to Content (e.g., social media post)")
    content_text_caption = fields.Text(string="Text/Caption")
    generated_image_id = fields.Many2one(
        'influence_gen.generated_image',
        string="Associated AI Generated Image",
        ondelete='set null'
    )
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
    feedback_history_ids = fields.One2many(
        'influence_gen.content_feedback',
        'content_submission_id',
        string="Feedback History"
    )
    is_final_submission = fields.Boolean(string="Is Final Submission?", default=False)

    @api.depends('campaign_id.name', 'influencer_profile_id.name', 'submission_date', 'version')
    def _compute_name(self):
        for record in self:
            date_str = fields.Datetime.from_string(record.submission_date).strftime('%Y-%m-%d') if record.submission_date else 'N/A'
            record.name = f"{record.campaign_id.name or 'N/A'} - {record.influencer_profile_id.name or 'N/A'} - V{record.version} - {date_str}"

    def _log_review_action(self, action, details=None):
        self.ensure_one()
        log_details = {'action': action, 'old_status': self._origin.review_status if self._origin else 'N/A', 'new_status': self.review_status}
        if details:
            log_details.update(details)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_REVIEWED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict=log_details
        )

    def _create_feedback_record(self, reviewer_user_id, feedback_text):
        self.ensure_one()
        self.env['influence_gen.content_feedback'].create({
            'content_submission_id': self.id,
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'feedback_text': feedback_text,
        })

    def action_approve(self, reviewer_user_id):
        """Approves content. Called by CampaignService. REQ-2-010."""
        self.ensure_one()
        if self.review_status not in ['pending_review', 'revision_requested']:
             raise UserError(_("Content can only be approved if 'Pending Review' or 'Revision Requested'."))

        vals = {
            'review_status': 'approved',
            'reviewed_by_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'is_final_submission': True # Or based on campaign rules
        }
        self.write(vals)
        self._log_review_action('approved')

        # Trigger notification "Content Approved" to influencer
        notification_service = self.env['influence_gen.infrastructure.integration.services'].sudo()
        if hasattr(notification_service, 'send_notification') and self.influencer_profile_id.user_id:
             notification_service.send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                notification_type='content_submission_approved',
                title=_("Content Approved!"),
                message=_("Your content submission '%s' for campaign '%s' has been approved.", self.name, self.campaign_id.name),
                target_model=self._name,
                target_res_id=self.id
            )

        # Potentially trigger payment record creation via PaymentService if is_final_submission
        if self.is_final_submission:
            payment_service = self.env['influence_gen.payment_service'].sudo() # Assuming service exists
            if hasattr(payment_service, 'trigger_payment_for_submission'):
                payment_service.trigger_payment_for_submission(self.id)
        return True

    def action_reject(self, reviewer_user_id, feedback_text):
        """Rejects content. REQ-2-010."""
        self.ensure_one()
        if self.review_status not in ['pending_review', 'revision_requested']:
            raise UserError(_("Content can only be rejected if 'Pending Review' or 'Revision Requested'."))
        if not feedback_text:
            raise UserError(_("Feedback text is required for rejecting content."))

        self.write({
            'review_status': 'rejected',
            'reviewed_by_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now()
        })
        self._create_feedback_record(reviewer_user_id, feedback_text)
        self._log_review_action('rejected', details={'feedback': feedback_text})

        # Trigger notification "Content Rejected" to influencer
        notification_service = self.env['influence_gen.infrastructure.integration.services'].sudo()
        if hasattr(notification_service, 'send_notification') and self.influencer_profile_id.user_id:
             notification_service.send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                notification_type='content_submission_rejected',
                title=_("Content Submission Update"),
                message=_("Your content submission '%s' for campaign '%s' has been rejected. Feedback: %s", self.name, self.campaign_id.name, feedback_text),
                target_model=self._name,
                target_res_id=self.id
            )
        return True

    def action_request_revision(self, reviewer_user_id, feedback_text):
        """Requests revision. REQ-2-010."""
        self.ensure_one()
        if self.review_status not in ['pending_review']:
            raise UserError(_("Revision can only be requested if content is 'Pending Review'."))
        if not feedback_text:
            raise UserError(_("Feedback text is required for requesting revision."))

        self.write({
            'review_status': 'revision_requested',
            'reviewed_by_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'is_final_submission': False
        })
        self._create_feedback_record(reviewer_user_id, feedback_text)
        self._log_review_action('revision_requested', details={'feedback': feedback_text})

        # Trigger notification "Revision Requested" to influencer
        notification_service = self.env['influence_gen.infrastructure.integration.services'].sudo()
        if hasattr(notification_service, 'send_notification') and self.influencer_profile_id.user_id:
             notification_service.send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                notification_type='content_submission_revision_requested',
                title=_("Content Submission Revision Requested"),
                message=_("Revisions have been requested for your content submission '%s' for campaign '%s'. Feedback: %s", self.name, self.campaign_id.name, feedback_text),
                target_model=self._name,
                target_res_id=self.id
            )
        return True

    def create_new_version_for_revision(self, new_content_data=None):
        """Creates a new submission record for a revision."""
        self.ensure_one()
        if self.review_status != 'revision_requested':
            raise UserError(_("A new version can only be created if the current status is 'Revision Requested'."))

        default_vals = {
            'campaign_application_id': self.campaign_application_id.id,
            'version': self.version + 1,
            'submission_date': fields.Datetime.now(),
            'review_status': 'pending_review',
            'is_final_submission': False,
            # Copy other relevant fields if needed, or clear them
            'content_link': new_content_data.get('content_link') if new_content_data else None,
            'content_text_caption': new_content_data.get('content_text_caption') if new_content_data else None,
            'generated_image_id': new_content_data.get('generated_image_id') if new_content_data else None,
        }
        # Handle attachments carefully if they are part of new_content_data
        # new_attachment_ids = new_content_data.get('content_attachment_ids', [])
        # default_vals['content_attachment_ids'] = [(6, 0, new_attachment_ids)]


        new_submission = self.copy(default=default_vals)
        # Mark old one as superseded if needed (e.g., by changing its status or a flag)
        # self.write({'review_status': 'superseded'}) # Example, not in SDS explicitly

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_NEW_VERSION',
            actor_user_id=self.influencer_profile_id.user_id.id, # Action by influencer
            action_performed='CREATE',
            target_object=new_submission,
            details_dict={'previous_version_id': self.id, 'new_version_id': new_submission.id}
        )
        return new_submission