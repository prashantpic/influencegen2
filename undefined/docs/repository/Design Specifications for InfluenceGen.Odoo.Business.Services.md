# Software Design Specification: InfluenceGen.Odoo.Business.Services

## 1. Introduction

### 1.1 Purpose
This document outlines the software design for the `InfluenceGen.Odoo.Business.Services` repository. This repository forms the core backend business logic and service operations layer for the InfluenceGen platform, built as a suite of custom Odoo 18 modules. It is responsible for data modeling, business rule enforcement, workflow orchestration, and service provision for various platform functionalities including influencer onboarding, campaign management, AI image generation integration, and payment processing.

### 1.2 Scope
The scope of this SDS covers the design and implementation of all Odoo models, services, wizards, security configurations, and data initializations within the `influence_gen_services` Odoo module. This includes:
- Defining and managing Odoo data models for key entities (Influencer, Campaign, KYC, AI Requests, Payments, etc.).
- Implementing business logic for influencer onboarding, KYC, social media/bank account validation.
- Managing the full campaign lifecycle.
- Orchestrating AI image generation requests with N8N, including quota management.
- Calculating influencer payments and integrating with Odoo Accounting.
- Enforcing server-side data validation and business rules.
- Managing platform configurations and consent.
- Implementing audit logging and data retention policies.

### 1.3 Definitions, Acronyms, and Abbreviations
- **AI**: Artificial Intelligence
- **API**: Application Programming Interface
- **CRUD**: Create, Read, Update, Delete
- **ETL**: Extract, Transform, Load
- **FAQ**: Frequently Asked Questions
- **GDPR**: General Data Protection Regulation
- **GPU**: Graphics Processing Unit
- **HTTP**: Hypertext Transfer Protocol
- **IaC**: Infrastructure as Code
- **ID**: Identifier
- **IP**: Internet Protocol
- **JSON**: JavaScript Object Notation
- **KYC**: Know Your Customer
- **L1/L2/L3**: Level 1/2/3 Support
- **MDM**: Master Data Management
- **MFA**: Multi-Factor Authentication
- **ORM**: Object-Relational Mapper
- **OS**: Operating System
- **OWL**: Odoo Web Library
- **PII**: Personally Identifiable Information
- **PK**: Primary Key
- **FK**: Foreign Key
- **POT**: Portable Object Template
- **QWeb**: Odoo's primary templating engine
- **RBAC**: Role-Based Access Control
- **REQ**: Requirement
- **REST**: Representational State Transfer
- **SLA**: Service Level Agreement
- **SME**: Subject Matter Expert
- **SMTP**: Simple Mail Transfer Protocol
- **SQL**: Structured Query Language
- **SRS**: Software Requirements Specification
- **SUS**: System Usability Scale
- **ToS**: Terms of Service
- **UAT**: User Acceptance Testing
- **UI**: User Interface
- **URI**: Uniform Resource Identifier
- **URL**: Uniform Resource Locator
- **UTC**: Coordinated Universal Time
- **UUID**: Universally Unique Identifier
- **UX**: User Experience
- **VPC**: Virtual Private Cloud
- **VRAM**: Video Random Access Memory
- **WCAG**: Web Content Accessibility Guidelines
- **XML**: Extensible Markup Language

### 1.4 References
- InfluenceGen Software Requirements Specification (SRS)
- InfluenceGen Architecture Design Document
- Odoo 18 Developer Documentation
- Organizational Data Governance Policy Document
- Organizational Coding Standards and Development Guidelines
- Organizational Security Policies

### 1.5 Overview
This document is structured to provide a detailed design for each component of the `InfluenceGen.Odoo.Business.Services` repository. It starts with module initialization, followed by detailed specifications for Odoo models, service classes, wizards, security configurations, and data files. Each component specification will include its purpose, implemented features, dependencies, high-level logic, and relevant requirement mappings.

## 2. System Architecture
The `InfluenceGen.Odoo.Business.Services` repository adheres to a Layered Architecture and leverages Odoo's inherent Model-Template-View (MTV) pattern. It primarily constitutes the "Business Logic Layer" in the overall InfluenceGen system architecture.

**Key Architectural Patterns Utilized:**
- **Modular Design (Odoo Modules):** The entire functionality is encapsulated within the `influence_gen_services` Odoo module, promoting separation of concerns.
- **Repository Pattern (via Odoo ORM):** Odoo models act as repositories, abstracting database interactions.
- **Service Layer:** Dedicated service classes encapsulate complex business logic and orchestrate operations spanning multiple models.
- **Mixin Pattern:** Reusable functionalities like audit logging are implemented as mixins.
- **Configuration Management:** Platform settings are managed via dedicated models or Odoo's `ir.config_parameter`.
- **Audit Logging:** A dedicated model and mixin handle comprehensive audit trail generation.

## 3. Module Structure and Initialization

### 3.1 `__init__.py` (Module Root)
- **Purpose:** Initializes the `influence_gen_services` Odoo module.
- **Logic:**
  python
  # odoo_modules/influence_gen_services/__init__.py
  from . import models
  from . import services
  from . import wizards
  from . import security # Though security is primarily XML, models for groups/rules might be defined
  from . import data # Though data is primarily XML, Python hooks can be defined if needed
  
- **Requirements:** Module Initialization
- **Documentation:** Main initializer for the `influence_gen_services` Odoo module.

### 3.2 `__manifest__.py`
- **Purpose:** Declares the `influence_gen_services` module to Odoo, specifying its properties, dependencies, and data files.
- **Logic:**
  python
  # odoo_modules/influence_gen_services/__manifest__.py
  {
      'name': 'InfluenceGen Core Services',
      'version': '18.0.1.0.0',
      'summary': 'Core business logic, data models, and services for the InfluenceGen platform.',
      'author': 'SSS-AI',
      'website': 'https://www.example.com', # Replace with actual website
      'category': 'Services/InfluenceGen',
      'license': 'AGPL-3', # Or appropriate license
      'depends': [
          'base',
          'mail',       # For mail.thread, mail.activity.mixin, mail.template
          'account',    # For integration with accounting (vendor bills, payments)
          'iap',        # If any Odoo IAP services are planned for use (e.g., for 3rd party integrations)
          # Add REPO-IGIA-004 and REPO-IGSCU-007 as module dependencies if they are Odoo modules
          # For now, assuming they are not direct Odoo module dependencies but Python libraries/services
          # integrated at a different level or managed as separate applications.
          # If REPO-IGIA-004 is an Odoo module, it would be 'influence_gen_integration_adapter'
          # If REPO-IGSCU-007 is an Odoo module, it would be 'influence_gen_shared_utilities'
      ],
      'data': [
          # Security files
          'security/ir.model.access.csv',
          'security/influence_gen_security.xml',
          # Data files
          'data/platform_setting_data.xml',
          'data/mail_template_data.xml',
          'data/scheduled_actions_data.xml',
          # Wizard views (if any are defined directly in XML, otherwise wizard actions)
          # Model views (if any specific backend views are defined in this module, typically minimal for a service module)
      ],
      'installable': True,
      'application': False, # This is a backend services module, not a standalone application
      'auto_install': False,
      'description': """
  Core backend business logic and service operations for the InfluenceGen platform.
  This module includes:
  - Data models for Influencer Profiles, Campaigns, KYC, AI Image Generation, Payments.
  - Business rules for onboarding, campaign management, AI integration, and payments.
  - Service layer for orchestrating complex operations.
      """,
  }
  
