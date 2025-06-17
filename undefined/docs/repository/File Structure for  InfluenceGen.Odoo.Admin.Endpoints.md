# Specification

# 1. Files

- **Path:** odoo_modules/influence_gen_admin/__init__.py  
**Description:** Initializes the Python package for the InfluenceGen Admin Odoo module, importing submodules like controllers, models (if any stubs/proxies were here, but typically models are in business layer), and wizards.  
**Template:** Odoo Python Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Python Module Init  
**Relative Path:** __init__.py  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes Python modules within this Odoo addon available for import.  
**Logic Description:** Contains import statements for Python files within the controllers and wizard directories.  
**Documentation:**
    
    - **Summary:** Standard Odoo module Python package initializer.
    
**Namespace:** odoo.addons.influence_gen_admin  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_admin/__manifest__.py  
**Description:** Odoo manifest file for the InfluenceGen Admin module. Defines module metadata, dependencies (e.g., on base Odoo apps, other InfluenceGen modules like core services), and data files (XML views, security rules, etc.).  
**Template:** Odoo Manifest  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    - Data File Loading
    
**Requirement Ids:**
    
    
**Purpose:** Declares the Odoo module, its properties, dependencies, and data files to be loaded.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'depends', 'data', 'installable', 'application'. 'depends' will list other Odoo modules this one relies on (e.g. 'mail', 'board', and the InfluenceGen core services module REPO-IGBS-003). 'data' will list all XML files for views, actions, menus, security, wizards, and initial data.  
**Documentation:**
    
    - **Summary:** Standard Odoo module manifest file.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_admin/security/influence_gen_security.xml  
**Description:** Defines custom security groups and access rules for the InfluenceGen Admin functionalities. This includes roles like 'InfluenceGen Platform Administrator' and potentially more granular admin roles. It uses Odoo's security group mechanism.  
**Template:** Odoo XML Security  
**Dependancy Level:** 1  
**Name:** influence_gen_security  
**Type:** XML  
**Relative Path:** security/influence_gen_security.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    - Configuration Management
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Role-Based Access Control Configuration
    
**Requirement Ids:**
    
    - REQ-PAC-001
    
**Purpose:** To define security groups and associate them with menus and actions within the InfluenceGen admin backend.  
**Logic Description:** Contains XML definitions for 'ir.model.category' to group InfluenceGen models, 'res.groups' to define security groups (e.g., 'group_influence_gen_admin'), and potentially 'ir.rule' for record-level security if needed beyond standard ACLs.  
**Documentation:**
    
    - **Summary:** Defines security groups for role-based access control in the InfluenceGen admin backend.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** odoo_modules/influence_gen_admin/security/ir.model.access.csv  
**Description:** CSV file defining model-level access control lists (ACLs) for all custom InfluenceGen models. Specifies read, write, create, and unlink permissions for different security groups (e.g., InfluenceGen Platform Administrator) on each model.  
**Template:** Odoo CSV ACL  
**Dependancy Level:** 1  
**Name:** ir.model.access  
**Type:** CSV  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Access Control
    
**Requirement Ids:**
    
    - REQ-PAC-001
    
**Purpose:** To control CRUD permissions for security groups on InfluenceGen custom Odoo models.  
**Logic Description:** A CSV file with columns: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. Each row defines permissions for a specific group on a specific model.  
**Documentation:**
    
    - **Summary:** Defines ACLs for all custom InfluenceGen models.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** odoo_modules/influence_gen_admin/views/influence_gen_admin_menus.xml  
**Description:** Defines the main menu structure for the InfluenceGen administrative backend within Odoo. Includes the root menu item for 'InfluenceGen Admin' and sub-menus for various management areas like Influencers, Campaigns, AI Settings, Payments, Configurations, Logs, etc.  
**Template:** Odoo XML Menu  
**Dependancy Level:** 2  
**Name:** influence_gen_admin_menus  
**Type:** XML  
**Relative Path:** views/influence_gen_admin_menus.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin Navigation Structure
    
**Requirement Ids:**
    
    - REQ-UIUX-003
    - REQ-UIUX-015
    - REQ-PAC-014
    
