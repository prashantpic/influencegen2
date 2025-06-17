# Specification

# 1. Data Transformation Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-13
  - **Technology Stack:**
    
    - Odoo 18 (Python, ORM, OWL, XML)
    - N8N
    - PostgreSQL
    - AI Service (Flux LoRA models via REST API)
    
  - **Service Interfaces:**
    
    - Odoo Internal Services
    - Odoo to N8N Webhook
    - N8N to AI Service REST API
    - N8N to Odoo Callback REST API
    - Odoo to 3rd Party KYC/Payment (Optional)
    
  - **Data Models:**
    
    - InfluencerProfile
    - KYCData
    - SocialMediaProfile
    - BankAccount
    - Campaign
    - CampaignApplication
    - ContentSubmission
    - AIImageModel
    - AIImageGenerationRequest
    - GeneratedImage
    - PaymentRecord
    - TermsConsent
    - AuditLog
    
  
- **Data Mapping Strategy:**
  
  - **Essential Mappings:**
    
    - **Mapping Id:** M001  
**Source:** Odoo AI Image Generation UI/Controller  
**Target:** N8N AIImageGenerationRequested Webhook Payload (EVT-AIG-001)  
**Transformation:** direct  
**Configuration:**
    
    - **Field Mappings:**
      
      - **Source:** userId  
**Target:** userId  
      - **Source:** prompt  
**Target:** prompt  
      - **Source:** negativePrompt  
**Target:** negativePrompt  
      - **Source:** modelId (from AIImageModel selection)  
**Target:** modelId  
      - **Source:** resolution  
**Target:** resolution  
      - **Source:** aspectRatio  
**Target:** aspectRatio  
      - **Source:** seed  
**Target:** seed  
      - **Source:** inferenceSteps  
**Target:** inferenceSteps  
      - **Source:** cfgScale  
**Target:** cfgScale  
      - **Source:** campaignId (optional)  
**Target:** campaignId  
      - **Source:** Generated AIImageGenerationRequest.id  
**Target:** requestId  
      - **Source:** Generated Correlation ID  
**Target:** correlationId  
      - **Source:** Constructed Odoo Callback URL  
**Target:** callbackUrl  
      
    
**Mapping Technique:** Object-to-Object field mapping  
**Justification:** REQ-AIGS-001, REQ-IL-002: Odoo must send necessary parameters to N8N.  
**Complexity:** medium  
    - **Mapping Id:** M002  
**Source:** N8N (from AI Service Success Response)  
**Target:** Odoo AIImageGenerationCompleted Callback Payload (EVT-AIG-002)  
**Transformation:** direct  
**Configuration:**
    
    - **Field Mappings:**
      
      - **Source:** Original requestId from EVT-AIG-001  
**Target:** requestId  
      - **Source:** Original correlationId from EVT-AIG-001  
**Target:** correlationId  
      - **Source:** AI Service image_data/image_url  
**Target:** imageData / imageUrl  
      - **Source:** AI Service image_metadata (format, size, width, height)  
**Target:** imageMetadata  
      - **Source:** Calculated image hash  
**Target:** hashValue  
      
    - **Status Field:** completed
    
**Mapping Technique:** Object-to-Object field mapping  
**Justification:** REQ-AIGS-001, REQ-IL-003: N8N must return successful image generation results to Odoo.  
**Complexity:** medium  
    - **Mapping Id:** M003  
**Source:** N8N (from AI Service Error Response or N8N Workflow Error)  
**Target:** Odoo AIImageGenerationFailed Callback Payload (EVT-AIG-003)  
**Transformation:** direct  
**Configuration:**
    
    - **Field Mappings:**
      
      - **Source:** Original requestId from EVT-AIG-001  
**Target:** requestId  
      - **Source:** Original correlationId from EVT-AIG-001  
**Target:** correlationId  
      - **Source:** AI Service error_code / N8N error_code  
**Target:** errorCode  
      - **Source:** AI Service error_message / N8N error_message  
**Target:** errorMessage  
      
    - **Status Field:** failed
    
**Mapping Technique:** Object-to-Object field mapping  
**Justification:** REQ-AIGS-001, REQ-IL-003: N8N must return failure information to Odoo.  
**Complexity:** simple  
    - **Mapping Id:** M004  
