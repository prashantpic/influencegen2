# Software Design Specification for InfluenceGen.Odoo.Admin.Endpoints (REPO-IGOA-002)

## 1. Introduction

This document outlines the software design specification for the `InfluenceGen.Odoo.Admin.Endpoints` repository. This Odoo module provides the backend user interface (UI) for platform administrators to manage all aspects of the InfluenceGen platform. It includes functionalities for influencer management (KYC review, account status), campaign lifecycle management, AI image generation settings, payment oversight, system configurations, and access to operational dashboards and audit logs.

This module acts as the presentation layer for administrative tasks and interacts with the `InfluenceGen.Odoo.Business.Services` (REPO-IGBS-003) for business logic and data operations.

**Architecture:** This module is part of the `influencegen-odoo-ui-layer` in a Layered Architecture, primarily utilizing Odoo's Model-Template-View (MTV) pattern for backend views and actions.

**Technology Stack:**
*   Framework: Odoo 18
*   Language: Python 3.11, XML
*   Technology: HTTP, Odoo Controllers, Odoo Backend Views (form, tree, kanban, search, dashboard), Odoo Actions, Odoo Wizards.

## 2. Module Structure and Files

### 2.1. Core Module Files

#### 2.1.1. `__init__.py`
*   **Purpose:** Initializes the Python package for the module.
*   **Logic:** Imports submodules: `controllers`, `wizard`.
*   **Namespace:** `odoo.addons.influence_gen_admin`
*   **Contents:**
    python
    # odoo_modules/influence_gen_admin/__init__.py
    from . import controllers
    from . import wizard
    

#### 2.1.2. `__manifest__.py`
*   **Purpose:** Declares the Odoo module, its metadata, dependencies, and data files.
*   **Logic:** A Python dictionary defining:
    *   `name`: "InfluenceGen Platform Administration"
    *   `version`: "18.0.1.0.0"
    *   `summary`: "Administrative interface for managing the InfluenceGen platform."
    *   `author`: "SSS-AI"
    *   `category`: "InfluenceGen/Administration"
    *   `license`: "AGPL-3"
    *   `depends`:
        *   `base`
        *   `mail`
        *   `board`
        *   `account` (for payment integration aspects)
        *   `influence_gen_services` (Technical name for REPO-IGBS-003)
    *   `data`: A list of all XML and CSV files (security, views, menus, wizards, data).
        python
        # Example structure for data list:
        'data': [
            'security/influence_gen_security.xml',
            'security/ir.model.access.csv',
            'views/influence_gen_admin_menus.xml',
            'views/influencer_profile_admin_views.xml',
            'views/kyc_data_admin_views.xml',
            'views/campaign_admin_views.xml',
            'views/campaign_application_admin_views.xml',
            'views/content_submission_admin_views.xml',
            'views/payment_record_admin_views.xml',
            'views/audit_log_admin_views.xml',
            'views/admin_dashboard_views.xml',
            'views/config_settings_views.xml',
            'views/ai_model_admin_views.xml',
            'views/ai_prompt_template_admin_views.xml',
            'views/ai_moderation_rule_admin_views.xml',
            'views/data_retention_policy_admin_views.xml',
            'views/legal_hold_admin_views.xml',
            'views/alert_rule_admin_views.xml',
            'views/maintenance_window_admin_views.xml',
            'views/tos_management_admin_views.xml',
            'views/ai_usage_log_admin_views.xml',
            'wizard/kyc_management_wizard_views.xml',
            'wizard/campaign_management_wizard_views.xml',
            'data/initial_config_data.xml',
        ],
        
    *   `installable`: `True`
    *   `application`: `True` (as it provides a main admin interface for a business application)

### 2.2. Security Configuration

