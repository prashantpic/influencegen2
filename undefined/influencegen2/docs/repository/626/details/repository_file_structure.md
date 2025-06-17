# Specification

# 1. Files

- **Path:** n8n_workflows/main_ai_image_generation_workflow.json  
**Description:** Core N8N workflow definition for orchestrating AI image generation. This JSON file contains all nodes, connections, and configurations for the workflow. It handles incoming requests from Odoo via webhook, interacts with specified AI image generation services, processes responses (including images or errors), implements retry logic for transient AI service failures, and securely calls back a designated Odoo API endpoint with the results. It leverages N8N's credential management for secure API key handling.  
**Template:** N8N Workflow JSON  
**Dependancy Level:** 1  
**Name:** main_ai_image_generation_workflow  
**Type:** WorkflowDefinition  
**Relative Path:** main_ai_image_generation_workflow.json  
**Repository Id:** REPO-IGN8N-005  
**Pattern Ids:**
    
    - PipesAndFilters
    - WebhookIntegration
    - AsynchronousTaskProcessing
    - AdapterPattern
    
**Members:**
    
    - **Name:** name  
**Type:** String  
**Attributes:** property  
    - **Name:** nodes  
**Type:** Array<Object>  
**Attributes:** property  
    - **Name:** connections  
**Type:** Array<Object>  
**Attributes:** property  
    - **Name:** active  
**Type:** Boolean  
**Attributes:** property  
    - **Name:** settings  
**Type:** Object  
**Attributes:** property  
    - **Name:** meta  
**Type:** Object  
**Attributes:** property  
    - **Name:** pinData  
**Type:** Object  
**Attributes:** property  
    
**Methods:**
    
    - **Name:** HandleOdooWebhookTrigger  
**Parameters:**
    
    - odooRequestPayload
    
**Return Type:** Object  
**Attributes:** WorkflowStage|NodeGroup  
    - **Name:** ParseAndValidateOdooRequest  
**Parameters:**
    
    - webhookData
    
**Return Type:** Object  
**Attributes:** WorkflowStage|NodeGroup  
    - **Name:** AdaptRequestToAIServiceAPI  
**Parameters:**
    
    - parsedOdooRequest
    - aiServiceType
    
**Return Type:** Object  
**Attributes:** WorkflowStage|NodeGroup  
    - **Name:** CallExternalAIService  
**Parameters:**
    
    - aiServiceApiPayload
    - aiServiceCredentials
    
**Return Type:** Object  
**Attributes:** WorkflowStage|NodeGroup|Retryable  
    - **Name:** ProcessAIServiceResponse  
**Parameters:**
    
    - aiServiceApiResponse
    
**Return Type:** Object  
**Attributes:** WorkflowStage|NodeGroup  
    - **Name:** FormatOdooCallbackPayload  
**Parameters:**
    
    - processedAiResult
    - originalOdooRequestId
    
**Return Type:** Object  
**Attributes:** WorkflowStage|NodeGroup  
    - **Name:** SendResultToOdooCallback  
**Parameters:**
    
    - odooCallbackPayload
    - odooCallbackAuth
    
**Return Type:** Object  
**Attributes:** WorkflowStage|NodeGroup  
    - **Name:** HandleWorkflowErrors  
**Parameters:**
    
    - errorObject
    
**Return Type:** void  
**Attributes:** WorkflowStage|NodeGroup  
    - **Name:** LogWorkflowExecutionStep  
**Parameters:**
    
    - stepName
    - status
    - details
    
**Return Type:** void  
**Attributes:** WorkflowStage|NodeGroup  
    
**Implemented Features:**
    
    - AI Image Generation Orchestration
    - Webhook Reception from Odoo
    - AI Service API Invocation (Flux LoRA models)
    - Response Handling (Success/Error)
    - Retry Logic for AI Service Calls
    - Odoo Callback API Invocation
    - Secure Credential Usage (via N8N vault)
    - Workflow Step Logging
    
