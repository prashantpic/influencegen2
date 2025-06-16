# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class InfluenceGenDataRetentionPolicy(models.Model):
    _name = 'influence_gen.data_retention_policy'
    _description = "Data Retention Policy"

    name = fields.Char(string="Policy Name", required=True)
    data_category = fields.Selection([
        # Granular categories matching various data types
        ('pii_influencer', 'Influencer PII (Profile)'),
        ('kyc_documents', 'KYC Documents & Data'),
        ('bank_details', 'Influencer Bank Details'),
        ('terms_consent', 'Terms of Service Consents'),
        ('social_media_profiles', 'Social Media Profiles (Non-verified)'),
        ('campaign_general', 'Campaign General Data (Definition, Goals)'),
        ('campaign_applications', 'Campaign Applications (Non-Approved)'),
        ('campaign_applications_approved', 'Campaign Applications (Approved)'),
        ('content_submissions_draft', 'Content Submissions (Draft/Rejected)'),
        ('content_submissions_approved', 'Content Submissions (Approved)'),
        ('ai_requests', 'AI Image Generation Requests'),
        ('ai_images_personal', 'AI Generated Images (Personal Use)'),
        ('ai_images_campaign', 'AI Generated Images (Campaign Use)'),
        ('payment_records_pending', 'Payment Records (Pending/Failed)'),
        ('payment_records_paid', 'Payment Records (Paid)'),
        ('audit_logs', 'System Audit Logs'),
        ('notification_logs', 'Notification Logs'), # Assuming a model for this might exist
        ('system_configs', 'Platform Settings History'), # If versioning settings
        ('other_transient', 'Other Transient Data')
    ], string="Data Category", required=True, index=True)
    
    model_name = fields.Char(
        string="Target Odoo Model Technical Name", 
        help="e.g., 'influence_gen.influencer_profile'. Optional if policy is category-driven across models."
    )
    retention_period_days = fields.Integer(
        string="Retention Period (Days)", 
        required=True, 
        help="Number of days data in this category should be actively retained. 0 means indefinite or managed by other means."
    )
    disposition_action = fields.Selection([
        ('delete', 'Secure Delete'),    # Hard delete
        ('anonymize', 'Anonymize'),     # Remove/Obfuscate PII
        ('archive', 'Archive')          # Set active=False or move to cold storage (conceptual)
    ], string="Disposition Action", required=True)
    
    is_active = fields.Boolean(string="Active Policy", default=True, index=True)
    description = fields.Text(string="Policy Description and Basis", help="e.g., Legal requirement, business need.")
    
    legal_hold_overrideable = fields.Boolean(
        string="Overrideable by Legal Hold?", 
        default=True,
        help="If False, this policy might still apply even if data is under legal hold (use with extreme caution)."
    )

    @api.model
    def get_active_policy(self, data_category: str = None, model_name: str = None) -> models.Model:
        """
        Retrieves the active policy for a given category or model.
        More specific policies (e.g., with model_name) might take precedence.
        """
        domain = [('is_active', '=', True)]
        if data_category:
            domain.append(('data_category', '=', data_category))
        if model_name:
            domain.append(('model_name', '=', model_name))
        
        # Prioritize policies that specify both model and category, then model, then category
        # This is a simplified search; more complex prioritization might be needed.
        policies = self.search(domain, order='model_name desc, data_category desc', limit=1) # Simple order
        return policies