#### 2.2.1. `security/influence_gen_security.xml`
*   **Purpose:** Defines custom security groups and categories. (REQ-PAC-001)
*   **Logic:**
    *   Define `ir.model.category` record:
        *   `id="module_category_influencegen_admin"`
        *   `name="InfluenceGen Platform"`
    *   Define `res.groups` record:
        *   `id="group_influence_gen_platform_admin"`
        *   `name="InfluenceGen / Platform Administrator"`
        *   `category_id="ref('module_category_influencegen_admin')"`
        *   Implies `base.group_user`.
*   **Requirement Mapping:** REQ-PAC-001

#### 2.2.2. `security/ir.model.access.csv`
*   **Purpose:** Defines model-level Access Control Lists (ACLs). (REQ-PAC-001)
*   **Logic:** A CSV file granting full CRUD permissions (`perm_read, perm_write, perm_create, perm_unlink = 1,1,1,1`) to the `group_influence_gen_platform_admin` for all relevant InfluenceGen custom models managed/viewed by this admin module.
    *   Models:
        *   `influence_gen.influencer_profile`
        *   `influence_gen.kyc_data`
        *   `influence_gen.campaign`
        *   `influence_gen.campaign_application`
        *   `influence_gen.content_submission`
        *   `influence_gen.payment_record`
        *   `influence_gen.audit_log` (read-only for admins, create by system)
        *   `influence_gen.ai_image_model`
        *   `influence_gen.ai_prompt_template`
        *   `influence_gen.ai_moderation_rule`
        *   `influence_gen.data_retention_policy`
        *   `influence_gen.legal_hold`
        *   `influence_gen.alert_rule`
        *   `influence_gen.maintenance_window`
        *   `influence_gen.terms_version`
        *   `influence_gen.usage_tracking_log` (read-only for admins, create by system)
        *   Related transient models for wizards (e.g., `influence_gen.kyc_rejection_wizard`).
*   **Requirement Mapping:** REQ-PAC-001

### 2.3. Views (XML)

#### 2.3.1. `views/influence_gen_admin_menus.xml`
*   **Purpose:** Defines the main administrative menu structure.
*   **Logic:** Defines `menuitem` records for a hierarchical menu accessible to `group_influence_gen_platform_admin`.
    *   Root Menu: "InfluenceGen Admin" (`id="menu_influence_gen_admin_root"`)
    *   Sub-menus (examples):
        *   "Dashboard" (action: `action_admin_dashboard`)
        *   "Influencer Management"
            *   "Influencers" (action: `action_influencer_profile_admin`)
            *   "KYC Submissions" (action: `action_kyc_data_admin`)
        *   "Campaign Management"
            *   "Campaigns" (action: `action_campaign_admin`)
            *   "Applications" (action: `action_campaign_application_admin`)
            *   "Content Submissions" (action: `action_content_submission_admin`)
        *   "AI Services"
            *   "AI Models" (action: `action_ai_model_admin`)
            *   "Prompt Templates" (action: `action_ai_prompt_template_admin`)
            *   "Moderation Rules" (action: `action_ai_moderation_rule_admin`)
            *   "Usage Logs" (action: `action_ai_usage_log_admin`)
        *   "Financials"
            *   "Payments" (action: `action_payment_record_admin`)
        *   "Platform Oversight"
            *   "Audit Trail" (action: `action_audit_log_admin`)
            *   (Links to Operational/System Health Dashboards if distinct actions are created)
        *   "Configuration" (links to Odoo's standard settings, then InfluenceGen specific sub-menus)
            *   "InfluenceGen Settings" (action: `action_influence_gen_config_settings`)
            *   "Terms & Policies" (action: `action_terms_version_admin`)
            *   "Data Retention" (action: `action_data_retention_policy_admin`)
            *   "Legal Holds" (action: `action_legal_hold_admin`)
            *   "Alert Rules" (action: `action_alert_rule_admin`)
            *   "Maintenance Windows" (action: `action_maintenance_window_admin`)
*   **Requirement Mapping:** REQ-UIUX-003, REQ-UIUX-015, REQ-PAC-014

#### 2.3.2. `views/influencer_profile_admin_views.xml`
*   **Model:** `influence_gen.influencer_profile` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):**
    *   Display core profile info: `fullName`, `email`, `phone`, `socialMediaProfiles` (One2many list), `areasOfInfluence` (Many2many tags).
    *   Status fields: `kycStatus` (readonly, with visual cues), `accountStatus` (selectable by admin).
    *   Administrative Actions: Buttons for "View KYC Submissions" (links to filtered `kyc_data_admin_views`), "Suspend Account", "Activate Account" (these buttons call server actions on the model).