**Requirement Ids:**
    
    - REQ-IL-001
    - REQ-AIGS-001
    - REQ-IL-005
    - REQ-IL-006
    - REQ-IL-007
    - REQ-IL-008
    - REQ-IL-009
    - REQ-IL-017
    - REQ-AIGS-013
    - REQ-ATEL-010
    
**Purpose:** Defines the N8N workflow that acts as the central orchestrator for AI image generation requests initiated from Odoo, managing communication with external AI services and returning results.  
**Logic Description:** 1. A Webhook node receives POST requests from Odoo containing AI image generation parameters.
2. Function/Set nodes parse the input, validate parameters, and prepare the request for the AI service (potentially using logic from ai_service_adapter.js for different AI backends like ComfyUI or StabilityAI).
3. An HTTP Request node calls the target AI service API using stored N8N credentials. This node is configured with retry mechanisms for transient errors.
4. IF/Switch nodes and Function nodes process the AI service's response, distinguishing between success (image data/URL) and errors.
5. For successes, the image URL or data is formatted for the Odoo callback (using logic from odoo_payload_handler.js).
6. For errors, a standardized error payload is created (using logic from error_processor.js).
7. Another HTTP Request node securely calls the Odoo callback API endpoint to deliver the result or error.
8. Throughout the workflow, Function nodes or specific logging mechanisms record key execution steps, input/output data (excluding sensitive info), and errors (potentially using logic from custom_logger.js) for traceability and debugging. These logs are intended to be captured by a centralized logging system.  
**Documentation:**
    
    - **Summary:** N8N workflow definition (JSON) for orchestrating AI image generation. Inputs: Odoo webhook request with image parameters. Outputs: Calls Odoo callback API with generated image URL/data or error details. Manages interactions with external AI service APIs.
    
**Namespace:** InfluenceGen.N8N.Workflows.AIImageGeneration  
**Metadata:**
    
    - **Category:** WorkflowDefinition
    
- **Path:** n8n_workflows/lib/ai_service_adapter.js  
**Description:** JavaScript helper module containing functions to adapt Odoo AI image generation request parameters to the specific API formats required by various AI services (e.g., ComfyUI, StabilityAI, other Flux LoRA model providers). This supports modularity and easy extension for new AI services. The functions defined here are intended to be embedded within N8N Function nodes in the main workflow.  
**Template:** JavaScript N8N Helper  
**Dependancy Level:** 0  
**Name:** ai_service_adapter  
**Type:** UtilityScript  
**Relative Path:** lib/ai_service_adapter.js  
**Repository Id:** REPO-IGN8N-005  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** adaptToAIService  
**Parameters:**
    
    - odooRequestParams
    - targetAIServiceType
    
**Return Type:** Object  
**Attributes:** public|static  
    - **Name:** getAIServiceEndpoint  
**Parameters:**
    
    - targetAIServiceType
    - modelName
    
**Return Type:** String  
**Attributes:** public|static  
    - **Name:** getAIServiceAuthHeaders  
**Parameters:**
    
    - targetAIServiceType
    - credentialsObject
    
**Return Type:** Object  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - AI Service Request Payload Transformation
    - AI Service Endpoint Resolution
    
**Requirement Ids:**
    
    - REQ-IL-006
    
**Purpose:** Provides reusable JavaScript logic to convert standardized Odoo AI requests into the specific formats required by different AI backend APIs.  
**Logic Description:** 1. The `adaptToAIService` function acts as a dispatcher based on `targetAIServiceType`.
2. Specific private functions (e.g., `_formatForComfyUI`, `_formatForStabilityAI`) handle the detailed mapping of Odoo parameters (prompt, negative_prompt, seed, steps, resolution, model_id etc.) to the AI service's expected JSON or form-data structure.
3. `getAIServiceEndpoint` resolves the correct API endpoint URL based on the service type and potentially the model.
4. `getAIServiceAuthHeaders` helps construct any service-specific authentication headers if they are more complex than what N8N's HTTP Request node credential handling offers directly. This function should primarily leverage N8N's credential system where possible.  
**Documentation:**
    
    - **Summary:** JavaScript helper for adapting AI image generation request parameters from Odoo to various external AI service API formats. To be used within N8N Function nodes.
    