**Source:** Odoo Registration Form (UI)  
**Target:** Odoo InfluencerProfile Model (DB Design)  
**Transformation:** direct  
**Configuration:**
    
    
**Mapping Technique:** Form-to-Model field mapping (Odoo standard)  
**Justification:** REQ-IOKYC-002: Influencer submits personal, contact, professional info.  
**Complexity:** simple  
    - **Mapping Id:** M005  
**Source:** Odoo KYC Document Upload (UI)  
**Target:** Odoo KYCData Model (DB Design) and File Store  
**Transformation:** direct  
**Configuration:**
    
    - **File Storage Mechanism:** Odoo `ir.attachment` or cloud storage
    
**Mapping Technique:** Form-to-Model and File Upload Handling  
**Justification:** REQ-IOKYC-004: Secure upload of ID documents.  
**Complexity:** medium  
    
  - **Object To Object Mappings:**
    
    - **Source Object:** Odoo AI Image Generation Request Data (internal)  
**Target Object:** N8N Webhook Payload (EVT-AIG-001)  
**Field Mappings:**
    
    - **Source Field:** prompt_text  
**Target Field:** prompt  
**Transformation:** direct  
**Data Type Conversion:** string_to_string  
    - **Source Field:** selected_model.id  
**Target Field:** modelId  
**Transformation:** direct  
**Data Type Conversion:** uuid_to_string  
    
    - **Source Object:** AI Service API Response (Success)  
**Target Object:** N8N Odoo Callback Payload (EVT-AIG-002)  
**Field Mappings:**
    
    - **Source Field:** ai_service.image.url  
**Target Field:** imageUrl  
**Transformation:** direct  
**Data Type Conversion:** url_to_string  
    - **Source Field:** ai_service.image.metadata.format  
**Target Field:** imageMetadata.format  
**Transformation:** direct  
**Data Type Conversion:** string_to_string  
    
    
  - **Data Type Conversions:**
    
    - **From:** Odoo DateTime (Python datetime)  
**To:** JSON ISO8601 string (for N8N/API)  
**Conversion Method:** Standard library serialization  
**Validation Required:** False  
    - **From:** Odoo Integer/Float  
**To:** JSON Number  
**Conversion Method:** Standard library serialization  
**Validation Required:** False  
    - **From:** JSON Number  
**To:** Odoo Integer/Float  
**Conversion Method:** Standard library deserialization  
**Validation Required:** True  
    
  - **Bidirectional Mappings:**
    
    
  
- **Schema Validation Requirements:**
  
  - **Field Level Validations:**
    
    - **Field:** InfluencerProfile.email  
**Rules:**
    
    - required
    - unique
    - valid_email_format
    
**Priority:** critical  
**Error Message:** A unique and valid email address is required.  
    - **Field:** SocialMediaProfile.handle (per platform)  
**Rules:**
    
    - required
    - unique_per_platform_influencer
    
**Priority:** critical  
**Error Message:** Social media handle must be unique for the selected platform.  
    - **Field:** SocialMediaProfile.platform_url  
**Rules:**
    
    - valid_url_format (specific to platform if REQ-IOKYC-003 implemented)
    
**Priority:** high  
**Error Message:** Invalid social media profile link format.  
    - **Field:** KYCData.document (file upload)  
**Rules:**
    
    - required_file
    - allowed_file_types (JPG, PNG, PDF)
    - max_file_size
    
**Priority:** critical  
**Error Message:** Invalid file type or size for ID document.  
    - **Field:** AIImageGenerationRequest.prompt  
**Rules:**
    
    - required
    - max_length
    - content_moderation_check
    
**Priority:** high  
**Error Message:** Prompt is required, too long, or contains restricted content.  
    - **Field:** AIImageGenerationRequest.inferenceSteps  
**Rules:**
    
    - integer_range (admin_configurable)
    
**Priority:** medium  
**Error Message:** Inference steps must be within the allowed range.  
    - **Field:** Campaign.name  
**Rules:**
    
    - required
    - unique
    
**Priority:** critical  
**Error Message:** Campaign name is required and must be unique.  
    
  - **Cross Field Validations:**
    
    - **Validation Id:** CV001  
**Fields:**
    
    - Campaign.startDate
    - Campaign.endDate
    
