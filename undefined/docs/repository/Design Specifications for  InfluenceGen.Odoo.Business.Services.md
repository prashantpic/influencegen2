# Software Design Specification for InfluenceGen.Odoo.Business.Services

## 1. Introduction

This document outlines the software design specification for the `InfluenceGen.Odoo.Business.Services` module. This module encapsulates the core business logic and domain services for the InfluenceGen platform, operating within the Odoo 18 framework. It is responsible for managing influencer onboarding, campaign lifecycles, AI image generation request processing, payment calculations, data validation, business rule enforcement, and data persistence via the Odoo ORM.

This layer interacts with the UI layers (influencer portal and admin backend) by providing services and model methods, and it relies on the `InfluenceGen.Odoo.Infrastructure.Integration.Services` layer for tasks like sending notifications, interacting with N8N, or other external API communications.

**Architecture Style**: Layered Architecture (This module represents the `influencegen-odoo-business-logic-layer`).

**Primary Technology**: Odoo 18, Python 3.11.9, Odoo ORM.

## 2. General Design Principles

*   **Modularity**: Logic is organized into Odoo models and distinct service classes for clear separation of concerns.
*   **Service Layer Pattern**: Complex business processes or logic spanning multiple models are encapsulated in service classes residing in the `services/` directory.
*   **Odoo ORM**: All database interactions are performed through the Odoo ORM, leveraging its features for data access, manipulation, and transactional integrity.
*   **Validation**: Robust server-side validation is implemented at both the model level (using `@api.constrains` and SQL constraints) and within service methods.
*   **Auditability**: Significant business operations and data modifications trigger the creation of audit log entries via the `audit_log_entry` model.
*   **Security**: Business logic adheres to security best practices, particularly in handling sensitive data and enforcing access controls implied by Odoo's security group mechanisms.
*   **Configuration Driven**: Key business rules, quotas, and parameters are designed to be configurable via `PlatformSetting` or specific configuration models rather than hardcoded.
*   **Extensibility**: Design aims to allow future enhancements and modifications with minimal impact on existing functionality.

## 3. Module Structure and Components

The module `influence_gen_services` will follow the standard Odoo module structure.

### 3.1. `__init__.py`
*   **Purpose**: Initializes the Python package for the Odoo business services module.
*   **Logic**:
    *   Imports the `models` submodule.
    *   Imports the `services` submodule.
    *   Imports the `wizards` submodule.
*   **Code**:
    python
    # odoo_modules/influence_gen_services/__init__.py
    from . import models
    from . import services
    from . import wizards
    

### 3.2. `__manifest__.py`
*   **Purpose**: Odoo module manifest file.
*   **Content**:
    python
    # odoo_modules/influence_gen_services/__manifest__.py
    {
        'name': 'InfluenceGen Business Services',
        'version': '18.0.1.0.0',
        'summary': 'Core business logic and domain services for the InfluenceGen platform.',
        'author': 'SSS-AI',
        'website': 'https://www.example.com', # Replace with actual website
        'category': 'Services/InfluenceGen',
        'depends': [
            'base',
            'mail',
            'account', # For payment integration
            # Add other Odoo core dependencies as identified (e.g., 'portal' if directly extending portal features here)
            'influence_gen_infrastructure_integration', # Dependency for REPO-IGOII-004
        ],
        'data': [
            'security/ir.model.access.csv',
            'security/influence_gen_security_groups.xml', # Define security groups if not in a base module
            # Data files for models (e.g., initial data for AreaOfInfluence, PlatformSetting defaults)
            'data/area_of_influence_data.xml',
            'data/platform_setting_data.xml',
            'data/data_retention_policy_data.xml',
            # Wizard views
            'wizards/data_retention_execution_wizard_views.xml',
            'wizards/legal_hold_management_wizard_views.xml',
            # Model views (if any backend views are managed directly by this service layer, e.g., for admin config)
            'views/influencer_profile_views.xml', # Example, may not be needed if UI repo handles this
            'views/campaign_views.xml',
            'views/ai_image_model_views.xml',
            'views/platform_setting_views.xml',
            'views/data_retention_policy_views.xml',
            'views/menu_items.xml', # To access admin configurations for this module
        ],
        'installable': True,
        'application': False,
        'auto_install': False,
        'description': """
    This module encapsulates the core business logic for the InfluenceGen platform, including:
    - Influencer Onboarding & KYC Processing
    - Campaign Management & Lifecycle
    - AI Image Generation Request Handling
    - Influencer Payment Calculation
    - Data Validation and Business Rule Enforcement
    - Data Retention and Legal Hold Management
    """,
    }
    
    **Note**: `influence_gen_infrastructure_integration` is assumed to be the module name for `REPO-IGOII-004`. Update if different.

### 3.3. `models/`

#### 3.3.1. `models/__init__.py`
*   **Purpose**: Initializes the `models` Python package.
*   **Logic**: Imports all model files.
    python
    # odoo_modules/influence_gen_services/models/__init__.py
    from . import influencer_profile
    from . import social_media_profile
    from . import kyc_data
    from . import bank_account
    from . import terms_consent
    from . import campaign
    from . import campaign_application
    from . import content_submission
    from . import content_feedback
    from . import ai_image_model
    from . import ai_image_generation_request
    from . import generated_image
    from . import payment_record
    from . import audit_log_entry
    from . import platform_setting
    from . import data_retention_policy
    from . import area_of_influence
    

