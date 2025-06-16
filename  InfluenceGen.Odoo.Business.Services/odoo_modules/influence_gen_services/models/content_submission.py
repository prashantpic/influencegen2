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
        'submission_id', 'attachment_id',
        string="Content Files"
    )
    content_link = fields.Char(string="Link to Content (e.g., social media post)")
    content_text_caption = fields.Text(string="Text/Caption")
    generated_image_id = fields.Many2one(
        'influence_gen.generated_image',
        string="Associated AI Generated Image",
        ondelete='set null' # Keep submission even if image deleted by retention
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
    version = fields.Integer(string="Version", default=1, readonly=True, copy=False) # Do not copy version for new submissions
    
    feedback_history_ids = fields.One2many(
        'influence_gen.content_feedback',
        'content_submission_id',
        string="Feedback History"
    )
    is_final_submission = fields.Boolean(string="Is Final Submission?", default=False, help="Indicates if this is the final approved version triggering payment eligibility.")

    @api.depends('campaign_id.name', 'influencer_profile_id.name', 'submission_date', 'version')
    def _compute_name(self) -> None:
        for sub in self:
            date_str = fields.Datetime.to_string(sub.submission_date) if sub.submission_date else 'N/A'
            sub.name = f"{sub.campaign_id.name or ''} - {sub.influencer_profile_id.name or ''} - V{sub.version} ({date_str})"

    def _create_feedback_record(self, reviewer_user_id: int, feedback_text: str):
        self.ensure_one()
        return self.env['influence_gen.content_feedback'].create({
            'content_submission_id': self.id,
            'reviewer_user_id': reviewer_user_id,
            'feedback_text': feedback_text,
        })

    def action_approve(self, reviewer_user_id: int) -> None:
        """
        Approves content. Called by CampaignService. REQ-2-010.
        """
        self.ensure_one()
        if self.review_status not in ['pending_review', 'revision_requested']:
            raise UserError(_("Content can only be approved if 'Pending Review' or 'Revision Requested'."))

        self.write({
            'review_status': 'approved',
            'reviewed_by_user_id': reviewer_user_id,
            'reviewed_at': fields.Datetime.now(),
            'is_final_submission': True # Default assumption, can be overridden by more complex logic
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_APPROVED',
            actor_user_id=reviewer_user_id,
            action_performed='APPROVE_CONTENT',
            target_object=self
        )
        # Trigger notification "Content Approved" to influencer
        self.env['influence_gen_integration.notification_service'].send_notification(
            user_id=self.influencer_profile_id.user_id.id,
            message_type='content_approved',
            title=_("Content Approved for %s", self.campaign_id.name),
            message_body=_("Your content submission for campaign '%s' (Version %s) has been approved!", self.campaign_id.name, self.version)
        )
        # Potentially trigger payment record creation via PaymentService if is_final_submission
        if self.is_final_submission:
            # self.env['influence_gen.services.payment_service'](self.env).create_payment_for_submission(self.id)
            pass # This logic is usually in the service layer

    def action_reject(self, reviewer_user_id: int, feedback_text: str) -> None:
        """
        Rejects content. REQ-2-010.
        """
        self.ensure_one()
        if not feedback_text:
            raise UserError(_("Feedback is required for rejecting content."))
        if self.review_status not in ['pending_review', 'revision_requested']:
            raise UserError(_("Content can only be rejected if 'Pending Review' or 'Revision Requested'."))

        self.write({
            'review_status': 'rejected',
            'reviewed_by_user_id': reviewer_user_id,
            'reviewed_at': fields.Datetime.now(),
            'is_final_submission': False
        })
        self._create_feedback_record(reviewer_user_id, feedback_text)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_REJECTED',
            actor_user_id=reviewer_user_id,
            action_performed='REJECT_CONTENT',
            target_object=self,
            details_dict={'feedback': feedback_text}
        )
        # Trigger notification "Content Rejected" to influencer
        self.env['influence_gen_integration.notification_service'].send_notification(
            user_id=self.influencer_profile_id.user_id.id,
            message_type='content_rejected',
            title=_("Content Submission Update for %s", self.campaign_id.name),
            message_body=_("Your content submission for campaign '%s' (Version %s) was rejected. Feedback: %s", self.campaign_id.name, self.version, feedback_text)
        )

    def action_request_revision(self, reviewer_user_id: int, feedback_text: str) -> None:
        """
        Requests revision. REQ-2-010.
        """
        self.ensure_one()
        if not feedback_text:
            raise UserError(_("Feedback is required for requesting a revision."))
        if self.review_status not in ['pending_review']: # Cannot request revision on already revised/rejected/approved item
            raise UserError(_("Revision can only be requested for content that is 'Pending Review'."))

        self.write({
            'review_status': 'revision_requested',
            'reviewed_by_user_id': reviewer_user_id,
            'reviewed_at': fields.Datetime.now(),
            'is_final_submission': False
        })
        self._create_feedback_record(reviewer_user_id, feedback_text)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_REVISION_REQUESTED',
            actor_user_id=reviewer_user_id,
            action_performed='REQUEST_REVISION',
            target_object=self,
            details_dict={'feedback': feedback_text}
        )
        # Trigger notification "Revision Requested" to influencer
        self.env['influence_gen_integration.notification_service'].send_notification(
            user_id=self.influencer_profile_id.user_id.id,
            message_type='content_revision_requested',
            title=_("Revision Requested for Content on %s", self.campaign_id.name),
            message_body=_("A revision has been requested for your content submission for campaign '%s' (Version %s). Feedback: %s", self.campaign_id.name, self.version, feedback_text)
        )

    def create_new_version_for_revision(self, new_content_data: dict) -> models.Model :
        """
        Creates a new submission record for a revision.
        `new_content_data` should contain fields like 'content_attachment_ids_commands',
        'content_link', 'content_text_caption', 'generated_image_id'.
        """
        self.ensure_one()
        if self.review_status not in ['revision_requested', 'rejected']: # Allow resubmission if rejected too
            raise UserError(_("A new version can only be submitted if the current status is 'Revision Requested' or 'Rejected'."))

        default_vals = {
            'campaign_application_id': self.campaign_application_id.id,
            'version': self.version + 1,
            'submission_date': fields.Datetime.now(),
            'review_status': 'pending_review',
            'is_final_submission': False,
            # Copy other relevant fields if necessary, or let them be default
        }
        
        # Prepare content data
        vals = default_vals.copy()
        vals.update({
            'content_link': new_content_data.get('content_link'),
            'content_text_caption': new_content_data.get('content_text_caption'),
            'generated_image_id': new_content_data.get('generated_image_id'),
        })
        
        # Handle M2M for attachments if provided
        # Example: new_content_data.get('content_attachment_ids_commands') could be [(6,0, [new_attach_ids])]
        if 'content_attachment_ids_commands' in new_content_data:
             vals['content_attachment_ids'] = new_content_data['content_attachment_ids_commands']


        new_submission = self.create(vals)

        # Optionally mark the old one as superseded or archive it
        # self.write({'review_status': 'superseded_by_v' + str(new_submission.version)})
        
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CONTENT_SUBMISSION_NEW_VERSION',
            actor_user_id=self.influencer_profile_id.user_id.id,
            action_performed='CREATE_NEW_VERSION',
            target_object=new_submission,
            details_dict={'previous_submission_id': self.id, 'previous_version': self.version}
        )
        return new_submission