# Specification

# 1. Files

- **Path:** odoo_modules/influence_gen_services/__init__.py  
**Description:** Initializes the Python package for the InfluenceGen Services Odoo module, importing submodules like models, services, and wizards.  
**Template:** Odoo Module __init__.py  
**Dependancy Level:** 3  
**Name:** __init__  
**Type:** Python Package Initializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** To make models, services, and wizards available when the Odoo module is loaded.  
**Logic Description:** Import sub-packages: models, services, wizards. Example: from . import models; from . import services  
**Documentation:**
    
    - **Summary:** Main initializer for the influence_gen_services Odoo module.
    
**Namespace:** odoo.addons.influence_gen_services  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_services/__manifest__.py  
**Description:** Odoo manifest file for the InfluenceGen Services module. Defines module metadata, dependencies, and data files.  
**Template:** Odoo Module __manifest__.py  
**Dependancy Level:** 4  
**Name:** __manifest__  
**Type:** Odoo Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    - Data File Loading
    
**Requirement Ids:**
    
    
**Purpose:** To declare the InfluenceGen Services module to Odoo, specify its properties, dependencies, and data to be loaded.  
**Logic Description:** Define module attributes like name, version, summary, author, category, dependencies (e.g., 'base', 'mail', 'account', 'iap'), and data files (security, views, demo data, initial data). Explicitly list all XML data files from 'security/' and 'data/' directories. List Python files for models and services in a way that Odoo discovers them (implicitly through __init__.py).  
**Documentation:**
    
    - **Summary:** Manifest file for the InfluenceGen Services module, detailing its integration with the Odoo framework.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_services/models/__init__.py  
**Description:** Initializes the Python package for Odoo models within the InfluenceGen Services module.  
**Template:** Odoo Models __init__.py  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** Python Package Initializer  
**Relative Path:** models/__init__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Discovery
    
**Requirement Ids:**
    
    
**Purpose:** To make all model files in the 'models' directory discoverable by Odoo.  
**Logic Description:** Import all Python files defined in the 'models' directory. Example: from . import influencer_profile; from . import campaign; ...  
**Documentation:**
    
    - **Summary:** Initializer for the data models of the InfluenceGen Services module.
    
**Namespace:** odoo.addons.influence_gen_services.models  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_services/models/base_audit_mixin.py  
**Description:** Odoo model mixin to provide common audit logging capabilities for other models.  
**Template:** Odoo Model Mixin  
**Dependancy Level:** 0  
**Name:** BaseAuditMixin  
**Type:** Odoo Model Mixin  
**Relative Path:** models/base_audit_mixin.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Mixin Pattern
    - Audit Logging
    
**Members:**
    
    
**Methods:**
    
    - **Name:** _log_audit_event  
**Parameters:**
    
    - self
    - action
    - target_entity_name=None
    - target_id=None
    - details=None
    
**Return Type:** void  
**Attributes:** protected  
    - **Name:** create  
**Parameters:**
    
    - self
    - vals_list
    
**Return Type:** recordset  
**Attributes:** public  
    - **Name:** write  
**Parameters:**
    
    - self
    - vals
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** unlink  
**Parameters:**
    
    - self
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - Automated Audit Logging for CRUD
    
**Requirement Ids:**
    
    - REQ-ATEL-005
    - REQ-ATEL-006
    
**Purpose:** To provide a reusable way to log create, write, and unlink operations on models that inherit this mixin, creating entries in the AuditLog model.  
**Logic Description:** Inherit from `models.AbstractModel`. Override `create`, `write`, and `unlink` methods to call `_log_audit_event` before or after super call. `_log_audit_event` will use `self.env['influence_gen.audit_log']` to create log entries. Capture old and new values in `write` if feasible and non-sensitive. Determine `target_entity_name` from `self._name` and `target_id` from `self.id`.  
**Documentation:**
    
    - **Summary:** Provides base audit logging functionality for key Odoo models within InfluenceGen.
    
**Namespace:** odoo.addons.influence_gen_services.models.base_audit_mixin  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/influencer_profile.py  
**Description:** Odoo model for Influencer Profile, storing personal, contact, professional information, KYC status, and consent records. Links to `res.users`.  
**Template:** Odoo Model  
**Dependancy Level:** 1  
**Name:** InfluencerProfile  
**Type:** Odoo Model  
**Relative Path:** models/influencer_profile.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _inherit  
**Type:** list  
**Attributes:** protected|static  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** full_name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** email  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** phone  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** residential_address  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** social_media_profile_ids  
**Type:** fields.One2many  
**Attributes:** public  
    - **Name:** area_of_influence_ids  
**Type:** fields.Many2many  
**Attributes:** public  
    - **Name:** audience_demographics  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** kyc_status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** kyc_data_ids  
**Type:** fields.One2many  
**Attributes:** public  
    - **Name:** bank_account_ids  
**Type:** fields.One2many  
**Attributes:** public  
    - **Name:** terms_consent_ids  
**Type:** fields.One2many  
**Attributes:** public  
    - **Name:** account_status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** activation_date  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** is_gdpr_erasure_requested  
**Type:** fields.Boolean  
**Attributes:** public  
    - **Name:** legal_hold_status  
**Type:** fields.Boolean  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** _sql_constraints_email_unique  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** protected  
    - **Name:** action_activate_account  
**Parameters:**
    
    - self
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** action_deactivate_account  
**Parameters:**
    
    - self
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** action_request_data_erasure  
**Parameters:**
    
    - self
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** get_latest_consent  
**Parameters:**
    
    - self
    
**Return Type:** recordset  
**Attributes:** public  
    - **Name:** update_kyc_status  
**Parameters:**
    
    - self
    - new_status
    - reviewer_id=None
    - notes=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** check_onboarding_completion  
**Parameters:**
    
    - self
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - Influencer Data Management
    - KYC Status Tracking
    - Account Activation
    - Consent Management
    
**Requirement Ids:**
    
    - REQ-DMG-002
    - REQ-IOKYC-002
    - REQ-IOKYC-009
    - REQ-IOKYC-012
    - REQ-IOKYC-014
    - REQ-IOKYC-016
    - REQ-DMG-020
    - REQ-DMG-021
    
**Purpose:** To define the data structure and business logic for influencer profiles, managing their lifecycle from registration to active participation.  
**Logic Description:** Define fields as per REQ-DMG-002. Implement SQL constraint for unique email. Methods for account activation/deactivation. Manage `kyc_status` and `account_status` based on related data (KYC, bank verification, consent). `_inherit` `mail.thread` and `mail.activity.mixin` for communication and tracking, and `BaseAuditMixin`. `audience_demographics` can be a JSON stored as Text or Odoo's `fields.Json`. Implement `check_onboarding_completion` to verify all necessary steps are done for activation.  
**Documentation:**
    
    - **Summary:** Represents an influencer on the platform, centralizing their personal, professional, and platform-specific data.
    
