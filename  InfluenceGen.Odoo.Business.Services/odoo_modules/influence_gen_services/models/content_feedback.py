# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

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
        readonly=True # Set by system based on who performs action
    )
    feedback_text = fields.Text(string="Feedback", required=True)
    # create_date is an Odoo default field, can be used as "Feedback Date"
    # It will be automatically set to fields.Datetime.now by default upon creation.
    # If explicitly named:
    # feedback_date = fields.Datetime(string="Feedback Date", default=fields.Datetime.now, readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'reviewer_user_id' not in vals: # Auto-set reviewer if not provided (e.g. if created from code)
                vals['reviewer_user_id'] = self.env.user.id
        return super(InfluenceGenContentFeedback, self).create(vals_list)