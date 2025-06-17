# Specification

# 1. Files

- **Path:** odoo_modules/influence_gen_admin/__init__.py  
**Description:** Initializes the Python package, importing submodules like models, wizards, and controllers.  
**Template:** Odoo Python Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** __init__.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Standard Odoo module init file to make Python modules discoverable.  
**Logic Description:** Contains import statements for `models`, `wizards`, `controllers` subdirectories if they exist and contain Python files.  
**Documentation:**
    
    - **Summary:** Bootstraps the 'influence_gen_admin' Odoo module's Python components.
    
**Namespace:** odoo.addons.influence_gen_admin  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_admin/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata, dependencies, and data files.  
**Template:** Odoo Manifest  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    
**Requirement Ids:**
    
    - REQ-DDSI-001
    
**Purpose:** Declares the Odoo module, its name, version, author, category, dependencies (e.g., influence_gen_services, base, mail), and list of XML/CSV data files to load.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'description', 'author', 'category', 'depends', 'data', 'installable', 'application'. 'depends' will include 'influence_gen_services' (REPO-IGBS-003), 'base'. 'data' will list all XML and CSV files for views, menus, security, actions, and default data.  
**Documentation:**
    
    - **Summary:** Defines the 'InfluenceGen Administration Backend' Odoo module and its properties.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_admin/security/ir.model.access.csv  
**Description:** Defines model-level access rights (CRUD) for various security groups for all InfluenceGen models managed by administrators.  
**Template:** Odoo Access CSV  
**Dependancy Level:** 0  
**Name:** ir.model.access  
**Type:** Security Configuration  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Role-Based Access Control
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Access Control
    
**Requirement Ids:**
    
    - REQ-PAC-001
    
**Purpose:** Specifies read, write, create, and delete permissions for different user groups (e.g., Platform Administrator) on InfluenceGen specific models and extended Odoo models.  
**Logic Description:** CSV file with columns: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. Entries for models like `influence_gen.campaign`, `influence_gen.influencer_profile`, `influence_gen.kyc_data`, `influence_gen.ai_model_config`, `influence_gen.legal_document_version`, `influence_gen.maintenance_window`, `influence_gen.legal_hold`, etc. granting permissions to the 'Platform Administrator' group.  
**Documentation:**
    
    - **Summary:** Manages access control lists for InfluenceGen data models for administrators.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** odoo_modules/influence_gen_admin/security/influence_gen_admin_groups.xml  
**Description:** Defines security groups for the InfluenceGen administration backend, primarily the 'Platform Administrator' role.  
**Template:** Odoo XML Data  
**Dependancy Level:** 0  
**Name:** influence_gen_admin_groups  
**Type:** Security Configuration  
**Relative Path:** security/influence_gen_admin_groups.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Role-Based Access Control
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Role Management
    
**Requirement Ids:**
    
    - REQ-PAC-001
    
**Purpose:** Creates Odoo security groups, such as 'InfluenceGen Platform Administrator', which will be used to assign access rights and menu visibility.  
**Logic Description:** XML file defining `<record model="res.groups">` for administrator roles. Example: `id="group_influence_gen_platform_admin" name="InfluenceGen Platform Administrator" category_id="module_category_influence_gen_administration"`.  
**Documentation:**
    
    - **Summary:** Establishes user roles (security groups) for managing the InfluenceGen platform.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** odoo_modules/influence_gen_admin/models/__init__.py  
**Description:** Initializes the Python models package for the admin backend.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** models/__init__.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Imports all model files within this directory to make them available to Odoo.  
**Logic Description:** Contains import statements for `res_config_settings`, `ai_model_config`, `legal_document_version`, `maintenance_window`, `legal_hold` etc.  
**Documentation:**
    
    - **Summary:** Aggregates admin-specific model definitions.
    
**Namespace:** odoo.addons.influence_gen_admin.models  
**Metadata:**
    
    - **Category:** Model
    
- **Path:** odoo_modules/influence_gen_admin/models/res_config_settings.py  
**Description:** Extends Odoo's base configuration settings model to add InfluenceGen platform-specific configurations.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** ResConfigSettings  
**Type:** Model  
**Relative Path:** models/res_config_settings.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Configuration Management
    
**Members:**
    
    - **Name:** influence_gen_password_min_length  