**Rule:** endDate >= startDate  
**Condition:** Both dates are provided  
**Error Handling:** Prevent save, display error message.  
    
  - **Business Rule Validations:**
    
    - **Rule Id:** BR001  
**Description:** Uniqueness of email address across all influencer profiles.  
**Fields:**
    
    - InfluencerProfile.email
    
**Logic:** Database uniqueness constraint, checked on save.  
**Priority:** critical  
    - **Rule Id:** BR002  
**Description:** Uniqueness of social media handle per platform per influencer.  
**Fields:**
    
    - SocialMediaProfile.platform
    - SocialMediaProfile.handle
    - SocialMediaProfile.influencerProfileId
    
**Logic:** Database uniqueness constraint (platform, handle), application logic for influencer scope.  
**Priority:** critical  
    - **Rule Id:** BR003  
**Description:** Enforce AI image generation quotas per user/role.  
**Fields:**
    
    - AIImageGenerationRequest.userId
    - AIImageModel (cost factor if any)
    
**Logic:** Check usage against AIUsageTrackingLog before allowing request.  
**Priority:** high  
    
  - **Conditional Validations:**
    
    
  - **Validation Groups:**
    
    - **Group Name:** InfluencerOnboarding  
**Validations:**
    
    - InfluencerProfile.email rules
    - SocialMediaProfile.handle rules
    - SocialMediaProfile.platform_url rules
    
**Execution Order:** 1  
**Stop On First Failure:** True  
    - **Group Name:** KYCDocUpload  
**Validations:**
    
    - KYCData.document rules
    
**Execution Order:** 2  
**Stop On First Failure:** True  
    
  
- **Transformation Pattern Evaluation:**
  
  - **Selected Patterns:**
    
    - **Pattern:** adapter  
**Use Case:** N8N workflow adapting Odoo AI generation request to specific AI service API format.  
**Implementation:** N8N HTTP Request node configured with dynamic parameters based on input from Odoo.  
**Justification:** REQ-IL-005, REQ-IL-006: N8N integrates with AI service APIs, design should be adaptable.  
    - **Pattern:** pipeline  
**Use Case:** N8N AI image generation workflow (Webhook In -> Parameter Mapping -> AI Service Call -> Response Processing -> Odoo Callback).  
**Implementation:** Sequence of N8N nodes.  
**Justification:** REQ-AIGS-001 implies a multi-step asynchronous process.  
    
  - **Pipeline Processing:**
    
    - **Required:** True
    - **Stages:**
      
      - **Stage:** Odoo_Request_Preparation  
**Transformation:** Mapping UI input to AIImageGenerationRequest model  
**Dependencies:**
    
    
      - **Stage:** Odoo_To_N8N_Webhook  
**Transformation:** Mapping AIImageGenerationRequest model to EVT-AIG-001 payload  
**Dependencies:**
    
    - Odoo_Request_Preparation
    
      - **Stage:** N8N_Webhook_Ingestion  
**Transformation:** N8N receives and parses EVT-AIG-001  
**Dependencies:**
    
    - Odoo_To_N8N_Webhook
    
      - **Stage:** N8N_AI_Service_Call_Prep  
**Transformation:** Mapping EVT-AIG-001 payload to AI Service API request format  
**Dependencies:**
    
    - N8N_Webhook_Ingestion
    
      - **Stage:** N8N_AI_Service_Interaction  
**Transformation:** N8N calls AI Service API and receives response  
**Dependencies:**
    
    - N8N_AI_Service_Call_Prep
    
      - **Stage:** N8N_Odoo_Callback_Prep  
**Transformation:** Mapping AI Service API response to EVT-AIG-002/003 payload  
**Dependencies:**
    
    - N8N_AI_Service_Interaction
    
      - **Stage:** N8N_To_Odoo_Callback  
**Transformation:** N8N sends EVT-AIG-002/003 to Odoo callback API  
**Dependencies:**
    
    - N8N_Odoo_Callback_Prep
    
      - **Stage:** Odoo_Callback_Processing  
