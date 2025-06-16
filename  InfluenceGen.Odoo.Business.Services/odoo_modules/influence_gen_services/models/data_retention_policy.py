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
        ('campaign_general', 'Campaign General Data'),
        ('campaign_applications', 'Campaign Applications'),
        ('content_submissions', 'Content Submissions'),
        ('ai_requests', 'AI Generation Requests'),
        ('ai_generated_images', 'AI Generated Images'),
        ('payment_records', 'Payment Records'),
        ('audit_logs', 'Audit Logs'),
        ('platform_settings_history', 'Platform Settings History'), # If versioning is implemented
        # Add more specific categories as needed
        ('personal_standard', 'Personal - Standard Retention (Images)'), # For generated_image.retention_category
        ('personal_extended', 'Personal - Extended Retention (Images)'),
        ('campaign_active', 'Campaign - Active Usage (Images)'),
        ('campaign_archival', 'Campaign - Archival (Images)'),
        ('legal_hold', 'Legal Hold (Images)') # For generated_image.retention_category, though legal hold is usually a flag
    ], string="Data Category", required=True, index=True)
    model_name = fields.Char(
        string="Target Odoo Model Technical Name",
        help="e.g., 'influence_gen.influencer_profile'. Used by automated retention jobs."
    )
    retention_period_days = fields.Integer(
        string="Retention Period (Days)",
        required=True,
        help="Number of days data in this category should be actively retained from its creation or last modification date."
    )
    disposition_action = fields.Selection([
        ('delete', 'Secure Delete'),
        ('anonymize', 'Anonymize'),
        ('archive', 'Archive') # Archive might mean setting active=False or moving to cold storage via infra
    ], string="Disposition Action", required=True)
    is_active = fields.Boolean(string="Active Policy", default=True, index=True)
    description = fields.Text(string="Policy Description and Basis")
    legal_hold_overrideable = fields.Boolean(
        string="Overrideable by Legal Hold?",
        default=True,
        help="If False, this policy might still apply even if data is under legal hold (use with extreme caution)."
    )

    @api.model
    def get_active_policy(cls, data_category=None, model_name=None):
        domain = [('is_active', '=', True)]
        if data_category:
            domain.append(('data_category', '=', data_category))
        if model_name:
            domain.append(('model_name', '=', model_name))
        
        # Add preference logic if multiple policies match (e.g., most specific, or by sequence)
        # For now, returns the first one found.
        policy = cls.search(domain, limit=1, order="id asc") # Simple order for consistency
        return policy