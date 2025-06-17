# Software Design Specification: InfluenceGen.Odoo.Portal.Endpoints

## 1. Introduction

This document outlines the software design specification for the `InfluenceGen.Odoo.Portal.Endpoints` repository. This repository is responsible for exposing all User Interface (UI) functionalities for influencers interacting with the InfluenceGen platform via the Odoo portal. It serves as the presentation layer, built using Odoo 18 controllers, QWeb templates, and OWL components, and interacts with the `InfluenceGen.Odoo.Business.Services` (REPO-IGBS-003) for business logic and data processing.

### 1.1. Purpose

The purpose of this SDS is to provide a detailed technical blueprint for developers to implement the `InfluenceGen.Odoo.Portal.Endpoints` module. It will guide the code generation process by specifying the structure, behavior, and interfaces of each component within this repository.

### 1.2. Scope

This SDS covers the design of:
*   Odoo HTTP Controllers for handling influencer portal requests.
*   QWeb templates for rendering portal pages.
*   OWL (Odoo Web Library) components for dynamic UI interactions.
*   Client-side JavaScript services for AJAX calls and utilities.
*   SCSS stylesheets for portal styling, responsiveness, and accessibility.
*   Module configuration files (`__manifest__.py`, `__init__.py`, data files).

Functionality includes:
*   Influencer Onboarding (Registration, KYC, Social/Bank Account Setup, ToS Agreement).
*   Campaign Management (Discovery, Details, Application, Content Submission).
*   AI Image Generation (Initiation, Status, Display, Prompt Management).
*   Influencer Profile Management (Dashboard, Profile Editing, Payment Info, Performance).
*   Accessibility (WCAG 2.1 AA compliance).
*   Notifications and UI Feedback.

### 1.3. Acronyms and Abbreviations
*   **SDS**: Software Design Specification
*   **UI**: User Interface
*   **UX**: User Experience
*   **KYC**: Know Your Customer
*   **AI**: Artificial Intelligence
*   **OWL**: Odoo Web Library
*   **QWeb**: Odoo's primary templating engine
*   **ORM**: Object-Relational Mapper
*   **HTTP**: HyperText Transfer Protocol
*   **AJAX**: Asynchronous JavaScript and XML
*   **JSON**: JavaScript Object Notation
*   **WCAG**: Web Content Accessibility Guidelines
*   **SCSS**: Sassy CSS (CSS preprocessor)
*   **CRUD**: Create, Read, Update, Delete
*   **ToS**: Terms of Service
*   **PII**: Personally Identifiable Information
*   **UAT**: User Acceptance Testing

## 2. System Overview

The `InfluenceGen.Odoo.Portal.Endpoints` repository forms the UI layer of the InfluenceGen platform within Odoo. It relies on the `InfluenceGen.Odoo.Business.Services` module for all business logic execution and data persistence. Communication with services like N8N (for AI image generation) is abstracted away by the business services layer; this UI layer primarily interacts with Odoo controllers which then call those services.

The architecture follows Odoo's MTV (Model-Template-View, similar to MVC) pattern:
*   **Models**: Handled by the business services layer (REPO-IGBS-003).
*   **Templates (Views)**: QWeb templates defined in this repository.
*   **Controllers**: Python HTTP controllers defined in this repository.
*   **OWL Components**: For client-side dynamic behavior and rich interactions.

## 3. Design Considerations

### 3.1. Technology Stack
*   **Framework**: Odoo 18
*   **Language**: Python 3.11+, JavaScript (ES2022+), XML
*   **Templating**: QWeb
*   **Frontend Framework**: Odoo Web Library (OWL) 2
*   **Styling**: SCSS, CSS3
*   **Communication**: HTTP, JSON for AJAX

### 3.2. Key Design Principles
*   **Modularity**: Code organized into logical Odoo modules and components.
*   **Reusability**: Common UI patterns and logic encapsulated in abstract OWL components or utility services.
*   **Maintainability**: Adherence to Odoo development best practices, clear code, and comprehensive documentation.
*   **User-Centricity**: Intuitive UI/UX, responsive design, and strong focus on accessibility (WCAG 2.1 AA).
*   **Security**: Client-side validation for immediate feedback, but all critical validation and security checks performed server-side by the business layer. Portal endpoints will use Odoo's authentication (`auth='user'`).
*   **Performance**: Optimize page load times and interactive element responsiveness.
*   **Localization**: All user-facing strings designed for translation using Odoo's i18n mechanisms.

## 4. Detailed Component Design

This section details the design of each file specified in the repository structure.

---

### 4.1. Module Configuration

#### 4.1.1. `odoo_modules/influence_gen_portal/__manifest__.py`
*   **Description**: Odoo module manifest file.
*   **Purpose**: Declares the InfluenceGen Portal module to Odoo, its dependencies, and assets.
*   **Logic Description**:
    python
    {
        'name': 'InfluenceGen Portal',
        'version': '18.0.1.0.0',
        'category': 'InfluenceGen/Portal',
        'summary': 'Influencer facing portal for the InfluenceGen platform.',
        'description': """
    Exposes all User Interface (UI) functionalities for influencers.
    Includes:
    - Influencer Onboarding (Registration, KYC, Social/Bank Accounts, ToS)
    - Campaign Management (Discovery, Application, Content Submission)
    - AI Image Generation Interface
    - Profile Management (Dashboard, Payments, Performance)
    """,
        'author': 'SSS-AI',
        'website': 'https://www.example.com', # Replace with actual website
        'depends': [
            'portal',
            'website',
            'mail',
            'influence_gen_business_services', # Assumed name for REPO-IGBS-003
        ],
        'data': [
            'security/ir.model.access.csv', # To be created if any custom portal models are needed here (unlikely, data models in business layer)
            'security/influence_gen_portal_security.xml', # For portal user group access rules
            'views/portal_layout_templates.xml',
            'views/portal_dashboard_templates.xml',
            'views/portal_profile_templates.xml',
            'views/portal_onboarding_templates.xml',
            'views/portal_campaign_discovery_templates.xml',
            'views/portal_campaign_details_templates.xml',
            'views/portal_campaign_application_templates.xml',
            'views/portal_content_submission_templates.xml',
            'views/portal_ai_image_generator_templates.xml',
            'views/portal_performance_templates.xml',
            'views/portal_accessibility_snippets.xml',
            'views/portal_error_templates.xml',
            'views/portal_guidance_templates.xml',
            'data/ir_ui_menu_data.xml', # Portal menu items
            # Add other data files if necessary (e.g., default values for settings specific to portal if not business layer)
        ],
        'assets': {
            'web.assets_frontend': [
                'influence_gen_portal/static/src/scss/portal_main.scss',
                'influence_gen_portal/static/src/scss/accessibility.scss',
                'influence_gen_portal/static/src/scss/responsive.scss',
                # Component SCSS (if any specific to components)
                # JS Services
                'influence_gen_portal/static/src/js/services/portal_service.js',
                'influence_gen_portal/static/src/js/services/ai_image_service.js',
                # JS Utilities
                'influence_gen_portal/static/src/js/utils/accessibility_utils.js',
                'influence_gen_portal/static/src/js/utils/localization_utils.js',
                # OWL Components
                'influence_gen_portal/static/src/js/components/abstract_form_component.js',
                'influence_gen_portal/static/src/js/components/file_uploader_component.js',
                'influence_gen_portal/static/src/js/components/ai_image_generator_component.js',
                # Main portal JS file if any orchestrating logic
                'influence_gen_portal/static/src/js/portal_main.js', # (if needed for global portal behaviors)
            ],
            'web.assets_qweb': [ # For OWL component XML templates
                'influence_gen_portal/static/src/xml/components/abstract_form_component.xml',
                'influence_gen_portal/static/src/xml/components/file_uploader_component.xml',
                'influence_gen_portal/static/src/xml/components/ai_image_generator_component.xml',
            ],
        },
        'installable': True,
        'application': False, # It's an addon to the main application
        'auto_install': False,
        'license': 'OEEL-1', # Or appropriate license
    }
    
*   **Requirements Met**: REQ-UIUX-001, REQ-DDSI-001

#### 4.1.2. `odoo_modules/influence_gen_portal/__init__.py`
*   **Description**: Python package initializer.
*   **Purpose**: Makes Python modules within this Odoo module importable.
*   **Logic Description**:
    python
    from . import controllers
    # from . import models # If any portal-specific models are defined (unlikely, models in business layer)
    # from . import wizards # If any portal-specific wizards
    
*   **Requirements Met**: REQ-DDSI-001

---

### 4.2. Controllers

#### 4.2.1. `odoo_modules/influence_gen_portal/controllers/__init__.py`
*   **Description**: Python package initializer for controllers.
*   **Purpose**: Aggregates all controller modules.
*   **Logic Description**:
    python
    from . import portal_main_controller
    from . import portal_onboarding_controller
    from . import portal_campaign_controller
    from . import portal_ai_image_controller
    
*   **Requirements Met**: REQ-DDSI-001