**Namespace:** odoo.addons.influence_gen_services.models.influencer_profile  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/area_of_influence.py  
**Description:** Odoo model for Areas of Influence (Niche categories).  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** AreaOfInfluence  
**Type:** Odoo Model  
**Relative Path:** models/area_of_influence.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** influencer_profile_ids  
**Type:** fields.Many2many  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** _sql_constraints_name_unique  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** protected  
    
**Implemented Features:**
    
    - Niche Management
    
**Requirement Ids:**
    
    - REQ-DMG-002
    
**Purpose:** To define and manage distinct areas of influence or niches that influencers can be associated with.  
**Logic Description:** Simple model with a unique name for each area of influence. Used in a Many2many relationship with InfluencerProfile. Inherit from `BaseAuditMixin`.  
**Documentation:**
    
    - **Summary:** Represents a category or niche of influence (e.g., Fashion, Gaming).
    
**Namespace:** odoo.addons.influence_gen_services.models.area_of_influence  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/social_media_profile.py  
**Description:** Odoo model for Influencer Social Media Profiles, including verification status.  
**Template:** Odoo Model  
**Dependancy Level:** 1  
**Name:** SocialMediaProfile  
**Type:** Odoo Model  
**Relative Path:** models/social_media_profile.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** influencer_profile_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** platform  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** handle  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** url  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** verification_status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** verification_method  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** verification_code  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** verified_at  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** audience_metrics_json  
**Type:** fields.Text  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** _sql_constraints_platform_handle_influencer_unique  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** protected  
    - **Name:** _check_url_format  
**Parameters:**
    
    - self
    
**Return Type:** None  
**Attributes:** protected|api.constrains  
    - **Name:** action_start_verification  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_confirm_verification  
**Parameters:**
    
    - self
    - input_code=None
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - Social Media Profile Management
    - Ownership Verification
    
**Requirement Ids:**
    
    - REQ-DMG-002
    - REQ-IOKYC-002
    - REQ-IOKYC-003
    - REQ-IOKYC-006
    - REQ-IOKYC-014
    
**Purpose:** To store and manage influencer social media profiles, including their verification status and methods.  
**Logic Description:** Fields for platform, handle, URL, verification status, method, etc. SQL constraint for unique handle per platform per influencer. Python constraint for URL format validation. Methods to initiate and confirm verification (e.g., generate code, check OAuth). Inherit from `BaseAuditMixin`.  
**Documentation:**
    
    - **Summary:** Represents an influencer's social media account on a specific platform.
    
**Namespace:** odoo.addons.influence_gen_services.models.social_media_profile  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/kyc_data.py  
**Description:** Odoo model for storing KYC verification data and document references.  
**Template:** Odoo Model  
**Dependancy Level:** 1  
**Name:** KycData  
**Type:** Odoo Model  
**Relative Path:** models/kyc_data.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** influencer_profile_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** document_type  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** document_front_attachment_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** document_back_attachment_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** verification_method  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** verification_status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** reviewer_user_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** reviewed_at  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** notes  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** external_verification_id  
**Type:** fields.Char  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** action_approve  
**Parameters:**
    
    - self
    - reviewer_id
    - notes=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_reject  
**Parameters:**
    
    - self
    - reviewer_id
    - reason
    - notes=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_request_more_info  
**Parameters:**
    
    - self
    - reviewer_id
    - required_info
    - notes=None
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - KYC Document Management
    - KYC Verification Workflow
    
**Requirement Ids:**
    
    - REQ-DMG-003
    - REQ-IOKYC-005
    - REQ-IOKYC-011
    - REQ-IOKYC-016
    
**Purpose:** To manage the KYC data submissions, their verification status, and link to uploaded documents.  
**Logic Description:** Fields for document type, references to `ir.attachment` for document storage, verification status, reviewer, notes. Methods to manage the review workflow (approve, reject, request more info). Update `influencer_profile_id.kyc_status` upon status change. Inherit `mail.thread` and `BaseAuditMixin`.  
**Documentation:**
    
    - **Summary:** Stores information related to a single KYC verification attempt for an influencer.
    
**Namespace:** odoo.addons.influence_gen_services.models.kyc_data  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/bank_account.py  
**Description:** Odoo model for Influencer Bank Account details, including verification.  
**Template:** Odoo Model  
**Dependancy Level:** 1  
**Name:** BankAccount  
**Type:** Odoo Model  
**Relative Path:** models/bank_account.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** influencer_profile_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** account_holder_name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** account_number_encrypted  
**Type:** fields.Binary  
**Attributes:** public  
    - **Name:** bank_name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** routing_number_encrypted  
**Type:** fields.Binary  
**Attributes:** public  
    - **Name:** iban_encrypted  
**Type:** fields.Binary  
**Attributes:** public  
    - **Name:** swift_code_encrypted  
**Type:** fields.Binary  
**Attributes:** public  
    - **Name:** verification_status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** verification_method  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** is_primary  
**Type:** fields.Boolean  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** action_verify_manually  
**Parameters:**
    
    - self
    - reviewer_id
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_initiate_micro_deposit  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_confirm_micro_deposit  
**Parameters:**
    
    - self
    - amount1
    - amount2
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** get_decrypted_account_number  
**Parameters:**
    
    - self
    
**Return Type:** str  
**Attributes:** public  
    
**Implemented Features:**
    
    - Bank Account Management
    - Bank Account Verification
    
**Requirement Ids:**
    
    - REQ-DMG-002
    - REQ-IPF-001
    - REQ-IPF-002
    - REQ-IOKYC-007
    - REQ-IOKYC-008
    - REQ-IPF-011
    