*   **Requirement Mapping:** REQ-IOKYC-011

#### 2.3.3. `views/kyc_data_admin_views.xml`
*   **Model:** `influence_gen.kyc_data` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):**
    *   Display influencer link, document type, links to view uploaded documents (`documentFrontUrl`, `documentBackUrl` as clickable URLs or embedded images if feasible).
    *   KYC management: `verificationStatus` (header status bar), `reviewerUserId` (defaults to current admin, readonly after first review), `reviewedAt`, `notes`.
    *   Actions: Buttons "Approve KYC", "Reject KYC" (opens `influence_gen.kyc_rejection_wizard`), "Request More Info" (opens `influence_gen.kyc_request_info_wizard`).
*   **Requirement Mapping:** REQ-IOKYC-011

#### 2.3.4. `views/campaign_admin_views.xml`
*   **Model:** `influence_gen.campaign` (from `influence_gen_services`)
*   **Views:** Tree, Form, Kanban, Search
*   **Key Features (Form View):**
    *   All campaign fields: `name`, `description`, `brandClient`, `goals`, `targetCriteria` (JSON field, consider a custom widget if Odoo's default JSON viewer is not user-friendly), `contentRequirements`, `budget`, `compensationModel`, `submissionDeadline`, `startDate`, `endDate`, `usageRights`, `status` (header status bar).
    *   Notebook pages for "Applications", "Content Submissions", "Performance Summary" (linking to related records or displaying aggregated data).
*   **Requirement Mapping:** REQ-2-001, REQ-2-002, REQ-2-003

#### 2.3.5. `views/campaign_application_admin_views.xml`
*   **Model:** `influence_gen.campaign_application` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):**
    *   Display applicant (`influencerProfileId` with link), campaign (`campaignId` with link), `proposal` text.
    *   Application management: `status` (header status bar), `submittedAt`, `reviewedAt`, `reviewerUserId`.
    *   Actions: Buttons "Approve Application", "Reject Application" (opens `influence_gen.campaign_app_rejection_wizard`).
*   **Requirement Mapping:** REQ-2-007

#### 2.3.6. `views/content_submission_admin_views.xml`
*   **Model:** `influence_gen.content_submission` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):**
    *   Display related campaign application, `contentUrl` (clickable link/preview), `generatedImageId` (if applicable, with link).
    *   Review management: `reviewStatus` (header status bar), `feedback` (chatter/history for feedback), `reviewedByUserId`, `reviewedAt`, `version`.
    *   Actions: Buttons "Approve Content", "Reject Content", "Request Revision" (opens `influence_gen.content_revision_wizard`).
*   **Requirement Mapping:** REQ-2-010

#### 2.3.7. `views/payment_record_admin_views.xml`
*   **Model:** `influence_gen.payment_record` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):**
    *   Display influencer, campaign, amount, currency, `status`, transaction details, payment dates.
    *   Actions: Button "Create Vendor Bill" (calls a server action to integrate with Odoo accounting), "Mark as Paid" (for manual status update if direct integration for status feedback is not complete).
*   **Requirement Mapping:** REQ-PAC-015 (UI part)

#### 2.3.8. `views/audit_log_admin_views.xml`
*   **Model:** `influence_gen.audit_log` (from `influence_gen_services`)
*   **Views:** Tree (read-only), Form (read-only), Search
*   **Key Features:**
    *   Tree View: `timestamp`, `eventType`, `actorUserId`, `targetEntity`, `targetId`, `action`, `ipAddress`, `outcome_summary`.
    *   Search View: Filters for all key fields, including date range for `timestamp` and keyword search in `details`.
    *   Form View: Detailed read-only view of a single log entry.
    *   Standard Odoo export functionality from tree view.