- **Requirements:** Module Definition, Dependency Management, Data File Loading
- **Documentation:** Manifest file for the InfluenceGen Services module.

## 4. Data Models (`models/`)

### 4.1 `models/__init__.py`
- **Purpose:** Initializes the Python package for Odoo models.
- **Logic:**
  python
  # odoo_modules/influence_gen_services/models/__init__.py
  from . import base_audit_mixin
  from . import influencer_profile
  from . import area_of_influence
  from . import social_media_profile
  from . import kyc_data
  from . import bank_account
  from . import terms_consent
  from . import campaign
  from . import campaign_kpi
  from . import campaign_application
  from . import content_submission
  from . import content_feedback_log
  from . import ai_image_model
  from . import ai_image_generation_request
  from . import generated_image
  from . import payment_record
  from . import audit_log
  from . import usage_tracking_log
  from . import platform_setting
  
- **Requirements:** Model Discovery
- **Documentation:** Initializer for the data models of the InfluenceGen Services module.

### 4.2 `models/base_audit_mixin.py`
- **Purpose:** Provides a reusable mixin for automated audit logging of CRUD operations on Odoo models.
- **Class:** `BaseAuditMixin(models.AbstractModel)`
- **Fields:**
    - `_name = 'influence_gen.base_audit_mixin'`
    - `_description = 'Base Audit Mixin for InfluenceGen Models'`
- **Methods:**
    - `_log_audit_event(self, action, target_entity_name=None, target_id=None, details=None, outcome='success', reason=None)`:
        - **Logic:** Creates an `influence_gen.audit_log` record.
            - `timestamp`: `fields.Datetime.now()`
            - `user_id`: `self.env.user.id` if available, else `None` (for system actions).
            - `event_type`: Derived from `target_entity_name` and `action` (e.g., 'influencer_profile_create', 'campaign_update').
            - `target_model`: `target_entity_name` or `self._name`.
            - `target_res_id`: `target_id` or `record.id` for single record operations.
            - `action`: The CRUD action (e.g., 'create', 'write', 'unlink').
            - `details_json`: JSON string of `details` (e.g., old/new values for `write`).
            - `ip_address`: Get from request if available (e.g., `self.env.request.httprequest.remote_addr`).
            - `outcome`: 'success' or 'failure'.
        - **Parameters:**
            - `action (str)`: The action being logged (e.g., 'create', 'write', 'unlink').
            - `target_entity_name (str, optional)`: Name of the target model if different from `self._name`.
            - `target_id (int, optional)`: ID of the target record if different from `self.id`.
            - `details (dict, optional)`: Dictionary of relevant details (e.g., changed fields, old/new values).
            - `outcome (str)`: 'success' or 'failure'.
            - `reason (str, optional)`: Reason for failure.
    - `create(self, vals_list)`:
        - **Logic:** Calls `super().create(vals_list)`. For each created record, calls `_log_audit_event('create', details={'created_values': vals})`.
        - **Returns:** `recordset` of created records.
    - `write(self, vals)`:
        - **Logic:**
            - Capture old values for fields in `vals` if needed for detailed logging.
            - Calls `super().write(vals)`.
            - For each record in `self`, calls `_log_audit_event('write', details={'updated_values': vals, 'old_values': captured_old_values})`. (Note: Capturing old values accurately can be complex and might require careful implementation, possibly by reading before super call).
        - **Returns:** `bool`
    - `unlink(self)`:
        - **Logic:** For each record in `self`, capture identifying information (e.g., `{'unlinked_record_name': record.display_name or str(record.id)}`). Calls `_log_audit_event('unlink', details=captured_info)`. Then calls `super().unlink()`.
        - **Returns:** `bool`
- **Requirements:** REQ-ATEL-005, REQ-ATEL-006
- **Documentation:** Provides base audit logging functionality for key Odoo models.

---
*(Detailed specifications for each model: `influencer_profile.py`, `area_of_influence.py`, `social_media_profile.py`, `kyc_data.py`, `bank_account.py`, `terms_consent.py`, `campaign.py`, `campaign_kpi.py`, `campaign_application.py`, `content_submission.py`, `content_feedback_log.py`, `ai_image_model.py`, `ai_image_generation_request.py`, `generated_image.py`, `payment_record.py`, `audit_log.py`, `usage_tracking_log.py`, `platform_setting.py` will follow. Each will detail fields, SQL constraints, Python constraints, methods with logic descriptions, and links to requirements. Below is an example for one model, the rest will follow a similar structure.)*
---

### 4.3 `models/influencer_profile.py`
- **Purpose:** Defines the data structure and business logic for influencer profiles.
- **Class:** `InfluencerProfile(models.Model)`
- **Inherits:** `['mail.thread', 'mail.activity.mixin', 'influence_gen.base_audit_mixin']`
- **Fields:**
    - `_name = 'influence_gen.influencer_profile'`
    - `_description = 'Influencer Profile'`
    - `user_id = fields.Many2one('res.users', string='Odoo User', required=True, ondelete='cascade', index=True, copy=False, help="System user associated with this influencer profile.")`
    - `full_name = fields.Char(string='Full Name', required=True, tracking=True)`
    - `email = fields.Char(string='Email Address', required=True, tracking=True, help="Primary email for communication and login.")`
    - `phone = fields.Char(string='Phone Number', tracking=True)`
    - `residential_address = fields.Text(string='Residential Address', tracking=True)`
    - `social_media_profile_ids = fields.One2many('influence_gen.social_media_profile', 'influencer_profile_id', string='Social Media Profiles')`
    - `area_of_influence_ids = fields.Many2many('influence_gen.area_of_influence', 'influencer_area_of_influence_rel', 'influencer_id', 'area_id', string='Areas of Influence')`
    - `audience_demographics = fields.Text(string='Audience Demographics (JSON)', help="Self-declared audience demographics, stored as JSON.")` # Consider fields.Json if Odoo 18 fully supports it with good UX.
    - `kyc_status = fields.Selection([('pending', 'Pending Submission'), ('submitted', 'Submitted, Awaiting Review'), ('in_review', 'In Review'), ('requires_more_info', 'Requires More Info'), ('approved', 'Approved'), ('rejected', 'Rejected')], string='KYC Status', default='pending', required=True, tracking=True, index=True)`
    - `kyc_data_ids = fields.One2many('influence_gen.kyc_data', 'influencer_profile_id', string='KYC Submissions')`
    - `bank_account_ids = fields.One2many('influence_gen.bank_account', 'influencer_profile_id', string='Bank Accounts')`
    - `terms_consent_ids = fields.One2many('influence_gen.terms_consent', 'influencer_profile_id', string='Terms Consents')`
    - `account_status = fields.Selection([('pending_verification', 'Pending Verification'), ('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended')], string='Account Status', default='pending_verification', required=True, tracking=True, index=True)`
    - `activation_date = fields.Datetime(string='Activation Date', readonly=True, tracking=True)`
    - `is_gdpr_erasure_requested = fields.Boolean(string='GDPR Erasure Requested', default=False, tracking=True)`
    - `legal_hold_status = fields.Boolean(string='Legal Hold Active', default=False, tracking=True, help="Indicates if this profile is under a legal hold, preventing deletion.")`
    - `company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)` # Standard Odoo field
