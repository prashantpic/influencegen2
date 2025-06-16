from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Security & Access (REQ-PAC-003)
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

    # AI Services (REQ-PAC-004, REQ-PAC-005)
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

    # KYC Configuration (REQ-PAC-007)
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

    # Data Retention (REQ-PAC-008, REQ-DRH-001, REQ-DRH-006)
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

    # Content Moderation (REQ-PAC-009)
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

    # Email Configuration (REQ-PAC-010)
    # Odoo manages SMTP servers primarily through `ir.mail_server` or `res.company`.
    # These fields provide a view/edit capability for the current company's settings.
    influence_gen_smtp_host = fields.Char(
        related='company_id.smtp_host',
        readonly=False
    )
    influence_gen_smtp_port = fields.Integer(
        related='company_id.smtp_port',
        readonly=False
    )
    influence_gen_smtp_user = fields.Char(
        related='company_id.smtp_user',
        readonly=False
    )
    influence_gen_smtp_password = fields.Char(
        related='company_id.smtp_pass',
        readonly=False
    )
    influence_gen_smtp_encryption = fields.Selection(
        related='company_id.smtp_encryption',
        readonly=False,
        selection=[('none', 'None'), ('starttls', 'STARTTLS'), ('ssl', 'SSL/TLS')]
    )

    # Logging & Monitoring (REQ-PAC-011, REQ-ATEL-003, REQ-ATEL-011)
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

    # API Configuration (REQ-PAC-013)
    influence_gen_api_rate_limit_callback = fields.Char(
        string="Callback API Rate Limit",
        config_parameter='influence_gen.api_rate_limit_callback',
        help="e.g., 100/minute"
    )

    # Payment Configuration (REQ-PAC-015)
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

    # Secrets Management (REQ-PAC-017)
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

    # Standard set_values and get_values methods are implicitly handled by Odoo
    # for fields with config_parameter attribute.
    # Explicit definition is only needed if custom logic is required beyond ir.config_parameter.
    # However, to be explicit as per SDS and standard practice for non-config_parameter fields
    # (though all listed here use config_parameter or related):

    # def set_values(self):
    #     super(ResConfigSettings, self).set_values()
    #     # Example for a field not using config_parameter:
    #     # self.env['ir.config_parameter'].sudo().set_param('my_module.my_field', self.my_field)

    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     # Example for a field not using config_parameter:
    #     # res.update(
    #     #     my_field=self.env['ir.config_parameter'].sudo().get_param('my_module.my_field'),
    #     # )
    #     return res