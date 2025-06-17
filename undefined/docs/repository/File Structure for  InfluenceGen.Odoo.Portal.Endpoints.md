# Specification

# 1. Files

- **Path:** odoo_modules/influence_gen_portal/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata, dependencies (e.g., portal, website, mail, and the core InfluenceGen business logic module), data files, and assets to be loaded.  
**Template:** Odoo Manifest Template  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Configuration  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    - REQ-DDSI-001
    
**Purpose:** Declares the InfluenceGen Portal module to Odoo, its dependencies, and assets.  
**Logic Description:** Contains a Python dictionary with keys like 'name', 'version', 'category', 'summary', 'description', 'author', 'website', 'depends', 'data', 'assets'. 'depends' should include 'portal', 'website', 'mail', and the main business logic module ID 'REPO-IGBS-003'. 'assets' section will list CSS and JS bundles.  
**Documentation:**
    
    - **Summary:** Defines the Odoo module for the InfluenceGen Portal UI, including its dependencies on other Odoo apps and custom modules, and specifies assets like CSS and JavaScript files to be loaded for the portal.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** ModuleConfiguration
    
- **Path:** odoo_modules/influence_gen_portal/__init__.py  
**Description:** Python package initializer for the Odoo module. Imports sub-packages and modules like controllers.  
**Template:** Python Init Template  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - REQ-DDSI-001
    
**Purpose:** Makes Python modules within this Odoo module importable.  
**Logic Description:** Imports the 'controllers' sub-package: 'from . import controllers'.  
**Documentation:**
    
    - **Summary:** Initializes the 'influence_gen_portal' Python package, primarily importing its 'controllers' sub-package to make them available to Odoo.
    
**Namespace:** odoo.addons.influence_gen_portal  
**Metadata:**
    
    - **Category:** ModuleConfiguration
    
- **Path:** odoo_modules/influence_gen_portal/controllers/__init__.py  
**Description:** Python package initializer for the controllers directory. Imports all portal controller files.  
**Template:** Python Init Template  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** controllers/__init__.py  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Controller Aggregation
    
**Requirement Ids:**
    
    - REQ-DDSI-001
    
**Purpose:** Aggregates all controller modules for easier import by the main module __init__.py.  
**Logic Description:** Imports specific controller modules: 'from . import portal_main_controller', 'from . import portal_onboarding_controller', 'from . import portal_campaign_controller', 'from . import portal_ai_image_controller'.  
**Documentation:**
    
    - **Summary:** Initializes the 'controllers' Python package, importing all specific portal controller classes to make them discoverable by Odoo's routing mechanism.
    
**Namespace:** odoo.addons.influence_gen_portal.controllers  
**Metadata:**
    
    - **Category:** Controller
    
- **Path:** odoo_modules/influence_gen_portal/controllers/portal_main_controller.py  
**Description:** Odoo HTTP controller for main influencer portal pages: dashboard, profile management, performance dashboard access, AI image generator entry point. Renders QWeb templates and interacts with business services.  
**Template:** Odoo Controller Template  
**Dependancy Level:** 2  
**Name:** portal_main_controller  
**Type:** Controller  
**Relative Path:** controllers/portal_main_controller.py  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    - **Name:** influencer_dashboard  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_profile  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** update_influencer_profile  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_payment_info  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** update_influencer_payment_info  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_ai_image_generator  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_performance_dashboard  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_consent_management  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_accept_terms  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    
**Implemented Features:**
    
    - Influencer Dashboard UI
    - Profile Management UI
    - Payment Information UI
    - AI Image Generator UI Entry
    - Performance Dashboard UI
    - Consent Management UI
    
**Requirement Ids:**
    
    - REQ-IPDPM-001
    - REQ-IPDPM-002
    - REQ-IPDPM-003
    - REQ-IPDPM-005
    - REQ-IPDPM-006
    - REQ-IPDPM-007
    - REQ-IPDPM-011
    - REQ-IOKYC-009
    - REQ-IOKYC-010
    - REQ-UIUX-017
    - REQ-IPF-001
    
**Purpose:** Handles requests for core influencer portal pages, fetches necessary data via business services, and renders appropriate QWeb templates.  
**Logic Description:** Each method defines an HTTP route (e.g., '/my/dashboard'). Methods retrieve influencer-specific data (profile, campaigns, payments, AI quota) from business services (REPO-IGBS-003). Renders QWeb templates, passing data for display. POST methods handle form submissions for profile/payment updates.  
**Documentation:**
    
    - **Summary:** Manages routing and data preparation for key influencer portal sections like the dashboard, profile editing, payment details, AI tool access, and performance views. Interacts with business logic services for data retrieval and updates.
    
**Namespace:** odoo.addons.influence_gen_portal.controllers.portal_main_controller  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/controllers/portal_onboarding_controller.py  
**Description:** Odoo HTTP controller for influencer onboarding: registration, KYC data submission, social media and bank account management during onboarding. Renders QWeb templates and interacts with business services.  
**Template:** Odoo Controller Template  
**Dependancy Level:** 2  
**Name:** portal_onboarding_controller  
**Type:** Controller  
**Relative Path:** controllers/portal_onboarding_controller.py  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    - **Name:** influencer_register  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** process_registration  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_kyc_submission  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** process_kyc_documents  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_social_media_setup  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** process_social_media_links  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_bank_account_setup  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** process_bank_account_details  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** influencer_tos_agreement  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** process_tos_agreement  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** check_kyc_status  
**Parameters:**
    
    - self
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    
**Implemented Features:**
    
    - Influencer Registration UI
    - KYC Data Submission UI
    - Social Media Account Setup UI
    - Bank Account Setup UI
    - ToS Agreement UI
    - KYC Status Display
    