- **SQL Constraints:**
    - `('email_unique', 'UNIQUE(email)', 'The email address must be unique across all influencers.')`
    - `('user_id_unique', 'UNIQUE(user_id)', 'An Odoo user can only be linked to one influencer profile.')`
- **Methods:**
    - `action_activate_account(self)`:
        - **Logic:** Sets `account_status` to 'active' and `activation_date` to `fields.Datetime.now()`. Ensures all onboarding prerequisites (KYC approved, primary bank account verified, terms consented) are met. Logs event. Sends notification.
        - **Requirements:** REQ-IOKYC-012
    - `action_deactivate_account(self)`:
        - **Logic:** Sets `account_status` to 'inactive'. Logs event.
    - `action_suspend_account(self)`:
        - **Logic:** Sets `account_status` to 'suspended'. Logs event.
    - `action_request_data_erasure(self)`:
        - **Logic:** Sets `is_gdpr_erasure_requested` to `True`. Triggers a notification/activity for an administrator to review the request (handled by `RetentionAndLegalHoldService`). Logs event.
        - **Requirements:** REQ-DMG-021
    - `get_latest_consent(self)`:
        - **Logic:** Searches `terms_consent_ids` and returns the latest record based on `consent_date`.
        - **Returns:** `recordset` of `influence_gen.terms_consent` (or empty).
        - **Requirements:** REQ-IOKYC-009
    - `update_kyc_status(self, new_status, reviewer_id=None, notes=None)`:
        - **Logic:** Updates `kyc_status`. If `new_status` is 'approved' and other conditions are met (bank account, terms), may trigger `check_and_activate_influencer_account()`. Sends notification.
        - **Internal call, typically from `KycData` model or `OnboardingService`.**
    - `check_onboarding_completion(self)`:
        - **Logic:** Checks if KYC is approved, at least one bank account is verified and primary, and latest ToS/PP are consented.
        - **Returns:** `bool`
        - **Requirements:** REQ-IOKYC-012
    - `name_get(self)`:
        - **Logic:** Override to return `full_name` or `email` as display name.
- **Requirements Met Directly:** REQ-DMG-002, REQ-IOKYC-002 (data fields), REQ-IOKYC-009 (consent linking), REQ-IOKYC-012 (activation), REQ-IOKYC-014 (data validation implicitly via field types/constraints), REQ-IOKYC-016 (audit via mixin), REQ-DMG-020 (fields for retention), REQ-DMG-021 (GDPR fields).
- **Documentation:** Represents an influencer on the platform.

---
*(Specifications for `area_of_influence.py`, `social_media_profile.py`, etc. will continue in this detailed format.)*
---

### 4.4 `models/audit_log.py`
- **Purpose:** To provide a dedicated, tamper-evident store for all significant system events and user actions.
- **Class:** `AuditLog(models.Model)`
- **Fields:**
    - `_name = 'influence_gen.audit_log'`
    - `_description = 'InfluenceGen Audit Log'`
    - `_order = 'timestamp desc'`
    - `timestamp = fields.Datetime(string='Timestamp (UTC)', required=True, default=fields.Datetime.now, readonly=True, index=True)`
    - `user_id = fields.Many2one('res.users', string='User/Actor', readonly=True, ondelete='set null', index=True, help="User who performed the action, or system if None.")`
    - `event_type = fields.Char(string='Event Type', required=True, readonly=True, index=True, help="Categorization of the event, e.g., 'user.login', 'kyc.status.change'.")`
    - `target_model = fields.Char(string='Target Model', readonly=True, index=True, help="Model name of the affected entity, e.g., 'influence_gen.campaign'.")`
    - `target_res_id = fields.Integer(string='Target Record ID', readonly=True, index=True, help="ID of the affected record in target_model.")` # Use Integer, as Odoo's res_id is typically integer. Could be Char for flexibility if UUIDs are used extensively for res_id elsewhere.
    - `action = fields.Char(string='Action Performed', required=True, readonly=True, help="e.g., 'create', 'write', 'unlink', 'approve', 'login_success', 'login_failure'.")`
    - `details_json = fields.Text(string='Details (JSON)', readonly=True, help="JSON string containing event-specific details, like changed values.")`
    - `ip_address = fields.Char(string='Source IP Address', readonly=True)`
    - `outcome = fields.Selection([('success', 'Success'), ('failure', 'Failure')], string='Outcome', required=True, readonly=True, default='success')`
    - `failure_reason = fields.Text(string='Failure Reason', readonly=True, help="Reason if the outcome was a failure.")`
    - `legal_hold_status = fields.Boolean(string='Under Legal Hold', default=False, copy=False, help="Indicates if this log entry itself is under a specific legal hold (rare, but for completeness).")`
    - `correlation_id = fields.Char(string='Correlation ID', readonly=True, index=True, help="ID to trace requests across multiple components.")`
- **Methods:** None (Data primarily created by `BaseAuditMixin` or services).
- **Security:** Access to this model should be highly restricted (e.g., only to specific Audit Administrator roles). No `perm_write` or `perm_unlink` for typical admin users to ensure tamper-evidence.
- **Requirements Met Directly:** REQ-ATEL-005, REQ-ATEL-006, REQ-ATEL-007, REQ-IOKYC-016, REQ-2-018, REQ-AIGS-012, REQ-IPF-009.
- **Documentation:** Stores detailed records of auditable events.