**Transformation:** Odoo processes callback, updates AIImageGenerationRequest, creates GeneratedImage  
**Dependencies:**
    
    - N8N_To_Odoo_Callback
    
      
    - **Parallelization:** False
    
  - **Processing Mode:**
    
    - **Real Time:**
      
      - **Required:** True
      - **Scenarios:**
        
        - AI Image Generation Request/Response flow (asynchronous real-time)
        - Odoo UI form submissions and validations
        
      - **Latency Requirements:** AI Gen: 10-20s (REQ-AIGS-008); UI interactions: <2s (REQ-UIUX-007)
      
    - **Batch:**
      
      - **Required:** False
      - **Batch Size:** 0
      - **Frequency:** 
      
    - **Streaming:**
      
      - **Required:** False
      - **Streaming Framework:** 
      - **Windowing Strategy:** 
      
    
  - **Canonical Data Model:**
    
    - **Applicable:** True
    - **Scope:**
      
      - Odoo-N8N AI Image Generation Interface (EVT-AIG-001, EVT-AIG-002, EVT-AIG-003 payloads)
      
    - **Benefits:**
      
      - Clear contract between Odoo and N8N for AI generation requests and responses.
      
    
  
- **Version Handling Strategy:**
  
  - **Schema Evolution:**
    
    - **Strategy:** Additive changes for JSON payloads. New API versions for Odoo callback endpoint for breaking changes.
    - **Versioning Scheme:** Semantic versioning for Odoo callback API (e.g., /v1/, /v2/).
    - **Compatibility:**
      
      - **Backward:** True
      - **Forward:** False
      - **Reasoning:** Odoo callback API should handle older N8N payload versions if possible. N8N workflows likely need updates for new Odoo callback API versions/payloads.
      
    
  - **Transformation Versioning:**
    
    - **Mechanism:** N8N workflow versioning. Odoo module versioning.
    - **Version Identification:** N8N workflow names/tags. Odoo module manifest versions.
    - **Migration Strategy:** Update N8N workflows and Odoo modules as needed, coordinated deployment.
    
  - **Data Model Changes:**
    
    - **Migration Path:** Odoo migration scripts (`migrations/` directory in modules) for database schema changes.
    - **Rollback Strategy:** Database backup/restore. Revert Odoo module code.
    - **Validation Strategy:** Testing in staging environment after migration.
    
  - **Schema Registry:**
    
    - **Required:** False
    - **Technology:** N/A (OpenAPI for Odoo callback REQ-DDSI-009, N8N workflow defines its input/output expectations)
    - **Governance:** N/A
    
  
- **Performance Optimization:**
  
  - **Critical Requirements:**
    
    - **Operation:** AI Image Generation End-to-End (Odoo request to Odoo result display)  
**Max Latency:** Average 10-20 seconds, P95 < 30s  
**Throughput Target:** 50-100 registrations/hour (REQ-IOKYC-015), 5000-10000 AI image requests/day (REQ-AIGS-009)  
**Justification:** REQ-AIGS-008, REQ-AIGS-009, REQ-IOKYC-015. User experience and system capacity.  
    - **Operation:** Odoo UI Page Load & Interactions  
**Max Latency:** Page load <3s, interactions <2s  
**Throughput Target:** N/A (concurrent user dependent)  
**Justification:** REQ-UIUX-007. User experience.  
    
  - **Parallelization Opportunities:**
    
    - **Transformation:** N8N AI Image Generation Workflow Instances  
**Parallelization Strategy:** N8N typically handles multiple webhook calls concurrently, up to its configured limits.  
**Expected Gain:** Increased throughput for AI image generation.  
    
  - **Caching Strategies:**
    
    - **Cache Type:** In-memory (Odoo ORM cache)  
**Cache Scope:** Frequently read, rarely changed Odoo records (e.g., AIImageModel list, active Campaign list for discovery).  
**Eviction Policy:** LRU / TTL (Odoo default)  
**Applicable Transformations:**
    
    - Data retrieval for campaign discovery UI
    - Data retrieval for AI model selection UI
    
    
  - **Memory Optimization:**
    
    - **Techniques:**
      
      - Efficient N8N workflow design (avoid loading large datasets into memory unless necessary)
      - Odoo ORM query optimization (avoid fetching unnecessary fields/records)
      
    - **Thresholds:** Monitor Odoo worker memory, N8N process memory.
    - **Monitoring Required:** True
    
  - **Lazy Evaluation:**
    
    - **Applicable:** False
    - **Scenarios:**
      
      
    - **Implementation:** 
    
  - **Bulk Processing:**
    
    - **Required:** False
    - **Batch Sizes:**
      
      - **Optimal:** 0
      - **Maximum:** 0
      
    - **Parallelism:** 0
    
  