**Purpose:** To create an organized and efficient navigation structure for administrators.  
**Logic Description:** Contains 'menuitem' records defining the hierarchy of menus. Each menuitem will have an 'id', 'name', 'parent' (if submenu), 'action' (linking to an Odoo window action), and 'groups' (restricting visibility to specific security groups like 'group_influence_gen_admin').  
**Documentation:**
    
    - **Summary:** Defines the primary navigation menus for the InfluenceGen admin backend.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/influencer_profile_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for managing Influencer Profiles (`influence_gen.influencer_profile` model). Includes fields for KYC status, account status, and actions for admins to manage these.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** influencer_profile_admin_views  
**Type:** XML  
**Relative Path:** views/influencer_profile_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Influencer Profile Management UI (Admin)
    
**Requirement Ids:**
    
    - REQ-IOKYC-011
    
**Purpose:** To provide administrators with interfaces to view and manage influencer profiles, including their KYC and account status.  
**Logic Description:** Contains 'record' tags defining 'ir.ui.view' for form, tree, and search views of the 'influence_gen.influencer_profile' model. Includes fields like fullName, email, kycStatus, accountStatus, and buttons for administrative actions (e.g., 'Approve KYC', 'Reject KYC', 'Suspend Account'). Also defines an 'ir.actions.act_window' to link these views to a menu item.  
**Documentation:**
    
    - **Summary:** Admin views for managing influencer profiles.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/kyc_data_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for reviewing and managing KYC Data submissions (`influence_gen.kyc_data` model). Allows admins to view submitted documents, record verification decisions, and request additional information.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** kyc_data_admin_views  
**Type:** XML  
**Relative Path:** views/kyc_data_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - KYC Submission Review UI
    
**Requirement Ids:**
    
    - REQ-IOKYC-011
    
**Purpose:** To enable administrators to review KYC submissions, view documents, and manage verification status.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for 'influence_gen.kyc_data'. Form view will display document references (links or embedded previews if possible), verification status, reviewer fields, and buttons for 'Approve', 'Reject', 'Request More Info' (triggering wizards). Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for KYC data review and management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/campaign_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, kanban, search) for creating and managing Campaigns (`influence_gen.campaign` model). Includes fields for campaign details, budget, timelines, content requirements, etc.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** campaign_admin_views  
**Type:** XML  
**Relative Path:** views/campaign_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign Creation & Management UI
    
**Requirement Ids:**
    
    - REQ-2-001
    - REQ-2-002
    - REQ-2-003
    
**Purpose:** To allow administrators to create, configure, and manage the lifecycle of marketing campaigns.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, kanban, search) for 'influence_gen.campaign'. Form view will include all fields specified in requirements (name, description, brand, goals, target criteria, content requirements, budget, compensation, deadlines, usage rights, status). Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for campaign creation and lifecycle management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/campaign_application_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for reviewing and managing Influencer Applications to Campaigns (`influence_gen.campaign_application` model). Allows admins to approve or reject applications.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** campaign_application_admin_views  
**Type:** XML  
**Relative Path:** views/campaign_application_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign Application Review UI
    
**Requirement Ids:**
    
    - REQ-2-007
    
**Purpose:** To enable administrators to review influencer applications for campaigns and manage their status.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for 'influence_gen.campaign_application'. Form view will display applicant details, proposal, and buttons for 'Approve Application', 'Reject Application' (triggering wizard). Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for reviewing campaign applications.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/content_submission_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for reviewing and moderating Content Submissions from influencers (`influence_gen.content_submission` model). Allows admins to approve, reject, or request revisions.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** content_submission_admin_views  
**Type:** XML  
**Relative Path:** views/content_submission_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Content Submission Moderation UI
    
**Requirement Ids:**
    
    - REQ-2-010
    
**Purpose:** To allow administrators to review, provide feedback on, and approve/reject influencer content submissions.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for 'influence_gen.content_submission'. Form view will display submitted content (link/preview), feedback history, and buttons for 'Approve Content', 'Reject Content', 'Request Revision' (triggering wizard). Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for moderating campaign content submissions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/payment_record_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for overseeing Influencer Payment Records (`influence_gen.payment_record` model). Allows admins to track amounts owed, payment statuses, and potentially initiate payment batches (linking to Odoo accounting).  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** payment_record_admin_views  
**Type:** XML  
**Relative Path:** views/payment_record_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Influencer Payment Oversight UI
    