### 4.5 `models/platform_setting.py`
- **Purpose:** To provide a flexible key-value store for platform-wide settings and business rule parameters.
- **Class:** `PlatformSetting(models.Model)`
- **Inherits:** `['influence_gen.base_audit_mixin']`
- **Fields:**
    - `_name = 'influence_gen.platform_setting'`
    - `_description = 'Platform Configuration Setting'`
    - `key = fields.Char(string='Setting Key', required=True, index=True, copy=False, help="Unique identifier for the setting, e.g., 'kyc.default_document_types'.")`
    - `value_char = fields.Char(string='Character Value')`
    - `value_text = fields.Text(string='Text Value')`
    - `value_int = fields.Integer(string='Integer Value')`
    - `value_float = fields.Float(string='Float Value')`
    - `value_bool = fields.Boolean(string='Boolean Value')`
    - `value_json = fields.Text(string='JSON Value')`
    - `value_type = fields.Selection([
        ('char', 'Character'),
        ('text', 'Text'),
        ('int', 'Integer'),
        ('float', 'Float'),
        ('bool', 'Boolean'),
        ('json', 'JSON')
      ], string='Value Type', required=True, default='char')`
    - `description = fields.Text(string='Description', help="Explanation of the setting and its purpose.")`
    - `module = fields.Char(string='Module', help="Module this setting primarily belongs to, for organization.")`
- **SQL Constraints:**
    - `('key_unique', 'UNIQUE(key)', 'The setting key must be unique.')`
- **Methods:**
    - `get_setting(cls, key_name, default=None)`: `@api.model`
        - **Logic:** Finds a setting by `key_name`. Returns its appropriately typed value. If not found, returns `default`.
        - **Returns:** Actual value (str, int, float, bool, dict/list from JSON) or `default`.
    - `set_setting(cls, key_name, value, value_type=None, description=None, module=None)`: `@api.model`
        - **Logic:** Creates or updates a setting. Determines `value_type` if not provided. Stores `value` in the corresponding `value_*` field.
        - **Returns:** `recordset` of the `platform.setting`.
    - `_get_typed_value(self)`: `compute` field or helper method
        - **Logic:** Returns the value from the correct `value_*` field based on `value_type`.
        - **Example:**
          python
          # Not a stored field, but a helper or can be a compute field
          def get_typed_value(self):
              self.ensure_one()
              if self.value_type == 'char': return self.value_char
              if self.value_type == 'text': return self.value_text
              # ... and so on for other types
              if self.value_type == 'json':
                  try:
                      return json.loads(self.value_json) if self.value_json else None
                  except json.JSONDecodeError:
                      return None # Or raise error
              return None
          
- **Requirements Met Directly:** REQ-IOKYC-017 (provides mechanism for KYC settings), general configuration needs.
- **Documentation:** Stores configurable key-value settings.

## 5. Services (`services/`)

### 5.1 `services/__init__.py`
- **Purpose:** Initializes the Python package for service layer classes.
- **Logic:**
  python
  # odoo_modules/influence_gen_services/services/__init__.py
  from . import onboarding_service
  from . import campaign_management_service
  from . import payment_processing_service
  from . import ai_integration_service
  from . import data_management_service
  from . import retention_and_legal_hold_service
  # Potentially an audit_trail_service if BaseAuditMixin is not sufficient for all cases
  
- **Requirements:** Service Discovery
- **Documentation:** Initializer for the service layer.

---
*(Detailed specifications for each service: `onboarding_service.py`, `campaign_management_service.py`, `payment_processing_service.py`, `ai_integration_service.py`, `data_management_service.py`, `retention_and_legal_hold_service.py` will follow. Each will detail its purpose, methods with parameters, return types, high-level logic, and links to requirements. Below is an example for one service.)*
---

### 5.2 `services/onboarding_service.py`
- **Purpose:** To manage the end-to-end workflow of influencer onboarding.
- **Class:** `OnboardingService(object)` (Not an Odoo `models.Model` or `models.TransientModel`, but a plain Python class instantiated with `env`).
- **Constructor:** `__init__(self, env)`: Stores `self.env = env`.
- **Methods:**
    - `process_registration_submission(self, influencer_vals)`:
        - **Logic:**
            1. Validates `influencer_vals` (email uniqueness, required fields).
            2. Creates `res.users` record (if not exists for email, or based on policy).
            3. Creates `influence_gen.influencer_profile` record linked to user, with initial status 'pending_verification'.
            4. Creates `influence_gen.terms_consent` if ToS/PP consent provided in `influencer_vals`.
            5. Logs audit event.
            6. Sends registration confirmation email (REQ-16-001).
        - **Returns:** `recordset` of the created `influence_gen.influencer_profile`.
        - **Requirements:** REQ-IOKYC-002
    - `submit_kyc_documents(self, influencer_id, document_data_list)`:
        - **Logic:** For each document in `document_data_list`:
            1. Creates `ir.attachment` for document files (front/back). (Handled by REPO-IGIA-004 for secure storage if complex)
            2. Creates `influence_gen.kyc_data` record linked to `influencer_id` and attachments. Sets status to 'submitted'.
            3. Updates influencer profile `kyc_status` to 'submitted' or 'in_review'.
            4. Logs audit event.
            5. Sends KYC submission received notification (REQ-16-002).
        - **Returns:** `bool` (success/failure)
        - **Requirements:** REQ-IOKYC-004 (data part), REQ-IOKYC-005 (triggers review)
    - `handle_kyc_review_decision(self, kyc_data_id, decision, reviewer_user_id, notes=None, required_info=None)`:
        - **Logic:**
            1. Finds `influence_gen.kyc_data` record.
            2. Updates its status, `reviewer_user_id`, `reviewed_at`, `notes`.
            3. If 'rejected', logs reason. If 'requires_more_info', logs `required_info`.
            4. Updates the main `influencer_profile_id.kyc_status` based on this decision and potentially other KYC items.
            5. If 'approved', calls `check_and_activate_influencer_account(influencer_id)`.
            6. Sends KYC status update notification (REQ-16-002).
            7. Logs audit event.
        - **Requirements:** REQ-IOKYC-005, REQ-IOKYC-011
    - `verify_social_media_account(self, social_profile_id, method, verification_input=None)`:
        - **Logic:**
            1. Finds `influence_gen.social_media_profile`.
            2. Implements logic for chosen `method` (e.g., 'oauth' might involve calling REPO-IGIA-004, 'code_in_bio' might involve an API call to check profile).
            3. Updates `verification_status`, `verified_at` on the `SocialMediaProfile` record.
            4. Logs audit event.
            5. Calls `check_and_activate_influencer_account(influencer_id)`.
        - **Returns:** `bool`
        - **Requirements:** REQ-IOKYC-006
    - `verify_bank_account(self, bank_account_id, method, verification_input=None)`:
        - **Logic:** Similar to social media verification. For 'micro_deposit', initiates process. For 'third_party_api', calls REPO-IGIA-004.
        - Updates `verification_status` on `BankAccount`.
        - Logs audit event.
        - Calls `check_and_activate_influencer_account(influencer_id)`.
        - **Returns:** `bool`
        - **Requirements:** REQ-IPF-002, REQ-IOKYC-008
    - `process_terms_consent(self, influencer_id, tos_version, privacy_policy_version)`:
        - **Logic:** Creates `influence_gen.terms_consent` record. Logs audit event. Calls `check_and_activate_influencer_account(influencer_id)`.
        - **Requirements:** REQ-IOKYC-009
    - `check_and_activate_influencer_account(self, influencer_id)`:
        - **Logic:**
            1. Fetches `InfluencerProfile`.
            2. Calls `influencer_profile.check_onboarding_completion()`.
            3. If complete and account is not 'active', calls `influencer_profile.action_activate_account()`.
            4. Sends account activation notification (REQ-16-003).
        - **Returns:** `bool` (if activated)
        - **Requirements:** REQ-IOKYC-012