- **Error Handling And Recovery:**
  
  - **Error Handling Strategies:**
    
    - **Error Type:** N8N Webhook Call Failure (Odoo -> N8N)  
**Strategy:** Retry with backoff, log persistent failure, alert admin.  
**Fallback Action:** User notified of submission failure in Odoo UI.  
**Escalation Path:**
    
    - Operations Team L1
    - Development Team L2
    
    - **Error Type:** Odoo Callback API Call Failure (N8N -> Odoo)  
**Strategy:** N8N retries with backoff, routes to N8N error workflow/DLQ on persistent failure, N8N alerts admin.  
**Fallback Action:** Odoo AI request status remains pending or eventually times out.  
**Escalation Path:**
    
    - N8N Admin/Dev Team L1
    - Operations Team L2
    
    - **Error Type:** AI Service API Error (within N8N)  
**Strategy:** N8N retries transient errors, captures error details, calls Odoo callback with failure status (EVT-AIG-003).  
**Fallback Action:** Odoo AI request status updated to 'failed', user notified.  
**Escalation Path:**
    
    - User notified via UI
    - Operations may investigate AI service health
    
    - **Error Type:** Odoo Data Validation Failure (e.g., on registration, campaign creation)  
**Strategy:** Prevent save, display user-friendly error message in UI.  
**Fallback Action:** User corrects input.  
**Escalation Path:**
    
    
    
  - **Logging Requirements:**
    
    - **Log Level:** INFO (Production default), DEBUG (for troubleshooting, configurable per REQ-ATEL-003)
    - **Included Data:**
      
      - Timestamp (UTC)
      - CorrelationID
      - RequestID
      - UserID
      - SourceComponent
      - TargetComponent
      - Action
      - Status
      - ErrorMessage (if error)
      
    - **Retention Period:** Operational logs: e.g., 30-90 days; Audit logs: 1-7 years (as per REQ-ATEL-007 and SRS 7.3)
    - **Alerting:** True
    
  - **Partial Success Handling:**
    
    - **Strategy:** N/A for current scope. AI image generation is typically all-or-nothing for a single request.
    - **Reporting Mechanism:** 
    - **Recovery Actions:**
      
      
    
  - **Circuit Breaking:**
    
    - **Dependency:** AI Image Generation Service (called by N8N)  
**Threshold:** e.g., >50% error rate over 2 minutes  
**Timeout:** e.g., 30 seconds per call  
**Fallback Strategy:** N8N workflow reports failure to Odoo (EVT-AIG-003).  
    
  - **Retry Strategies:**
    
    - **Operation:** Odoo call to N8N AI Gen Webhook  
**Max Retries:** 3  
**Backoff Strategy:** exponential  
**Retry Conditions:**
    
    - network_error
    - http_5xx_error
    
    - **Operation:** N8N call to Odoo Callback API  
**Max Retries:** 3  
**Backoff Strategy:** exponential  
**Retry Conditions:**
    
    - network_error
    - http_5xx_error
    
    - **Operation:** N8N call to AI Service API  
**Max Retries:** 2  
**Backoff Strategy:** fixed  
**Retry Conditions:**
    
    - ai_service_transient_error
    - http_5xx_error (from AI service)
    
    
  - **Error Notifications:**
    
    - **Condition:** Persistent N8N Webhook Call Failure  
**Recipients:**
    
    - Platform Administrators
    - Operations Team
    
**Severity:** critical  
**Channel:** Email, Monitoring Dashboard  
    - **Condition:** Persistent Odoo Callback API Call Failure (from N8N DLQ/Error Workflow)  
**Recipients:**
    
    - Platform Administrators
    - Operations Team
    
**Severity:** critical  
**Channel:** Email, Monitoring Dashboard  
    - **Condition:** High AI Image Generation Failure Rate (from AI Service)  
**Recipients:**
    
    - Platform Administrators
    - Operations Team
    
