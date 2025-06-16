# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class InfluenceGenCampaign(models.Model):
    _name = 'influence_gen.campaign'
    _description = "Marketing Campaign"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Campaign Name", required=True, index=True, tracking=True)
    description = fields.Text(string="Description")
    brand_client_id = fields.Many2one(
        'res.partner',
        string="Brand/Client",
        domain="[('is_company', '=', True)]"
    )
    goals_kpis = fields.Text(string="Goals and KPIs")
    target_influencer_criteria_json = fields.Text(
        string="Target Influencer Criteria (JSON)",
        help="e.g., niche, follower_count_min/max, engagement_rate_min"
    )
    content_requirements_text = fields.Text(
        string="Content Requirements",
        help="e.g., post type, key messages, hashtags, do's/don'ts"
    )
    budget = fields.Float(string="Campaign Budget", digits='Account')
    compensation_model_type = fields.Selection([
        ('flat_fee', 'Flat Fee'),
        ('commission', 'Commission-Based'),
        ('product_only', 'Product Only'),
        ('hybrid', 'Hybrid')
    ], string="Compensation Model Type", required=True)
    compensation_details = fields.Text(
        string="Compensation Model Details",
        help="e.g., flat fee amount, commission rate/structure"
    )
    submission_deadline_content = fields.Datetime(string="Content Submission Deadline")
    start_date = fields.Date(string="Campaign Start Date", required=True)
    end_date = fields.Date(string="Campaign End Date", required=True)
    usage_rights_description = fields.Text(string="Content Usage Rights")
    usage_rights_duration_months = fields.Integer(string="Usage Rights Duration (Months)")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('pending_review', 'Pending Review'), # Admin to review campaign setup before publishing
        ('published', 'Published/Open'),    # Open for applications
        ('in_progress', 'In Progress'),      # Applications closed, content being created/posted
        ('completed', 'Completed'),          # All activities finished, awaiting final metrics/payments
        ('archived', 'Archived'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', required=True, tracking=True, index=True)

    campaign_application_ids = fields.One2many('influence_gen.campaign_application', 'campaign_id', string="Applications")
    payment_record_ids = fields.One2many('influence_gen.payment_record', 'campaign_id', string="Payment Records")

    total_applications_count = fields.Integer(string="Total Applications", compute='_compute_campaign_counts', store=True)
    approved_applications_count = fields.Integer(string="Approved Applications", compute='_compute_campaign_counts', store=True)
    total_budget_allocated = fields.Float(string="Total Budget Allocated", compute='_compute_budget_metrics', digits='Account', store=True)
    actual_performance_metrics_json = fields.Text(string="Actual Performance Metrics (JSON)")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Campaign name must be unique!')
    ]

    @api.constrains('start_date', 'end_date', 'submission_deadline_content')
    def _check_dates(self) -> None:
        """
        Validate date logic. REQ-DMG-016.
        """
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("Campaign End Date cannot be before Start Date."))
            if record.submission_deadline_content and record.end_date and \
               fields.Datetime.to_datetime(record.submission_deadline_content).date() > record.end_date:
                raise ValidationError(_("Content Submission Deadline cannot be after Campaign End Date."))
            # if record.submission_deadline_content and record.start_date and \
            #    fields.Datetime.to_datetime(record.submission_deadline_content).date() < record.start_date:
            #     raise ValidationError(_("Content Submission Deadline cannot be before Campaign Start Date."))

    @api.depends('campaign_application_ids', 'campaign_application_ids.status')
    def _compute_campaign_counts(self) -> None:
        for campaign in self:
            campaign.total_applications_count = len(campaign.campaign_application_ids)
            campaign.approved_applications_count = len(campaign.campaign_application_ids.filtered(lambda app: app.status == 'approved'))

    @api.depends('payment_record_ids.amount', 'payment_record_ids.status')
    def _compute_budget_metrics(self) -> None:
        for campaign in self:
            # Simplified: considers payments not failed or cancelled.
            # Real allocation might involve committed amounts from approved applications
            # with specific compensation details.
            valid_payments = campaign.payment_record_ids.filtered(
                lambda p: p.status not in ('failed', 'cancelled')
            )
            campaign.total_budget_allocated = sum(valid_payments.mapped('amount'))

    def _log_status_change(self, new_status: str, old_status: str):
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_STATUS_CHANGE',
            actor_user_id=self.env.user.id,
            action_performed=f'STATUS_CHANGE_{old_status.upper()}_TO_{new_status.upper()}',
            target_object=self,
            details_dict={'old_status': old_status, 'new_status': new_status}
        )

    def action_publish(self) -> None:
        for record in self:
            if record.status not in ['draft', 'pending_review']:
                raise UserError(_("Only campaigns in 'Draft' or 'Pending Review' status can be published."))
            old_status = record.status
            record.write({'status': 'published'})
            record._log_status_change('published', old_status)
            # Potentially notify relevant users/groups

    def action_set_in_progress(self) -> None:
        for record in self:
            if record.status not in ['published']: # Can also move from pending_review if admin starts it early
                raise UserError(_("Campaign must be 'Published' to set to 'In Progress'."))
            old_status = record.status
            record.write({'status': 'in_progress'})
            record._log_status_change('in_progress', old_status)

    def action_complete(self) -> None:
        for record in self:
            if record.status not in ['in_progress']:
                raise UserError(_("Campaign must be 'In Progress' to be marked as 'Completed'."))
            old_status = record.status
            record.write({'status': 'completed'})
            record._log_status_change('completed', old_status)
            # Potentially trigger final payment calculations or reporting

    def action_archive(self) -> None:
        for record in self:
            # Typically completed or cancelled campaigns can be archived
            if record.status not in ['completed', 'cancelled']:
                 raise UserError(_("Only 'Completed' or 'Cancelled' campaigns can be archived."))
            old_status = record.status
            record.write({'status': 'archived'})
            record._log_status_change('archived', old_status)


    def action_cancel(self) -> None:
        for record in self:
            if record.status in ['completed', 'archived', 'cancelled']:
                raise UserError(_("Campaign is already %s and cannot be cancelled.", record.status))
            old_status = record.status
            record.write({'status': 'cancelled'})
            record._log_status_change('cancelled', old_status)
            # Notify applicants, handle pending payments etc.

    def add_manual_performance_metric(self, metric_name: str, metric_value, influencer_id: int = None, submission_id: int = None) -> None:
        """
        Allows admins to manually input performance data. REQ-2-011.
        """
        self.ensure_one()
        try:
            metrics = json.loads(self.actual_performance_metrics_json or '{}')
        except json.JSONDecodeError:
            metrics = {}

        # Structure JSON to allow per-influencer/submission metrics
        # Example: metrics['overall'][metric_name] = metric_value
        #          metrics['by_influencer'][influencer_id][metric_name] = metric_value
        # For simplicity, let's add to a general list or a top-level key
        
        key = metric_name
        if influencer_id:
            key = f"influencer_{influencer_id}_{metric_name}"
        elif submission_id:
            key = f"submission_{submission_id}_{metric_name}"
        
        metrics[key] = metric_value
        self.write({'actual_performance_metrics_json': json.dumps(metrics)})

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_PERFORMANCE_METRIC_ADDED',
            actor_user_id=self.env.user.id,
            action_performed='ADD_METRIC',
            target_object=self,
            details_dict={
                'metric_name': metric_name,
                'metric_value': metric_value,
                'influencer_id': influencer_id,
                'submission_id': submission_id
            }
        )