**Requirement Ids:**
    
    - REQ-IOKYC-001
    - REQ-IOKYC-002
    - REQ-IOKYC-003
    - REQ-IOKYC-004
    - REQ-IOKYC-005
    - REQ-IOKYC-006
    - REQ-IOKYC-007
    - REQ-IOKYC-008
    - REQ-IOKYC-009
    - REQ-IOKYC-010
    - REQ-IOKYC-014
    - REQ-IPF-001
    
**Purpose:** Manages HTTP requests for all steps of the influencer onboarding process, including form display and data submission.  
**Logic Description:** Defines routes for each onboarding step (e.g., '/influencer/register', '/my/kyc/submit'). GET methods render forms. POST methods process submitted data, call business services for validation and storage, handle file uploads for KYC, and redirect to next steps or display status.  
**Documentation:**
    
    - **Summary:** Handles web requests for the influencer registration and KYC journey. This includes displaying forms for personal details, document uploads, social media links, bank accounts, and ToS agreement, and processing submitted data.
    
**Namespace:** odoo.addons.influence_gen_portal.controllers.portal_onboarding_controller  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/controllers/portal_campaign_controller.py  
**Description:** Odoo HTTP controller for influencer campaign interactions: campaign discovery, viewing details, applying for campaigns, and content submission. Renders QWeb templates and interacts with business services.  
**Template:** Odoo Controller Template  
**Dependancy Level:** 2  
**Name:** portal_campaign_controller  
**Type:** Controller  
**Relative Path:** controllers/portal_campaign_controller.py  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    - **Name:** campaign_discovery  
**Parameters:**
    
    - self
    - page=1
    - search=None
    - sort_by=None
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** campaign_details  
**Parameters:**
    
    - self
    - campaign_id
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** campaign_apply  
**Parameters:**
    
    - self
    - campaign_id
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** process_campaign_application  
**Parameters:**
    
    - self
    - campaign_id
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** campaign_content_submission_form  
**Parameters:**
    
    - self
    - campaign_application_id
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    - **Name:** process_content_submission  
**Parameters:**
    
    - self
    - campaign_application_id
    - **post
    
**Return Type:** odoo.http.Response  
**Attributes:** public  
    
**Implemented Features:**
    
    - Campaign Discovery UI
    - Campaign Details UI
    - Campaign Application UI
    - Content Submission UI
    
**Requirement Ids:**
    
    - REQ-IPDPM-004
    - REQ-2-004
    - REQ-2-005
    - REQ-2-006
    - REQ-2-009
    - REQ-2-011
    - REQ-2-016
    - REQ-UIUX-018
    
**Purpose:** Handles HTTP requests related to influencer participation in campaigns.  
**Logic Description:** Defines routes for campaign listing, details, application, and content submission. Retrieves campaign data using business services, handles search/filter/sort parameters, renders QWeb templates. POST methods process applications and content uploads.  
**Documentation:**
    
    - **Summary:** Manages routes for influencers to discover, view, apply for, and submit content to campaigns. It fetches campaign data, handles application submissions, and manages content uploads through the portal.
    
**Namespace:** odoo.addons.influence_gen_portal.controllers.portal_campaign_controller  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/controllers/portal_ai_image_controller.py  
**Description:** Odoo HTTP controller specifically for AJAX interactions related to AI image generation, such as initiating generation and checking status. This might be merged into portal_main_controller if interactions are simple.  
**Template:** Odoo Controller Template  
**Dependancy Level:** 2  
**Name:** portal_ai_image_controller  
**Type:** Controller  
**Relative Path:** controllers/portal_ai_image_controller.py  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    - WebhookIntegration
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initiate_ai_image_generation  
**Parameters:**
    
    - self
    - **params
    
**Return Type:** odoo.http.Response  
**Attributes:** public|json  
    - **Name:** get_ai_image_generation_status  
**Parameters:**
    
    - self
    - request_id
    - **kw
    
**Return Type:** odoo.http.Response  
**Attributes:** public|json  
    
**Implemented Features:**
    
    - AI Image Generation Initiation
    - AI Image Generation Status Check
    
**Requirement Ids:**
    
    - REQ-AIGS-001
    - REQ-AIGS-005
    - REQ-AIGS-008
    - REQ-16-006
    
**Purpose:** Handles asynchronous AJAX requests from the AI image generation UI to trigger generation and poll for status updates.  
**Logic Description:** Defines JSON routes. 'initiate_ai_image_generation' takes prompts/params, calls the business service (which then calls N8N), and returns a request ID. 'get_ai_image_generation_status' polls the status of a given request ID.  
**Documentation:**
    
    - **Summary:** Provides backend HTTP endpoints for the AI image generation feature. This includes an endpoint to receive generation requests from the UI and an endpoint to query the status of ongoing generation tasks.
    