**Requirement Ids:**
    
    - REQ-PAC-015
    
**Purpose:** To provide administrators with tools to manage and track influencer payments.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for 'influence_gen.payment_record'. Views will display influencer, campaign, amount, status, transaction ID, and payment dates. Buttons for actions like 'Mark as Paid' (if manual update) or 'Generate Vendor Bill' (if integrating with Odoo accounting). Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for managing influencer payment records.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/audit_log_admin_views.xml  
**Description:** Defines Odoo backend views (tree/list, read-only form, search) for reviewing Audit Logs (`influence_gen.audit_log` model). Provides filtering, searching, and export capabilities.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** audit_log_admin_views  
**Type:** XML  
**Relative Path:** views/audit_log_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Review UI
    
**Requirement Ids:**
    
    - REQ-PAC-016
    - REQ-ATEL-008
    - REQ-UIUX-016
    
**Purpose:** To enable administrators to review system audit trails for compliance and investigation.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (tree, form - read-only, search) for 'influence_gen.audit_log'. Tree view will display key audit log fields (timestamp, user, action, target). Search view will allow filtering by these fields and keyword search in details. Form view for details. Defines an 'ir.actions.act_window'. Export functionality is standard in Odoo tree views.  
**Documentation:**
    
    - **Summary:** Admin views for reviewing audit logs.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/admin_dashboard_views.xml  
**Description:** Defines Odoo backend dashboard views for Platform Administrators. This includes a main admin dashboard, system health indicators, operational log summaries (if feasible to display from centralized logging), and campaign performance overviews.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** admin_dashboard_views  
**Type:** XML  
**Relative Path:** views/admin_dashboard_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin Dashboards (Main, Health, Ops, Campaign Performance)
    
**Requirement Ids:**
    
    - REQ-2-012
    - REQ-PAC-016
    - REQ-UIUX-019
    - REQ-12-007
    - REQ-PAC-014
    
**Purpose:** To provide administrators with at-a-glance views of key platform metrics and operational status.  
**Logic Description:** Contains 'record' tags defining 'ir.actions.act_window' for dashboards (e.g., type 'ir.actions.client' if using custom OWL components, or 'ir.ui.view' of type 'dashboard'). May involve QWeb templates if highly custom, or Odoo's standard dashboard elements. Data for these dashboards might be fetched by `dashboard_controller.py` and rendered by JS components.  
**Documentation:**
    
    - **Summary:** Defines various administrative dashboards.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/config_settings_views.xml  
**Description:** Defines Odoo backend views for managing InfluenceGen platform configurations using Odoo's `res.config.settings` mechanism. Covers general settings, KYC rules, AI configurations (linking to dedicated models), payment settings, logging/alerting, and ToS management.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** config_settings_views  
**Type:** XML  
**Relative Path:** views/config_settings_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    - Configuration Management
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Centralized Platform Configuration UI
    
**Requirement Ids:**
    
    - REQ-PAC-003
    - REQ-PAC-007
    - REQ-AIGS-002
    - REQ-AIGS-003
    - REQ-AIGS-004
    - REQ-PAC-005
    - REQ-PAC-006
    - REQ-PAC-004
    - REQ-PAC-009
    - REQ-PAC-010
    - REQ-PAC-011
    - REQ-PAC-015
    - REQ-PAC-017
    - REQ-UIUX-022
    
**Purpose:** To provide a unified interface for administrators to configure various aspects of the InfluenceGen platform.  
**Logic Description:** Contains 'record' tags defining an 'ir.ui.view' that inherits from 'res.config.settings.view.form'. Adds new sections and fields for InfluenceGen specific settings. Fields will correspond to `ir.config_parameter` entries or fields on a transient `res.config.settings` model that handles saving to `ir.config_parameter` or other specific setting models. Links to more complex CRUD views (e.g., AI Models, Alert Rules) will be provided.  
**Documentation:**
    
    - **Summary:** Centralized admin view for platform configuration settings.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/ai_model_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for managing AI Image Models (`influence_gen.ai_image_model` model), including their names, descriptions, and active status.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** ai_model_admin_views  
