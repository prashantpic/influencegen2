from odoo import api, fields, models, _

class InfluenceGenContentFeedback(models.Model):
    _name = 'influence_gen.content_feedback'
    _description = "Feedback on Content Submission"
    _order = 'create_date desc'

    content_submission_id = fields.Many2one(
        'influence_gen.content_submission',
        string="Content Submission",
        required=True,
        ondelete='cascade',
        index=True
    )
    reviewer_user_id = fields.Many2one(
        'res.users',
        string="Reviewer",
        required=True,
        readonly=True,
        # As per SDS, default=lambda self: self.env.user - but this makes it editable unless readonly.
        # Logic for setting this should be in the calling method (e.g. content_submission actions)
    )
    feedback_text = fields.Text(
        string="Feedback",
        required=True
    )
    # create_date is an Odoo default field, no need to redefine unless attributes change
    # It's listed in SDS with default=fields.Datetime.now, readonly=True, which are Odoo defaults.
    # We can rely on the default 'create_date' field.
    # If explicit control is needed for some reason not apparent:
    # create_date = fields.Datetime(string="Feedback Date", default=fields.Datetime.now, readonly=True)

    # REQ-2-010: This model supports the feedback mechanism for content review.
    # REQ-DMG-001, REQ-DMG-006: Data management aspects are handled by its existence and relation to content_submission.

    # No specific methods defined in SDS for this model, beyond standard ORM capabilities.
    # Logic for creating feedback records is typically in the `content_submission` model's
    # `action_reject` or `action_request_revision` methods.