**Namespace:** odoo.addons.influence_gen_portal.controllers.portal_ai_image_controller  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_layout_templates.xml  
**Description:** QWeb templates defining the main layout structure for the influencer portal, including header, footer, navigation menus, and common portal elements.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 2  
**Name:** portal_layout_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_layout_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Portal Main Layout
    - Portal Navigation
    
**Requirement Ids:**
    
    - REQ-IPDPM-001
    - REQ-UIUX-001
    - REQ-UIUX-002
    - REQ-UIUX-010
    - REQ-UIUX-012
    
**Purpose:** Provides the consistent look and feel and navigation structure for all influencer portal pages.  
**Logic Description:** Defines templates like 'influence_gen_portal.portal_layout' inheriting from Odoo's 'portal.portal_layout'. Adds InfluenceGen specific menu items (Dashboard, Profile, Campaigns, AI Tools, Payments, Performance, Help/Documentation). Ensures responsive structure.  
**Documentation:**
    
    - **Summary:** Contains QWeb templates for the overall structure of the influencer portal. This includes the main portal layout, navigation bar with links to different sections, header, and footer, ensuring a consistent experience.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_dashboard_templates.xml  
**Description:** QWeb templates for the influencer's personalized dashboard, displaying summary information and quick links.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 3  
**Name:** portal_dashboard_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_dashboard_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Influencer Dashboard UI
    
**Requirement Ids:**
    
    - REQ-IPDPM-002
    - REQ-UIUX-019
    
**Purpose:** Renders the main dashboard page for logged-in influencers.  
**Logic Description:** Defines a template for '/my/dashboard'. Displays widgets for active campaigns, pending tasks (KYC, content submission), recent notifications, AI image quota status, and quick links to key portal sections.  
**Documentation:**
    
    - **Summary:** QWeb templates for rendering the influencer's personalized dashboard. This will show summaries of active campaigns, pending tasks, recent notifications, AI generation quota, and quick access links.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_profile_templates.xml  
**Description:** QWeb templates for influencer profile viewing and editing, KYC status display, consent records, and payment information management.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 3  
**Name:** portal_profile_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_profile_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Profile Management UI
    - KYC Status Display
    - Consent Records UI
    - Payment Information UI
    
**Requirement Ids:**
    
    - REQ-IPDPM-003
    - REQ-IPDPM-007
    - REQ-IPDPM-011
    - REQ-IOKYC-010
    - REQ-UIUX-017
    - REQ-IPF-001
    
**Purpose:** Renders the influencer profile page with forms for viewing/editing data and displaying status information.  
**Logic Description:** Defines templates for '/my/profile'. Includes sections for personal details, contact info, professional info, social media links (potentially using an OWL component), KYC status, bank account details, payment history, and ToS/Privacy Policy consent history. Forms for editing relevant data fields.  
**Documentation:**
    
    - **Summary:** Contains QWeb templates for the influencer's profile page. This includes sections to view and edit personal, contact, and professional information, manage social media links, view KYC status, see payment details and history, and review consent to terms.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_onboarding_templates.xml  
**Description:** QWeb templates for the multi-step influencer onboarding process, including registration form, KYC document upload, social media link input, bank details input, and ToS agreement.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 3  
**Name:** portal_onboarding_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_onboarding_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Influencer Registration UI
    - KYC Data Submission UI
    - Social Media Account Setup UI
    - Bank Account Setup UI
    - ToS Agreement UI
    
**Requirement Ids:**
    
    - REQ-IOKYC-001
    - REQ-IOKYC-002
    - REQ-IOKYC-004
    - REQ-IOKYC-006
    - REQ-IOKYC-007
    - REQ-IOKYC-008
    - REQ-IOKYC-009
    
**Purpose:** Provides the UI for each step of the influencer registration and KYC process.  
**Logic Description:** Templates for '/influencer/register', '/my/kyc/submit', '/my/social/setup', '/my/bank/setup', '/my/tos/agree'. Forms for each data collection step, including file upload widgets for KYC documents. Clear instructions and progress indicators. Incorporates OWL components for dynamic fields or validation if needed.  
**Documentation:**
    
    - **Summary:** QWeb templates for the various stages of the influencer onboarding process. Includes forms for registration, personal information, social media profiles, KYC document uploads, bank account details submission, and agreement to terms of service.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_campaign_discovery_templates.xml  
**Description:** QWeb templates for campaign discovery, including campaign listing, search fields, filter options, and sorting controls.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 3  
**Name:** portal_campaign_discovery_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_campaign_discovery_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign Discovery UI
    
**Requirement Ids:**
    
    - REQ-2-004
    - REQ-UIUX-018
    
**Purpose:** Renders the page where influencers can find and browse available campaigns.  
**Logic Description:** Template for '/my/campaigns'. Displays a list of campaigns (using a campaign_card_component snippet or OWL component). Includes search bar, filter controls (niche, compensation, platform), and sort options. Pagination for large lists.  
**Documentation:**
    
    - **Summary:** QWeb templates for the campaign discovery page. This will allow influencers to browse available campaigns, use search functionality, apply filters (e.g., by niche, compensation), and sort the campaign list.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_campaign_details_templates.xml  
**Description:** QWeb template for displaying detailed information about a specific campaign.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 3  
**Name:** portal_campaign_details_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_campaign_details_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign Details UI
    
**Requirement Ids:**
    
    - REQ-2-005
    