**Severity:** warning  
**Channel:** Email, Monitoring Dashboard  
    
  
- **Project Specific Transformations:**
  
  ### .1. Odoo AI Image Generation Request to N8N Webhook Payload
  Transforms data from Odoo's AIImageGenerationRequest model and UI inputs into the JSON payload expected by the N8N AI Image Generation Webhook.

  #### .1.1. Transformation Id
  PST-001

  #### .1.4. Source
  
  - **Service:** InfluenceGen Odoo UI Layer / Business Logic Layer
  - **Model:** AIImageGenerationRequest (and related UI form data)
  - **Fields:**
    
    - userId
    - prompt
    - negativePrompt
    - modelId
    - resolution
    - aspectRatio
    - seed
    - inferenceSteps
    - cfgScale
    - campaignId (optional)
    
  
  #### .1.5. Target
  
  - **Service:** N8N Orchestration Layer (Webhook)
  - **Model:** EVT-AIG-001 Payload Schema
  - **Fields:**
    
    - requestId
    - correlationId
    - userId
    - prompt
    - negativePrompt
    - modelId
    - resolution
    - aspectRatio
    - seed
    - inferenceSteps
    - cfgScale
    - campaignId
    - callbackUrl
    
  
  #### .1.6. Transformation
  
  - **Type:** direct
  - **Logic:** Direct field-to-field mapping. `requestId` and `correlationId` are generated by Odoo. `callbackUrl` is constructed by Odoo.
  - **Configuration:**
    
    
  
  #### .1.7. Frequency
  real-time (on user request)

  #### .1.8. Criticality
  critical

  #### .1.9. Dependencies
  
  - REQ-AIGS-001
  - REQ-IL-002
  
  #### .1.10. Validation
  
  - **Pre Transformation:**
    
    - Odoo UI/model validation for prompt, parameters (REQ-AIGS-003, REQ-AIGS-004).
    
  - **Post Transformation:**
    
    - N8N webhook input schema validation (implicit by N8N).
    
  
  #### .1.11. Performance
  
  - **Expected Volume:** Up to 10,000/day (REQ-AIGS-009)
  - **Latency Requirement:** Webhook call from Odoo should be fast (<500ms)
  - **Optimization Strategy:** Efficient Odoo controller logic.
  
  ### .2. N8N AI Service Response to Odoo Callback Payload (Success)
  Transforms a successful AI image generation response from the AI service into the JSON payload for the Odoo AIImageGenerationCompleted callback.

  #### .2.1. Transformation Id
  PST-002

  #### .2.4. Source
  
  - **Service:** AI Image Generation Service (via N8N)
  - **Model:** AI Service API Success Response
  - **Fields:**
    
    - image_data_or_url
    - image_metadata (format, size, width, height)
    - any_service_specific_ids
    
  
  #### .2.5. Target
  
  - **Service:** InfluenceGen Odoo Infrastructure & Integration Services Layer (Callback API)
  - **Model:** EVT-AIG-002 Payload Schema
  - **Fields:**
    
    - requestId
    - correlationId
    - status ('completed')
    - imageData / imageUrl
    - imageMetadata
    - hashValue
    
  
  #### .2.6. Transformation
  
  - **Type:** direct
  - **Logic:** Map AI service output to callback fields. N8N calculates `hashValue`. `requestId` and `correlationId` are passed through from the initial Odoo request.
  - **Configuration:**
    
    
  
  #### .2.7. Frequency
  real-time (on AI service completion)

  #### .2.8. Criticality
  critical

  #### .2.9. Dependencies
  
  - REQ-AIGS-001
  - REQ-IL-003
  - REQ-AIGS-006
  
  #### .2.10. Validation
  
  - **Pre Transformation:**
    
    - N8N checks AI service response for success status and expected data.
    
  - **Post Transformation:**
    
    - Odoo callback API input schema validation (implicit by Odoo controller).
    
  
  #### .2.11. Performance
  
  - **Expected Volume:** Up to 10,000/day
  - **Latency Requirement:** N8N processing and callback should be efficient.
  - **Optimization Strategy:** Minimize data manipulation in N8N.
  
  ### .3. N8N AI Service/Workflow Error to Odoo Callback Payload (Failure)
  Transforms an AI service error or N8N workflow error into the JSON payload for the Odoo AIImageGenerationFailed callback.

  #### .3.1. Transformation Id
  PST-003

  #### .3.4. Source
  
  - **Service:** AI Image Generation Service (via N8N) or N8N Workflow
  - **Model:** AI Service API Error Response / N8N Workflow Error Object
  - **Fields:**
    
    - error_code
    - error_message
    
  
  #### .3.5. Target
  
  - **Service:** InfluenceGen Odoo Infrastructure & Integration Services Layer (Callback API)
  - **Model:** EVT-AIG-003 Payload Schema
  - **Fields:**
    
    - requestId
    - correlationId
    - status ('failed')
    - errorCode
    - errorMessage
    
  
  #### .3.6. Transformation
  
  - **Type:** direct
  - **Logic:** Map error details to callback fields. `requestId` and `correlationId` are passed through from the initial Odoo request.
  - **Configuration:**
    
    
  
  #### .3.7. Frequency
  real-time (on error occurrence)

  #### .3.8. Criticality
  important

  #### .3.9. Dependencies
  
  - REQ-AIGS-001
  - REQ-IL-003
  
  #### .3.10. Validation
  
  - **Pre Transformation:**
    
    - N8N captures error details.
    
  - **Post Transformation:**
    
    - Odoo callback API input schema validation.
    
  
  #### .3.11. Performance
  
  - **Expected Volume:** Low (ideally)
  - **Latency Requirement:** Callback should be prompt.
  - **Optimization Strategy:** N/A
  
  ### .4. Odoo Callback Payload Processing and Odoo Model Update
  Processes the incoming JSON payload from N8N callback, downloads image if URL provided, updates AIImageGenerationRequest status, and creates/updates GeneratedImage record in Odoo.

  #### .4.1. Transformation Id
  PST-004

  #### .4.4. Source
  
  - **Service:** N8N Orchestration Layer (Callback)
  - **Model:** EVT-AIG-002 / EVT-AIG-003 Payload Schema
  - **Fields:**
    
    - requestId
    - status
    - imageData/imageUrl
    - imageMetadata
    - hashValue
    - errorCode
    - errorMessage
    
  
  #### .4.5. Target
  
  - **Service:** InfluenceGen Odoo Business Logic Layer / Infrastructure Layer
  - **Model:** AIImageGenerationRequest, GeneratedImage, Odoo File Store/Cloud Storage
  - **Fields:**
    
    - status
    - errorDetails (in AIImageGenerationRequest)
    - storageUrl
    - fileFormat
    - fileSize
    - width
    - height
    - hashValue
    - retentionCategory
    - usageRights (in GeneratedImage)
    
  
  #### .4.6. Transformation
  
  - **Type:** custom
  - **Logic:** If status is 'completed': Download image if `imageUrl` is present (REQ-IL-010), save image to Odoo filestore/cloud (REQ-AIGS-006), create `GeneratedImage` record, update `AIImageGenerationRequest` status and link to `GeneratedImage`. If status is 'failed': Update `AIImageGenerationRequest` status and `errorDetails`.
  - **Configuration:**
    
    - **Storage_Type:** odoo_filestore | cloud_s3 (configurable)
    
  
  #### .4.7. Frequency
  real-time (on callback receipt)

  #### .4.8. Criticality
  critical

  #### .4.9. Dependencies
  
  - REQ-AIGS-006
  - REQ-IL-010
  - REQ-AIGS-010
  
  #### .4.10. Validation
  
  - **Pre Transformation:**
    
    - Odoo validates incoming callback payload schema, authenticity of call.
    
  - **Post Transformation:**
    
    - Verify `AIImageGenerationRequest` status updated correctly. Verify `GeneratedImage` record created with correct metadata and image stored.
    
  
  #### .4.11. Performance
  
  - **Expected Volume:** Up to 10,000/day
  - **Latency Requirement:** Callback processing should be efficient, image download time considered.
  - **Optimization Strategy:** Optimized image download and storage logic.
  
  
