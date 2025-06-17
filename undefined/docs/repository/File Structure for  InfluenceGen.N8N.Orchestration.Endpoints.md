# Specification

# 1. Files

- **Path:** n8n_workflows/utils/logging_helpers.js  
**Description:** Contains JavaScript helper functions for standardized, structured logging within N8N Function nodes. This code is intended to be embedded within N8N Function nodes responsible for logging various stages of workflow execution, errors, and contextual information. Ensures logs are consistent and can be easily parsed by a centralized logging system.  
**Template:** JavaScript Helper Module  
**Dependancy Level:** 0  
**Name:** logging_helpers  
**Type:** JavaScript Utility  
**Relative Path:** utils/logging_helpers.js  
**Repository Id:** REPO-N8NO-005  
**Pattern Ids:**
    
    - Helper/UtilityPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** formatLogEntry  
**Parameters:**
    
    - level (string)
    - message (string)
    - context (object)
    
**Return Type:** object  
**Attributes:** static  
    - **Name:** logInfo  
**Parameters:**
    
    - workflowInstance (object)
    - nodeName (string)
    - message (string)
    - data (object)
    
**Return Type:** void  
**Attributes:** static  
    - **Name:** logError  
**Parameters:**
    
    - workflowInstance (object)
    - nodeName (string)
    - errorMessage (string)
    - errorDetails (object)
    
**Return Type:** void  
**Attributes:** static  
    
**Implemented Features:**
    
    - Structured Logging Utilities
    
**Requirement Ids:**
    
    - REQ-ATEL-010
    
**Purpose:** To provide reusable JavaScript functions for consistent and structured logging within N8N Function nodes, supporting REQ-ATEL-010.  
**Logic Description:** Includes functions to create structured log messages (JSON format) with common fields like timestamp, level, message, workflow ID, node ID, correlation ID, and custom context. This facilitates easier integration with centralized logging solutions.  
**Documentation:**
    
    - **Summary:** Helper functions for N8N Function nodes to generate structured logs. Inputs include log level, message, and contextual data. Output is typically a JSON object written to console or N8N execution log.
    
**Namespace:** InfluenceGen.N8N.Utils.Logging  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** n8n_workflows/utils/data_transformation_helpers.js  
**Description:** Contains JavaScript helper functions for common data transformations required within N8N Function nodes, such as formatting request payloads for AI services or Odoo callbacks, and parsing responses. This code is intended for embedding into relevant Function nodes.  
**Template:** JavaScript Helper Module  
**Dependancy Level:** 0  
**Name:** data_transformation_helpers  
**Type:** JavaScript Utility  
**Relative Path:** utils/data_transformation_helpers.js  
**Repository Id:** REPO-N8NO-005  
**Pattern Ids:**
    
    - Helper/UtilityPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** prepareAIServiceRequest  
**Parameters:**
    
    - odooPayload (object)
    - aiServiceConfig (object)
    
**Return Type:** object  
**Attributes:** static  
    - **Name:** formatOdooCallbackPayload  
**Parameters:**
    
    - aiServiceResponse (object)
    - originalRequest (object)
    - isSuccess (boolean)
    
**Return Type:** object  
**Attributes:** static  
    - **Name:** extractImageDetails  
**Parameters:**
    
    - aiServiceResponse (object)
    
**Return Type:** object  
**Attributes:** static  
    
**Implemented Features:**
    
    - Data Formatting
    - Payload Transformation
    
**Requirement Ids:**
    
    - REQ-AIGS-001
    - REQ-IL-005
    - REQ-IL-003
    
**Purpose:** To provide reusable JavaScript functions for transforming data between Odoo, N8N, and AI services, ensuring correct payload structures.  
**Logic Description:** Includes functions to map fields from Odoo's request to the AI service's expected format, and to structure the AI service's response for the Odoo callback. Handles potential variations in data structures.  
**Documentation:**
    
    - **Summary:** Helper functions for N8N Function nodes to transform data. Inputs are typically JSON objects from previous nodes. Outputs are transformed JSON objects for subsequent nodes.
    
**Namespace:** InfluenceGen.N8N.Utils.Transformation  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** n8n_workflows/workflows/sub_workflows/ai_service_flux_lora_adapter.n8n.json  
**Description:** N8N sub-workflow acting as an adapter for a specific AI image generation service supporting Flux LoRA models. It encapsulates the direct API call logic, parameter mapping, and authentication specific to this AI service. Called by the main AI image generation workflow to promote adaptability (REQ-IL-006).  
**Template:** N8N Workflow JSON  
**Dependancy Level:** 1  
**Name:** ai_service_flux_lora_adapter  
**Type:** N8N Sub-Workflow  
**Relative Path:** workflows/sub_workflows/ai_service_flux_lora_adapter.n8n.json  
**Repository Id:** REPO-N8NO-005  
**Pattern Ids:**
    
    - AdapterPattern
    - ServiceGateway
    