**Type:** XML  
**Relative Path:** views/ai_model_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Management UI
    
**Requirement Ids:**
    
    - REQ-AIGS-004
    - REQ-PAC-005
    
**Purpose:** To allow administrators to configure and manage the list of available AI image generation models.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for 'influence_gen.ai_image_model'. Includes fields for model name, description, trigger keywords, isActive, externalModelId. Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for managing AI image models.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/ai_prompt_template_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for managing AI Prompt Templates (`influence_gen.ai_prompt_template` model).  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** ai_prompt_template_admin_views  
**Type:** XML  
**Relative Path:** views/ai_prompt_template_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Prompt Template Management UI
    
**Requirement Ids:**
    
    - REQ-AIGS-003
    - REQ-PAC-005
    - REQ-UIUX-021
    
**Purpose:** To enable administrators to create and manage reusable prompt templates for AI image generation.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for a new model like 'influence_gen.ai_prompt_template'. Fields would include template name, prompt text, category/theme. Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for managing AI prompt templates.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/ai_moderation_rule_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for managing AI content moderation rules (`influence_gen.ai_moderation_rule` model), such as denylists for prompts.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** ai_moderation_rule_admin_views  
**Type:** XML  
**Relative Path:** views/ai_moderation_rule_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Prompt Moderation Rule UI
    
**Requirement Ids:**
    
    - REQ-AIGS-003
    - REQ-PAC-009
    
**Purpose:** To allow administrators to configure rules for moderating AI image generation prompts.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for a new model like 'influence_gen.ai_moderation_rule'. Fields would include rule type (e.g., 'denylist_keyword'), rule value, description. Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for managing AI prompt moderation rules.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/data_retention_policy_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for managing Data Retention Policies (`influence_gen.data_retention_policy` model). Allows admins to define retention periods for different data categories.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** data_retention_policy_admin_views  
**Type:** XML  
**Relative Path:** views/data_retention_policy_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Data Retention Policy Management UI
    
**Requirement Ids:**
    
    - REQ-DRH-008
    
**Purpose:** To enable administrators to configure data retention policies for various data types.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for a new model like 'influence_gen.data_retention_policy'. Fields include data category, retention period (e.g., in days/months/years), action upon expiry (delete/anonymize/archive). Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for managing data retention policies.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/legal_hold_admin_views.xml  
**Description:** Defines Odoo backend views for managing Legal Holds. This might involve extending existing model views (e.g., Influencer Profile, Campaign) with legal hold status fields and actions, or a dedicated view if legal holds are managed as separate entities.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** legal_hold_admin_views  
**Type:** XML  
**Relative Path:** views/legal_hold_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Legal Hold Management UI
    
**Requirement Ids:**
    
    - REQ-DRH-008
    - REQ-DRH-009
    
**Purpose:** To allow authorized administrators to place, manage, and lift legal holds on specific data.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view'. If legal hold is a field on multiple models, this file might contain XML snippets to be inherited into those models' views. If a dedicated 'influence_gen.legal_hold' model exists, this file defines views for it. Includes fields for hold reason, scope, status, dates, and user placing/lifting the hold. Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for managing legal holds on data.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/alert_rule_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for managing system Alert Rules (`influence_gen.alert_rule` model). Allows admins to configure conditions for triggering alerts, severity, and notification channels/recipients.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** alert_rule_admin_views  
**Type:** XML  
**Relative Path:** views/alert_rule_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - System Alert Rule Configuration UI
    
**Requirement Ids:**
    
    - REQ-PAC-011
    
**Purpose:** To enable administrators to define rules for system alerts based on events or thresholds.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for a new model like 'influence_gen.alert_rule'. Fields include rule name, monitored metric/event, condition, threshold, severity, notification channels (e.g., email groups, webhook URL), recipients. Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for configuring system alert rules.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/maintenance_window_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, calendar, search) for managing scheduled Maintenance Windows (`influence_gen.maintenance_window` model).  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** maintenance_window_admin_views  
**Type:** XML  
**Relative Path:** views/maintenance_window_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Maintenance Window Management UI
    