*   **Requirement Mapping:** REQ-PAC-016, REQ-ATEL-008, REQ-UIUX-016

#### 2.3.9. `views/admin_dashboard_views.xml`
*   **Purpose:** Defines main administrative dashboards.
*   **Views:** Dashboard (using `ir.ui.view` type `dashboard` or `ir.actions.client` for OWL components)
*   **Key Features:**
    *   Main Admin Dashboard: KPIs (e.g., Active Influencers, Campaigns In Progress), quick links.
    *   System Health Dashboard (conceptual, data via `dashboard_controller.py`): API status, AI service health.
    *   Campaign Performance Dashboard: Aggregated metrics from `influence_gen.campaign_performance_mv` or direct queries.
*   **Requirement Mapping:** REQ-2-012, REQ-PAC-016, REQ-UIUX-019, REQ-12-007, REQ-PAC-014

#### 2.3.10. `views/config_settings_views.xml`
*   **Model:** `res.config.settings` (transient, extended by `influence_gen.config.settings` in business layer)
*   **Views:** Form (inheriting `res.config.settings.view.form`)
*   **Key Features:**
    *   New page "InfluenceGen Settings" with sections for:
        *   User & Security (Password Policies, MFA for Admins) - REQ-PAC-003
        *   KYC Configuration (Accepted ID types, social verification params) - REQ-PAC-007
        *   AI Image Generation (Enabled roles, quotas, default params, ranges, links to manage AI Models, Prompt Templates, Moderation Rules) - REQ-AIGS-002, REQ-AIGS-003, REQ-AIGS-004, REQ-PAC-005, REQ-PAC-004, REQ-UIUX-022
        *   Legal & Compliance (Links to ToS/Policy Management, Data Retention Policy Management) - REQ-PAC-006
        *   Notifications & Email (SMTP link, link to Mail Templates for InfluenceGen) - REQ-PAC-010
        *   Operational Settings (Log Level config link, Alert Rule management link) - REQ-PAC-011
        *   Payment Processing (Default journal, expense account) - REQ-PAC-015
        *   Integration Settings (API keys, Webhook URLs stored securely as `ir.config_parameter`) - REQ-PAC-017
*   **Requirement Mapping:** Covers multiple REQ-PAC-*, REQ-AIGS-*

#### 2.3.11. `views/ai_model_admin_views.xml`
*   **Model:** `influence_gen.ai_image_model` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):** `name`, `description`, `triggerKeywords`, `isActive`, `externalModelId`.
*   **Requirement Mapping:** REQ-AIGS-004, REQ-PAC-005

#### 2.3.12. `views/ai_prompt_template_admin_views.xml`
*   **Model:** `influence_gen.ai_prompt_template` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):** `name`, `promptText`, `category`.
*   **Requirement Mapping:** REQ-AIGS-003, REQ-PAC-005, REQ-UIUX-021

#### 2.3.13. `views/ai_moderation_rule_admin_views.xml`
*   **Model:** `influence_gen.ai_moderation_rule` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):** `name`, `ruleType` (selection: denylist_keyword, regex), `value`, `description`, `isActive`.
*   **Requirement Mapping:** REQ-AIGS-003, REQ-PAC-009

#### 2.3.14. `views/data_retention_policy_admin_views.xml`
*   **Model:** `influence_gen.data_retention_policy` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):** `dataCategory` (selection), `retentionPeriodDays`, `actionOnExpiry` (selection).
*   **Requirement Mapping:** REQ-DRH-008 (UI part for managing policies which REQ-DRH-001 defines)

