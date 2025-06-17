# Architecture Design Specification

# 1. Components

- **Components:**
  
  ### .1. InfluencerPortalComponent
  Provides all UI elements for the influencer-facing portal within Odoo. This includes forms, dashboards, lists, and interactive elements built with Odoo's presentation framework (XML Views, QWeb Templates, OWL Components).

  #### .1.4. Type
  Odoo UI Module

  #### .1.5. Dependencies
  
  - ig-bl-001
  - ig-bl-002
  - ig-bl-003
  - ig-bl-004
  - ig-bl-006
  
  #### .1.6. Properties
  
  - **Module Name:** influence_gen_portal
  
  #### .1.7. Interfaces
  
  
  #### .1.8. Technology
  Odoo 18 (XML, QWeb, OWL, CSS, Python Controllers)

  #### .1.9. Resources
  
  - **Cpu:** Shared with Odoo Application Server
  - **Memory:** Shared with Odoo Application Server
  - **Storage:** N/A (UI component)
  - **Network:** N/A (UI component)
  
  #### .1.10. Configuration
  
  - **View Inheritance:** Standard Odoo view extension mechanisms
  - **Owl Component Registration:** Standard OWL registration
  
  #### .1.11. Health Check
  None

  #### .1.12. Responsible Features
  
  - REQ-IOKYC-001
  - REQ-IOKYC-004
  - REQ-2-004
  - REQ-2-005
  - REQ-2-006
  - REQ-2-009
  - REQ-AIGS-005
  - REQ-AIGS-008
  - REQ-IPDPM-001
  - REQ-IPDPM-002
  - REQ-IPDPM-003
  - REQ-IPDPM-004
  - REQ-IPDPM-005
  - REQ-IPDPM-006
  - REQ-IPDPM-007
  - REQ-IPDPM-008
  - REQ-IPDPM-009
  - REQ-IPDPM-010
  - REQ-IPDPM-011
  - REQ-UIUX-001
  - REQ-UIUX-002
  - REQ-UIUX-004
  - REQ-UIUX-005
  - REQ-UIUX-007
  - REQ-UIUX-008
  - REQ-UIUX-009
  - REQ-UIUX-010
  - REQ-UIUX-011
  - REQ-UIUX-012
  - REQ-UIUX-013
  - REQ-UIUX-014
  - REQ-UIUX-017
  - REQ-UIUX-018
  - REQ-UIUX-019
  - REQ-UIUX-020
  - REQ-UIUX-021
  - REQ-UIUX-022
  - REQ-14-001
  - REQ-14-002
  - REQ-14-003
  - REQ-14-004
  - REQ-14-005
  - REQ-16-006
  - REQ-16-007
  - REQ-16-013
  
  #### .1.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  - **Allowed Roles:**
    
    - Influencer
    
  - **Data Visibility:** User-specific data based on Odoo record rules
  
  ### .2. AdminInterfaceComponent
  Provides all UI elements for platform administrators within the Odoo backend. This includes forms, lists, kanban views, reports, and configuration interfaces.

  #### .2.4. Type
  Odoo UI Module

  #### .2.5. Dependencies
  
  - ig-bl-001
  - ig-bl-002
  - ig-bl-003
  - ig-bl-004
  - ig-bl-005
  - ig-bl-007
  
  #### .2.6. Properties
  
  - **Module Name:** influence_gen_admin
  
  #### .2.7. Interfaces
  
  
  #### .2.8. Technology
  Odoo 18 (XML, Python Actions, Forms, Lists, Kanbans)

  #### .2.9. Resources
  
  - **Cpu:** Shared with Odoo Application Server
  - **Memory:** Shared with Odoo Application Server
  - **Storage:** N/A (UI component)
  - **Network:** N/A (UI component)
  
  #### .2.10. Configuration
  
  - **Menu Items:** Configured via XML data files
  - **Action Windows:** Defined via XML data files
  
  #### .2.11. Health Check
  None

  #### .2.12. Responsible Features
  
  - REQ-IOKYC-011
  - REQ-2-001
  - REQ-2-002
  - REQ-2-003
  - REQ-2-007
  - REQ-2-010
  - REQ-2-012
  - REQ-AIGS-002
  - REQ-AIGS-003
  - REQ-AIGS-004
  - REQ-AIGS-007
  - REQ-PAC-001
  - REQ-PAC-002
  - REQ-PAC-003
  - REQ-PAC-004
  - REQ-PAC-005
  - REQ-PAC-006
  - REQ-PAC-007
  - REQ-PAC-008
  - REQ-PAC-009
  - REQ-PAC-010
  - REQ-PAC-011
  - REQ-PAC-012
  - REQ-PAC-013
  - REQ-PAC-014
  - REQ-PAC-015
  - REQ-PAC-016
  - REQ-PAC-017
  - REQ-UIUX-003
  - REQ-UIUX-015
  - REQ-UIUX-016
  - REQ-UIUX-019
  - REQ-UIUX-021
  - REQ-UIUX-022
  - REQ-ATEL-003
  - REQ-ATEL-008
  - REQ-DRH-001
  - REQ-DRH-003
  - REQ-DRH-005
  - REQ-DRH-008
  - REQ-12-007
  - REQ-16-012
  
  #### .2.13. Security
  
  - **Requires Authentication:** True
  - **Requires Authorization:** True
  - **Allowed Roles:**
    
    - Platform Administrator
    - Finance Manager (subset)
    
  - **Data Visibility:** Full platform data access based on Odoo security groups
  
  ### .3. InfluencerOnboardingService
  Manages influencer registration, profile data, KYC processes, social media, and bank account verification. Encapsulates logic within Odoo Models: `influence_gen.influencer_profile`, `influence_gen.kyc_data`, `influence_gen.social_media_profile`, `influence_gen.bank_account`, `influence_gen.terms_consent`.

  #### .3.4. Type
  Odoo Business Logic Service/Module

  #### .3.5. Dependencies
  
  - ig-infra-004
  - ig-infra-005
  - ig-infra-002
  - ig-infra-006
  
  #### .3.6. Properties
  
  - **Main Models:**
    
    - influence_gen.influencer_profile
    - influence_gen.kyc_data
    - influence_gen.social_media_profile
    - influence_gen.bank_account
    - influence_gen.terms_consent
    
  
  #### .3.7. Interfaces
  
  
  #### .3.8. Technology
  Odoo 18 (Python, Odoo ORM)

  #### .3.9. Resources
  
  - **Cpu:** Shared with Odoo Application Server
  - **Memory:** Shared with Odoo Application Server
  
  #### .3.10. Configuration
  
  - **Kyc Verification Rules:** Configured via PlatformConfigService
  - **Unique Constraints:** Enforced at DB level via Odoo models
  
  #### .3.11. Health Check
  None

  #### .3.12. Responsible Features
  
  - REQ-IOKYC-002
  - REQ-IOKYC-003
  - REQ-IOKYC-005
  - REQ-IOKYC-006
  - REQ-IOKYC-007
  - REQ-IOKYC-008
  - REQ-IOKYC-009
  - REQ-IOKYC-012
  - REQ-IOKYC-014
  - REQ-IPF-001
  - REQ-IPF-002
  - REQ-DMG-002
  - REQ-DMG-003
  - REQ-DMG-014
  - REQ-DMG-015
  
  #### .3.13. Security
  
  - **Data Handling:** Handles PII, KYC documents, financial info. Must adhere to encryption and access control policies.
  
  ### .4. CampaignService
  Manages all aspects of campaign lifecycle, influencer applications, content submissions, and performance tracking. Encapsulates logic within Odoo Models: `influence_gen.campaign`, `influence_gen.campaign_application`, `influence_gen.content_submission`, and potentially `influence_gen.campaign_performance_mv`.

  #### .4.4. Type
  Odoo Business Logic Service/Module

  #### .4.5. Dependencies
  
  - ig-infra-004
  - ig-infra-005
  - ig-bl-004
  - ig-infra-002
  
  #### .4.6. Properties
  
  - **Main Models:**
    
    - influence_gen.campaign
    - influence_gen.campaign_application
    - influence_gen.content_submission
    
  
  #### .4.7. Interfaces
  
  
  #### .4.8. Technology
  Odoo 18 (Python, Odoo ORM)

  #### .4.9. Resources
  
  - **Cpu:** Shared with Odoo Application Server
  - **Memory:** Shared with Odoo Application Server
  
  #### .4.10. Configuration
  
  - **Campaign Status Transitions:** Managed by business logic within models
  - **Compensation Models:** Configurable per campaign
  
  #### .4.11. Health Check
  None

  #### .4.12. Responsible Features
  
  - REQ-2-001
  - REQ-2-002
  - REQ-2-003
  - REQ-2-004
  - REQ-2-006
  - REQ-2-007
  - REQ-2-009
  - REQ-2-010
  - REQ-2-011
  - REQ-2-012
  - REQ-2-013
  - REQ-2-016
  - REQ-2-017
  - REQ-DMG-004
  - REQ-DMG-005
  - REQ-DMG-006
  
  #### .4.13. Security
  
  - **Data Handling:** Manages campaign details, influencer applications, and content.
  
  ### .5. AIImageService
  Manages AI image generation requests, model configurations, generated image metadata, and usage tracking/quotas. Encapsulates logic within Odoo Models: `influence_gen.ai_image_model`, `influence_gen.ai_image_request`, `influence_gen.generated_image`.

  #### .5.4. Type
  Odoo Business Logic Service/Module

  #### .5.5. Dependencies
  
  - ig-infra-003
  - ig-infra-005
  - ig-infra-002
  - ig-bl-005
  
  #### .5.6. Properties
  
  - **Main Models:**
    
    - influence_gen.ai_image_model
    - influence_gen.ai_image_request
    - influence_gen.generated_image
    
  
  #### .5.7. Interfaces
  
  
  #### .5.8. Technology
  Odoo 18 (Python, Odoo ORM)

  #### .5.9. Resources
  
  - **Cpu:** Shared with Odoo Application Server
  - **Memory:** Shared with Odoo Application Server
  
  #### .5.10. Configuration
  
  - **Quota Rules:** Configured via PlatformConfigService
  - **Default Parameters:** Configured via PlatformConfigService
  
  #### .5.11. Health Check
  None

  #### .5.12. Responsible Features
  
  - REQ-AIGS-001
  - REQ-AIGS-002
  - REQ-AIGS-003
  - REQ-AIGS-004
  - REQ-AIGS-006
  - REQ-AIGS-007
  - REQ-AIGS-010
  - REQ-AIGS-011
  - REQ-DMG-007
  - REQ-DMG-008
  - REQ-DMG-023
  
  #### .5.13. Security
  
  - **Data Handling:** Manages prompts, generated images, and usage data.
  
  ### .6. PaymentService
  Manages influencer payment calculations, generation of payment requests, and integration with Odoo Accounting. Encapsulates logic within Odoo Models: `influence_gen.payment_record` and uses `influence_gen.bank_account`.

  #### .6.4. Type
  Odoo Business Logic Service/Module

  #### .6.5. Dependencies
  
  - ig-bl-002
  - ig-bl-001
  - ig-infra-007
  - ig-infra-005
  
  #### .6.6. Properties
  
  - **Main Models:**
    
    - influence_gen.payment_record
    
  
  #### .6.7. Interfaces
  
  
  #### .6.8. Technology
  Odoo 18 (Python, Odoo ORM)

  #### .6.9. Resources
  
  - **Cpu:** Shared with Odoo Application Server
  - **Memory:** Shared with Odoo Application Server
  
  #### .6.10. Configuration
  
  - **Payment Processing Rules:** Business logic and integration points with Odoo Accounting
  
  #### .6.11. Health Check
  None

  #### .6.12. Responsible Features
  
  - REQ-2-014
  - REQ-2-015
  - REQ-IPF-003
  - REQ-IPF-004
  - REQ-IPF-005
  - REQ-IPF-006
  - REQ-IPF-007
  - REQ-IPF-008
  - REQ-IPF-010
  - REQ-IPF-011
  - REQ-DMG-009
  
  #### .6.13. Security
  
  - **Data Handling:** Manages financial data related to influencer payments. Must adhere to strict security and encryption.
  
  ### .7. PlatformConfigService
  Manages platform-wide configurations, roles/permissions, ToS/Privacy Policy versions, and business rules parameters. Uses Odoo's `ir.config_parameter`, security models, and custom setting models (e.g., `influence_gen.terms_document`).

  #### .7.4. Type
  Odoo Business Logic Service/Module

  #### .7.5. Dependencies
  
  - ig-infra-005
  - ig-infra-004
  
  #### .7.6. Properties
  
  - **Main Models:**
    
    - ir.config_parameter
    - res.groups
    - ir.model.access
    - influence_gen.terms_document
    
  
  #### .7.7. Interfaces
  
  
  #### .7.8. Technology
  Odoo 18 (Python, Odoo ORM)

  #### .7.9. Resources
  
  - **Cpu:** Shared with Odoo Application Server
  - **Memory:** Shared with Odoo Application Server
  
  #### .7.10. Configuration
  
  
  #### .7.11. Health Check
  None

  #### .7.12. Responsible Features
  
  - REQ-PAC-001
  - REQ-PAC-002
  - REQ-PAC-003
  - REQ-PAC-004
  - REQ-PAC-005
  - REQ-PAC-006
  - REQ-PAC-007
  - REQ-PAC-008
  - REQ-PAC-009
  - REQ-PAC-010
  - REQ-PAC-011
  - REQ-PAC-012
  - REQ-PAC-013
  - REQ-PAC-015
  - REQ-PAC-017
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
  
  #### .7.13. Security
  
  - **Access Control:** Configuration capabilities restricted to Platform Administrators.
  
  ### .8. UserProfileService
  Manages general user profile aspects by leveraging Odoo's `res.users` and `res.partner` models, linking them to `influence_gen.influencer_profile`.

  #### .8.4. Type
  Odoo Business Logic Service/Module

  #### .8.5. Dependencies
  
  - ig-bl-001
  
  #### .8.6. Properties
  
  - **Main Models:**
    
    - res.users
    - res.partner
    
  
  #### .8.7. Interfaces
  
  
  #### .8.8. Technology
  Odoo 18 (Python, Odoo ORM)

  #### .8.9. Resources
  
  - **Cpu:** Shared with Odoo Application Server
  - **Memory:** Shared with Odoo Application Server
  
  #### .8.10. Configuration
  
  
  #### .8.11. Health Check
  None

  #### .8.12. Responsible Features
  
  - REQ-IPDPM-003
  
  #### .8.13. Security
  
  - **Data Handling:** Manages user account details.
  
  ### .9. AuditService
  Manages the viewing and querying of audit logs. Data is written by AuditTrailWriterService. This service focuses on retrieval and presentation logic for admins. Uses `influence_gen.audit_log` model.

  #### .9.4. Type
  Odoo Business Logic Service/Module

  #### .9.5. Dependencies
  
  - ig-infra-001
  
  #### .9.6. Properties
  
  - **Main Models:**
    
    - influence_gen.audit_log
    
  
  #### .9.7. Interfaces
  
  
  #### .9.8. Technology
  Odoo 18 (Python, Odoo ORM)

  #### .9.9. Resources
  
  - **Cpu:** Shared with Odoo Application Server
  - **Memory:** Shared with Odoo Application Server
  
  #### .9.10. Configuration
  
  
  #### .9.11. Health Check
  None

  #### .9.12. Responsible Features
  
  - REQ-ATEL-008
  - REQ-ATEL-011
  
  #### .9.13. Security
  
  - **Access Control:** Audit log access restricted to Platform Administrators.
  
  ### .10. OdooCoreServicesProxy
  Represents the use of Odoo's built-in services: ORM for database operations, cron for scheduled tasks, and base model functionalities.

  #### .10.4. Type
  Odoo Core Proxy

  #### .10.5. Dependencies
  
  
  #### .10.6. Properties
  
  
  #### .10.7. Interfaces
  
  
  #### .10.8. Technology
  Odoo 18 ORM, Odoo Cron

  #### .10.9. Resources
  
  
  #### .10.10. Configuration
  
  - **Database Connection:** Managed by Odoo server configuration
  - **Cron Worker Configuration:** Managed by Odoo server configuration
  
  #### .10.11. Health Check
  None

  #### .10.12. Responsible Features
  
  - Implicit in all data persistence REQs (REQ-DMG-001 to REQ-DMG-010)
  - REQ-DRH-002 (via cron)
  - REQ-ATEL-001 (Odoo module logging)
  
  #### .10.13. Security
  
  - **Data Access:** Mediated by Odoo ORM and record rules.
  
  ### .11. FileStorageAdapter
  Manages secure storage and retrieval of files (KYC documents, campaign content, AI images), abstracting Odoo filestore (`ir.attachment`) or a configured cloud storage solution.

  #### .11.4. Type
  Adapter

  #### .11.5. Dependencies
  
  
  #### .11.6. Properties
  
  - **Storage Type:** Odoo Filestore / Cloud Storage (configurable)
  
  #### .11.7. Interfaces
  
  
  #### .11.8. Technology
  Odoo 18 (`ir.attachment`), Python libraries (e.g., Boto3 for S3)

  #### .11.9. Resources
  
  - **Storage:** Dependent on volume of uploads
  
  #### .11.10. Configuration
  
  - **Max File Size:** Configurable (REQ-IOKYC-004, REQ-2-009)
  - **Allowed File Types:** Configurable (REQ-IOKYC-004, REQ-2-009)
  - **Cloud Storage Credentials:** Securely managed if cloud storage is used
  
  #### .11.11. Health Check
  None

  #### .11.12. Responsible Features
  
  - REQ-IOKYC-004
  - REQ-2-009
  - REQ-AIGS-006
  - REQ-AIGS-009
  
  #### .11.13. Security
  
  - **Encryption At Rest:** Ensured by underlying storage solution or Odoo.
  - **Access Control:** Permissions managed by Odoo for `ir.attachment` or bucket policies for cloud storage.
  
  ### .12. N8NWebhookGateway
  Handles outgoing webhook calls from Odoo to N8N for initiating asynchronous tasks (e.g., AI image generation) and provides a secure Odoo REST API callback endpoint for N8N to return results.

  #### .12.4. Type
  Gateway

  #### .12.5. Dependencies
  
  - ig-bl-003
  
  #### .12.6. Properties
  
  
  #### .12.7. Interfaces
  
  - **Name:** OdooToN8NWebhookInterface  