**Requirement Ids:**
    
    - REQ-PAC-012
    
**Purpose:** To allow administrators to schedule and communicate planned system maintenance.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, calendar, search) for a new model like 'influence_gen.maintenance_window'. Fields include start/end datetime, reason, communication message, affected services. Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for managing scheduled maintenance windows.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/tos_management_admin_views.xml  
**Description:** Defines Odoo backend views (form, tree/list, search) for managing versions of Terms of Service and Privacy Policy documents (`influence_gen.terms_version` model).  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** tos_management_admin_views  
**Type:** XML  
**Relative Path:** views/tos_management_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - ToS/Privacy Policy Version Management UI
    
**Requirement Ids:**
    
    - REQ-PAC-006
    
**Purpose:** To enable administrators to upload, manage, and version control legal documents like ToS and Privacy Policy.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form, tree, search) for a new model like 'influence_gen.terms_version'. Fields include document type (ToS/PrivacyPolicy), version_number, effective_date, content (HTML/Text or attachment), isActive flag. Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for managing ToS and Privacy Policy versions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/views/ai_usage_log_admin_views.xml  
**Description:** Defines Odoo backend views (tree/list, read-only form, search, graph) for viewing AI Image Generation Usage Logs (`influence_gen.usage_tracking_log` model). This supports REQ-AIGS-007.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** ai_usage_log_admin_views  
**Type:** XML  
**Relative Path:** views/ai_usage_log_admin_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Usage Log Viewing UI
    
**Requirement Ids:**
    
    - REQ-AIGS-007
    
**Purpose:** To allow administrators to view and analyze AI image generation usage metrics.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (tree, form - read-only, search, graph) for 'influence_gen.usage_tracking_log'. Views will display user, campaign, timestamp, model used, images generated, API calls. Search view for filtering. Graph view for basic analytics. Defines an 'ir.actions.act_window'.  
**Documentation:**
    
    - **Summary:** Admin views for AI image generation usage logs.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/controllers/__init__.py  
**Description:** Initializes the Python package for controllers within the InfluenceGen Admin module.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Module Init  
**Relative Path:** controllers/__init__.py  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes controller classes available for import by Odoo.  
**Logic Description:** Contains import statements for controller files like `dashboard_controller.py`.  
**Documentation:**
    
    - **Summary:** Initializes the controllers submodule.
    
**Namespace:** odoo.addons.influence_gen_admin.controllers  
**Metadata:**
    
    - **Category:** Controller
    
- **Path:** odoo_modules/influence_gen_admin/controllers/dashboard_controller.py  
**Description:** Python controller for handling HTTP requests related to custom administrative dashboards. Fetches and processes data to be displayed on dashboards if standard Odoo views are insufficient.  
**Template:** Odoo Python Controller  
**Dependancy Level:** 2  
**Name:** dashboard_controller  
**Type:** Controller  
**Relative Path:** controllers/dashboard_controller.py  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_system_health_data  
**Parameters:**
    
    - **kw
    
**Return Type:** dict  
**Attributes:** json  
    - **Name:** get_campaign_performance_summary  
**Parameters:**
    
    - **kw
    
**Return Type:** dict  
**Attributes:** json  
    - **Name:** get_operational_log_summary  
**Parameters:**
    
    - **kw
    
**Return Type:** dict  
**Attributes:** json  
    
**Implemented Features:**
    
    - Admin Dashboard Data Provisioning
    
**Requirement Ids:**
    
    - REQ-2-012
    - REQ-PAC-016
    - REQ-12-007
    
**Purpose:** To provide backend data for rich, interactive administrative dashboards.  
**Logic Description:** Defines HTTP routes (e.g., using `@http.route`) that are called by JavaScript (OWL components) in custom dashboard views. Methods query relevant Odoo models (from Business Services layer) to aggregate data for system health, campaign performance, operational log insights, etc., and return it as JSON.  
**Documentation:**
    
    - **Summary:** Controller for custom admin dashboard data.
    
**Namespace:** odoo.addons.influence_gen_admin.controllers.dashboard_controller  
**Metadata:**
    
    - **Category:** Controller
    