**Namespace:** InfluenceGen.N8N.Helpers  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** n8n_workflows/lib/odoo_payload_handler.js  
**Description:** JavaScript helper module responsible for validating and parsing incoming webhook payloads from Odoo, and for formatting payloads (both success and error) to be sent back to Odoo's callback API. Ensures consistent data contract adherence. The functions defined here are intended to be embedded within N8N Function nodes.  
**Template:** JavaScript N8N Helper  
**Dependancy Level:** 0  
**Name:** odoo_payload_handler  
**Type:** UtilityScript  
**Relative Path:** lib/odoo_payload_handler.js  
**Repository Id:** REPO-IGN8N-005  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** parseAndValidateOdooWebhook  
**Parameters:**
    
    - webhookBody
    
**Return Type:** Object  
**Attributes:** public|static  
    - **Name:** formatSuccessCallback  
**Parameters:**
    
    - imageUrlOrData
    - originalRequestId
    - generationMetadata
    
**Return Type:** Object  
**Attributes:** public|static  
    - **Name:** formatErrorCallback  
**Parameters:**
    
    - errorMessage
    - errorCode
    - originalRequestId
    
**Return Type:** Object  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Odoo Webhook Payload Parsing
    - Odoo Webhook Payload Validation
    - Odoo Callback Payload Formatting (Success/Error)
    
**Requirement Ids:**
    
    - REQ-AIGS-001
    
**Purpose:** Provides JavaScript functions for robust parsing of incoming Odoo requests and consistent formatting of callback responses to Odoo.  
**Logic Description:** 1. `parseAndValidateOdooWebhook`: Accesses fields from Odoo's webhook data. Performs basic validation (e.g., presence of required fields like `request_id`, `prompt`). Throws an error or returns a structured error object if validation fails.
2. `formatSuccessCallback`: Constructs the JSON payload for a successful image generation, including `status: 'completed'`, the image URL or base64 data, the original Odoo `request_id`, and any other relevant metadata (e.g., seed used, dimensions).
3. `formatErrorCallback`: Constructs the JSON payload for a failed image generation, including `status: 'failed'`, a descriptive `error_message`, an optional `error_code`, and the original Odoo `request_id`.  
**Documentation:**
    
    - **Summary:** JavaScript helper for parsing incoming Odoo webhook data and formatting payloads for the Odoo callback API. Ensures consistent communication structure. To be used within N8N Function nodes.
    
**Namespace:** InfluenceGen.N8N.Helpers  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** n8n_workflows/lib/error_processor.js  
**Description:** JavaScript helper module with functions for standardizing error objects received from external AI services or generated within the N8N workflow itself. This helps in creating consistent error messages for logging and for the Odoo callback. The functions defined here are intended to be embedded within N8N Function nodes.  
**Template:** JavaScript N8N Helper  
**Dependancy Level:** 0  
**Name:** error_processor  
**Type:** UtilityScript  
**Relative Path:** lib/error_processor.js  
**Repository Id:** REPO-IGN8N-005  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** normalizeAIServiceError  
**Parameters:**
    
    - rawErrorFromAIService
    - serviceType
    
**Return Type:** Object  
**Attributes:** public|static  
    - **Name:** createWorkflowErrorObject  
**Parameters:**
    
    - errorMessage
    - stepName
    - internalErrorCode
    
**Return Type:** Object  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - AI Service Error Normalization
    - Workflow Error Object Creation
    
**Requirement Ids:**
    
    - REQ-IL-009
    
**Purpose:** Provides functions to process and standardize error information from various sources within the AI image generation workflow for consistent reporting.  
**Logic Description:** 1. `normalizeAIServiceError`: Takes the raw error response from an AI service (e.g., HTTP error object, JSON error payload) and the type of service. It extracts key information like status code, a user-friendly message, and any specific error codes/details, returning a standardized error object (e.g., `{ message: '...', code: '...', details: '...' }`).
2. `createWorkflowErrorObject`: Creates a standardized error object for errors originating within the N8N workflow logic itself, including a message, the name of the N8N step where the error occurred, and an optional internal error code.  
**Documentation:**
    
    - **Summary:** JavaScript helper for normalizing error objects from AI services and creating standardized error objects for internal workflow failures. Used within N8N Function nodes.
    
