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
    target_influencer_criteria_json = fields.Text(string="Target Influencer Criteria (JSON)")
    content_requirements_text = fields.Text(string="Content Requirements")
    budget = fields.Float(string="Campaign Budget", digits='Account')
    compensation_model_type = fields.Selection([
        ('flat_fee', 'Flat Fee'),
        ('commission', 'Commission-Based'),
        ('product_only', 'Product Only'),
        ('hybrid', 'Hybrid')
    ], string="Compensation Model Type", required=True)
    compensation_details = fields.Text(string="Compensation Model Details")
    submission_deadline_content = fields.Datetime(string="Content Submission Deadline")
    start_date = fields.Date(string="Campaign Start Date", required=True)
    end_date = fields.Date(string="Campaign End Date", required=True)
    usage_rights_description = fields.Text(string="Content Usage Rights")
    usage_rights_duration_months = fields.Integer(string="Usage Rights Duration (Months)")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('pending_review', 'Pending Review'),
        ('published', 'Published/Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', required=True, tracking=True, index=True)

    campaign_application_ids = fields.One2many('influence_gen.campaign_application', 'campaign_id', string="Applications")
    payment_record_ids = fields.One2many('influence_gen.payment_record', 'campaign_id', string="Payment Records")

    total_applications_count = fields.Integer(string="Total Applications", compute='_compute_campaign_counts', store=True)
    approved_applications_count = fields.Integer(string="Approved Applications", compute='_compute_campaign_counts', store=True)
    total_budget_allocated = fields.Float(string="Total Budget Allocated", compute='_compute_budget_metrics', digits='Account', store=True)
    actual_performance_metrics_json = fields.Text(string="Actual Performance Metrics (JSON)", default="{}")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Campaign name must be unique!')
    ]

    @api.constrains('start_date', 'end_date', 'submission_deadline_content')
    def _check_dates(self):
        """Validate date logic. REQ-DMG-016."""
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError(_("Campaign End Date cannot be before Start Date."))
            if record.submission_deadline_content and record.end_date and \
               fields.Datetime.to_datetime(record.submission_deadline_content).date() > record.end_date:
                raise ValidationError(_("Content Submission Deadline cannot be after Campaign End Date."))
            # if record.submission_deadline_content and record.start_date and \
            #    fields.Datetime.to_datetime(record.submission_deadline_content).date() < record.start_date:
            #     raise ValidationError(_("Content Submission Deadline should ideally be on or after the Campaign Start Date."))


    @api.depends('campaign_application_ids', 'campaign_application_ids.status')
    def _compute_campaign_counts(self):
        for record in self:
            record.total_applications_count = len(record.campaign_application_ids)
            record.approved_applications_count = len(record.campaign_application_ids.filtered(lambda app: app.status == 'approved'))

    @api.depends('payment_record_ids.amount', 'payment_record_ids.status')
    def _compute_budget_metrics(self):
        for record in self:
            valid_payments = record.payment_record_ids.filtered(lambda p: p.status not in ['failed', 'cancelled'])
            record.total_budget_allocated = sum(valid_payments.mapped('amount'))

    def _log_status_change(self, new_status, old_status=None):
        self.ensure_one()
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_STATUS_CHANGED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'old_status': old_status or self._origin.status if self._origin else 'N/A', 'new_status': new_status}
        )

    def action_publish(self):
        for record in self:
            if record.status not in ['draft', 'pending_review']:
                 raise ValidationError(_("Campaign can only be published from 'Draft' or 'Pending Review' state."))
            old_status = record.status
            record.status = 'published'
            record._log_status_change('published', old_status)
        return True

    def action_set_in_progress(self):
        for record in self:
            if record.status not in ['published']:
                raise ValidationError(_("Campaign can only be set to 'In Progress' from 'Published' state."))
            old_status = record.status
            record.status = 'in_progress'
            record._log_status_change('in_progress', old_status)
        return True

    def action_complete(self):
        for record in self:
            if record.status not in ['in_progress']:
                 raise ValidationError(_("Campaign can only be completed from 'In Progress' state."))
            old_status = record.status
            record.status = 'completed'
            record._log_status_change('completed', old_status)
        return True

    def action_archive(self):
        for record in self:
            # Typically, completed or cancelled campaigns can be archived
            if record.status not in ['completed', 'cancelled', 'draft']:
                raise ValidationError(_("Campaign can only be archived if it's 'Completed', 'Cancelled' or 'Draft'."))
            old_status = record.status
            record.status = 'archived' # Or use active=False if preferred for Odoo standard archival
            record._log_status_change('archived', old_status)
        return True

    def action_cancel(self):
        for record in self:
            # Campaigns can be cancelled unless already completed or archived.
            if record.status in ['completed', 'archived', 'cancelled']:
                raise ValidationError(_("Campaign cannot be cancelled if it's already '%s'.") % record.status)
            old_status = record.status
            record.status = 'cancelled'
            record._log_status_change('cancelled', old_status)
            # Potentially notify applicants/participants
        return True

    def add_manual_performance_metric(self, metric_name, metric_value, influencer_id=None, submission_id=None):
        """Allows admins to manually input performance data. REQ-2-011."""
        self.ensure_one()
        try:
            metrics = json.loads(self.actual_performance_metrics_json or '{}')
        except json.JSONDecodeError:
            metrics = {}

        # Structure JSON to allow per-influencer/submission metrics if needed
        # Example: metrics['overall'][metric_name] = metric_value
        # Example: metrics['influencer_specific'][influencer_id][metric_name] = metric_value
        # For simplicity, using a basic overall structure for now
        if influencer_id:
            metrics.setdefault('by_influencer', {}).setdefault(str(influencer_id), {})[metric_name] = metric_value
        elif submission_id:
            metrics.setdefault('by_submission', {}).setdefault(str(submission_id), {})[metric_name] = metric_value
        else:
            metrics.setdefault('overall_metrics', {})[metric_name] = metric_value
        
        self.actual_performance_metrics_json = json.dumps(metrics)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_PERFORMANCE_METRIC_ADDED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={
                'metric_name': metric_name,
                'metric_value': metric_value,
                'influencer_id': influencer_id,
                'submission_id': submission_id
            }
        )
        return True