from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Security & Access
    influence_gen_password_min_length = fields.Integer(
        string="Min Password Length",
        config_parameter='influence_gen.password_min_length',
        help="Minimum length for user passwords."
    )
    influence_gen_password_complexity_regex = fields.Char(
        string="Password Complexity Regex",
        config_parameter='influence_gen.password_complexity_regex',
        help="Regex for password complexity requirements."
    )
    influence_gen_mfa_admin_mandatory = fields.Boolean(
        string="Mandatory MFA for Admins",
        config_parameter='influence_gen.mfa_admin_mandatory',
        help="If checked, MFA/2FA will be mandatory for Platform Administrator accounts."
    )

    # AI Services
    influence_gen_ai_quota_default_images_per_month = fields.Integer(
        string="Default AI Images/Month",
        config_parameter='influence_gen.ai_quota_default_images_per_month'
    )
    influence_gen_ai_default_resolution = fields.Char(
        string="Default AI Image Resolution",
        config_parameter='influence_gen.ai_default_resolution',
        help="e.g., 1024x1024"
    )
    influence_gen_ai_default_aspect_ratio = fields.Char(
        string="Default AI Aspect Ratio",
        config_parameter='influence_gen.ai_default_aspect_ratio',
        help="e.g., 16:9"
    )
    influence_gen_ai_default_cfg_scale = fields.Float(
        string="Default AI CFG Scale",
        config_parameter='influence_gen.ai_default_cfg_scale'
    )
    influence_gen_ai_default_inference_steps = fields.Integer(
        string="Default AI Inference Steps",
        config_parameter='influence_gen.ai_default_inference_steps'
    )

    # KYC Configuration
    influence_gen_kyc_accepted_doc_types = fields.Char(
        string="Accepted ID Document Types",
        config_parameter='influence_gen.kyc_accepted_doc_types',
        help="Comma-separated list, e.g., Passport,Driver's License"
    )
    influence_gen_kyc_social_verify_method = fields.Selection(
        selection=[
            ('oauth', 'OAuth'),
            ('code_in_bio', 'Code in Bio/Post'),
            ('manual', 'Manual Review')
        ],
        string="Social Media Verification Method",
        config_parameter='influence_gen.kyc_social_verify_method'
    )

    # Data Retention
    influence_gen_retention_pii_days = fields.Integer(
        string="PII Retention (Days)",
        config_parameter='influence_gen.retention_pii_days',
        help="Retention period for inactive influencer PII."
    )
    influence_gen_retention_kyc_docs_days = fields.Integer(
        string="KYC Docs Retention (Days)",
        config_parameter='influence_gen.retention_kyc_docs_days'
    )
    influence_gen_retention_campaign_data_days = fields.Integer(
        string="Campaign Data Retention (Days)",
        config_parameter='influence_gen.retention_campaign_data_days'
    )
    influence_gen_retention_generated_images_personal_days = fields.Integer(
        string="Personal AI Images Retention (Days)",
        config_parameter='influence_gen.retention_generated_images_personal_days'
    )
    influence_gen_retention_audit_logs_days = fields.Integer(
        string="Audit Logs Retention (Days)",
        config_parameter='influence_gen.retention_audit_logs_days'
    )
    influence_gen_retention_operational_logs_days = fields.Integer(
        string="Operational Logs Retention (Days)",
        config_parameter='influence_gen.retention_operational_logs_days'
    )

    # Content Moderation
    influence_gen_content_moderation_ai_prompt_denylist = fields.Text(
        string="AI Prompt Denylist Keywords",
        config_parameter='influence_gen.content_moderation_ai_prompt_denylist',
        help="Comma-separated keywords/phrases."
    )
    influence_gen_content_moderation_api_key = fields.Char(
        string="Content Moderation API Key",
        config_parameter='influence_gen.content_moderation_api_key',
        help="For third-party moderation service."
    )
    influence_gen_content_moderation_api_endpoint = fields.Char(
        string="Content Moderation API Endpoint",
        config_parameter='influence_gen.content_moderation_api_endpoint'
    )

    # Email Configuration
    influence_gen_smtp_host = fields.Char(related='company_id.smtp_host', readonly=False)
    influence_gen_smtp_port = fields.Integer(related='company_id.smtp_port', readonly=False)
    influence_gen_smtp_user = fields.Char(related='company_id.smtp_user', readonly=False)
    influence_gen_smtp_password = fields.Char(related='company_id.smtp_pass', readonly=False)
    influence_gen_smtp_encryption = fields.Selection(
        related='company_id.smtp_encryption',
        readonly=False,
        selection=[('none', 'None'), ('starttls', 'STARTTLS'), ('ssl', 'SSL/TLS')]
    )

    # Logging & Monitoring
    influence_gen_log_level_odoo_default = fields.Selection(
        selection=[
            ('DEBUG', 'Debug'),
            ('INFO', 'Info'),
            ('WARNING', 'Warning'),
            ('ERROR', 'Error'),
            ('CRITICAL', 'Critical')
        ],
        string="Default Odoo Log Level",
        config_parameter='influence_gen.log_level_odoo_default'
    )
    influence_gen_log_level_n8n_default = fields.Selection(
        selection=[
            ('DEBUG', 'Debug'),
            ('INFO', 'Info'),
            ('WARNING', 'Warning'),
            ('ERROR', 'Error'),
            ('CRITICAL', 'Critical')
        ],
        string="Default N8N Log Level",
        config_parameter='influence_gen.log_level_n8n_default'
    )
    influence_gen_alert_critical_email_to = fields.Char(
        string="Critical Alerts Email Recipient(s)",
        config_parameter='influence_gen.alert_critical_email_to'
    )

    # API Configuration
    influence_gen_api_rate_limit_callback = fields.Char(
        string="Callback API Rate Limit",
        config_parameter='influence_gen.api_rate_limit_callback',
        help="e.g., 100/minute"
    )

    # Payment Configuration
    influence_gen_payment_default_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string="Default Payment Journal",
        config_parameter='influence_gen.payment_default_journal_id',
        domain="[('type', 'in', ('bank', 'cash'))]"
    )
    influence_gen_payment_default_expense_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Default Expense Account for Payouts",
        config_parameter='influence_gen.payment_default_expense_account_id'
    )

    # Secrets Management
    influence_gen_secrets_management_type = fields.Selection(
        selection=[
            ('env', 'Environment Variables'),
            ('odoo_internal', 'Odoo Internal (Encrypted)'),
            ('vault', 'External Vault')
        ],
        string="Secrets Management Type",
        config_parameter='influence_gen.secrets_management_type',
        default='env'
    )
    influence_gen_secrets_vault_url = fields.Char(
        string="External Vault URL",
        config_parameter='influence_gen.secrets_vault_url',
        help="URL for HashiCorp Vault or similar."
    )
    influence_gen_secrets_vault_token_path = fields.Char(
        string="Vault Token/Auth Path",
        config_parameter='influence_gen.secrets_vault_token_path'
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('influence_gen.password_min_length', self.influence_gen_password_min_length)
        ICP.set_param('influence_gen.password_complexity_regex', self.influence_gen_password_complexity_regex)
        ICP.set_param('influence_gen.mfa_admin_mandatory', self.influence_gen_mfa_admin_mandatory)
        ICP.set_param('influence_gen.ai_quota_default_images_per_month', self.influence_gen_ai_quota_default_images_per_month)
        ICP.set_param('influence_gen.ai_default_resolution', self.influence_gen_ai_default_resolution)
        ICP.set_param('influence_gen.ai_default_aspect_ratio', self.influence_gen_ai_default_aspect_ratio)
        ICP.set_param('influence_gen.ai_default_cfg_scale', self.influence_gen_ai_default_cfg_scale)
        ICP.set_param('influence_gen.ai_default_inference_steps', self.influence_gen_ai_default_inference_steps)
        ICP.set_param('influence_gen.kyc_accepted_doc_types', self.influence_gen_kyc_accepted_doc_types)
        ICP.set_param('influence_gen.kyc_social_verify_method', self.influence_gen_kyc_social_verify_method)
        ICP.set_param('influence_gen.retention_pii_days', self.influence_gen_retention_pii_days)
        ICP.set_param('influence_gen.retention_kyc_docs_days', self.influence_gen_retention_kyc_docs_days)
        ICP.set_param('influence_gen.retention_campaign_data_days', self.influence_gen_retention_campaign_data_days)
        ICP.set_param('influence_gen.retention_generated_images_personal_days', self.influence_gen_retention_generated_images_personal_days)
        ICP.set_param('influence_gen.retention_audit_logs_days', self.influence_gen_retention_audit_logs_days)
        ICP.set_param('influence_gen.retention_operational_logs_days', self.influence_gen_retention_operational_logs_days)
        ICP.set_param('influence_gen.content_moderation_ai_prompt_denylist', self.influence_gen_content_moderation_ai_prompt_denylist)
        ICP.set_param('influence_gen.content_moderation_api_key', self.influence_gen_content_moderation_api_key)
        ICP.set_param('influence_gen.content_moderation_api_endpoint', self.influence_gen_content_moderation_api_endpoint)
        ICP.set_param('influence_gen.log_level_odoo_default', self.influence_gen_log_level_odoo_default)
        ICP.set_param('influence_gen.log_level_n8n_default', self.influence_gen_log_level_n8n_default)
        ICP.set_param('influence_gen.alert_critical_email_to', self.influence_gen_alert_critical_email_to)
        ICP.set_param('influence_gen.api_rate_limit_callback', self.influence_gen_api_rate_limit_callback)
        ICP.set_param('influence_gen.payment_default_journal_id', self.influence_gen_payment_default_journal_id.id)
        ICP.set_param('influence_gen.payment_default_expense_account_id', self.influence_gen_payment_default_expense_account_id.id)
        ICP.set_param('influence_gen.secrets_management_type', self.influence_gen_secrets_management_type)
        ICP.set_param('influence_gen.secrets_vault_url', self.influence_gen_secrets_vault_url)
        ICP.set_param('influence_gen.secrets_vault_token_path', self.influence_gen_secrets_vault_token_path)

        # For related fields, assignment here is enough as Odoo handles saving them.
        # self.company_id.smtp_host = self.influence_gen_smtp_host
        # ... and so on for other related fields if they were not readonly=False in the first place
        # but since they are directly related and readonly=False, direct modification on view is fine.


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICP = self.env['ir.config_parameter'].sudo()
        res.update(
            influence_gen_password_min_length=int(ICP.get_param('influence_gen.password_min_length', default=0)),
            influence_gen_password_complexity_regex=ICP.get_param('influence_gen.password_complexity_regex', default=''),
            influence_gen_mfa_admin_mandatory=ICP.get_param('influence_gen.mfa_admin_mandatory', default=False) == 'True',
            influence_gen_ai_quota_default_images_per_month=int(ICP.get_param('influence_gen.ai_quota_default_images_per_month', default=0)),
            influence_gen_ai_default_resolution=ICP.get_param('influence_gen.ai_default_resolution', default=''),
            influence_gen_ai_default_aspect_ratio=ICP.get_param('influence_gen.ai_default_aspect_ratio', default=''),
            influence_gen_ai_default_cfg_scale=float(ICP.get_param('influence_gen.ai_default_cfg_scale', default=0.0)),
            influence_gen_ai_default_inference_steps=int(ICP.get_param('influence_gen.ai_default_inference_steps', default=0)),
            influence_gen_kyc_accepted_doc_types=ICP.get_param('influence_gen.kyc_accepted_doc_types', default=''),
            influence_gen_kyc_social_verify_method=ICP.get_param('influence_gen.kyc_social_verify_method', default='manual'),
            influence_gen_retention_pii_days=int(ICP.get_param('influence_gen.retention_pii_days', default=0)),
            influence_gen_retention_kyc_docs_days=int(ICP.get_param('influence_gen.retention_kyc_docs_days', default=0)),
            influence_gen_retention_campaign_data_days=int(ICP.get_param('influence_gen.retention_campaign_data_days', default=0)),
            influence_gen_retention_generated_images_personal_days=int(ICP.get_param('influence_gen.retention_generated_images_personal_days', default=0)),
            influence_gen_retention_audit_logs_days=int(ICP.get_param('influence_gen.retention_audit_logs_days', default=0)),
            influence_gen_retention_operational_logs_days=int(ICP.get_param('influence_gen.retention_operational_logs_days', default=0)),
            influence_gen_content_moderation_ai_prompt_denylist=ICP.get_param('influence_gen.content_moderation_ai_prompt_denylist', default=''),
            influence_gen_content_moderation_api_key=ICP.get_param('influence_gen.content_moderation_api_key', default=''),
            influence_gen_content_moderation_api_endpoint=ICP.get_param('influence_gen.content_moderation_api_endpoint', default=''),
            influence_gen_log_level_odoo_default=ICP.get_param('influence_gen.log_level_odoo_default', default='INFO'),
            influence_gen_log_level_n8n_default=ICP.get_param('influence_gen.log_level_n8n_default', default='INFO'),
            influence_gen_alert_critical_email_to=ICP.get_param('influence_gen.alert_critical_email_to', default=''),
            influence_gen_api_rate_limit_callback=ICP.get_param('influence_gen.api_rate_limit_callback', default=''),
            influence_gen_payment_default_journal_id=int(ICP.get_param('influence_gen.payment_default_journal_id', default=0)) or False,
            influence_gen_payment_default_expense_account_id=int(ICP.get_param('influence_gen.payment_default_expense_account_id', default=0)) or False,
            influence_gen_secrets_management_type=ICP.get_param('influence_gen.secrets_management_type', default='env'),
            influence_gen_secrets_vault_url=ICP.get_param('influence_gen.secrets_vault_url', default=''),
            influence_gen_secrets_vault_token_path=ICP.get_param('influence_gen.secrets_vault_token_path', default=''),
        )
        return res