#### 4.2.2. `odoo_modules/influence_gen_portal/controllers/portal_main_controller.py`
*   **Description**: Odoo HTTP controller for main influencer portal pages.
*   **Purpose**: Handles requests for core influencer portal pages, fetches data via business services, renders QWeb templates.
*   **Namespace**: `odoo.addons.influence_gen_portal.controllers.portal_main_controller`
*   **Class**: `InfluenceGenPortalMain(http.Controller)`
    *   **Dependencies**: `influence_gen.influencer_profile` service (from REPO-IGBS-003), `influence_gen.payment_record` service, `influence_gen.campaign` service, `influence_gen.terms_consent` service, `influence_gen.ai_usage_quota` service.
    *   **Methods**:
        *   `influencer_dashboard(self, **kw)`:
            *   **Route**: `/my/dashboard`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**:
                1.  Get current Odoo user and their associated `influencer.profile` record.
                2.  Fetch summary data: active campaigns, pending KYC/content tasks, recent notifications, AI image quota.
                3.  Prepare values for QWeb template.
            *   **Return**: Renders `influence_gen_portal.portal_dashboard` template.
            *   **Requirements Met**: REQ-IPDPM-001, REQ-IPDPM-002
        *   `influencer_profile(self, **kw)`:
            *   **Route**: `/my/profile`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch influencer profile details, KYC status, bank accounts.
            *   **Return**: Renders `influence_gen_portal.portal_profile_main` template.
            *   **Requirements Met**: REQ-IPDPM-003, REQ-IOKYC-010, REQ-UIUX-017
        *   `update_influencer_profile(self, **post)`:
            *   **Route**: `/my/profile/update`, `auth='user'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**:
                1.  Validate submitted form data (`**post`).
                2.  Call business service to update non-sensitive influencer profile fields. Handle re-verification triggers for sensitive data.
                3.  Handle success/error messages.
            *   **Return**: Redirect to `/my/profile` with status message.
            *   **Requirements Met**: REQ-IPDPM-003
        *   `influencer_payment_info(self, **kw)`:
            *   **Route**: `/my/payments`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch influencer's bank account details, payment history, amounts owed.
            *   **Return**: Renders `influence_gen_portal.portal_payment_info` template.
            *   **Requirements Met**: REQ-IPDPM-007, REQ-IPF-001
        *   `update_influencer_payment_info(self, **post)`:
            *   **Route**: `/my/payments/update`, `auth='user'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**:
                1.  Validate submitted bank account data.
                2.  Call business service to add/update bank account details (may trigger re-verification).
            *   **Return**: Redirect to `/my/payments` with status message.
            *   **Requirements Met**: REQ-IPDPM-007, REQ-IPF-001
        *   `influencer_ai_image_generator(self, **kw)`:
            *   **Route**: `/my/ai-image-generator`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch user's AI image quota, available models, saved prompts.
            *   **Return**: Renders `influence_gen_portal.portal_ai_image_generator_page` template (which will host the OWL component).
            *   **Requirements Met**: REQ-IPDPM-006, REQ-AIGS-001, REQ-AIGS-005
        *   `influencer_performance_dashboard(self, **kw)`:
            *   **Route**: `/my/performance`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch performance data for the influencer's campaigns.
            *   **Return**: Renders `influence_gen_portal.portal_performance_dashboard` template.
            *   **Requirements Met**: REQ-IPDPM-005, REQ-UIUX-019
        *   `influencer_consent_management(self, **kw)`:
            *   **Route**: `/my/consent`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch influencer's consent history for ToS/Privacy Policy. Check if new versions need acceptance.
            *   **Return**: Renders `influence_gen_portal.portal_consent_management` template.
            *   **Requirements Met**: REQ-IPDPM-011, REQ-IOKYC-009
        *   `influencer_accept_terms(self, **post)`:
            *   **Route**: `/my/consent/accept`, `auth='user'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**:
                1.  Receive `tos_version` and `privacy_policy_version` consented to.
                2.  Call business service to log consent.
            *   **Return**: Redirect to `/my/dashboard` or previous page with status message.
            *   **Requirements Met**: REQ-IPDPM-011, REQ-IOKYC-009

#### 4.2.3. `odoo_modules/influence_gen_portal/controllers/portal_onboarding_controller.py`
*   **Description**: Odoo HTTP controller for influencer onboarding steps.
*   **Purpose**: Manages UI for registration, KYC, social/bank account setup.
*   **Namespace**: `odoo.addons.influence_gen_portal.controllers.portal_onboarding_controller`
*   **Class**: `InfluenceGenPortalOnboarding(http.Controller)`
    *   **Dependencies**: `influence_gen.onboarding_service` (from REPO-IGBS-003).
    *   **Methods**:
        *   `influencer_register(self, **kw)`:
            *   **Route**: `/influencer/register`, `auth='public'`, `type='http'`, `website=True`
            *   **Logic**: If user logged in and already an influencer, redirect to dashboard. Else, render registration form.
            *   **Return**: Renders `influence_gen_portal.portal_registration_form` template.
            *   **Requirements Met**: REQ-IOKYC-001
        *   `process_registration(self, **post)`:
            *   **Route**: `/influencer/register/process`, `auth='public'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**:
                1.  Validate registration data (name, email, password).
                2.  Call business service to create Odoo user and `influencer.profile` record (initial status).
                3.  Log in the user.
            *   **Return**: Redirect to KYC submission step (`/my/kyc/submit`) or dashboard with message.
            *   **Requirements Met**: REQ-IOKYC-001, REQ-IOKYC-002
        *   `influencer_kyc_submission(self, **kw)`:
            *   **Route**: `/my/kyc/submit`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Check if KYC already submitted/approved. Fetch current KYC status.
            *   **Return**: Renders `influence_gen_portal.portal_kyc_submission_form` template.
            *   **Requirements Met**: REQ-IOKYC-004, REQ-IOKYC-005, REQ-IOKYC-010
        *   `process_kyc_documents(self, **post)`:
            *   **Route**: `/my/kyc/submit/process`, `auth='user'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**:
                1.  Handle file uploads for ID documents (front, back).
                2.  Validate file types, sizes.
                3.  Call business service to save document references and update KYC status.
            *   **Return**: Redirect to next onboarding step or KYC status page.
            *   **Requirements Met**: REQ-IOKYC-004, REQ-IOKYC-014
        *   `influencer_social_media_setup(self, **kw)`:
            *   **Route**: `/my/social/setup`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch existing social media links for the influencer.
            *   **Return**: Renders `influence_gen_portal.portal_social_media_form` template.
            *   **Requirements Met**: REQ-IOKYC-002, REQ-IOKYC-003, REQ-IOKYC-006
        *   `process_social_media_links(self, **post)`:
            *   **Route**: `/my/social/setup/process`, `auth='user'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**:
                1.  Validate submitted social media links (format, uniqueness).
                2.  Call business service to save/update links and trigger verification process.
            *   **Return**: Redirect to next step or profile page.
            *   **Requirements Met**: REQ-IOKYC-002, REQ-IOKYC-003, REQ-IOKYC-006, REQ-IOKYC-014
        *   `influencer_bank_account_setup(self, **kw)`:
            *   **Route**: `/my/bank/setup`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch existing bank account details for the influencer.
            *   **Return**: Renders `influence_gen_portal.portal_bank_account_form` template.
            *   **Requirements Met**: REQ-IOKYC-007, REQ-IOKYC-008, REQ-IPF-001
        *   `process_bank_account_details(self, **post)`:
            *   **Route**: `/my/bank/setup/process`, `auth='user'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**:
                1.  Validate submitted bank account data.
                2.  Call business service to save details and trigger verification.
            *   **Return**: Redirect to next step or profile page.
            *   **Requirements Met**: REQ-IOKYC-007, REQ-IOKYC-008, REQ-IPF-001
        *   `influencer_tos_agreement(self, **kw)`:
            *   **Route**: `/my/tos/agree`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch current ToS/Privacy Policy versions.
            *   **Return**: Renders `influence_gen_portal.portal_tos_agreement_form` template.
            *   **Requirements Met**: REQ-IOKYC-009
        *   `process_tos_agreement(self, **post)`:
            *   **Route**: `/my/tos/agree/process`, `auth='user'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**: Record influencer's consent to specific ToS/Privacy Policy versions.
            *   **Return**: Redirect to dashboard or onboarding completion page.
            *   **Requirements Met**: REQ-IOKYC-009
        *   `check_kyc_status(self, **kw)`:
            *   **Route**: `/my/kyc/status`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetches and displays detailed current KYC status, including required actions if any.
            *   **Return**: Renders `influence_gen_portal.portal_kyc_status_page` template.
            *   **Requirements Met**: REQ-IOKYC-010, REQ-UIUX-017

