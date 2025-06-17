# Software Design Specification: InfluenceGen.Odoo.Admin.Backend

## 1. Introduction

This document outlines the software design specification for the `InfluenceGen.Odoo.Admin.Backend` repository. This Odoo module provides the backend User Interface (UI) and administrative functionalities for Platform Administrators managing the InfluenceGen system. It enables administrators to oversee and manage all aspects of the platform, including user and campaign lifecycles, Know Your Customer (KYC) processes, AI service configurations, financial oversight, system monitoring, and core platform settings.

This module interacts primarily with `InfluenceGen.Odoo.Business.Services` (REPO-IGBS-003) for business logic and data operations, and may utilize shared UI components from `InfluenceGen.Odoo.Shared.UIComponents` (REPO-IGSUC-006) and core utilities from `InfluenceGen.Odoo.Shared.Core.Utilities` (REPO-IGSCU-007).

**Target Framework**: Odoo 18
**Primary Languages**: Python, XML

## 2. Module Overview (`__manifest__.py`)

The `__manifest__.py` file will define the module's metadata and dependencies.

python
{
    'name': 'InfluenceGen Administration Backend',
    'version': '18.0.1.0.0',
    'summary': 'Administrative backend for the InfluenceGen Platform.',
    'description': """
        Provides all backend User Interface (UI) functionalities for Platform Administrators 
        managing the InfluenceGen system within Odoo. This includes interfaces for:
        - User management (influencers, roles, permissions)
        - Campaign creation and lifecycle management
        - KYC submission review and approval/rejection
        - Content moderation
        - System configuration (AI models, quotas, email templates, business rules)
        - Payment oversight
        - Viewing audit logs and system health dashboards
    """,
    'author': 'SSS-AI',
    'website': 'https://www.example.com', # Replace with actual website
    'category': 'InfluenceGen/Administration',
    'depends': [
        'base',
        'mail',
        'account', # For payment related configurations (e.g., journal selection)
        'influence_gen_services', # REPO-IGBS-003
        # 'influence_gen_shared_ui', # REPO-IGSUC-006 (if backend shared components are used)
        # 'influence_gen_shared_core', # REPO-IGSCU-007 (if utilities are used here)
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/influence_gen_admin_groups.xml',
        # Data
        'data/influence_gen_admin_groups_data.xml', # For module category
        # Wizards
        'wizards/broadcast_notification_wizard_view.xml',
        'wizards/kyc_request_info_wizard_view.xml',
        # Views
        'views/influence_gen_admin_menus.xml',
        'views/platform_config_settings_views.xml',
        'views/user_management_views.xml', # Extensions to Odoo user/group views
        'views/kyc_submission_views.xml',
        'views/campaign_management_views.xml', # Covers campaign, application, submission admin views
        'views/ai_model_config_views.xml',
        'views/ai_usage_tracking_views.xml',
        'views/payment_management_views.xml',
        'views/legal_document_version_views.xml',
        'views/maintenance_window_views.xml',
        'views/legal_hold_management_views.xml',
        'views/audit_log_viewer_views.xml',
        'views/system_health_dashboard_views.xml', # Placeholder, may need controller
        'views/performance_dashboard_views.xml', # Placeholder, may need controller
    ],
    'installable': True,
    'application': True, # If it's a main application entry point
    'auto_install': False,
    'icon': 'influence_gen_admin/static/description/icon.png', # Requires an icon file
    'license': 'LGPL-3', # Or appropriate license
}

**Requirements Met**: REQ-DDSI-001 (Module Definition)

## 3. Security Configuration

### 3.1. Security Groups (`security/influence_gen_admin_groups.xml`)

Defines the primary security group for platform administrators.

*   **File Content**:
    xml
    <odoo>
        <data noupdate="1">
            <record id="module_category_influence_gen_administration" model="ir.module.category">
                <field name="name">InfluenceGen</field>
                <field name="description">Manages all aspects of the InfluenceGen Platform.</field>
                <field name="sequence">25</field>
            </record>

            <record id="group_influence_gen_platform_admin" model="res.groups">
                <field name="name">InfluenceGen Platform Administrator</field>
                <field name="category_id" ref="module_category_influence_gen_administration"/>
                <field name="comment">Full access to manage and configure the InfluenceGen platform.</field>
                <!-- Implied groups can be added if admins should inherit other base permissions -->
                <!-- <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/> -->
            </record>
        </data>
    </odoo>
    
*   **Purpose**: Establishes the "InfluenceGen Platform Administrator" role.
*   **Requirements Met**: REQ-PAC-001 (Role Management).

### 3.2. Access Control Lists (`security/ir.model.access.csv`)

Defines CRUD permissions for the Platform Administrator group on relevant models. Models like `influence_gen.influencer_profile`, `influence_gen.campaign`, etc., are defined in `influence_gen_services` (REPO-IGBS-003) but access rights for admin users are defined here.

