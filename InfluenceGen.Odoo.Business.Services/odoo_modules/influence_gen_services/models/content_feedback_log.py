# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ContentFeedbackLog(models.Model):
    """
    Logs an instance of feedback provided on a content submission.
    This model maintains a historical log of all feedback provided during the review
    of a content submission, allowing for a full audit trail of the review process.
    It inherits from BaseAuditMixin to log creation events.
    REQ-DMG-006: Manages feedback related to content submissions.
    REQ-2-010: Stores feedback provided during content review.
    """
    _name = 'influence_gen.content_feedback_log'
    _description = 'Content Feedback Log'
    _inherit = ['influence_gen.base_audit_mixin']
    _order = 'timestamp desc'

    content_submission_id = fields.Many2one(
        'influence_gen.content_submission',
        string='Content Submission',
        required=True,
        ondelete='cascade',
        index=True,
        help="The content submission this feedback pertains to."
    )
    reviewer_user_id = fields.Many2one(
        'res.users',
        string='Reviewer',
        ondelete='set null',
        help="The user who provided this feedback."
    )
    feedback_text = fields.Text(
        string='Feedback',
        help="The actual feedback text provided by the reviewer."
    )
    timestamp = fields.Datetime(
        string='Timestamp',
        required=True,
        default=fields.Datetime.now,
        readonly=True,
        help="Date and time when the feedback was recorded."
    )