**Members:**
    
    
**Methods:**
    
    - **Name:** StartNode  
**Parameters:**
    
    - inputData (object containing prompt, params, model_config, api_credential_name)
    
**Return Type:** WorkflowData  
**Attributes:** Trigger  
    - **Name:** ParameterMappingNode  
**Parameters:**
    
    - WorkflowData
    
**Return Type:** WorkflowData (with AI service specific payload)  
**Attributes:** FunctionNode  
    - **Name:** AIServiceCallNode_FluxLoRA  
**Parameters:**
    
    - WorkflowData (AI service specific payload)
    
**Return Type:** WorkflowData (AI service response)  
**Attributes:** HTTPRequestNode  
    - **Name:** ResponseFormattingNode  
**Parameters:**
    
    - WorkflowData (AI service response)
    
**Return Type:** WorkflowData (standardized response for parent workflow)  
**Attributes:** FunctionNode  
    - **Name:** LoggingNode_Adapter  
**Parameters:**
    
    - WorkflowData
    
**Return Type:** WorkflowData  
**Attributes:** FunctionNode  
    
**Implemented Features:**
    
    - AI Service API Interaction (Flux LoRA specific)
    - Parameter Mapping
    - AI Service Authentication
    
**Requirement Ids:**
    
    - REQ-IL-006
    - REQ-IL-005
    - REQ-IL-007
    
**Purpose:** To abstract the interaction details with a specific AI service (Flux LoRA), enabling easier changes or additions of AI providers.  
**Logic Description:** 1. Receives standardized parameters (prompt, generation settings, AI model details, credential reference) from the calling workflow. 2. Maps these parameters to the specific request format required by the Flux LoRA AI service. 3. Uses an HTTP Request node configured with the Flux LoRA service endpoint and N8N credentials for authentication. Implements HTTPS (REQ-IL-007). 4. Processes the AI service's response, extracting the image URL/data and any error information. 5. Formats this into a standardized response structure. 6. Returns the standardized response to the parent workflow. Includes logging steps (REQ-ATEL-010).  
**Documentation:**
    
    - **Summary:** N8N sub-workflow to interact with a Flux LoRA AI service. Takes standardized input, makes the API call, and returns a standardized output. Handles service-specific authentication and request/response formats.
    
**Namespace:** InfluenceGen.N8N.Workflows.Adapters  
**Metadata:**
    
    - **Category:** Workflow
    
- **Path:** n8n_workflows/workflows/ai_image_generation_workflow.n8n.json  
**Description:** Main N8N workflow orchestrating AI image generation requests. It is triggered by a webhook from Odoo, calls an AI image generation service (potentially via an adapter sub-workflow like `ai_service_flux_lora_adapter`), handles responses and errors, logs execution details, and calls back a designated Odoo API endpoint with the result.  
**Template:** N8N Workflow JSON  
**Dependancy Level:** 2  
**Name:** ai_image_generation_workflow  
**Type:** N8N Workflow  
**Relative Path:** workflows/ai_image_generation_workflow.n8n.json  
**Repository Id:** REPO-N8NO-005  
**Pattern Ids:**
    
    - WebhookIntegration
    - AsynchronousTaskProcessing
    - ServiceOrchestration
    - AdapterPattern
    - ErrorHandling
    - RetryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** OdooWebhookTriggerNode  
**Parameters:**
    
    - HttpRequestData (from Odoo)
    
**Return Type:** WorkflowData  
**Attributes:** WebhookTrigger  
    - **Name:** InputValidationAndPreparationNode  
**Parameters:**
    
    - WorkflowData
    
**Return Type:** WorkflowData (validated and prepared)  
**Attributes:** FunctionNode  
    - **Name:** ExecuteAIServiceAdapterNode  
**Parameters:**
    
    - WorkflowData (prepared for AI adapter)
    
**Return Type:** WorkflowData (standardized AI response)  
**Attributes:** ExecuteWorkflowNode  
    - **Name:** ResponseProcessingNode  
**Parameters:**
    
    - WorkflowData (standardized AI response)
    
**Return Type:** WorkflowData (payload for Odoo callback)  
**Attributes:** FunctionNode  
    - **Name:** OdooCallbackNode  
**Parameters:**
    
    - WorkflowData (payload for Odoo callback)
    
**Return Type:** WorkflowData (Odoo callback response)  
**Attributes:** HTTPRequestNode  
    - **Name:** MainWorkflowLoggingNode  
**Parameters:**
    
    - WorkflowData
    - stepName (string)
    