#### 4.2.4. `odoo_modules/influence_gen_portal/controllers/portal_campaign_controller.py`
*   **Description**: Odoo HTTP controller for influencer campaign interactions.
*   **Purpose**: Manages UI for campaign discovery, application, and content submission.
*   **Namespace**: `odoo.addons.influence_gen_portal.controllers.portal_campaign_controller`
*   **Class**: `InfluenceGenPortalCampaign(http.Controller)`
    *   **Dependencies**: `influence_gen.campaign_service`, `influence_gen.content_submission_service` (from REPO-IGBS-003).
    *   **Methods**:
        *   `campaign_discovery(self, page=1, search=None, sort_by=None, **kw)`:
            *   **Route**: `/my/campaigns`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**:
                1.  Fetch list of 'Published' campaigns based on search, sort, filter criteria (`kw` for filters).
                2.  Implement pagination.
            *   **Return**: Renders `influence_gen_portal.portal_campaign_discovery_list` template.
            *   **Requirements Met**: REQ-IPDPM-004, REQ-2-004, REQ-UIUX-018
        *   `campaign_details(self, campaign_id, **kw)`:
            *   **Route**: `/my/campaigns/<model("influence_gen.campaign"):campaign_id>`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch detailed information for the specified `campaign_id`. Check if influencer can apply.
            *   **Return**: Renders `influence_gen_portal.portal_campaign_detail_page` template.
            *   **Requirements Met**: REQ-2-005
        *   `campaign_apply(self, campaign_id, **kw)`:
            *   **Route**: `/my/campaigns/<model("influence_gen.campaign"):campaign_id>/apply`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: If GET, render application form. Fetch campaign details for context.
            *   **Return**: Renders `influence_gen_portal.portal_campaign_application_form` template.
            *   **Requirements Met**: REQ-2-006
        *   `process_campaign_application(self, campaign_id, **post)`:
            *   **Route**: `/my/campaigns/<model("influence_gen.campaign"):campaign_id>/apply/process`, `auth='user'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**:
                1.  Validate application data (proposal, confirmations).
                2.  Call business service to create campaign application.
            *   **Return**: Redirect to campaign discovery or application status page with message.
            *   **Requirements Met**: REQ-2-006
        *   `campaign_content_submission_form(self, campaign_application_id, **kw)`:
            *   **Route**: `/my/campaigns/submit/<model("influence_gen.campaign_application"):campaign_application_id>`, `auth='user'`, `type='http'`, `website=True`
            *   **Logic**: Fetch details of the campaign application. Fetch influencer's AI-generated images eligible for this campaign.
            *   **Return**: Renders `influence_gen_portal.portal_content_submission_page` template.
            *   **Requirements Met**: REQ-2-009, REQ-2-016
        *   `process_content_submission(self, campaign_application_id, **post)`:
            *   **Route**: `/my/campaigns/submit/<model("influence_gen.campaign_application"):campaign_application_id>/process`, `auth='user'`, `type='http'`, `methods=['POST']`, `website=True`, `csrf=True`
            *   **Logic**:
                1.  Handle file uploads, link inputs, AI image selections.
                2.  Validate submission against campaign requirements.
                3.  Call business service to create content submission record.
            *   **Return**: Redirect to campaign participation page or dashboard with message.
            *   **Requirements Met**: REQ-2-009, REQ-2-016

#### 4.2.5. `odoo_modules/influence_gen_portal/controllers/portal_ai_image_controller.py`
*   **Description**: Odoo HTTP controller for AJAX interactions for AI image generation.
*   **Purpose**: Handles asynchronous requests from the AI image generation UI.
*   **Namespace**: `odoo.addons.influence_gen_portal.controllers.portal_ai_image_controller`
*   **Class**: `InfluenceGenPortalAIImage(http.Controller)`
    *   **Dependencies**: `influence_gen.ai_image_service` (from REPO-IGBS-003).
    *   **Methods**:
        *   `initiate_ai_image_generation(self, **params)`:
            *   **Route**: `/my/ai/generate`, `auth='user'`, `type='json'`, `methods=['POST']`, `csrf=True`
            *   **Logic**:
                1.  Extract prompt, negative_prompt, model_id, resolution, aspect_ratio, seed, inference_steps, cfg_scale, intended_use, campaign_id (optional) from `params`.
                2.  Call business service (`influence_gen.ai_image_service`) to validate params, check quota, and trigger N8N webhook asynchronously.
                3.  The business service should return a unique `request_id`.
            *   **Return**: JSON response `{'request_id': 'some_uuid', 'status': 'queued'}` or error.
            *   **Requirements Met**: REQ-AIGS-001, REQ-AIGS-005, REQ-AIGS-010
        *   `get_ai_image_generation_status(self, request_id, **kw)`:
            *   **Route**: `/my/ai/generate/status`, `auth='user'`, `type='json'`, `methods=['GET']`
            *   **Params**: `request_id`
            *   **Logic**: Call business service to fetch status and potentially image URL(s) for the given `request_id`.
            *   **Return**: JSON response `{'request_id': request_id, 'status': 'processing|completed|failed', 'images': [{'id': 'img_uuid', 'url': '...'}], 'error_message': '...'}`.
            *   **Requirements Met**: REQ-AIGS-005, REQ-AIGS-008, REQ-16-006

---

### 4.3. Views (QWeb Templates)

#### 4.3.1. `odoo_modules/influence_gen_portal/views/portal_layout_templates.xml`
*   **Description**: QWeb templates for main portal layout.
*   **Purpose**: Provides consistent structure and navigation.
*   **Templates**:
    *   `influence_gen_portal.portal_layout` (inherits `portal.portal_layout`):
        *   Adds InfluenceGen specific CSS/JS assets.
        *   Customizes header/footer if needed.
        *   Defines main navigation menu structure using `ir.ui.menu` records (see `ir_ui_menu_data.xml`). Links include:
            *   Dashboard (`/my/dashboard`)
            *   Profile (`/my/profile`)
            *   Campaigns (`/my/campaigns`)
            *   AI Image Generator (`/my/ai-image-generator`)
            *   Payments (`/my/payments`)
            *   Performance (`/my/performance`)
            *   Consent (`/my/consent`)
            *   Help/Documentation (link to KB/FAQ)
*   **Requirements Met**: REQ-IPDPM-001, REQ-UIUX-001, REQ-UIUX-002, REQ-UIUX-010, REQ-UIUX-012

#### 4.3.2. `odoo_modules/influence_gen_portal/views/portal_dashboard_templates.xml`
*   **Description**: QWeb templates for the influencer's personalized dashboard.
*   **Purpose**: Renders the main dashboard.
*   **Templates**:
    *   `influence_gen_portal.portal_dashboard`:
        *   Page title: "My Dashboard".
        *   Sections/Widgets for:
            *   Summary of active campaigns (count, links).
            *   Pending tasks (e.g., "Complete KYC", "Submit content for Campaign X").
            *   Recent platform notifications (if any).
            *   AI Image Generation quota status (e.g., "Images remaining: X/Y").
            *   Quick links to key portal areas.
*   **Requirements Met**: REQ-IPDPM-002, REQ-UIUX-019

#### 4.3.3. `odoo_modules/influence_gen_portal/views/portal_profile_templates.xml`
*   **Description**: QWeb templates for influencer profile, KYC, consent, payments.
*   **Purpose**: Renders profile viewing/editing and related information.
*   **Templates**:
    *   `influence_gen_portal.portal_profile_main`:
        *   Page title: "My Profile".
        *   Tabs/Sections for:
            *   **Personal & Contact Info**: Form to view/edit `fullName`, `email` (display only, or special process for change), `phone`, `residentialAddress`. (REQ-IPDPM-003)
            *   **Professional Info**: Form to view/edit `areasOfInfluence` (multi-select or tag input), `audienceDemographics` (structured input or textarea for JSON).
            *   **Social Media Accounts**: List existing, form to add/edit `platform`, `handle`, `url`. Display `verificationStatus`. (REQ-IOKYC-002, REQ-IPDPM-003)
            *   **KYC Status**: Display current `kycStatus`, `reviewedAt`, `reviewerUserId`. Link to `/my/kyc/submit` if actions needed. (REQ-IOKYC-010, REQ-UIUX-017)
            *   **Payment Information (`influence_gen_portal.portal_payment_info` template called within a tab)**:
                *   View/edit bank account details: `accountHolderName`, `accountNumber`, `bankName`, etc. Display `verificationStatus`. (REQ-IPDPM-007, REQ-IPF-001)
                *   Payment history list (date, campaign, amount, status).
            *   **Consent Records (`influence_gen_portal.portal_consent_management` template called within a tab)**:
                *   List of `tosVersion`, `privacyPolicyVersion`, `consentDate`. (REQ-IPDPM-011, REQ-IOKYC-009)
                *   Form to accept new versions if pending.
*   **Requirements Met**: REQ-IPDPM-003, REQ-IPDPM-007, REQ-IPDPM-011, REQ-IOKYC-009, REQ-IOKYC-010, REQ-UIUX-017, REQ-IPF-001

#### 4.3.4. `odoo_modules/influence_gen_portal/views/portal_onboarding_templates.xml`
*   **Description**: QWeb templates for multi-step influencer onboarding.
*   **Purpose**: UI for registration and KYC process.
*   **Templates**:
    *   `influence_gen_portal.portal_registration_form`:
        *   Public page. Form fields for `fullName`, `email`, `password`, `confirm_password`.
        *   Client-side validation.
        *   Requirements Met: REQ-IOKYC-001, REQ-IOKYC-002
    *   `influence_gen_portal.portal_kyc_submission_form`:
        *   Authenticated page. Form fields for `documentType`.
        *   File upload widget (`FileUploaderComponent` t-call or OWL mount) for ID documents.
        *   Instructions on acceptable files.
        *   Requirements Met: REQ-IOKYC-004, REQ-IOKYC-005
    *   `influence_gen_portal.portal_social_media_form`:
        *   Authenticated page. Form for adding/editing social media profiles (platform, handle, URL).
        *   Instructions for verification methods (e.g., OAuth if available, code in bio).
        *   Requirements Met: REQ-IOKYC-002, REQ-IOKYC-003, REQ-IOKYC-006
    *   `influence_gen_portal.portal_bank_account_form`:
        *   Authenticated page. Form for bank account details.
        *   Instructions for verification.
        *   Requirements Met: REQ-IOKYC-007, REQ-IOKYC-008, REQ-IPF-001
    *   `influence_gen_portal.portal_tos_agreement_form`:
        *   Authenticated page. Display links to ToS and Privacy Policy.
        *   Checkbox for explicit consent.
        *   Requirements Met: REQ-IOKYC-009
    *   `influence_gen_portal.portal_kyc_status_page`:
        *   Authenticated page. Displays current KYC status, messages from admin if info is required.
        *   Requirements Met: REQ-IOKYC-010, REQ-UIUX-017

#### 4.3.5. `odoo_modules/influence_gen_portal/views/portal_campaign_discovery_templates.xml`
*   **Description**: QWeb templates for campaign discovery.
*   **Purpose**: Renders campaign listing, search, filter, sort.
*   **Templates**:
    *   `influence_gen_portal.portal_campaign_discovery_list`:
        *   Page title: "Discover Campaigns".
        *   Search bar (keyword search).
        *   Filter controls: Niche (dropdown/tags), Compensation Type (dropdown), Keywords (covered by search).
        *   Sort controls: Deadline, Compensation, Recently Added (dropdown).
        *   Campaign listing area:
            *   Loop through campaigns (`t-foreach`).
            *   Each campaign displayed as a card/list item showing: Name, Brand, Brief Description, Compensation Teaser, Deadline.
            *   Link to campaign details page.
        *   Pagination controls.
*   **Requirements Met**: REQ-2-004, REQ-UIUX-018

#### 4.3.6. `odoo_modules/influence_gen_portal/views/portal_campaign_details_templates.xml`
*   **Description**: QWeb template for specific campaign details.
*   **Purpose**: Renders detailed view of a campaign.
*   **Templates**:
    *   `influence_gen_portal.portal_campaign_detail_page`:
        *   Page title: Campaign Name.
        *   Sections for:
            *   Campaign Name, Description, Brand, Goals.
            *   Target Influencer Criteria (if public).
            *   Content Requirements (type, messages, hashtags, do's/don'ts).
            *   Compensation Model & Amount/Range (if public).
            *   Deadlines, Usage Rights Summary.
        *   "Apply to Campaign" button (if influencer is eligible and campaign is open).
*   **Requirements Met**: REQ-2-005

#### 4.3.7. `odoo_modules/influence_gen_portal/views/portal_campaign_application_templates.xml`
*   **Description**: QWeb template for campaign application form.
*   **Purpose**: Renders application form.
*   **Templates**:
    *   `influence_gen_portal.portal_campaign_application_form`:
        *   Page title: "Apply for: [Campaign Name]".
        *   Display key campaign requirements for confirmation.
        *   Form fields:
            *   Custom proposal (textarea, if required by campaign settings).
            *   Answers to specific questions (if any).
            *   Checkbox: "I understand and agree to the campaign requirements, content guidelines, and usage rights."
        *   Submit button.
*   **Requirements Met**: REQ-2-006

#### 4.3.8. `odoo_modules/influence_gen_portal/views/portal_content_submission_templates.xml`
*   **Description**: QWeb template for content submission.
*   **Purpose**: Renders content submission form.
*   **Templates**:
    *   `influence_gen_portal.portal_content_submission_page`:
        *   Page title: "Submit Content for: [Campaign Name]".
        *   Link to campaign brief/requirements.
        *   Form fields:
            *   Text captions (textarea).
            *   File upload (`FileUploaderComponent` t-call or OWL mount) for images/videos. (REQ-2-009)
            *   Link to draft/published post (URL input).
            *   Option to select from user's AI-generated images (if feature enabled, links to a modal or picker). (REQ-2-016)
        *   Submission history for this application (feedback, revisions).
        *   Submit button.
*   **Requirements Met**: REQ-2-009, REQ-2-016

#### 4.3.9. `odoo_modules/influence_gen_portal/views/portal_ai_image_generator_templates.xml`
*   **Description**: QWeb template hosting the AI image generation OWL component.
*   **Purpose**: Main page structure for AI image tool.
*   **Templates**:
    *   `influence_gen_portal.portal_ai_image_generator_page`:
        *   Page title: "AI Image Generator".
        *   Placeholder `div` for mounting `AIImageGeneratorComponent`.
        *   Instructions or introductory text.
        *   Display user's current AI image generation quota. (REQ-IPDPM-006)
*   **Requirements Met**: REQ-AIGS-001, REQ-AIGS-005, REQ-UIUX-004, REQ-UIUX-005, REQ-UIUX-021, REQ-UIUX-022, REQ-IPDPM-006

#### 4.3.10. `odoo_modules/influence_gen_portal/views/portal_performance_templates.xml`
*   **Description**: QWeb templates for influencer performance metrics.
*   **Purpose**: Renders performance data page.
*   **Templates**:
    *   `influence_gen_portal.portal_performance_dashboard`:
        *   Page title: "My Performance".
        *   Loop through campaigns influencer participated in.
        *   For each campaign, display:
            *   Campaign Name.
            *   Submitted content links/previews.
            *   Performance metrics (reach, engagement, clicks, views, conversions as inputted/defined). (REQ-2-011)
        *   May use OWL components for charts/graphs if complex visualization is needed.
*   **Requirements Met**: REQ-IPDPM-005, REQ-2-011, REQ-UIUX-019

#### 4.3.11. `odoo_modules/influence_gen_portal/views/portal_accessibility_snippets.xml`
*   **Description**: QWeb snippets for WCAG 2.1 AA compliance.
*   **Purpose**: Reusable snippets for accessibility.
*   **Templates**:
    *   `influence_gen_portal.snippet_skip_to_content`: A "Skip to Main Content" link for keyboard users, visible on focus.
    *   Potentially other utility snippets if common ARIA patterns are needed beyond what Odoo's base offers. Most ARIA will be inline in main templates.
*   **Requirements Met**: REQ-14-001, REQ-14-002, REQ-14-003, REQ-14-004, REQ-14-005, REQ-UIUX-020

#### 4.3.12. `odoo_modules/influence_gen_portal/views/portal_error_templates.xml`
*   **Description**: QWeb templates for user-friendly error pages.
*   **Purpose**: Standardized display for portal errors.
*   **Templates**:
    *   `influence_gen_portal.portal_error_page` (can be called by controllers for generic errors):
        *   Takes error `title`, `message`, and optional `suggestions` as parameters.
        *   User-friendly language, avoids technical jargon.
        *   Link to homepage or support.
    *   May override Odoo's default 403, 404, 500 error pages for portal context if needed (`website.403`, `website.404`, `website.http_error`).
*   **Requirements Met**: REQ-UIUX-009, REQ-16-013

#### 4.3.13. `odoo_modules/influence_gen_portal/views/portal_guidance_templates.xml`
*   **Description**: QWeb templates/snippets for in-app guidance.
*   **Purpose**: Structures for tooltips, help icons, tour placeholders.
*   **Templates**:
    *   `influence_gen_portal.snippet_help_tooltip`:
        *   Takes `help_text` as parameter.
        *   Renders a small help icon (?) that shows `help_text` on hover/focus (using Bootstrap popover/tooltip or custom OWL).
    *   Placeholders in main templates (e.g., `<div class="tour-step" data-step="1" data-intro="Welcome! This is your dashboard."></div>`) if a JS tour library is used.
*   **Requirements Met**: REQ-IPDPM-009, REQ-UIUX-011

#### 4.3.14. `odoo_modules/influence_gen_portal/views/assets.xml`
*   **Description**: XML for defining frontend assets.
*   **Purpose**: Registers CSS and JS for the portal.
*   **Logic Description**: (as detailed in `__manifest__.py`'s assets section, this file implements it)
    xml
    <odoo>
        <data>
            <template id="assets_frontend_influence_gen" name="InfluenceGen Portal Assets" inherit_id="web.assets_frontend">
                <xpath expr="." position="inside">
                    <link rel="stylesheet" type="text/scss" href="/influence_gen_portal/static/src/scss/portal_main.scss"/>
                    <link rel="stylesheet" type="text/scss" href="/influence_gen_portal/static/src/scss/accessibility.scss"/>
                    <link rel="stylesheet" type="text/scss" href="/influence_gen_portal/static/src/scss/responsive.scss"/>
                    <!-- Add component-specific SCSS if they are standalone -->
                    <!-- <link rel="stylesheet" type="text/scss" href="/influence_gen_portal/static/src/scss/components/ai_image_generator.scss"/> -->

                    <script type="text/javascript" src="/influence_gen_portal/static/src/js/services/portal_service.js"></script>
                    <script type="text/javascript" src="/influence_gen_portal/static/src/js/services/ai_image_service.js"></script>
                    <script type="text/javascript" src="/influence_gen_portal/static/src/js/utils/accessibility_utils.js"></script>
                    <script type="text/javascript" src="/influence_gen_portal/static/src/js/utils/localization_utils.js"></script>
                    
                    <!-- OWL Components (JS) -->
                    <script type="text/javascript" src="/influence_gen_portal/static/src/js/components/abstract_form_component.js"></script>
                    <script type="text/javascript" src="/influence_gen_portal/static/src/js/components/file_uploader_component.js"></script>
                    <script type="text/javascript" src="/influence_gen_portal/static/src/js/components/ai_image_generator_component.js"></script>
                    
                    <!-- Main portal JS, if any -->
                    <!-- <script type="text/javascript" src="/influence_gen_portal/static/src/js/portal_main.js"></script> -->
                </xpath>
            </template>

            <template id="assets_qweb_influence_gen" name="InfluenceGen Portal QWeb Assets" inherit_id="web.assets_qweb">
                <xpath expr="." position="inside">
                    <template src="/influence_gen_portal/static/src/xml/components/abstract_form_component.xml"/>
                    <template src="/influence_gen_portal/static/src/xml/components/file_uploader_component.xml"/>
                    <template src="/influence_gen_portal/static/src/xml/components/ai_image_generator_component.xml"/>
                </xpath>
            </template>
        </data>
    </odoo>
    
*   **Requirements Met**: REQ-UIUX-001, REQ-DDSI-001

---

### 4.4. Static Resources (JavaScript - OWL Components & Services)

#### 4.4.1. `odoo_modules/influence_gen_portal/static/src/js/components/abstract_form_component.js`
*   **Description**: Abstract OWL component for base form functionality.
*   **Purpose**: Reusable logic for portal forms (validation, submission).
*   **Namespace**: `influence_gen_portal.AbstractFormComponent`
*   **Extends**: `owl.Component`
*   **Props**:
    *   `submitUrl` (String, required): URL to submit the form data to.
    *   `initialData` (Object, optional): Initial data to populate the form.
    *   `validationRules` (Object, optional): Field-specific validation rules (e.g., `{fieldName: [{type: 'required'}, {type: 'email'}]}`).
    *   `successRedirectUrl` (String, optional): URL to redirect to on successful submission.
*   **State**:
    *   `formData` (Object): Holds current form field values.
    *   `formErrors` (Object): Holds error messages for fields.
    *   `isSubmitting` (Boolean): Tracks submission state.
    *   `globalError` (String): For non-field specific errors.
*   **Methods**:
    *   `setup()`: Initialize `formData` from `initialData` or empty, initialize `formErrors`.
    *   `_onInputChange(event)`: Update `formData` for the changed field. Clear field-specific error. Optionally, trigger field validation.
    *   `_validateField(fieldName, value)`: Validate a single field based on `validationRules`. Update `formErrors[fieldName]`. Return `true` if valid.
    *   `_validateForm()`: Iterate through all fields, call `_validateField`. Return `true` if all valid.
    *   `async _onSubmit(event)`:
        1.  Prevent default form submission.
        2.  Set `isSubmitting = true`, clear `globalError`.
        3.  If `_validateForm()` is false, set `isSubmitting = false` and return.
        4.  Call `portal_service.rpc(this.props.submitUrl, this.state.formData)` (or a more specific service method).
        5.  Handle success:
            *   Display success notification.
            *   If `successRedirectUrl`, redirect.
            *   Optionally, emit a 'form-submitted' event with response.
        6.  Handle error:
            *   Set `globalError` or field-specific errors from response.
            *   Display error notification.
        7.  Set `isSubmitting = false`.
*   **Template (`abstract_form_component.xml`)**:
    *   A generic `<form>` structure.
    *   Slots for form fields to be defined by extending components.
    *   Displays `globalError`.
    *   Submit button with `isSubmitting` state.
*   **Requirements Met**: REQ-IOKYC-014 (client-side part)

#### 4.4.2. `odoo_modules/influence_gen_portal/static/src/js/components/file_uploader_component.js`
*   **Description**: OWL component for file uploads.
*   **Purpose**: Interactive UI for selecting and uploading files.
*   **Namespace**: `influence_gen_portal.FileUploaderComponent`
*   **Extends**: `owl.Component`
*   **Props**:
    *   `acceptedFileTypes` (String, required): Comma-separated list of MIME types or extensions (e.g., "image/jpeg,image/png,.pdf").
    *   `maxFileSize` (Number, optional): Max file size in bytes.
    *   `uploadUrl` (String, required): Backend URL to upload files to.
    *   `fieldName` (String, required): Name of the file input field for the backend.
    *   `multiple` (Boolean, optional, default: false): Allow multiple file selection.
    *   `label` (String, optional, default: "Upload File(s)"): Label for the uploader.
*   **State**:
    *   `selectedFiles` (Array<Object>): List of file objects selected by user, with properties like `name`, `size`, `type`, `status ('pending'|'uploading'|'success'|'error')`, `progress (0-100)`, `errorMessage`.
*   **Methods**:
    *   `setup()`: Initialize `selectedFiles`.
    *   `_onFileDrop(event)`, `_onFileChange(event)`: Handle file selection. Call `_addFilesToList`.
    *   `_addFilesToList(fileList)`:
        1.  Iterate through `fileList`.
        2.  For each file, call `_validateFile`.
        3.  If valid, add to `selectedFiles` with 'pending' status.
        4.  Optionally, auto-start upload by calling `_uploadFile`.
    *   `_validateFile(file)`: Check against `acceptedFileTypes` and `maxFileSize`. Return `true` or error message.
    *   `async _uploadFile(fileObject)`:
        1.  Update `fileObject.status` to 'uploading', `progress` to 0.
        2.  Use `XMLHttpRequest` or `fetch` with `portal_service` for CSRF to POST to `uploadUrl`.
        3.  Update `fileObject.progress` based on XHR progress events.
        4.  On success: update `fileObject.status` to 'success', store server response (e.g., attachment ID). Emit 'upload-success' event.
        5.  On error: update `fileObject.status` to 'error', `errorMessage`. Emit 'upload-error' event.
    *   `startUpload(fileObject)`: Manually trigger `_uploadFile` if not auto-started.
    *   `removeFile(fileObject)`: Remove file from `selectedFiles`. If uploading, abort XHR.
*   **Template (`file_uploader_component.xml`)**:
    *   File input `<input type="file">`.
    *   Drag-and-drop area.
    *   List of selected files: display name, size, status, progress bar, remove button.
    *   Display validation errors.
*   **Requirements Met**: REQ-IOKYC-004, REQ-2-009, REQ-IOKYC-014 (file type/size validation)

#### 4.4.3. `odoo_modules/influence_gen_portal/static/src/js/components/ai_image_generator_component.js`
*   **Description**: Main OWL component for AI Image Generation.
*   **Purpose**: Interactive UI for generating AI images.
*   **Namespace**: `influence_gen_portal.AIImageGeneratorComponent`
*   **Extends**: `owl.Component`
*   **Props**:
    *   `initialQuota` (Object, optional): User's current quota `{ used: number, total: number }`.
    *   `defaultParams` (Object, optional): Default generation parameters from admin config.
    *   `paramRanges` (Object, optional): Allowed ranges/options for parameters from admin config.
*   **State**:
    *   `prompt` (String): Current positive prompt.
    *   `negativePrompt` (String): Current negative prompt.
    *   `generationParams` (Object): Current selected parameters (resolution, aspect_ratio, model_id, seed, steps, cfg_scale).
    *   `availableModels` (Array<Object>): List of AI models fetched from backend.
    *   `generatedImages` (Array<Object>): List of `{ id, url, requestId, status }`.
    *   `isLoading` (Boolean): True while a request is processing.
    *   `errorMessage` (String): Error message from generation or validation.
    *   `quotaStatus` (Object): Updated quota.
    *   `savedPrompts` (Array<String>): User's saved prompts.
    *   `templatePrompts` (Array<String>): Admin-defined template prompts.
    *   `activeRequestId` (String): ID of the current generation request being polled.
*   **Methods**:
    *   `setup()`: Initialize state variables.
    *   `onWillStart()`: Call `_loadInitialData`.
    *   `async _loadInitialData()`:
        1.  Fetch `availableModels` using `ai_image_service.getAvailableModels()`.
        2.  Fetch `savedPrompts` using `ai_image_service.getSavedPrompts()`.
        3.  Fetch `templatePrompts` (needs a service method).
        4.  Initialize `generationParams` with `props.defaultParams`.
        5.  Initialize `quotaStatus` with `props.initialQuota`.
    *   `async generateImage()`:
        1.  Set `isLoading = true`, clear `errorMessage`, `generatedImages = []`.
        2.  Validate prompts and parameters against `props.paramRanges` and content moderation (client-side check if possible, server will re-check). (REQ-16-007 for UI feedback on moderation).
        3.  If validation fails, set `errorMessage`, `isLoading = false`, return.
        4.  Call `ai_image_service.initiateGeneration({ prompt, negativePrompt, ...generationParams })`.
        5.  If successful, store `activeRequestId`, start polling `_pollGenerationStatus`.
        6.  Else, call `_handleGenerationError`. (REQ-16-006 for UI feedback)
    *   `async _pollGenerationStatus()`:
        1.  Periodically call `ai_image_service.checkGenerationStatus(this.state.activeRequestId)`.
        2.  If 'completed': call `_handleGenerationResult`, stop polling.
        3.  If 'failed': call `_handleGenerationError`, stop polling.
        4.  If 'processing': continue polling (with timeout/max retries).
        5.  Display progress/status to user (REQ-AIGS-008, REQ-16-006).
    *   `_handleGenerationResult(result)`:
        1.  Set `isLoading = false`.
        2.  Update `generatedImages` with `result.images`.
        3.  Update `quotaStatus` if info available in result.
    *   `_handleGenerationError(error)`:
        1.  Set `isLoading = false`.
        2.  Set `errorMessage` (e.g., error.message or "Generation failed.").
    *   `downloadImage(imageUrl)`: Trigger browser download.
    *   `useImageInCampaign(image)`: Emit event or call service to associate image with a campaign (logic TBD based on how this is integrated with content submission). (REQ-2-016)
    *   `async savePrompt()`: Call `ai_image_service.saveUserPrompt(this.state.prompt)`. Add to `savedPrompts` on success.
    *   `reusePrompt(promptText)`: Set `this.state.prompt = promptText`.
    *   `_updateParam(paramName, value)`: Update `this.state.generationParams[paramName] = value`.
*   **Template (`ai_image_generator_component.xml`)**:
    *   Input field for `prompt`.
    *   Input field for `negativePrompt`.
    *   Controls for `generationParams`: dropdown for `model_id`, sliders/inputs for `resolution`, `aspect_ratio`, `seed`, `steps`, `cfg_scale`. Enforce ranges from `props.paramRanges`. (REQ-UIUX-004, REQ-UIUX-022)
    *   Section to display `savedPrompts` and `templatePrompts` for reuse. (REQ-UIUX-021)
    *   "Generate" button, disabled when `isLoading`.
    *   Loading indicator/progress message when `isLoading`. (REQ-UIUX-005, REQ-16-006)
    *   Display `errorMessage`.
    *   Display `quotaStatus`.
    *   Area to display `generatedImages`: loop, show `<img>`, download button, "Use in Campaign" button. (REQ-UIUX-005)
*   **Requirements Met**: REQ-AIGS-001, REQ-AIGS-005, REQ-AIGS-008, REQ-AIGS-010, REQ-IPDPM-006, REQ-UIUX-004, REQ-UIUX-005, REQ-UIUX-021, REQ-UIUX-022, REQ-16-006, REQ-16-007, REQ-2-016

#### 4.4.4. `odoo_modules/influence_gen_portal/static/src/js/services/portal_service.js`
*   **Description**: JS service for portal utility functions.
*   **Purpose**: Abstracts backend calls and UI notifications.
*   **Namespace**: `influence_gen_portal.services.portal`
*   **Methods**:
    *   `async rpc(route, params = {}, method = 'call')`:
        *   Uses `odoo.core.serviceRegistry.get('rpc')` or `this.env.services.rpc` if in an OWL component context (if this service is meant to be an OWL service). If a global utility, it might need direct access to `odoo.define` and `ajax.rpc`.
        *   Constructs the full URL or Odoo RPC parameters.
        *   Handles CSRF token automatically if using Odoo's RPC.
        *   Returns a Promise.
    *   `notify(message, type = 'info', sticky = false)`:
        *   Uses `odoo.core.serviceRegistry.get('notification').add()` or `this.env.services.notification.add()`.
        *   Types: 'info', 'success', 'warning', 'danger'.
*   **Requirements Met**: REQ-UIUX-007 (indirectly by enabling fast AJAX), REQ-UIUX-009 (by providing notification mechanism)

#### 4.4.5. `odoo_modules/influence_gen_portal/static/src/js/services/ai_image_service.js`
*   **Description**: JS service for AI image generation client-side logic.
*   **Purpose**: Encapsulates API calls for AI image generation.
*   **Namespace**: `influence_gen_portal.services.aiImage`
*   **Dependencies**: `portal_service`
*   **Methods**:
    *   `async initiateGeneration(params)`:
        *   Calls `portal_service.rpc('/my/ai/generate', params, 'POST')`.
        *   Returns Promise<Object> (`{request_id, status}`).
    *   `async checkGenerationStatus(requestId)`:
        *   Calls `portal_service.rpc('/my/ai/generate/status', { request_id: requestId }, 'GET')`.
        *   Returns Promise<Object> (`{request_id, status, images?, error_message?}`).
    *   `async getAvailableModels()`:
        *   Calls `portal_service.rpc('/my/ai/models', {}, 'GET')` (Backend controller for this needed, likely in `portal_ai_image_controller.py` or a config service).
        *   Returns Promise<Array>.
    *   `async getSavedPrompts()`:
        *   Calls `portal_service.rpc('/my/ai/prompts/saved', {}, 'GET')` (Backend controller needed).
        *   Returns Promise<Array>.
    *   `async saveUserPrompt(promptText)`:
        *   Calls `portal_service.rpc('/my/ai/prompts/save', { prompt: promptText }, 'POST')` (Backend controller needed).
        *   Returns Promise<void>.
*   **Requirements Met**: REQ-AIGS-001, REQ-AIGS-010, REQ-UIUX-021

#### 4.4.6. `odoo_modules/influence_gen_portal/static/src/js/utils/accessibility_utils.js`
*   **Description**: Utility functions for WCAG compliance.
*   **Purpose**: Common JS utilities for accessibility.
*   **Namespace**: `influence_gen_portal.utils.accessibility`
*   **Methods**:
    *   `manageFocus(elementSelector)`: Safely attempts to set focus to the element.
        javascript
        // Example
        const el = document.querySelector(elementSelector);
        if (el && typeof el.focus === 'function') {
            el.focus();
        }
        
    *   `announceToScreenReader(message)`:
        *   Creates or uses an existing ARIA live region (`aria-live="assertive"` or `"polite"`) and updates its content with `message`.
    *   `checkColorContrast(fgColor, bgColor)`: (Primarily a dev tool, not runtime typically)
        *   Algorithm to calculate contrast ratio. For runtime, this would be a design system concern.
*   **Requirements Met**: REQ-14-001, REQ-14-002, REQ-14-003, REQ-14-004

#### 4.4.7. `odoo_modules/influence_gen_portal/static/src/js/utils/localization_utils.js`
*   **Description**: Utilities for client-side localization.
*   **Purpose**: Supplements Odoo's localization if needed.
*   **Namespace**: `influence_gen_portal.utils.localization`
*   **Note**: Odoo's framework (`@web/core/l10n/localization`) and field formatters (`@web/views/fields/formatters`) should be preferred. This utility might be minimal or not needed if Odoo's built-ins are sufficient.
*   **Methods**:
    *   `formatDate(date, locale)`: (Likely not needed, use Odoo's field widgets or server-formatted strings).
    *   `formatCurrency(amount, currencyCode, locale)`: (Likely not needed, use Odoo's field widgets or server-formatted strings).
*   **Requirements Met**: REQ-UIUX-014 (mostly by relying on Odoo core)

#### 4.4.8. `odoo_modules/influence_gen_portal/static/src/js/portal_main.js` (Optional)
*   **Description**: Main JavaScript file for global portal behaviors not tied to specific OWL components.
*   **Purpose**: Initialize global event listeners, common UI enhancements.
*   **Logic**:
    *   Could include initialization for in-app guidance tours (e.g., using a library like Shepherd.js or Intro.js) if complex tours are needed.
    *   Event listeners for common portal actions.
    *   This file might be very lean or unnecessary if most logic is in OWL components.

---

### 4.5. Static Resources (SCSS)

#### 4.5.1. `odoo_modules/influence_gen_portal/static/src/scss/portal_main.scss`
*   **Description**: Main SCSS file for the portal.
*   **Purpose**: Aggregates all SCSS, applies global styles.
*   **Structure**:
    scss
    // 1. Variables & Mixins (if any custom ones, or import Odoo's)
    // @import "variables";
    // @import "mixins";

    // 2. Base/Global Styles (body, typography, links specific to portal)
    // @import "base";

    // 3. Layout Styles (header, footer, sidebar adjustments for portal)
    // @import "layout";

    // 4. Component-Specific Styles
    // @import "components/file_uploader";
    // @import "components/ai_image_generator";
    // @import "components/dashboard_widgets";

    // 5. Page-Specific Styles
    // @import "pages/profile";
    // @import "pages/campaign_discovery";

    // 6. Accessibility Styles (imported)
    @import "accessibility";

    // 7. Responsive Styles (imported)
    @import "responsive";
    
*   **Requirements Met**: REQ-UIUX-001, REQ-UIUX-002, REQ-UIUX-010

#### 4.5.2. `odoo_modules/influence_gen_portal/static/src/scss/accessibility.scss`
*   **Description**: SCSS for accessibility enhancements.
*   **Purpose**: Styles for WCAG compliance.
*   **Content**:
    *   Styles for highly visible focus indicators on all focusable elements (`:focus`, `:focus-visible`).
    *   `sr-only` or `visually-hidden` classes for text intended only for screen readers.
    *   Ensure sufficient contrast for custom components if Odoo defaults are overridden.
    *   Styles to support "information not conveyed by color alone" (e.g., icons with text, underlines for links in text blocks).
*   **Requirements Met**: REQ-14-001, REQ-14-002, REQ-14-004, REQ-UIUX-020

#### 4.5.3. `odoo_modules/influence_gen_portal/static/src/scss/responsive.scss`
*   **Description**: SCSS for responsive design.
*   **Purpose**: Adapts UI to different screen sizes.
*   **Content**:
    *   `@media` queries for common breakpoints (e.g., mobile, tablet, desktop).
    *   Adjustments to grid layouts, font sizes, element visibility, navigation menus (e.g., collapsing to a hamburger menu).
    *   Ensure Odoo's responsive classes (`d-none`, `d-md-block`, etc.) are used appropriately.
*   **Requirements Met**: REQ-UIUX-002, REQ-IPDPM-008

---

### 4.6. Internationalization (i18n)

#### 4.6.1. `odoo_modules/influence_gen_portal/i18n/influence_gen_portal.pot`
*   **Description**: Main translation template file.
*   **Purpose**: Base for language-specific .po files.
*   **Generation**: This file will be automatically generated by Odoo's i18n tools (`odoo-bin ... --i18n-export`). Developers must ensure all user-facing strings in Python, XML (QWeb), and JavaScript (OWL) are correctly marked for translation (e.g., `_("string")` in Python, `t-esc="_t('string')"` or `_t("string")` in JS/XML).
*   **Requirements Met**: REQ-UIUX-013

---

### 4.7. Data Files

#### 4.7.1. `odoo_modules/influence_gen_portal/data/ir_ui_menu_data.xml`
*   **Description**: XML defining portal menu items.
*   **Purpose**: Creates navigation structure in the influencer portal.
*   **Logic Description**:
    xml
    <odoo>
        <data noupdate="1"> <!-- noupdate="1" to prevent overriding on module update if customized -->
            <!-- Main Portal Menu for InfluenceGen -->
            <menuitem name="InfluenceGen Dashboard" id="menu_influence_gen_dashboard"
                      parent="portal.portal_my_home" sequence="10"
                      action="action_influence_gen_dashboard"/>
            <record id="action_influence_gen_dashboard" model="ir.actions.act_url">
                <field name="name">Dashboard</field>
                <field name="url">/my/dashboard</field>
                <field name="target">self</field>
            </record>

            <menuitem name="My Profile" id="menu_influence_gen_profile"
                      parent="portal.portal_my_home" sequence="20"
                      action="action_influence_gen_profile"/>
            <record id="action_influence_gen_profile" model="ir.actions.act_url">
                <field name="name">My Profile</field>
                <field name="url">/my/profile</field>
                <field name="target">self</field>
            </record>

            <menuitem name="Campaigns" id="menu_influence_gen_campaigns"
                      parent="portal.portal_my_home" sequence="30"
                      action="action_influence_gen_campaigns"/>
            <record id="action_influence_gen_campaigns" model="ir.actions.act_url">
                <field name="name">Campaigns</field>
                <field name="url">/my/campaigns</field>
                <field name="target">self</field>
            </record>

            <menuitem name="AI Image Generator" id="menu_influence_gen_ai_image"
                      parent="portal.portal_my_home" sequence="40"
                      action="action_influence_gen_ai_image"/>
            <record id="action_influence_gen_ai_image" model="ir.actions.act_url">
                <field name="name">AI Image Generator</field>
                <field name="url">/my/ai-image-generator</field>
                <field name="target">self</field>
            </record>

            <menuitem name="Payments" id="menu_influence_gen_payments"
                      parent="portal.portal_my_home" sequence="50"
                      action="action_influence_gen_payments"/>
            <record id="action_influence_gen_payments" model="ir.actions.act_url">
                <field name="name">Payments</field>
                <field name="url">/my/payments</field>
                <field name="target">self</field>
            </record>

            <menuitem name="Performance" id="menu_influence_gen_performance"
                      parent="portal.portal_my_home" sequence="60"
                      action="action_influence_gen_performance"/>
            <record id="action_influence_gen_performance" model="ir.actions.act_url">
                <field name="name">Performance</field>
                <field name="url">/my/performance</field>
                <field name="target">self</field>
            </record>
            
            <menuitem name="Consent Management" id="menu_influence_gen_consent"
                      parent="portal.portal_my_home" sequence="70"
                      action="action_influence_gen_consent"/>
            <record id="action_influence_gen_consent" model="ir.actions.act_url">
                <field name="name">Terms & Consent</field>
                <field name="url">/my/consent</field>
                <field name="target">self</field>
            </record>

            <!-- Add Help/Documentation link if it's an external URL or a specific portal page -->
            <menuitem name="Help & Documentation" id="menu_influence_gen_help"
                      parent="portal.portal_my_home" sequence="100"
                      action="action_influence_gen_help_kb"/> 
            <record id="action_influence_gen_help_kb" model="ir.actions.act_url">
                <field name="name">Help & Documentation</field>
                <field name="url">/help/influencegen</field> <!-- Example URL for KB, adjust as needed -->
                <field name="target">self</field>
            </record>

        </data>
    </odoo>
    
*   **Requirements Met**: REQ-IPDPM-001, REQ-IPDPM-004, REQ-IPDPM-005, REQ-IPDPM-006, REQ-IPDPM-007

---

### 4.8. Security Files

#### 4.8.1. `odoo_modules/influence_gen_portal/security/ir.model.access.csv`
*   **Description**: Defines model access rights.
*   **Purpose**: Control CRUD permissions for models.
*   **Note**: Since most data models reside in the business services layer (`REPO-IGBS-003`), this file might be minimal or empty if no new models are defined directly within `influence_gen_portal`. Access to portal pages is controlled by controller `auth` types and potentially route-specific checks. If any helper models are created within this portal module (e.g., for transient data for a complex form), their access rights would be defined here. Typically, portal users interact via controllers, not direct model access.
*   **Example (if a portal-specific helper model `influence_gen_portal.helper` existed)**:
    csv
    id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
    access_influence_gen_portal_helper_portal_user,influence_gen_portal.helper portal user,model_influence_gen_portal_helper,base.group_portal,1,1,1,0
    

#### 4.8.2. `odoo_modules/influence_gen_portal/security/influence_gen_portal_security.xml`
*   **Description**: XML file for defining security groups or record rules specific to portal access, if needed beyond Odoo's default portal group.
*   **Purpose**: Fine-grained access control for portal functionalities.
*   **Logic Description**:
    *   Could define a specific group for "Verified Influencers" if access to certain portal sections is conditional on KYC approval, beyond just being a `portal_user`.
        xml
        <odoo>
            <data>
                <!-- <record id="group_influence_gen_verified_influencer" model="res.groups">
                    <field name="name">Verified Influencer</field>
                    <field name="category_id" ref="base.module_category_hidden"/>
                    <field name="implied_ids" eval="[(4, ref('base.group_portal'))]"/>
                </record> -->

                <!-- Record rules might be used to restrict access to certain portal controller routes if Odoo's
                     standard auth='user' and checks within controllers are not sufficient.
                     Example: A record rule on a menu item to make it visible only to verified influencers.
                     However, controller logic is often preferred for portal page access. -->
            </data>
        </odoo>
        
    *   **Note**: Most access control for portal pages will be handled by `auth='user'` on controller routes and then further checks within the controller methods (e.g., `if request.env.user.influencer_profile_id.kyc_status != 'approved': raise werkzeug.exceptions.Forbidden()`). This file might primarily be used if specific groups are needed to show/hide menu items via `groups` attribute on `<menuitem>`.

## 5. Data Model (Brief Overview)

This module primarily interacts with data models defined in `InfluenceGen.Odoo.Business.Services` (REPO-IGBS-003). The UI layer (`influence_gen_portal`) does not define its own persistent data models but rather renders and collects data for those models. Key data entities interacted with include:
*   `influence_gen.influencer_profile`
*   `influence_gen.kyc_data`
*   `influence_gen.social_media_profile`
*   `influence_gen.bank_account`
*   `influence_gen.campaign`
*   `influence_gen.campaign_application`
*   `influence_gen.content_submission`
*   `influence_gen.ai_image_generation_request`
*   `influence_gen.generated_image`
*   `influence_gen.payment_record`
*   `influence_gen.terms_consent`

## 6. Interface Definitions

### 6.1. User Interfaces
As detailed in section 4.3 (Views) and 4.4 (Static Resources - OWL Components).

### 6.2. Internal Interfaces (Controller to Service)
Controllers in this module will call public methods on services defined in `InfluenceGen.Odoo.Business.Services`. Examples:
*   `request.env['influence_gen.onboarding_service'].process_registration_data(data)`
*   `request.env['influence_gen.campaign_service'].get_discoverable_campaigns(filters)`
*   `request.env['influence_gen.ai_image_service'].initiate_generation_request(user_id, params)`

### 6.3. External Interfaces (Controller to Client - AJAX)
*   `/my/ai/generate` (POST, JSON): For `portal_ai_image_controller.initiate_ai_image_generation`.
*   `/my/ai/generate/status` (GET, JSON): For `portal_ai_image_controller.get_ai_image_generation_status`.
*   Other AJAX endpoints if specific OWL components require them for partial updates or complex interactions not covered by full page loads/form submissions.

## 7. Non-Functional Requirements Implementation

*   **Performance (REQ-UIUX-007)**: Achieved through efficient QWeb rendering, optimized OWL components, judicious use of AJAX, and reliance on performant business layer services. Page load times and interaction responsiveness will be primary metrics.
*   **Scalability**: This UI layer scales with Odoo's web server capabilities. Asynchronous operations (AI image gen) offload heavy work.
*   **Security**: `auth='user'` on routes, CSRF protection on POSTs, client-side validation for UX, server-side validation by business layer, secure file handling delegated to business layer.
*   **Usability (REQ-UIUX-008, REQ-IPDPM-009)**: Adherence to Odoo UI/UX, clear navigation, informative messages (REQ-UIUX-009, REQ-16-013), in-app guidance (REQ-UIUX-011).
*   **Accessibility (REQ-14-\*, REQ-UIUX-020)**: Implemented via semantic HTML in QWeb, ARIA attributes, keyboard navigation support in OWL/JS, sufficient color contrast in SCSS, alt text for images. Use of `accessibility_utils.js`.
*   **Maintainability**: Modular controllers, templates, and OWL components. Adherence to Odoo best practices.
*   **Localization (REQ-UIUX-013, REQ-UIUX-014)**: All strings translatable. Date/number/currency formatting relies on Odoo's localization.

## 8. Error Handling and Logging

*   User-facing errors displayed via QWeb templates or JS notifications (`portal_service.notify`). Messages will be clear and actionable (REQ-UIUX-009, REQ-16-013).
*   Controller methods will catch exceptions from business service calls and translate them into user-friendly error messages or appropriate HTTP error responses.
*   Client-side JavaScript (OWL components, services) will handle AJAX errors and update UI accordingly.
*   Detailed operational logging is primarily the responsibility of the business and infrastructure layers. This UI layer contributes to logs via Odoo's standard request logging and any specific logging added in controllers if needed for UI-specific issues.

## 9. Deployment Considerations

This module will be deployed as a standard Odoo addon. Dependencies must be installed. Assets (JS, SCSS) will be compiled and bundled by Odoo.

## 10. Future Considerations
*   Integration of more sophisticated client-side frameworks if OWL proves insufficient for complex UI needs (unlikely for standard portal).
*   WebSockets for real-time updates (e.g., AI image generation status) instead of polling, if Odoo infrastructure supports it easily.

# AI Code Generation Instructions

**General Instructions for AI:**
1.  **Target Odoo Version**: Strictly Odoo 18.
2.  **Languages**: Python 3.11+ for controllers, JavaScript (ES2022+) for OWL components and services, XML for QWeb templates and OWL component templates, SCSS for styles.
3.  **Frameworks**: Odoo HTTP Controllers, Odoo Portal framework, QWeb, OWL 2.
4.  **Dependencies**:
    *   This module (`influence_gen_portal`) depends on `portal`, `website`, `mail`, and an assumed core business logic module named `influence_gen_business_services`. When interacting with business logic, use `request.env['model.name'].sudo(user_id_if_needed_for_specific_user_context_else_current_user_is_fine).method_name(...)`.
    *   For portal controllers, ensure `auth='user'` and `website=True` for routes requiring login, and `auth='public'` for public registration pages. Use `csrf=True` for POST routes.
5.  **Code Style**: Adhere to Odoo development guidelines and Python PEP 8. JavaScript should follow modern best practices (e.g., ESLint with a common configuration).
6.  **Error Handling**: Implement robust error handling. User-facing errors must be clear and informative. Log technical details for backend issues (logging primarily handled by business layer).
7.  **Security**:
    *   Validate all user inputs on the client-side for UX and robustly on the server-side (delegated to business services).
    *   Use Odoo's CSRF protection for all state-changing POST requests.
    *   Access control in controllers: check `request.env.user` and associated `influencer_profile_id` for permissions before rendering pages or processing actions.
8.  **Localization**: All user-facing strings in Python code, XML templates, and JavaScript must be translatable (e.g., `_("Text")` in Python, `t-esc="_t('Text')"` or `_t("Text")` in JS/XML).
9.  **Accessibility (WCAG 2.1 AA)**:
    *   Use semantic HTML5 elements.
    *   Provide `alt` text for all informative images.
    *   Ensure all interactive elements are keyboard accessible and have visible focus indicators.
    *   Use ARIA attributes appropriately to define roles, states, and properties for custom widgets or dynamic content.
    *   Ensure sufficient color contrast (primarily a SCSS/design concern, but be mindful).
10. **Comments**: Add clear comments explaining complex logic or non-obvious decisions. Generate Odoo standard documentation strings for Python methods and classes.
11. **Modularity**: Keep components and controllers focused on their specific responsibilities.

**Instructions per File Type:**

*   **For `__manifest__.py`**:
    *   Generate the manifest dictionary as detailed in SDS section 4.1.1. Ensure all dependencies, data files, and asset files are correctly listed.
*   **For `__init__.py` files**:
    *   Generate simple import statements as detailed in the SDS.
*   **For Python Controllers (`*.py` in `controllers/`)**:
    *   Create classes inheriting from `odoo.http.Controller`.
    *   Implement methods with `@http.route(...)` decorators as specified in the SDS for each controller.
    *   For methods rendering QWeb templates:
        *   Fetch necessary data by calling services from `influence_gen_business_services` (e.g., `request.env['influence_gen.onboarding_service']`).
        *   Prepare a `qcontext` dictionary with data for the template.
        *   Render the template using `request.render('module_name.template_id', qcontext)`.
    *   For JSON endpoints:
        *   Set `type='json'`.
        *   Process input parameters.
        *   Call business services.
        *   Return Python dictionaries which Odoo will serialize to JSON.
    *   Implement security checks (e.g., ensuring the logged-in user is an influencer and has rights to access/modify specific data).
*   **For QWeb Templates (`*.xml` in `views/`)**:
    *   Use Odoo QWeb syntax (`t-name`, `t-extend`, `t-foreach`, `t-if`, `t-esc`, `t-attf`, `t-call`).
    *   Inherit from `influence_gen_portal.portal_layout` or `portal.portal_layout` for consistent portal styling.
    *   Structure HTML semantically for accessibility.
    *   Use Odoo's form helpers and Bootstrap classes for layout and styling.
    *   Include placeholders for dynamic data passed from controllers.
    *   For forms, ensure `csrf_token` is included if not using Odoo's form helpers that add it automatically.
    *   Mount OWL components where specified (e.g., `<div t-component="module_name.ComponentName" t-props="props_dict"/>`).
*   **For OWL Components (`*.js` and `*.xml` in `static/src/`)**:
    *   **JS File**:
        *   Import necessary modules from `@odoo/owl` (e.g., `Component`, `useState`, `onWillStart`, `useRef`).
        *   Define component class extending `Component`.
        *   Define `props` (static defaultProps if needed).
        *   Use `useState` for reactive state.
        *   Implement `setup` for initialization, event listeners, and service instantiation.
        *   Implement methods for event handling and business logic (e.g., calling JS services).
        *   Define `static template = "module_name.ComponentNameTemplate";`
    *   **XML File (Template)**:
        *   Define the component's template using QWeb syntax within `<templates><t t-name="module_name.ComponentNameTemplate">...</t></templates>`.
        *   Use OWL directives (`t-on-click`, `t-model`, `t-if`, `t-foreach`, `t-att`, `t-props`).
        *   Ensure accessibility (ARIA attributes, keyboard interactions if custom).
*   **For JavaScript Services (`*.js` in `static/src/services/`)**:
    *   Define an object or class with static methods, or an OWL-style service.
    *   Use `odoo.define` for Odoo JS module system.
    *   For `portal_service.rpc`: leverage `@web/core/network/rpc_service` or `odoo.ajax.rpc`.
    *   For `portal_service.notify`: leverage `@web/core/notifications/notification_service`.
*   **For JavaScript Utilities (`*.js` in `static/src/utils/`)**:
    *   Define utility functions. Use `odoo.define` if they need to be part of Odoo's JS registry.
*   **For SCSS Files (`*.scss` in `static/src/scss/`)**:
    *   Write SCSS adhering to BEM or a similar methodology for clarity.
    *   Use variables for colors, fonts, spacing to maintain consistency.
    *   Implement responsive styles using media queries.
    *   Ensure accessibility for focus indicators and contrast.
*   **For Data XML Files (`*.xml` in `data/`)**:
    *   Generate `ir.ui.menu` records as specified, ensuring correct `parent_id`, `action`, and `sequence`.
    *   Generate `ir.actions.act_url` records for menu actions.
*   **For Security XML/CSV Files (`*.xml`, `*.csv` in `security/`)**:
    *   Generate `ir.model.access.csv` entries if any new models are directly defined in this portal module (unlikely).
    *   Generate `res.groups` or `ir.rule` records in the XML file if specific portal security group logic is needed beyond controller-level checks.

**Specific File Instructions will follow the SDS structure provided.**
Focus on the logic descriptions and method signatures from the SDS when generating code for each file.
Ensure calls to the business layer `influence_gen_business_services` are correctly formulated (e.g., `request.env['influence_gen.module_name'].method_name(...)`).