- **Implementation Priority:**
  
  - **Component:** PST-001 (Odoo to N8N Request)  
**Priority:** high  
**Dependencies:**
    
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** PST-002 (N8N to Odoo Success Callback)  
**Priority:** high  
**Dependencies:**
    
    - PST-001
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** PST-003 (N8N to Odoo Failure Callback)  
**Priority:** high  
**Dependencies:**
    
    - PST-001
    
**Estimated Effort:** Low  
**Risk Level:** low  
  - **Component:** PST-004 (Odoo Callback Processing Logic)  
**Priority:** high  
**Dependencies:**
    
    - PST-002
    - PST-003
    
**Estimated Effort:** Medium-High  
**Risk Level:** medium  
  - **Component:** Field Level Validations for Onboarding (M004, M005)  
**Priority:** high  
**Dependencies:**
    
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** Retry Mechanisms for Odoo-N8N Interface  
**Priority:** high  
**Dependencies:**
    
    - PST-001
    - PST-002
    - PST-003
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  
- **Risk Assessment:**
  
  - **Risk:** Data loss or corruption during Odoo-N8N-AI service transformations.  
**Impact:** high  
**Probability:** medium  
**Mitigation:** Robust error handling, retry mechanisms, comprehensive logging, checksums for image data, transactional integrity where possible in Odoo.  
**Contingency Plan:** Manual data reconciliation and correction based on logs. Re-triggering of failed requests.  
  - **Risk:** Schema inconsistencies between Odoo, N8N payloads, and AI service APIs.  