*   **File Content**:
    csv
    id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
    access_influence_gen_platform_admin_config_settings,influence_gen.platform_admin.config_settings,model_res_config_settings,group_influence_gen_platform_admin,1,1,1,1
    access_influence_gen_platform_admin_ai_model_config,influence_gen.platform_admin.ai_model_config,model_influence_gen_ai_model_config,group_influence_gen_platform_admin,1,1,1,1
    access_influence_gen_platform_admin_legal_doc_version,influence_gen.platform_admin.legal_doc_version,model_influence_gen_legal_document_version,group_influence_gen_platform_admin,1,1,1,1
    access_influence_gen_platform_admin_maintenance_window,influence_gen.platform_admin.maintenance_window,model_influence_gen_maintenance_window,group_influence_gen_platform_admin,1,1,1,1
    access_influence_gen_platform_admin_legal_hold,influence_gen.platform_admin.legal_hold,model_influence_gen_legal_hold,group_influence_gen_platform_admin,1,1,1,1
    
    # Access to models defined in influence_gen_services
    access_admin_influencer_profile,influence_gen.admin.influencer_profile,model_influence_gen_influencer_profile,group_influence_gen_platform_admin,1,1,1,1
    access_admin_kyc_data,influence_gen.admin.kyc_data,model_influence_gen_kyc_data,group_influence_gen_platform_admin,1,1,1,1
    access_admin_social_media_profile,influence_gen.admin.social_media_profile,model_influence_gen_social_media_profile,group_influence_gen_platform_admin,1,1,1,1
    access_admin_bank_account,influence_gen.admin.bank_account,model_influence_gen_bank_account,group_influence_gen_platform_admin,1,1,1,1
    access_admin_campaign,influence_gen.admin.campaign,model_influence_gen_campaign,group_influence_gen_platform_admin,1,1,1,1
    access_admin_campaign_application,influence_gen.admin.campaign_application,model_influence_gen_campaign_application,group_influence_gen_platform_admin,1,1,1,1
    access_admin_content_submission,influence_gen.admin.content_submission,model_influence_gen_content_submission,group_influence_gen_platform_admin,1,1,1,1
    access_admin_ai_image_generation_request,influence_gen.admin.ai_image_generation_request,model_influence_gen_ai_image_generation_request,group_influence_gen_platform_admin,1,1,1,1
    access_admin_generated_image,influence_gen.admin.generated_image,model_influence_gen_generated_image,group_influence_gen_platform_admin,1,1,1,1
    access_admin_payment_record,influence_gen.admin.payment_record,model_influence_gen_payment_record,group_influence_gen_platform_admin,1,1,1,1
    access_admin_terms_consent,influence_gen.admin.terms_consent,model_influence_gen_terms_consent,group_influence_gen_platform_admin,1,1,1,1
    access_admin_audit_log,influence_gen.admin.audit_log,model_influence_gen_audit_log,group_influence_gen_platform_admin,1,0,0,0
    # Potentially access to res.users and res.groups if admin needs to manage them beyond standard Odoo
    access_admin_res_users,influence_gen.admin.res_users,base.model_res_users,group_influence_gen_platform_admin,1,1,1,1
    access_admin_res_groups,influence_gen.admin.res_groups,base.model_res_groups,group_influence_gen_platform_admin,1,1,1,1
    
*   **Purpose**: Grants full CRUD permissions to Platform Administrators on all InfluenceGen-specific models and configuration models within this module. Read-only for Audit Logs.
*   **Requirements Met**: REQ-PAC-001 (Access Control).

## 4. Data Initialization

### 4.1. Module Category (`data/influence_gen_admin_groups_data.xml`)

This file is primarily used to define the `ir.module.category` referenced in `influence_gen_admin_groups.xml`.