- **Path:** odoo_modules/influence_gen_admin/wizard/__init__.py  
**Description:** Initializes the Python package for wizards within the InfluenceGen Admin module.  
**Template:** Odoo Python Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Module Init  
**Relative Path:** wizard/__init__.py  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Makes wizard model classes available for import by Odoo.  
**Logic Description:** Contains import statements for wizard Python files like `kyc_management_wizards.py`.  
**Documentation:**
    
    - **Summary:** Initializes the wizards submodule.
    
**Namespace:** odoo.addons.influence_gen_admin.wizard  
**Metadata:**
    
    - **Category:** Wizard
    
- **Path:** odoo_modules/influence_gen_admin/wizard/kyc_management_wizards.py  
**Description:** Python logic for KYC management wizards, such as rejecting KYC submissions with a reason, or requesting additional information from influencers.  
**Template:** Odoo Python Wizard  
**Dependancy Level:** 2  
**Name:** kyc_management_wizards  
**Type:** Wizard Model  
**Relative Path:** wizard/kyc_management_wizards.py  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    - **Name:** rejection_reason  
**Type:** fields.Text  
**Attributes:**   
    - **Name:** additional_info_request  
**Type:** fields.Text  
**Attributes:**   
    
**Methods:**
    
    - **Name:** action_confirm_rejection  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** action_send_info_request  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - KYC Rejection Wizard Logic
    - KYC Request Info Wizard Logic
    
**Requirement Ids:**
    
    - REQ-IOKYC-011
    
**Purpose:** To handle multi-step or modal dialog based administrative actions for KYC management.  
**Logic Description:** Defines transient models (`models.TransientModel`) for KYC wizards. `KycRejectionWizard` has a field for rejection reason and a method to update the KYCData record and send notification. `KycRequestInfoWizard` has a field for the information request message and a method to update KYCData and notify the influencer.  
**Documentation:**
    
    - **Summary:** Implements wizard logic for KYC rejection and requesting additional information.
    
**Namespace:** odoo.addons.influence_gen_admin.wizard.kyc_management_wizards  
**Metadata:**
    
    - **Category:** Wizard
    
- **Path:** odoo_modules/influence_gen_admin/wizard/kyc_management_wizard_views.xml  
**Description:** XML views for KYC management wizards, defining the UI (forms) for these modal dialogs.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** kyc_management_wizard_views  
**Type:** XML  
**Relative Path:** wizard/kyc_management_wizard_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - KYC Rejection Wizard UI
    - KYC Request Info Wizard UI
    
**Requirement Ids:**
    
    - REQ-IOKYC-011
    
**Purpose:** To define the user interface for KYC management wizards.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form type) for the transient models defined in `kyc_management_wizards.py`. Includes fields for inputting rejection reasons or information requests, and buttons to confirm/cancel.  
**Documentation:**
    
    - **Summary:** XML views for KYC management wizards.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/wizard/campaign_management_wizards.py  
**Description:** Python logic for Campaign and Content management wizards, such as rejecting campaign applications or requesting content revisions.  
**Template:** Odoo Python Wizard  
**Dependancy Level:** 2  
**Name:** campaign_management_wizards  
**Type:** Wizard Model  
**Relative Path:** wizard/campaign_management_wizards.py  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    - **Name:** application_rejection_reason  
**Type:** fields.Text  
**Attributes:**   
    - **Name:** content_revision_feedback  
**Type:** fields.Text  
**Attributes:**   
    
**Methods:**
    
    - **Name:** action_confirm_application_rejection  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** action_request_content_revision  
**Parameters:**
    
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Campaign Application Rejection Wizard Logic
    - Content Revision Request Wizard Logic
    
**Requirement Ids:**
    
    - REQ-2-007
    - REQ-2-008
    - REQ-2-010
    
**Purpose:** To handle modal dialog based administrative actions for campaign and content management.  
**Logic Description:** Defines transient models for campaign related wizards. `CampaignApplicationRejectionWizard` for application rejection. `ContentRevisionWizard` for requesting content revisions. Methods update relevant records and trigger notifications (REQ-2-008).  
**Documentation:**
    
    - **Summary:** Implements wizard logic for campaign application rejection and content revision requests.
    
