# Specification

# 1. Files

- **Path:** odoo_modules/influence_gen_services/__init__.py  
**Description:** Initializes the Python package for the Odoo business services module, importing submodules like 'models', 'services', and 'wizards'.  
**Template:** Python Package Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'influence_gen_services' directory a Python package and exposes its submodules.  
**Logic Description:** Contains import statements for 'models', 'services', and 'wizards' sub-packages/modules.  
**Documentation:**
    
    - **Summary:** Standard Odoo module __init__.py file.
    
**Namespace:** odoo.addons.influence_gen_services  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_services/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata such as name, version, author, dependencies, and data files.  
**Template:** Odoo Manifest  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** ModuleDescriptor  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    
**Requirement Ids:**
    
    
**Purpose:** Provides Odoo with essential information about the 'influence_gen_services' module.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'depends' (e.g., ['base', 'mail']), 'data' (listing XML and CSV files), 'installable', 'application'. Depends will list Odoo core modules this module relies upon.  
**Documentation:**
    
    - **Summary:** Standard Odoo module manifest. Lists dependencies like 'base', 'mail', and data files such as security CSVs and wizard XML views.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_services/models/__init__.py  
**Description:** Initializes the 'models' Python package, importing all Odoo model files defined within this directory.  
**Template:** Python Package Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** models/__init__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Loading
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'models' directory a Python package and ensures all model classes are loaded by Odoo.  
**Logic Description:** Contains import statements for each model file (e.g., 'from . import influencer_profile').  
**Documentation:**
    
    - **Summary:** Imports all Odoo models for the InfluenceGen services module.
    
**Namespace:** odoo.addons.influence_gen_services.models  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_services/models/influencer_profile.py  
**Description:** Odoo model for Influencer Profile. Manages personal, contact, professional information, social media links, KYC status, payment details linkage, consent records, and account status. Implements business logic for profile updates, uniqueness checks, and data validation.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** influencer_profile  
**Type:** Model  
**Relative Path:** models/influencer_profile.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    - Service Layer (methods)
    
**Members:**
    
    - **Name:** name  
**Type:** String  
**Attributes:** char  
    - **Name:** user_id  
**Type:** Many2one  
**Attributes:** comodel_name='res.users'  
    - **Name:** email  
**Type:** String  
**Attributes:** char  
    - **Name:** phone  
**Type:** String  
**Attributes:** char  
    - **Name:** residential_address  
**Type:** String  
**Attributes:** char  
    - **Name:** audience_demographics  
**Type:** Text  
**Attributes:** fields.Text (for JSON-like storage)  
    - **Name:** kyc_status  
**Type:** Selection  
**Attributes:** selection=[('pending', 'Pending'), ('in_review', 'In Review'), ('approved', 'Approved'), ('rejected', 'Rejected')]  
    - **Name:** account_status  
**Type:** Selection  
**Attributes:** selection=[('inactive', 'Inactive'), ('active', 'Active'), ('suspended', 'Suspended')]  
    - **Name:** social_media_profile_ids  
**Type:** One2many  
**Attributes:** comodel_name='influence_gen.social_media_profile'  
    - **Name:** kyc_data_ids  
**Type:** One2many  
**Attributes:** comodel_name='influence_gen.kyc_data'  
    - **Name:** bank_account_ids  
**Type:** One2many  
**Attributes:** comodel_name='influence_gen.bank_account'  
    - **Name:** terms_consent_ids  
**Type:** One2many  
**Attributes:** comodel_name='influence_gen.terms_consent'  
    - **Name:** area_of_influence_ids  
**Type:** Many2many  
**Attributes:** comodel_name='influence_gen.area_of_influence'  
    
**Methods:**
    
    - **Name:** action_activate_account  
**Parameters:**
    
    - self
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** action_deactivate_account  
**Parameters:**
    
    - self
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** update_kyc_status  
**Parameters:**
    
    - self
    - new_status
    - notes=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _validate_email_uniqueness  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private|@api.constrains('email')  
    - **Name:** check_onboarding_completion  
**Parameters:**
    
    - self
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** get_active_payment_details  
**Parameters:**
    
    - self
    
**Return Type:** recordset  
**Attributes:** public  
    
**Implemented Features:**
    
    - Influencer Profile Management
    - Account Activation Logic
    - KYC Status Tracking
    - Consent Linking
    
**Requirement Ids:**
    
    - REQ-IOKYC-002
    - REQ-IOKYC-009
    - REQ-IOKYC-012
    - REQ-DMG-001
    - REQ-DMG-002
    - REQ-DMG-013
    - REQ-DMG-014
    - REQ-DMG-015
    - REQ-DMG-016
    
**Purpose:** Defines the data structure and business logic for influencer profiles.  
**Logic Description:** Contains fields for all influencer attributes. Implements methods for account activation/deactivation based on KYC and onboarding completion (REQ-IOKYC-012). Includes validation for email uniqueness (REQ-IOKYC-002 part). Manages links to other related entities like KYC, bank accounts, and consent.  
**Documentation:**
    
    - **Summary:** Model for storing and managing influencer profile data and related business logic.
    
**Namespace:** odoo.addons.influence_gen_services.models.influencer_profile  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/social_media_profile.py  
**Description:** Odoo model for Influencer Social Media Profiles. Manages platform, handle, URL, verification status, and metrics. Implements logic for social media handle uniqueness per platform and format validation.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** social_media_profile  
**Type:** Model  
**Relative Path:** models/social_media_profile.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** influencer_profile_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.influencer_profile'  
    - **Name:** platform  
**Type:** String  
**Attributes:** char  
    - **Name:** handle  
**Type:** String  
**Attributes:** char  
    - **Name:** url  
**Type:** String  
**Attributes:** char  
    - **Name:** verification_status  
**Type:** Selection  
**Attributes:** selection=[('pending', 'Pending'), ('verified', 'Verified'), ('failed', 'Failed')]  
    - **Name:** verification_method  
**Type:** String  
**Attributes:** char  
    - **Name:** verification_code  
**Type:** String  
**Attributes:** char  
    - **Name:** audience_metrics  
**Type:** Text  
**Attributes:** fields.Text (for JSON)  
    
**Methods:**
    
    - **Name:** verify_ownership  
**Parameters:**
    
    - self
    - method
    - verification_data=None
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** _validate_handle_uniqueness_per_platform  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private|@api.constrains('handle', 'platform', 'influencer_profile_id')  
    - **Name:** _validate_social_media_url_format  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private|@api.constrains('url', 'platform')  
    
**Implemented Features:**
    
    - Social Media Profile Management
    - Ownership Verification Logic
    - Handle Uniqueness
    
**Requirement Ids:**
    
    - REQ-IOKYC-002
    - REQ-IOKYC-006
    - REQ-DMG-001
    - REQ-DMG-002
    - REQ-DMG-014
    - REQ-DMG-015
    