**Impact:** high  
**Probability:** medium  
**Mitigation:** Detailed and versioned API/payload specifications (OpenAPI for Odoo callback), thorough integration testing, contract testing if feasible.  
**Contingency Plan:** Rapid patching of transformation logic in Odoo or N8N. Rollback to previous stable versions.  
  - **Risk:** Performance bottlenecks in transformation logic, especially N8N workflows or Odoo callback processing.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Performance testing, optimization of N8N workflows (e.g., minimize in-memory processing of large data), efficient Odoo ORM usage, asynchronous image downloading in Odoo callback.  
**Contingency Plan:** Scale N8N/Odoo resources. Optimize critical code paths post-identification.  
  - **Risk:** Inadequate validation leading to data quality issues in Odoo.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Comprehensive server-side validation (REQ-IOKYC-014, REQ-DMG-013), clearly defined business rule validations (REQ-DMG-015), data quality monitoring.  
**Contingency Plan:** Data cleansing scripts/processes (REQ-DMG-017).  
  
- **Recommendations:**
  
  - **Category:** Data Mapping & Validation  
**Recommendation:** Implement strict schema validation for all JSON payloads exchanged between Odoo and N8N (EVT-AIG-001, EVT-AIG-002, EVT-AIG-003) on both sending and receiving ends.  
**Justification:** Ensures data integrity and helps catch integration errors early. Aligns with REQ-IL-004.  
**Priority:** high  
**Implementation Notes:** Use JSON Schema validation libraries in Python (Odoo) and potentially within N8N custom function nodes if needed.  
  - **Category:** Transformation Logic  
**Recommendation:** Keep transformation logic within N8N workflows minimal and focused on adapting data between Odoo and the AI service. Complex business logic related to the AI request or result interpretation should reside in Odoo.  
**Justification:** Maintains separation of concerns; Odoo as the system of record and primary business logic engine. N8N as orchestrator/integrator.  
**Priority:** high  
**Implementation Notes:** Use N8N primarily for data routing, simple field mapping, and API calls.  
  - **Category:** Error Handling  
**Recommendation:** Ensure that error messages transformed and passed from N8N to Odoo (EVT-AIG-003) are standardized and include enough detail (original error code/message from AI service if possible) for effective troubleshooting in Odoo.  
**Justification:** Aids administrators in diagnosing AI generation failures without needing direct access to N8N or AI service logs for every issue.  
**Priority:** high  
**Implementation Notes:** Define a common error structure within the EVT-AIG-003 payload.  
  - **Category:** Performance  
**Recommendation:** If image data is passed directly in payloads (EVT-AIG-002 `imageData`), ensure Odoo and N8N configurations (e.g., HTTP body size limits) can handle expected image sizes. Prefer `imageUrl` for larger images if network performance for download is acceptable.  
**Justification:** Prevents issues with large payloads causing HTTP errors or excessive memory usage. `REQ-IL-010` allows both methods.  
**Priority:** medium  
**Implementation Notes:** Assess typical image sizes. Configure web server (Odoo) and N8N webhook/HTTP node settings accordingly.  
  


---

