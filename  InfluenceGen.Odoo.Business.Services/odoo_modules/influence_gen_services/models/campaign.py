import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class InfluenceGenCampaign(models.Model):
    _name = 'influence_gen.campaign'
    _description = "Marketing Campaign"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc' # Default order, can be adjusted

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
    actual_performance_metrics_json = fields.Text(string="Actual Performance Metrics (JSON)")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Campaign name must be unique!')
    ]

    @api.constrains('start_date', 'end_date', 'submission_deadline_content')
    def _check_dates(self):
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
    def _compute_campaign_counts(self):
        for campaign in self:
            campaign.total_applications_count = len(campaign.campaign_application_ids)
            campaign.approved_applications_count = len(campaign.campaign_application_ids.filtered(lambda app: app.status == 'approved'))

    @api.depends('payment_record_ids.amount', 'payment_record_ids.status')
    def _compute_budget_metrics(self):
        for campaign in self:
            valid_payments = campaign.payment_record_ids.filtered(
                lambda p: p.status not in ('failed', 'cancelled')
            )
            campaign.total_budget_allocated = sum(valid_payments.mapped('amount'))

    def _log_status_change(self, old_status, new_status):
        self.ensure_one()
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_STATUS_CHANGED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'old_status': old_status, 'new_status': new_status, 'campaign_id': self.id}
        )

    def action_publish(self):
        for record in self:
            if record.status not in ('draft', 'pending_review'):
                raise ValidationError(_("Campaign can only be published from 'Draft' or 'Pending Review' state."))
            old_status = record.status
            record.status = 'published'
            record._log_status_change(old_status, 'published')
        return True

    def action_set_in_progress(self):
        for record in self:
            if record.status not in ('published'): # Or other valid states
                raise ValidationError(_("Campaign can only be set to 'In Progress' from 'Published' state."))
            old_status = record.status
            record.status = 'in_progress'
            record._log_status_change(old_status, 'in_progress')
        return True

    def action_complete(self):
        for record in self:
            if record.status not in ('in_progress'): # Or other valid states
                raise ValidationError(_("Campaign can only be completed from 'In Progress' state."))
            old_status = record.status
            record.status = 'completed'
            record._log_status_change(old_status, 'completed')
        return True

    def action_archive(self):
        for record in self:
            old_status = record.status
            record.status = 'archived'
            record._log_status_change(old_status, 'archived')
        return True

    def action_cancel(self):
        for record in self:
            # Add cancellation conditions if any (e.g., no active payments)
            old_status = record.status
            record.status = 'cancelled'
            record._log_status_change(old_status, 'cancelled')
        return True

    def add_manual_performance_metric(self, metric_name, metric_value, influencer_id=None, submission_id=None):
        self.ensure_one()
        try:
            metrics_data = json.loads(self.actual_performance_metrics_json or '{}')
        except json.JSONDecodeError:
            metrics_data = {}

        # Structure can be simple key-value or more complex
        if influencer_id:
            influencer_key = str(influencer_id.id if hasattr(influencer_id, 'id') else influencer_id)
            if influencer_key not in metrics_data:
                metrics_data[influencer_key] = {}
            if submission_id:
                submission_key = str(submission_id.id if hasattr(submission_id, 'id') else submission_id)
                if submission_key not in metrics_data[influencer_key]:
                    metrics_data[influencer_key][submission_key] = {}
                metrics_data[influencer_key][submission_key][metric_name] = metric_value
            else:
                metrics_data[influencer_key][metric_name] = metric_value
        else:
            metrics_data[metric_name] = metric_value

        self.actual_performance_metrics_json = json.dumps(metrics_data, indent=2)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_PERFORMANCE_METRIC_ADDED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={
                'campaign_id': self.id,
                'metric_name': metric_name,
                'metric_value': metric_value,
                'influencer_id': influencer_id.id if hasattr(influencer_id, 'id') else influencer_id,
                'submission_id': submission_id.id if hasattr(submission_id, 'id') else submission_id,
            }
        )
        return True