- **Documentation:** Orchestrates influencer onboarding.

### 5.3 `services/campaign_management_service.py`
- **Purpose:** To orchestrate complex campaign-related operations.
- **Class:** `CampaignManagementService(object)`
- **Constructor:** `__init__(self, env)`
- **Methods:**
    - `create_campaign(self, campaign_vals)`: (REQ-2-001, REQ-2-002, REQ-2-003)
        - Logic: Validates vals. Creates `Campaign` record and associated `CampaignKpi` records. Logs.
        - Returns: `recordset` of `Campaign`.
    - `update_campaign_status(self, campaign_id, new_status)`: (REQ-2-017)
        - Logic: Finds `Campaign`. Validates `new_status` transition. Updates status. Logs. Sends relevant notifications (e.g., campaign published).
    - `review_campaign_application(self, application_id, decision, reviewer_user_id, reason=None)`: (REQ-2-007)
        - Logic: Finds `CampaignApplication`. Updates status, reviewer, reason. Logs. Sends notifications (REQ-16-004).
    - `review_content_submission(self, submission_id, decision, reviewer_user_id, feedback=None)`: (REQ-2-010)
        - Logic: Finds `ContentSubmission`. Updates status, reviewer. Creates `ContentFeedbackLog` entry. Logs. Sends notifications (REQ-16-005). If approved, may trigger payment record creation via `PaymentProcessingService`.
    - `record_campaign_performance(self, submission_id_or_campaign_id, metrics_data)`: (REQ-2-011)
        - Logic: Updates `performance_data_json` on `ContentSubmission` or aggregates on `Campaign.actualPerformanceMetrics`. Updates related `CampaignKpi.actual_value`. Logs.
    - `get_campaign_performance_summary(self, campaign_id)`: (REQ-2-012)
        - Logic: Aggregates KPIs and performance data for a campaign.
        - Returns: `dict` summary.
    - `get_influencer_performance_summary(self, influencer_id, campaign_id=None)`: (REQ-2-012)
        - Logic: Aggregates performance for an influencer across one or all campaigns.
        - Returns: `dict` summary.
- **Documentation:** Manages campaign lifecycle.

### 5.4 `services/payment_processing_service.py`
- **Purpose:** To manage influencer compensation.
- **Class:** `PaymentProcessingService(object)`
- **Constructor:** `__init__(self, env)`
- **Methods:**
    - `calculate_amounts_owed(self, campaign_id=None, influencer_id=None, for_date=None)`: (REQ-IPF-004, REQ-2-013)
        - Logic: Calculates owed amounts based on approved content submissions, campaign compensation models, and performance (if commission-based).
        - Returns: `list` of `dicts` with `{'influencer_id': X, 'amount': Y, 'currency_id': Z, 'reason': '...'}`.
    - `create_payment_records_for_approved_content(self, content_submission_ids)`: (REQ-IPF-004)
        - Logic: For each approved `ContentSubmission`, creates a `PaymentRecord` if one doesn't already exist for that submission and compensation criteria are met.
        - Returns: `recordset` of created `PaymentRecord`.
    - `generate_payment_batch_for_review(self, payment_record_ids)`: (REQ-IPF-005)
        - Logic: Groups specified `PaymentRecord`s (e.g., those in 'pending_approval' status) into a batch for administrative review before processing. Does not process yet.
        - Returns: `dict` representing the batch summary (total amount, count, etc.).
    - `process_payment_batch_with_odoo_accounting(self, payment_record_ids_to_process)`: (REQ-IPF-006, REQ-2-014)
        - Logic: For each `PaymentRecord` in `payment_record_ids_to_process` (assumed approved):
            1. Finds or creates a vendor (`res.partner`) for the influencer.
            2. Creates an Odoo Vendor Bill (`account.move` of type `in_invoice`) with appropriate lines.
            3. Updates `PaymentRecord.odoo_vendor_bill_id` and status to 'processing_bill'.
            4. Logs audit event.
        - Returns: `dict` with `{'success_count': X, 'failure_count': Y, 'failed_ids': [...]}`.
    - `update_payment_status_from_accounting(self, vendor_bill_id, new_accounting_status)`: (REQ-IPF-006, REQ-2-015)
        - Logic: Called by Odoo accounting automation/hook when a vendor bill's payment status changes. Finds related `PaymentRecord` and updates its status (e.g., to 'paid', 'payment_failed'). Logs. Sends notification to influencer.
    - `handle_payment_failure(self, payment_record_id, failure_reason)`: (REQ-IPF-010)
        - Logic: Updates `PaymentRecord` status to 'failed'. Logs. Triggers alert to finance/admin team.
- **Documentation:** Handles influencer payments.

### 5.5 `services/ai_integration_service.py`
- **Purpose:** To orchestrate AI image generation.
- **Class:** `AiIntegrationService(object)`
- **Constructor:** `__init__(self, env)`
- **Methods:**
    - `initiate_ai_image_generation(self, user_id, influencer_profile_id, prompt_data, generation_params, campaign_id=None, intended_use='personal')`: (REQ-AIGS-001, REQ-AIGS-004)
        - Logic:
            1. Calls `validate_ai_prompt(prompt_data['prompt'])`. If invalid, returns error.
            2. Calls `check_user_ai_quota(influencer_profile_id)`. If quota exceeded, returns error.
            3. Creates `AiImageGenerationRequest` record with status 'queued'.
            4. Calls REPO-IGIA-004 (e.g., `N8nIntegrationAdapter.trigger_ai_generation_workflow(request_id, payload)`).
            5. Updates request status to 'processing_n8n'. Logs.
        - Returns: `recordset` of `AiImageGenerationRequest`.
    - `handle_n8n_image_result_callback(self, request_id, image_results_list, n8n_execution_id)`: (REQ-AIGS-001, REQ-AIGS-006, REQ-AIGS-010)
        - Logic: Finds `AiImageGenerationRequest`. For each image in `image_results_list`:
            1. Handles image data (direct or download from link via REPO-IGIA-004).
            2. Creates `ir.attachment` and `GeneratedImage` record, linking to request.
            3. Calculates hash. Sets retention category based on `request.intended_use` and `request.campaign_id.usage_rights`.
            4. Updates request status to 'completed'.
            5. Calls `decrement_user_ai_quota`. Calls `log_ai_usage`. Logs.
    - `handle_n8n_image_error_callback(self, request_id, error_message, n8n_execution_id)`: (REQ-AIGS-001)
        - Logic: Finds `AiImageGenerationRequest`. Updates status to 'failed', stores `error_message`. Logs. Sends failure notification.
    - `check_user_ai_quota(self, influencer_profile_id)`: (REQ-AIGS-002)
        - Logic: Reads quota settings (from `PlatformSetting` or user/role config) and current usage (from `UsageTrackingLog`) for the influencer.
        - Returns: `bool` (true if quota available).
    - `decrement_user_ai_quota(self, influencer_profile_id, images_generated=1)`: (REQ-AIGS-002)
        - Logic: Updates usage count (not directly stored, but affects subsequent `check_user_ai_quota` calls by logging usage).
    - `log_ai_usage(self, request_id, images_generated, api_calls_to_ai_service)`: (REQ-AIGS-007)
        - Logic: Creates `UsageTrackingLog` record for the AI generation event.
    - `validate_ai_prompt(self, prompt_text)`: (REQ-AIGS-003)
        - Logic: Applies content moderation rules (denylist from `PlatformSetting`, or calls external moderation API via REPO-IGIA-004).
        - Returns: `(is_valid: bool, reason: str or None)`
