# -*- coding: utf-8 -*-
from odoo import models, fields, api

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
        readonly=True
    )
    feedback_text = fields.Text(
        string="Feedback",
        required=True
    )
    create_date = fields.Datetime(
        string="Feedback Date",
        default=fields.Datetime.now, # Odoo default, but specified in SDS
        readonly=True
    )