#### 2.3.15. `views/legal_hold_admin_views.xml`
*   **Model:** `influence_gen.legal_hold` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):** `name` (reason), `targetModel` (selection), `targetRecordId` (reference or char), `status` (active/lifted), dates, responsible users.
*   **Requirement Mapping:** REQ-DRH-008, REQ-DRH-009

#### 2.3.16. `views/alert_rule_admin_views.xml`
*   **Model:** `influence_gen.alert_rule` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):** `name`, `monitoredMetric`, `condition`, `thresholdValue`, `severity`, `notificationChannels`, `recipients`, `isActive`.
*   **Requirement Mapping:** REQ-PAC-011

#### 2.3.17. `views/maintenance_window_admin_views.xml`
*   **Model:** `influence_gen.maintenance_window` (from `influence_gen_services`)
*   **Views:** Tree, Form, Calendar, Search
*   **Key Features (Form View):** `name` (reason), `startDatetime`, `endDatetime`, `status`, `communicationMessage`.
*   **Requirement Mapping:** REQ-PAC-012

#### 2.3.18. `views/tos_management_admin_views.xml`
*   **Model:** `influence_gen.terms_version` (from `influence_gen_services`)
*   **Views:** Tree, Form, Search
*   **Key Features (Form View):** `documentType` (ToS/PrivacyPolicy), `versionNumber`, `effectiveDate`, `content` (HTML/Text or attachment), `isActive`.
*   **Requirement Mapping:** REQ-PAC-006

#### 2.3.19. `views/ai_usage_log_admin_views.xml`
*   **Model:** `influence_gen.usage_tracking_log` (from `influence_gen_services`)
*   **Views:** Tree, Form (read-only), Search, Graph
*   **Key Features (Tree View):** `userId`, `campaignId`, `timestamp`, `modelId`, `imagesGenerated`.
*   **Requirement Mapping:** REQ-AIGS-007

### 2.4. Controllers (Python)

#### 2.4.1. `controllers/__init__.py`
*   **Purpose:** Initializes controllers submodule.
*   **Logic:** `from . import dashboard_controller`

#### 2.4.2. `controllers/dashboard_controller.py`
*   **Purpose:** Backend logic for custom administrative dashboards.
*   **Class:** `AdminDashboardController(http.Controller)`
*   **Methods:**
    *   `get_system_health_data(self, **kw)`:
        *   Route: `/influence_gen_admin/dashboard/system_health`, auth: `user`, type: `json`.
        *   Logic: Calls services in `REPO-IGBS-003` to fetch system health metrics.
        *   Returns: JSON data for dashboard widgets.
    *   `get_campaign_performance_summary(self, **kw)`:
        *   Route: `/influence_gen_admin/dashboard/campaign_performance`, auth: `user`, type: `json`.
        *   Logic: Queries `influence_gen.campaign_performance_mv` or calls services.
        *   Returns: JSON data for campaign performance charts/KPIs.
    *   `get_operational_log_summary(self, **kw)`:
        *   Route: `/influence_gen_admin/dashboard/ops_log_summary`, auth: `user`, type: `json`.
        *   Logic: Placeholder for fetching high-level operational log summaries. May provide links or basic stats if direct integration with centralized logging is complex for UI.
        *   Returns: JSON data.
*   **Requirement Mapping:** REQ-2-012, REQ-PAC-016, REQ-12-007

### 2.5. Wizards (Python & XML)

#### 2.5.1. `wizard/__init__.py`
*   **Purpose:** Initializes wizards submodule.
*   **Logic:**
    python
    from . import kyc_management_wizards
    from . import campaign_management_wizards
    