**Namespace:** odoo.addons.influence_gen_admin.wizard.campaign_management_wizards  
**Metadata:**
    
    - **Category:** Wizard
    
- **Path:** odoo_modules/influence_gen_admin/wizard/campaign_management_wizard_views.xml  
**Description:** XML views for Campaign and Content management wizards.  
**Template:** Odoo XML View  
**Dependancy Level:** 3  
**Name:** campaign_management_wizard_views  
**Type:** XML  
**Relative Path:** wizard/campaign_management_wizard_views.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign Application Rejection Wizard UI
    - Content Revision Request Wizard UI
    
**Requirement Ids:**
    
    - REQ-2-007
    - REQ-2-010
    
**Purpose:** To define the user interface for campaign and content management wizards.  
**Logic Description:** Contains 'record' tags for 'ir.ui.view' (form type) for the transient models in `campaign_management_wizards.py`. UI for inputting rejection reasons or revision feedback.  
**Documentation:**
    
    - **Summary:** XML views for campaign and content management wizards.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/static/src/js/custom_admin_dashboard.js  
**Description:** JavaScript (OWL components) for rendering and managing custom administrative dashboards if they require dynamic client-side interactions beyond standard Odoo dashboard capabilities.  
**Template:** Odoo OWL Component  
**Dependancy Level:** 4  
**Name:** custom_admin_dashboard  
**Type:** JavaScript  
**Relative Path:** static/src/js/custom_admin_dashboard.js  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Model-View-Controller (MVC) / Model-Template-View (MTV)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Dynamic Admin Dashboard Rendering
    
**Requirement Ids:**
    
    - REQ-2-012
    - REQ-PAC-016
    - REQ-UIUX-019
    - REQ-12-007
    
**Purpose:** To provide rich, interactive dashboard experiences for administrators.  
**Logic Description:** Defines OWL components that fetch data from `dashboard_controller.py` (or other sources) and render charts, graphs, and key metrics for system health, campaign performance, operational log summaries. These components would be embedded in XML views of type 'qweb' or client actions.  
**Documentation:**
    
    - **Summary:** OWL components for custom administrative dashboards.
    
**Namespace:** odoo.addons.influence_gen_admin.static.src.js  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/static/src/css/admin_backend_styles.css  
**Description:** Custom CSS/SCSS styles for the InfluenceGen administrative backend, if specific styling beyond standard Odoo themes is required for branding or improved UX.  
**Template:** CSS/SCSS  
**Dependancy Level:** 1  
**Name:** admin_backend_styles  
**Type:** CSS  
**Relative Path:** static/src/css/admin_backend_styles.css  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Admin UI Styling
    
**Requirement Ids:**
    
    - REQ-UIUX-003
    
**Purpose:** To apply custom visual styles to the InfluenceGen admin interface.  
**Logic Description:** Contains CSS rules to customize the appearance of InfluenceGen specific views, dashboards, or elements in the Odoo backend. To be included in the module's assets.  
**Documentation:**
    
    - **Summary:** Custom styles for the admin backend UI.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_admin/data/initial_config_data.xml  
**Description:** XML data file for loading initial or default configurations, such as default admin roles specific to InfluenceGen, pre-defined email templates (if not using Odoo's standard ones directly), or default platform settings.  
**Template:** Odoo XML Data  
**Dependancy Level:** 2  
**Name:** initial_config_data  
**Type:** XML  
**Relative Path:** data/initial_config_data.xml  
**Repository Id:** REPO-IGOA-002  
**Pattern Ids:**
    
    - Configuration Management
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default Configuration Loading
    
**Requirement Ids:**
    
    - REQ-PAC-001
    - REQ-PAC-010
    
**Purpose:** To set up initial system parameters and default data upon module installation.  
**Logic Description:** Contains 'record' tags to create initial instances of models like 'res.groups' (for InfluenceGen Admin group), 'mail.template' (for specific notifications REQ-2-008), or 'ir.config_parameter' for default settings. This file is listed in the '__manifest__.py' 'data' section.  
**Documentation:**
    
    - **Summary:** Provides initial data and default configurations for the admin module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Data
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableAdvancedAIDashboard
  - EnableCustomAlertRouting
  
- **Database Configs:**
  
  


---