**Purpose:** Manages influencer social media profiles and their verification.  
**Logic Description:** Stores social media details. Implements uniqueness constraint for handle per platform per influencer. Includes methods for triggering and processing ownership verification (e.g., OAuth, code in bio) (REQ-IOKYC-006). Validation for URL formats.  
**Documentation:**
    
    - **Summary:** Model for influencer social media accounts, including verification processes.
    
**Namespace:** odoo.addons.influence_gen_services.models.social_media_profile  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/kyc_data.py  
**Description:** Odoo model for KYC Data. Manages submitted identification documents, verification details, status, and reviewer information. Implements logic for KYC verification workflows.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** kyc_data  
**Type:** Model  
**Relative Path:** models/kyc_data.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** influencer_profile_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.influencer_profile'  
    - **Name:** document_type  
**Type:** String  
**Attributes:** char  
    - **Name:** document_front_attachment_id  
**Type:** Many2one  
**Attributes:** comodel_name='ir.attachment'  
    - **Name:** document_back_attachment_id  
**Type:** Many2one  
**Attributes:** comodel_name='ir.attachment'  
    - **Name:** verification_method  
**Type:** String  
**Attributes:** char  
    - **Name:** verification_status  
**Type:** Selection  
**Attributes:** selection=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('needs_more_info', 'Needs More Info')]  
    - **Name:** reviewer_user_id  
**Type:** Many2one  
**Attributes:** comodel_name='res.users'  
    - **Name:** reviewed_at  
**Type:** Datetime  
**Attributes:** fields.Datetime  
    - **Name:** notes  
**Type:** Text  
**Attributes:** fields.Text  
    
**Methods:**
    
    - **Name:** process_kyc_submission  
**Parameters:**
    
    - self
    - submission_data
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** approve_kyc  
**Parameters:**
    
    - self
    - reviewer_id
    - notes=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** reject_kyc  
**Parameters:**
    
    - self
    - reviewer_id
    - reason
    - notes=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** request_more_info_kyc  
**Parameters:**
    
    - self
    - reviewer_id
    - required_info
    - notes=None
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - KYC Data Management
    - KYC Verification Workflow Logic
    
**Requirement Ids:**
    
    - REQ-IOKYC-005
    - REQ-DMG-001
    - REQ-DMG-003
    
**Purpose:** Manages KYC submissions and the verification process.  
**Logic Description:** Stores references to KYC documents (likely as `ir.attachment` IDs) and details of the verification process. Implements methods for manual review outcomes (approve, reject, request more info) as per REQ-IOKYC-005. Updates overall KYC status on `InfluencerProfile`.  
**Documentation:**
    
    - **Summary:** Model for handling KYC document submissions and their verification status.
    
**Namespace:** odoo.addons.influence_gen_services.models.kyc_data  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/bank_account.py  
**Description:** Odoo model for Influencer Bank Accounts. Manages bank details, verification status, and primary account designation. Sensitive financial data is handled securely. Implements logic for bank account verification.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** bank_account  
**Type:** Model  
**Relative Path:** models/bank_account.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** influencer_profile_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.influencer_profile'  
    - **Name:** account_holder_name  
**Type:** String  
**Attributes:** char  
    - **Name:** account_number_encrypted  
**Type:** String  
**Attributes:** char (stores encrypted value)  
    - **Name:** bank_name  
**Type:** String  
**Attributes:** char  
    - **Name:** routing_number_encrypted  
**Type:** String  
**Attributes:** char (stores encrypted value)  
    - **Name:** iban_encrypted  
**Type:** String  
**Attributes:** char (stores encrypted value)  
    - **Name:** swift_code_encrypted  
**Type:** String  
**Attributes:** char (stores encrypted value)  
    - **Name:** verification_status  
**Type:** Selection  
**Attributes:** selection=[('pending', 'Pending'), ('verified', 'Verified'), ('failed', 'Failed')]  
    - **Name:** verification_method  
**Type:** String  
**Attributes:** char  
    - **Name:** is_primary  
**Type:** Boolean  
**Attributes:** fields.Boolean  
    
**Methods:**
    
    - **Name:** verify_bank_account  
**Parameters:**
    
    - self
    - method
    - verification_data=None
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** set_as_primary  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _compute_decrypted_fields  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private|@api.depends_context('show_decrypted') (example)  
    
**Implemented Features:**
    
    - Bank Account Management
    - Bank Account Verification Logic
    - Secure Storage of Financial Data
    
**Requirement Ids:**
    
    - REQ-IOKYC-008
    - REQ-IPF-007
    - REQ-DMG-001
    - REQ-DMG-002
    
**Purpose:** Manages influencer bank account details and verification for payouts.  
**Logic Description:** Stores bank account information with encryption for sensitive fields. Implements logic for bank account verification (REQ-IOKYC-008) via different methods (e.g., micro-deposit, third-party). Handles setting a primary account for payouts.  
**Documentation:**
    
    - **Summary:** Model for influencer bank accounts, focusing on secure data storage and verification.
    
**Namespace:** odoo.addons.influence_gen_services.models.bank_account  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/terms_consent.py  
**Description:** Odoo model for Terms Consent. Logs influencer agreement to platform Terms of Service (ToS) and Privacy Policy, including version and timestamp.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** terms_consent  
**Type:** Model  
**Relative Path:** models/terms_consent.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** influencer_profile_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.influencer_profile'  
    - **Name:** tos_version  
**Type:** String  
**Attributes:** char  
    - **Name:** privacy_policy_version  
**Type:** String  
**Attributes:** char  
    - **Name:** consent_date  
**Type:** Datetime  
**Attributes:** fields.Datetime  
    
**Methods:**
    
    - **Name:** log_consent  
**Parameters:**
    
    - cls
    - influencer_id
    - tos_version
    - privacy_policy_version
    
**Return Type:** record  
**Attributes:** classmethod|@api.model  
    
**Implemented Features:**
    
    - Consent Logging for ToS/Privacy Policy
    
**Requirement Ids:**
    
    - REQ-IOKYC-009
    - REQ-DMG-001
    - REQ-DMG-002
    
**Purpose:** Records explicit user consent to legal documents.  
**Logic Description:** Stores the specific version of ToS and Privacy Policy agreed to by an influencer, along with the timestamp of consent (REQ-IOKYC-009). This is crucial for compliance and auditability.  
**Documentation:**
    
    - **Summary:** Model for tracking influencer consent to Terms of Service and Privacy Policy.
    
**Namespace:** odoo.addons.influence_gen_services.models.terms_consent  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/campaign.py  
**Description:** Odoo model for Campaigns. Manages campaign details, goals, KPIs, target criteria, content requirements, budget, compensation models, timelines, and usage rights. Implements logic for campaign lifecycle management and performance metric aggregation.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** campaign  
**Type:** Model  
**Relative Path:** models/campaign.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    - Service Layer (methods)
    
**Members:**
    
    - **Name:** name  
**Type:** String  
**Attributes:** char  
    - **Name:** description  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** brand_client  
**Type:** String  
**Attributes:** char  
    - **Name:** goals  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** target_criteria  