- **Documentation:** Manages AI image generation pipeline.

### 5.6 `services/data_management_service.py`
- **Purpose:** Handles data quality, cleansing, anonymization, and MDM.
- **Class:** `DataManagementService(object)`
- **Constructor:** `__init__(self, env)`
- **Methods:**
    - `identify_data_quality_issues(self, model_name, domain=None, rules_key_prefix='data_quality.')`: (REQ-DMG-017, REQ-DMG-018)
        - Logic: Iterates through records of `model_name`. Applies data quality rules (fetched from `PlatformSetting` using `rules_key_prefix`) to identify issues (e.g., missing required fields not caught by DB, inconsistent formats).
        - Returns: `list` of `dicts` describing issues.
    - `cleanse_influencer_data(self, influencer_ids, rules_to_apply)`: (REQ-DMG-017)
        - Logic: Applies specific cleansing rules (e.g., formatting phone numbers, standardizing addresses) to given `InfluencerProfile` records. Logs changes.
    - `generate_anonymized_dataset_for_staging(self, models_to_anonymize_config)`: (REQ-DMG-022)
        - **Logic:** For each model in `models_to_anonymize_config` (which specifies fields and anonymization techniques like masking, randomization, generalization):
            1. Reads data.
            2. Applies anonymization transformations.
            3. Prepares data for export or direct load into a staging DB (outside Odoo transaction scope typically).
        - **Returns:** Path to anonymized data files or status message.
        - **Note:** This is a complex task. Might involve Odoo's `odoo.tools.sql.SQLCursor` for direct DB manipulation for performance if done within Odoo, or external ETL tools.
    - `apply_mdm_rules_influencer(self, influencer_ids=None, auto_merge_threshold=0.85)`: (REQ-DMG-012)
        - Logic: Implements influencer deduplication logic based on defined MDM strategy (e.g., fuzzy matching on name/email). Flags potential duplicates or attempts auto-merge if confidence is high. Logs actions.
- **Documentation:** Provides data management services.

### 5.7 `services/retention_and_legal_hold_service.py`
- **Purpose:** Manages data lifecycle according to retention policies and legal holds.
- **Class:** `RetentionAndLegalHoldService(object)`
- **Constructor:** `__init__(self, env)`
- **Methods:**
    - `get_retention_policy(self, data_category_key)`: (REQ-DRH-001)
        - Logic: Fetches retention period and disposition action (delete, anonymize, archive) from `PlatformSetting` for `data_category_key`.
        - Returns: `dict` like `{'period_days': 365, 'action': 'anonymize'}`.
    - `apply_retention_policies_automated(self)`: (REQ-DRH-002, REQ-DRH-006, REQ-ATEL-007)
        - **Logic:** **CRON JOB METHOD.** Iterates through configured data categories:
            1. Gets policy via `get_retention_policy()`.
            2. Finds records older than `period_days` that are NOT under `legal_hold_status = True`.
            3. Performs disposition action:
                - 'delete': `record.unlink()`.
                - 'anonymize': Calls a model-specific anonymization method (e.g., `influencer_profile.anonymize()`).
                - 'archive': Calls `archive_data_batch()` or flags for archival.
            4. Logs disposition actions.
    - `process_manual_erasure_request(self, model_name, record_id, requestor_user_id, justification_text)`: (REQ-DRH-003, REQ-DRH-004)
        - Logic:
            1. Finds record. Checks `legal_hold_status`. Checks against financial record keeping rules, campaign usage rights (if applicable).
            2. If clear for erasure, performs deletion or anonymization.
            3. Logs the request, assessment, decision, and action taken in `AuditLog` and potentially a dedicated GDPR request log model.
        - Returns: `bool` (success/failure).
    - `archive_data_batch(self, model_name, domain, archive_target_info)`: (REQ-DRH-007)
        - Logic: Exports data matching `domain` from `model_name` to a secure archival storage solution (details in `archive_target_info`). Marks records as archived. Logs.
    - `place_legal_hold(self, model_name, record_id_or_domain, hold_reason, placed_by_user_id)`: (REQ-DRH-008, REQ-DRH-009)
        - Logic: Finds records. Sets `legal_hold_status = True` on them. Logs in `AuditLog` with `hold_reason`.
        - Returns: `bool`.
    - `lift_legal_hold(self, model_name, record_id_or_domain, lifted_by_user_id, lift_reason)`: (REQ-DRH-008, REQ-DRH-009)
        - Logic: Finds records. Sets `legal_hold_status = False`. Logs in `AuditLog` with `lift_reason`.
        - Returns: `bool`.
    - `check_legal_hold(self, model_name, record_id)`: (REQ-DRH-009)
        - Logic: Checks `legal_hold_status` of the record.
        - Returns: `bool`.
- **Documentation:** Manages data retention, archival, and legal holds.


## 6. Wizards (`wizards/`)

### 6.1 `wizards/__init__.py`
- **Purpose:** Initializes the Python package for wizard models.
- **Logic:**
  python
  # odoo_modules/influence_gen_services/wizards/__init__.py
  from . import kyc_manual_review_wizard
  # Add other wizards if any, e.g., campaign_bulk_action_wizard
  
- **Requirements:** Wizard Discovery
- **Documentation:** Initializer for wizard components.