**Namespace:** InfluenceGen.N8N.Helpers  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** n8n_workflows/lib/custom_logger.js  
**Description:** JavaScript helper module for implementing custom, structured logging within N8N Function nodes. This facilitates detailed traceability and can be used to send logs to external centralized logging systems if N8N's native execution log is insufficient. The functions defined here are intended to be embedded within N8N Function nodes.  
**Template:** JavaScript N8N Helper  
**Dependancy Level:** 0  
**Name:** custom_logger  
**Type:** UtilityScript  
**Relative Path:** lib/custom_logger.js  
**Repository Id:** REPO-IGN8N-005  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** logEvent  
**Parameters:**
    
    - level
    - message
    - contextData
    
**Return Type:** void  
**Attributes:** public|static  
    - **Name:** getCorrelationId  
**Parameters:**
    
    - n8nExecutionData
    
**Return Type:** String  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Structured Event Logging
    - Correlation ID Extraction for Logging
    
**Requirement Ids:**
    
    - REQ-ATEL-010
    
**Purpose:** Provides standardized functions for structured logging within N8N workflows, including correlation IDs, to enhance traceability and support centralized logging efforts.  
**Logic Description:** 1. `logEvent`: Takes a log level (e.g., 'INFO', 'ERROR', 'DEBUG'), a message string, and a contextData object. It constructs a structured log entry (JSON object) including timestamp, level, message, correlation ID (obtained via `getCorrelationId`), and the contextData. This structured entry is then output using `console.log` (for N8N to capture) or sent to an external logging API if configured.
2. `getCorrelationId`: Extracts a correlation ID from the N8N execution data (e.g., from the initial webhook payload passed by Odoo or a generated execution ID) to link log entries across different steps or systems.  
**Documentation:**
    
    - **Summary:** JavaScript helper for custom and structured logging within N8N Function nodes. Facilitates consistent logging format and inclusion of correlation IDs. Used within N8N Function nodes.
    
**Namespace:** InfluenceGen.N8N.Helpers  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** n8n_workflows/package.json  
**Description:** NPM package file to manage development dependencies for JavaScript helper scripts used in N8N Function nodes. This includes tools like ESLint for code linting and Prettier for code formatting, helping maintain code quality and consistency for the .js files in the lib/ directory. This file is not directly used by N8N for workflow execution but supports the development process.  
**Template:** Node.js Package JSON  
**Dependancy Level:** 0  
**Name:** influencegen-n8n-workflow-helpers  
**Type:** Configuration  
**Relative Path:** package.json  
**Repository Id:** REPO-IGN8N-005  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** name  
**Type:** String  
**Attributes:** property  
    - **Name:** version  
**Type:** String  
**Attributes:** property  
    - **Name:** description  
**Type:** String  
**Attributes:** property  
    - **Name:** scripts  
**Type:** Object  
**Attributes:** property  
    - **Name:** devDependencies  
**Type:** Object  
**Attributes:** property  
    
**Methods:**
    
    
**Implemented Features:**
    
    - JavaScript Development Tooling Configuration
    
**Requirement Ids:**
    
    - REQ-DDSI-003
    
**Purpose:** Configures development tools (linters, formatters) for the JavaScript helper scripts, ensuring code quality and consistency before their logic is embedded into N8N Function nodes.  
**Logic Description:** Standard `package.json` file. `devDependencies` section lists ESLint, Prettier, and any relevant plugins. `scripts` section includes commands like `"lint": "eslint lib/**/*.js"` and `"format": "prettier --write lib/**/*.js"` to enforce coding standards on the JavaScript helper files.  
**Documentation:**
    
    - **Summary:** Defines development dependencies and scripts for linting and formatting JavaScript helper files used within N8N Function nodes.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

