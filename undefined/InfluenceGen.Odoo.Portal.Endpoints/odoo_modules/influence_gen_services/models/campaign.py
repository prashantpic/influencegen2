# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class Campaign(models.Model):
    """
    Marketing Campaign Model
    Represents a marketing campaign with all its defining characteristics and operational status.
    This model defines and manages marketing campaigns, including their details,
    lifecycle, budgeting, compensation models, and associated data.
    Inherits mail.thread and mail.activity.mixin for communication and tracking,
    and BaseAuditMixin for audit logging.
    REQ-DMG-004, REQ-2-001, REQ-2-002, REQ-2-003, REQ-2-017, REQ-IPF-003
    """
    _name = 'influence_gen.campaign'
    _description = 'Marketing Campaign'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'influence_gen.base_audit_mixin']
    _order = 'start_date desc, name'

    name = fields.Char(
        string='Name', 
        required=True, 
        index=True, 
        tracking=True,
        help="Unique name of the marketing campaign."
    )
    description = fields.Text(
        string='Description', 
        tracking=True,
        help="Detailed description of the campaign."
    )
    brand_client = fields.Char(
        string='Brand/Client', 
        tracking=True,
        help="The brand or client for whom the campaign is run."
    )
    goals = fields.Text(
        string='Goals', 
        tracking=True,
        help="Objectives and goals of the campaign."
    )
    kpi_ids = fields.One2many(
        comodel_name='influence_gen.campaign_kpi', 
        inverse_name='campaign_id', 
        string='KPIs',
        help="Key Performance Indicators for this campaign."
    )
    target_criteria_json = fields.Text(
        string='Target Criteria (JSON)', 
        help="JSON string defining target influencer criteria (e.g., audience niche, location, follower count)."
    )
    content_requirements = fields.Text(
        string='Content Requirements', 
        tracking=True,
        help="Specific requirements for the content to be created by influencers."
    )
    budget = fields.Monetary(
        string='Budget', 
        currency_field='currency_id', 
        tracking=True,
        help="Total budget allocated for the campaign."
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency', 
        string='Currency', 
        default=lambda self: self.env.company.currency_id, 
        required=True,
        help="Currency for the campaign budget and financial transactions."
    )
    compensation_model_type = fields.Selection([
        ('flat_fee', 'Flat Fee'),
        ('cpm', 'Cost Per Mille (CPM)'),
        ('cpa', 'Cost Per Acquisition (CPA)'),
        ('commission', 'Commission-based'),
        ('hybrid', 'Hybrid (Mixed)'),
        ('product_only', 'Product/Service Only'),
        ('other', 'Other')
        ], 
        string='Compensation Model Type', 
        tracking=True,
        help="Type of compensation model used for influencers in this campaign."
    )
    compensation_details = fields.Text(
        string='Compensation Details', 
        help="Detailed explanation of the compensation structure, rates, and terms."
    )
    submission_deadline = fields.Datetime(
        string='Submission Deadline', 
        tracking=True,
        help="Deadline for influencers to submit their content."
    )
    start_date = fields.Date(
        string='Start Date', 
        tracking=True, 
        required=True,
        index=True,
        help="The official start date of the campaign."
    )
    end_date = fields.Date(
        string='End Date', 
        tracking=True, 
        required=True,
        index=True,
        help="The official end date of the campaign."
    )
    usage_rights = fields.Text(
        string='Usage Rights', 
        tracking=True,
        help="Details on the usage rights for the content submitted by influencers."
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'), # Added for potential approval workflow
        ('published', 'Published'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
        ('cancelled', 'Cancelled') # Added for campaigns that don't proceed
        ], 
        string='Status', 
        default='draft', 
        required=True, 
        tracking=True, 
        index=True,
        copy=False,
        help="Current status of the campaign lifecycle."
    )
    campaign_application_ids = fields.One2many(
        comodel_name='influence_gen.campaign_application', 
        inverse_name='campaign_id', 
        string='Applications',
        help="Applications received from influencers for this campaign."
    )
    payment_record_ids = fields.One2many(
        comodel_name='influence_gen.payment_record', 
        inverse_name='campaign_id', 
        string='Payment Records',
        help="Payment records associated with this campaign."
    )
    active = fields.Boolean(
        string='Active', 
        default=True, 
        help="Set to false to hide the campaign without deleting it. Archived campaigns are typically inactive."
    )
    company_id = fields.Many2one(
        comodel_name='res.company', 
        string='Company', 
        default=lambda self: self.env.company, 
        required=True,
        help="Company to which this campaign belongs."
    )
    user_id = fields.Many2one(
        'res.users', 
        string='Campaign Manager', 
        default=lambda self: self.env.user,
        tracking=True,
        help="User responsible for managing this campaign."
    )

    _sql_constraints = [
        ('name_company_unique', 'UNIQUE(name, company_id)', 'Campaign name must be unique per company.'),
    ]

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Ensures that the end date is not earlier than the start date."""
        for campaign in self:
            if campaign.start_date and campaign.end_date and campaign.end_date < campaign.start_date:
                raise ValidationError(_('The campaign end date cannot be earlier than the start date.'))

    def action_publish(self):
        """Sets the campaign status to 'Published'."""
        self.ensure_one()
        if self.status not in ['draft', 'pending_approval', 'cancelled']:
             raise ValidationError(_("Campaign can only be published from Draft, Pending Approval or Cancelled state."))
        self.status = 'published'
        self.message_post(body=_("Campaign '%s' has been published.") % self.name)
        # Potentially send notifications to relevant user groups or trigger other actions

    def action_start_progress(self):
        """Sets the campaign status to 'In Progress'."""
        self.ensure_one()
        if self.status not in ['published']:
            raise ValidationError(_("Campaign can only be started from Published state."))
        self.status = 'in_progress'
        self.message_post(body=_("Campaign '%s' is now in progress.") % self.name)

    def action_complete(self):
        """Sets the campaign status to 'Completed'."""
        self.ensure_one()
        if self.status not in ['in_progress']:
            raise ValidationError(_("Campaign can only be completed from In Progress state."))
        self.status = 'completed'
        self.message_post(body=_("Campaign '%s' has been completed.") % self.name)
        # Trigger final payment calculations or performance reviews

    def action_archive(self):
        """Sets the campaign status to 'Archived' and deactivates it."""
        self.ensure_one()
        self.status = 'archived'
        self.active = False
        self.message_post(body=_("Campaign '%s' has been archived.") % self.name)

    def action_cancel(self):
        """Sets the campaign status to 'Cancelled'."""
        self.ensure_one()
        if self.status in ['completed', 'archived', 'in_progress']:
             raise ValidationError(_("Cannot cancel a campaign that is already in progress, completed or archived."))
        self.status = 'cancelled'
        self.message_post(body=_("Campaign '%s' has been cancelled.") % self.name)

    def action_reset_to_draft(self):
        """Resets a campaign (e.g., from 'Cancelled' or 'Pending Approval') back to 'Draft'."""
        self.ensure_one()
        if self.status not in ['pending_approval', 'cancelled']:
            raise ValidationError(_("Campaign can only be reset to draft from Pending Approval or Cancelled state."))
        self.status = 'draft'
        self.active = True # Ensure it's active if reset
        self.message_post(body=_("Campaign '%s' has been reset to draft.") % self.name)

    def calculate_aggregated_kpis(self):
        """
        Calculates and returns aggregated Key Performance Indicators (KPIs) for the campaign.
        This could involve summing target/actual values from kpi_ids or
        aggregating performance data from related ContentSubmissions.
        """
        self.ensure_one()
        aggregated_data = {
            'total_target_value': 0.0,
            'total_actual_value': 0.0,
            'kpi_details': []
        }
        for kpi in self.kpi_ids:
            aggregated_data['total_target_value'] += kpi.target_value
            aggregated_data['total_actual_value'] += kpi.actual_value
            aggregated_data['kpi_details'].append({
                'name': kpi.name,
                'target': kpi.target_value,
                'actual': kpi.actual_value,
                'unit': kpi.unit_of_measure
            })
        
        # Further aggregation could happen here based on ContentSubmission.performance_data_json
        # For example, summing up reach, engagement, etc. from all approved submissions.
        # This part requires a clear definition of how performance_data_json is structured.
        _logger.info("Aggregated KPIs for campaign %s: %s", self.name, aggregated_data)
        return aggregated_data