**Type:** Text  
**Attributes:** fields.Text (for JSON)  
    - **Name:** content_requirements  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** budget  
**Type:** Float  
**Attributes:** fields.Float  
    - **Name:** compensation_model_details  
**Type:** Text  
**Attributes:** fields.Text (stores specifics of the model, e.g. flat fee amount, commission rate)  
    - **Name:** compensation_model_type  
**Type:** Selection  
**Attributes:** selection=[('flat_fee', 'Flat Fee'), ('commission', 'Commission'), ('product_only', 'Product Only')]  
    - **Name:** submission_deadline  
**Type:** Datetime  
**Attributes:** fields.Datetime  
    - **Name:** start_date  
**Type:** Date  
**Attributes:** fields.Date  
    - **Name:** end_date  
**Type:** Date  
**Attributes:** fields.Date  
    - **Name:** usage_rights  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** status  
**Type:** Selection  
**Attributes:** selection=[('draft', 'Draft'), ('published', 'Published'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('archived', 'Archived'), ('cancelled', 'Cancelled')]  
    - **Name:** campaign_application_ids  
**Type:** One2many  
**Attributes:** comodel_name='influence_gen.campaign_application'  
    - **Name:** payment_record_ids  
**Type:** One2many  
**Attributes:** comodel_name='influence_gen.payment_record'  
    - **Name:** total_amount_owed_computed  
**Type:** Float  
**Attributes:** compute='_compute_total_amount_owed'  
    
**Methods:**
    
    - **Name:** action_publish_campaign  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** action_close_campaign  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** update_performance_metrics  
**Parameters:**
    
    - self
    - metrics_data
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _compute_total_amount_owed  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private|@api.depends('payment_record_ids.amount', 'payment_record_ids.status')  
    - **Name:** _validate_dates  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private|@api.constrains('start_date', 'end_date', 'submission_deadline')  
    
**Implemented Features:**
    
    - Campaign Management
    - Campaign Lifecycle
    - Performance Tracking (manual input handling)
    - Compensation Model Definition
    
**Requirement Ids:**
    
    - REQ-2-001
    - REQ-2-002
    - REQ-2-011
    - REQ-2-013
    - REQ-IPF-003
    - REQ-DMG-001
    - REQ-DMG-004
    - REQ-DMG-016
    
**Purpose:** Defines campaigns, their attributes, and associated business logic.  
**Logic Description:** Manages all aspects of a campaign as per REQ-2-001, REQ-2-002, REQ-IPF-003. Includes methods for lifecycle state transitions (e.g., publish, close). Stores content requirements and target influencer criteria. Contains logic for tracking performance manually (REQ-2-011) and calculating total amounts owed to influencers for this campaign (REQ-2-013). Implements date validations (REQ-DMG-016).  
**Documentation:**
    
    - **Summary:** Model for creating, managing, and tracking marketing campaigns.
    
**Namespace:** odoo.addons.influence_gen_services.models.campaign  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/campaign_application.py  
**Description:** Odoo model for Campaign Applications. Links influencers to campaigns, stores application status, proposals, and review details.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** campaign_application  
**Type:** Model  
**Relative Path:** models/campaign_application.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** campaign_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.campaign'  
    - **Name:** influencer_profile_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.influencer_profile'  
    - **Name:** proposal  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** status  
**Type:** Selection  
**Attributes:** selection=[('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')]  
    - **Name:** submitted_at  
**Type:** Datetime  
**Attributes:** fields.Datetime  
    - **Name:** reviewed_at  
**Type:** Datetime  
**Attributes:** fields.Datetime  
    - **Name:** reviewer_user_id  
**Type:** Many2one  
**Attributes:** comodel_name='res.users'  
    - **Name:** rejection_reason  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** content_submission_ids  
**Type:** One2many  
**Attributes:** comodel_name='influence_gen.content_submission'  
    
**Methods:**
    
    - **Name:** approve_application  
**Parameters:**
    
    - self
    - reviewer_id
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** reject_application  
**Parameters:**
    
    - self
    - reviewer_id
    - reason
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Campaign Application Management
    - Application Review Workflow
    
**Requirement Ids:**
    
    - REQ-2-007
    - REQ-DMG-001
    - REQ-DMG-005
    
**Purpose:** Manages influencer applications for campaigns.  
**Logic Description:** Tracks the status of an influencer's application to a campaign. Implements methods for administrators to approve or reject applications (REQ-2-007), updating status and logging reviewer/reason.  
**Documentation:**
    
    - **Summary:** Model handling applications made by influencers to participate in campaigns.
    
**Namespace:** odoo.addons.influence_gen_services.models.campaign_application  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/content_submission.py  
**Description:** Odoo model for Content Submissions. Manages content submitted by influencers for campaigns, including files/links, review status, feedback history, and versions. Implements content review workflow logic.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** content_submission  
**Type:** Model  
**Relative Path:** models/content_submission.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** campaign_application_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.campaign_application'  
    - **Name:** generated_image_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.generated_image'  
    - **Name:** content_attachment_id  
**Type:** Many2one  
**Attributes:** comodel_name='ir.attachment'  
    - **Name:** content_link  
**Type:** String  
**Attributes:** char  
    - **Name:** submission_date  
**Type:** Datetime  
**Attributes:** fields.Datetime  
    - **Name:** review_status  
**Type:** Selection  
**Attributes:** selection=[('pending_review', 'Pending Review'), ('revision_requested', 'Revision Requested'), ('approved', 'Approved'), ('rejected', 'Rejected')]  
    - **Name:** feedback_history_ids  
**Type:** One2many  
**Attributes:** comodel_name='influence_gen.content_feedback'  
    - **Name:** version  
**Type:** Integer  
**Attributes:** fields.Integer  
    
**Methods:**
    
    - **Name:** approve_content  
**Parameters:**
    
    - self
    - reviewer_id
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** reject_content  
**Parameters:**
    
    - self
    - reviewer_id
    - feedback_text
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** request_revision  
**Parameters:**
    
    - self
    - reviewer_id
    - feedback_text
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** submit_new_version  
**Parameters:**
    
    - self
    - new_content_data
    
**Return Type:** record  
**Attributes:** public  
    
**Implemented Features:**
    
    - Content Submission Management
    - Content Review Workflow
    - Feedback History
    
**Requirement Ids:**
    
    - REQ-2-010
    - REQ-DMG-001
    - REQ-DMG-006
    
**Purpose:** Manages content submissions by influencers and their review process.  
**Logic Description:** Tracks submitted content, its review status, and feedback. Implements methods for administrators to approve, reject, or request revisions (REQ-2-010). Handles content versioning. Links to AI generated images if applicable.  
**Documentation:**
    
    - **Summary:** Model for handling content submitted by influencers for campaigns.
    
**Namespace:** odoo.addons.influence_gen_services.models.content_submission  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/content_feedback.py  
**Description:** Odoo model for Content Feedback. Stores individual feedback entries related to content submissions.  
**Template:** Odoo Model  
**Dependancy Level:** 1  
**Name:** content_feedback  
**Type:** Model  
**Relative Path:** models/content_feedback.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** content_submission_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.content_submission'  
    - **Name:** reviewer_user_id  
**Type:** Many2one  
**Attributes:** comodel_name='res.users'  
    - **Name:** feedback_text  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** created_at  
**Type:** Datetime  
**Attributes:** fields.Datetime, default=fields.Datetime.now  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Content Feedback Logging
    
**Requirement Ids:**
    
    - REQ-2-010
    - REQ-DMG-001
    - REQ-DMG-006
    
**Purpose:** Stores feedback provided by reviewers for content submissions.  
**Logic Description:** A simple model to log individual pieces of feedback for a content submission, linking the feedback to the submission, the reviewer, and the timestamp.  
**Documentation:**
    
    - **Summary:** Model for storing feedback associated with content submissions.
    
**Namespace:** odoo.addons.influence_gen_services.models.content_feedback  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/ai_image_model.py  
**Description:** Odoo model for AI Image Models. Manages configurations for available AI image generation models, including Flux LoRA models.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** ai_image_model  
**Type:** Model  
**Relative Path:** models/ai_image_model.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** name  
**Type:** String  
**Attributes:** char  
    - **Name:** description  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** trigger_keywords  
**Type:** String  
**Attributes:** char  
    - **Name:** is_active  
**Type:** Boolean  
**Attributes:** fields.Boolean  
    - **Name:** external_model_id  
**Type:** String  
**Attributes:** char  
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Model Configuration Management
    
**Requirement Ids:**
    
    - REQ-AIGS-004
    - REQ-DMG-001
    
**Purpose:** Stores configuration details for usable AI image generation models.  
**Logic Description:** Allows administrators to define and manage AI models available in the system, including their names, descriptions, and any trigger keywords or external IDs (REQ-AIGS-004).  
**Documentation:**
    
    - **Summary:** Model for managing AI image generation model configurations.
    
**Namespace:** odoo.addons.influence_gen_services.models.ai_image_model  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/ai_image_generation_request.py  
**Description:** Odoo model for AI Image Generation Requests. Records user prompts, parameters, status, and links to generated images. Implements prompt validation, parameter handling, and quota enforcement logic.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** ai_image_generation_request  
**Type:** Model  
**Relative Path:** models/ai_image_generation_request.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    - Service Layer (methods)
    
**Members:**
    
    - **Name:** user_id  
**Type:** Many2one  
**Attributes:** comodel_name='res.users'  
    - **Name:** influencer_profile_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.influencer_profile'  
    - **Name:** campaign_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.campaign'  
    - **Name:** prompt  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** negative_prompt  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** model_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.ai_image_model'  
    - **Name:** resolution  
**Type:** String  
**Attributes:** char  
    - **Name:** aspect_ratio  
**Type:** String  
**Attributes:** char  
    - **Name:** seed  
**Type:** Integer  
**Attributes:** fields.Integer  
    - **Name:** inference_steps  
**Type:** Integer  
**Attributes:** fields.Integer  
    - **Name:** cfg_scale  
**Type:** Float  
**Attributes:** fields.Float  
    - **Name:** status  
**Type:** Selection  
**Attributes:** selection=[('queued', 'Queued'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed'), ('cancelled', 'Cancelled')]  
    - **Name:** intended_use  
**Type:** String  
**Attributes:** char  
    - **Name:** error_details  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** n8n_execution_id  
**Type:** String  
**Attributes:** char  
    - **Name:** generated_image_ids  
**Type:** One2many  
**Attributes:** comodel_name='influence_gen.generated_image'  
    
**Methods:**
    
    - **Name:** validate_prompt_and_params  
**Parameters:**
    
    - self
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** check_user_quota  
**Parameters:**
    
    - self
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** decrement_user_quota  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** process_generation_result  
**Parameters:**
    
    - self
    - result_data
    - n8n_execution_id
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - AI Image Request Management
    - Prompt Validation
    - Quota Enforcement
    - Parameter Handling
    
**Requirement Ids:**
    
    - REQ-AIGS-002
    - REQ-AIGS-003
    - REQ-AIGS-004
    - REQ-AIGS-007
    - REQ-AIGS-010
    - REQ-DMG-001
    - REQ-DMG-007
    - REQ-DMG-023
    
**Purpose:** Manages AI image generation requests and associated business logic.  
**Logic Description:** Stores details of each AI image generation request. Implements prompt moderation/filtering logic (REQ-AIGS-003), configurable parameter handling (REQ-AIGS-004), and user/role-based quota enforcement (REQ-AIGS-002, REQ-AIGS-007). Updates status based on N8N callback.  
**Documentation:**
    
    - **Summary:** Model for handling AI image generation requests, including validation and quota checks.
    
**Namespace:** odoo.addons.influence_gen_services.models.ai_image_generation_request  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/generated_image.py  
**Description:** Odoo model for Generated AI Images. Stores metadata, storage links, associations, usage rights, and retention flags for AI-generated images. Implements logic for hash calculation and retention policy application.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** generated_image  
**Type:** Model  
**Relative Path:** models/generated_image.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** request_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.ai_image_generation_request'  
    - **Name:** storage_attachment_id  
**Type:** Many2one  
**Attributes:** comodel_name='ir.attachment'  
    - **Name:** file_format  
**Type:** String  
**Attributes:** char  
    - **Name:** file_size  
**Type:** Integer  
**Attributes:** fields.Integer  
    - **Name:** width  
**Type:** Integer  
**Attributes:** fields.Integer  
    - **Name:** height  
**Type:** Integer  
**Attributes:** fields.Integer  
    - **Name:** hash_value  
**Type:** String  
**Attributes:** char  
    - **Name:** retention_category  
**Type:** String  
**Attributes:** char  
    - **Name:** usage_rights_details  
**Type:** Text  
**Attributes:** fields.Text  
    
**Methods:**
    
    - **Name:** calculate_and_store_hash  
**Parameters:**
    
    - self
    - image_binary_data
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** apply_retention_policy  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Generated Image Metadata Management
    - Image Hash Calculation
    - Retention Policy Application for Images
    
**Requirement Ids:**
    
    - REQ-AIGS-006
    - REQ-AIGS-010
    - REQ-AIGS-011
    - REQ-DRH-005
    - REQ-DMG-001
    - REQ-DMG-008
    
**Purpose:** Manages metadata and lifecycle of AI-generated images.  
**Logic Description:** Stores metadata for each generated image, including a secure storage link (likely `ir.attachment` ID) (REQ-AIGS-006, REQ-AIGS-010). Implements logic to calculate and store an image hash for integrity/deduplication. Manages retention flags and applies retention policies (REQ-AIGS-011, REQ-DRH-005).  
**Documentation:**
    
    - **Summary:** Model for storing metadata and managing AI-generated images.
    
**Namespace:** odoo.addons.influence_gen_services.models.generated_image  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/payment_record.py  
**Description:** Odoo model for Payment Records. Manages influencer payment details, status, and links to campaigns/deliverables. Implements logic for calculating amounts owed and initiating payment requests (interfacing with Odoo Accounting integration).  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** payment_record  
**Type:** Model  
**Relative Path:** models/payment_record.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    - Service Layer (methods)
    
**Members:**
    
    - **Name:** influencer_profile_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.influencer_profile'  
    - **Name:** campaign_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.campaign'  
    - **Name:** content_submission_id  
**Type:** Many2one  
**Attributes:** comodel_name='influence_gen.content_submission'  
    - **Name:** amount  
**Type:** Float  
**Attributes:** fields.Float  
    - **Name:** currency_id  
**Type:** Many2one  
**Attributes:** comodel_name='res.currency'  
    - **Name:** status  
**Type:** Selection  
**Attributes:** selection=[('pending_approval', 'Pending Approval'), ('approved', 'Approved for Payment'), ('processing', 'Processing'), ('paid', 'Paid'), ('failed', 'Failed'), ('cancelled', 'Cancelled')]  
    - **Name:** transaction_id_external  
**Type:** String  
**Attributes:** char  
    - **Name:** payment_method  
**Type:** String  
**Attributes:** char  
    - **Name:** due_date  
**Type:** Date  
**Attributes:** fields.Date  
    - **Name:** paid_date  
**Type:** Date  
**Attributes:** fields.Date  
    - **Name:** odoo_vendor_bill_id  
**Type:** Many2one  
**Attributes:** comodel_name='account.move' (Odoo's journal entry/vendor bill model)  
    
**Methods:**
    
    - **Name:** calculate_payment_amount  
**Parameters:**
    
    - cls
    - campaign_id
    - influencer_id
    - content_submission_id=None
    
**Return Type:** Float  
**Attributes:** classmethod|@api.model  
    - **Name:** create_payment_from_campaign_deliverable  
**Parameters:**
    
    - cls
    - content_submission_id
    
**Return Type:** record  
**Attributes:** classmethod|@api.model  
    - **Name:** mark_as_paid  
**Parameters:**
    
    - self
    - transaction_id
    - paid_date
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** initiate_payment_processing  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public (triggers creation of vendor bill via accounting integration service)  
    
**Implemented Features:**
    
    - Payment Record Management
    - Payment Amount Calculation
    - Payment Status Tracking
    - Integration with Accounting (data preparation)
    
**Requirement Ids:**
    
    - REQ-2-013
    - REQ-2-014
    - REQ-2-015
    - REQ-IPF-004
    - REQ-IPF-005
    - REQ-IPF-007
    - REQ-DMG-001
    - REQ-DMG-009
    
**Purpose:** Manages financial records for influencer payments.  
**Logic Description:** Stores details of payments owed and made to influencers (REQ-IPF-007). Implements logic to calculate amounts owed based on campaign compensation models and approved deliverables (REQ-2-013, REQ-IPF-004). Handles status updates (REQ-2-015) and prepares data for generating payment requests/batches for Odoo's accounting module (REQ-2-014, REQ-IPF-005).  
**Documentation:**
    
    - **Summary:** Model for tracking and managing influencer payments and financial records.
    
**Namespace:** odoo.addons.influence_gen_services.models.payment_record  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/audit_log_entry.py  
**Description:** Odoo model for Audit Log Entries. Stores records of significant system events and user actions for security, compliance, and troubleshooting. This model itself primarily defines the storage structure; other models/services create entries.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** audit_log_entry  
**Type:** Model  
**Relative Path:** models/audit_log_entry.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** timestamp  
**Type:** Datetime  
**Attributes:** fields.Datetime, default=fields.Datetime.now  
    - **Name:** event_type  
**Type:** String  
**Attributes:** char  
    - **Name:** actor_user_id  
**Type:** Many2one  
**Attributes:** comodel_name='res.users'  
    - **Name:** target_model_name  
**Type:** String  
**Attributes:** char  
    - **Name:** target_record_id  
**Type:** Integer  
**Attributes:** fields.Integer  
    - **Name:** action_performed  
**Type:** String  
**Attributes:** char  
    - **Name:** details  
**Type:** Text  
**Attributes:** fields.Text (for JSON-like data)  
    - **Name:** ip_address  
**Type:** String  
**Attributes:** char  
    
**Methods:**
    
    - **Name:** create_log_entry  
**Parameters:**
    
    - cls
    - event_type
    - actor_user_id
    - action_performed
    - target_model_name=None
    - target_record_id=None
    - details=None
    - ip_address=None
    
**Return Type:** record  
**Attributes:** classmethod|@api.model  
    
**Implemented Features:**
    
    - Audit Log Storage Structure
    - Audit Log Creation Helper
    
**Requirement Ids:**
    
    - REQ-ATEL-005
    - REQ-ATEL-006
    - REQ-DMG-001
    
**Purpose:** Defines the structure for storing audit trail records.  
**Logic Description:** This model provides the database table structure for audit log entries as per REQ-ATEL-006. It includes a helper class method `create_log_entry` that other services and models can call to consistently create new audit records (REQ-ATEL-005).  
**Documentation:**
    
    - **Summary:** Model for storing audit trail entries of significant system events.
    
**Namespace:** odoo.addons.influence_gen_services.models.audit_log_entry  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/platform_setting.py  
**Description:** Odoo model for Platform Settings. Manages platform-wide configurations and business rule parameters.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** platform_setting  
**Type:** Model  
**Relative Path:** models/platform_setting.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** key  
**Type:** String  
**Attributes:** char, index=True, unique=True  
    - **Name:** value  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** data_type  
**Type:** Selection  
**Attributes:** selection=[('string', 'String'), ('integer', 'Integer'), ('float', 'Float'), ('boolean', 'Boolean'), ('json', 'JSON')]  
    - **Name:** description  
**Type:** Text  
**Attributes:** fields.Text  
    
**Methods:**
    
    - **Name:** get_setting  
**Parameters:**
    
    - cls
    - key_name
    - default_value=None
    
**Return Type:** any  
**Attributes:** classmethod|@api.model  
    - **Name:** set_setting  
**Parameters:**
    
    - cls
    - key_name
    - value
    - data_type
    - description=None
    
**Return Type:** record  
**Attributes:** classmethod|@api.model  
    
**Implemented Features:**
    
    - Platform Configuration Management
    - Business Rule Parameter Storage
    
**Requirement Ids:**
    
    - REQ-AIGS-002
    - REQ-AIGS-003
    - REQ-AIGS-004
    - REQ-DRH-001
    - REQ-DMG-001
    
**Purpose:** Provides a generic way to store and retrieve platform-level configurations.  
**Logic Description:** A key-value store for various platform settings, including AI quotas (REQ-AIGS-002), prompt moderation rules (REQ-AIGS-003), AI parameter defaults/ranges (REQ-AIGS-004), and data retention policy parameters (REQ-DRH-001). Includes methods to easily get/set settings.  
**Documentation:**
    
    - **Summary:** Model for managing global platform configuration settings.
    
**Namespace:** odoo.addons.influence_gen_services.models.platform_setting  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/data_retention_policy.py  
**Description:** Odoo model for Data Retention Policies. Defines retention periods for different data categories and links to rules for disposition.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** data_retention_policy  
**Type:** Model  
**Relative Path:** models/data_retention_policy.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** name  
**Type:** String  
**Attributes:** char  
    - **Name:** data_category  
**Type:** Selection  
**Attributes:** selection=[('pii', 'PII'), ('kyc', 'KYC Documents'), ('campaign_data', 'Campaign Data'), ('generated_images', 'Generated Images'), ('n8n_logs', 'N8N Logs'), ('system_logs', 'System Logs'), ('audit_logs', 'Audit Logs')]  
    - **Name:** retention_period_days  
**Type:** Integer  
**Attributes:** fields.Integer  
    - **Name:** disposition_action  
**Type:** Selection  
**Attributes:** selection=[('delete', 'Secure Delete'), ('anonymize', 'Anonymize'), ('archive', 'Archive')]  
    - **Name:** is_active  
**Type:** Boolean  
**Attributes:** fields.Boolean, default=True  
    - **Name:** description  
**Type:** Text  
**Attributes:** fields.Text  
    
**Methods:**
    
    - **Name:** get_active_policy_for_category  
**Parameters:**
    
    - cls
    - data_category
    
**Return Type:** record  
**Attributes:** classmethod|@api.model  
    
**Implemented Features:**
    
    - Data Retention Policy Definition
    
**Requirement Ids:**
    
    - REQ-DRH-001
    - REQ-DRH-005
    - REQ-DRH-006
    - REQ-IPF-008
    - REQ-AIGS-011
    - REQ-DMG-001
    
**Purpose:** Defines data retention policies for various data categories within the system.  
**Logic Description:** Allows administrators to define retention periods and disposition actions for different types of data (REQ-DRH-001, REQ-DRH-005, REQ-DRH-006, REQ-IPF-008, REQ-AIGS-011). These policies are then used by data management services or scheduled jobs to enforce retention.  
**Documentation:**
    
    - **Summary:** Model for defining and managing data retention policies.
    
**Namespace:** odoo.addons.influence_gen_services.models.data_retention_policy  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/models/area_of_influence.py  
**Description:** Odoo model for Area of Influence. Stores distinct areas of influence/niches for influencers.  
**Template:** Odoo Model  
**Dependancy Level:** 0  
**Name:** area_of_influence  
**Type:** Model  
**Relative Path:** models/area_of_influence.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    - Active Record
    
**Members:**
    
    - **Name:** name  
**Type:** String  
**Attributes:** char, required=True, index=True, unique=True  
    - **Name:** description  
**Type:** Text  
**Attributes:** fields.Text  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Area of Influence Management
    
**Requirement Ids:**
    
    - REQ-DMG-001
    - REQ-DMG-002
    
**Purpose:** Defines categories for influencer expertise or niche.  
**Logic Description:** A simple lookup table to store and manage areas of influence, used in Many2many relationship with InfluencerProfile.  
**Documentation:**
    
    - **Summary:** Model for storing distinct areas of influence/niches.
    
**Namespace:** odoo.addons.influence_gen_services.models.area_of_influence  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/__init__.py  
**Description:** Initializes the 'services' Python package, importing service classes for business process orchestration.  
**Template:** Python Package Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** services/__init__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Loading
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'services' directory a Python package and exposes service classes.  
**Logic Description:** Contains import statements for each service file (e.g., 'from . import onboarding_service').  
**Documentation:**
    
    - **Summary:** Imports all service classes for the InfluenceGen services module.
    
**Namespace:** odoo.addons.influence_gen_services.services  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_services/services/onboarding_service.py  
**Description:** Service class for orchestrating the influencer onboarding process, including KYC, social media, and bank account verifications, and ToS consent.  
**Template:** Python Service  
**Dependancy Level:** 1  
**Name:** onboarding_service  
**Type:** Service  
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
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** process_registration_submission  
**Parameters:**
    
    - self
    - influencer_data
    
**Return Type:** record (InfluencerProfile)  
**Attributes:** public  
    - **Name:** handle_kyc_document_submission  
**Parameters:**
    
    - self
    - influencer_id
    - document_data
    
**Return Type:** record (KYCData)  
**Attributes:** public  
    - **Name:** handle_kyc_review_decision  
**Parameters:**
    
    - self
    - kyc_data_id
    - decision
    - reviewer_id
    - notes=None
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** initiate_social_media_verification  
**Parameters:**
    
    - self
    - social_profile_id
    
**Return Type:** dict (verification_details)  
**Attributes:** public  
    - **Name:** confirm_social_media_verification  
**Parameters:**
    
    - self
    - social_profile_id
    - verification_input
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** initiate_bank_account_verification  
**Parameters:**
    
    - self
    - bank_account_id
    
**Return Type:** dict (verification_details)  
**Attributes:** public  
    - **Name:** confirm_bank_account_verification  
**Parameters:**
    
    - self
    - bank_account_id
    - verification_input
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** record_terms_consent  
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
    
**Return Type:** Boolean  
**Attributes:** public  
    
**Implemented Features:**
    
    - Onboarding Orchestration
    - KYC Workflow Management
    - Social Media Verification Flow
    - Bank Account Verification Flow
    - Account Activation Logic
    
**Requirement Ids:**
    
    - REQ-IOKYC-002
    - REQ-IOKYC-005
    - REQ-IOKYC-006
    - REQ-IOKYC-008
    - REQ-IOKYC-009
    - REQ-IOKYC-012
    
**Purpose:** Orchestrates the multi-step influencer onboarding and verification process.  
**Logic Description:** Coordinates interactions between InfluencerProfile, KYCData, SocialMediaProfile, BankAccount, and TermsConsent models. Manages the state transitions of the onboarding process, ensuring all steps are completed before activating an account (REQ-IOKYC-012). Interacts with notification services for status updates.  
**Documentation:**
    
    - **Summary:** Service responsible for managing the end-to-end influencer onboarding lifecycle.
    
**Namespace:** odoo.addons.influence_gen_services.services.onboarding_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/campaign_service.py  
**Description:** Service class for orchestrating campaign management processes, including creation, application review, content submission review, and performance metric aggregation.  
**Template:** Python Service  
**Dependancy Level:** 1  
**Name:** campaign_service  
**Type:** Service  
**Relative Path:** services/campaign_service.py  
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
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** create_campaign  
**Parameters:**
    
    - self
    - campaign_data
    
**Return Type:** record (Campaign)  
**Attributes:** public  
    - **Name:** update_campaign_status  
**Parameters:**
    
    - self
    - campaign_id
    - new_status
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** process_campaign_application  
**Parameters:**
    
    - self
    - influencer_id
    - campaign_id
    - proposal_data
    
**Return Type:** record (CampaignApplication)  
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
    - **Name:** handle_content_submission  
**Parameters:**
    
    - self
    - application_id
    - content_data
    
**Return Type:** record (ContentSubmission)  
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
    - **Name:** record_campaign_performance_metrics  
**Parameters:**
    
    - self
    - campaign_id
    - influencer_id
    - submission_id
    - metrics_data
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Campaign Orchestration
    - Application Review Workflow
    - Content Review Workflow
    - Performance Metric Handling
    
**Requirement Ids:**
    
    - REQ-2-001
    - REQ-2-002
    - REQ-2-007
    - REQ-2-010
    - REQ-2-011
    
**Purpose:** Orchestrates the lifecycle and operational aspects of campaigns.  
**Logic Description:** Manages campaign creation (REQ-2-001, REQ-2-002), application review (REQ-2-007), content submission and review (REQ-2-010). Coordinates with Campaign, CampaignApplication, and ContentSubmission models. Handles input of performance metrics (REQ-2-011).  
**Documentation:**
    
    - **Summary:** Service for managing campaign creation, influencer participation, content, and performance.
    
**Namespace:** odoo.addons.influence_gen_services.services.campaign_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/ai_image_service.py  
**Description:** Service class for handling AI image generation business logic, such as prompt validation, parameter processing, quota management, and AI-generated image metadata management.  
**Template:** Python Service  
**Dependancy Level:** 1  
**Name:** ai_image_service  
**Type:** Service  
**Relative Path:** services/ai_image_service.py  
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
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** prepare_ai_generation_request  
**Parameters:**
    
    - self
    - user_id
    - prompt_data
    - parameter_data
    
**Return Type:** record (AIImageGenerationRequest) or error_dict  
**Attributes:** public  
    - **Name:** process_ai_generation_callback  
**Parameters:**
    
    - self
    - request_id
    - image_data
    - n8n_execution_id
    
**Return Type:** record (GeneratedImage) or error_dict  
**Attributes:** public  
    - **Name:** get_user_ai_quota_status  
**Parameters:**
    
    - self
    - user_id
    
**Return Type:** dict  
**Attributes:** public  
    - **Name:** manage_ai_model_configurations  
**Parameters:**
    
    - self
    - action ('add'|'update'|'deactivate')
    - model_data
    
**Return Type:** record (AIImageModel) or Boolean  
**Attributes:** public  
    
**Implemented Features:**
    
    - AI Request Preparation
    - AI Callback Processing
    - AI Quota Management
    - AI Model Configuration Logic
    
**Requirement Ids:**
    
    - REQ-AIGS-002
    - REQ-AIGS-003
    - REQ-AIGS-004
    - REQ-AIGS-006
    - REQ-AIGS-007
    - REQ-AIGS-010
    - REQ-AIGS-011
    
**Purpose:** Encapsulates business logic related to AI image generation requests and results.  
**Logic Description:** Handles validation of AI prompts (REQ-AIGS-003), checks and updates user quotas (REQ-AIGS-002, REQ-AIGS-007). Prepares request data for N8N. Processes callbacks from N8N, creates GeneratedImage records (REQ-AIGS-006, REQ-AIGS-010), and links them to requests. Manages AI model config logic (REQ-AIGS-004) and image retention flags (REQ-AIGS-011).  
**Documentation:**
    
    - **Summary:** Service for managing the business aspects of AI image generation.
    
**Namespace:** odoo.addons.influence_gen_services.services.ai_image_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/payment_service.py  
**Description:** Service class for orchestrating influencer payment processes, including calculating amounts owed, preparing payment batches, and interfacing with accounting integration logic.  
**Template:** Python Service  
**Dependancy Level:** 1  
**Name:** payment_service  
**Type:** Service  
**Relative Path:** services/payment_service.py  
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
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** calculate_owed_amounts_for_influencer  
**Parameters:**
    
    - self
    - influencer_id
    - campaign_id=None
    
**Return Type:** list_of_dicts (payment_details)  
**Attributes:** public  
    - **Name:** generate_payment_batch_data  
**Parameters:**
    
    - self
    - influencer_ids=None
    - campaign_id=None
    - due_date_filter=None
    
**Return Type:** dict (batch_data)  
**Attributes:** public  
    - **Name:** process_payment_batch_creation  
**Parameters:**
    
    - self
    - batch_data
    
**Return Type:** list_of_records (PaymentRecord)  
**Attributes:** public  
    - **Name:** update_payment_status_from_accounting  
**Parameters:**
    
    - self
    - payment_record_id
    - new_status
    - transaction_id=None
    - paid_date=None
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - Payment Calculation Orchestration
    - Payment Batch Preparation
    - Payment Status Update Logic
    
**Requirement Ids:**
    
    - REQ-2-013
    - REQ-2-014
    - REQ-2-015
    - REQ-IPF-003
    - REQ-IPF-004
    - REQ-IPF-005
    
**Purpose:** Orchestrates the financial processes related to influencer payments.  
**Logic Description:** Calculates amounts owed to influencers based on approved deliverables and campaign compensation models (REQ-2-013, REQ-IPF-003, REQ-IPF-004). Prepares data for generating payment requests or batches to be processed by Odoo Accounting (REQ-2-014, REQ-IPF-005). Handles updates to payment statuses (REQ-2-015).  
**Documentation:**
    
    - **Summary:** Service for managing calculations, batching, and status tracking of influencer payments.
    
**Namespace:** odoo.addons.influence_gen_services.services.payment_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/services/data_management_service.py  
**Description:** Service class for managing data governance aspects, including the execution of data retention policies, archival processes, and legal hold management.  
**Template:** Python Service  
**Dependancy Level:** 1  
**Name:** data_management_service  
**Type:** Service  
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
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** apply_data_retention_policies  
**Parameters:**
    
    - self
    - data_category=None
    
**Return Type:** dict (summary_of_actions)  
**Attributes:** public (typically called by a scheduled job)  
    - **Name:** process_pii_erasure_request  
**Parameters:**
    
    - self
    - influencer_id
    - data_scope
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** assess_pii_in_campaign_content_for_erasure  
**Parameters:**
    
    - self
    - content_submission_id
    - influencer_id
    
**Return Type:** dict (assessment_result)  
**Attributes:** public  
    - **Name:** archive_data_batch  
**Parameters:**
    
    - self
    - data_category
    - criteria
    
**Return Type:** dict (archival_summary)  
**Attributes:** public  
    - **Name:** apply_legal_hold  
**Parameters:**
    
    - self
    - entity_name
    - record_ids
    - hold_reason
    
**Return Type:** Boolean  
**Attributes:** public  
    - **Name:** lift_legal_hold  
**Parameters:**
    
    - self
    - entity_name
    - record_ids
    
**Return Type:** Boolean  
**Attributes:** public  
    
**Implemented Features:**
    
    - Data Retention Policy Enforcement
    - PII Erasure Request Processing
    - Data Archival Orchestration
    - Legal Hold Management
    
**Requirement Ids:**
    
    - REQ-DRH-001
    - REQ-DRH-002
    - REQ-DRH-003
    - REQ-DRH-004
    - REQ-DRH-005
    - REQ-DRH-006
    - REQ-DRH-007
    - REQ-DRH-009
    - REQ-IPF-008
    - REQ-AIGS-011
    
**Purpose:** Orchestrates data lifecycle management tasks like retention, archival, and legal holds.  
**Logic Description:** Implements the logic to enforce data retention policies defined in `DataRetentionPolicy` model (REQ-DRH-001, REQ-DRH-002, REQ-IPF-008, REQ-AIGS-011). Handles PII erasure requests, including assessment for campaign content (REQ-DRH-003, REQ-DRH-004). Manages data archival (REQ-DRH-007) and legal hold application/lifting (REQ-DRH-009).  
**Documentation:**
    
    - **Summary:** Service responsible for data governance, including retention, archival, and legal hold processes.
    
**Namespace:** odoo.addons.influence_gen_services.services.data_management_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/wizards/__init__.py  
**Description:** Initializes the 'wizards' Python package, importing Odoo wizard model files.  
**Template:** Python Package Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** wizards/__init__.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Wizard Loading
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'wizards' directory a Python package for Odoo transient models.  
**Logic Description:** Contains import statements for each wizard file (e.g., 'from . import data_retention_execution_wizard').  
**Documentation:**
    
    - **Summary:** Imports all wizard models for the InfluenceGen services module.
    
**Namespace:** odoo.addons.influence_gen_services.wizards  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_services/wizards/data_retention_execution_wizard.py  
**Description:** Odoo transient model (wizard) for manually triggering and configuring data retention/disposition tasks.  
**Template:** Odoo Wizard  
**Dependancy Level:** 2  
**Name:** data_retention_execution_wizard  
**Type:** Wizard  
**Relative Path:** wizards/data_retention_execution_wizard.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** data_category_filter  
**Type:** Selection  
**Attributes:** selection from DataRetentionPolicy data_category  
    - **Name:** execution_date_filter  
**Type:** Date  
**Attributes:** fields.Date  
    - **Name:** dry_run  
**Type:** Boolean  
**Attributes:** fields.Boolean  
    
**Methods:**
    
    - **Name:** action_execute_retention  
**Parameters:**
    
    - self
    
**Return Type:** dict (action or None)  
**Attributes:** public  
    
**Implemented Features:**
    
    - Manual Data Retention Trigger
    
**Requirement Ids:**
    
    - REQ-DRH-002
    
**Purpose:** Provides an administrative interface to manually initiate data retention tasks.  
**Logic Description:** A transient model allowing administrators to select data categories and filters to manually trigger the data disposition processes defined in `DataManagementService`. This is complementary to automated scheduled jobs (REQ-DRH-002). UI for this wizard would be defined in an XML file.  
**Documentation:**
    
    - **Summary:** Wizard for administrative execution of data retention processes.
    
**Namespace:** odoo.addons.influence_gen_services.wizards.data_retention_execution_wizard  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/wizards/legal_hold_management_wizard.py  
**Description:** Odoo transient model (wizard) for managing legal holds on data entities.  
**Template:** Odoo Wizard  
**Dependancy Level:** 2  
**Name:** legal_hold_management_wizard  
**Type:** Wizard  
**Relative Path:** wizards/legal_hold_management_wizard.py  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** target_model_name_selection  
**Type:** Selection  
**Attributes:** selection of relevant models  
    - **Name:** target_record_ids_char  
**Type:** String  
**Attributes:** char (comma-separated IDs)  
    - **Name:** hold_reason  
**Type:** Text  
**Attributes:** fields.Text  
    - **Name:** action_type  
**Type:** Selection  
**Attributes:** selection=[('apply', 'Apply Hold'), ('lift', 'Lift Hold')]  
    
**Methods:**
    
    - **Name:** action_process_legal_hold  
**Parameters:**
    
    - self
    
**Return Type:** dict (action or None)  
**Attributes:** public  
    
**Implemented Features:**
    
    - Legal Hold Management Interface Logic
    
**Requirement Ids:**
    
    - REQ-DRH-009
    
**Purpose:** Provides an administrative interface for applying or lifting legal holds.  
**Logic Description:** A transient model allowing administrators to specify entities and records to place under or remove from legal hold (REQ-DRH-009). Interacts with `DataManagementService` to execute the hold logic. UI for this wizard would be defined in an XML file.  
**Documentation:**
    
    - **Summary:** Wizard for administrative management of legal holds on data.
    
**Namespace:** odoo.addons.influence_gen_services.wizards.legal_hold_management_wizard  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_services/security/ir.model.access.csv  
**Description:** CSV file defining model-level access rights (read, write, create, unlink) for various security groups within Odoo.  
**Template:** Odoo Security CSV  
**Dependancy Level:** 0  
**Name:** ir.model.access.csv  
**Type:** SecurityConfiguration  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Data Access Control
    
**Requirement Ids:**
    
    - REQ-PAC-001
    - REQ-PAC-002
    - REQ-AIGS-002
    
**Purpose:** Defines permissions for Odoo security groups on InfluenceGen models.  
**Logic Description:** Standard Odoo access control file. Specifies which groups can perform CRUD operations on each model defined in this module. For example, influencers might have read/write to their own profile but not others; admins have full access. Handles REQ-PAC-001, REQ-PAC-002 implicitly by defining what configured roles can access.  
**Documentation:**
    
    - **Summary:** Defines access control lists for the InfluenceGen service models.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** odoo_modules/influence_gen_services/i18n/influence_gen_services.pot  
**Description:** Standard Odoo Portable Object Template (.pot) file. Contains all translatable strings extracted from Python code and XML views for this module.  
**Template:** Odoo POT File  
**Dependancy Level:** 0  
**Name:** influence_gen_services.pot  
**Type:** LocalizationTemplate  
**Relative Path:** i18n/influence_gen_services.pot  
**Repository Id:** REPO-IGBS-003  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Localization Support (Template)
    
**Requirement Ids:**
    
    
**Purpose:** Serves as the master template for translating module strings into different languages.  
**Logic Description:** Generated by Odoo's i18n tools, this file lists all strings marked for translation in the module's Python files and XML views. It is used by translators to create .po files for specific languages.  
**Documentation:**
    
    - **Summary:** Localization template file for the InfluenceGen services module.
    
**Namespace:** None  
**Metadata:**
    
    - **Category:** Localization
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableAdvancedKycVerification
  - EnableAutomatedPaymentBatching
  - EnableAiPromptContentModeration
  - EnableDataArchivalFeature
  
- **Database Configs:**
  
  - influence_gen.default_tos_version
  - influence_gen.default_privacy_policy_version
  - influence_gen.ai_image_default_quota_per_user
  - influence_gen.kyc_document_max_file_size_mb
  - influence_gen.data_retention_pii_days
  - influence_gen.data_retention_audit_log_days
  


---