**Purpose:** Renders the detailed view of a selected campaign.  
**Logic Description:** Template for '/my/campaigns/<campaign_id>'. Displays comprehensive campaign details: name, description, brand, goals, content requirements, compensation, deadlines, usage rights. 'Apply' button if eligible.  
**Documentation:**
    
    - **Summary:** QWeb template to show the full details of a selected campaign, including description, brand, goals, content requirements, compensation, deadlines, and usage rights.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_campaign_application_templates.xml  
**Description:** QWeb template for the campaign application form, potentially including proposal input.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 3  
**Name:** portal_campaign_application_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_campaign_application_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign Application UI
    
**Requirement Ids:**
    
    - REQ-2-006
    
**Purpose:** Renders the form for influencers to apply to a campaign.  
**Logic Description:** Template for '/my/campaigns/<campaign_id>/apply'. Includes fields for custom proposal (if required), confirmation checkboxes for understanding requirements. Form submission handled by portal_campaign_controller.  
**Documentation:**
    
    - **Summary:** QWeb template for the campaign application form. This may include fields for a custom proposal, answers to specific questions, or confirmation of understanding campaign requirements.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_content_submission_templates.xml  
**Description:** QWeb template for the content submission form for active campaigns, including file upload and link input.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 3  
**Name:** portal_content_submission_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_content_submission_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Content Submission UI
    
**Requirement Ids:**
    
    - REQ-2-009
    - REQ-2-016
    
**Purpose:** Renders the form for influencers to submit their content for a campaign.  
**Logic Description:** Template for '/my/campaigns/submit/<campaign_application_id>'. Includes fields for text captions, file uploads (image/video), links to posts. Option to select from AI-generated images. Form submission handled by portal_campaign_controller.  
**Documentation:**
    
    - **Summary:** QWeb template for the campaign content submission interface. This allows influencers to upload content files (images, videos), submit text captions, and provide links to their posts. It also allows linking AI-generated images.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_ai_image_generator_templates.xml  
**Description:** QWeb template hosting the OWL component for AI image generation, including input fields for prompts, parameters, and display area for results.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 3  
**Name:** portal_ai_image_generator_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_ai_image_generator_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Image Generator UI Entry
    
**Requirement Ids:**
    
    - REQ-AIGS-001
    - REQ-AIGS-005
    - REQ-UIUX-004
    - REQ-UIUX-005
    - REQ-UIUX-021
    - REQ-UIUX-022
    - REQ-IPDPM-006
    
**Purpose:** Provides the main page structure for the AI image generation tool, where the interactive OWL component will be mounted.  
**Logic Description:** Template for '/my/ai-image-generator'. Contains a placeholder div where the `ai_image_generator_component` (OWL) will be rendered. May include surrounding text, instructions, or links to saved prompts/templates.  
**Documentation:**
    
    - **Summary:** QWeb template that serves as the container for the AI image generation OWL component. It sets up the page layout for users to interact with the AI image generation tool.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_performance_templates.xml  
**Description:** QWeb templates for displaying influencer-specific campaign performance metrics.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 3  
**Name:** portal_performance_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_performance_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Performance Dashboard UI
    
**Requirement Ids:**
    
    - REQ-IPDPM-005
    - REQ-2-011
    - REQ-UIUX-019
    
**Purpose:** Renders the page where influencers can view their performance data for campaigns.  
**Logic Description:** Template for '/my/performance'. Displays performance metrics (reach, engagement, clicks, etc.) for campaigns the influencer participated in. Data is fetched by the controller. May use OWL components for charts.  
**Documentation:**
    
    - **Summary:** QWeb templates to display performance dashboards for influencers, showing metrics related to their campaign contributions (e.g., reach, engagement, clicks).
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_accessibility_snippets.xml  
**Description:** QWeb snippets to promote WCAG 2.1 AA compliance, such as skip links or ARIA attribute helpers, if not directly part of other templates.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 2  
**Name:** portal_accessibility_snippets  
**Type:** ViewXML  
**Relative Path:** views/portal_accessibility_snippets.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Accessibility Enhancements
    
**Requirement Ids:**
    
    - REQ-14-001
    - REQ-14-002
    - REQ-14-003
    - REQ-14-004
    - REQ-14-005
    - REQ-UIUX-020
    
**Purpose:** Contains reusable QWeb snippets to aid in achieving WCAG 2.1 AA compliance across the portal.  
**Logic Description:** May include templates for generating skip-to-content links, standard ARIA landmark roles if not covered by Odoo's base portal, or utility templates for adding ARIA attributes dynamically if needed. Most ARIA roles should be directly in main templates.  
**Documentation:**
    
    - **Summary:** Provides reusable QWeb snippets to assist in meeting WCAG 2.1 Level AA accessibility standards. This could include templates for skip links, common ARIA patterns, or visually hidden text for screen readers.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_error_templates.xml  
**Description:** QWeb templates for displaying user-friendly error messages and pages (e.g., 404, 500 specific to portal).  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 2  
**Name:** portal_error_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_error_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - User-Friendly Error Display
    
**Requirement Ids:**
    
    - REQ-UIUX-009
    - REQ-16-013
    