#### 2.5.2. `wizard/kyc_management_wizards.py`
*   **Purpose:** Logic for KYC management modal dialogs.
*   **Classes:**
    *   `KycRejectionWizard(models.TransientModel)`:
        *   `_name = 'influence_gen.kyc_rejection_wizard'`
        *   Fields: `kyc_data_id` (Many2one `influence_gen.kyc_data`), `rejection_reason` (Text, required).
        *   Method `action_confirm_rejection(self)`: Updates KYC record status to 'rejected', logs reason, triggers notification (via business service REQ-16-002).
    *   `KycRequestInfoWizard(models.TransientModel)`:
        *   `_name = 'influence_gen.kyc_request_info_wizard'`
        *   Fields: `kyc_data_id` (Many2one `influence_gen.kyc_data`), `info_request_message` (Text, required).
        *   Method `action_send_info_request(self)`: Updates KYC record status to 'needs_more_info', logs request, triggers notification (via business service REQ-16-002).
*   **Requirement Mapping:** REQ-IOKYC-011

#### 2.5.3. `wizard/kyc_management_wizard_views.xml`
*   **Purpose:** UI (forms) for KYC wizards.
*   **Logic:** Defines `ir.ui.view` records (form type) for `influence_gen.kyc_rejection_wizard` and `influence_gen.kyc_request_info_wizard`, including input fields and action buttons. Defines `ir.actions.act_window` to launch these wizards, typically called from buttons on the `influence_gen.kyc_data` form view.
*   **Requirement Mapping:** REQ-IOKYC-011

#### 2.5.4. `wizard/campaign_management_wizards.py`
*   **Purpose:** Logic for campaign and content management modal dialogs.
*   **Classes:**
    *   `CampaignApplicationRejectionWizard(models.TransientModel)`:
        *   `_name = 'influence_gen.campaign_app_rejection_wizard'`
        *   Fields: `application_id` (Many2one `influence_gen.campaign_application`), `rejection_reason` (Text, required).
        *   Method `action_confirm_application_rejection(self)`: Updates application status to 'rejected', logs reason, triggers notification (REQ-16-004 via business service).
    *   `ContentRevisionWizard(models.TransientModel)`:
        *   `_name = 'influence_gen.content_revision_wizard'`
        *   Fields: `submission_id` (Many2one `influence_gen.content_submission`), `revision_feedback` (Text, required).
        *   Method `action_request_content_revision(self)`: Updates submission status to 'needs_revision', logs feedback, triggers notification (REQ-16-005 via business service).
*   **Requirement Mapping:** REQ-2-007, REQ-2-008, REQ-2-010

#### 2.5.5. `wizard/campaign_management_wizard_views.xml`
*   **Purpose:** UI (forms) for campaign/content wizards.
*   **Logic:** Defines `ir.ui.view` records for the wizards in `campaign_management_wizards.py` and corresponding `ir.actions.act_window`.
*   **Requirement Mapping:** REQ-2-007, REQ-2-010

### 2.6. Static Assets

#### 2.6.1. `static/src/js/custom_admin_dashboard.js`
*   **Purpose:** JavaScript (OWL components) for dynamic admin dashboards.
*   **Logic:** Defines OWL components to fetch data from `dashboard_controller.py` endpoints using Odoo's `rpc` service. Renders charts (e.g., using Chart.js if available in Odoo core/assets or simple SVG) and KPI cards.
    *   Component `AdminMainDashboard`: Main container, fetches initial data.
    *   Component `AdminKPIWidget`: Reusable for displaying KPI values.
    *   Component `AdminChartWidget`: Reusable for displaying various chart types.
*   Components are registered and included via assets in `__manifest__.py`.
*   **Requirement Mapping:** REQ-2-012, REQ-PAC-016, REQ-UIUX-019, REQ-12-007

#### 2.6.2. `static/src/css/admin_backend_styles.css`
*   **Purpose:** Custom styling for the admin backend.
*   **Logic:** Contains CSS/SCSS rules for any custom styling needs of InfluenceGen admin views or dashboards that go beyond standard Odoo themes. Should be minimal. Included via assets.
*   **Requirement Mapping:** REQ-UIUX-003

### 2.7. Data Files

