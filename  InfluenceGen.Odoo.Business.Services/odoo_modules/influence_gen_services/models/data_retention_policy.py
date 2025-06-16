# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class InfluenceGenDataRetentionPolicy(models.Model):
    _name = 'influence_gen.data_retention_policy'
    _description = "Data Retention Policy"

    name = fields.Char(string="Policy Name", required=True)
    data_category = fields.Selection([
        ('pii_influencer', 'Influencer PII'),
        ('kyc_documents', 'KYC Documents'),
        ('social_media_profiles', 'Social Media Profiles'),
        ('bank_accounts', 'Bank Accounts'),
        ('terms_consents', 'Terms Consents'),
        ('campaign_data', 'Campaign Data (General)'),
        ('campaign_applications', 'Campaign Applications'),
        ('content_submissions', 'Content Submissions'),
        ('ai_image_requests', 'AI Image Requests'),
        ('generated_images_personal', 'Generated Images (Personal)'),
        ('generated_images_campaign', 'Generated Images (Campaign)'),
        ('payment_records', 'Payment Records'),
        ('audit_logs', 'Audit Logs'),
        ('platform_settings_history', 'Platform Settings History'), # If versioning settings
        ('n8n_interaction_logs', 'N8N Interaction Logs'), # If stored in Odoo
        ('system_operational_logs', 'System Operational Logs') # If stored in Odoo
        # Add more specific categories as needed
    ], string="Data Category", required=True, index=True)
    
    model_name = fields.Char(
        string="Target Odoo Model Technical Name",
        help="e.g., 'influence_gen.influencer_profile'. Used by DataManagementService to find records."
    )
    retention_period_days = fields.Integer(
        string="Retention Period (Days)",
        required=True,
        help="Number of days data in this category should be actively retained from its creation or relevant event date."
    )
    disposition_action = fields.Selection([
        ('delete', 'Secure Delete'),
        ('anonymize', 'Anonymize'),
        ('archive', 'Archive') # May involve moving to cold storage or setting 'active=False'
    ], string="Disposition Action", required=True)
    is_active = fields.Boolean(string="Active Policy", default=True, index=True)
    description = fields.Text(string="Policy Description and Basis", help="Details about the policy, its purpose, and legal/business reasons.")
    legal_hold_overrideable = fields.Boolean(
        string="Overrideable by Legal Hold?",
        default=True,
        help="If False, this policy might still apply even if data is under legal hold (use with extreme caution)."
    )

    @api.model
    def get_active_policy(cls, data_category=None, model_name=None):
        """Retrieves the active policy for a given category or model.
           Prefers data_category if both are provided.
        """
        domain = [('is_active', '=', True)]
        if data_category:
            domain.append(('data_category', '=', data_category))
        elif model_name:
            domain.append(('model_name', '=', model_name))
        else: # Either category or model name must be provided
            return cls.env['influence_gen.data_retention_policy'] # Return empty recordset

        # It's possible multiple policies could match (e.g. for same category)
        # Add ordering or further logic if a single definitive policy is needed
        policies = cls.search(domain, order='id asc') # Example order
        return policies[0] if policies else cls.env['influence_gen.data_retention_policy']