**Purpose:** Provides standardized and user-friendly display for various error conditions within the portal.  
**Logic Description:** Templates for custom error pages (e.g., 'influence_gen_portal.error_page') or snippets for inline error messages. Ensures messages are clear, informative, and suggest corrective actions per REQ-UIUX-009.  
**Documentation:**
    
    - **Summary:** QWeb templates for rendering standardized, user-friendly error messages or dedicated error pages (e.g., for 403, 404, 500 errors encountered within the portal context).
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/portal_guidance_templates.xml  
**Description:** QWeb templates or snippets that can be used to integrate in-app guidance elements like tooltips or placeholders for guided tours.  
**Template:** Odoo QWeb Template  
**Dependancy Level:** 2  
**Name:** portal_guidance_templates  
**Type:** ViewXML  
**Relative Path:** views/portal_guidance_templates.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - In-App Guidance Structure
    
**Requirement Ids:**
    
    - REQ-IPDPM-009
    - REQ-UIUX-011
    
**Purpose:** Provides structures for embedding help text, tooltips, or triggering guided tours.  
**Logic Description:** Templates for standard tooltip structures, help icons with popovers, or placeholders for JavaScript-driven guided tour steps. Content for guidance will often be dynamic or configured elsewhere.  
**Documentation:**
    
    - **Summary:** Contains QWeb template structures or snippets that facilitate the implementation of in-app guidance, such as tooltips, help icons, or placeholders for JavaScript-driven tours.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/views/assets.xml  
**Description:** XML file defining frontend assets (CSS, JS) to be loaded for the InfluenceGen portal. References SCSS and JS files from the static directory.  
**Template:** Odoo Assets XML Template  
**Dependancy Level:** 1  
**Name:** assets  
**Type:** ConfigurationXML  
**Relative Path:** views/assets.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Asset Declaration
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    - REQ-DDSI-001
    
**Purpose:** Registers all static resources (CSS, SCSS, JavaScript) with Odoo's asset management system for inclusion in portal pages.  
**Logic Description:** Contains <odoo><data><template id="assets_frontend" inherit_id="web.assets_frontend"> entries to add paths to SCSS/CSS files and JavaScript files/bundles for the portal UI.  
**Documentation:**
    
    - **Summary:** Declares the JavaScript and CSS/SCSS assets required for the InfluenceGen portal, ensuring they are loaded by Odoo's asset management system.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** odoo_modules/influence_gen_portal/static/src/js/components/abstract_form_component.js  
**Description:** Abstract OWL component providing base functionality for forms, including common validation handling and submission logic for portal forms.  
**Template:** OWL Component JS  
**Dependancy Level:** 2  
**Name:** AbstractFormComponent  
**Type:** OWLComponentJS  
**Relative Path:** static/src/js/components/abstract_form_component.js  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    - **Name:** formData  
**Type:** Object  
**Attributes:** public  
    - **Name:** formErrors  
**Type:** Object  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _onInputChange  
**Parameters:**
    
    - event
    
**Return Type:** void  
**Attributes:** protected  
    - **Name:** _validateField  
**Parameters:**
    
    - fieldName
    - value
    
**Return Type:** boolean  
**Attributes:** protected  
    - **Name:** _validateForm  
**Parameters:**
    
    
**Return Type:** boolean  
**Attributes:** protected  
    - **Name:** _onSubmit  
**Parameters:**
    
    - event
    
**Return Type:** Promise<void>  
**Attributes:** protected  
    
**Implemented Features:**
    
    - Reusable Form Logic
    - Client-Side Form Validation
    
**Requirement Ids:**
    
    - REQ-IOKYC-014
    
**Purpose:** Provides a reusable base for creating interactive forms in the portal with consistent validation and submission patterns.  
**Logic Description:** Implements common form behaviors: state management for form data, handling input changes, performing client-side validation based on rules passed or defined, managing error states, and abstracting form submission logic. Uses portal_service for AJAX calls.  
**Documentation:**
    
    - **Summary:** A base OWL component for portal forms, encapsulating common logic for data handling, client-side validation feedback, and submission processing. Designed to be extended by specific form components.
    
**Namespace:** influence_gen_portal.AbstractFormComponent  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/static/src/js/components/file_uploader_component.js  
**Description:** OWL component for handling file uploads, with support for drag & drop, file type validation, and progress display. Used for KYC documents and campaign content.  
**Template:** OWL Component JS  
**Dependancy Level:** 3  
**Name:** FileUploaderComponent  
**Type:** OWLComponentJS  
**Relative Path:** static/src/js/components/file_uploader_component.js  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    - **Name:** acceptedFileTypes  
**Type:** Array<string>  
**Attributes:** public|props  
    - **Name:** maxFileSize  
**Type:** number  
**Attributes:** public|props  
    - **Name:** uploadedFiles  
**Type:** Array<Object>  
**Attributes:** public|state  
    - **Name:** uploadProgress  
**Type:** Object  
**Attributes:** public|state  
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _onFileDrop  
**Parameters:**
    
    - event
    
**Return Type:** void  
**Attributes:** protected  
    - **Name:** _onFileChange  
**Parameters:**
    
    - event
    
**Return Type:** void  
**Attributes:** protected  
    - **Name:** _validateFile  
**Parameters:**
    
    - file
    
**Return Type:** boolean  
**Attributes:** protected  
    - **Name:** _uploadFile  
**Parameters:**
    
    - file
    
**Return Type:** Promise<void>  
**Attributes:** protected  
    - **Name:** removeFile  
**Parameters:**
    
    - fileIndex
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - File Upload UI
    - File Validation
    