**Type:** fields.Integer  
**Attributes:**   
    - **Name:** influence_gen_password_complexity_regex  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** influence_gen_mfa_admin_mandatory  
**Type:** fields.Boolean  
**Attributes:**   
    - **Name:** influence_gen_ai_quota_default_images_per_month  
**Type:** fields.Integer  
**Attributes:**   
    - **Name:** influence_gen_ai_default_resolution  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** influence_gen_kyc_accepted_doc_types  
**Type:** fields.Char  
**Attributes:** help='Comma-separated list'  
    - **Name:** influence_gen_data_retention_pii_days  
**Type:** fields.Integer  
**Attributes:**   
    - **Name:** influence_gen_content_moderation_keywords_denylist  
**Type:** fields.Text  
**Attributes:**   
    - **Name:** influence_gen_smtp_host  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** influence_gen_log_level_default  
**Type:** fields.Selection  
**Attributes:** selection=[('DEBUG', 'Debug'), ('INFO', 'Info'), ('WARN', 'Warning'), ('ERROR', 'Error')  
    - **Name:** influence_gen_api_rate_limit_default  
**Type:** fields.Char  
**Attributes:**   
    - **Name:** influence_gen_payment_default_journal_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='account.journal'  
    - **Name:** influence_gen_secrets_management_url  
**Type:** fields.Char  
**Attributes:**   
    
**Methods:**
    
    - **Name:** set_values  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** api.model  
    - **Name:** get_values  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** api.model  
    
**Implemented Features:**
    
    - Platform Configuration Management
    
**Requirement Ids:**
    
    - REQ-PAC-003
    - REQ-PAC-004
    - REQ-PAC-005
    - REQ-PAC-007
    - REQ-PAC-008
    - REQ-PAC-009
    - REQ-PAC-010
    - REQ-PAC-011
    - REQ-PAC-013
    - REQ-PAC-015
    - REQ-PAC-017
    - REQ-ATEL-003
    - REQ-ATEL-011
    - REQ-DRH-001
    - REQ-DRH-006
    
**Purpose:** Defines fields for InfluenceGen settings in Odoo's general settings interface. Handles saving and loading these settings.  
**Logic Description:** Inherits from `res.config.settings`. Defines various `fields.*` related to InfluenceGen configurations. Implements `set_values` to save configurations (e.g., using `ir.config_parameter`) and `get_values` to retrieve them. Fields will cover password policies, AI quotas/parameters, KYC rules, data retention periods, content moderation, email/SMTP, logging levels, rate limits, payment integration defaults, and secrets management references.  
**Documentation:**
    
    - **Summary:** Model for managing all InfluenceGen system configurations accessible via the Odoo settings panel.
    
**Namespace:** odoo.addons.influence_gen_admin.models  
**Metadata:**
    
    - **Category:** Model
    
- **Path:** odoo_modules/influence_gen_admin/models/ai_model_config.py  
**Description:** Model to manage the list of available AI image generation models (e.g., Flux LoRA models) and their metadata.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** AiModelConfig  
**Type:** Model  
**Relative Path:** models/ai_model_config.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Configuration Management
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required=True string='Model Name'  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** string='Description'  
    - **Name:** model_type  
**Type:** fields.Selection  
**Attributes:** selection=[('flux_lora', 'Flux LoRA'), ('other', 'Other')] required=True string='Model Type'  
    - **Name:** trigger_keywords  
**Type:** fields.Char  
**Attributes:** string='Trigger Keywords'  
    - **Name:** api_endpoint_info  
**Type:** fields.Char  
**Attributes:** string='API Endpoint/Identifier'  
    - **Name:** is_active  
**Type:** fields.Boolean  
**Attributes:** string='Active' default=True  
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Management
    
**Requirement Ids:**
    
    - REQ-PAC-005
    - REQ-AIGS-004
    
**Purpose:** Allows administrators to define and manage the AI models (especially LoRA models) available for image generation within the platform.  
**Logic Description:** Defines an Odoo model `influence_gen.ai_model_config` with fields for model name, type, description, associated keywords, API specific identifiers, and active status. This allows admins to curate the list of usable models.  
**Documentation:**
    
    - **Summary:** Manages the configuration and metadata of AI image generation models.
    
**Namespace:** odoo.addons.influence_gen_admin.models  
**Metadata:**
    
    - **Category:** Model
    
- **Path:** odoo_modules/influence_gen_admin/models/legal_document_version.py  
**Description:** Model to manage versions of Terms of Service (ToS) and Privacy Policy documents.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** LegalDocumentVersion  
**Type:** Model  
**Relative Path:** models/legal_document_version.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Configuration Management
    
**Members:**
    
    - **Name:** document_type  
**Type:** fields.Selection  
**Attributes:** selection=[('tos', 'Terms of Service'), ('privacy_policy', 'Privacy Policy')] required=True string='Document Type'  
    - **Name:** version  
**Type:** fields.Char  
**Attributes:** required=True string='Version'  
    - **Name:** content  
**Type:** fields.Html  
**Attributes:** required=True string='Content'  
    - **Name:** effective_date  
**Type:** fields.Date  
**Attributes:** required=True string='Effective Date'  
    - **Name:** is_active  
**Type:** fields.Boolean  
**Attributes:** string='Active' default=False  
    
**Methods:**
    
    - **Name:** _check_active_version_unicity  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** api.constrains('is_active', 'document_type')  
    
**Implemented Features:**
    
    - ToS/Privacy Policy Management
    
**Requirement Ids:**
    
    - REQ-PAC-006
    
**Purpose:** Enables administrators to upload, version, and activate ToS and Privacy Policy documents. Ensures only one active version per document type.  
**Logic Description:** Defines an Odoo model `influence_gen.legal_document_version` with fields for document type, version string, HTML content, effective date, and an active flag. A constraint ensures only one version of each document type can be active at a time.  
**Documentation:**
    
    - **Summary:** Manages different versions of legal documents like ToS and Privacy Policy.
    
**Namespace:** odoo.addons.influence_gen_admin.models  
**Metadata:**
    
    - **Category:** Model
    
- **Path:** odoo_modules/influence_gen_admin/models/maintenance_window.py  
**Description:** Model to schedule and manage planned system maintenance windows.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** MaintenanceWindow  
**Type:** Model  
**Relative Path:** models/maintenance_window.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Configuration Management
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required=True string='Title'  
    - **Name:** start_datetime  
**Type:** fields.Datetime  
**Attributes:** required=True string='Start Time'  
    - **Name:** end_datetime  
**Type:** fields.Datetime  
**Attributes:** required=True string='End Time'  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** string='Description/Impact'  
    - **Name:** notify_users  
**Type:** fields.Boolean  
**Attributes:** string='Notify Users' default=True  
    - **Name:** notification_message  
**Type:** fields.Text  
**Attributes:** string='Notification Message'  
    
**Methods:**
    
    - **Name:** action_send_notification  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Maintenance Window Scheduling
    
**Requirement Ids:**
    
    - REQ-PAC-012
    
**Purpose:** Allows administrators to define, schedule, and document planned maintenance windows, and optionally trigger notifications.  
**Logic Description:** Defines an Odoo model `influence_gen.maintenance_window` with fields for title, start/end times, description, and notification details. A method could be added to trigger user notifications or integrate with system banners.  
**Documentation:**
    
    - **Summary:** Manages the scheduling and communication of system maintenance periods.
    
**Namespace:** odoo.addons.influence_gen_admin.models  
**Metadata:**
    
    - **Category:** Model
    
- **Path:** odoo_modules/influence_gen_admin/models/legal_hold.py  
**Description:** Model to manage legal holds on specific data entities within the InfluenceGen platform.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** LegalHold  
**Type:** Model  
**Relative Path:** models/legal_hold.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Configuration Management
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required=True string='Hold Name/Case ID'  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** string='Reason for Hold'  
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** selection=[('active', 'Active'), ('lifted', 'Lifted')] required=True default='active' string='Status'  
    - **Name:** target_model_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='ir.model' string='Target Model' required=True  
    - **Name:** target_record_ids_char  
**Type:** fields.Char  
**Attributes:** string='Target Record IDs (comma-separated)'  
    - **Name:** target_influencer_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='influence_gen.influencer_profile' string='Target Influencer'  
    - **Name:** target_campaign_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='influence_gen.campaign' string='Target Campaign'  
    - **Name:** effective_date  
**Type:** fields.Date  
**Attributes:** required=True string='Effective Date'  
    - **Name:** lifted_date  
**Type:** fields.Date  
**Attributes:** string='Lifted Date'  
    - **Name:** created_by_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users' string='Created By' readonly=True  
    
**Methods:**
    
    - **Name:** action_lift_hold  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Legal Hold Management
    
**Requirement Ids:**
    
    - REQ-DRH-008
    - REQ-DRH-009
    
**Purpose:** Enables authorized administrators to place, manage, and lift legal holds on specified data, preventing its modification or deletion.  
**Logic Description:** Defines `influence_gen.legal_hold` model with fields for hold name, reason, status, target data (model and record IDs or specific entities like influencer/campaign), effective/lifted dates. Logic in other models (data retention service) must check against active legal holds before data disposition.  
**Documentation:**
    
    - **Summary:** Manages legal hold records, ensuring data preservation for legal or regulatory needs.
    
**Namespace:** odoo.addons.influence_gen_admin.models  
**Metadata:**
    
    - **Category:** Model
    
- **Path:** odoo_modules/influence_gen_admin/views/influence_gen_admin_menus.xml  
**Description:** Defines the main menu structure for the InfluenceGen administration backend.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** influence_gen_admin_menus  
**Type:** View  
**Relative Path:** views/influence_gen_admin_menus.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin Navigation
    
**Requirement Ids:**
    
    - REQ-PAC-014
    - REQ-UIUX-003
    - REQ-UIUX-015
    
**Purpose:** Creates top-level and sub-menu items for accessing all InfluenceGen administrative functionalities, ensuring an organized and efficient interface.  
**Logic Description:** XML file defining `<menuitem>` records. A main 'InfluenceGen Admin' menu, with sub-menus for 'KYC Management', 'Campaign Management', 'User Management', 'AI Services', 'Financials', 'System Configuration', 'Monitoring & Logs', 'Data Management', 'Notifications'. Each sub-menu will link to specific actions.  
**Documentation:**
    
    - **Summary:** Defines the primary navigation structure for administrators within the InfluenceGen Odoo backend.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/kyc_submission_views.xml  
**Description:** XML views (list, form, kanban, search) and actions for managing influencer KYC submissions by administrators.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** kyc_submission_views  
**Type:** View  
**Relative Path:** views/kyc_submission_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - KYC Review Interface
    
**Requirement Ids:**
    
    - REQ-IOKYC-011
    
**Purpose:** Provides administrators with interfaces to view, review, approve, reject, or request more information for KYC submissions. Links to the `influence_gen.kyc_data` model (from business services).  
**Logic Description:** Defines `<record model="ir.ui.view">` for list, form, kanban, and search views for `influence_gen.kyc_data`. Form view will include buttons to trigger actions like 'Approve KYC', 'Reject KYC', 'Request More Information' (which might open a wizard). Defines `<record model="ir.actions.act_window">` to make these views accessible via menus.  
**Documentation:**
    
    - **Summary:** User interfaces for administrative review and management of influencer KYC submissions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/user_management_views.xml  
**Description:** Extends Odoo's user and group views for platform administrator specific actions and information display.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** user_management_views  
**Type:** View  
**Relative Path:** views/user_management_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Role Management UI
    - User Account Management UI
    
**Requirement Ids:**
    
    - REQ-PAC-001
    - REQ-PAC-002
    
**Purpose:** Provides interfaces for administrators to manage user accounts (create, modify, activate/deactivate) and assign roles (security groups).  
**Logic Description:** XML file possibly inheriting and extending existing `res.users` and `res.groups` views to add InfluenceGen specific fields or actions if necessary. Defines actions to access these views. May link to the `influence_gen_admin_groups.xml` for group management.  
**Documentation:**
    
    - **Summary:** Admin UIs for managing user accounts and their roles/permissions within the InfluenceGen platform.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/platform_config_settings_views.xml  
**Description:** View for `res.config.settings` to manage InfluenceGen platform-wide configurations.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** platform_config_settings_views  
**Type:** View  
**Relative Path:** views/platform_config_settings_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - Configuration Management
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Centralized Platform Configuration UI
    
**Requirement Ids:**
    
    - REQ-PAC-003
    - REQ-PAC-004
    - REQ-PAC-005
    - REQ-PAC-007
    - REQ-PAC-008
    - REQ-PAC-009
    - REQ-PAC-010
    - REQ-PAC-011
    - REQ-PAC-013
    - REQ-PAC-015
    - REQ-PAC-017
    - REQ-UIUX-015
    
**Purpose:** Provides a centralized UI within Odoo's settings for administrators to configure various aspects of the InfluenceGen platform.  
**Logic Description:** XML file defining a form view inheriting from `res.config.settings.view_form`. Adds sections and fields defined in `models/res_config_settings.py` for password policies, AI quotas, default AI parameters, KYC rules (e.g. accepted doc types), data retention periods, content moderation keywords, SMTP settings, default logging levels, API rate limits, payment journal defaults, and references to secrets. Defines an action to open these settings.  
**Documentation:**
    
    - **Summary:** UI for administrators to configure global settings for the InfluenceGen platform.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/ai_model_config_views.xml  
**Description:** XML views (list, form) and actions for managing AI image generation models.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** ai_model_config_views  
**Type:** View  
**Relative Path:** views/ai_model_config_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Management UI
    
**Requirement Ids:**
    
    - REQ-PAC-005
    - REQ-AIGS-004
    
**Purpose:** Provides UI for administrators to define and manage AI models available in the system.  
**Logic Description:** Defines list and form views for the `influence_gen.ai_model_config` model. Includes fields for model name, description, type, keywords, API info, and active status. Defines an action to access these views.  
**Documentation:**
    
    - **Summary:** Interfaces for managing the list and properties of AI image generation models.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/legal_document_version_views.xml  
**Description:** XML views (list, form) and actions for managing ToS and Privacy Policy document versions.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** legal_document_version_views  
**Type:** View  
**Relative Path:** views/legal_document_version_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Legal Document Management UI
    
**Requirement Ids:**
    
    - REQ-PAC-006
    
**Purpose:** Provides UI for administrators to manage versions of legal documents like ToS and Privacy Policy.  
**Logic Description:** Defines list and form views for the `influence_gen.legal_document_version` model. Includes fields for document type, version, content (HTML), effective date, and active status. Defines an action to access these views.  
**Documentation:**
    
    - **Summary:** Interfaces for managing and versioning Terms of Service and Privacy Policy documents.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/maintenance_window_views.xml  
**Description:** XML views (list, form, calendar) and actions for managing scheduled maintenance windows.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** maintenance_window_views  
**Type:** View  
**Relative Path:** views/maintenance_window_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Maintenance Window UI
    
**Requirement Ids:**
    
    - REQ-PAC-012
    
**Purpose:** Provides UI for administrators to schedule and manage planned system maintenance.  
**Logic Description:** Defines list, form, and potentially calendar views for the `influence_gen.maintenance_window` model. Fields include title, start/end times, description, notification options. Defines an action.  
**Documentation:**
    
    - **Summary:** Interfaces for scheduling and managing system maintenance windows.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/campaign_management_views.xml  
**Description:** Views (list, form, kanban, search) and actions for campaign creation and lifecycle management.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** campaign_management_views  
**Type:** View  
**Relative Path:** views/campaign_management_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign Creation UI
    - Campaign Review UI
    - Content Approval UI
    
**Requirement Ids:**
    
    - REQ-2-001
    - REQ-2-002
    - REQ-2-003
    - REQ-2-007
    - REQ-2-010
    
**Purpose:** UIs for admins to create new campaigns, define criteria, review influencer applications, and manage submitted content. Interacts with `influence_gen.campaign`, `influence_gen.campaign_application`, `influence_gen.content_submission` models.  
**Logic Description:** Defines views for `influence_gen.campaign` (name, description, goals, budget, etc.), `influence_gen.campaign_application` (proposals, status, approve/reject actions), and `influence_gen.content_submission` (view content, feedback, approve/reject actions). Includes necessary window actions.  
**Documentation:**
    
    - **Summary:** Administrative interfaces for comprehensive campaign lifecycle management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/performance_dashboard_views.xml  
**Description:** XML view definition for the administrator's performance dashboard.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** performance_dashboard_views  
**Type:** View  
**Relative Path:** views/performance_dashboard_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin Performance Dashboard UI
    
**Requirement Ids:**
    
    - REQ-2-012
    - REQ-UIUX-015
    
**Purpose:** Provides an overview of platform-wide campaign performance, influencer activity, and other key metrics for administrators.  
**Logic Description:** Defines an Odoo dashboard view (e.g., using `<dashboard>`) or a custom QWeb view if more complex visualizations are needed. It will aggregate data from various models (e.g., campaigns, applications, payments). May require methods on underlying models or controllers to fetch and prepare data.  
**Documentation:**
    
    - **Summary:** Dashboard UI for administrators to monitor key performance indicators of the platform.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/payment_management_views.xml  
**Description:** Views and actions for managing influencer payments, including tracking owed amounts and payment statuses.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** payment_management_views  
**Type:** View  
**Relative Path:** views/payment_management_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Payment Oversight UI
    - Payment Batch Generation UI
    
**Requirement Ids:**
    
    - REQ-2-014
    - REQ-2-015
    - REQ-IPF-003
    - REQ-IPF-004
    - REQ-IPF-005
    - REQ-IPF-007
    - REQ-IPF-008
    
**Purpose:** UIs for administrators to oversee influencer payments, generate payment requests/batches, and record payment statuses. Interacts with `influence_gen.payment_record` model.  
**Logic Description:** Defines list, form, and search views for `influence_gen.payment_record`. Form view will show details like amount, status, influencer, campaign. List view will allow batch actions like 'Generate Vendor Bills' (REQ-2-014) or 'Mark as Paid'. Includes actions for managing compensation models and payment settings (linked to `res.config.settings`).  
**Documentation:**
    
    - **Summary:** Administrative interfaces for managing and tracking influencer payments.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/ai_usage_tracking_views.xml  
**Description:** Views for administrators to monitor AI image generation usage metrics.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** ai_usage_tracking_views  
**Type:** View  
**Relative Path:** views/ai_usage_tracking_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Usage Reporting UI
    
**Requirement Ids:**
    
    - REQ-AIGS-007
    
**Purpose:** Provides administrators with reports or dashboards displaying AI image generation usage (images per user/campaign, API calls). Likely views on `influence_gen.ai_image_generation_request` or a dedicated aggregated model.  
**Logic Description:** Defines graph and pivot views for `influence_gen.ai_image_generation_request` or a related aggregated model (e.g., `influence_gen.ai_usage_summary`). Allows grouping by user, campaign, model. Defines an action to access these views.  
**Documentation:**
    
    - **Summary:** UI for administrators to view and analyze AI image generation usage data.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/audit_log_viewer_views.xml  
**Description:** Views for administrators to review audit logs with filtering, searching, and export capabilities.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** audit_log_viewer_views  
**Type:** View  
**Relative Path:** views/audit_log_viewer_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Review UI
    
**Requirement Ids:**
    
    - REQ-PAC-016
    - REQ-UIUX-016
    - REQ-ATEL-008
    
**Purpose:** Provides a secure interface for administrators to access and analyze audit trail logs. Interacts with the `influence_gen.audit_log` model.  
**Logic Description:** Defines list and search views for the `influence_gen.audit_log` model. Search view includes filters for timestamp, user, event type, target entity/ID. List view displays key audit log fields. Potentially an export action. Defines a window action for menu access.  
**Documentation:**
    
    - **Summary:** Interface for administrators to search, filter, and export audit trail logs.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/system_health_dashboard_views.xml  
**Description:** Custom dashboard for administrators to view system health metrics.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** system_health_dashboard_views  
**Type:** View  
**Relative Path:** views/system_health_dashboard_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - System Health Dashboard UI
    
**Requirement Ids:**
    
    - REQ-PAC-014
    - REQ-12-007
    
**Purpose:** Presents key system health indicators to administrators for operational oversight.  
**Logic Description:** Defines an Odoo dashboard view (`<dashboard>`) or a QWeb view that aggregates and displays metrics like API error rates, queue lengths, resource utilization. Data might be fetched via model methods or specific controller endpoints if very dynamic.  
**Documentation:**
    
    - **Summary:** Dashboard providing an overview of system health and operational status to administrators.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/views/legal_hold_management_views.xml  
**Description:** Views and actions for managing legal holds on data.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** legal_hold_management_views  
**Type:** View  
**Relative Path:** views/legal_hold_management_views.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Legal Hold Management UI
    
**Requirement Ids:**
    
    - REQ-DRH-003
    - REQ-DRH-004
    - REQ-DRH-007
    - REQ-DRH-008
    - REQ-DRH-009
    
**Purpose:** Provides UI for administrators to create, view, manage, and lift legal holds on specific platform data.  
**Logic Description:** Defines list and form views for the `influence_gen.legal_hold` model. Form view allows specifying target data and hold reason. Actions for 'Lift Hold'. Defines a window action for menu access.  
**Documentation:**
    
    - **Summary:** Interfaces for managing legal holds to preserve data as required.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** View
    
- **Path:** odoo_modules/influence_gen_admin/wizards/__init__.py  
**Description:** Initializes the Python wizards package.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** wizards/__init__.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Wizard Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Imports all wizard model files within this directory.  
**Logic Description:** Contains import statements for `broadcast_notification_wizard`, `kyc_request_info_wizard`, etc.  
**Documentation:**
    
    - **Summary:** Aggregates wizard model definitions.
    
**Namespace:** odoo.addons.influence_gen_admin.wizards  
**Metadata:**
    
    - **Category:** Wizard
    
- **Path:** odoo_modules/influence_gen_admin/wizards/broadcast_notification_wizard.py  
**Description:** Transient model for the broadcast notification wizard.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** BroadcastNotificationWizard  
**Type:** Wizard Model  
**Relative Path:** wizards/broadcast_notification_wizard.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** message_subject  
**Type:** fields.Char  
**Attributes:** string='Subject' required=True  
    - **Name:** message_body  
**Type:** fields.Html  
**Attributes:** string='Message Body' required=True  
    - **Name:** target_user_group_ids  
**Type:** fields.Many2many  
**Attributes:** comodel_name='res.groups' string='Target User Groups'  
    - **Name:** send_email  
**Type:** fields.Boolean  
**Attributes:** string='Send as Email' default=True  
    - **Name:** show_in_app_banner  
**Type:** fields.Boolean  
**Attributes:** string='Show In-App Banner'  
    
**Methods:**
    
    - **Name:** action_send_notification  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:**   
    
**Implemented Features:**
    
    - Broadcast Notification Logic
    
**Requirement Ids:**
    
    - REQ-16-012
    
**Purpose:** Defines the logic for administrators to compose and send broadcast notifications to user groups.  
**Logic Description:** Inherits from `models.TransientModel`. Defines fields for message subject, body, target groups, and notification channels. The `action_send_notification` method will handle the sending logic (e.g., creating mail messages or in-app notifications).  
**Documentation:**
    
    - **Summary:** Model for the wizard that allows administrators to send broadcast messages.
    
**Namespace:** odoo.addons.influence_gen_admin.wizards  
**Metadata:**
    
    - **Category:** Wizard
    
- **Path:** odoo_modules/influence_gen_admin/wizards/broadcast_notification_wizard_view.xml  
**Description:** XML view for the broadcast notification wizard.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** broadcast_notification_wizard_view  
**Type:** Wizard View  
**Relative Path:** wizards/broadcast_notification_wizard_view.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Broadcast Notification UI
    
**Requirement Ids:**
    
    - REQ-16-012
    
**Purpose:** Provides the UI for administrators to compose and send broadcast notifications.  
**Logic Description:** Defines a form view for the `influence_gen.broadcast_notification_wizard` model. Includes fields for subject, body, target groups, and send options. Buttons for 'Send Notification' and 'Cancel'. Defines an `ir.actions.act_window` to launch the wizard.  
**Documentation:**
    
    - **Summary:** Wizard interface for sending broadcast notifications to platform users.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Wizard
    
- **Path:** odoo_modules/influence_gen_admin/wizards/kyc_request_info_wizard.py  
**Description:** Transient model for requesting additional information during KYC review.  
**Template:** Odoo Python Model  
**Dependancy Level:** 1  
**Name:** KycRequestInfoWizard  
**Type:** Wizard Model  
**Relative Path:** wizards/kyc_request_info_wizard.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** kyc_submission_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='influence_gen.kyc_data' string='KYC Submission' readonly=True  
    - **Name:** message_to_influencer  
**Type:** fields.Text  
**Attributes:** string='Message to Influencer' required=True  
    
**Methods:**
    
    - **Name:** action_send_request  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:**   
    
**Implemented Features:**
    
    - KYC Additional Info Request Logic
    
**Requirement Ids:**
    
    - REQ-IOKYC-011
    
**Purpose:** Allows administrators to compose a message to an influencer requesting additional information for their KYC verification.  
**Logic Description:** Inherits from `models.TransientModel`. Stores a reference to the KYC submission and the message. `action_send_request` will update the KYC status to 'information_required', log the request, and trigger an email notification to the influencer.  
**Documentation:**
    
    - **Summary:** Wizard model for administrators to request further details for KYC processing.
    
**Namespace:** odoo.addons.influence_gen_admin.wizards  
**Metadata:**
    
    - **Category:** Wizard
    
- **Path:** odoo_modules/influence_gen_admin/wizards/kyc_request_info_wizard_view.xml  
**Description:** XML view for the KYC request additional information wizard.  
**Template:** Odoo XML View  
**Dependancy Level:** 2  
**Name:** kyc_request_info_wizard_view  
**Type:** Wizard View  
**Relative Path:** wizards/kyc_request_info_wizard_view.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - KYC Additional Info Request UI
    
**Requirement Ids:**
    
    - REQ-IOKYC-011
    
**Purpose:** UI for administrators to specify what additional information is needed from an influencer for KYC.  
**Logic Description:** Defines a form view for `influence_gen.kyc_request_info_wizard`. Includes a text field for the message and a button to send the request.  
**Documentation:**
    
    - **Summary:** Wizard interface for requesting additional KYC information from influencers.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Wizard
    
- **Path:** odoo_modules/influence_gen_admin/data/influence_gen_admin_groups_data.xml  
**Description:** Data file to initialize default security groups if not fully handled in security XML, or to assign users to default groups.  
**Template:** Odoo XML Data  
**Dependancy Level:** 3  
**Name:** influence_gen_admin_groups_data  
**Type:** Data  
**Relative Path:** data/influence_gen_admin_groups_data.xml  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default Group Initialization
    
**Requirement Ids:**
    
    - REQ-PAC-001
    
**Purpose:** Ensures the 'Platform Administrator' group exists and potentially assigns default Odoo admin user to it if appropriate for initial setup.  
**Logic Description:** XML file with `<record model="res.groups">` or `<function model="res.users" name="_add_influence_gen_admin_group_to_admin">` if programmatic assignment is needed. Generally, group definition is in security XML, so this might be for assigning users or category for menu.  
**Documentation:**
    
    - **Summary:** Initializes default data related to administrative security groups.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Data
    
- **Path:** odoo_modules/influence_gen_admin/controllers/__init__.py  
**Description:** Initializes the Python controllers package for the admin backend.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Init  
**Relative Path:** controllers/__init__.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Controller Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Imports controller files if any custom HTTP routes are defined for the admin backend.  
**Logic Description:** Contains import statements for any controller files, e.g., `import . import main`.  
**Documentation:**
    
    - **Summary:** Aggregates admin backend controller definitions.
    
**Namespace:** odoo.addons.influence_gen_admin.controllers  
**Metadata:**
    
    - **Category:** Controller
    
- **Path:** odoo_modules/influence_gen_admin/controllers/main.py  
**Description:** Main Python controller for custom admin backend HTTP routes, if needed (e.g., for complex dashboard data).  
**Template:** Odoo Python Controller  
**Dependancy Level:** 2  
**Name:** MainAdminController  
**Type:** Controller  
**Relative Path:** controllers/main.py  
**Repository Id:** REPO-IGAA-002  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_system_health_data  
**Parameters:**
    
    
**Return Type:** JsonRequest  
**Attributes:** http.route('/influence_gen/admin/system_health_data', type='json', auth='user', methods=['POST'])  
    
**Implemented Features:**
    
    - Custom Dashboard Data Endpoints
    
**Requirement Ids:**
    
    - REQ-PAC-014
    - REQ-12-007
    
**Purpose:** Provides custom JSON endpoints that might be called by admin dashboard views if the data required is too complex for simple model methods or computed fields.  
**Logic Description:** Inherits from `odoo.http.Controller`. Defines `@http.route` decorated methods to handle specific requests, for instance, fetching aggregated data for system health dashboards. Ensures proper authentication (`auth='user'`) and checks for admin privileges.  
**Documentation:**
    
    - **Summary:** Handles custom HTTP requests for the InfluenceGen admin backend, typically for data-intensive dashboard components.
    
**Namespace:** odoo.addons.influence_gen_admin.controllers  
**Metadata:**
    
    - **Category:** Controller
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableAdvancedAIMetricsDashboard
  - EnableAutomatedDataRetentionExecution
  - UseExternalSecretsVaultForAPIKeys
  
- **Database Configs:**
  
  


---

