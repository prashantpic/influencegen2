# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class InfluenceGenDataRetentionPolicy(models.Model):
    _name = 'influence_gen.data_retention_policy'
    _description = "Data Retention Policy"

    name = fields.Char(string="Policy Name", required=True)
    data_category = fields.Selection([
        ('pii_influencer', 'Influencer PII'),
        ('kyc_documents', 'KYC Documents'),
        ('social_media_profiles', 'Social Media Profiles (unverified)'),
        ('campaign_applications_rejected', 'Campaign Applications (Rejected/Withdrawn)'),
        ('campaign_data_inactive', 'Campaign Data (Inactive/Archived)'),
        ('content_submissions_rejected', 'Content Submissions (Rejected)'),
        ('ai_images_personal', 'AI Generated Images (Personal)'),
        ('ai_images_campaign_expired', 'AI Generated Images (Campaign Expired)'),
        ('payment_records_old', 'Payment Records (Old)'),
        ('audit_logs', 'Audit Logs'),
        ('platform_settings_log', 'Platform Settings Change Log'), # Example
        ('usage_logs_ai', 'AI Usage Logs'),
        # Add more specific categories as needed
    ], string="Data Category", required=True, index=True)
    
    model_name = fields.Char(
        string="Target Odoo Model Technical Name",
        help="e.g., 'influence_gen.influencer_profile'. Used by automated processes."
    )
    domain_filter = fields.Char(
        string="Domain Filter",
        default="[]",
        help="Odoo domain to select records for this policy. E.g., [('status','=','archived')]"
    )
    date_field_for_retention = fields.Char(
        string="Date Field for Retention",
        default="create_date",
        help="Technical name of the date field on the target model used to calculate retention period (e.g., 'create_date', 'write_date', 'end_date')."
    )
    retention_period_days = fields.Integer(
        string="Retention Period (Days)", required=True,
        help="Number of days data in this category should be actively retained from the date_field_for_retention."
    )
    disposition_action = fields.Selection([
        ('delete', 'Secure Delete'),
        ('anonymize', 'Anonymize'), # Anonymization needs model-specific logic
        ('archive', 'Archive (Set active=False)') # Odoo's default archive
    ], string="Disposition Action", required=True)
    
    is_active = fields.Boolean(string="Active Policy", default=True, index=True)
    description = fields.Text(string="Policy Description and Basis")
    legal_hold_overrideable = fields.Boolean(
        string="Overrideable by Legal Hold?", default=True,
        help="If False, this policy will be applied even if records are under legal hold (use with extreme caution)."
    )
    sequence = fields.Integer(string="Sequence", default=10, help="Order of execution for policies if overlap.")

    @api.model
    def get_active_policy(self, data_category=None, model_name=None):
        """Retrieves the active policy for a given category or model."""
        domain = [('is_active', '=', True)]
        if data_category:
            domain.append(('data_category', '=', data_category))
        if model_name:
            domain.append(('model_name', '=', model_name))
        
        # Return the first one found if multiple match (e.g. by sequence or most specific)
        return self.search(domain, order='sequence asc', limit=1)