**Requirement Ids:**
    
    - REQ-IOKYC-004
    - REQ-2-009
    - REQ-IOKYC-014
    
**Purpose:** Provides an interactive and user-friendly interface for selecting and uploading files.  
**Logic Description:** Manages file selection (input or drag-and-drop). Validates files against `acceptedFileTypes` and `maxFileSize` props. Displays selected files and upload progress. Communicates with backend controllers to perform actual upload. Emits events on success/failure.  
**Documentation:**
    
    - **Summary:** An OWL component for handling file uploads. It supports features like drag-and-drop, file type/size validation, preview of selected files, and progress indication during upload.
    
**Namespace:** influence_gen_portal.FileUploaderComponent  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/static/src/js/components/ai_image_generator_component.js  
**Description:** Main OWL component for the AI Image Generation interface. Handles prompt input, parameter selection, initiation of generation, and display of results.  
**Template:** OWL Component JS  
**Dependancy Level:** 4  
**Name:** AIImageGeneratorComponent  
**Type:** OWLComponentJS  
**Relative Path:** static/src/js/components/ai_image_generator_component.js  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    - MVC/MTV
    
**Members:**
    
    - **Name:** prompt  
**Type:** string  
**Attributes:** public|state  
    - **Name:** negativePrompt  
**Type:** string  
**Attributes:** public|state  
    - **Name:** generationParams  
**Type:** Object  
**Attributes:** public|state  
    - **Name:** availableModels  
**Type:** Array<Object>  
**Attributes:** public|state  
    - **Name:** generatedImages  
**Type:** Array<Object>  
**Attributes:** public|state  
    - **Name:** isLoading  
**Type:** boolean  
**Attributes:** public|state  
    - **Name:** errorMessage  
**Type:** string  
**Attributes:** public|state  
    - **Name:** quotaStatus  
**Type:** Object  
**Attributes:** public|state  
    - **Name:** savedPrompts  
**Type:** Array<string>  
**Attributes:** public|state  
    - **Name:** templatePrompts  
**Type:** Array<string>  
**Attributes:** public|state  
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** Promise<void>  
**Attributes:** public  
    - **Name:** _loadInitialData  
**Parameters:**
    
    
**Return Type:** Promise<void>  
**Attributes:** protected  
    - **Name:** generateImage  
**Parameters:**
    
    
**Return Type:** Promise<void>  
**Attributes:** public  
    - **Name:** _handleGenerationResult  
**Parameters:**
    
    - result
    
**Return Type:** void  
**Attributes:** protected  
    - **Name:** _handleGenerationError  
**Parameters:**
    
    - error
    
**Return Type:** void  
**Attributes:** protected  
    - **Name:** downloadImage  
**Parameters:**
    
    - imageUrl
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** useImageInCampaign  
**Parameters:**
    
    - image
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** savePrompt  
**Parameters:**
    
    - promptText
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** reusePrompt  
**Parameters:**
    
    - promptText
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _updateParam  
**Parameters:**
    
    - paramName
    - value
    
**Return Type:** void  
**Attributes:** protected  
    
**Implemented Features:**
    
    - AI Image Generation UI
    - Prompt Management UI
    - Parameter Configuration UI
    - Result Display & Actions
    - Quota Display
    - Error Handling UI
    
**Requirement Ids:**
    
    - REQ-AIGS-001
    - REQ-AIGS-005
    - REQ-AIGS-008
    - REQ-AIGS-010
    - REQ-IPDPM-006
    - REQ-UIUX-004
    - REQ-UIUX-005
    - REQ-UIUX-021
    - REQ-UIUX-022
    - REQ-16-006
    - REQ-16-007
    - REQ-2-016
    
**Purpose:** Provides the complete interactive UI for users to generate AI images.  
**Logic Description:** Manages state for prompts, parameters, models, and results. Fetches available models, saved/template prompts on load. Handles user input for parameters, enforcing ranges/defaults from props/config. Calls `ai_image_service.js` to initiate generation. Displays loading indicators. Updates UI dynamically with generated images or error messages. Handles download and 'use in campaign' actions.  
**Documentation:**
    
    - **Summary:** The core OWL component for the AI image generation tool. It includes input fields for prompts, controls for generation parameters, options to save/reuse prompts, display area for generated images, and actions like download or use in campaign.
    
**Namespace:** influence_gen_portal.AIImageGeneratorComponent  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_portal/static/src/js/services/portal_service.js  
**Description:** JavaScript service providing utility functions for the portal, such as making authenticated AJAX calls to Odoo backend controllers.  
**Template:** JavaScript Service  
**Dependancy Level:** 2  
**Name:** portal_service  
**Type:** JavaScriptService  
**Relative Path:** static/src/js/services/portal_service.js  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** rpc  
**Parameters:**
    
    - route
    - params
    
**Return Type:** Promise<any>  
**Attributes:** public|static  
    - **Name:** notify  
**Parameters:**
    
    - message
    - type='info'
    - sticky=false
    
**Return Type:** void  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Backend Communication Utility
    - UI Notification Utility
    
**Requirement Ids:**
    
    - REQ-UIUX-007
    - REQ-UIUX-009
    
