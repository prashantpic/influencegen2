# -*- coding: utf-8 -*-
import json
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class InfluenceGenCampaign(models.Model):
    _name = 'influence_gen.campaign'
    _description = "Marketing Campaign"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Campaign Name", required=True, index=True, tracking=True)
    description = fields.Text(string="Description")
    brand_client_id = fields.Many2one(
        'res.partner', string="Brand/Client",
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

    campaign_application_ids = fields.One2many(
        'influence_gen.campaign_application', 'campaign_id', string="Applications"
    )
    payment_record_ids = fields.One2many(
        'influence_gen.payment_record', 'campaign_id', string="Payment Records"
    )

    total_applications_count = fields.Integer(
        string="Total Applications", compute='_compute_campaign_counts', store=True
    )
    approved_applications_count = fields.Integer(
        string="Approved Applications", compute='_compute_campaign_counts', store=True
    )
    total_budget_allocated = fields.Float(
        string="Total Budget Allocated", compute='_compute_budget_metrics',
        digits='Account', store=True # Simplified, might need more complex logic for store
    )
    actual_performance_metrics_json = fields.Text(string="Actual Performance Metrics (JSON)")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Campaign name must be unique!')
    ]

    @api.constrains('start_date', 'end_date', 'submission_deadline_content')
    def _check_dates(self):
        """Validate date logic. REQ-DMG-016."""
        for campaign in self:
            if campaign.start_date and campaign.end_date and campaign.end_date < campaign.start_date:
                raise ValidationError(_("Campaign End Date cannot be before Start Date."))
            if campaign.submission_deadline_content and campaign.end_date and \
               campaign.submission_deadline_content > fields.Datetime.to_datetime(campaign.end_date):
                raise ValidationError(_("Content Submission Deadline cannot be after Campaign End Date."))
            # if campaign.submission_deadline_content and campaign.start_date and \
            #    campaign.submission_deadline_content < fields.Datetime.to_datetime(campaign.start_date):
            #     raise ValidationError(_("Content Submission Deadline should ideally be on or after Campaign Start Date."))


    @api.depends('campaign_application_ids', 'campaign_application_ids.status')
    def _compute_campaign_counts(self):
        for campaign in self:
            campaign.total_applications_count = len(campaign.campaign_application_ids)
            campaign.approved_applications_count = len(
                campaign.campaign_application_ids.filtered(lambda app: app.status == 'approved')
            )

    @api.depends('payment_record_ids.amount', 'payment_record_ids.status')
    def _compute_budget_metrics(self):
        for campaign in self:
            approved_payments = campaign.payment_record_ids.filtered(
                lambda p: p.status not in ('failed', 'cancelled')
            )
            campaign.total_budget_allocated = sum(approved_payments.mapped('amount'))

    def _log_status_change(self, new_status):
        self.ensure_one()
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_STATUS_CHANGED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE_STATUS',
            target_object=self,
            details_dict={'new_status': new_status, 'old_status': self.status}
        )

    def action_publish(self):
        """Sets campaign status to 'Published/Open'. REQ-2-001 related logic."""
        for campaign in self:
            if campaign.status not in ('draft', 'pending_review'):
                raise ValidationError(_("Only draft or pending review campaigns can be published."))
            old_status = campaign.status
            campaign.write({'status': 'published'})
            campaign._log_status_change('published')
        return True

    def action_set_in_progress(self):
        for campaign in self:
            if campaign.status != 'published':
                 raise ValidationError(_("Only published campaigns can be set to 'In Progress'."))
            old_status = campaign.status
            campaign.write({'status': 'in_progress'})
            campaign._log_status_change('in_progress')
        return True

    def action_complete(self):
        for campaign in self:
            if campaign.status != 'in_progress':
                raise ValidationError(_("Only 'In Progress' campaigns can be completed."))
            old_status = campaign.status
            campaign.write({'status': 'completed'})
            campaign._log_status_change('completed')
        return True

    def action_archive(self):
        for campaign in self:
            if campaign.status not in ('completed', 'cancelled'):
                raise ValidationError(_("Only completed or cancelled campaigns can be archived."))
            old_status = campaign.status
            campaign.write({'status': 'archived'})
            campaign._log_status_change('archived')
        return True

    def action_cancel(self):
        for campaign in self:
            # Add logic: check if there are ongoing activities that prevent cancellation
            if campaign.status in ('completed', 'archived', 'cancelled'):
                raise ValidationError(_("Campaign is already %s and cannot be cancelled.", campaign.status))
            old_status = campaign.status
            campaign.write({'status': 'cancelled'})
            campaign._log_status_change('cancelled')
            # Potentially notify applicants/participants
        return True

    def add_manual_performance_metric(self, metric_name, metric_value, influencer_id=None, submission_id=None):
        """Allows admins to manually input performance data. REQ-2-011."""
        self.ensure_one()
        metrics = json.loads(self.actual_performance_metrics_json or '{}')
        
        # Structure JSON to allow per-influencer/submission metrics if needed.
        # Example: metrics = {'general': {}, 'influencer_X': {}, 'submission_Y': {}}
        key_path = ['general'] # Default to general campaign metrics
        if influencer_id:
            key_path = [f'influencer_{influencer_id}']
        if submission_id: # Submission specific takes precedence
            key_path = [f'submission_{submission_id}']
        
        current_level = metrics
        for key_part in key_path[:-1]:
            current_level = current_level.setdefault(key_part, {})
        current_level[key_path[-1]] = current_level.get(key_path[-1], {})
        current_level[key_path[-1]][metric_name] = metric_value

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
        return True