### 6.2 `wizards/kyc_manual_review_wizard.py`
- **Purpose:** To provide a UI for administrators during manual KYC review.
- **Class:** `KycManualReviewWizard(models.TransientModel)`
- **Fields:**
    - `_name = 'influence_gen.kyc_manual_review_wizard'`
    - `_description = 'KYC Manual Review Wizard'`
    - `kyc_data_id = fields.Many2one('influence_gen.kyc_data', string='KYC Submission', required=True, readonly=True)`
    - `decision = fields.Selection([('approved', 'Approve'), ('rejected', 'Reject'), ('requires_more_info', 'Request More Information')], string='Decision', required=True)`
    - `rejection_reason_text = fields.Text(string='Rejection Reason', help="Required if decision is 'Reject'.")`
    - `required_info_text = fields.Text(string='Information Required', help="Required if decision is 'Request More Information'.")`
    - `reviewer_notes = fields.Text(string='Internal Reviewer Notes')`
- **Methods:**
    - `action_confirm_review(self)`:
        - **Logic:**
            1. Gets `reviewer_user_id = self.env.user.id`.
            2. Calls `self.env['influence_gen.services.onboarding'].handle_kyc_review_decision(self.kyc_data_id.id, self.decision, reviewer_user_id, notes=self.reviewer_notes, required_info=self.required_info_text if self.decision == 'requires_more_info' else self.rejection_reason_text if self.decision == 'rejected' else None)`.
            3. Returns an action to close the wizard or refresh the view.
        - **Returns:** `dict` (Odoo action).
- **XML View:** An associated XML view (`kyc_manual_review_wizard_view.xml` - typically placed in a `views/` directory and listed in manifest) will define the form layout for this wizard.
- **Requirements:** REQ-IOKYC-011
- **Documentation:** Wizard for manual KYC review.

## 7. Security (`security/`)

### 7.1 `security/ir.model.access.csv`
- **Purpose:** Defines model-level CRUD access rights for user groups.
- **Format:** Standard Odoo CSV format.
- **Content (Examples):**
  csv
  id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
  access_influencer_profile_user,influence_gen.influencer_profile user,model_influence_gen_influencer_profile,base.group_user,1,1,1,0 
  # Influencers can RWC their own profile (record rules needed for 'own') but not delete.
  access_influencer_profile_admin,influence_gen.influencer_profile admin,model_influence_gen_influencer_profile,influence_gen_services.group_influence_gen_admin,1,1,1,1
  access_campaign_user,influence_gen.campaign user,model_influence_gen_campaign,base.group_user,1,0,0,0 
  # Influencers can read campaigns.
  access_campaign_admin,influence_gen.campaign admin,model_influence_gen_campaign,influence_gen_services.group_influence_gen_admin,1,1,1,1
  access_audit_log_admin,influence_gen.audit_log admin,model_influence_gen_audit_log,influence_gen_services.group_influence_gen_admin,1,0,0,0 
  # Admins can read audit logs, but not create/write/delete directly.
  # ... (Define for all custom models and relevant groups)
  
- **Requirements:** Implicitly supports all REQs by ensuring data is accessible/modifiable only by authorized roles.
- **Documentation:** Model access control lists.

### 7.2 `security/influence_gen_security.xml`
- **Purpose:** Defines custom security groups (roles) and record-level access rules.
- **Format:** Odoo XML.
- **Content (Examples):**
  xml
  <odoo>
      <data noupdate="1"> <!-- noupdate="1" for groups to prevent overwrite on update if manually changed -->
          <record id="group_influence_gen_admin" model="res.groups">
              <field name="name">InfluenceGen / Platform Administrator</field>
              <field name="category_id" ref="base.module_category_services_project"/> <!-- Or a custom category -->
              <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
              <!-- Add users to this group to grant admin rights -->
          </record>

          <record id="group_influence_gen_influencer" model="res.groups">
              <field name="name">InfluenceGen / Influencer</field>
              <field name="category_id" ref="base.module_category_services_project"/>
              <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
              <!-- Portal users are typically added to base.group_portal, and also this group -->
          </record>

          <!-- Example Record Rule: Influencer can only see/edit their own profile -->
          <record id="influencer_profile_self_rule" model="ir.rule">
              <field name="name">Influencer Profile: Own Records Only</field>
              <field name="model_id" ref="model_influence_gen_influencer_profile"/>
              <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
              <field name="perm_read" eval="True"/>
              <field name="perm_write" eval="True"/>
              <field name="perm_create" eval="True"/> <!-- Usually they create their own profile via portal -->
              <field name="perm_unlink" eval="False"/> <!-- Prevent self-deletion by default -->
              <field name="domain_force">[('user_id','=',user.id)]</field>
          </record>
          
          <!-- Rule to allow admin to see all profiles -->
           <record id="influencer_profile_admin_all_rule" model="ir.rule">
              <field name="name">Influencer Profile: Admin All Access</field>
              <field name="model_id" ref="model_influence_gen_influencer_profile"/>
              <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
              <field name="perm_read" eval="True"/>
              <field name="perm_write" eval="True"/>
              <field name="perm_create" eval="True"/>
              <field name="perm_unlink" eval="True"/>
              <field name="domain_force">[(1,'=',1)]</field>
          </record>

          <!-- ... (Define other necessary record rules) -->
      </data>
  </odoo>
  
- **Requirements:** Supports role-based access control as defined in platform administration requirements (e.g., REQ-PAC-001).
- **Documentation:** Custom security groups and record rules.

## 8. Data (`data/`)

### 8.1 `data/__init__.py`
- **Purpose:** Typically empty in Odoo for XML data files.
- **Logic:** Empty.
- **Documentation:** Initializer for the data directory.

### 8.2 `data/platform_setting_data.xml`
- **Purpose:** To load initial/default values for system configurations.
- **Format:** Odoo XML.
- **Content (Examples):**
  xml
  <odoo>
      <data noupdate="1"> <!-- noupdate="1" so these defaults aren't overwritten on module update if manually changed -->
          <record id="setting_default_kyc_doc_types" model="influence_gen.platform_setting">
              <field name="key">kyc.default_document_types</field>
              <field name="value_json">["Passport", "Driver's License", "National ID"]</field>
              <field name="value_type">json</field>
              <field name="description">Default accepted KYC document types (list of strings).</field>
              <field name="module">influence_gen_services</field>
          </record>
          <record id="setting_ai_default_quota" model="influence_gen.platform_setting">
              <field name="key">ai.image_generation.default_monthly_quota</field>
              <field name="value_int">100</field>
              <field name="value_type">int</field>
              <field name="description">Default monthly AI image generation quota per influencer.</field>
              <field name="module">influence_gen_services</field>
          </record>
          <record id="setting_retention_pii_days" model="influence_gen.platform_setting">
              <field name="key">retention.pii.inactive_influencer_days</field>
              <field name="value_int">2555</field> <!-- Approx 7 years -->
              <field name="value_type">int</field>
              <field name="description">Retention period in days for PII of inactive influencers before anonymization/deletion.</field>
              <field name="module">influence_gen_services</field>
          </record>
          <!-- ... (Other default settings) -->
      </data>
  </odoo>
  