**Purpose:** Abstracts common frontend tasks like API calls and displaying notifications.  
**Logic Description:** The `rpc` method wraps Odoo's core RPC mechanism for calling backend Python controller methods, handling CSRF tokens and error responses. The `notify` method provides a consistent way to display toast notifications or alerts to the user.  
**Documentation:**
    
    - **Summary:** A JavaScript service offering helper functions for the portal frontend, primarily for making AJAX requests to Odoo backend controllers and displaying standardized UI notifications.
    
**Namespace:** influence_gen_portal.services.portal  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_portal/static/src/js/services/ai_image_service.js  
**Description:** JavaScript service dedicated to handling client-side logic for AI image generation, such as API calls to the AI image controller.  
**Template:** JavaScript Service  
**Dependancy Level:** 3  
**Name:** ai_image_service  
**Type:** JavaScriptService  
**Relative Path:** static/src/js/services/ai_image_service.js  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initiateGeneration  
**Parameters:**
    
    - params
    
**Return Type:** Promise<Object>  
**Attributes:** public|static  
    - **Name:** checkGenerationStatus  
**Parameters:**
    
    - requestId
    
**Return Type:** Promise<Object>  
**Attributes:** public|static  
    - **Name:** getAvailableModels  
**Parameters:**
    
    
**Return Type:** Promise<Array>  
**Attributes:** public|static  
    - **Name:** getSavedPrompts  
**Parameters:**
    
    
**Return Type:** Promise<Array>  
**Attributes:** public|static  
    - **Name:** saveUserPrompt  
**Parameters:**
    
    - promptText
    
**Return Type:** Promise<void>  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - AI Image Generation API Client
    
**Requirement Ids:**
    
    - REQ-AIGS-001
    - REQ-AIGS-010
    - REQ-UIUX-021
    
**Purpose:** Encapsulates communication with the backend for AI image generation tasks.  
**Logic Description:** Uses `portal_service.rpc` to call methods on `portal_ai_image_controller.py`. `initiateGeneration` sends prompt/params. `checkGenerationStatus` polls for results. Other methods fetch configuration or user data related to AI generation.  
**Documentation:**
    
    - **Summary:** Manages client-side interactions for AI image generation. This service makes API calls to initiate image generation, fetch status updates, retrieve available models, and manage user-saved prompts.
    
**Namespace:** influence_gen_portal.services.aiImage  
**Metadata:**
    
    - **Category:** Service
    
- **Path:** odoo_modules/influence_gen_portal/static/src/js/utils/accessibility_utils.js  
**Description:** Utility functions to assist with WCAG 2.1 AA compliance, such as focus management, ARIA attribute manipulation, etc.  
**Template:** JavaScript Utility  
**Dependancy Level:** 1  
**Name:** accessibility_utils  
**Type:** JavaScriptUtility  
**Relative Path:** static/src/js/utils/accessibility_utils.js  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** manageFocus  
**Parameters:**
    
    - elementSelector
    
**Return Type:** void  
**Attributes:** public|static  
    - **Name:** announceToScreenReader  
**Parameters:**
    
    - message
    
**Return Type:** void  
**Attributes:** public|static  
    - **Name:** checkColorContrast  
**Parameters:**
    
    - fgColor
    - bgColor
    
**Return Type:** boolean  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Accessibility Helper Functions
    
**Requirement Ids:**
    
    - REQ-14-001
    - REQ-14-002
    - REQ-14-003
    - REQ-14-004
    
**Purpose:** Provides common JavaScript utilities to enhance accessibility of OWL components.  
**Logic Description:** `manageFocus` helps programmatically set focus. `announceToScreenReader` uses ARIA live regions to announce dynamic changes. `checkColorContrast` might be a helper for developers during UI building, not typically runtime.  
**Documentation:**
    
    - **Summary:** Contains JavaScript helper functions to aid in implementing WCAG 2.1 AA accessibility features, such as managing keyboard focus, making announcements to screen readers, or dynamic ARIA attribute updates.
    
**Namespace:** influence_gen_portal.utils.accessibility  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_portal/static/src/js/utils/localization_utils.js  
**Description:** Utility functions for client-side localization of dates, numbers, and currencies if Odoo's default mechanisms are insufficient or need augmentation for specific portal needs.  
**Template:** JavaScript Utility  
**Dependancy Level:** 1  
**Name:** localization_utils  
**Type:** JavaScriptUtility  
**Relative Path:** static/src/js/utils/localization_utils.js  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** formatDate  
**Parameters:**
    
    - date
    - locale
    
**Return Type:** string  
**Attributes:** public|static  
    - **Name:** formatCurrency  
**Parameters:**
    
    - amount
    - currencyCode
    - locale
    
**Return Type:** string  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Client-Side Localization Helpers
    
**Requirement Ids:**
    
    - REQ-UIUX-014
    
**Purpose:** Provides supplementary client-side formatting for data if Odoo's built-in localization needs specific overrides or custom handling in OWL components.  
**Logic Description:** Wraps or extends JavaScript's `Intl` object or other localization libraries to provide consistent formatting. Primarily, rely on Odoo's server-side formatting passed to templates and OWL component props.  
**Documentation:**
    
    - **Summary:** JavaScript utilities for client-side formatting of dates, numbers, and currencies according to user locale preferences. This complements Odoo's server-side localization.
    
