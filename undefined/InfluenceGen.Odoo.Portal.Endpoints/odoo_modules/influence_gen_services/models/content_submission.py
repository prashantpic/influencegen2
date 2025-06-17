# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class ContentSubmission(models.Model):
    _name = 'influence_gen.content_submission'
    _description = 'Content Submission for Campaigns'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'influence_gen.base_audit_mixin']
    _order = 'submission_date desc, id desc'

    campaign_application_id = fields.Many2one(
        'influence_gen.campaign_application', string='Campaign Application',
        required=True, ondelete='cascade', index=True, tracking=True)
    campaign_id = fields.Many2one(
        'influence_gen.campaign', string='Campaign',
        related='campaign_application_id.campaign_id', store=True, readonly=True, index=True, tracking=True)
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string='Influencer',
        related='campaign_application_id.influencer_profile_id', store=True, readonly=True, index=True, tracking=True)

    generated_image_id = fields.Many2one(
        'influence_gen.generated_image', string='AI Generated Image',
        ondelete='set null', help="Link to an AI-generated image used in this submission.", tracking=True)
    content_url = fields.Char(string='Content URL', help="URL to the live content (e.g., social media post).", tracking=True)
    content_attachment_id = fields.Many2one(
        'ir.attachment', string='Content Attachment',
        help="Directly uploaded content file.", tracking=True)
    file_type = fields.Char(string='File Type', help="MIME type or common name of the content.", tracking=True)

    submission_date = fields.Datetime(
        string='Submission Date', default=fields.Datetime.now,
        required=True, readonly=True, tracking=True) # REQ-2-009

    review_status = fields.Selection([
        ('pending_review', 'Pending Review'),
        ('revision_requested', 'Revision Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Review Status', default='pending_review', required=True, tracking=True, index=True, copy=False) # REQ-2-010

    feedback_history_ids = fields.One2many(
        'influence_gen.content_feedback_log', 'content_submission_id',
        string='Feedback History', readonly=True)

    reviewed_by_user_id = fields.Many2one(
        'res.users', string='Reviewed By', readonly=True, tracking=True, copy=False)
    reviewed_at = fields.Datetime(string='Reviewed At', readonly=True, tracking=True, copy=False)
    version = fields.Integer(string='Version', default=1, required=True, tracking=True, copy=False, help="Version number of the submission.")

    performance_data_json = fields.Text(
        string='Performance Data (JSON)',
        help="JSON string containing performance metrics for this content (e.g., likes, views, clicks).", tracking=True) # REQ-2-011

    # REQ-DMG-006: Content Submission Management
    # REQ-2-018: Audit trail (via BaseAuditMixin)

    @api.constrains('content_url', 'content_attachment_id')
    def _check_content_presence(self):
        for record in self:
            if not record.content_url and not record.content_attachment_id and not record.generated_image_id:
                raise ValidationError(_("A content submission must have either a URL, an attachment, or an AI generated image linked."))

    def action_approve_content(self, reviewer_id=None):
        """Approves the content submission."""
        # REQ-2-010
        self.ensure_one()
        if self.review_status == 'approved':
            raise UserError(_("This content submission is already approved."))

        reviewer = reviewer_id or self.env.user
        vals = {
            'review_status': 'approved',
            'reviewed_by_user_id': reviewer.id,
            'reviewed_at': fields.Datetime.now(),
        }
        self.write(vals)
        self.message_post(body=_("Content submission approved by %s.") % reviewer.name)

        # Potentially trigger payment record creation via service
        # self.env['influence_gen.services.payment_processing'].create_payment_records_for_approved_content(self.ids)
        # Notify influencer (REQ-16-005)
        # self._send_status_notification('approved')
        return True

    def action_reject_content(self, feedback_text, reviewer_id=None):
        """Rejects the content submission with feedback."""
        # REQ-2-010
        self.ensure_one()
        if self.review_status == 'rejected':
            raise UserError(_("This content submission is already rejected."))
        if not feedback_text:
            raise UserError(_("Feedback text is required for rejecting a submission."))

        reviewer = reviewer_id or self.env.user
        vals = {
            'review_status': 'rejected',
            'reviewed_by_user_id': reviewer.id,
            'reviewed_at': fields.Datetime.now(),
        }
        self.write(vals)
        self.env['influence_gen.content_feedback_log'].create({
            'content_submission_id': self.id,
            'reviewer_user_id': reviewer.id,
            'feedback_text': feedback_text,
            'timestamp': fields.Datetime.now(),
        })
        self.message_post(body=_("Content submission rejected by %s. Feedback: %s") % (reviewer.name, feedback_text))
        # Notify influencer (REQ-16-005)
        # self._send_status_notification('rejected', feedback_text)
        return True

    def action_request_revision(self, feedback_text, reviewer_id=None):
        """Requests revision for the content submission with feedback."""
        # REQ-2-010
        self.ensure_one()
        if not feedback_text:
            raise UserError(_("Feedback text is required for requesting a revision."))

        reviewer = reviewer_id or self.env.user
        vals = {
            'review_status': 'revision_requested',
            'reviewed_by_user_id': reviewer.id,
            'reviewed_at': fields.Datetime.now(),
        }
        self.write(vals)
        self.env['influence_gen.content_feedback_log'].create({
            'content_submission_id': self.id,
            'reviewer_user_id': reviewer.id,
            'feedback_text': feedback_text,
            'timestamp': fields.Datetime.now(),
        })
        self.message_post(body=_("Revision requested for content submission by %s. Feedback: %s") % (reviewer.name, feedback_text))
        # Notify influencer (REQ-16-005)
        # self._send_status_notification('revision_requested', feedback_text)
        return True

    def submit_new_version(self, new_attachment_id=None, new_url=None, new_generated_image_id=None):
        """
        Creates a new version of this content submission or updates if policy allows.
        This simplified version creates a new submission record for a new version.
        A more complex approach might involve archiving the old one or having a parent/child relationship.
        For this implementation, we'll create a new record copying essential data and incrementing version.
        """
        # REQ-DMG-006: Version Control (conceptual)
        self.ensure_one()
        if self.review_status not in ['revision_requested', 'rejected']:
             raise UserError(_("You can only submit a new version for submissions that require revision or were rejected."))

        if not new_url and not new_attachment_id and not new_generated_image_id:
            raise UserError(_("A new version must have either a URL, an attachment, or an AI generated image linked."))

        default_vals = {
            'campaign_application_id': self.campaign_application_id.id,
            'submission_date': fields.Datetime.now(),
            'review_status': 'pending_review',
            'version': self.version + 1,
            'performance_data_json': None, # Reset performance data for new version
            'reviewed_by_user_id': False,
            'reviewed_at': False,
            'content_url': new_url,
            'content_attachment_id': new_attachment_id.id if new_attachment_id else False,
            'generated_image_id': new_generated_image_id.id if new_generated_image_id else False,
            'file_type': self.file_type # Or derive from new attachment
        }
        
        # Archive the current submission by changing its status or setting it inactive
        # self.write({'active': False, 'review_status': 'archived_ superseded'}) # Example of archiving

        new_submission = self.copy(default=default_vals)
        new_submission.message_post(body=_("New version (v%s) submitted, superseding v%s (ID: %s).") % (new_submission.version, self.version, self.id))
        self.message_post(body=_("This submission (v%s) has been superseded by new version v%s (ID: %s).") % (self.version, new_submission.version, new_submission.id))
        
        # Optionally, mark the old one as superseded or inactive
        self.write({'review_status': 'rejected'}) # Or a new 'superseded' status if defined

        return new_submission

    def name_get(self):
        """Custom display name."""
        result = []
        for submission in self:
            name = _("Submission v%s for %s (%s)") % (
                submission.version,
                submission.campaign_id.name or _('N/A'),
                submission.influencer_profile_id.full_name or _('N/A')
            )
            result.append((submission.id, name))
        return result

    def _send_status_notification(self, status, feedback=None):
        """Helper to send notification to influencer about status change."""
        # REQ-16-005
        # This should ideally call a mail template or a notification service
        # For now, this is a placeholder
        _logger.info(f"Sending notification for content submission ID {self.id}: Status {status}, Feedback: {feedback}")
        # Example:
        # template = self.env.ref('influence_gen_services.email_template_content_submission_update', raise_if_not_found=False)
        # if template and self.influencer_profile_id.email:
        #     template.with_context(feedback=feedback).send_mail(self.id, force_send=True)
        pass