**Type:** Outbound HTTP POST  
**Operations:**
    
    - initiateAIImageGeneration
    
  - **Name:** N8NToOdooCallbackAPI  
**Type:** Inbound REST API (HTTP POST)  
**Operations:**
    
    - receiveAIImageResult
    
**Endpoint:** /influence_gen/n8n_callback/ai_image  
  
  #### .12.8. Technology
  Odoo 18 (Python HTTP Controllers, `requests` library)

  #### .12.9. Resources
  
  - **Network:** Handles HTTP traffic to/from N8N
  
  #### .12.10. Configuration
  
  - **N8N Webhook Url:** Configurable (REQ-PAC-017)
  - **Callback Api Auth Token:** Securely managed (REQ-IL-004, REQ-IL-008)
  
  #### .12.11. Health Check
  
  - **Path:** /influence_gen/n8n_callback/health
  - **Interval:** 60
  - **Timeout:** 5
  
  #### .12.12. Responsible Features
  
  - REQ-IL-002
  - REQ-IL-003
  - REQ-IL-010
  - REQ-IL-016
  - REQ-DDSI-009
  
  #### .12.13. Security
  
  - **Outbound:** Uses N8N webhook authentication.
  - **Inbound:** Callback endpoint secured with token authentication and rate limiting (REQ-PAC-013).
  
  ### .13. NotificationDispatchService
  Manages the dispatch of all system notifications, primarily email, using Odoo's mail system and templates.

  #### .13.4. Type
  Odoo Infrastructure Service

  #### .13.5. Dependencies
  
  - ig-bl-005
  
  #### .13.6. Properties
  
  
  #### .13.7. Interfaces
  
  
  #### .13.8. Technology
  Odoo 18 Mail (`mail.template`, `mail.mail`)

  #### .13.9. Resources
  
  
  #### .13.10. Configuration
  
  - **Smtp Server Settings:** Configured in Odoo (REQ-PAC-010)
  - **Email Templates:** Managed in Odoo (REQ-PAC-010)
  
  #### .13.11. Health Check
  None

  #### .13.12. Responsible Features
  
  - REQ-IOKYC-010
  - REQ-2-008
  - REQ-IPF-010
  - REQ-16-001
  - REQ-16-002
  - REQ-16-003
  - REQ-16-004
  - REQ-16-005
  - REQ-16-008
  - REQ-16-009
  - REQ-16-010
  - REQ-16-011
  - REQ-16-012
  - REQ-16-014
  - REQ-16-015
  - REQ-16-016
  - REQ-16-017
  
  #### .13.13. Security
  
  - **Email Security:** Depends on SMTP server configuration (TLS, SPF, DKIM).
  
  ### .14. AuditTrailWriterService
  Responsible for writing all audit log entries to the persistent store (Odoo's `influence_gen.audit_log` model).

  #### .14.4. Type
  Odoo Infrastructure Service

  #### .14.5. Dependencies
  
  - ig-infra-001
  
  #### .14.6. Properties
  
  
  #### .14.7. Interfaces
  
  
  #### .14.8. Technology
  Odoo 18 ORM

  #### .14.9. Resources
  
  
  #### .14.10. Configuration
  
  - **Audit Log Retention:** Configured via PlatformConfigService (REQ-DRH-006)
  
  #### .14.11. Health Check
  None

  #### .14.12. Responsible Features
  
  - REQ-IOKYC-016
  - REQ-2-018
  - REQ-AIGS-012
  - REQ-AIGS-015
  - REQ-IPF-009
  - REQ-ATEL-001
  - REQ-ATEL-002
  - REQ-ATEL-005
  - REQ-ATEL-006
  - REQ-ATEL-007
  - REQ-ATEL-009
  - REQ-ATEL-010
  - REQ-ATEL-011
  - REQ-12-001
  - REQ-12-006
  
  #### .14.13. Security
  
  - **Tamper Evidence:** Relies on database security and restricted write access to audit log table.
  
  ### .15. ThirdPartyVerificationGateway
  Manages integrations with external third-party services for KYC identity verification and bank account verification.

  #### .15.4. Type
  Gateway

  #### .15.5. Dependencies
  
  
  #### .15.6. Properties
  
  
  #### .15.7. Interfaces
  
  - **Name:** IdentityVerificationAPI  
**Type:** Outbound REST/SOAP API  
  - **Name:** BankAccountVerificationAPI  
**Type:** Outbound REST/SOAP API  
  
  #### .15.8. Technology
  Python (`requests` library or specific SDKs)

  #### .15.9. Resources
  
  - **Network:** Handles HTTP traffic to third-party services.
  
  #### .15.10. Configuration
  
  - **Api Keys:** Securely managed (REQ-PAC-017, REQ-IL-008)
  - **Service Endpoints:** Configurable
  
  #### .15.11. Health Check
  None

  #### .15.12. Responsible Features
  
  - REQ-IOKYC-005
  - REQ-IOKYC-008
  - REQ-IPF-002
  - REQ-IL-011
  
  #### .15.13. Security
  
  - **Data Transmission:** Must use HTTPS (TLS 1.2+).
  - **Credential Management:** API keys stored securely.
  
  ### .16. AccountingIntegrationGateway
  Manages integration with Odoo's internal Version 18 Accounting module for creating vendor bills or equivalent financial documents.

  #### .16.4. Type
  Odoo Internal Gateway/Adapter

  #### .16.5. Dependencies
  
  
  #### .16.6. Properties
  
  
  #### .16.7. Interfaces
  
  
  #### .16.8. Technology
  Odoo 18 (Python, calling methods of Odoo's `account` module)

  #### .16.9. Resources
  
  
  #### .16.10. Configuration
  
  - **Default Journal:** Configurable (REQ-PAC-015)
  - **Default Accounts:** Configurable (REQ-PAC-015)
  
  #### .16.11. Health Check
  None

  #### .16.12. Responsible Features
  
  - REQ-IPF-006
  - REQ-2-014
  
  #### .16.13. Security
  
  - **Access Control:** Leverages Odoo's internal access rights for accounting operations.
  
  ### .17. AIImageGenerationN8NWorkflow
  The N8N workflow that receives requests from Odoo, orchestrates calls to the AI model serving API (primarily Flux LoRA models), handles responses, and sends results back to Odoo's callback endpoint.

  #### .17.4. Type
  N8N Workflow

  #### .17.5. Dependencies
  
  - ig-infra-003
  - ig-n8n-002
  
  #### .17.6. Properties
  
  - **Workflow File Name:** influencegen_ai_image_v1.json
  
  #### .17.7. Interfaces
  
  - **Name:** OdooWebhookTrigger  
**Type:** Inbound Webhook Node  
  - **Name:** AICallbackToOdoo  
**Type:** Outbound HTTP Request Node (to Odoo callback)  
  
  #### .17.8. Technology
  N8N (Nodes: Webhook, HTTP Request, Function, Switch, Merge, Error Trigger)

  #### .17.9. Resources
  
  - **Cpu:** Dependent on N8N instance provisioning
  - **Memory:** Dependent on N8N instance provisioning
  - **Network:** Handles traffic to AI service and Odoo
  
  #### .17.10. Configuration
  
  - **Ai Service Api Url:** N8N Credential/Variable
  - **Ai Service Api Key:** N8N Credential
  - **Odoo Callback Url:** N8N Variable
  - **Odoo Callback Auth Token:** N8N Credential
  - **Retry Logic:** Configured in N8N nodes (REQ-IL-009)
  
  #### .17.11. Health Check
  
  - **Path:** N/A (N8N instance health is monitored separately)
  - **Interval:** 0
  - **Timeout:** 0
  
  #### .17.12. Responsible Features
  
  - REQ-AIGS-001
  - REQ-IL-001
  - REQ-IL-005
  - REQ-IL-006
  - REQ-IL-007
  - REQ-IL-009
  - REQ-IL-017
  - REQ-ATEL-010
  
  #### .17.13. Security
  
  - **Credential Management:** Uses N8N's built-in credential manager (REQ-IL-008).
  - **Data Handling:** Processes prompts and image data; must adhere to secure practices (REQ-IL-017).
  
  ### .18. AIModelServingAPIProxyNode
  A conceptual representation of the N8N HTTP Request node(s) specifically configured to communicate with the designated AI Model Serving Infrastructure API (e.g., ComfyUI, Automatic1111 API, cloud ML platform endpoint).

  #### .18.4. Type
  N8N Connector Node

  #### .18.5. Dependencies
  
  
  #### .18.6. Properties
  
  - **Target Aiservice:** Flux LoRA Models via REST API
  
  #### .18.7. Interfaces
  
  - **Name:** AIModelServingRestAPI  
**Type:** Outbound REST API  
  
  #### .18.8. Technology
  N8N HTTP Request Node

  #### .18.9. Resources
  
  
  #### .18.10. Configuration
  
  - **Api Endpoint:** Configured in N8N workflow/credential
  - **Authentication Method:** API Key / Token (configured in N8N)
  
  #### .18.11. Health Check
  None

  #### .18.12. Responsible Features
  
  - REQ-AIGS-001
  - REQ-AIGS-013
  - REQ-AIGS-016
  - REQ-IL-005
  
  #### .18.13. Security
  
  - **Communication:** Must use HTTPS to AI service.
  
  
- **Configuration:**
  
  - **Environment:** Production/Staging/Development
  - **Logging Level:** INFO (configurable per component/environment via REQ-PAC-011, REQ-ATEL-003)
  - **Global Settings:** Managed via ig-bl-005 (PlatformConfigService)
  


---

# 2. Component_Relations

- **Architecture:**
  
  - **Components:**
    
    - **Id:** influencegen-onboarding-kyc-module  
**Name:** InfluencerOnboardingKYCModule  
**Description:** Handles all aspects of influencer registration, profile management, Know Your Customer (KYC) processes, bank account detail submission, and consent management. It provides both public-facing interfaces for prospective influencers and administrative interfaces for KYC review.  
**Type:** OdooModule  
**Dependencies:**
    
    - odoo-core-framework
    - notification-module
    - audit-logging-module
    - file-storage-service
    - third-party-kyc-service-adapter
    - third-party-bank-verification-service-adapter
    - data-management-governance-module
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Odoo Compatibility:** 18.0
    
**Interfaces:**
    
    - PublicRegistrationAPI (Odoo Controllers/Views)
    - InfluencerProfileAPI (Odoo Controllers/Views)
    - AdminKYCManagementAPI (Odoo Controllers/Views)
    
**Technology:** Odoo 18 (Python, XML, OWL, JavaScript)  
**Resources:**
    
    - **Cpu:** Shared with Odoo application server
    - **Memory:** Shared with Odoo application server
    - **Storage:** Dependent on KYC document volume (via FileStorageService)
    
**Configuration:**
    
    - **Kyc Document Types:** Configurable list (e.g., Passport, Driver's License)
    - **File Upload Restrictions:** Configurable (format, max size)
    - **Social Media Verification Methods:** Configurable (e.g., OAuth, code placement)
    - **Bank Account Verification Methods:** Configurable (e.g., 3rd party, micro-deposit, manual)
    
**Health Check:**
    
    - **Path:** /influencegen/health/onboarding
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
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
    - REQ-IOKYC-011
    - REQ-IOKYC-012
    - REQ-IOKYC-013
    - REQ-IOKYC-014
    - REQ-IOKYC-016
    - REQ-IOKYC-017
    - REQ-IPF-001
    - REQ-IPF-002
    - REQ-IPDPM-003
    
**Security:**
    
    - **Requires Authentication:** Varies (public for registration, authenticated for profile/admin)
    - **Requires Authorization:** Varies (influencer role, admin role)
    - **Data Encryption:** PII, KYC docs, financial details (AES-256 at rest, TLS 1.2+ in transit)
    
    - **Id:** influencegen-campaign-management-module  
**Name:** CampaignManagementModule  
**Description:** Manages the entire lifecycle of influencer marketing campaigns, from creation and influencer application/selection to content submission, review, and performance tracking.  
**Type:** OdooModule  
**Dependencies:**
    
    - odoo-core-framework
    - influencegen-onboarding-kyc-module
    - notification-module
    - audit-logging-module
    - file-storage-service
    - payment-financials-module
    - data-management-governance-module
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Odoo Compatibility:** 18.0
    
**Interfaces:**
    
    - CampaignAdminAPI (Odoo Controllers/Views)
    - CampaignInfluencerAPI (Odoo Controllers/Views for discovery, application, submission)
    
**Technology:** Odoo 18 (Python, XML, OWL, JavaScript)  
**Resources:**
    
    - **Cpu:** Shared with Odoo application server
    - **Memory:** Shared with Odoo application server
    - **Storage:** Dependent on content submission volume (via FileStorageService)
    
**Configuration:**
    
    - **Compensation Models:** Configurable list (e.g., flat fee, per post, commission)
    - **Content Submission File Types:** Configurable (e.g., JPG, PNG, MP4)
    - **Kpi Metrics:** Definable per campaign
    
**Health Check:**
    
    - **Path:** /influencegen/health/campaign
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-2-001
    - REQ-2-002
    - REQ-2-003
    - REQ-2-004
    - REQ-2-005
    - REQ-2-006
    - REQ-2-007
    - REQ-2-008
    - REQ-2-009
    - REQ-2-010
    - REQ-2-011
    - REQ-2-012
    - REQ-2-013
    - REQ-2-014
    - REQ-2-015
    - REQ-2-016
    - REQ-2-017
    - REQ-2-018
    - REQ-IPDPM-004
    - REQ-IPDPM-005
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** Varies (influencer role, admin role)
    - **Data Encryption:** Campaign sensitive data (as per PII/Financials)
    
    - **Id:** influencegen-ai-integration-module-odoo  
**Name:** AIIntegrationModule_Odoo  
**Description:** Handles the Odoo-side responsibilities for AI image generation, including user interface, request initiation to N8N, callback handling from N8N, and storage of generated images and metadata.  
**Type:** OdooModule  
**Dependencies:**
    
    - odoo-core-framework
    - n8n-image-workflow-component
    - notification-module
    - audit-logging-module
    - file-storage-service
    - platform-administration-module
    - data-management-governance-module
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Odoo Compatibility:** 18.0
    
**Interfaces:**
    
    - AIImageGenerationUI (Odoo Views/OWL)
    - N8NWebhookCallerAPI (Python service)
    - N8NCallbackReceiverAPI (Odoo HTTP Controller)
    
**Technology:** Odoo 18 (Python, XML, OWL, JavaScript)  
**Resources:**
    
    - **Cpu:** Shared with Odoo application server
    - **Memory:** Shared with Odoo application server
    - **Storage:** Dependent on generated image volume (via FileStorageService)
    
**Configuration:**
    
    - **N8N Webhook Url:** Configurable
    - **Default Aigeneration Params:** Configurable
    - **Ai Model List:** Manageable by Admin
    
**Health Check:**
    
    - **Path:** /influencegen/health/ai_odoo
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-AIGS-001 (Odoo part)
    - REQ-AIGS-002
    - REQ-AIGS-003
    - REQ-AIGS-004
    - REQ-AIGS-005
    - REQ-AIGS-006
    - REQ-AIGS-007
    - REQ-AIGS-008 (Odoo part)
    - REQ-AIGS-010
    - REQ-AIGS-011
    - REQ-AIGS-015
    - REQ-IL-002
    - REQ-IL-003
    - REQ-IL-010
    - REQ-IL-016
    - REQ-IPDPM-006
    - REQ-UIUX-004
    - REQ-UIUX-005
    - REQ-UIUX-021
    - REQ-UIUX-022
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** Specific roles (e.g., authorized influencers, admins)
    - **Data Encryption:** Generated images if sensitive, related metadata
    
    - **Id:** n8n-image-workflow-component  
**Name:** AIImageGenerationWorkflow_N8N  
**Description:** N8N workflow responsible for orchestrating the AI image generation process by receiving requests from Odoo, interacting with the AI backend service, and returning results to Odoo.  
**Type:** N8NWorkflow  
**Dependencies:**
    
    - influencegen-ai-integration-module-odoo (via Webhook/Callback)
    - ai-backend-service
    
**Properties:**
    
    - **Version:** 1.0.0
    - **N8N Compatibility:** Latest Stable
    
**Interfaces:**
    
    - OdooRequestWebhook (N8N Webhook Node)
    - AIServiceAPIClient (N8N HTTP Request Node)
    - OdooCallbackAPIClient (N8N HTTP Request Node)
    
**Technology:** N8N  
**Resources:**
    
    - **Cpu:** Dependent on N8N instance provisioning
    - **Memory:** Dependent on N8N instance provisioning
    - **Network:** Required for Odoo & AI service communication
    
**Configuration:**
    
    - **Ai Service Api Endpoint:** Configurable in N8N credentials/workflow
    - **Ai Service Api Key:** Managed by N8N credentials
    - **Odoo Callback Url:** Configurable in workflow
    
**Health Check:**
    
    - **Path:** N/A (Monitored via N8N execution logs and Odoo callback success)
    - **Interval:** 0
    - **Timeout:** 0
    
**Responsible Features:**
    
    - REQ-AIGS-001 (N8N part)
    - REQ-AIGS-008 (N8N part)
    - REQ-IL-001
    - REQ-IL-005
    - REQ-IL-006
    - REQ-IL-007 (N8N parts)
    - REQ-IL-009
    - REQ-ATEL-010
    
**Security:**
    
    - **Requires Authentication:** Webhook security (e.g., secret token)
    - **Data Protection:** Handles prompts and image data in transit; secure credential management in N8N
    
    - **Id:** influencegen-payment-financials-module  
**Name:** PaymentFinancialsModule  
**Description:** Manages influencer payment calculations, generation of payment requests/batches, and integration with Odoo's accounting module for payment execution and status tracking.  
**Type:** OdooModule  
**Dependencies:**
    
    - odoo-core-framework
    - odoo-accounting-module
    - influencegen-onboarding-kyc-module
    - influencegen-campaign-management-module
    - notification-module
    - audit-logging-module
    - data-management-governance-module
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Odoo Compatibility:** 18.0
    
**Interfaces:**
    
    - PaymentAdminAPI (Odoo Controllers/Views)
    - AccountingIntegrationService (Python service)
    
**Technology:** Odoo 18 (Python, XML)  
**Resources:**
    
    - **Cpu:** Shared with Odoo application server
    - **Memory:** Shared with Odoo application server
    
**Configuration:**
    
    - **Default Payment Journal:** Configurable (Odoo accounting setting)
    - **Payment Failure Alert Recipients:** Configurable email list
    
**Health Check:**
    
    - **Path:** /influencegen/health/payment
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-IPF-003
    - REQ-IPF-004
    - REQ-IPF-005
    - REQ-IPF-006
    - REQ-IPF-007
    - REQ-IPF-008
    - REQ-IPF-009
    - REQ-IPF-010
    - REQ-IPF-011
    - REQ-IPF-012
    - REQ-2-013 (calculation part)
    - REQ-2-014 (generation part)
    - REQ-2-015 (status reflection)
    - REQ-IPDPM-007
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** Admin role for management, Influencer role for viewing own payment info
    - **Data Encryption:** Financial details (AES-256 at rest, TLS 1.2+ in transit)
    
    - **Id:** influencegen-platform-administration-module  
**Name:** PlatformAdministrationModule  
**Description:** Provides centralized administrative interfaces for managing users, roles, permissions, system configurations (AI, KYC, email, etc.), platform-wide policies, and accessing operational oversight tools.  
**Type:** OdooModule  
**Dependencies:**
    
    - odoo-core-framework
    - audit-logging-module
    - notification-module
    - data-management-governance-module
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Odoo Compatibility:** 18.0
    
**Interfaces:**
    
    - AdminConfigurationUI (Odoo Views)
    - UserManagementUI (Odoo Views)
    - SystemMonitoringAccessUI (Odoo Views linking to logs/dashboards)
    
**Technology:** Odoo 18 (Python, XML)  
**Resources:**
    
    - **Cpu:** Shared with Odoo application server
    - **Memory:** Shared with Odoo application server
    
**Configuration:**
    
    - **Log Levels Per Component:** Configurable
    - **Alert Rules:** Configurable
    
**Health Check:**
    
    - **Path:** /influencegen/health/admin
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-PAC-001
    - REQ-PAC-002
    - REQ-PAC-003
    - REQ-PAC-004
    - REQ-PAC-005
    - REQ-PAC-006
    - REQ-PAC-007
    - REQ-PAC-008
    - REQ-PAC-009
    - REQ-PAC-010
    - REQ-PAC-011
    - REQ-PAC-012
    - REQ-PAC-013
    - REQ-PAC-014
    - REQ-PAC-015
    - REQ-PAC-016
    - REQ-PAC-017
    - REQ-UIUX-015
    - REQ-UIUX-016
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** Platform Administrator role
    - **Secure Credential Management:** For API keys, etc.
    
    - **Id:** influencegen-influencer-portal-module  
**Name:** InfluencerPortalModule  
**Description:** Provides the dedicated user interface for activated influencers, including dashboards, profile management, campaign interaction, AI tool access, and payment information viewing. Ensures adherence to UI/UX and accessibility standards.  
**Type:** OdooModule  
**Dependencies:**
    
    - odoo-core-framework
    - influencegen-onboarding-kyc-module
    - influencegen-campaign-management-module
    - influencegen-ai-integration-module-odoo
    - influencegen-payment-financials-module
    - notification-module
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Odoo Compatibility:** 18.0
    
**Interfaces:**
    
    - InfluencerDashboardUI (Odoo Views/OWL)
    - ProfileManagementUI (Odoo Views/OWL)
    - CampaignDiscoveryUI (Odoo Views/OWL)
    - ContentSubmissionUI (Odoo Views/OWL)
    
**Technology:** Odoo 18 (Python Controllers, XML, QWeb, OWL, JavaScript)  
**Resources:**
    
    - **Cpu:** Shared with Odoo application server
    - **Memory:** Shared with Odoo application server
    
**Configuration:**
    
    
**Health Check:**
    
    - **Path:** /influencegen/health/portal
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-IPDPM-001
    - REQ-IPDPM-002
    - REQ-IPDPM-003
    - REQ-IPDPM-004
    - REQ-IPDPM-005
    - REQ-IPDPM-006
    - REQ-IPDPM-007
    - REQ-IPDPM-008
    - REQ-IPDPM-009
    - REQ-IPDPM-010
    - REQ-IPDPM-011
    - REQ-UIUX-001
    - REQ-UIUX-002
    - REQ-UIUX-007
    - REQ-UIUX-008
    - REQ-UIUX-010
    - REQ-UIUX-017
    - REQ-UIUX-018
    - REQ-UIUX-019
    - REQ-UIUX-020
    - REQ-14-001
    - REQ-14-002
    - REQ-14-003
    - REQ-14-004
    - REQ-14-005
    - REQ-14-006
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** Influencer role
    
    - **Id:** influencegen-audit-logging-module  
**Name:** AuditLoggingModule  
**Description:** Manages the creation, storage, and retrieval of comprehensive audit trail records for significant system events and user actions. Integrates with a centralized logging solution.  
**Type:** OdooModule  
**Dependencies:**
    
    - odoo-core-framework
    - centralized-logging-solution-adapter
    - data-management-governance-module
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Odoo Compatibility:** 18.0
    
**Interfaces:**
    
    - AuditLogWriterService (Python service)
    - AuditLogViewerUI (Odoo Views for Admin)
    
**Technology:** Odoo 18 (Python, XML)  
**Resources:**
    
    - **Cpu:** Shared with Odoo application server
    - **Memory:** Shared with Odoo application server
    - **Storage:** Dependent on audit log volume (managed by Odoo DB or centralized solution)
    
**Configuration:**
    
    - **Audit Log Retention Period:** Configurable (via DataManagementGovernanceModule)
    - **Tamper Evidence Mechanism:** Database constraints, secure storage
    
**Health Check:**
    
    - **Path:** /influencegen/health/audit
    - **Interval:** 120
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-ATEL-001
    - REQ-ATEL-002
    - REQ-ATEL-003
    - REQ-ATEL-004
    - REQ-ATEL-005
    - REQ-ATEL-006
    - REQ-ATEL-007
    - REQ-ATEL-008
    - REQ-ATEL-009
    - REQ-ATEL-011
    - REQ-IOKYC-016
    - REQ-2-018
    - REQ-AIGS-015
    - REQ-IPF-009
    - REQ-AIGS-012
    
**Security:**
    
    - **Requires Authentication:** For viewing (Admin role)
    - **Log Integrity:** Protection against unauthorized modification/deletion
    
    - **Id:** influencegen-notification-module  
**Name:** NotificationModule  
**Description:** Handles all system-generated notifications, including emails to influencers and administrators, UI feedback messages, and system alerts for operational issues.  
**Type:** OdooModule  
**Dependencies:**
    
    - odoo-core-framework
    - platform-administration-module
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Odoo Compatibility:** 18.0
    
**Interfaces:**
    
    - EmailNotificationService (Python service using Odoo Mail)
    - UINotificationService (OWL/JavaScript utilities)
    - SystemAlertTriggerService (Python service)
    
**Technology:** Odoo 18 (Python, XML, Odoo Mail Templates, OWL)  
**Resources:**
    
    - **Cpu:** Shared with Odoo application server
    - **Memory:** Shared with Odoo application server
    
**Configuration:**
    
    - **Email Templates:** Manageable by Admin (via PlatformAdministrationModule)
    - **Smtp Server Settings:** Manageable by Admin (via PlatformAdministrationModule)
    - **Alert Notification Channels:** Configurable (e.g., email, Slack integration)
    
**Health Check:**
    
    - **Path:** /influencegen/health/notification
    - **Interval:** 60
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-16-001
    - REQ-16-002
    - REQ-16-003
    - REQ-16-004
    - REQ-16-005
    - REQ-16-006
    - REQ-16-007
    - REQ-16-008
    - REQ-16-009
    - REQ-16-010
    - REQ-16-011
    - REQ-16-012
    - REQ-16-013
    - REQ-16-014
    - REQ-16-015
    - REQ-16-016
    - REQ-16-017
    - REQ-IOKYC-010
    - REQ-2-008
    - REQ-IPF-010
    
**Security:**
    
    - **Requires Authentication:** For triggering certain admin notifications
    
    - **Id:** influencegen-data-management-governance-module  
**Name:** DataManagementGovernanceModule  
**Description:** Oversees data modeling standards, validation rules, data quality processes, and the implementation of data retention, archival, and legal hold policies across the InfluenceGen platform.  
**Type:** OdooModule  
**Dependencies:**
    
    - odoo-core-framework
    - platform-administration-module
    - audit-logging-module
    
**Properties:**
    
    - **Version:** 1.0.0
    - **Odoo Compatibility:** 18.0
    
**Interfaces:**
    
    - DataRetentionPolicyAdminUI (Odoo Views)
    - LegalHoldAdminUI (Odoo Views)
    - DataValidationRuleEngine (Python logic within Odoo Models)
    - DataAnonymizationTooling (Scripts/Odoo Actions for non-prod data)
    
**Technology:** Odoo 18 (Python, XML, Odoo Scheduled Actions)  
**Resources:**
    
    - **Cpu:** Shared with Odoo application server (higher during retention jobs)
    - **Memory:** Shared with Odoo application server
    
**Configuration:**
    
    - **Data Retention Periods By Category:** Configurable by Admin
    - **Archival Storage Path:** Configurable
    - **Gdpr Compliance Settings:** Based on Odoo's capabilities & custom logic
    
**Health Check:**
    
    - **Path:** /influencegen/health/datagov
    - **Interval:** 120
    - **Timeout:** 10
    
**Responsible Features:**
    
    - REQ-DMG-001
    - REQ-DMG-002
    - REQ-DMG-003
    - REQ-DMG-004
    - REQ-DMG-005
    - REQ-DMG-006
    - REQ-DMG-007
    - REQ-DMG-008
    - REQ-DMG-009
    - REQ-DMG-010
    - REQ-DMG-013
    - REQ-DMG-014
    - REQ-DMG-015
    - REQ-DMG-016
    - REQ-DMG-017
    - REQ-DMG-019
    - REQ-DMG-020
    - REQ-DMG-021
    - REQ-DMG-022
    - REQ-DMG-023
    - REQ-DMG-024
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
    
**Security:**
    
    - **Requires Authentication:** True
    - **Requires Authorization:** Platform Administrator role
    - **Data Protection:** Ensures policies for PII and sensitive data are enforced.
    
    
  - **Configuration:**
    
    - **Environment:** Production
    - **Logging Level:** INFO (configurable per component via PlatformAdminModule)
    - **Database Url:** Odoo Default (PostgreSQL)
    - **Cache Ttl:** Varies (Odoo default, custom caching where applicable)
    - **Max Threads:** Odoo Worker Configuration
    
  


---