**Namespace:** influence_gen_portal.utils.localization  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_portal/static/src/scss/portal_main.scss  
**Description:** Main SCSS file for the InfluenceGen portal, importing variables, component-specific styles, and page-specific styles. Defines overall portal look and feel.  
**Template:** SCSS Stylesheet  
**Dependancy Level:** 1  
**Name:** portal_main  
**Type:** SCSS  
**Relative Path:** static/src/scss/portal_main.scss  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Portal Styling
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    - REQ-UIUX-002
    - REQ-UIUX-010
    
**Purpose:** Aggregates all SCSS for the portal and applies global styles.  
**Logic Description:** Imports `variables.scss`. Imports styles from `components/` and `pages/` subdirectories. Defines global portal styles, layout adjustments, and ensures consistency with Odoo's design language.  
**Documentation:**
    
    - **Summary:** The primary SCSS file that orchestrates all styles for the InfluenceGen portal. It imports variables, base styles, component-specific styles, and page-specific styles.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** odoo_modules/influence_gen_portal/static/src/scss/accessibility.scss  
**Description:** SCSS file containing styles specifically to enhance accessibility, such as improved focus indicators or high-contrast mode adjustments.  
**Template:** SCSS Stylesheet  
**Dependancy Level:** 1  
**Name:** accessibility  
**Type:** SCSS  
**Relative Path:** static/src/scss/accessibility.scss  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Accessibility Styling
    
**Requirement Ids:**
    
    - REQ-14-001
    - REQ-14-002
    - REQ-14-004
    - REQ-UIUX-020
    
**Purpose:** Provides dedicated styles to meet WCAG 2.1 AA requirements.  
**Logic Description:** Defines styles for highly visible keyboard focus indicators. May include styles for a high-contrast theme if implemented. Ensures sufficient contrast for UI elements where Odoo defaults might not suffice. Addresses any specific styling needs for screen reader compatibility (e.g., visually hidden text).  
**Documentation:**
    
    - **Summary:** Contains SCSS rules specifically aimed at improving accessibility in compliance with WCAG 2.1 AA. This includes styles for focus indicators, high-contrast adjustments, and other accessibility-related visual enhancements.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** odoo_modules/influence_gen_portal/static/src/scss/responsive.scss  
**Description:** SCSS file containing all media queries and responsive design adjustments to ensure the portal UI adapts to different screen sizes.  
**Template:** SCSS Stylesheet  
**Dependancy Level:** 1  
**Name:** responsive  
**Type:** SCSS  
**Relative Path:** static/src/scss/responsive.scss  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Responsive UI Design
    
**Requirement Ids:**
    
    - REQ-UIUX-002
    - REQ-IPDPM-008
    
**Purpose:** Ensures the portal is usable and looks good on desktops, tablets, and mobile devices.  
**Logic Description:** Contains `@media` queries targeting various breakpoints. Adjusts layout, font sizes, visibility of elements, and navigation patterns for different screen widths. Ensures Odoo's responsive framework is correctly leveraged and extended where needed.  
**Documentation:**
    
    - **Summary:** Holds SCSS media queries and responsive styles to ensure the InfluenceGen portal adapts gracefully to various screen sizes and devices (desktops, tablets, mobiles).
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** odoo_modules/influence_gen_portal/i18n/influence_gen_portal.pot  
**Description:** Main translation template file (.pot) for the InfluenceGen portal module. Contains all translatable strings.  
**Template:** Odoo POT File  
**Dependancy Level:** 0  
**Name:** influence_gen_portal  
**Type:** TranslationTemplate  
**Relative Path:** i18n/influence_gen_portal.pot  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Localization Support (Base)
    
**Requirement Ids:**
    
    - REQ-UIUX-013
    
**Purpose:** Serves as the base for creating language-specific .po translation files.  
**Logic Description:** Generated by Odoo's i18n tools by scanning source code (Python, XML, JS) for translatable strings (e.g., wrapped in _() or _t()). Contains 'msgid' entries for each string.  
**Documentation:**
    
    - **Summary:** The Portable Object Template (.pot) file containing all translatable strings extracted from the InfluenceGen portal module's source code and templates. This file is used as a base for creating language-specific .po files.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Localization
    
- **Path:** odoo_modules/influence_gen_portal/data/ir_ui_menu_data.xml  
**Description:** XML data file defining portal menu items for accessing InfluenceGen functionalities.  
**Template:** Odoo Data XML  
**Dependancy Level:** 1  
**Name:** ir_ui_menu_data  
**Type:** DataXML  
**Relative Path:** data/ir_ui_menu_data.xml  
**Repository Id:** REPO-IGOP-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Portal Navigation Menu
    
**Requirement Ids:**
    
    - REQ-IPDPM-001
    - REQ-IPDPM-004
    - REQ-IPDPM-005
    - REQ-IPDPM-006
    - REQ-IPDPM-007
    
**Purpose:** Creates the navigation structure within the influencer portal.  
**Logic Description:** Defines `ir.ui.menu` records with appropriate `name`, `parent_id`, `action`, and `sequence` attributes to build the portal menu (e.g., Dashboard, Profile, Campaigns, AI Tools, Payments, Performance). Actions link to controller routes.  
**Documentation:**
    
    - **Summary:** Defines the menu items that will appear in the influencer portal's navigation, linking to various sections like Dashboard, Profile, Campaigns, AI Tools, and Payments.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Data
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableAdvancedAIParamsForProUsers
  - enableVideoContentSubmission
  
- **Database Configs:**
  
  


---