- **Requirements:** REQ-IOKYC-017 (example), supports general configuration requirements.
- **Documentation:** Default platform settings.

### 8.3 `data/mail_template_data.xml`
- **Purpose:** To define standard email templates for system notifications.
- **Format:** Odoo XML.
- **Content (Examples for one template):**
  xml
  <odoo>
      <data noupdate="0"> <!-- noupdate="0" allows templates to be updated on module upgrade -->
          <record id="email_template_influencer_registration_confirmation" model="mail.template">
              <field name="name">Influencer Registration Confirmation</field>
              <field name="model_id" ref="model_influence_gen_influencer_profile"/>
              <field name="subject">Welcome to InfluenceGen! Your Registration is Received</field>
              <field name="email_from">"${object.company_id.email_formatted | safe}"</field>
              <field name="email_to">"${object.email | safe}"</field>
              <field name="body_html"><![CDATA[
  <p>Dear ${object.full_name},</p>
  <p>Thank you for registering with InfluenceGen! We have received your application.</p>
  <p>Our team will review your information. You will be notified about the status of your KYC verification and account activation shortly.</p>
  <p>You can check your application status by logging into your portal.</p>
  <p>Best regards,<br/>The InfluenceGen Team</p>
              ]]></field>
              <field name="user_signature" eval="False"/>
              <field name="auto_delete" eval="True"/>
          </record>
          <!-- ... (Define templates for REQ-16-001 to REQ-16-005, etc.) -->
      </data>
  </odoo>
  
- **Requirements:** REQ-16-001, REQ-16-002, REQ-16-003, REQ-16-004, REQ-16-005, REQ-16-015.
- **Documentation:** System email templates.

### 8.4 `data/scheduled_actions_data.xml`
- **Purpose:** To define Odoo cron jobs for automated background tasks.
- **Format:** Odoo XML.
- **Content (Examples):**
  xml
  <odoo>
      <data noupdate="1">
          <record id="ir_cron_apply_retention_policies" model="ir.cron">
              <field name="name">InfluenceGen: Apply Data Retention Policies</field>
              <field name="model_id" ref="model_influence_gen_retention_and_legal_hold_service"/> <!-- Placeholder if using a model for service, or use `ir.model.fields` with model name -->
              <field name="state">code</field>
              <field name="code">model.env['influence_gen.services.retention_and_legal_hold'].apply_retention_policies_automated()</field> <!-- Correct way to call service method -->
              <field name="user_id" ref="base.user_root"/>
              <field name="interval_number">1</field>
              <field name="interval_type">days</field>
              <field name="numbercall">-1</field>
              <field name="doall" eval="False"/>
              <field name="active" eval="True"/>
          </record>
          
          <record id="ir_cron_reset_monthly_ai_quotas" model="ir.cron">
              <field name="name">InfluenceGen: Reset Monthly AI Quotas</field>
              <field name="model_id" ref="model_influence_gen_ai_integration_service"/> <!-- Placeholder -->
              <field name="state">code</field>
              <field name="code">model.env['influence_gen.services.ai_integration'].reset_monthly_quotas_for_all_users()</field> <!-- Method to be defined in service -->
              <field name="user_id" ref="base.user_root"/>
              <field name="interval_number">1</field>
              <field name="interval_type">months</field> <!-- Runs monthly -->
              <field name="nextcall" eval="(DateTime.now() + relativedelta(months=1, day=1, hour=1, minute=0, second=0)).strftime('%Y-%m-%d %H:%M:%S')" />
              <field name="numbercall">-1</field>
              <field name="doall" eval="False"/>
              <field name="active" eval="True"/>
          </record>
      </data>
  </odoo>
  
- **Requirements:** REQ-DRH-002 (retention), REQ-AIGS-002 (quota reset if applicable).
- **Documentation:** Scheduled background tasks.

## 9. Internationalization (`i18n/`)

### 9.1 `i18n/influence_gen_services.pot`
- **Purpose:** Template file for translating module strings.
- **Format:** PO/POT file.
- **Content:** This file will be automatically generated by Odoo's `makepot` command based on translatable strings found in Python code (e.g., `_("My String")`) and XML views. It will contain `msgid` (original string) and empty `msgstr` (translation) pairs.
- **Example snippet:**
  po
  # Odoo Note
  # Entries from Python files
  #. module: influence_gen_services
  #: model:ir.model.fields,field_description:influence_gen_services.field_influence_gen_influencer_profile__full_name
  msgid "Full Name"
  msgstr ""
  
- **Requirements:** REQ-L10N-003.
- **Documentation:** Translation template file.

## 10. Feature Toggles and Configuration
- **Feature Toggles (Examples, managed via `PlatformSetting` or dedicated model):**
    - `kyc.automated_verification_enabled` (Boolean): REQ-IOKYC-005 related.
    - `kyc.micro_deposit_verification_enabled` (Boolean): REQ-IPF-002 related.
    - `ai.advanced_quota_management_enabled` (Boolean): REQ-AIGS-002 related.
    - `data_retention.automated_archival_enabled` (Boolean): REQ-DRH-002, REQ-DRH-007 related.
- **Database Configurations:** Standard Odoo database connection handled by Odoo framework. Specific connection details for external services (AI, KYC, Payment Gateways) will be managed securely via REPO-IGIA-004 and referenced by this service layer if needed, likely through Odoo's configuration parameters or a dedicated secure credential store.

## 11. Data Validation Strategy
- **Server-Side (Mandatory):**
    - **Odoo ORM Constraints:** Python constraints (`@api.constrains`) and SQL constraints (`_sql_constraints`) will be used for model-level validation (format, range, uniqueness, cross-field). (REQ-DMG-010, REQ-DMG-013, REQ-DMG-014, REQ-DMG-016)
    - **Service Layer Validation:** Business services will perform complex validations before calling model methods or interacting with external systems. (REQ-DMG-015)
- **Client-Side (For UX, handled by UI layer - REPO-IGOP-001 & REPO-IGAA-002):** Basic format and required field checks for immediate feedback.

## 12. Dependencies
- **REPO-IGIA-004 (InfluenceGen.Integration.Adapter):** For all interactions with N8N (triggering AI workflows, receiving callbacks) and potentially for direct integrations with third-party KYC, bank verification, or payment services if not routed via N8N. This business service layer will call methods exposed by the adapter.
- **REPO-IGSCU-007 (InfluenceGen.Shared.CommonUtilities):** For any shared utility functions (e.g., advanced encryption beyond Odoo's default if needed, complex data transformation helpers, common constants).

This SDS provides a comprehensive design for the `InfluenceGen.Odoo.Business.Services` repository. Further details for each model and service method will be elaborated during the implementation phase following these specifications.