**Purpose:** To securely store and manage influencer bank account details and their verification status.  
**Logic Description:** Fields for account holder name, encrypted bank details (use Odoo's encryption capabilities or custom if stronger needed), verification status. Methods for different verification processes. Ensure only one primary account per influencer. Inherit `mail.thread` and `BaseAuditMixin`. Implement compute/inverse fields for displaying masked numbers while storing encrypted values.  
**Documentation:**
    
    - **Summary:** Represents an influencer's bank account for receiving payouts.
    
**Namespace:** odoo.addons.influence_gen_services.models.bank_account  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/terms_consent.py  
**Description:** Odoo model for recording influencer consent to Terms of Service and Privacy Policy versions.  
**Template:** Odoo Model  
**Dependancy Level:** 1  
**Name:** TermsConsent  
**Type:** Odoo Model  
**Relative Path:** models/terms_consent.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** influencer_profile_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** tos_version  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** privacy_policy_version  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** consent_date  
**Type:** fields.Datetime  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Consent Logging
    
**Requirement Ids:**
    
    - REQ-DMG-002
    - REQ-IOKYC-009
    - REQ-ATEL-005
    
**Purpose:** To log each instance of an influencer providing consent to specific versions of legal documents.  
**Logic Description:** Stores influencer, document versions (ToS, Privacy Policy), and timestamp of consent. Inherit from `BaseAuditMixin` for create events.  
**Documentation:**
    
    - **Summary:** Records an influencer's agreement to a specific version of Terms of Service and Privacy Policy.
    
**Namespace:** odoo.addons.influence_gen_services.models.terms_consent  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/campaign.py  
**Description:** Odoo model for Marketing Campaigns.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** Campaign  
**Type:** Odoo Model  
**Relative Path:** models/campaign.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** brand_client  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** goals  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** kpi_ids  
**Type:** fields.One2many  
**Attributes:** public  
    - **Name:** target_criteria_json  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** content_requirements  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** budget  
**Type:** fields.Monetary  
**Attributes:** public  
    - **Name:** currency_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** compensation_model_type  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** compensation_details  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** submission_deadline  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** start_date  
**Type:** fields.Date  
**Attributes:** public  
    - **Name:** end_date  
**Type:** fields.Date  
**Attributes:** public  
    - **Name:** usage_rights  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** campaign_application_ids  
**Type:** fields.One2many  
**Attributes:** public  
    - **Name:** payment_record_ids  
**Type:** fields.One2many  
**Attributes:** public  
    - **Name:** active  
**Type:** fields.Boolean  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** _sql_constraints_name_unique  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** protected  
    - **Name:** _check_dates  
**Parameters:**
    
    - self
    
**Return Type:** None  
**Attributes:** protected|api.constrains  
    - **Name:** action_publish  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_start_progress  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_complete  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_archive  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** calculate_aggregated_kpis  
**Parameters:**
    
    - self
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Campaign Creation
    - Lifecycle Management
    - Budgeting
    - Compensation Models
    
**Requirement Ids:**
    
    - REQ-DMG-004
    - REQ-2-001
    - REQ-2-002
    - REQ-2-003
    - REQ-2-017
    - REQ-IPF-003
    
**Purpose:** To define and manage marketing campaigns, including their details, lifecycle, and associated data.  
**Logic Description:** Fields for all campaign attributes. `_inherit` `mail.thread` and `BaseAuditMixin`. Implement status transitions (draft, published, in_progress, completed, archived). Validate dates (end_date > start_date). KPI definition might be a separate related model (`campaign.kpi`) with `kpi_ids` as O2M. `target_criteria_json` for flexible targeting. `compensation_model_type` (selection) and `compensation_details` (Text/JSON) for flexibility.  
**Documentation:**
    
    - **Summary:** Represents a marketing campaign with all its defining characteristics and operational status.
    
**Namespace:** odoo.addons.influence_gen_services.models.campaign  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/campaign_kpi.py  
**Description:** Odoo model for defining Key Performance Indicators (KPIs) for a campaign.  
**Template:** Odoo Model  
**Dependancy Level:** 1  
**Name:** CampaignKpi  
**Type:** Odoo Model  
**Relative Path:** models/campaign_kpi.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** campaign_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** target_value  
**Type:** fields.Float  
**Attributes:** public  
    - **Name:** actual_value  
**Type:** fields.Float  
**Attributes:** public  
    - **Name:** unit_of_measure  
**Type:** fields.Char  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign KPI Tracking
    
**Requirement Ids:**
    
    - REQ-DMG-004
    - REQ-2-001
    
**Purpose:** To store and track specific KPIs associated with a marketing campaign.  
**Logic Description:** Defines individual KPIs for a campaign, including name, target value, actual value (can be computed or manually entered), and unit. This model is linked to the Campaign model via a Many2one relationship (or One2many from Campaign).  
**Documentation:**
    
    - **Summary:** Represents a specific Key Performance Indicator for a campaign.
    
**Namespace:** odoo.addons.influence_gen_services.models.campaign_kpi  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/campaign_application.py  
**Description:** Odoo model for Influencer Applications to Campaigns.  
**Template:** Odoo Model  
**Dependancy Level:** 2  
**Name:** CampaignApplication  
**Type:** Odoo Model  
**Relative Path:** models/campaign_application.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** campaign_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** influencer_profile_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** proposal  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** submitted_at  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** reviewed_at  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** reviewer_user_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** rejection_reason  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** content_submission_ids  
**Type:** fields.One2many  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** _sql_constraints_campaign_influencer_unique  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** protected  
    - **Name:** action_approve_application  
**Parameters:**
    
    - self
    - reviewer_id
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_reject_application  
**Parameters:**
    
    - self
    - reviewer_id
    - reason=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_withdraw_application  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Campaign Application Management
    - Application Review Workflow
    
**Requirement Ids:**
    
    - REQ-DMG-005
    - REQ-2-007
    - REQ-2-018
    
**Purpose:** To manage influencer applications for campaigns and their review process.  
**Logic Description:** Links Campaign and InfluencerProfile. Fields for proposal, status, timestamps. Methods for application status changes. Inherit `mail.thread` and `BaseAuditMixin`.  
**Documentation:**
    
    - **Summary:** Represents an influencer's application to participate in a specific campaign.
    
**Namespace:** odoo.addons.influence_gen_services.models.campaign_application  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/content_submission.py  
**Description:** Odoo model for Content Submissions by influencers for campaigns.  
**Template:** Odoo Model  
**Dependancy Level:** 3  
**Name:** ContentSubmission  
**Type:** Odoo Model  
**Relative Path:** models/content_submission.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** campaign_application_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** campaign_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** influencer_profile_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** generated_image_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** content_url  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** content_attachment_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** file_type  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** submission_date  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** review_status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** feedback_history_ids  
**Type:** fields.One2many  
**Attributes:** public  
    - **Name:** reviewed_by_user_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** reviewed_at  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** version  
**Type:** fields.Integer  
**Attributes:** public  
    - **Name:** performance_data_json  
**Type:** fields.Text  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** action_approve_content  
**Parameters:**
    
    - self
    - reviewer_id
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_reject_content  
**Parameters:**
    
    - self
    - reviewer_id
    - feedback_text
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_request_revision  
**Parameters:**
    
    - self
    - reviewer_id
    - feedback_text
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** submit_new_version  
**Parameters:**
    
    - self
    - new_attachment_id=None
    - new_url=None
    
**Return Type:** recordset  
**Attributes:** public  
    
**Implemented Features:**
    
    - Content Submission Management
    - Content Review Workflow
    - Version Control
    
**Requirement Ids:**
    
    - REQ-DMG-006
    - REQ-2-009
    - REQ-2-010
    - REQ-2-011
    - REQ-2-018
    
**Purpose:** To manage content submitted by influencers, its review lifecycle, and associated feedback.  
**Logic Description:** Links to CampaignApplication. Fields for content (URL or attachment), status, feedback history (perhaps another model `content.feedback.log` as O2M), versioning. Computed fields for `campaign_id` and `influencer_profile_id` from `campaign_application_id`. Inherit `mail.thread` and `BaseAuditMixin`. `performance_data_json` for REQ-2-011.  
**Documentation:**
    
    - **Summary:** Represents a piece of content submitted by an influencer for a campaign.
    
**Namespace:** odoo.addons.influence_gen_services.models.content_submission  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/content_feedback_log.py  
**Description:** Odoo model for logging feedback history on content submissions.  
**Template:** Odoo Model  
**Dependancy Level:** 4  
**Name:** ContentFeedbackLog  
**Type:** Odoo Model  
**Relative Path:** models/content_feedback_log.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** content_submission_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** reviewer_user_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** feedback_text  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** timestamp  
**Type:** fields.Datetime  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Content Feedback History
    
**Requirement Ids:**
    
    - REQ-DMG-006
    - REQ-2-010
    
**Purpose:** To maintain a historical log of all feedback provided during the review of a content submission.  
**Logic Description:** Stores a single feedback entry, linked to a ContentSubmission and the reviewer. This allows for a full audit trail of the review process. Inherit from `BaseAuditMixin` (for creation).  
**Documentation:**
    
    - **Summary:** Logs an instance of feedback provided on a content submission.
    
**Namespace:** odoo.addons.influence_gen_services.models.content_feedback_log  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/ai_image_model.py  
**Description:** Odoo model for AI Image Generation Models available in the system.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** AiImageModel  
**Type:** Odoo Model  
**Relative Path:** models/ai_image_model.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** trigger_keywords  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** is_active  
**Type:** fields.Boolean  
**Attributes:** public  
    - **Name:** external_model_id  
**Type:** fields.Char  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** _sql_constraints_name_unique  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** protected  
    
**Implemented Features:**
    
    - AI Model Configuration
    
**Requirement Ids:**
    
    - REQ-DMG-007
    - REQ-AIGS-004
    
**Purpose:** To define and manage the list of AI image generation models (e.g., Flux LoRA models) available to users.  
**Logic Description:** Stores model name, description, trigger keywords, active status, and external ID for API calls. Managed by Platform Administrators. Inherit from `BaseAuditMixin`.  
**Documentation:**
    
    - **Summary:** Represents an AI image generation model that can be selected by users.
    
**Namespace:** odoo.addons.influence_gen_services.models.ai_image_model  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/ai_image_generation_request.py  
**Description:** Odoo model for AI Image Generation Requests.  
**Template:** Odoo Model  
**Dependancy Level:** 2  
**Name:** AiImageGenerationRequest  
**Type:** Odoo Model  
**Relative Path:** models/ai_image_generation_request.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** influencer_profile_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** campaign_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** prompt  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** negative_prompt  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** model_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** resolution  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** aspect_ratio  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** seed  
**Type:** fields.Integer  
**Attributes:** public  
    - **Name:** inference_steps  
**Type:** fields.Integer  
**Attributes:** public  
    - **Name:** cfg_scale  
**Type:** fields.Float  
**Attributes:** public  
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** intended_use  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** error_details  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** n8n_execution_id  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** generated_image_ids  
**Type:** fields.One2many  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** action_submit_to_n8n  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** process_n8n_callback_success  
**Parameters:**
    
    - self
    - image_data_list
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** process_n8n_callback_failure  
**Parameters:**
    
    - self
    - error_message
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _check_quota  
**Parameters:**
    
    - self
    
**Return Type:** bool  
**Attributes:** protected  
    
**Implemented Features:**
    
    - AI Image Request Management
    - Quota Enforcement
    - N8N Integration Preparation
    
**Requirement Ids:**
    
    - REQ-DMG-007
    - REQ-AIGS-001
    - REQ-AIGS-002
    - REQ-AIGS-003
    - REQ-AIGS-004
    - REQ-AIGS-007
    - REQ-AIGS-012
    
**Purpose:** To record and manage user requests for AI image generation, including parameters, status, and links to results.  
**Logic Description:** Fields for user, prompts, parameters, model, status, N8N ID, etc. `_check_quota` method to be called before submission. `action_submit_to_n8n` calls the `ai_integration_service`. Methods to handle callbacks from N8N to update status and link generated images. Inherit `mail.thread` and `BaseAuditMixin`.  
**Documentation:**
    
    - **Summary:** Represents a single request made by a user to generate an AI image.
    
**Namespace:** odoo.addons.influence_gen_services.models.ai_image_generation_request  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/generated_image.py  
**Description:** Odoo model for metadata of AI Generated Images.  
**Template:** Odoo Model  
**Dependancy Level:** 3  
**Name:** GeneratedImage  
**Type:** Odoo Model  
**Relative Path:** models/generated_image.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** request_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** image_attachment_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** storage_url  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** file_format  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** file_size  
**Type:** fields.Integer  
**Attributes:** public  
    - **Name:** width  
**Type:** fields.Integer  
**Attributes:** public  
    - **Name:** height  
**Type:** fields.Integer  
**Attributes:** public  
    - **Name:** hash_value  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** retention_category  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** usage_rights  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** is_campaign_asset  
**Type:** fields.Boolean  
**Attributes:** public  
    - **Name:** legal_hold_status  
**Type:** fields.Boolean  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** action_mark_for_deletion  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Generated Image Metadata Storage
    - Retention Categorization
    
**Requirement Ids:**
    
    - REQ-DMG-008
    - REQ-AIGS-006
    - REQ-AIGS-010
    - REQ-AIGS-011
    - REQ-DMG-020
    
**Purpose:** To store metadata about AI-generated images, including storage references, hashes, and retention information.  
**Logic Description:** Links to `AiImageGenerationRequest`. Fields for storage info (attachment or URL), hash, retention category. `image_attachment_id` links to `ir.attachment`. `storage_url` could be used if stored externally. Inherit `BaseAuditMixin`.  
**Documentation:**
    
    - **Summary:** Represents an image generated by the AI service, storing its metadata and links.
    
**Namespace:** odoo.addons.influence_gen_services.models.generated_image  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/payment_record.py  
**Description:** Odoo model for Influencer Payment Records.  
**Template:** Odoo Model  
**Dependancy Level:** 4  
**Name:** PaymentRecord  
**Type:** Odoo Model  
**Relative Path:** models/payment_record.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Repository Pattern (via Odoo ORM)
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** influencer_profile_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** campaign_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** content_submission_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** amount  
**Type:** fields.Monetary  
**Attributes:** public  
    - **Name:** currency_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** status  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** transaction_id  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** payment_method  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** due_date  
**Type:** fields.Date  
**Attributes:** public  
    - **Name:** paid_date  
**Type:** fields.Date  
**Attributes:** public  
    - **Name:** odoo_vendor_bill_id  
**Type:** fields.Many2one  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** action_mark_as_paid  
**Parameters:**
    
    - self
    - transaction_id=None
    - paid_date=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_process_via_odoo_accounting  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Payment Tracking
    - Payment Status Management
    - Odoo Accounting Integration Link
    
**Requirement Ids:**
    
    - REQ-DMG-009
    - REQ-IPF-004
    - REQ-IPF-005
    - REQ-IPF-007
    - REQ-2-013
    - REQ-2-015
    
**Purpose:** To track payments owed to influencers, their status, and manage integration with Odoo's accounting.  
**Logic Description:** Links to Influencer, Campaign, Content Submission. Fields for amount, currency, status, transaction ID. `odoo_vendor_bill_id` to link to `account.move` if using vendor bills. Methods to update status, trigger processing via `payment_processing_service`. Inherit `mail.thread` and `BaseAuditMixin`.  
**Documentation:**
    
    - **Summary:** Represents a payment transaction or obligation to an influencer.
    
**Namespace:** odoo.addons.influence_gen_services.models.payment_record  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/audit_log.py  
**Description:** Odoo model for storing Audit Trail records.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** AuditLog  
**Type:** Odoo Model  
**Relative Path:** models/audit_log.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Audit Logging
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _order  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** timestamp  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** event_type  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** target_model  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** target_res_id  
**Type:** fields.Integer  
**Attributes:** public  
    - **Name:** action  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** details_json  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** ip_address  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** outcome  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** legal_hold_status  
**Type:** fields.Boolean  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Trail Storage
    
**Requirement Ids:**
    
    - REQ-ATEL-005
    - REQ-ATEL-006
    - REQ-ATEL-007
    - REQ-IOKYC-016
    - REQ-2-018
    - REQ-AIGS-012
    - REQ-IPF-009
    
**Purpose:** To provide a dedicated, tamper-evident store for all significant system events and user actions as per REQ-ATEL-005.  
**Logic Description:** Fields for timestamp, user, event type, affected entity (model and ID), action, outcome, IP, and details (JSON). Order by timestamp desc. This model is primarily for data storage; creation is handled by the `BaseAuditMixin` or `audit_trail_service`.  
**Documentation:**
    
    - **Summary:** Stores detailed records of auditable events within the InfluenceGen platform.
    
**Namespace:** odoo.addons.influence_gen_services.models.audit_log  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/usage_tracking_log.py  
**Description:** Odoo model for tracking platform feature usage, especially AI image generation.  
**Template:** Odoo Model  
**Dependancy Level:** 2  
**Name:** UsageTrackingLog  
**Type:** Odoo Model  
**Relative Path:** models/usage_tracking_log.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** influencer_profile_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** feature_name  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** timestamp  
**Type:** fields.Datetime  
**Attributes:** public  
    - **Name:** campaign_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** details_json  
**Type:** fields.Text  
**Attributes:** public  
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Usage Tracking
    - Feature Usage Logging
    
**Requirement Ids:**
    
    - REQ-DMG-023
    - REQ-AIGS-007
    
**Purpose:** To log usage of specific platform features, particularly AI image generation, for analytics, quota management, and resource planning.  
**Logic Description:** Fields for user, feature used (e.g., 'ai_image_generation'), timestamp, campaign context, and details (e.g., model used, parameters, API calls made for AI generation). Creation handled by relevant services (e.g., `ai_integration_service`).  
**Documentation:**
    
    - **Summary:** Logs instances of platform feature usage for tracking and analysis.
    
**Namespace:** odoo.addons.influence_gen_services.models.usage_tracking_log  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/platform_setting.py  
**Description:** Odoo model for storing platform-wide configuration settings.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** PlatformSetting  
**Type:** Odoo Model  
**Relative Path:** models/platform_setting.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Configuration Management
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** key  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** value_char  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** value_text  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** value_int  
**Type:** fields.Integer  
**Attributes:** public  
    - **Name:** value_float  
**Type:** fields.Float  
**Attributes:** public  
    - **Name:** value_bool  
**Type:** fields.Boolean  
**Attributes:** public  
    - **Name:** value_type  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** _sql_constraints_key_unique  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** protected  
    - **Name:** get_setting  
**Parameters:**
    
    - cls
    - key_name
    - default=None
    
**Return Type:** any  
**Attributes:** public|classmethod  
    - **Name:** set_setting  
**Parameters:**
    
    - cls
    - key_name
    - value
    - value_type=None
    - description=None
    
**Return Type:** recordset  
**Attributes:** public|classmethod  
    
**Implemented Features:**
    
    - System Configuration Management
    
**Requirement Ids:**
    
    - REQ-IOKYC-017
    
**Purpose:** To provide a flexible way to store and manage various platform settings and business rule parameters that can be changed without code deployment.  
**Logic Description:** A key-value store with type information. `get_setting` and `set_setting` class methods for easy access. `value_type` selection field indicates which `value_*` field to use. Inherit from `BaseAuditMixin` for logging changes to settings.  
**Documentation:**
    
    - **Summary:** Stores configurable key-value settings for the InfluenceGen platform.
    
**Namespace:** odoo.addons.influence_gen_services.models.platform_setting  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/__init__.py  
**Description:** Initializes the Python package for service layer classes within the InfluenceGen Services module.  
**Template:** Odoo Services __init__.py  
**Dependancy Level:** 2  
**Name:** __init__  
**Type:** Python Package Initializer  
**Relative Path:** services/__init__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    - Service Layer
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    
**Requirement Ids:**
    
    
**Purpose:** To make all service files in the 'services' directory discoverable.  
**Logic Description:** Import all Python files defined in the 'services' directory. Example: from . import onboarding_service; from . import campaign_management_service; ...  
**Documentation:**
    
    - **Summary:** Initializer for the service layer components of the InfluenceGen Services module.
    
**Namespace:** odoo.addons.influence_gen_services.services  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_services/services/onboarding_service.py  
**Description:** Service class for orchestrating influencer onboarding and KYC processes.  
**Template:** Odoo Service  
**Dependancy Level:** 3  
**Name:** OnboardingService  
**Type:** Odoo Service  
**Relative Path:** services/onboarding_service.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Service Layer
    
**Members:**
    
    - **Name:** env  
**Type:** odoo.api.Environment  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** process_registration_submission  
**Parameters:**
    
    - self
    - influencer_vals
    
**Return Type:** recordset  
**Attributes:** public  
    - **Name:** submit_kyc_documents  
**Parameters:**
    
    - self
    - influencer_id
    - document_data_list
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** handle_kyc_review_decision  
**Parameters:**
    
    - self
    - kyc_data_id
    - decision
    - reviewer_id
    - notes=None
    - required_info=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** verify_social_media_account  
**Parameters:**
    
    - self
    - social_profile_id
    - method
    - verification_input=None
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** verify_bank_account  
**Parameters:**
    
    - self
    - bank_account_id
    - method
    - verification_input=None
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** process_terms_consent  
**Parameters:**
    
    - self
    - influencer_id
    - tos_version
    - privacy_policy_version
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** check_and_activate_influencer_account  
**Parameters:**
    
    - self
    - influencer_id
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - Influencer Onboarding Orchestration
    - KYC Workflow Management
    - Account Activation Logic
    
**Requirement Ids:**
    
    - REQ-IOKYC-002
    - REQ-IOKYC-005
    - REQ-IOKYC-006
    - REQ-IOKYC-008
    - REQ-IOKYC-009
    - REQ-IOKYC-011
    - REQ-IOKYC-012
    
**Purpose:** To manage the end-to-end workflow of influencer onboarding, including KYC, social media, and bank account verification, leading to account activation.  
**Logic Description:** Coordinates interactions between `InfluencerProfile`, `KycData`, `SocialMediaProfile`, `BankAccount`, and `TermsConsent` models. Implements the state machine for onboarding statuses. `check_and_activate_influencer_account` verifies all prerequisite conditions are met. Interacts with external verification services via REPO-IGIA-004 if needed.  
**Documentation:**
    
    - **Summary:** Orchestrates the complex business processes involved in onboarding a new influencer.
    
**Namespace:** odoo.addons.influence_gen_services.services.onboarding_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/campaign_management_service.py  
**Description:** Service class for managing campaign lifecycle, applications, content, and performance.  
**Template:** Odoo Service  
**Dependancy Level:** 3  
**Name:** CampaignManagementService  
**Type:** Odoo Service  
**Relative Path:** services/campaign_management_service.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Service Layer
    
**Members:**
    
    - **Name:** env  
**Type:** odoo.api.Environment  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** create_campaign  
**Parameters:**
    
    - self
    - campaign_vals
    
**Return Type:** recordset  
**Attributes:** public  
    - **Name:** update_campaign_status  
**Parameters:**
    
    - self
    - campaign_id
    - new_status
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** review_campaign_application  
**Parameters:**
    
    - self
    - application_id
    - decision
    - reviewer_id
    - reason=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** review_content_submission  
**Parameters:**
    
    - self
    - submission_id
    - decision
    - reviewer_id
    - feedback=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** record_campaign_performance  
**Parameters:**
    
    - self
    - submission_id_or_campaign_id
    - metrics_data
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** get_campaign_performance_summary  
**Parameters:**
    
    - self
    - campaign_id
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** get_influencer_performance_summary  
**Parameters:**
    
    - self
    - influencer_id
    - campaign_id=None
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Campaign Lifecycle Orchestration
    - Application Review Service
    - Content Moderation Service
    - Performance Tracking Service
    
**Requirement Ids:**
    
    - REQ-2-001
    - REQ-2-007
    - REQ-2-010
    - REQ-2-011
    - REQ-2-012
    - REQ-2-017
    - REQ-2-018
    
**Purpose:** To orchestrate complex campaign-related operations, including status transitions, review processes, and performance metric aggregation.  
**Logic Description:** Interacts with `Campaign`, `CampaignApplication`, `ContentSubmission` models. `update_campaign_status` handles campaign state changes. `review_campaign_application` and `review_content_submission` manage approval workflows. `record_campaign_performance` updates performance data on `ContentSubmission` or `Campaign`. `get_..._summary` methods aggregate data for dashboards.  
**Documentation:**
    
    - **Summary:** Manages business logic related to the lifecycle of campaigns, influencer participation, and content.
    
**Namespace:** odoo.addons.influence_gen_services.services.campaign_management_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/payment_processing_service.py  
**Description:** Service class for handling influencer payment calculations, batching, and Odoo accounting integration.  
**Template:** Odoo Service  
**Dependancy Level:** 3  
**Name:** PaymentProcessingService  
**Type:** Odoo Service  
**Relative Path:** services/payment_processing_service.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Service Layer
    
**Members:**
    
    - **Name:** env  
**Type:** odoo.api.Environment  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** calculate_amounts_owed  
**Parameters:**
    
    - self
    - campaign_id=None
    - influencer_id=None
    
**Return Type:** list_of_dicts  
**Attributes:** public  
    - **Name:** create_payment_records_for_approved_content  
**Parameters:**
    
    - self
    - content_submission_ids
    
**Return Type:** recordset  
**Attributes:** public  
    - **Name:** generate_payment_batch  
**Parameters:**
    
    - self
    - payment_record_ids
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** process_payment_batch_with_odoo_accounting  
**Parameters:**
    
    - self
    - payment_batch_data
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** update_payment_status  
**Parameters:**
    
    - self
    - payment_record_id_or_transaction_id
    - new_status
    - details=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** handle_payment_failure  
**Parameters:**
    
    - self
    - payment_record_id
    - failure_reason
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Payment Calculation
    - Payment Batch Generation
    - Odoo Accounting Integration for Payments
    - Payment Status Management
    
**Requirement Ids:**
    
    - REQ-IPF-003
    - REQ-IPF-004
    - REQ-IPF-005
    - REQ-IPF-006
    - REQ-IPF-009
    - REQ-IPF-010
    - REQ-2-013
    - REQ-2-014
    - REQ-2-015
    
**Purpose:** To manage the financial aspects of influencer compensation, from calculating dues to initiating payments via Odoo accounting.  
**Logic Description:** Interacts with `PaymentRecord`, `Campaign`, `ContentSubmission`, `BankAccount`, and Odoo's `account.move` (Vendor Bill) and `account.payment`. `calculate_amounts_owed` implements logic based on compensation models. `create_payment_records...` generates records based on approved work. `process_payment_batch...` creates vendor bills. `handle_payment_failure` triggers alerts (REQ-IPF-010).  
**Documentation:**
    
    - **Summary:** Handles business logic for influencer payments, including calculations and integration with financial systems.
    
**Namespace:** odoo.addons.influence_gen_services.services.payment_processing_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/ai_integration_service.py  
**Description:** Service class for managing AI image generation requests, N8N interaction, and quota management.  
**Template:** Odoo Service  
**Dependancy Level:** 3  
**Name:** AiIntegrationService  
**Type:** Odoo Service  
**Relative Path:** services/ai_integration_service.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Service Layer
    
**Members:**
    
    - **Name:** env  
**Type:** odoo.api.Environment  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** initiate_ai_image_generation  
**Parameters:**
    
    - self
    - user_id
    - prompt_data
    - generation_params
    
**Return Type:** recordset  
**Attributes:** public  
    - **Name:** handle_n8n_image_result_callback  
**Parameters:**
    
    - self
    - request_id
    - image_results
    - n8n_execution_id
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** handle_n8n_image_error_callback  
**Parameters:**
    
    - self
    - request_id
    - error_message
    - n8n_execution_id
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** check_user_ai_quota  
**Parameters:**
    
    - self
    - user_id
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** decrement_user_ai_quota  
**Parameters:**
    
    - self
    - user_id
    - images_generated=1
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** log_ai_usage  
**Parameters:**
    
    - self
    - request_id
    - images_generated
    - api_calls
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** validate_ai_prompt  
**Parameters:**
    
    - self
    - prompt_text
    
**Return Type:** tuple  
**Attributes:** public  
    
**Implemented Features:**
    
    - AI Image Generation Orchestration
    - N8N Integration Management
    - AI Quota Enforcement
    - AI Usage Logging
    - Prompt Moderation Logic
    
**Requirement Ids:**
    
    - REQ-AIGS-001
    - REQ-AIGS-002
    - REQ-AIGS-003
    - REQ-AIGS-004
    - REQ-AIGS-006
    - REQ-AIGS-007
    - REQ-AIGS-015
    
**Purpose:** To orchestrate the AI image generation process, interact with N8N (via REPO-IGIA-004), enforce usage quotas, and manage related data.  
**Logic Description:** Creates `AiImageGenerationRequest`. `initiate_ai_image_generation` calls `check_user_ai_quota`, validates prompt (REQ-AIGS-003), then calls REPO-IGIA-004 to trigger N8N. Callback methods update `AiImageGenerationRequest` and create `GeneratedImage` records (REQ-AIGS-006, REQ-AIGS-010). `log_ai_usage` creates `UsageTrackingLog` entries (REQ-AIGS-007).  
**Documentation:**
    
    - **Summary:** Manages interactions with the AI image generation pipeline (N8N) and associated business logic.
    
**Namespace:** odoo.addons.influence_gen_services.services.ai_integration_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/data_management_service.py  
**Description:** Service class for data quality, cleansing, masking, and MDM-related operations.  
**Template:** Odoo Service  
**Dependancy Level:** 3  
**Name:** DataManagementService  
**Type:** Odoo Service  
**Relative Path:** services/data_management_service.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Service Layer
    
**Members:**
    
    - **Name:** env  
**Type:** odoo.api.Environment  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** identify_data_quality_issues  
**Parameters:**
    
    - self
    - model_name
    - domain=None
    
**Return Type:** list_of_issues  
**Attributes:** public  
    - **Name:** cleanse_influencer_data  
**Parameters:**
    
    - self
    - influencer_ids
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** generate_anonymized_dataset_for_staging  
**Parameters:**
    
    - self
    - models_to_anonymize
    
**Return Type:** str  
**Attributes:** public  
    - **Name:** apply_mdm_rules  
**Parameters:**
    
    - self
    - model_name
    - record_ids
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Data Cleansing Operations
    - Data Anonymization for Non-Production
    - MDM Rule Application
    
**Requirement Ids:**
    
    - REQ-DMG-012
    - REQ-DMG-017
    - REQ-DMG-022
    
**Purpose:** To provide services for maintaining data quality, preparing data for non-production environments, and applying master data management principles.  
**Logic Description:** `identify_data_quality_issues` uses predefined business rules (from `PlatformSetting` or hardcoded) to find inconsistent/incomplete data. `cleanse_influencer_data` applies correction rules. `generate_anonymized_dataset_for_staging` implements logic to mask/anonymize PII for specific models (REQ-DMG-022). `apply_mdm_rules` could handle deduplication or golden record logic based on documented strategy.  
**Documentation:**
    
    - **Summary:** Provides services related to data quality, anonymization, and master data management.
    
**Namespace:** odoo.addons.influence_gen_services.services.data_management_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/retention_and_legal_hold_service.py  
**Description:** Service class for managing data retention policies, disposition, archival, and legal holds.  
**Template:** Odoo Service  
**Dependancy Level:** 3  
**Name:** RetentionAndLegalHoldService  
**Type:** Odoo Service  
**Relative Path:** services/retention_and_legal_hold_service.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Service Layer
    
**Members:**
    
    - **Name:** env  
**Type:** odoo.api.Environment  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** get_retention_policy  
**Parameters:**
    
    - self
    - data_category
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** apply_retention_policies_automated  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** process_manual_erasure_request  
**Parameters:**
    
    - self
    - model_name
    - record_id
    - requestor_id
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** archive_data_batch  
**Parameters:**
    
    - self
    - model_name
    - domain
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** place_legal_hold  
**Parameters:**
    
    - self
    - model_name
    - record_id
    - hold_reason
    - placed_by_user_id
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** lift_legal_hold  
**Parameters:**
    
    - self
    - model_name
    - record_id
    - lifted_by_user_id
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** check_legal_hold  
**Parameters:**
    
    - self
    - model_name
    - record_id
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - Data Retention Policy Management
    - Automated Data Disposition
    - Manual Erasure Processing
    - Data Archival
    - Legal Hold Management
    
**Requirement Ids:**
    
    - REQ-DRH-001
    - REQ-DRH-002
    - REQ-DRH-003
    - REQ-DRH-004
    - REQ-DRH-005
    - REQ-DRH-006
    - REQ-DRH-007
    - REQ-DRH-008
    - REQ-DRH-009
    - REQ-DRH-010
    - REQ-IOKYC-018
    - REQ-AIGS-011
    - REQ-IPF-008
    - REQ-ATEL-007
    
**Purpose:** To manage the lifecycle of data according to defined retention policies, including archival and legal hold functionalities.  
**Logic Description:** Reads policies from `PlatformSetting` or a dedicated retention policy model. `apply_retention_policies_automated` is a cron job method that identifies expired data (respecting legal holds) and triggers deletion/anonymization/archival. `process_manual_erasure_request` handles GDPR erasure. `place_legal_hold` and `lift_legal_hold` update a `legal_hold_status` field on relevant models and log to audit trail. Archival logic would move data to a different state or storage.  
**Documentation:**
    
    - **Summary:** Manages data retention, archival, and legal hold processes according to platform policies.
    
**Namespace:** odoo.addons.influence_gen_services.services.retention_and_legal_hold_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/wizards/__init__.py  
**Description:** Initializes the Python package for wizard models within the InfluenceGen Services module.  
**Template:** Odoo Wizards __init__.py  
**Dependancy Level:** 2  
**Name:** __init__  
**Type:** Python Package Initializer  
**Relative Path:** wizards/__init__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Wizard Discovery
    
**Requirement Ids:**
    
    
**Purpose:** To make all wizard (transient model) files in the 'wizards' directory discoverable by Odoo.  
**Logic Description:** Import all Python files defined in the 'wizards' directory. Example: from . import kyc_manual_review_wizard;  
**Documentation:**
    
    - **Summary:** Initializer for wizard (transient model) components used for specific user actions.
    
**Namespace:** odoo.addons.influence_gen_services.wizards  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_services/wizards/kyc_manual_review_wizard.py  
**Description:** Odoo transient model (wizard) for facilitating the manual KYC review process by administrators.  
**Template:** Odoo Wizard Model  
**Dependancy Level:** 3  
**Name:** KycManualReviewWizard  
**Type:** Odoo Wizard Model  
**Relative Path:** wizards/kyc_manual_review_wizard.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Wizard Pattern
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** _description  
**Type:** str  
**Attributes:** protected|static  
    - **Name:** kyc_data_id  
**Type:** fields.Many2one  
**Attributes:** public  
    - **Name:** decision  
**Type:** fields.Selection  
**Attributes:** public  
    - **Name:** rejection_reason_text  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** required_info_text  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** reviewer_notes  
**Type:** fields.Text  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** action_confirm_review  
**Parameters:**
    
    - self
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - Manual KYC Review Action
    
**Requirement Ids:**
    
    - REQ-IOKYC-011
    
**Purpose:** To provide a structured UI for administrators to input their decision and notes during a manual KYC review.  
**Logic Description:** Transient model. Fields to select decision (approve, reject, more info), input reasons/notes. `action_confirm_review` calls the `onboarding_service` or `KycData` model methods to update the KYC status and log the review.  
**Documentation:**
    
    - **Summary:** A wizard to guide administrators through the manual KYC review and decision-making process.
    
**Namespace:** odoo.addons.influence_gen_services.wizards.kyc_manual_review_wizard  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/security/ir.model.access.csv  
**Description:** Defines model access rights (CRUD) for different user groups within the InfluenceGen Services module.  
**Template:** Odoo Security ir.model.access.csv  
**Dependancy Level:** 3  
**Name:** ir.model.access  
**Type:** Odoo Security Data  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Role-Based Access Control
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Access Control
    
**Requirement Ids:**
    
    
**Purpose:** To specify which user groups can perform read, write, create, and delete operations on each custom Odoo model.  
**Logic Description:** CSV file with columns: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. Define access rights for models like `influence_gen.influencer_profile`, `influence_gen.campaign`, etc., for groups like 'base.group_user' (for influencers), 'influence_gen_services.group_platform_admin'. Ensure least privilege.  
**Documentation:**
    
    - **Summary:** Configures access control lists (ACLs) for all custom models in the module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** odoo_modules/influence_gen_services/security/influence_gen_security.xml  
**Description:** Defines custom security groups and record rules for the InfluenceGen Services module.  
**Template:** Odoo Security XML  
**Dependancy Level:** 3  
**Name:** influence_gen_security  
**Type:** Odoo Security Data  
**Relative Path:** security/influence_gen_security.xml  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Role-Based Access Control
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Security Group Definition
    - Record Rule Definition
    
**Requirement Ids:**
    
    
**Purpose:** To create specific user roles (security groups) like 'Platform Administrator', 'Influencer', and define record-level access rules if needed.  
**Logic Description:** XML file defining `record` tags for `res.groups` (e.g., `group_influence_gen_admin`, `group_influence_gen_influencer`). Define `ir.rule` records for fine-grained row-level security if necessary (e.g., influencer can only see their own profile).  
**Documentation:**
    
    - **Summary:** Defines custom security groups and record-level security rules for the module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** odoo_modules/influence_gen_services/data/__init__.py  
**Description:** Initializes the Python package for data files within the InfluenceGen Services module.  
**Template:** Odoo Data __init__.py  
**Dependancy Level:** 2  
**Name:** __init__  
**Type:** Python Package Initializer  
**Relative Path:** data/__init__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Modular Design (Odoo Modules)
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    
**Requirement Ids:**
    
    
**Purpose:** Required by Odoo, though data files are usually XML and listed in manifest.  
**Logic Description:** Typically empty for Odoo modules where data is loaded via XML files listed in the manifest.  
**Documentation:**
    
    - **Summary:** Initializer for the data directory (primarily for XML data files).
    
**Namespace:** odoo.addons.influence_gen_services.data  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_services/data/platform_setting_data.xml  
**Description:** XML data file for loading default platform settings.  
**Template:** Odoo XML Data  
**Dependancy Level:** 3  
**Name:** platform_setting_data  
**Type:** Odoo Data XML  
**Relative Path:** data/platform_setting_data.xml  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Configuration Management
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default Platform Configuration
    
**Requirement Ids:**
    
    - REQ-IOKYC-017
    
**Purpose:** To load initial/default values for system configurations managed by the `PlatformSetting` model.  
**Logic Description:** Contains `<record>` tags for `influence_gen.platform_setting` model to define default settings like AI quota limits, default KYC document types, retention periods, etc.  
**Documentation:**
    
    - **Summary:** Provides default values for system-wide platform settings.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Data
    
- **Path:** odoo_modules/influence_gen_services/data/mail_template_data.xml  
**Description:** XML data file for defining email templates used by the system.  
**Template:** Odoo XML Data  
**Dependancy Level:** 3  
**Name:** mail_template_data  
**Type:** Odoo Data XML  
**Relative Path:** data/mail_template_data.xml  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default Email Templates
    
**Requirement Ids:**
    
    - REQ-16-001
    - REQ-16-002
    - REQ-16-003
    - REQ-16-004
    - REQ-16-005
    
**Purpose:** To define the structure and content of various email notifications sent by the platform.  
**Logic Description:** Contains `<record>` tags for `mail.template` model. Defines templates for registration confirmation, KYC status updates, campaign application updates, content submission feedback, etc. Use Odoo's dynamic placeholders.  
**Documentation:**
    
    - **Summary:** Stores definitions for system email templates used for various notifications.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Data
    
- **Path:** odoo_modules/influence_gen_services/data/scheduled_actions_data.xml  
**Description:** XML data file for defining Odoo scheduled actions (cron jobs).  
**Template:** Odoo XML Data  
**Dependancy Level:** 3  
**Name:** scheduled_actions_data  
**Type:** Odoo Data XML  
**Relative Path:** data/scheduled_actions_data.xml  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Task Scheduling
    
**Requirement Ids:**
    
    - REQ-DRH-002
    - REQ-AIGS-002
    
**Purpose:** To define automated background tasks such as data retention policy enforcement, AI quota resets, etc.  
**Logic Description:** Contains `<record>` tags for `ir.cron` model. Defines cron jobs to call methods on services like `retention_and_legal_hold_service.apply_retention_policies_automated()` or methods to reset monthly AI quotas.  
**Documentation:**
    
    - **Summary:** Configures scheduled background tasks (cron jobs) for the platform.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Data
    
- **Path:** odoo_modules/influence_gen_services/i18n/influence_gen_services.pot  
**Description:** Standard Odoo Portable Object Template (POT) file for module translations.  
**Template:** Odoo i18n POT  
**Dependancy Level:** 4  
**Name:** influence_gen_services  
**Type:** Odoo i18n Data  
**Relative Path:** i18n/influence_gen_services.pot  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Localization Support (Template)
    
**Requirement Ids:**
    
    - REQ-L10N-003
    
**Purpose:** To provide a template for translating all user-visible strings in the InfluenceGen Services module into other languages.  
**Logic Description:** This file is typically generated by Odoo's `makepot` command. It will contain all strings marked for translation in Python code and XML views.  
**Documentation:**
    
    - **Summary:** Translation template file for the InfluenceGen Services module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** i18n
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableAutomatedKycVerification
  - EnableMicroDepositVerification
  - EnableAdvancedAiQuotaManagement
  - EnableAutomatedDataArchival
  
- **Database Configs:**
  
  


---