#### 3.3.2. `models/influencer_profile.py`
*   **Class**: `InfluenceGenInfluencerProfile`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.influencer_profile`
*   `_description`: "Influencer Profile"
*   `_inherit`: Potentially `['mail.thread', 'mail.activity.mixin']` for communication and activities.
*   **Fields**:
    *   `name`: `fields.Char(string="Full Name", required=True, tracking=True)` (Corresponds to `fullName` in DB design)
    *   `user_id`: `fields.Many2one('res.users', string="Odoo User", ondelete='cascade', required=True, index=True, copy=False)`
    *   `email`: `fields.Char(string="Email", required=True, tracking=True, index=True)` (Related to `user_id.login` but can be distinct if business logic allows)
    *   `phone`: `fields.Char(string="Phone Number", tracking=True)`
    *   `residential_address`: `fields.Text(string="Residential Address", tracking=True)`
    *   `audience_demographics`: `fields.Text(string="Audience Demographics (JSON)")`
    *   `kyc_status`: `fields.Selection([('pending', 'Pending'), ('in_review', 'In Review'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('needs_more_info', 'Needs More Info')], string="KYC Status", default='pending', required=True, tracking=True, index=True)`
    *   `account_status`: `fields.Selection([('inactive', 'Inactive'), ('pending_activation', 'Pending Activation'), ('active', 'Active'), ('suspended', 'Suspended')], string="Account Status", default='inactive', required=True, tracking=True, index=True)`
    *   `social_media_profile_ids`: `fields.One2many('influence_gen.social_media_profile', 'influencer_profile_id', string="Social Media Profiles")`
    *   `kyc_data_ids`: `fields.One2many('influence_gen.kyc_data', 'influencer_profile_id', string="KYC Submissions")`
    *   `bank_account_ids`: `fields.One2many('influence_gen.bank_account', 'influencer_profile_id', string="Bank Accounts")`
    *   `terms_consent_ids`: `fields.One2many('influence_gen.terms_consent', 'influencer_profile_id', string="Terms Consents")`
    *   `area_of_influence_ids`: `fields.Many2many('influence_gen.area_of_influence', 'influencer_area_of_influence_rel', 'influencer_id', 'area_id', string="Areas of Influence")`
    *   `create_date` (Odoo default)
    *   `write_date` (Odoo default)
    *   `onboarding_checklist_json`: `fields.Text(string="Onboarding Checklist (JSON)", default='{}', help="Stores status of various onboarding steps: kyc_submitted, bank_submitted, tos_agreed, etc.")`
*   **SQL Constraints**:
    *   `('email_uniq', 'unique(email)', 'The email address must be unique!')`
    *   `('user_id_uniq', 'unique(user_id)', 'An Odoo user can only be linked to one influencer profile!')`
*   **Methods**:
    *   `_compute_display_name(self)`: Standard Odoo method if needed.
    *   `action_activate_account(self)`:
        *   **Purpose**: Activates the influencer's account. REQ-IOKYC-012.
        *   **Logic**:
            1.  Check if `kyc_status` is 'approved'.
            2.  Check if all required onboarding steps are completed (e.g., based on `onboarding_checklist_json` or presence of verified bank account, ToS consent).
            3.  If all checks pass, set `account_status` to 'active'.
            4.  Log audit event via `AuditLogEntry.create_log_entry`.
            5.  Trigger notification "Account Activated" via notification service (REPO-IGOII-004).
            6.  Return `True` if activated, `False` otherwise.
        *   **Error Handling**: Raise `UserError` if prerequisites not met.
    *   `action_deactivate_account(self, reason="Administrative action")`:
        *   **Purpose**: Deactivates or suspends the influencer's account.
        *   **Logic**:
            1.  Set `account_status` to 'suspended' or 'inactive'.
            2.  Log audit event with reason.
            3.  Trigger notification "Account Deactivated/Suspended".
    *   `update_kyc_status(self, new_status, notes=None)`:
        *   **Purpose**: Updates the overall KYC status of the influencer, usually called by `KYCData` model or `OnboardingService`.
        *   **Logic**:
            1.  Set `kyc_status` to `new_status`.
            2.  If `new_status` is 'approved', attempt `action_activate_account()`.
            3.  Log audit event.
            4.  (Notification triggered by `OnboardingService` or calling method).
    *   `@api.constrains('email') def _check_email_format(self)`:
        *   **Purpose**: Validate email format. REQ-DMG-014.
        *   **Logic**: Use regex or Odoo utility to validate email format. Raise `ValidationError` if invalid.
    *   `check_onboarding_completion(self)`:
        *   **Purpose**: Internal method to check if all mandatory onboarding steps are complete.
        *   **Logic**:
            1.  Verify `kyc_status` is 'approved'.
            2.  Verify at least one `bank_account_id` has `verification_status` 'verified'.
            3.  Verify latest `terms_consent_id` exists and corresponds to current active ToS/Privacy versions.
            4.  Verify at least one `social_media_profile_id` is `verified`.
            5.  Return `True` if all conditions met, `False` otherwise.
    *   `get_latest_terms_consent(self)`:
        *   **Purpose**: Fetches the most recent terms consent record for the influencer.
        *   **Logic**: Search `terms_consent_ids` ordered by `consent_date` desc, limit 1.
    *   `update_onboarding_step_status(self, step_key, status=True)`:
        *   **Purpose**: Updates the `onboarding_checklist_json` for a given step.
        *   **Logic**:
            1. Read `onboarding_checklist_json`.
            2. Update the `step_key` with `status`.
            3. Write back the updated JSON.
    *   `get_primary_bank_account(self)`:
        * **Purpose**: Returns the primary bank account for payouts.
        * **Logic**: Search `bank_account_ids` where `is_primary` is True. Limit 1.

#### 3.3.3. `models/social_media_profile.py`
*   **Class**: `InfluenceGenSocialMediaProfile`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.social_media_profile`
*   `_description`: "Influencer Social Media Profile"
*   **Fields**:
    *   `influencer_profile_id`: `fields.Many2one('influence_gen.influencer_profile', string="Influencer Profile", required=True, ondelete='cascade', index=True)`
    *   `platform`: `fields.Selection([...], string="Platform", required=True)` (e.g., [('instagram', 'Instagram'), ('tiktok', 'TikTok'), ('youtube', 'YouTube'), ('twitter_x', 'Twitter/X'), ('facebook', 'Facebook'), ('linkedin', 'LinkedIn'), ('other', 'Other')])
    *   `platform_other`: `fields.Char(string="Other Platform Name")` (Used if platform is 'other')
    *   `handle`: `fields.Char(string="Handle/Username", required=True)`
    *   `url`: `fields.Char(string="Profile URL")`
    *   `verification_status`: `fields.Selection([('pending', 'Pending'), ('verification_initiated', 'Verification Initiated'), ('verified', 'Verified'), ('failed', 'Failed')], string="Ownership Verification Status", default='pending', required=True, tracking=True, index=True)`
    *   `verification_method`: `fields.Selection([('oauth', 'OAuth'), ('code_in_bio', 'Code in Bio/Post'), ('manual', 'Manual Review'), ('api_insights', 'API Insights')], string="Verification Method")`
    *   `verification_code`: `fields.Char(string="System-Generated Verification Code")` (For 'code_in_bio' method)
    *   `verified_at`: `fields.Datetime(string="Verified At", readonly=True)`
    *   `audience_metrics_json`: `fields.Text(string="Audience Metrics (JSON)")` (e.g., follower_count, engagement_rate)
    *   `last_fetched_at`: `fields.Datetime(string="Metrics Last Fetched At")`
*   **SQL Constraints**:
    *   `('platform_handle_influencer_uniq', 'unique(platform, handle, influencer_profile_id)', 'This social media handle is already registered for this platform by the influencer.')` (As per REQ-IOKYC-002)
*   **Methods**:
    *   `@api.constrains('url', 'platform') def _check_url_format(self)`:
        *   **Purpose**: Validate URL format based on platform. REQ-DMG-015.
        *   **Logic**: Implement regex checks for common platform URL patterns. Raise `ValidationError` if invalid.
    *   `action_initiate_verification(self, method)`:
        *   **Purpose**: Called by `OnboardingService` to start a verification process. REQ-IOKYC-006.
        *   **Logic**:
            1.  Set `verification_method` to `method`.
            2.  If `method` is 'code_in_bio', generate a unique `verification_code` and store it.
            3.  Set `verification_status` to 'verification_initiated'.
            4.  Log audit event.
            5.  Return details needed by UI (e.g., the code for 'code_in_bio').
    *   `action_confirm_verification(self, verification_input=None)`:
        *   **Purpose**: Called by `OnboardingService` to confirm verification. REQ-IOKYC-006.
        *   **Logic**:
            1.  If `verification_method` is 'code_in_bio':
                *   Requires external check (simulated or by admin via UI calling this). Compare `verification_input` (e.g., code found by system/admin) with `self.verification_code`.
            2.  If `verification_method` is 'oauth':
                *   This implies an external OAuth flow, result passed via `verification_input`.
            3.  If `verification_method` is 'manual':
                *   Admin marks as verified.
            4.  If successful: set `verification_status` to 'verified', `verified_at` to `fields.Datetime.now()`.
            5.  If failed: set `verification_status` to 'failed'.
            6.  Log audit event.
            7.  Update `influencer_profile_id.onboarding_checklist_json` for social media verification step.
            8.  Return `True` for success, `False` for failure.
    *   `fetch_audience_metrics(self)`: (Placeholder for potential future enhancement)
        *   **Purpose**: To fetch metrics from social media APIs.
        *   **Logic**: Would call an external service via the infrastructure layer.

#### 3.3.4. `models/kyc_data.py`
*   **Class**: `InfluenceGenKycData`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.kyc_data`
*   `_description`: "Influencer KYC Data Submission"
*   `_order`: `create_date desc`
*   **Fields**:
    *   `influencer_profile_id`: `fields.Many2one('influence_gen.influencer_profile', string="Influencer Profile", required=True, ondelete='cascade', index=True)`
    *   `document_type`: `fields.Selection([...], string="Document Type", required=True)` (e.g., [('passport', 'Passport'), ('driver_license', "Driver's License"), ('national_id', 'National ID')])
    *   `document_front_attachment_id`: `fields.Many2one('ir.attachment', string="Document Front", required=True)`
    *   `document_back_attachment_id`: `fields.Many2one('ir.attachment', string="Document Back (Optional)")`
    *   `submission_date`: `fields.Datetime(string="Submission Date", default=fields.Datetime.now, readonly=True)`
    *   `verification_method`: `fields.Selection([('manual', 'Manual Review'), ('third_party_api', 'Third-Party API')], string="Verification Method", required=True)`
    *   `verification_status`: `fields.Selection([('pending', 'Pending Review'), ('in_review', 'In Review'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('needs_more_info', 'Needs More Info')], string="Verification Status", default='pending', required=True, tracking=True, index=True)`
    *   `reviewer_user_id`: `fields.Many2one('res.users', string="Reviewed By", readonly=True, index=True)`
    *   `reviewed_at`: `fields.Datetime(string="Reviewed At", readonly=True)`
    *   `notes`: `fields.Text(string="Reviewer Notes / Reason for Rejection / Info Requested")`
    *   `third_party_reference_id`: `fields.Char(string="Third-Party Verification ID")` (If using third-party API)
*   **Methods**:
    *   `action_submit_for_review(self)`:
        *   **Purpose**: Marks the submission as ready for review.
        *   **Logic**: Set `verification_status` to 'in_review'. Log audit. Notify admins.
    *   `action_approve(self, reviewer_user_id, notes=None)`:
        *   **Purpose**: Approves the KYC submission. Called by `OnboardingService` or admin UI. REQ-IOKYC-005.
        *   **Logic**:
            1.  Set `verification_status` to 'approved', `reviewer_user_id` to `reviewer_user_id`, `reviewed_at` to `now()`, `notes` if provided.
            2.  Call `self.influencer_profile_id.update_kyc_status('approved')`.
            3.  Update `influencer_profile_id.onboarding_checklist_json` for KYC step.
            4.  Log audit event.
    *   `action_reject(self, reviewer_user_id, reason_notes)`:
        *   **Purpose**: Rejects the KYC submission. REQ-IOKYC-005.
        *   **Logic**:
            1.  Set `verification_status` to 'rejected', `reviewer_user_id`, `reviewed_at`, `notes` to `reason_notes`.
            2.  Call `self.influencer_profile_id.update_kyc_status('rejected', notes=reason_notes)`.
            3.  Log audit event.
    *   `action_request_more_info(self, reviewer_user_id, info_needed_notes)`:
        *   **Purpose**: Requests more information for the KYC submission. REQ-IOKYC-005.
        *   **Logic**:
            1.  Set `verification_status` to 'needs_more_info', `reviewer_user_id`, `reviewed_at`, `notes` to `info_needed_notes`.
            2.  Call `self.influencer_profile_id.update_kyc_status('needs_more_info', notes=info_needed_notes)`.
            3.  Log audit event.

#### 3.3.5. `models/bank_account.py`
*   **Class**: `InfluenceGenBankAccount`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.bank_account`
*   `_description`: "Influencer Bank Account"
*   **Fields**:
    *   `influencer_profile_id`: `fields.Many2one('influence_gen.influencer_profile', string="Influencer Profile", required=True, ondelete='cascade', index=True)`
    *   `account_holder_name`: `fields.Char(string="Account Holder Name", required=True)`
    *   `account_number_encrypted`: `fields.Char(string="Account Number (Encrypted)", required=True)` (Actual encryption handled by utilities/infra layer)
    *   `bank_name`: `fields.Char(string="Bank Name", required=True)`
    *   `routing_number_encrypted`: `fields.Char(string="Routing Number (Encrypted)")`
    *   `iban_encrypted`: `fields.Char(string="IBAN (Encrypted)")`
    *   `swift_code_encrypted`: `fields.Char(string="SWIFT Code (Encrypted)")`
    *   `bank_address`: `fields.Text(string="Bank Address")`
    *   `country_id`: `fields.Many2one('res.country', string="Bank Country")`
    *   `verification_status`: `fields.Selection([('pending', 'Pending'), ('verification_initiated', 'Verification Initiated'), ('verified', 'Verified'), ('failed', 'Failed')], string="Verification Status", default='pending', required=True, tracking=True, index=True)`
    *   `verification_method`: `fields.Selection([('micro_deposit', 'Micro-Deposit'), ('third_party_api', 'Third-Party API'), ('manual_document', 'Manual Document Review')], string="Verification Method")`
    *   `is_primary`: `fields.Boolean(string="Primary Account", default=False, help="Is this the primary account for payouts?")`
*   **Methods**:
    *   `@api.constrains('influencer_profile_id', 'is_primary') def _check_single_primary_account(self)`:
        *   **Purpose**: Ensure an influencer has only one primary bank account.
        *   **Logic**: If `is_primary` is True, search for other primary accounts for the same influencer. If found, raise `ValidationError`.
    *   `action_set_as_primary(self)`:
        *   **Purpose**: Sets this bank account as primary, ensuring others are not.
        *   **Logic**:
            1.  Set `is_primary` to `True` for `self`.
            2.  Find other bank accounts for `self.influencer_profile_id` and set their `is_primary` to `False`.
            3.  Log audit event.
    *   `action_initiate_verification(self, method)`:
        *   **Purpose**: Called by `OnboardingService` to start bank verification. REQ-IOKYC-008.
        *   **Logic**:
            1.  Set `verification_method` to `method`.
            2.  Set `verification_status` to 'verification_initiated'.
            3.  If `method` is 'micro_deposit', trigger external process (via infra layer) to send micro-deposits.
            4.  Log audit event.
            5.  Return details if needed (e.g., instructions for influencer).
    *   `action_confirm_verification(self, verification_input=None)`:
        *   **Purpose**: Called by `OnboardingService` to confirm bank verification. REQ-IOKYC-008.
        *   **Logic**:
            1.  Based on `verification_method` (micro-deposit amounts, third-party API response, manual review).
            2.  If successful: set `verification_status` to 'verified'. Update `influencer_profile_id.onboarding_checklist_json` for bank verification.
            3.  If failed: set `verification_status` to 'failed'.
            4.  Log audit event.
            5.  Return `True` for success, `False` for failure.

#### 3.3.6. `models/terms_consent.py`
*   **Class**: `InfluenceGenTermsConsent`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.terms_consent`
*   `_description`: "Influencer Terms and Policy Consent"
*   `_order`: `consent_date desc`
*   **Fields**:
    *   `influencer_profile_id`: `fields.Many2one('influence_gen.influencer_profile', string="Influencer Profile", required=True, ondelete='cascade', index=True)`
    *   `tos_version`: `fields.Char(string="Terms of Service Version", required=True)`
    *   `privacy_policy_version`: `fields.Char(string="Privacy Policy Version", required=True)`
    *   `consent_date`: `fields.Datetime(string="Consent Date", default=fields.Datetime.now, required=True, readonly=True)`
    *   `ip_address`: `fields.Char(string="IP Address of Consent")`
*   **Methods**:
    *   `@api.model def create_consent(cls, influencer_id, tos_version, privacy_policy_version, ip_address=None)`:
        *   **Purpose**: Logs a new consent record. REQ-IOKYC-009.
        *   **Logic**:
            1.  Create a new `influence_gen.terms_consent` record with provided data.
            2.  Update `influencer_profile_id.onboarding_checklist_json` for ToS agreement.
            3.  Log audit event.
            4.  Return the created record.

#### 3.3.7. `models/campaign.py`
*   **Class**: `InfluenceGenCampaign`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.campaign`
*   `_description`: "Marketing Campaign"
*   `_inherit`: `['mail.thread', 'mail.activity.mixin']`
*   **Fields**:
    *   `name`: `fields.Char(string="Campaign Name", required=True, index=True, tracking=True)`
    *   `description`: `fields.Text(string="Description")`
    *   `brand_client_id`: `fields.Many2one('res.partner', string="Brand/Client", domain="[('is_company', '=', True)]")` (Assuming brands are partners)
    *   `goals_kpis`: `fields.Text(string="Goals and KPIs")`
    *   `target_influencer_criteria_json`: `fields.Text(string="Target Influencer Criteria (JSON)")` (e.g., niche, follower_count_min/max, engagement_rate_min)
    *   `content_requirements_text`: `fields.Text(string="Content Requirements")` (e.g., post type, key messages, hashtags, do's/don'ts)
    *   `budget`: `fields.Float(string="Campaign Budget", digits='Account')`
    *   `compensation_model_type`: `fields.Selection([('flat_fee', 'Flat Fee'), ('commission', 'Commission-Based'), ('product_only', 'Product Only'), ('hybrid', 'Hybrid')], string="Compensation Model Type", required=True)`
    *   `compensation_details`: `fields.Text(string="Compensation Model Details")` (e.g., flat fee amount, commission rate/structure)
    *   `submission_deadline_content`: `fields.Datetime(string="Content Submission Deadline")`
    *   `start_date`: `fields.Date(string="Campaign Start Date", required=True)`
    *   `end_date`: `fields.Date(string="Campaign End Date", required=True)`
    *   `usage_rights_description`: `fields.Text(string="Content Usage Rights")`
    *   `usage_rights_duration_months`: `fields.Integer(string="Usage Rights Duration (Months)")`
    *   `status`: `fields.Selection([('draft', 'Draft'), ('pending_review', 'Pending Review'), ('published', 'Published/Open'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('archived', 'Archived'), ('cancelled', 'Cancelled')], string="Status", default='draft', required=True, tracking=True, index=True)`
    *   `campaign_application_ids`: `fields.One2many('influence_gen.campaign_application', 'campaign_id', string="Applications")`
    *   `payment_record_ids`: `fields.One2many('influence_gen.payment_record', 'campaign_id', string="Payment Records")`
    *   `total_applications_count`: `fields.Integer(string="Total Applications", compute='_compute_campaign_counts')`
    *   `approved_applications_count`: `fields.Integer(string="Approved Applications", compute='_compute_campaign_counts')`
    *   `total_budget_allocated`: `fields.Float(string="Total Budget Allocated", compute='_compute_budget_metrics', digits='Account')`
    *   `actual_performance_metrics_json`: `fields.Text(string="Actual Performance Metrics (JSON)")`
*   **SQL Constraints**:
    *   `('name_uniq', 'unique(name)', 'Campaign name must be unique!')`
*   **Methods**:
    *   `@api.constrains('start_date', 'end_date', 'submission_deadline_content') def _check_dates(self)`:
        *   **Purpose**: Validate date logic. REQ-DMG-016.
        *   **Logic**: `end_date` >= `start_date`. `submission_deadline_content` <= `end_date` (and likely before or on `end_date`). Raise `ValidationError`.
    *   `@api.depends('campaign_application_ids', 'campaign_application_ids.status') def _compute_campaign_counts(self)`:
        *   **Logic**: Calculate `total_applications_count` and `approved_applications_count`.
    *   `@api.depends('payment_record_ids.amount', 'payment_record_ids.status') def _compute_budget_metrics(self)`: (Simplified, might be more complex)
        *   **Logic**: Calculate `total_budget_allocated` based on `payment_record_ids` that are not 'failed' or 'cancelled'.
    *   `action_publish(self)`:
        *   **Purpose**: Sets campaign status to 'Published/Open'. REQ-2-001 related logic.
        *   **Logic**: Set `status` = 'published'. Log audit.
    *   `action_set_in_progress(self)`:
        *   **Logic**: Set `status` = 'in_progress'. Log audit.
    *   `action_complete(self)`:
        *   **Logic**: Set `status` = 'completed'. Log audit.
    *   `action_archive(self)`:
        *   **Logic**: Set `status` = 'archived'. Log audit.
    *   `action_cancel(self)`:
        *   **Logic**: Set `status` = 'cancelled'. Log audit.
    *   `add_manual_performance_metric(self, metric_name, metric_value, influencer_id=None, submission_id=None)`:
        *   **Purpose**: Allows admins to manually input performance data. REQ-2-011.
        *   **Logic**:
            1.  Update/append to `actual_performance_metrics_json`. Structure JSON to allow per-influencer/submission metrics if needed.
            2.  Log audit event.

#### 3.3.8. `models/campaign_application.py`
*   **Class**: `InfluenceGenCampaignApplication`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.campaign_application`
*   `_description`: "Campaign Application by Influencer"
*   `_order`: `submitted_at desc`
*   **Fields**:
    *   `campaign_id`: `fields.Many2one('influence_gen.campaign', string="Campaign", required=True, ondelete='cascade', index=True)`
    *   `influencer_profile_id`: `fields.Many2one('influence_gen.influencer_profile', string="Influencer", required=True, ondelete='cascade', index=True)`
    *   `name`: `fields.Char(string="Application Reference", compute='_compute_name', store=True)`
    *   `proposal_text`: `fields.Text(string="Proposal / Expression of Interest")`
    *   `custom_questions_answers_json`: `fields.Text(string="Custom Questions & Answers (JSON)")`
    *   `status`: `fields.Selection([('submitted', 'Submitted'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('withdrawn_by_influencer', 'Withdrawn by Influencer')], string="Application Status", default='submitted', required=True, tracking=True, index=True)`
    *   `submitted_at`: `fields.Datetime(string="Submitted At", default=fields.Datetime.now, readonly=True)`
    *   `reviewed_at`: `fields.Datetime(string="Reviewed At", readonly=True)`
    *   `reviewer_user_id`: `fields.Many2one('res.users', string="Reviewed By", readonly=True, index=True)`
    *   `rejection_reason`: `fields.Text(string="Reason for Rejection")`
    *   `content_submission_ids`: `fields.One2many('influence_gen.content_submission', 'campaign_application_id', string="Content Submissions")`
*   **SQL Constraints**:
    *   `('campaign_influencer_uniq', 'unique(campaign_id, influencer_profile_id)', 'An influencer can only apply to a specific campaign once.')`
*   **Methods**:
    *   `@api.depends('campaign_id.name', 'influencer_profile_id.name') def _compute_name(self)`:
        *   **Logic**: Create a display name like "[Campaign Name] - [Influencer Name]".
    *   `action_approve(self, reviewer_user_id)`:
        *   **Purpose**: Approves the application. Called by `CampaignService`. REQ-2-007.
        *   **Logic**:
            1.  Set `status` to 'approved', `reviewer_user_id`, `reviewed_at`.
            2.  Log audit event.
            3.  Trigger notification "Application Approved" to influencer.
    *   `action_reject(self, reviewer_user_id, reason)`:
        *   **Purpose**: Rejects the application. REQ-2-007.
        *   **Logic**:
            1.  Set `status` to 'rejected', `reviewer_user_id`, `reviewed_at`, `rejection_reason` to `reason`.
            2.  Log audit event.
            3.  Trigger notification "Application Rejected" to influencer.
    *   `action_withdraw(self)`: (Called by influencer via portal)
        *   **Purpose**: Allows influencer to withdraw their application.
        *   **Logic**: Set `status` to 'withdrawn_by_influencer'. Log audit.

#### 3.3.9. `models/content_submission.py`
*   **Class**: `InfluenceGenContentSubmission`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.content_submission`
*   `_description`: "Campaign Content Submission"
*   `_order`: `submission_date desc`
*   **Fields**:
    *   `campaign_application_id`: `fields.Many2one('influence_gen.campaign_application', string="Campaign Application", required=True, ondelete='cascade', index=True)`
    *   `campaign_id`: `fields.Many2one(related='campaign_application_id.campaign_id', string="Campaign", store=True, readonly=True, index=True)`
    *   `influencer_profile_id`: `fields.Many2one(related='campaign_application_id.influencer_profile_id', string="Influencer", store=True, readonly=True, index=True)`
    *   `name`: `fields.Char(string="Submission Title/Reference", compute='_compute_name', store=True)`
    *   `content_attachment_ids`: `fields.Many2many('ir.attachment', string="Content Files")` (For uploaded files)
    *   `content_link`: `fields.Char(string="Link to Content (e.g., social media post)")`
    *   `content_text_caption`: `fields.Text(string="Text/Caption")`
    *   `generated_image_id`: `fields.Many2one('influence_gen.generated_image', string="Associated AI Generated Image", ondelete='set null')`
    *   `submission_date`: `fields.Datetime(string="Submission Date", default=fields.Datetime.now, readonly=True)`
    *   `review_status`: `fields.Selection([('pending_review', 'Pending Review'), ('revision_requested', 'Revision Requested'), ('approved', 'Approved'), ('rejected', 'Rejected')], string="Review Status", default='pending_review', required=True, tracking=True, index=True)`
    *   `reviewed_by_user_id`: `fields.Many2one('res.users', string="Reviewed By", readonly=True, index=True)`
    *   `reviewed_at`: `fields.Datetime(string="Reviewed At", readonly=True)`
    *   `version`: `fields.Integer(string="Version", default=1, readonly=True)`
    *   `feedback_history_ids`: `fields.One2many('influence_gen.content_feedback', 'content_submission_id', string="Feedback History")`
    *   `is_final_submission`: `fields.Boolean(string="Is Final Submission?", default=False)` (Could be used to trigger payment logic)
*   **Methods**:
    *   `@api.depends('campaign_id.name', 'influencer_profile_id.name', 'submission_date') def _compute_name(self)`:
        *   **Logic**: e.g., "[Campaign] - [Influencer] - Submission [Date]".
    *   `action_approve(self, reviewer_user_id)`:
        *   **Purpose**: Approves content. Called by `CampaignService`. REQ-2-010.
        *   **Logic**:
            1.  Set `review_status` to 'approved', `reviewed_by_user_id`, `reviewed_at`.
            2.  Set `is_final_submission` to `True` (or based on campaign rules).
            3.  Log audit event.
            4.  Trigger notification "Content Approved" to influencer.
            5.  Potentially trigger payment record creation via `PaymentService` if `is_final_submission`.
    *   `action_reject(self, reviewer_user_id, feedback_text)`:
        *   **Purpose**: Rejects content. REQ-2-010.
        *   **Logic**:
            1.  Set `review_status` to 'rejected', `reviewed_by_user_id`, `reviewed_at`.
            2.  Create a `influence_gen.content_feedback` record with `feedback_text`.
            3.  Log audit event.
            4.  Trigger notification "Content Rejected" to influencer.
    *   `action_request_revision(self, reviewer_user_id, feedback_text)`:
        *   **Purpose**: Requests revision. REQ-2-010.
        *   **Logic**:
            1.  Set `review_status` to 'revision_requested', `reviewed_by_user_id`, `reviewed_at`.
            2.  Create a `influence_gen.content_feedback` record with `feedback_text`.
            3.  Log audit event.
            4.  Trigger notification "Revision Requested" to influencer.
    *   `create_new_version_for_revision(self, new_content_data)`:
        *   **Purpose**: Creates a new submission record for a revision.
        *   **Logic**:
            1.  `self.copy()` with updated `version` number (incremented), new `content_attachment_ids`/`content_link`, `submission_date` = now(), `review_status` = 'pending_review'.
            2.  Link previous version or mark old one as superseded if needed.
            3.  Return new submission record.

#### 3.3.10. `models/content_feedback.py`
*   **Class**: `InfluenceGenContentFeedback`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.content_feedback`
*   `_description`: "Feedback on Content Submission"
*   `_order`: `create_date desc`
*   **Fields**:
    *   `content_submission_id`: `fields.Many2one('influence_gen.content_submission', string="Content Submission", required=True, ondelete='cascade', index=True)`
    *   `reviewer_user_id`: `fields.Many2one('res.users', string="Reviewer", required=True, readonly=True)`
    *   `feedback_text`: `fields.Text(string="Feedback", required=True)`
    *   `create_date`: `fields.Datetime(string="Feedback Date", default=fields.Datetime.now, readonly=True)` (Odoo default)

#### 3.3.11. `models/ai_image_model.py`
*   **Class**: `InfluenceGenAiImageModel`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.ai_image_model`
*   `_description`: "AI Image Generation Model Configuration"
*   **Fields**:
    *   `name`: `fields.Char(string="Model Name", required=True, unique=True, index=True)`
    *   `description`: `fields.Text(string="Description")`
    *   `trigger_keywords`: `fields.Char(string="Trigger Keywords (comma-separated)")`
    *   `is_active`: `fields.Boolean(string="Active", default=True, index=True)`
    *   `external_model_id`: `fields.Char(string="External Model ID (for AI Service)")`
    *   `notes`: `fields.Text(string="Internal Notes")`

#### 3.3.12. `models/ai_image_generation_request.py`
*   **Class**: `InfluenceGenAiImageGenerationRequest`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.ai_image_generation_request`
*   `_description`: "AI Image Generation Request"
*   `_order`: `create_date desc`
*   **Fields**:
    *   `user_id`: `fields.Many2one('res.users', string="Requesting User", required=True, ondelete='restrict', index=True)`
    *   `influencer_profile_id`: `fields.Many2one('influence_gen.influencer_profile', string="Associated Influencer Profile", compute='_compute_influencer_profile', store=True, readonly=True, index=True)`
    *   `campaign_id`: `fields.Many2one('influence_gen.campaign', string="Associated Campaign", ondelete='set null', index=True)`
    *   `prompt`: `fields.Text(string="Prompt", required=True)`
    *   `negative_prompt`: `fields.Text(string="Negative Prompt")`
    *   `model_id`: `fields.Many2one('influence_gen.ai_image_model', string="AI Model Used", required=True, ondelete='restrict')`
    *   `resolution_width`: `fields.Integer(string="Width (px)")`
    *   `resolution_height`: `fields.Integer(string="Height (px)")`
    *   `aspect_ratio`: `fields.Char(string="Aspect Ratio")` (e.g., "1:1", "16:9")
    *   `seed`: `fields.Integer(string="Seed")`
    *   `inference_steps`: `fields.Integer(string="Inference Steps")`
    *   `cfg_scale`: `fields.Float(string="CFG Scale", digits=(3,1))`
    *   `status`: `fields.Selection([('queued', 'Queued'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], string="Status", default='queued', required=True, tracking=True, index=True)`
    *   `intended_use`: `fields.Selection([('personal_exploration', 'Personal Exploration'), ('campaign_specific', 'Campaign Specific')], string="Intended Use", default='personal_exploration', required=True)`
    *   `error_details`: `fields.Text(string="Error Details", readonly=True)`
    *   `n8n_execution_id`: `fields.Char(string="N8N Execution ID", readonly=True, index=True)`
    *   `generated_image_ids`: `fields.One2many('influence_gen.generated_image', 'request_id', string="Generated Images")`
    *   `usage_tracking_log_ids`: `fields.One2many('influence_gen.usage_tracking_log', 'ai_request_id', string="Usage Logs")`
*   **Methods**:
    *   `@api.depends('user_id') def _compute_influencer_profile(self)`:
        *   **Logic**: Find `influence_gen.influencer_profile` linked to `self.user_id`.
    *   `action_cancel_request(self)`:
        *   **Logic**: If status is 'queued' or 'processing' (if cancellable), set status to 'cancelled'. Log audit. Potentially notify N8N if processing.
    *   `_log_usage(self, event_type="request_created", details=None)`:
        *   **Purpose**: Internal helper to create UsageTrackingLog entries. REQ-AIGS-007.
        *   **Logic**: Create `influence_gen.usage_tracking_log` record linked to this request.

#### 3.3.13. `models/generated_image.py`
*   **Class**: `InfluenceGenGeneratedImage`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.generated_image`
*   `_description`: "AI Generated Image"
*   `_order`: `create_date desc`
*   **Fields**:
    *   `request_id`: `fields.Many2one('influence_gen.ai_image_generation_request', string="Source Request", required=True, ondelete='cascade', index=True)`
    *   `user_id`: `fields.Many2one(related='request_id.user_id', string="Generated By User", store=True, readonly=True, index=True)`
    *   `influencer_profile_id`: `fields.Many2one(related='request_id.influencer_profile_id', string="Generated For Influencer", store=True, readonly=True, index=True)`
    *   `campaign_id`: `fields.Many2one(related='request_id.campaign_id', string="Associated Campaign", store=True, readonly=True, index=True)`
    *   `storage_attachment_id`: `fields.Many2one('ir.attachment', string="Image File Attachment", required=True, ondelete='restrict')`
    *   `name`: `fields.Char(string="Image Name/Title", related='storage_attachment_id.name', readonly=False)`
    *   `file_format`: `fields.Char(string="File Format", compute='_compute_file_details', store=True)`
    *   `file_size`: `fields.Integer(string="File Size (bytes)", compute='_compute_file_details', store=True)`
    *   `width`: `fields.Integer(string="Width (px)", related='request_id.resolution_width', store=True, readonly=True)`
    *   `height`: `fields.Integer(string="Height (px)", related='request_id.resolution_height', store=True, readonly=True)`
    *   `hash_value`: `fields.Char(string="Image Hash (SHA256)", index=True, readonly=True)`
    *   `retention_category`: `fields.Selection([...], string="Retention Category", required=True, index=True)` (e.g., based on `request_id.intended_use` and `campaign_id.usage_rights_duration_months`)
    *   `usage_rights_details`: `fields.Text(string="Specific Usage Rights Applied", compute='_compute_usage_rights', store=True)`
    *   `is_submitted_to_campaign`: `fields.Boolean(string="Submitted to Campaign?", compute='_compute_is_submitted_to_campaign', store=True)`
*   **Methods**:
    *   `@api.depends('storage_attachment_id.mimetype', 'storage_attachment_id.file_size') def _compute_file_details(self)`:
        *   **Logic**: Populate `file_format` from mimetype and `file_size`.
    *   `@api.model def create_from_generation(cls, request_id, attachment_id, image_binary_data)`:
        *   **Purpose**: Main method to create a `GeneratedImage` record after successful AI generation. REQ-AIGS-006, REQ-AIGS-010.
        *   **Logic**:
            1.  Calculate `hash_value` from `image_binary_data`.
            2.  Determine `retention_category` based on `request_id.intended_use` and `request_id.campaign_id.usage_rights_duration_months` if applicable.
            3.  Create the `GeneratedImage` record.
            4.  Log audit event.
            5.  Return created record.
    *   `@api.depends('request_id.campaign_id.usage_rights_description', 'request_id.intended_use') def _compute_usage_rights(self)`:
        *   **Logic**: Determine and set `usage_rights_details` based on campaign or default platform policy for personal use.
    *   `_compute_is_submitted_to_campaign(self)`:
        *   **Logic**: Check if this `generated_image_id` is referenced in any `influence_gen.content_submission` record.
    *   `action_apply_retention_policy(self)`:
        *   **Purpose**: Called by `DataManagementService` or scheduled job. REQ-AIGS-011, REQ-DRH-005.
        *   **Logic**: Based on `retention_category` and `create_date`, determine if image should be deleted/archived. If so, perform action (e.g., unlink `storage_attachment_id` and self, or flag for archival). Log action.

#### 3.3.14. `models/payment_record.py`
*   **Class**: `InfluenceGenPaymentRecord`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.payment_record`
*   `_description`: "Influencer Payment Record"
*   `_order`: `create_date desc`
*   **Fields**:
    *   `name`: `fields.Char(string="Payment Reference", compute='_compute_name', store=True)`
    *   `influencer_profile_id`: `fields.Many2one('influence_gen.influencer_profile', string="Influencer", required=True, ondelete='restrict', index=True)`
    *   `campaign_id`: `fields.Many2one('influence_gen.campaign', string="Campaign", ondelete='set null', index=True)`
    *   `content_submission_id`: `fields.Many2one('influence_gen.content_submission', string="Related Content Submission", ondelete='set null', index=True)`
    *   `amount`: `fields.Monetary(string="Amount", required=True, currency_field='currency_id')`
    *   `currency_id`: `fields.Many2one('res.currency', string="Currency", required=True, default=lambda self: self.env.company.currency_id.id)`
    *   `status`: `fields.Selection([('pending_approval', 'Pending Approval'), ('approved_for_payment', 'Approved for Payment'), ('processing', 'Processing'), ('paid', 'Paid'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], string="Status", default='pending_approval', required=True, tracking=True, index=True)`
    *   `transaction_id_external`: `fields.Char(string="External Transaction ID", readonly=True)`
    *   `payment_method_type`: `fields.Char(string="Payment Method Type")` (e.g., from BankAccount)
    *   `bank_account_id`: `fields.Many2one('influence_gen.bank_account', string="Paid to Bank Account", ondelete='restrict')`
    *   `due_date`: `fields.Date(string="Due Date", index=True)`
    *   `paid_date`: `fields.Date(string="Paid Date", readonly=True)`
    *   `notes`: `fields.Text(string="Notes")`
    *   `odoo_vendor_bill_id`: `fields.Many2one('account.move', string="Odoo Vendor Bill/Payment", readonly=True, copy=False, index=True)` (Link to Odoo accounting transaction)
*   **Methods**:
    *   `@api.depends('influencer_profile_id.name', 'amount', 'currency_id.symbol', 'create_date') def _compute_name(self)`:
        *   **Logic**: e.g., "[Influencer] - [Amount] [Currency] - [Date]".
    *   `action_approve_for_payment(self)`:
        *   **Purpose**: Admin approves the payment record.
        *   **Logic**: Set `status` to 'approved_for_payment'. Log audit. Trigger `PaymentService` to potentially batch this for vendor bill creation.
    *   `action_mark_as_processing(self, vendor_bill_id=None)`:
        *   **Logic**: Set `status` to 'processing'. If `vendor_bill_id`, link it. Log audit.
    *   `action_mark_as_paid(self, transaction_id_external, paid_date, payment_method_type=None, bank_account_id=None)`:
        *   **Purpose**: Marks payment as paid. REQ-2-015.
        *   **Logic**: Set `status` to 'paid', `transaction_id_external`, `paid_date`. Optionally `payment_method_type`, `bank_account_id`. Log audit. Notify influencer.
    *   `action_mark_as_failed(self, reason)`:
        *   **Logic**: Set `status` to 'failed', add `reason` to `notes`. Log audit. Notify admin/influencer.
    *   `action_cancel_payment(self, reason)`:
        *   **Logic**: Set `status` to 'cancelled', add `reason` to `notes`. Log audit.

#### 3.3.15. `models/audit_log_entry.py`
*   **Class**: `InfluenceGenAuditLogEntry`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.audit_log_entry`
*   `_description`: "System Audit Log Entry"
*   `_order`: `timestamp desc`
*   **Fields**:
    *   `timestamp`: `fields.Datetime(string="Timestamp (UTC)", default=fields.Datetime.now, required=True, readonly=True, index=True)`
    *   `event_type`: `fields.Char(string="Event Type", required=True, index=True)` (e.g., 'USER_LOGIN_SUCCESS', 'KYC_STATUS_UPDATED', 'CAMPAIGN_CREATED')
    *   `actor_user_id`: `fields.Many2one('res.users', string="Actor User", ondelete='set null', readonly=True, index=True)`
    *   `actor_description`: `fields.Char(string="Actor Description", compute='_compute_actor_description', store=True)` (e.g., User name or "System Process")
    *   `target_model_name`: `fields.Char(string="Target Model", readonly=True, index=True)`
    *   `target_record_id`: `fields.Integer(string="Target Record ID", readonly=True, index=True)`
    *   `target_record_display_name`: `fields.Char(string="Target Record Name", compute='_compute_target_display_name', store=False)` (Non-stored, for display)
    *   `action_performed`: `fields.Char(string="Action Performed", required=True, readonly=True)` (e.g., 'CREATE', 'WRITE', 'UNLINK', 'LOGIN_ATTEMPT')
    *   `details_json`: `fields.Text(string="Details (JSON)", readonly=True)` (Store old/new values, parameters, etc.)
    *   `ip_address`: `fields.Char(string="Source IP Address", readonly=True)`
    *   `outcome`: `fields.Selection([('success', 'Success'), ('failure', 'Failure')], string="Outcome", readonly=True)`
    *   `failure_reason`: `fields.Text(string="Failure Reason", readonly=True)`
*   **Methods**:
    *   `@api.model def create_log(cls, event_type, actor_user_id, action_performed, target_object=None, details_dict=None, ip_address=None, outcome='success', failure_reason=None)`:
        *   **Purpose**: Central method to create audit log entries. REQ-ATEL-005, REQ-ATEL-006.
        *   **Logic**:
            1.  Gather all required information.
            2.  If `target_object` (an Odoo recordset) is provided, extract `target_model_name` and `target_record_id`.
            3.  Serialize `details_dict` to JSON for `details_json`.
            4.  `cls.create({...})` with the prepared values.
    *   `@api.depends('actor_user_id') def _compute_actor_description(self)`:
        *   **Logic**: If `actor_user_id`, set to `actor_user_id.name`. Else, "System Process".
    *   `def _compute_target_display_name(self)`: (May need careful implementation to avoid performance issues or errors if target record deleted)
        *   **Logic**: If `target_model_name` and `target_record_id`, try to fetch and return `display_name` of the target record. Handle exceptions if record not found.

#### 3.3.16. `models/platform_setting.py`
*   **Class**: `InfluenceGenPlatformSetting`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.platform_setting`
*   `_description`: "InfluenceGen Platform Setting"
*   **Fields**:
    *   `key`: `fields.Char(string="Setting Key", required=True, index=True, unique=True, copy=False)`
    *   `value_text`: `fields.Text(string="Setting Value")`
    *   `value_type`: `fields.Selection([('string', 'String'), ('integer', 'Integer'), ('float', 'Float'), ('boolean', 'Boolean'), ('json', 'JSON')], string="Value Type", required=True, default='string')`
    *   `description`: `fields.Text(string="Description")`
    *   `module`: `fields.Char(string="Module", help="Technical name of the module that defines this setting.")`
*   **Methods**:
    *   `@api.model def get_param(cls, key, default=None)`:
        *   **Purpose**: Retrieves a setting value, casting it to its `value_type`.
        *   **Logic**:
            1.  Search for record with `key`.
            2.  If not found, return `default`.
            3.  Cast `value_text` based on `value_type` (e.g., `bool(value_text == 'True')`, `int(value_text)`, `json.loads(value_text)`).
            4.  Return casted value.
    *   `@api.model def set_param(cls, key, value, value_type, description=None, module=None)`:
        *   **Purpose**: Creates or updates a setting.
        *   **Logic**:
            1.  Search for record with `key`.
            2.  Convert `value` to string for `value_text` (e.g., `str(value)`, `json.dumps(value)`).
            3.  If record exists, update it. Else, create new.
            4.  Log audit of setting change.

#### 3.3.17. `models/data_retention_policy.py`
*   **Class**: `InfluenceGenDataRetentionPolicy`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.data_retention_policy`
*   `_description`: "Data Retention Policy"
*   **Fields**:
    *   `name`: `fields.Char(string="Policy Name", required=True)`
    *   `data_category`: `fields.Selection([...], string="Data Category", required=True, index=True)` (e.g., [('pii_influencer', 'Influencer PII'), ('kyc_documents', 'KYC Documents'), ... ('audit_logs', 'Audit Logs')])
    *   `model_name`: `fields.Char(string="Target Odoo Model Technical Name")` (e.g., 'influence_gen.influencer_profile')
    *   `retention_period_days`: `fields.Integer(string="Retention Period (Days)", required=True, help="Number of days data in this category should be actively retained.")`
    *   `disposition_action`: `fields.Selection([('delete', 'Secure Delete'), ('anonymize', 'Anonymize'), ('archive', 'Archive')], string="Disposition Action", required=True)`
    *   `is_active`: `fields.Boolean(string="Active Policy", default=True, index=True)`
    *   `description`: `fields.Text(string="Policy Description and Basis")`
    *   `legal_hold_overrideable`: `fields.Boolean(string="Overrideable by Legal Hold?", default=True)`
*   **Methods**:
    *   `@api.model def get_active_policy(cls, data_category=None, model_name=None)`:
        *   **Purpose**: Retrieves the active policy for a given category or model.
        *   **Logic**: Search for active policy matching criteria.
#### 3.3.18. `models/area_of_influence.py`
*   **Class**: `InfluenceGenAreaOfInfluence`
*   **Inherits**: `models.Model`
*   `_name`: `influence_gen.area_of_influence`
*   `_description`: "Area of Influence / Niche"
*   `_order`: `name`
*   **Fields**:
    *   `name`: `fields.Char(string="Name", required=True, index=True, unique=True)`
    *   `description`: `fields.Text(string="Description")`
    *   `influencer_profile_ids`: `fields.Many2many('influence_gen.influencer_profile', 'influencer_area_of_influence_rel', 'area_id', 'influencer_id', string="Influencers")`

### 3.4. `services/`

#### 3.4.1. `services/__init__.py`
*   **Purpose**: Initializes the `services` Python package.
*   **Logic**: Imports all service classes.
    python
    # odoo_modules/influence_gen_services/services/__init__.py
    from . import onboarding_service
    from . import campaign_service
    from . import ai_image_service
    from . import payment_service
    from . import data_management_service
    # Potentially an audit_service if complex audit logic is needed beyond model helper
    

#### 3.4.2. `services/onboarding_service.py`
*   **Class**: `OnboardingService`
*   **Purpose**: Orchestrates the influencer onboarding process.
*   **Methods**:
    *   `__init__(self, env)`: Store `self.env`.
    *   `process_registration_submission(self, influencer_data)`: REQ-IOKYC-002.
        *   **Logic**:
            1.  Validate `influencer_data` (required fields, formats).
            2.  Create `res.users` record (if not exists/provided).
            3.  Create `influence_gen.influencer_profile` record, link to user. Set initial `kyc_status`, `account_status`.
            4.  Create `influence_gen.social_media_profile` records from submitted data.
            5.  Initialize `onboarding_checklist_json`.
            6.  Log audit event.
            7.  Trigger "Registration Received" notification via `NotificationService` (REPO-IGOII-004).
            8.  Return created `InfluencerProfile` record.
    *   `handle_kyc_document_submission(self, influencer_id, document_type, front_attachment_data, back_attachment_data=None, verification_method='manual')`: REQ-IOKYC-005.
        *   **Logic**:
            1.  Find `InfluencerProfile` by `influencer_id`.
            2.  Create `ir.attachment` records for `front_attachment_data` and `back_attachment_data`.
            3.  Create `influence_gen.kyc_data` record, linking attachments, setting `verification_method`.
            4.  Update `influencer_profile_id.kyc_status` to 'in_review'.
            5.  Update `influencer_profile_id.onboarding_checklist_json` for kyc submission.
            6.  Log audit.
            7.  Trigger notification "KYC Documents Received" to influencer and "KYC Awaiting Review" to admins.
    *   `handle_kyc_review_decision(self, kyc_data_id, decision, reviewer_user_id, notes=None, reason_if_rejected=None, info_needed_if_more_info=None)`: REQ-IOKYC-005.
        *   **Logic**:
            1.  Fetch `KYCData` record.
            2.  Based on `decision` ('approved', 'rejected', 'needs_more_info'):
                *   Call `kyc_data_id.action_approve(reviewer_user_id, notes)` or `action_reject(...)` or `action_request_more_info(...)`.
            3.  Trigger appropriate notification to influencer ("KYC Approved/Rejected/More Info Needed").
    *   `initiate_social_media_verification(self, social_profile_id, method)`: REQ-IOKYC-006.
        *   **Logic**:
            1.  Fetch `SocialMediaProfile` record.
            2.  Call `social_profile_id.action_initiate_verification(method)`.
            3.  Return verification details (e.g., code) for UI.
            4.  Trigger notification to influencer with instructions if needed.
    *   `confirm_social_media_verification(self, social_profile_id, verification_input=None)`: REQ-IOKYC-006.
        *   **Logic**:
            1.  Fetch `SocialMediaProfile` record.
            2.  Call `social_profile_id.action_confirm_verification(verification_input)`.
            3.  If successful, notify influencer. If failed, notify and potentially log.
    *   `initiate_bank_account_verification(self, bank_account_id, method)`: REQ-IOKYC-008.
        *   **Logic**: Similar to social media verification initiation.
    *   `confirm_bank_account_verification(self, bank_account_id, verification_input=None)`: REQ-IOKYC-008.
        *   **Logic**: Similar to social media verification confirmation.
    *   `record_terms_consent(self, influencer_id, tos_version, privacy_policy_version, ip_address=None)`: REQ-IOKYC-009.
        *   **Logic**: Call `TermsConsent.create_consent(...)`.
    *   `check_and_activate_influencer_account(self, influencer_id)`: REQ-IOKYC-012.
        *   **Logic**:
            1.  Fetch `InfluencerProfile`.
            2.  Call `influencer_id.check_onboarding_completion()`.
            3.  If true, call `influencer_id.action_activate_account()`.

#### 3.4.3. `services/campaign_service.py`
*   **Class**: `CampaignService`
*   **Purpose**: Orchestrates campaign management.
*   **Methods**:
    *   `__init__(self, env)`: Store `self.env`.
    *   `create_campaign(self, campaign_data)`: REQ-2-001, REQ-2-002, REQ-IPF-003.
        *   **Logic**: Validate data, create `Campaign` record. Log audit.
    *   `update_campaign_status(self, campaign_id, new_status)`:
        *   **Logic**: Fetch `Campaign`. Call appropriate `action_...` method on it (e.g., `action_publish`).
    *   `process_campaign_application(self, influencer_id, campaign_id, proposal_text=None, custom_answers_json=None)`:
        *   **Logic**:
            1.  Validate eligibility if any rules apply.
            2.  Create `CampaignApplication` record.
            3.  Log audit.
            4.  Trigger "Application Submitted" notification to influencer and relevant admin/manager.
    *   `review_campaign_application(self, application_id, decision, reviewer_user_id, reason_if_rejected=None)`: REQ-2-007.
        *   **Logic**:
            1.  Fetch `CampaignApplication`.
            2.  If `decision` is 'approved', call `application_id.action_approve(reviewer_user_id)`.
            3.  If `decision` is 'rejected', call `application_id.action_reject(reviewer_user_id, reason_if_rejected)`.
            4.  (Notifications are handled by model actions).
    *   `handle_content_submission(self, application_id, content_attachments=None, content_link=None, content_caption=None, generated_image_id=None)`:
        *   **Logic**:
            1.  Fetch `CampaignApplication`.
            2.  Create `ContentSubmission` record. Link `ir.attachment` for files.
            3.  Log audit.
            4.  Trigger "Content Submitted" notification to admin.
    *   `review_content_submission(self, submission_id, decision, reviewer_user_id, feedback_text=None)`: REQ-2-010. (Corresponds to `SEQ-CMP-005`)
        *   **Logic**:
            1.  Fetch `ContentSubmission`.
            2.  Based on `decision` ('approved', 'rejected', 'revision_requested'):
                *   Call respective `action_...` method on `submission_id` (e.g., `action_approve`, `action_reject`, `action_request_revision`).
            3.  (Notifications handled by model actions).
    *   `record_campaign_performance_metrics(self, campaign_id, metrics_data, influencer_id=None, submission_id=None)`: REQ-2-011.
        *   **Logic**:
            1.  Fetch `Campaign`.
            2.  Call `campaign_id.add_manual_performance_metric(...)`.
            3.  Log audit.

#### 3.4.4. `services/ai_image_service.py`
*   **Class**: `AIImageService`
*   **Purpose**: Manages AI image generation business logic.
*   **Methods**:
    *   `__init__(self, env)`: Store `self.env`.
    *   `prepare_ai_generation_request(self, user_id, prompt, negative_prompt=None, model_id=None, campaign_id=None, intended_use='personal_exploration', **params)`: REQ-AIGS-003, REQ-AIGS-004.
        *   **Logic**:
            1.  Fetch `res.users` and associated `InfluencerProfile`.
            2.  Validate `prompt` against content moderation rules (from `PlatformSetting` or dedicated service). REQ-AIGS-003. If fails, return error.
            3.  Validate `params` against `PlatformSetting` defaults/ranges for AI parameters. REQ-AIGS-004.
            4.  Check user's AI generation quota (from `PlatformSetting` and `UsageTrackingLog`). REQ-AIGS-002. If exceeded, return error.
            5.  Create `AIImageGenerationRequest` record with status 'queued'.
            6.  Decrement user quota (or pre-authorize).
            7.  Log `UsageTrackingLog` for the request initiation. REQ-AIGS-007.
            8.  Trigger webhook to N8N via Infrastructure Integration Service (REPO-IGOII-004), passing request ID and parameters.
            9.  Log audit.
            10. Return created `AIImageGenerationRequest` record.
    *   `process_ai_generation_callback(self, request_id, image_binary_data_or_url, n8n_execution_id, success=True, error_details=None)`: REQ-AIGS-006, REQ-AIGS-010.
        *   **Logic**:
            1.  Fetch `AIImageGenerationRequest` by `request_id`.
            2.  Update `n8n_execution_id`.
            3.  If `success`:
                *   If `image_binary_data_or_url` is URL, instruct Infrastructure layer to download it. Get binary data.
                *   Create `ir.attachment` for the image.
                *   Call `GeneratedImage.create_from_generation(request_id, attachment_id, image_binary_data)`.
                *   Set `AIImageGenerationRequest.status` to 'completed'.
                *   Log `UsageTrackingLog` for successful generation.
            4.  If `not success`:
                *   Set `AIImageGenerationRequest.status` to 'failed', store `error_details`.
                *   Revert quota decrement if applicable.
                *   Log `UsageTrackingLog` for failed attempt.
            5.  Log audit.
            6.  Trigger UI update/notification to user about completion/failure.
    *   `get_user_ai_quota_status(self, user_id)`: REQ-AIGS-002, REQ-AIGS-007.
        *   **Logic**: Fetch default quota from `PlatformSetting`. Fetch user's usage from `UsageTrackingLog`. Calculate remaining quota.
    *   `manage_ai_model_configurations(self, action, model_data=None, model_id=None)`: REQ-AIGS-004.
        *   **Logic**: CRUD operations on `AIImageModel` records. Log audit.

#### 3.4.5. `services/payment_service.py`
*   **Class**: `PaymentService`
*   **Purpose**: Manages influencer payment calculations and batching.
*   **Methods**:
    *   `__init__(self, env)`: Store `self.env`.
    *   `calculate_owed_amounts_for_influencer(self, influencer_id, campaign_id=None)`: REQ-2-013, REQ-IPF-004.
        *   **Logic**:
            1.  Fetch approved `ContentSubmission` records for the influencer (and optionally campaign).
            2.  For each, determine compensation based on `Campaign.compensation_model_type` and `compensation_details`.
            3.  Aggregate amounts not yet in a 'paid' or 'processing' `PaymentRecord`.
            4.  Return list of payment details (amount, currency, related submission/campaign).
    *   `generate_payment_batch_data(self, influencer_ids=None, campaign_id=None, due_date_filter=None)`: REQ-2-014, REQ-IPF-005.
        *   **Logic**:
            1.  Identify pending `PaymentRecord` records matching criteria (status 'approved_for_payment').
            2.  Group them for batch processing.
            3.  Return data suitable for creating vendor bills in Odoo accounting.
    *   `process_payment_batch_creation(self, payment_record_ids_to_process)`: REQ-2-014, REQ-IPF-005.
        *   **Logic**:
            1.  For given `PaymentRecord` IDs (status 'approved_for_payment'):
                *   Call Infrastructure Integration Service to create Vendor Bills in `account.move`.
                *   Update `PaymentRecord.odoo_vendor_bill_id` and set `status` to 'processing'.
            2.  Log audit.
    *   `update_payment_status_from_accounting(self, payment_record_id_or_bill_ref, new_status, transaction_id_external=None, paid_date=None, failure_reason=None)`: REQ-2-015.
        *   **Logic**:
            1.  Fetch `PaymentRecord` (either directly or via `odoo_vendor_bill_id`).
            2.  If `new_status` is 'paid', call `payment_record_id.action_mark_as_paid(...)`.
            3.  If `new_status` is 'failed', call `payment_record_id.action_mark_as_failed(...)`.
            4.  Log audit.

#### 3.4.6. `services/data_management_service.py`
*   **Class**: `DataManagementService`
*   **Purpose**: Manages data retention, archival, and legal holds.
*   **Methods**:
    *   `__init__(self, env)`: Store `self.env`.
    *   `apply_data_retention_policies(self, data_category=None, dry_run=False)`: REQ-DRH-001, REQ-DRH-002, REQ-DRH-005, REQ-DRH-006, REQ-IPF-008, REQ-AIGS-011.
        *   **Logic**:
            1.  Fetch active `DataRetentionPolicy` records (filtered by `data_category` if provided).
            2.  For each policy:
                *   Identify records in `policy.model_name` older than `policy.retention_period_days` and not under legal hold (check `LegalHold` model - not explicitly defined in file structure, assume an implicit one or use flags on target models).
                *   If `dry_run`, log what would be done.
                *   Else, perform `policy.disposition_action` ('delete', 'anonymize', 'archive').
                    *   'delete': `record.unlink()`.
                    *   'anonymize': Implement anonymization logic specific to the model (e.g., clear PII fields).
                    *   'archive': Flag for archival or trigger archival process via infra layer. REQ-DRH-007.
                *   Log disposition actions in audit log.
    *   `process_pii_erasure_request(self, influencer_id, data_scope_description)`: REQ-DRH-003.
        *   **Logic**:
            1.  Identify PII data for `influencer_id` based on `data_scope_description`.
            2.  Check for legal holds or overriding contractual constraints.
            3.  If clear, perform secure deletion/anonymization.
            4.  Log actions and decision process in audit log.
    *   `assess_pii_in_campaign_content_for_erasure(self, content_submission_id, influencer_id)`: REQ-DRH-004.
        *   **Logic**:
            1.  Fetch `ContentSubmission`.
            2.  Assess campaign usage rights from `content_submission_id.campaign_id`.
            3.  Provide admin UI (wizard likely) with assessment. If admin decides to delete/anonymize, call appropriate methods.
            4.  Log assessment and action.
    *   `apply_legal_hold(self, model_name, record_ids, hold_reason, applied_by_user_id)`: REQ-DRH-009.
        *   **Logic**:
            1.  For each `record_id` in `model_name`, set a `legal_hold_active = True` flag and `legal_hold_reason = hold_reason` (assuming these fields exist on relevant models or a central LegalHold model).
            2.  Log audit.
    *   `lift_legal_hold(self, model_name, record_ids, lifted_by_user_id)`: REQ-DRH-009.
        *   **Logic**: Set `legal_hold_active = False` for specified records. Log audit.

### 3.5. `wizards/`

#### 3.5.1. `wizards/__init__.py`
*   **Purpose**: Initializes `wizards` package.
*   **Logic**: Imports wizard model files.
    python
    # odoo_modules/influence_gen_services/wizards/__init__.py
    from . import data_retention_execution_wizard
    from . import legal_hold_management_wizard
    

#### 3.5.2. `wizards/data_retention_execution_wizard.py`
*   **Class**: `DataRetentionExecutionWizard`
*   **Inherits**: `models.TransientModel`
*   `_name`: `influence_gen.data_retention_execution_wizard`
*   `_description`: "Manual Data Retention Execution Wizard"
*   **Fields**:
    *   `data_category_filter`: `fields.Selection(related='influence_gen.data_retention_policy.data_category', string="Data Category to Process")` (Needs adjustment for wizard context)
    *   `model_name_filter`: `fields.Char(string="Target Model (Optional)")`
    *   `older_than_date_filter`: `fields.Date(string="Process Data Older Than")`
    *   `dry_run`: `fields.Boolean(string="Dry Run (Log actions only)", default=True)`
*   **Methods**:
    *   `action_execute_retention(self)`: REQ-DRH-002.
        *   **Logic**:
            1.  Call `DataManagementService.apply_data_retention_policies` with parameters from wizard fields.
            2.  Display summary of actions or log file location to user.
            3.  Return action to close wizard or show results.

#### 3.5.3. `wizards/legal_hold_management_wizard.py`
*   **Class**: `LegalHoldManagementWizard`
*   **Inherits**: `models.TransientModel`
*   `_name`: `influence_gen.legal_hold_management_wizard`
*   `_description`: "Legal Hold Management Wizard"
*   **Fields**:
    *   `target_model_selection`: `fields.Selection([...], string="Target Model", required=True)` (List of models that can be put on hold, e.g., `influence_gen.influencer_profile`, `influence_gen.campaign`)
    *   `target_record_ids_char`: `fields.Char(string="Record IDs (comma-separated)", required=True)`
    *   `hold_reason`: `fields.Text(string="Reason for Hold/Lift", required=True)`
    *   `action_type`: `fields.Selection([('apply', 'Apply Hold'), ('lift', 'Lift Hold')], string="Action", required=True)`
*   **Methods**:
    *   `action_process_legal_hold(self)`: REQ-DRH-009.
        *   **Logic**:
            1.  Parse `target_record_ids_char` into a list of integers.
            2.  If `self.action_type == 'apply'`, call `DataManagementService.apply_legal_hold(self.target_model_selection, record_ids, self.hold_reason, self.env.user.id)`.
            3.  If `self.action_type == 'lift'`, call `DataManagementService.lift_legal_hold(self.target_model_selection, record_ids, self.env.user.id)`.
            4.  Display success/failure message.

### 3.6. `security/`

#### 3.6.1. `security/ir.model.access.csv`
*   **Purpose**: Defines model-level access rights. REQ-PAC-001, REQ-PAC-002, REQ-AIGS-002.
*   **Content Examples**:
    csv
    id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
    access_influencer_profile_group_influencer,influence_gen.influencer_profile for group_influencer,model_influence_gen_influencer_profile,influence_gen_security.group_influence_gen_influencer,1,1,0,0
    access_influencer_profile_group_admin,influence_gen.influencer_profile for group_admin,model_influence_gen_influencer_profile,influence_gen_security.group_influence_gen_admin,1,1,1,1
    # ... (similar entries for all custom models and groups: influencer, admin, campaign_manager etc.)
    access_campaign_group_admin,influence_gen.campaign for group_admin,model_influence_gen_campaign,influence_gen_security.group_influence_gen_admin,1,1,1,1
    access_campaign_group_influencer,influence_gen.campaign for group_influencer,model_influence_gen_campaign,influence_gen_security.group_influence_gen_influencer,1,0,0,0
    access_ai_image_request_group_influencer,influence_gen.ai_image_generation_request for group_influencer,model_influence_gen_ai_image_generation_request,influence_gen_security.group_influence_gen_influencer,1,0,1,0 
    # (influencer can create and read own requests)
    access_audit_log_group_admin,influence_gen.audit_log_entry for group_admin,model_influence_gen_audit_log_entry,influence_gen_security.group_influence_gen_admin,1,0,0,0
    # ... and so on for all models defined
    
    **Note**: Assumes security groups like `group_influence_gen_influencer`, `group_influence_gen_admin` are defined in `influence_gen_security_groups.xml`.

#### 3.6.2. `security/influence_gen_security_groups.xml` (If not in a base/core InfluenceGen module)
*   **Purpose**: Defines Odoo security groups/roles. REQ-PAC-001.
*   **Content Example**:
    xml
    <odoo>
        <data noupdate="1">
            <record id="module_category_influence_gen" model="ir.module.category">
                <field name="name">InfluenceGen</field>
                <field name="description">User access levels for InfluenceGen Platform</field>
                <field name="sequence">25</field>
            </record>

            <record id="group_influence_gen_influencer" model="res.groups">
                <field name="name">Influencer</field>
                <field name="category_id" ref="module_category_influence_gen"/>
                <field name="implied_ids" eval="[(4, ref('base.group_portal'))]"/> 
            </record>

            <record id="group_influence_gen_campaign_manager" model="res.groups">
                <field name="name">Campaign Manager</field>
                <field name="category_id" ref="module_category_influence_gen"/>
                <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
            </record>

            <record id="group_influence_gen_admin" model="res.groups">
                <field name="name">Platform Administrator</field>
                <field name="category_id" ref="module_category_influence_gen"/>
                <field name="implied_ids" eval="[(4, ref('group_influence_gen_campaign_manager'))]"/>
                <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
            </record>
        </data>
    </odoo>
    

### 3.7. `data/`
*   XML files for initial/demo data.
    *   `area_of_influence_data.xml`: Pre-populate some common areas of influence.
    *   `platform_setting_data.xml`: Define default platform settings (e.g., default AI quota).
    *   `data_retention_policy_data.xml`: Define default retention policies.

### 3.8. `views/`
*   XML files defining Odoo views for backend administration of the models in this service layer, if not handled by a separate admin UI module.
    *   `influencer_profile_views.xml`, `campaign_views.xml`, `ai_image_model_views.xml`, `platform_setting_views.xml`, `data_retention_policy_views.xml`: Tree, Form, Search views.
    *   `menu_items.xml`: Menu items for accessing these admin views.

### 3.9. `wizards/*.xml` (View definitions for wizards)
*   `data_retention_execution_wizard_views.xml`
*   `legal_hold_management_wizard_views.xml`

### 3.10. `i18n/influence_gen_services.pot`
*   Standard Odoo POT file, generated by Odoo's tools. Will contain all translatable strings from Python code and XML views.

## 4. Key Business Logic Flows and Service Interactions

### 4.1. Influencer Onboarding
1.  **Registration**: `OnboardingService.process_registration_submission` creates `InfluencerProfile`, links to `res.users`, creates `SocialMediaProfile` stubs.
2.  **KYC Submission**: User uploads docs (UI Layer -> Infra Layer for file storage -> `OnboardingService.handle_kyc_document_submission`). Service creates `KYCData` record.
3.  **KYC Review**: Admin reviews (UI Layer -> `OnboardingService.handle_kyc_review_decision`). Service updates `KYCData` and `InfluencerProfile.kyc_status`.
4.  **Social Media Verification**:
    *   Influencer initiates (UI -> `OnboardingService.initiate_social_media_verification`). Service updates `SocialMediaProfile`, may generate code.
    *   Influencer provides proof / OAuth (UI -> `OnboardingService.confirm_social_media_verification`). Service updates `SocialMediaProfile`.
5.  **Bank Account Verification**: Similar flow to social media, using `OnboardingService` and `BankAccount` model methods.
6.  **ToS Consent**: Influencer agrees (UI -> `OnboardingService.record_terms_consent`).
7.  **Account Activation**: `OnboardingService.check_and_activate_influencer_account` (can be triggered after any key step completion) checks all prerequisites and calls `InfluencerProfile.action_activate_account`.

### 4.2. Campaign Workflow
1.  **Campaign Creation**: Admin creates (UI -> `CampaignService.create_campaign`).
2.  **Application**: Influencer applies (UI -> `CampaignService.process_campaign_application`).
3.  **Application Review**: Admin reviews (UI -> `CampaignService.review_campaign_application`).
4.  **Content Submission**: Influencer submits (UI -> Infra for files -> `CampaignService.handle_content_submission`).
5.  **Content Review**: Admin reviews (UI -> `CampaignService.review_content_submission`). (Implements `SEQ-CMP-005`).
6.  **Performance Metrics**: Admin/Influencer inputs (UI -> `CampaignService.record_campaign_performance_metrics`).

### 4.3. AI Image Generation
1.  **Request**: User requests (UI -> `AIImageService.prepare_ai_generation_request`). Service validates, checks quota, creates `AIImageGenerationRequest`, logs usage, triggers N8N via Infra Layer.
2.  **Callback**: N8N calls back Odoo (Infra Layer receives -> `AIImageService.process_ai_generation_callback`). Service creates `GeneratedImage`, updates request status, logs usage.

### 4.4. Payment Processing
1.  **Calculation**: System/Admin triggers (e.g., post-campaign, UI -> `PaymentService.calculate_owed_amounts_for_influencer`).
2.  **Batch Preparation**: Admin triggers (UI -> `PaymentService.generate_payment_batch_data`).
3.  **Vendor Bill Creation**: System/Admin triggers (UI/Batch -> `PaymentService.process_payment_batch_creation`). This calls Infra layer to interact with `account.move`.
4.  **Status Update**: Odoo Accounting process completes (hook/manual -> `PaymentService.update_payment_status_from_accounting`).

### 4.5. Data Management (Scheduled/Manual)
1.  **Retention Policy Execution**: Scheduled job or Admin Wizard -> `DataManagementService.apply_data_retention_policies`.
2.  **Legal Hold**: Admin Wizard -> `DataManagementService.apply_legal_hold` or `lift_legal_hold`.

## 5. Error Handling and Logging
*   **Error Handling**:
    *   Business rule violations within models should raise `odoo.exceptions.ValidationError`.
    *   Operational errors or user input errors in services that need to be shown to user should raise `odoo.exceptions.UserError`.
    *   Service methods should handle exceptions from model calls or other services gracefully.
*   **Logging**:
    *   All critical operations, state changes, and errors must be logged to the `influence_gen.audit_log_entry` model using the `AuditLogEntry.create_log()` method (REQ-ATEL-005, REQ-ATEL-006).
    *   Standard Odoo logging (`_logger`) should be used for operational/debug logging within Python code.

## 6. Dependencies on Other Repositories
*   **`REPO-IGOII-004` (InfluenceGen.Odoo.Infrastructure.Integration.Services)**:
    *   For sending email notifications.
    *   For initiating webhook calls to N8N.
    *   For handling file storage interactions (if abstracted beyond `ir.attachment`).
    *   For interacting with Odoo's `account.move` to create vendor bills.
    *   For making calls to any third-party KYC/Bank verification APIs (if logic is not fully in N8N).
*   **`REPO-IGEI-006` (N8N_Workflows_InfluenceGen)**: (Indirect dependency)
    *   This business service layer prepares data for N8N and processes results from N8N. The actual N8N workflows are in the external repository.

## 7. Configuration Parameters (Managed via `PlatformSetting` model)
*   `influence_gen.default_tos_version`: (String) Current default ToS version.
*   `influence_gen.default_privacy_policy_version`: (String) Current default Privacy Policy version.
*   `influence_gen.ai_image_default_quota_per_user_monthly`: (Integer) Default monthly AI image generation quota.
*   `influence_gen.ai_image_prompt_moderation_enabled`: (Boolean) Toggle for AI prompt moderation.
*   `influence_gen.ai_image_param_default_resolution`: (String) e.g., "1024x1024"
*   `influence_gen.ai_image_param_range_inference_steps`: (JSON String) e.g., `{"min": 10, "max": 50}`
*   (Other AI parameter defaults/ranges as needed)
*   `influence_gen.kyc_document_max_file_size_mb`: (Integer) Max file size for KYC docs.
*   `influence_gen.social_media_verification_code_expiry_hours`: (Integer)
*   `influence_gen.bank_micro_deposit_attempts_max`: (Integer)

## 8. Data Model Notes
*   Refer to the detailed Database Design document for specific field types, constraints, and indexes. This SDS focuses on the Odoo ORM representation and associated business logic.
*   Encryption of sensitive fields (e.g., `_encrypted` suffix) implies that the stored value is encrypted. The business logic layer methods will work with these encrypted values, assuming utilities or an underlying mechanism handles the actual crypto operations during input/output if raw values are needed (which should be minimized).

This SDS provides a comprehensive blueprint for the development of the `InfluenceGen.Odoo.Business.Services` module. Each model and service method needs to be implemented adhering to these specifications and the referenced requirements.