#### 2.7.1. `data/initial_config_data.xml`
*   **Purpose:** Loads initial or default configuration data.
*   **Logic:**
    *   Create `ir.model.category` for "InfluenceGen Platform".
    *   Create `res.groups` for `group_influence_gen_platform_admin`.
    *   Set default `ir.config_parameter` values for some settings defined in `config_settings_views.xml` (e.g., default password policy parameters if desired).
    *   Potentially define `mail.template` records for specific admin-triggered notifications if not using standard ones.
*   **Requirement Mapping:** REQ-PAC-001, REQ-PAC-010

## 3. Key Design Considerations

*   **Service Layer Interaction:** All UI actions (buttons, wizard confirmations) that involve business logic or data manipulation beyond simple CRUD will call methods on the service layer models defined in `REPO-IGBS-003` (`influence_gen_services`). This admin module focuses on presentation and user interaction within the Odoo backend.
*   **Read-Only Fields:** Many fields in admin views will be read-only, displaying data managed by influencers or system processes (e.g., `kycStatus` on influencer profile, which is changed via `KYCData` review). Admins will have specific actions to trigger changes.
*   **Configuration Models:** For complex configurations like AI Prompt Templates, Moderation Rules, Data Retention Policies, etc., dedicated models (defined in `REPO-IGBS-003`) will be created and managed via standard Odoo CRUD views defined in this admin module. Simpler settings will use `res.config.settings` and `ir.config_parameter`.
*   **Efficiency for Admins (REQ-UIUX-003):**
    *   Organized menu structure.
    *   Efficient list views with relevant default filters and sorting.
    *   Quick actions/buttons for common tasks.
    *   Dashboards for at-a-glance information.
*   **Security:** All views, menus, and actions must be secured using `groups` attribute, restricting access to `group_influence_gen_platform_admin`. Sensitive data display (e.g., API keys in config) should be handled carefully (e.g., write-only, display masked).
*   **Extensibility:** Design should allow for future addition of new administrative sections or configuration options by adding new views, menus, and extending `res.config.settings`.

## 4. AI Instructions for Code Generation

1.  **General Instructions for Odoo Module Structure:**
    *   Generate the standard Odoo module directory structure: `__init__.py`, `__manifest__.py`, `controllers/`, `data/`, `models/` (though most models are in services, this admin module might have `res.config.settings` extensions and wizard models), `security/`, `static/src/css/`, `static/src/js/`, `static/src/xml/` (for OWL templates if any), `views/`, `wizard/`.
    *   Ensure all Python files have UTF-8 encoding headers and Odoo S.A. license headers (or specified project license).
    *   Ensure all XML files have XML declaration and UTF-8 encoding.

2.  **For `__manifest__.py`:**
    *   List all XML files from the `views/`, `security/`, `wizard/`, and `data/` directories in the `'data'` key.
    *   Include `influence_gen_services` (or the correct technical name of REPO-IGBS-003) in the `'depends'` list, along with other standard Odoo dependencies like `base`, `mail`, `board`, `account`.

3.  **For XML View Files (`views/*.xml`, `wizard/*.xml`):**
    *   For each model, generate corresponding `ir.actions.act_window` and `menuitem` records. Link actions to menu items.
    *   Apply `groups="influence_gen_admin.group_influence_gen_platform_admin"` to all admin-specific menu items and actions.
    *   **Form Views:**
        *   Use `<sheet>`, `<group>`, and `<notebook>` for layout.
        *   Include all relevant fields as per the SDS for each model.
        *   Use appropriate widgets (e.g., `widget="url"`, `widget="many2many_tags"`, `widget="json"`).
        *   Implement `<header>` with `<button>` elements for actions and a `<field name="status" widget="statusbar"/>` where applicable.
        *   For fields linking to other records (e.g., `influencerProfileId`), make them clickable to navigate.
    *   **Tree/List Views:**
        *   Select key columns for display. Make them concise.
        *   Consider default sorting if applicable.
    *   **Search Views:**
        *   Include `<field>` elements for common search/filter criteria.
        *   Define `<filter>` elements for predefined filters (e.g., by status).
    *   **Kanban Views (e.g., for Campaigns):**
        *   Define fields for card display.
        *   Specify grouping field (e.g., `status`).
    *   **Dashboard Views (`admin_dashboard_views.xml`):**
        *   If using standard Odoo dashboards, define `ir.ui.view` with `arch` type `dashboard`.
        *   If using custom OWL components, define `ir.actions.client` with `tag` pointing to the OWL component name, and potentially a QWeb template (`<template>`) to structure the dashboard if it's not fully JS-driven.
    *   **Configuration Settings (`config_settings_views.xml`):**
        *   Inherit `res.config.settings.view.form`.
        *   Use `xpath` to add new pages or groups.
        *   Define `<setting>` tags or direct fields for each configuration option. For `ir.config_parameter` fields, ensure the Python model `res.config.settings` has corresponding `get_` and `set_` methods.