**Return Type:** WorkflowData  
**Attributes:** FunctionNode  
    - **Name:** ErrorHandlingBranchNode  
**Parameters:**
    
    - WorkflowData (error object)
    
**Return Type:** WorkflowData (formatted error payload for Odoo callback)  
**Attributes:** ErrorTrigger, FunctionNode  
    - **Name:** RetryLogicConfiguration  
**Parameters:**
    
    - On AIServiceCallNode or ExecuteAIServiceAdapterNode
    
**Return Type:** N/A  
**Attributes:** NodeSetting  
    
**Implemented Features:**
    
    - AI Image Generation Orchestration
    - Odoo Webhook Reception
    - Asynchronous Processing
    - AI Service Integration via Adapter
    - Odoo API Callback
    - Error Handling and Retries
    - Workflow Event Logging
    - Secure Communication
    
**Requirement Ids:**
    
    - REQ-AIGS-001
    - REQ-IL-001
    - REQ-IL-003
    - REQ-IL-005
    - REQ-IL-006
    - REQ-IL-007
    - REQ-IL-009
    - REQ-ATEL-010
    
**Purpose:** To reliably and asynchronously process AI image generation requests from Odoo, integrate with AI services, and return results to Odoo.  
**Logic Description:** 1. **OdooWebhookTriggerNode**: Receives HTTP POST from Odoo containing prompt, parameters, `correlationId`, and AI model preference. Authenticates request (e.g., bearer token). (REQ-AIGS-001). 2. **InputValidationAndPreparationNode**: (Function Node) Validates essential input. Extracts `correlationId`. Prepares parameters for the AI service adapter. Logs request reception with `correlationId`. (REQ-ATEL-010). 3. **ExecuteAIServiceAdapterNode**: (Execute Workflow Node) Calls the appropriate AI service adapter sub-workflow (e.g., `ai_service_flux_lora_adapter.n8n.json`), passing prepared data. Configured with retry settings (e.g., 3 retries, exponential backoff for network/transient errors from adapter). (REQ-IL-005, REQ-IL-006, REQ-IL-009). 4. **ResponseProcessingNode**: (Function Node) Processes the standardized response from the adapter. Extracts image URL/data or error details. Logs AI service interaction outcome. 5. **OdooCallbackNode**: (HTTP Request Node) Sends the result (image URL/data or error details) and `correlationId` to the Odoo callback API endpoint. Uses HTTPS. (REQ-IL-003, REQ-IL-007). 6. **MainWorkflowLoggingNode**: (Function Node) Used at various points to log significant events and `correlationId`. (REQ-ATEL-010). 7. **ErrorHandlingBranchNode**: Catches errors from previous nodes (e.g., persistent AI service failure, validation errors). Formats a standardized error payload and sends it to Odoo via OdooCallbackNode. Logs the error. (REQ-IL-009).  
**Documentation:**
    
    - **Summary:** This N8N workflow is the central orchestrator for AI image generation. It receives requests from Odoo, manages interaction with AI services (via adapters), and sends results back to Odoo. Includes comprehensive error handling, retry logic, and logging.
    
**Namespace:** InfluenceGen.N8N.Workflows.Main  
**Metadata:**
    
    - **Category:** Workflow
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  - N8N_ENCRYPTION_KEY (Environment Variable - for N8N internal credential encryption)
  - ODOO_CALLBACK_BASE_URL (Environment Variable - e.g., https://odoo.example.com/api/influencegen)
  - ODOO_CALLBACK_IMAGE_RESULT_ENDPOINT (Environment Variable - e.g., /image_result_callback)
  - ODOO_CALLBACK_API_KEY_CREDENTIAL_NAME (N8N Credential Name - for authenticating N8N calls to Odoo)
  - AI_SERVICE_FLUX_LORA_API_BASE_URL (Environment Variable - e.g., https://ai.example.com/fluxlora)
  - AI_SERVICE_FLUX_LORA_API_KEY_CREDENTIAL_NAME (N8N Credential Name - for Flux LoRA service)
  - AI_SERVICE_ADAPTER_SUBWORKFLOW_ID_FLUX_LORA (Environment Variable - ID of the ai_service_flux_lora_adapter workflow)
  - N8N_LOG_LEVEL (Environment Variable - e.g., 'info', 'debug', for N8N's own logging, if supported for centralized collection REQ-ATEL-010)
  - CENTRAL_LOGGING_WEBHOOK_URL (Environment Variable - if custom logging nodes push to an external log aggregator REQ-ATEL-010)
  - N8N_EXECUTIONS_DATA_PRUNE_MAX_AGE (Environment Variable - for N8N's internal execution log retention REQ-ATEL-010, REQ-DDSI-005 implied system maintenance)
  


---