*   **File Content**: (Content already shown in `influence_gen_admin_groups.xml` - ensure it's there or here and not duplicated. Standard practice is often in the security XML itself.)
    xml
    <odoo>
        <data noupdate="1">
            <!-- This record might already be in security/influence_gen_admin_groups.xml -->
            <!-- If not, it should be here to ensure the category exists. -->
            <!-- <record id="module_category_influence_gen_administration" model="ir.module.category">
                <field name="name">InfluenceGen</field>
                <field name="description">Manages all aspects of the InfluenceGen Platform.</field>
                <field name="sequence">25</field>
            </record> -->
        </data>
    </odoo>
    
*   **Purpose**: Ensures the "InfluenceGen" application category is available for grouping menus and security groups.
*   **Requirements Met**: REQ-PAC-001 (related to group categorization).

## 5. Models (`models/`)

Python files defining Odoo models specific to administrative configurations and backend logic.

### 5.1. `__init__.py`

*   **Purpose**: Initializes the `models` Python package.
*   **Logic**: Imports all model files:
    python
    from . import res_config_settings
    from . import ai_model_config
    from . import legal_document_version
    from . import maintenance_window
    from . import legal_hold
    # Add other admin-specific models if any
    

### 5.2. `res_config_settings.py`

Extends Odoo's global settings to manage InfluenceGen platform configurations.

*   **Class**: `ResConfigSettings(models.TransientModel)`
*   **Inherits**: `res.config.settings`
*   **Fields**:
    *   **Security & Access (REQ-PAC-003)**:
        *   `influence_gen_password_min_length` (fields.Integer, config_parameter='influence_gen.password_min_length', string="Min Password Length", help="Minimum length for user passwords.")
        *   `influence_gen_password_complexity_regex` (fields.Char, config_parameter='influence_gen.password_complexity_regex', string="Password Complexity Regex", help="Regex for password complexity requirements.")
        *   `influence_gen_mfa_admin_mandatory` (fields.Boolean, config_parameter='influence_gen.mfa_admin_mandatory', string="Mandatory MFA for Admins", help="If checked, MFA/2FA will be mandatory for Platform Administrator accounts.")
    *   **AI Services (REQ-PAC-004, REQ-PAC-005)**:
        *   `influence_gen_ai_quota_default_images_per_month` (fields.Integer, config_parameter='influence_gen.ai_quota_default_images_per_month', string="Default AI Images/Month")
        *   `influence_gen_ai_default_resolution` (fields.Char, config_parameter='influence_gen.ai_default_resolution', string="Default AI Image Resolution", help="e.g., 1024x1024")
        *   `influence_gen_ai_default_aspect_ratio` (fields.Char, config_parameter='influence_gen.ai_default_aspect_ratio', string="Default AI Aspect Ratio", help="e.g., 16:9")
        *   `influence_gen_ai_default_cfg_scale` (fields.Float, config_parameter='influence_gen.ai_default_cfg_scale', string="Default AI CFG Scale")
        *   `influence_gen_ai_default_inference_steps` (fields.Integer, config_parameter='influence_gen.ai_default_inference_steps', string="Default AI Inference Steps")
    *   **KYC Configuration (REQ-PAC-007)**:
        *   `influence_gen_kyc_accepted_doc_types` (fields.Char, config_parameter='influence_gen.kyc_accepted_doc_types', string="Accepted ID Document Types", help="Comma-separated list, e.g., Passport,Driver's License")
        *   `influence_gen_kyc_social_verify_method` (fields.Selection, selection=[('oauth', 'OAuth'), ('code_in_bio', 'Code in Bio/Post'), ('manual', 'Manual Review')], config_parameter='influence_gen.kyc_social_verify_method', string="Social Media Verification Method")
    *   **Data Retention (REQ-PAC-008, REQ-DRH-001, REQ-DRH-006)**:
        *   `influence_gen_retention_pii_days` (fields.Integer, config_parameter='influence_gen.retention_pii_days', string="PII Retention (Days)", help="Retention period for inactive influencer PII.")
        *   `influence_gen_retention_kyc_docs_days` (fields.Integer, config_parameter='influence_gen.retention_kyc_docs_days', string="KYC Docs Retention (Days)")
        *   `influence_gen_retention_campaign_data_days` (fields.Integer, config_parameter='influence_gen.retention_campaign_data_days', string="Campaign Data Retention (Days)")
        *   `influence_gen_retention_generated_images_personal_days` (fields.Integer, config_parameter='influence_gen.retention_generated_images_personal_days', string="Personal AI Images Retention (Days)")
        *   `influence_gen_retention_audit_logs_days` (fields.Integer, config_parameter='influence_gen.retention_audit_logs_days', string="Audit Logs Retention (Days)")
        *   `influence_gen_retention_operational_logs_days` (fields.Integer, config_parameter='influence_gen.retention_operational_logs_days', string="Operational Logs Retention (Days)")
    *   **Content Moderation (REQ-PAC-009)**:
        *   `influence_gen_content_moderation_ai_prompt_denylist` (fields.Text, config_parameter='influence_gen.content_moderation_ai_prompt_denylist', string="AI Prompt Denylist Keywords", help="Comma-separated keywords/phrases.")
        *   `influence_gen_content_moderation_api_key` (fields.Char, config_parameter='influence_gen.content_moderation_api_key', string="Content Moderation API Key", help="For third-party moderation service.")
        *   `influence_gen_content_moderation_api_endpoint` (fields.Char, config_parameter='influence_gen.content_moderation_api_endpoint', string="Content Moderation API Endpoint")
    *   **Email Configuration (REQ-PAC-010)**:
        *   `influence_gen_smtp_host` (fields.Char, related='company_id.smtp_host', readonly=False) <!-- Odoo handles SMTP via res.company or ir.mail_server -->
        *   `influence_gen_smtp_port` (fields.Integer, related='company_id.smtp_port', readonly=False)
        *   `influence_gen_smtp_user` (fields.Char, related='company_id.smtp_user', readonly=False)
        *   `influence_gen_smtp_password` (fields.Char, related='company_id.smtp_pass', readonly=False)
        *   `influence_gen_smtp_encryption` (fields.Selection, related='company_id.smtp_encryption', readonly=False, selection=[('none', 'None'), ('starttls', 'STARTTLS'), ('ssl', 'SSL/TLS')])
        *   *Note*: Odoo manages SMTP servers primarily through `ir.mail_server`. This section in `res.config.settings` might show current outgoing server or link to its configuration. Email templates are managed via `mail.template` model directly.
    *   **Logging & Monitoring (REQ-PAC-011, REQ-ATEL-003, REQ-ATEL-011)**:
        *   `influence_gen_log_level_odoo_default` (fields.Selection, selection=[('DEBUG', 'Debug'), ('INFO', 'Info'), ('WARNING', 'Warning'), ('ERROR', 'Error'), ('CRITICAL', 'Critical')], config_parameter='influence_gen.log_level_odoo_default', string="Default Odoo Log Level")
        *   `influence_gen_log_level_n8n_default` (fields.Selection, selection=[('DEBUG', 'Debug'), ('INFO', 'Info'), ('WARNING', 'Warning'), ('ERROR', 'Error'), ('CRITICAL', 'Critical')], config_parameter='influence_gen.log_level_n8n_default', string="Default N8N Log Level")
        *   `influence_gen_alert_critical_email_to` (fields.Char, config_parameter='influence_gen.alert_critical_email_to', string="Critical Alerts Email Recipient(s)")
    *   **API Configuration (REQ-PAC-013)**:
        *   `influence_gen_api_rate_limit_callback` (fields.Char, config_parameter='influence_gen.api_rate_limit_callback', string="Callback API Rate Limit", help="e.g., 100/minute")
    *   **Payment Configuration (REQ-PAC-015)**:
        *   `influence_gen_payment_default_journal_id` (fields.Many2one, comodel_name='account.journal', string="Default Payment Journal", config_parameter='influence_gen.payment_default_journal_id', domain="[('type', 'in', ('bank', 'cash'))]")
        *   `influence_gen_payment_default_expense_account_id` (fields.Many2one, comodel_name='account.account', string="Default Expense Account for Payouts", config_parameter='influence_gen.payment_default_expense_account_id')
    *   **Secrets Management (REQ-PAC-017)**:
        *   `influence_gen_secrets_management_type` (fields.Selection, selection=[('env', 'Environment Variables'), ('odoo_internal', 'Odoo Internal (Encrypted)'), ('vault', 'External Vault')], string="Secrets Management Type", config_parameter='influence_gen.secrets_management_type', default='env')
        *   `influence_gen_secrets_vault_url` (fields.Char, string="External Vault URL", config_parameter='influence_gen.secrets_vault_url', help="URL for HashiCorp Vault or similar.")
        *   `influence_gen_secrets_vault_token_path` (fields.Char, string="Vault Token/Auth Path", config_parameter='influence_gen.secrets_vault_token_path')
*   **Methods**:
    *   `set_values(self)`: Saves settings to `ir.config_parameter` or related models.
    *   `get_values(self)`: Retrieves settings.
*   **Requirements Met**: REQ-PAC-003, REQ-PAC-004, REQ-PAC-005, REQ-PAC-007, REQ-PAC-008, REQ-PAC-009, REQ-PAC-010, REQ-PAC-011, REQ-PAC-013, REQ-PAC-015, REQ-PAC-017, REQ-ATEL-003, REQ-ATEL-011, REQ-DRH-001, REQ-DRH-006.

### 5.3. `ai_model_config.py`

Manages configurations for AI image generation models.

*   **Class**: `AiModelConfig(models.Model)`
*   **`_name`**: `influence_gen.ai_model_config`
*   **`_description`**: "InfluenceGen AI Model Configuration"
*   **Fields**:
    *   `name` (fields.Char, required=True, string='Model Name')
    *   `description` (fields.Text, string='Description')
    *   `model_type` (fields.Selection, selection=[('flux_lora', 'Flux LoRA'), ('stable_diffusion_xl', 'Stable Diffusion XL'), ('other', 'Other')], required=True, string='Model Type', default='flux_lora')
    *   `trigger_keywords` (fields.Char, string='Trigger Keywords', help="Comma-separated keywords specific to this model/LoRA.")
    *   `api_endpoint_info` (fields.Char, string='API Endpoint/Identifier', help="Identifier for N8N/AI service to use this model.")
    *   `is_active` (fields.Boolean, string='Active', default=True, index=True)
    *   `default_params_json` (fields.Text, string='Default Parameters (JSON)', help="JSON string for default parameters like sampler, scheduler if model-specific.")
*   **Requirements Met**: REQ-PAC-005, REQ-AIGS-004.

### 5.4. `legal_document_version.py`

Manages versions of legal documents (ToS, Privacy Policy).

*   **Class**: `LegalDocumentVersion(models.Model)`
*   **`_name`**: `influence_gen.legal_document_version`
*   **`_description`**: "InfluenceGen Legal Document Version"
*   **`_order`**: `document_type, effective_date desc`
*   **Fields**:
    *   `document_type` (fields.Selection, selection=[('tos', 'Terms of Service'), ('privacy_policy', 'Privacy Policy')], required=True, string='Document Type')
    *   `version` (fields.Char, required=True, string='Version')
    *   `content` (fields.Html, required=True, string='Content')
    *   `effective_date` (fields.Date, required=True, string='Effective Date', default=fields.Date.today)
    *   `is_active` (fields.Boolean, string='Active', default=False, copy=False)
    *   `attachment_id` (fields.Many2one, 'ir.attachment', string="Document File")
*   **Constraints**:
    python
    from odoo.exceptions import ValidationError
    @api.constrains('is_active', 'document_type')
    def _check_active_version_unicity(self):
        for record in self:
            if record.is_active:
                domain = [
                    ('id', '!=', record.id),
                    ('document_type', '=', record.document_type),
                    ('is_active', '=', True)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(f"Only one version of {record.document_type} can be active at a time.")
    
*   **Requirements Met**: REQ-PAC-006.

### 5.5. `maintenance_window.py`

Schedules and manages planned system maintenance.

*   **Class**: `MaintenanceWindow(models.Model)`
*   **`_name`**: `influence_gen.maintenance_window`
*   **`_description`**: "InfluenceGen Maintenance Window"
*   **Fields**:
    *   `name` (fields.Char, required=True, string='Title')
    *   `start_datetime` (fields.Datetime, required=True, string='Start Time')
    *   `end_datetime` (fields.Datetime, required=True, string='End Time')
    *   `description` (fields.Text, string='Description/Impact')
    *   `notify_users` (fields.Boolean, string='Notify Users', default=True)
    *   `notification_message` (fields.Text, string='Notification Message', help="Custom message for user notification. If empty, a default message will be used.")
    *   `status` (fields.Selection, selection=[('planned', 'Planned'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], string="Status", default="planned", readonly=True, copy=False)
*   **Methods**:
    *   `action_send_notification(self)`: Creates a Broadcast Notification or sends emails directly.
    *   `action_start_maintenance(self)`: Sets status to 'in_progress'.
    *   `action_complete_maintenance(self)`: Sets status to 'completed'.
    *   `action_cancel_maintenance(self)`: Sets status to 'cancelled'.
*   **Requirements Met**: REQ-PAC-012.

### 5.6. `legal_hold.py`

Manages legal holds on data.

*   **Class**: `LegalHold(models.Model)`
*   **`_name`**: `influence_gen.legal_hold`
*   **`_description`**: "InfluenceGen Legal Hold"
*   **Fields**:
    *   `name` (fields.Char, required=True, string='Hold Name/Case ID', index=True)
    *   `description` (fields.Text, string='Reason for Hold', required=True)
    *   `status` (fields.Selection, selection=[('active', 'Active'), ('lifted', 'Lifted')], required=True, default='active', string='Status', index=True)
    *   `target_model_id` (fields.Many2one, comodel_name='ir.model', string='Target Model', help="The model containing the data to be held.")
    *   `target_record_id` (fields.Reference, selection=lambda self: [(model.model, model.name) for model in self.env['ir.model'].search([])], string="Target Record", help="Specific record to be held. Use if holding a single record.")
    *   `target_influencer_id` (fields.Many2one, comodel_name='influence_gen.influencer_profile', string='Target Influencer', help="If holding all data related to a specific influencer.")
    *   `target_campaign_id` (fields.Many2one, comodel_name='influence_gen.campaign', string='Target Campaign', help="If holding all data related to a specific campaign.")
    *   `effective_date` (fields.Date, required=True, string='Effective Date', default=fields.Date.today)
    *   `lifted_date` (fields.Date, string='Lifted Date')
    *   `created_by_id` (fields.Many2one, comodel_name='res.users', string='Created By', readonly=True, default=lambda self: self.env.user)
    *   `lifted_by_id` (fields.Many2one, comodel_name='res.users', string='Lifted By', readonly=True)
*   **Methods**:
    *   `action_lift_hold(self)`: Sets status to 'lifted', `lifted_date` to now, `lifted_by_id` to current user. Logs this action.
*   **Requirements Met**: REQ-DRH-008, REQ-DRH-009 (this model provides the mechanism; enforcement logic is in services/core models).

## 6. Views (`views/`)

XML files defining the user interface for administrators.

### 6.1. `influence_gen_admin_menus.xml`

*   **Purpose**: Defines the main navigation structure in the Odoo backend for InfluenceGen administration.
*   **Logic**:
    *   Root Menu: "InfluenceGen Admin" (`id="menu_influence_gen_admin_root"`, `web_icon="influence_gen_admin,static/description/icon.png"`).
    *   Sub-menus:
        *   Dashboard (action to `system_health_dashboard_views.xml` or `performance_dashboard_views.xml`).
        *   Influencers (action to `influence_gen.influencer_profile` list view from services repo).
        *   KYC Management (action for `influence_gen.kyc_data` list view).
        *   Campaigns (action for `influence_gen.campaign` list view).
        *   Content Submissions (action for `influence_gen.content_submission` list view).
        *   AI Services
            *   AI Model Configuration (action for `influence_gen.ai_model_config`).
            *   AI Usage Tracking (action for `ai_usage_tracking_views.xml`).
        *   Financials
            *   Payments (action for `influence_gen.payment_record` list view).
        *   User & Access
            *   Users (standard Odoo action `base.action_res_users`).
            *   Groups (standard Odoo action `base.action_res_groups`).
        *   Legal & Compliance
            *   Legal Documents (action for `influence_gen.legal_document_version`).
            *   Legal Holds (action for `influence_gen.legal_hold`).
        *   System Operations
            *   Audit Logs (action for `audit_log_viewer_views.xml`).
            *   Maintenance Windows (action for `influence_gen.maintenance_window`).
            *   Broadcast Notifications (action for `broadcast_notification_wizard`).
        *   Configuration (action for `res.config.settings` specific to InfluenceGen).
*   **Access**: All menu items will be restricted to `group_influence_gen_platform_admin`.
*   **Requirements Met**: REQ-PAC-014, REQ-UIUX-003, REQ-UIUX-015.

### 6.2. `kyc_submission_views.xml`

*   **Model**: `influence_gen.kyc_data` (defined in REPO-IGBS-003).
*   **Views**: List, Form, Kanban, Search.
    *   **List**: Fields: `influencer_profile_id`, `document_type`, `submission_date` (from `create_date` of KYCData), `verification_status`, `reviewer_id`, `reviewed_at`. Filters for status.
    *   **Form**:
        *   Display `influencer_profile_id` (as link).
        *   Fields: `document_type`, `document_front_url` (display as image/link), `document_back_url` (if present).
        *   `verification_status` (dropdown or statusbar).
        *   `reviewer_id`, `reviewed_at`, `notes`.
        *   Buttons in header:
            *   "Approve" (calls `action_approve` on `influence_gen.kyc_data`). Visible if status is 'pending' or 'in_review'.
            *   "Reject" (calls `action_reject` on `influence_gen.kyc_data`). Visible if status is 'pending' or 'in_review'.
            *   "Request More Info" (opens `influence_gen.kyc_request_info_wizard` with current record ID in context). Visible if status is 'pending' or 'in_review'.
    *   **Search**: Filter by `influencer_profile_id`, `verification_status`, `document_type`.
*   **Action**: `ir.actions.act_window` for `influence_gen.kyc_data`.
*   **Requirements Met**: REQ-IOKYC-011.

### 6.3. `user_management_views.xml`

*   **Purpose**: Extends Odoo's native user and group management views for specific InfluenceGen needs.
*   **Logic**:
    *   Inherit `base.view_users_form` and `base.view_users_tree`:
        *   Add a tab/page "InfluenceGen Profile" to user form if user is an influencer, showing related `influence_gen.influencer_profile` fields (read-only summary, link to full profile).
        *   Possibly add quick links or indicators related to KYC status or campaign participation if useful for admins.
    *   Inherit `base.view_groups_form` and `base.view_groups_tree` to ensure `group_influence_gen_platform_admin` is clearly visible and manageable.
*   **Requirements Met**: REQ-PAC-001, REQ-PAC-002.

### 6.4. `platform_config_settings_views.xml`

*   **Model**: `res.config.settings`.
*   **View Type**: Form.
*   **Logic**:
    *   Inherits `res.config.settings.view_form`.
    *   Adds a new configuration page for "InfluenceGen Platform" or integrates into existing pages.
    *   Uses `<app_settings_block>` or `<div>` with classes `o_setting_box` for each group of settings.
    *   Fields defined in `models/res_config_settings.py` are placed here with appropriate labels and help texts.
    *   Sections: Security, AI Services, KYC, Data Retention, Content Moderation, Email, Logging, API Config, Payments, Secrets.
    *   Example snippet:
        xml
        <record id="influence_gen_config_settings_view_form" model="ir.ui.view">
            <field name="name">influence.gen.config.settings.view.form</field>
            <field name="model">res.config.settings</field>
            <field name="inherit_id" ref="base_setup.res_config_settings_view_form"/>
            <field name="arch" type="xml">
                <xpath expr="//div[hasclass('settings')]" position="inside">
                    <div class="app_settings_block" data-string="InfluenceGen" string="InfluenceGen Platform" data-key="influence_gen_admin">
                        <h2>Security Policies</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane">
                                    <field name="influence_gen_mfa_admin_mandatory"/>
                                </div>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_mfa_admin_mandatory"/>
                                    <div class="text-muted">
                                        Enforce Multi-Factor Authentication for Platform Administrators.
                                    </div>
                                </div>
                            </div>
                            <!-- More settings here -->
                        </div>
                        <h2>AI Services Configuration</h2>
                        <!-- AI settings fields -->
                        </div>
                    </div>
                </xpath>
            </field>
        </record>
        <record id="influence_gen_config_action" model="ir.actions.act_window">
            <field name="name">InfluenceGen Settings</field>
            <field name="res_model">res.config.settings</field>
            <field name="view_mode">form</field>
            <field name="target">inline</field>
            <field name="context">{'module' : 'influence_gen_admin', 'bin_size': False}</field>
        </record>
        
*   **Requirements Met**: REQ-PAC-003, REQ-PAC-004, REQ-PAC-005, REQ-PAC-007, REQ-PAC-008, REQ-PAC-009, REQ-PAC-010, REQ-PAC-011, REQ-PAC-013, REQ-PAC-015, REQ-PAC-017, REQ-UIUX-015.

### 6.5. `ai_model_config_views.xml`

*   **Model**: `influence_gen.ai_model_config`.
*   **Views**: List, Form.
    *   **List**: `name`, `model_type`, `is_active`.
    *   **Form**: All fields: `name`, `description`, `model_type`, `trigger_keywords`, `api_endpoint_info`, `default_params_json`, `is_active`.
*   **Action**: `ir.actions.act_window` for `influence_gen.ai_model_config`.
*   **Requirements Met**: REQ-PAC-005, REQ-AIGS-004.

### 6.6. `legal_document_version_views.xml`

*   **Model**: `influence_gen.legal_document_version`.
*   **Views**: List, Form.
    *   **List**: `document_type`, `version`, `effective_date`, `is_active`.
    *   **Form**: All fields: `document_type`, `version`, `content` (using `widget="html"`), `effective_date`, `attachment_id`, `is_active`.
*   **Action**: `ir.actions.act_window` for `influence_gen.legal_document_version`.
*   **Requirements Met**: REQ-PAC-006.

### 6.7. `maintenance_window_views.xml`

*   **Model**: `influence_gen.maintenance_window`.
*   **Views**: List, Form, Calendar.
    *   **List**: `name`, `start_datetime`, `end_datetime`, `status`, `notify_users`.
    *   **Form**: All fields. Buttons in header for `action_start_maintenance`, `action_complete_maintenance`, `action_cancel_maintenance`, `action_send_notification`.
    *   **Calendar**: `date_start="start_datetime"`, `date_stop="end_datetime"`, `display="name"`, `color="status"`.
*   **Action**: `ir.actions.act_window` for `influence_gen.maintenance_window`.
*   **Requirements Met**: REQ-PAC-012.

### 6.8. `campaign_management_views.xml`

This file will contain views for `influence_gen.campaign`, `influence_gen.campaign_application`, and `influence_gen.content_submission` models (defined in REPO-IGBS-003).

*   **Campaign Views (`influence_gen.campaign`)**:
    *   List: `name`, `brand_client`, `start_date`, `end_date`, `status`, `budget`.
    *   Form: Tabs for "Details" (`name`, `description`, `brand_client`, `goals`, `budget`, `compensation_model`, `submission_deadline`, `start_date`, `end_date`, `status`), "Targeting & Content" (`target_criteria` (JSON widget or structured fields), `content_requirements`, `usage_rights`), "Applications" (One2many `campaign_application_ids`), "Submissions" (One2many related or through applications). Buttons for status transitions (`action_publish`, `action_close`, etc. defined on the model).
    *   Kanban: Grouped by `status`. Fields displayed: `name`, `brand_client`, `end_date`.
    *   Search: By `name`, `brand_client`, `status`.
    *   Action for campaigns.
*   **Campaign Application Views (`influence_gen.campaign_application`)**: (Primarily viewed as One2many from Campaign)
    *   List (Tree in Form): `influencer_profile_id`, `submitted_at`, `status`.
    *   Form: `influencer_profile_id` (readonly link), `campaign_id` (readonly link), `proposal`, `status`. Buttons "Approve Application", "Reject Application" (calling model methods).
*   **Content Submission Views (`influence_gen.content_submission`)**: (Primarily viewed as One2many from Campaign Application)
    *   List (Tree in Form): `submission_date`, `content_url` (as link), `review_status`, `version`.
    *   Form: `campaign_application_id` (readonly link), `content_url` (display content if image/video, or link), `file_type`, `submission_date`, `review_status`, `feedback`. Buttons "Approve Content", "Request Revision", "Reject Content" (calling model methods).
*   **Requirements Met**: REQ-2-001, REQ-2-002, REQ-2-003 (Campaign Setup UI), REQ-2-007 (Application Review UI), REQ-2-010 (Content Review/Approval UI).

### 6.9. `performance_dashboard_views.xml`

*   **Purpose**: Provides administrators with performance overview.
*   **Logic**:
    *   Could be an Odoo `<dashboard>` view definition, aggregating data using graph, pivot, and list views on `CampaignPerformanceMV` or directly from `influence_gen.campaign` and related models via specific methods if `CampaignPerformanceMV` is not directly queryable as a standard model.
    *   Key Metrics (REQ-2-012): Aggregated campaign performance vs goals, influencer contribution summaries.
    *   Visualizations: Charts for campaign statuses, budget vs actual (if tracked), engagement trends (if data available).
*   **Action**: `ir.actions.act_window` for the dashboard.
*   **Requirements Met**: REQ-2-012, REQ-UIUX-015.

### 6.10. `payment_management_views.xml`

*   **Model**: `influence_gen.payment_record` (defined in REPO-IGBS-003).
*   **Views**: List, Form, Search.
    *   **List**: `influencer_profile_id`, `campaign_id`, `amount`, `currency`, `status`, `due_date`, `paid_date`, `transaction_id`. Batch action "Generate Vendor Bills" (if integration with Odoo accounting is semi-manual) or "Mark as Paid" (if payments are external).
    *   **Form**: All fields. Read-only for most once processed. Link to Odoo Vendor Bill/Payment if generated.
    *   **Search**: By `influencer_profile_id`, `campaign_id`, `status`, `payment_method`.
*   **Action**: `ir.actions.act_window` for `influence_gen.payment_record`.
*   **Requirements Met**: REQ-2-014 (UI for generating requests/batches), REQ-2-015 (UI for recording/viewing statuses), REQ-IPF-003, REQ-IPF-004, REQ-IPF-005, REQ-IPF-007, REQ-IPF-008 (data subject to retention).

### 6.11. `ai_usage_tracking_views.xml`

*   **Model**: `influence_gen.ai_image_generation_request` (defined in REPO-IGBS-003) or a dedicated summary model.
*   **Views**: Graph, Pivot, List, Search.
    *   **Graph/Pivot**: Aggregate `count` of requests grouped by `user_id.partner_id.name` (User), `campaign_id.name` (Campaign), `model_id.name` (AI Model), `status`, `date_trunc('month', create_date)` (Month).
    *   **List**: `create_date`, `user_id`, `campaign_id`, `model_id`, `status`, `prompt` (shortened).
    *   **Search**: Filter by `user_id`, `campaign_id`, `model_id`, `create_date` range.
*   **Action**: `ir.actions.act_window`.
*   **Requirements Met**: REQ-AIGS-007.

### 6.12. `audit_log_viewer_views.xml`

*   **Model**: `influence_gen.audit_log` (defined in REPO-IGBS-003).
*   **Views**: List, Form (read-only), Search.
    *   **List**: `timestamp`, `actor_user_id`, `event_type`, `action`, `target_entity`, `target_id` (or display name of target), `ip_address`.
    *   **Form**: All fields of the audit log, read-only. `details` field (JSON) might be displayed formatted or as raw text.
    *   **Search**:
        *   Filters: `timestamp` (date range), `actor_user_id`, `event_type` (selection if possible), `action`, `target_entity`, `ip_address`.
        *   Text search: On `details` if indexed, or on other Char/Text fields.
*   **Action**: `ir.actions.act_window` with `context="{'search_default_order_by_timestamp_desc': 1}"`.
*   **Export**: Odoo's default export functionality should be available. Custom export action if specific formatting is needed.
*   **Requirements Met**: REQ-PAC-016, REQ-UIUX-016, REQ-ATEL-008.

### 6.13. `system_health_dashboard_views.xml`

*   **Purpose**: Display key system health metrics.
*   **Logic**:
    *   An Odoo `<dashboard>` view or a QWeb template rendered by a controller (`controllers/main.py::get_system_health_data`).
    *   Placeholders for:
        *   API Error Rates (graph/KPI from monitoring system).
        *   N8N Workflow Queue Lengths (graph/KPI from N8N monitoring or Odoo if tracked).
        *   AI Service Availability (status indicator).
        *   Server Resource Utilization (CPU, Memory, Disk for Odoo, N8N, AI servers - graphs/KPIs).
        *   Database Performance Metrics (e.g., slow queries count, connection pool status - from DB monitoring).
*   **Action**: `ir.actions.act_window`.
*   **Requirements Met**: REQ-PAC-014, REQ-12-007.

### 6.14. `legal_hold_management_views.xml`

*   **Model**: `influence_gen.legal_hold`.
*   **Views**: List, Form, Search.
    *   **List**: `name`, `status`, `target_model_id`, display name of `target_record_id` or `target_influencer_id.name` or `target_campaign_id.name`, `effective_date`, `lifted_date`.
    *   **Form**: All fields from the model. Button "Lift Hold" (calls `action_lift_hold`).
    *   **Search**: Filter by `name`, `status`, `target_model_id`, `target_influencer_id`, `target_campaign_id`.
*   **Action**: `ir.actions.act_window` for `influence_gen.legal_hold`.
*   **Requirements Met**: REQ-DRH-003, REQ-DRH-004, REQ-DRH-007, REQ-DRH-008, REQ-DRH-009.

## 7. Wizards (`wizards/`)

Transient models for multi-step user interactions.

### 7.1. `__init__.py`

*   **Purpose**: Initializes the `wizards` Python package.
*   **Logic**: Imports all wizard files:
    python
    from . import broadcast_notification_wizard
    from . import kyc_request_info_wizard
    # Add other admin-specific wizards if any
    

### 7.2. `broadcast_notification_wizard.py`

*   **Class**: `BroadcastNotificationWizard(models.TransientModel)`
*   **`_name`**: `influence_gen.broadcast_notification_wizard`
*   **Fields**:
    *   `message_subject` (fields.Char, string='Subject', required=True)
    *   `message_body` (fields.Html, string='Message Body', required=True)
    *   `target_user_group_ids` (fields.Many2many, comodel_name='res.groups', string='Target User Groups', help="Leave empty to target all active internal users and portal users (influencers).")
    *   `target_influencer_ids` (fields.Many2many, comodel_name='influence_gen.influencer_profile', string="Specific Influencers")
    *   `send_email` (fields.Boolean, string='Send as Email', default=True)
    *   `show_in_app_banner_duration_hours` (fields.Integer, string='Show In-App Banner (Hours)', help="0 for no banner.")
*   **Method**: `action_send_notification(self)`:
    *   Collects target users based on selected groups or specific influencers.
    *   If `send_email`, iterates through users and uses `mail.mail` or a mail template to send emails.
    *   If `show_in_app_banner_duration_hours > 0`, creates records for a system-wide banner display model (this model needs to be defined, possibly in shared UI components, or use Odoo's built-in announcement/activity features if suitable).
*   **Requirements Met**: REQ-16-012.

### 7.3. `broadcast_notification_wizard_view.xml`

*   **Model**: `influence_gen.broadcast_notification_wizard`.
*   **View Type**: Form.
*   **Logic**: Form with fields `message_subject`, `message_body`, `target_user_group_ids`, `target_influencer_ids`, `send_email`, `show_in_app_banner_duration_hours`. Footer with "Send Notification" (calls `action_send_notification`) and "Cancel" buttons.
*   **Action**: `ir.actions.act_window` with `target='new'`.
*   **Requirements Met**: REQ-16-012.

### 7.4. `kyc_request_info_wizard.py`

*   **Class**: `KycRequestInfoWizard(models.TransientModel)`
*   **`_name`**: `influence_gen.kyc_request_info_wizard`
*   **Fields**:
    *   `kyc_submission_id` (fields.Many2one, comodel_name='influence_gen.kyc_data', string='KYC Submission', required=True, readonly=True)
    *   `message_to_influencer` (fields.Text, string='Message to Influencer', required=True, help="Detail what additional information or clarification is needed.")
*   **Method**: `action_send_request(self)`:
    *   Updates `self.kyc_submission_id.verification_status` to `'needs_more_info'`.
    *   Appends `self.message_to_influencer` to a communication log on `kyc_submission_id` or its related `influencer_profile_id`.
    *   Triggers an email notification (REQ-16-002) to the influencer associated with `kyc_submission_id.influencer_profile_id`, including the message.
    *   Logs the action in the audit trail.
*   **Requirements Met**: REQ-IOKYC-011.

### 7.5. `kyc_request_info_wizard_view.xml`

*   **Model**: `influence_gen.kyc_request_info_wizard`.
*   **View Type**: Form.
*   **Logic**: Form displaying `kyc_submission_id` (readonly, pre-filled from context) and `message_to_influencer`. Footer with "Send Request" (calls `action_send_request`) and "Cancel" buttons.
*   **Action**: Launched from a button on the `influence_gen.kyc_data` form view, passing `active_id` in context.
*   **Requirements Met**: REQ-IOKYC-011.

## 8. Controllers (`controllers/`)

Python files defining custom HTTP routes if needed for backend interactions.

### 8.1. `__init__.py`

*   **Purpose**: Initializes the `controllers` Python package.
*   **Logic**: `from . import main`

### 8.2. `main.py`

*   **Class**: `InfluenceGenAdminController(http.Controller)`
*   **Methods**:
    *   `get_system_health_data(self, **kwargs)`:
        *   `@http.route('/influence_gen/admin/system_health_data', type='json', auth='user', methods=['POST'], csrf=False)`
        *   **Logic**:
            1.  Verify user has `group_influence_gen_platform_admin` rights. Raise `AccessError` if not.
            2.  Fetch system health metrics. This is highly dependent on the actual monitoring setup.
                *   Could query internal Odoo models (e.g., count of failed cron jobs, queue lengths if tracked in Odoo).
                *   Could make HTTP requests to external monitoring system APIs (e.g., Prometheus, Datadog) if Odoo server can reach them and has credentials. This is complex and needs careful security for API keys.
                *   Placeholder for specific metrics: `{'api_error_rate': 0.05, 'n8n_queue_length': 10, ...}`
            3.  Return data as JSON.
        *   **Requirements Met**: REQ-PAC-014, REQ-12-007 (backend part for System Health Dashboard UI).
    *   `get_admin_performance_dashboard_data(self, **kwargs)`:
        *   `@http.route('/influence_gen/admin/performance_dashboard_data', type='json', auth='user', methods=['POST'], csrf=False)`
        *   **Logic**:
            1.  Verify admin rights.
            2.  Fetch data for the admin performance dashboard from `CampaignPerformanceMV` or by aggregating data from `influence_gen.campaign`, `influence_gen.campaign_application`, `influence_gen.content_submission`, `influence_gen.payment_record`.
            3.  Return data structured for charting/display.
        *   **Requirements Met**: REQ-2-012 (backend part for Admin Performance Dashboard UI).

## 9. Non-Functional Requirements Implementation Notes

*   **Usability (REQ-UIUX-003)**: Achieved by leveraging standard Odoo backend patterns (familiar to proficient admins), clear menu structures (`influence_gen_admin_menus.xml`), and organized views. Efficiency is targeted by providing direct actions and relevant information in list and form views.
*   **Configuration (REQ-PAC-*)**: Centralized in `res.config.settings` and specific models like `ai_model_config`, `legal_document_version`, etc., all accessible via admin menus.
*   **Auditability (REQ-ATEL-*)**: The `audit_log_viewer_views.xml` provides the UI for REQ-ATEL-008. Configuration changes, particularly to `res.config.settings` and other admin-managed models, will trigger audit logs created by the business services layer. REQ-ATEL-003 (configurable log levels) and REQ-ATEL-011 (auditing logging config changes) are handled via `res.config.settings`.
*   **Data Retention and Legal Hold UI (REQ-DRH-*)**:
    *   Configuration of retention policies via `res.config.settings` (REQ-DRH-001, REQ-DRH-006).
    *   UI for managing legal holds via `legal_hold_management_views.xml` (REQ-DRH-008).
    *   Wizards or actions for manual deletion/anonymization requests (REQ-DRH-003, REQ-DRH-004) might be added if direct model actions are insufficient, or handled by service calls from forms.
*   **Notifications (REQ-16-012)**: Implemented via `broadcast_notification_wizard`.
*   **UI Consistency (REQ-UIUX-001, REQ-UIUX-010)**: Adherence to Odoo's backend view types (form, list, kanban, search, graph, pivot, calendar, dashboard) and common action patterns.

## 10. Dependencies and Interactions

*   **`influence_gen_services` (REPO-IGBS-003)**: This is the primary dependency. The admin backend UI acts as a presentation layer for the business logic and data models defined in the services module. Most Odoo views in this admin module will be for models defined in `influence_gen_services`. Actions triggered from the UI (e.g., "Approve KYC", "Publish Campaign") will call methods on those service models.
*   **Odoo Core Modules**: `base` (for all core Odoo functionality, users, groups, settings), `mail` (for notifications, messaging), `account` (for payment journal configuration).
*   **`influence_gen_shared_ui` (REPO-IGSUC-006)**: May be used if there are shared backend UI widgets or components (e.g., a custom banner system for `show_in_app_banner`).
*   **`influence_gen_shared_core` (REPO-IGSCU-007)**: May be used for shared utility functions or constants, though less likely for direct UI rendering.

## 11. Future Considerations / Extensibility

*   More granular dashboards for specific areas (e.g., detailed KYC processing times, payment aging).
*   Integration with more sophisticated Business Intelligence (BI) tools if Odoo's reporting is insufficient for complex analytics.
*   Workflow visualization tools for campaign progress or KYC status flow.