4.  **For Python Controller Files (`controllers/*.py`):**
    *   Import necessary Odoo modules (`odoo.http`, `odoo.http.request`).
    *   Define controller classes inheriting from `http.Controller`.
    *   Use `@http.route('/route/path', type='json', auth='user', methods=['POST'], csrf=False)` for JSON API endpoints. `csrf=False` is generally needed if called from JS without Odoo's form submission mechanism, but ensure proper security if so. For dashboard data fetching, `type='json', auth='user'` is typical.
    *   Ensure methods access data via service calls to `REPO-IGBS-003` rather than direct ORM calls where complex logic is involved.
    *   Return `http.Response` with `json.dumps(data)` for JSON endpoints.

5.  **For Python Wizard Files (`wizard/*.py`):**
    *   Define classes inheriting from `models.TransientModel`.
    *   Define fields required for the wizard's operation.
    *   Implement action methods (e.g., `action_confirm_rejection`) that perform the wizard's logic, update target records, and potentially trigger service calls (e.g., for notifications). These methods should return an action dictionary to close the wizard or open another view.

6.  **For Security Files (`security/*.xml`, `security/ir.model.access.csv`):**
    *   In `influence_gen_security.xml`, correctly define the module category and the primary admin group.
    *   In `ir.model.access.csv`, ensure all custom models from `influence_gen_services` that are accessed by this admin module have appropriate permissions defined for the `group_influence_gen_platform_admin`. For logs like `influence_gen.audit_log` or `influence_gen.usage_tracking_log`, grant read access but deny write/create/delete for typical admins (creation is by system).

7.  **For JavaScript Files (`static/src/js/*.js` for OWL components):**
    *   Define OWL components using `Component`, `useState`, `onWillStart`, etc.
    *   Use `this.env.services.rpc` or `this.env.services.http` to make calls to backend controllers.
    *   Structure components for reusability (e.g., KPI widget, chart widget).
    *   Ensure components are registered in the Odoo JS registry (e.g., `registry.category("actions").add("influence_gen_admin.AdminDashboard", AdminMainDashboard);`).
    *   Define XML templates (`<t t-name="..."/>`) for OWL components, likely in a separate `static/src/xml/dashboard_templates.xml` file which then needs to be added to `__manifest__.py` assets.

8.  **For Data Files (`data/*.xml`):**
    *   Use `<record>` tags with appropriate model names.
    *   Ensure IDs are unique and follow a consistent naming convention.
    *   For `ir.config_parameter`, remember to set `group_ids` if the parameter should only be visible/editable by system admins (`base.group_system`).

9.  **General Coding Standards:**
    *   Follow PEP 8 for Python.
    *   Use Odoo's conventions for field naming (`snake_case`), model naming (`project_prefix.model_name`), XML IDs (`module_name.view_id_purpose`).
    *   Add comments to complex Python logic and XML structures.
    *   Ensure all user-facing strings in Python and XML are translatable (`_()` in Python, implicit in XML views).

This detailed breakdown should provide sufficient guidance for generating the code for the `InfluenceGen.Odoo.Admin.Endpoints` module.