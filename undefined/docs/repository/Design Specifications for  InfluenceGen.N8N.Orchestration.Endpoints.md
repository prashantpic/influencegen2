# Software Design Specification (SDS) for InfluenceGen.N8N.Orchestration.Endpoints

## 1. Introduction

This document outlines the software design specifications for the `InfluenceGen.N8N.Orchestration.Endpoints` repository. This repository is responsible for the N8N workflow automation layer within the InfluenceGen platform. Its primary function is to orchestrate asynchronous tasks, particularly AI image generation requests initiated by Odoo. These N8N workflows will interact with external AI model serving APIs (primarily Flux LoRA models), manage errors and retries, and communicate results back to a designated Odoo API endpoint.

This SDS will detail the design of the N8N workflows and associated JavaScript helper functions.

**Relevant Requirements:** REQ-AIGS-001, REQ-IL-001, REQ-IL-003, REQ-IL-005, REQ-IL-006, REQ-IL-007, REQ-IL-009, REQ-ATEL-010, REQ-DDSI-005.

## 2. System Architecture Context

This repository implements the `n8n-orchestration-layer` within the overall Layered Architecture of the InfluenceGen system. It acts as an intermediary and orchestration engine between the `InfluenceGen Odoo Infrastructure & Integration Services Layer` (specifically REPO-IGOII-004 for callbacks from Odoo) and external AI services.

## 3. Design Goals

*   **Reliability**: Ensure robust and resilient processing of AI image generation requests, including error handling and retry mechanisms (REQ-IL-009).
*   **Asynchronicity**: Process tasks asynchronously to prevent blocking Odoo's main processes (REQ-AIGS-001).
*   **Adaptability**: Design integrations with AI services to be adaptable to different AI service APIs with minimal code changes (REQ-IL-006).
*   **Security**: Ensure secure communication (HTTPS) and secure management of credentials for AI services (REQ-IL-007).
*   **Observability**: Implement comprehensive and structured logging for traceability and troubleshooting (REQ-ATEL-010).
*   **Maintainability**: Develop modular workflows and helper functions that are easy to understand and update.

## 4. Component Design

### 4.1 JavaScript Helper Utilities (`utils/`)

#### 4.1.1 `logging_helpers.js`

*   **Purpose**: Provides standardized JavaScript helper functions for structured logging within N8N Function nodes, supporting REQ-ATEL-010. Logs are intended to be JSON formatted for easy parsing by a centralized logging system.
*   **Namespace**: `InfluenceGen.N8N.Utils.Logging`
*   **Functions**:
    *   **`formatLogEntry(level, message, context)`**
        *   **Parameters**:
            *   `level` (string): Log level (e.g., "INFO", "ERROR", "DEBUG").
            *   `message` (string): The main log message.
            *   `context` (object): An object containing additional contextual information. Expected to include `workflowInstance` (N8N execution data to extract `executionId`, `workflowId`), `nodeName`, `correlationId`, and any other relevant data.
        *   **Return Value**: `object` - A structured log entry.
        *   **Logic Description**:
            1.  Creates a base log object with a UTC timestamp (`new Date().toISOString()`).
            2.  Adds `level` and `message` to the log object.
            3.  Extracts `executionId` (from `workflowInstance.id`), `workflowId` (from `workflowInstance.workflowId`), `nodeName`, and `correlationId` from the `context` object and adds them to the log object.
            4.  Merges any other properties from `context.data` or a dedicated `context.payload` into the log object.
            5.  Returns the structured log object.
    *   **`logInfo(workflowInstance, nodeName, correlationId, message, data = {})`**
        *   **Parameters**:
            *   `workflowInstance` (object): The N8N workflow execution instance data (e.g., from `$execution`).
            *   `nodeName` (string): The name of the N8N node generating the log.
            *   `correlationId` (string): The correlation ID for distributed tracing.
            *   `message` (string): The informational message.
            *   `data` (object, optional): Additional data to include in the log context.
        *   **Return Value**: `void`
        *   **Logic Description**:
            1.  Calls `formatLogEntry` with `level = "INFO"`, the provided `message`, and a context object containing `workflowInstance`, `nodeName`, `correlationId`, and `data`.
            2.  Outputs the formatted log entry (e.g., using `console.log(JSON.stringify(logEntry))` or directly if N8N handles object logging appropriately for its execution log).
    *   **`logError(workflowInstance, nodeName, correlationId, errorMessage, errorDetails = {})`**
        *   **Parameters**:
            *   `workflowInstance` (object): The N8N workflow execution instance data.
            *   `nodeName` (string): The name of the N8N node generating the log.
            *   `correlationId` (string): The correlation ID.
            *   `errorMessage` (string): The primary error message.
            *   `errorDetails` (object, optional): Additional details about the error (e.g., stack trace, error code, input data causing the error).
        *   **Return Value**: `void`
        *   **Logic Description**:
            1.  Calls `formatLogEntry` with `level = "ERROR"`, the `errorMessage`, and a context object containing `workflowInstance`, `nodeName`, `correlationId`, and `errorDetails`.
            2.  Outputs the formatted log entry.
*   **Usage Context**: These functions will be embedded or copied into N8N Function nodes responsible for logging.

#### 4.1.2 `data_transformation_helpers.js`

*   **Purpose**: Provides JavaScript helper functions for common data transformations between Odoo, N8N, and external AI services, ensuring correct payload structures (REQ-AIGS-001, REQ-IL-005, REQ-IL-003).
*   **Namespace**: `InfluenceGen.N8N.Utils.Transformation`
*   **Functions**:
    *   **`prepareAIServiceRequest(odooPayload, aiServiceConfig)`**
        *   **Parameters**:
            *   `odooPayload` (object): The payload received from Odoo (e.g., prompt, negative_prompt, resolution, aspect_ratio, seed, inference_steps, cfg_scale, model_preference, correlation_id).
            *   `aiServiceConfig` (object): Configuration specific to the target AI service adapter (e.g., might contain model mapping keys or default parameters if not provided by Odoo).
        *   **Return Value**: `object` - The request payload formatted for the *standardized input* of an AI service adapter sub-workflow.
        *   **Logic Description**:
            1.  Extracts relevant fields from `odooPayload`.
            2.  Maps Odoo field names to standardized field names expected by AI service adapters (e.g., `model_preference` from Odoo might map to `model_identifier` for the adapter).
            3.  Applies any default values or transformations based on `aiServiceConfig` if necessary.
            4.  Ensures `correlationId` is preserved.
            5.  Returns the structured object.
    *   **`formatOdooCallbackPayload(aiServiceResponse, originalRequest, isSuccess)`**
        *   **Parameters**:
            *   `aiServiceResponse` (object): The standardized response from the AI service adapter sub-workflow (contains image_url/data or error details).
            *   `originalRequest` (object): The initial Odoo request payload (to retrieve `correlationId` and other context if needed).
            *   `isSuccess` (boolean): Flag indicating if the AI generation was successful.
        *   **Return Value**: `object` - The payload formatted for the Odoo callback API.
        *   **Logic Description**:
            1.  Creates a base callback payload object.
            2.  Includes `correlationId` from `originalRequest.correlationId`.
            3.  Sets a `status` field ("success" or "error") based on `isSuccess`.
            4.  If `isSuccess` is true:
                *   Adds image details from `aiServiceResponse` (e.g., `imageUrl`, `imageData`, `metadata`).
            5.  If `isSuccess` is false:
                *   Adds error details from `aiServiceResponse` (e.g., `errorCode`, `errorMessage`).
            6.  Returns the structured object.
    *   **`extractImageDetails(aiServiceAdapterResponse)`**
        *   **Parameters**:
            *   `aiServiceAdapterResponse` (object): The raw response from the AI service adapter sub-workflow (standardized response).
        *   **Return Value**: `object` - An object containing extracted image details (e.g., `imageUrl`, `imageData`, `format`, `dimensions`) or null if not successful.
        *   **Logic Description**:
            1.  Checks if the `aiServiceAdapterResponse` indicates success.
            2.  If successful, parses the response to extract image URL, direct image data (if provided), and any available metadata like format or dimensions.
            3.  Handles cases where image might be a URL or base64 encoded data.
            4.  Returns an object with these details. If not successful or image details are not found, returns null or an error indicator.
*   **Usage Context**: These functions will be embedded into N8N Function nodes within the main workflow and adapter sub-workflows.

### 4.2 N8N Workflows (`workflows/`)

#### 4.2.1 Sub-Workflow: `ai_service_flux_lora_adapter.n8n.json`

*   **Purpose**: Acts as an adapter for a specific AI image generation service that supports Flux LoRA models. Encapsulates API call logic, parameter mapping, and authentication specific to this service, promoting adaptability (REQ-IL-006, REQ-IL-005).
*   **Trigger**: Called by an "Execute Workflow" node from a parent workflow (e.g., `ai_image_generation_workflow`).
*   **Input Data Structure (from parent workflow)**:
    json
    {
      "prompt": "string",
      "negative_prompt": "string (optional)",
      "model_identifier": "string (Flux LoRA model ID specific to AI service)",
      "resolution": "string (e.g., '1024x1024')",
      "aspect_ratio": "string (e.g., '1:1')",
      "seed": "number (optional)",
      "inference_steps": "number (optional)",
      "cfg_scale": "number (optional)",
      "api_credential_name": "string (N8N credential name for this AI service)",
      "correlationId": "string",
      "ai_service_base_url": "string (e.g., AI_SERVICE_FLUX_LORA_API_BASE_URL from env)"
    }
    
*   **Output Data Structure (to parent workflow)**:
    *   **Success Case**:
        json
        {
          "status": "success",
          "imageUrl": "string (URL of the generated image, or null if data is direct)",
          "imageData": "string (base64 encoded image, or null if URL is provided)",
          "contentType": "string (e.g., 'image/png')",
          "metadata": { /* any relevant metadata from AI service */ }
        }
        
    *   **Error Case**:
        json
        {
          "status": "error",
          "errorCode": "string (AI service error code or internal adapter error)",
          "errorMessage": "string (description of the error)"
        }
        
*   **Key Nodes and Logic**:
    1.  **Start Node**:
        *   **Type**: Start
        *   **Purpose**: Entry point of the sub-workflow. Receives input data.
    2.  **Log Request Received Node**:
        *   **Type**: Function
        *   **Purpose**: Logs the reception of the request using `logging_helpers.logInfo`.
        *   **JavaScript**:
            javascript
            const logging = {/* logging_helpers.js content */};
            const wfInstance = $execution;
            const nodeName = $currentNode.name;
            const correlationId = items[0].json.correlationId;
            const inputData = items[0].json;
            logging.logInfo(wfInstance, nodeName, correlationId, "Flux LoRA Adapter: Request received", { input: inputData });
            return items;
            
    3.  **Parameter Mapping Node**:
        *   **Type**: Function
        *   **Purpose**: Maps the standardized input parameters to the specific request format required by the Flux LoRA AI service API.
        *   **JavaScript**:
            javascript
            // Example - actual mapping depends on the AI service API
            const input = items[0].json;
            const aiServicePayload = {
              text_prompt: input.prompt,
              neg_prompt: input.negative_prompt,
              model: input.model_identifier,
              width: parseInt(input.resolution.split('x')[0]),
              height: parseInt(input.resolution.split('x')[1]),
              // ... map other parameters like seed, steps, cfg_scale
            };
            // Add logging for mapped payload (excluding sensitive parts if any)
            return [{ json: { aiServicePayload, originalInput: input } }];
            
    4.  **Call Flux LoRA AI Service Node**:
        *   **Type**: HTTP Request
        *   **Purpose**: Makes the API call to the external Flux LoRA AI service (REQ-IL-005).
        *   **Configuration**:
            *   **URL**: `{{ $json.originalInput.ai_service_base_url }}/generate` (or specific endpoint)
            *   **Method**: POST
            *   **Authentication**: Generic Credential Type -> Header Auth (or as required by AI service). Credential selected via `{{ $json.originalInput.api_credential_name }}`.
            *   **Body Type**: JSON
            *   **JSON Body**: `{{ JSON.stringify($json.aiServicePayload) }}`
            *   **Options**:
                *   `Send / Receive Timeout`: Configurable (e.g., 120000 ms for long generations).
                *   `SSL/TLS Verification`: Enabled (REQ-IL-007).
        *   **Error Handling**: "Continue on Fail" might be enabled if custom error processing is done in the next node, otherwise errors propagate to the sub-workflow's error output.
    5.  **Process AI Service Response Node**:
        *   **Type**: Function
        *   **Purpose**: Processes the response from the AI service. Extracts image URL/data and any error information. Formats this into a standardized response structure for the parent workflow.
        *   **JavaScript**:
            javascript
            const logging = {/* logging_helpers.js content */};
            const wfInstance = $execution;
            const nodeName = $currentNode.name;
            const inputData = items[0].json; // Contains response from HTTP Request & originalInput
            const correlationId = inputData.originalInput.correlationId;

            if (inputData.response && inputData.response.statusCode >= 200 && inputData.response.statusCode < 300) {
                const aiResponse = inputData.response.body; // Assuming body is parsed JSON
                // Example: extract image URL or base64 data
                const imageUrl = aiResponse.images && aiResponse.images[0] ? aiResponse.images[0].url : null;
                const imageData = aiResponse.images && aiResponse.images[0] ? aiResponse.images[0].base64 : null;
                const contentType = imageUrl ? 'image/url_reference' : (imageData ? 'image/png_base64' : 'unknown'); // Adjust based on actual AI response

                const successOutput = {
                    status: "success",
                    imageUrl: imageUrl,
                    imageData: imageData,
                    contentType: contentType,
                    metadata: aiResponse.metadata || {}
                };
                logging.logInfo(wfInstance, nodeName, correlationId, "Flux LoRA Adapter: AI Service call successful", { output: successOutput });
                return [{ json: successOutput }];
            } else {
                const errorOutput = {
                    status: "error",
                    errorCode: inputData.response ? inputData.response.statusCode : "ADAPTER_AI_CALL_FAILED",
                    errorMessage: inputData.response && inputData.response.body ? (inputData.response.body.error || JSON.stringify(inputData.response.body)) : "AI service call failed or timed out."
                };
                logging.logError(wfInstance, nodeName, correlationId, "Flux LoRA Adapter: AI Service call failed", { error: errorOutput, response: inputData.response });
                // To ensure this error is caught by the parent workflow's error handling via 'Continue on Fail' on Execute Workflow,
                // we might need to explicitly throw an error here or ensure the parent workflow checks the 'status' field.
                // For simplicity, returning the error structure. The parent will check 'status'.
                return [{ json: errorOutput }];
            }
            
    6.  **End Node (Success Output)**:
        *   **Type**: (Implicit) Output of "Process AI Service Response Node" if successful.
    7.  **End Node (Error Output - if specific error handling implemented within sub-workflow)**:
        *   **Type**: (Implicit) Output of "Process AI Service Response Node" if error.
*   **Logging**: Uses `logging_helpers.js` functions within Function nodes to log key steps and errors with `correlationId`.
*   **Security**: Uses N8N credentials for AI service API keys. All communication uses HTTPS (REQ-IL-007).

#### 4.2.2 Main Workflow: `ai_image_generation_workflow.n8n.json`

*   **Purpose**: Main N8N workflow to reliably and asynchronously process AI image generation requests from Odoo, integrate with AI services via adapters, and return results to Odoo (REQ-AIGS-001, REQ-IL-001, REQ-IL-009).
*   **Trigger**: Odoo Webhook (HTTP POST).
*   **Input Data Structure (from Odoo Webhook)**:
    json
    // As defined by Odoo service sending the request (REPO-IGOII-004)
    {
      "prompt": "string",
      "negative_prompt": "string (optional)",
      "resolution": "string (e.g., '1024x1024')",
      "aspect_ratio": "string (e.g., '1:1')",
      "seed": "number (optional)",
      "inference_steps": "number (optional)",
      "cfg_scale": "number (optional)",
      "model_preference": "string (e.g., 'Flux_v1', 'General_Creative')", // Used to select adapter/model
      "campaign_id": "string (optional UUID)",
      "user_id": "string (Odoo user ID)",
      "influencer_profile_id": "string (UUID)",
      "correlation_id": "string (UUID, generated by Odoo)"
      // Other params as defined by REQ-AIGS-004
    }
    
*   **Output Data Structure (to Odoo Callback API - REPO-IGOII-004)**:
    *   Payload constructed by `data_transformation_helpers.formatOdooCallbackPayload`.
    *   **Success Case**:
        json
        {
          "correlationId": "string",
          "status": "success",
          "imageUrl": "string (optional)",
          "imageData": "string (optional, base64)",
          "contentType": "string",
          "metadata": { /* ... */ }
        }
        
    *   **Error Case**:
        json
        {
          "correlationId": "string",
          "status": "error",
          "errorCode": "string",
          "errorMessage": "string"
        }
        
*   **Key Nodes and Logic**:
    1.  **Odoo Webhook Trigger Node**:
        *   **Type**: Webhook
        *   **Purpose**: Receives image generation requests from Odoo (REQ-AIGS-001).
        *   **Configuration**:
            *   **Path**: `/influencegen/ai/image_generate` (configurable via environment variable `N8N_WEBHOOK_PATH_AI_IMAGE` if desired)
            *   **HTTP Method**: POST
            *   **Authentication**: Generic Credential Type -> Header Auth (using a shared secret/API key stored as N8N credential, name e.g., `N8N_WEBHOOK_AUTH_ODOO`). Odoo must send this header.
            *   **Response Mode**: `Respond when workflow finishes` (or `On Received` if Odoo expects immediate ack and callback handles result). Given async nature, `On Received` with a simple ACK (e.g., `{"status": "received", "correlationId": "..."}`) is better, and the actual result is sent via OdooCallbackNode. Let's assume `On Received` with ACK.
    2.  **Initial Log & Correlation ID Node**:
        *   **Type**: Function
        *   **Purpose**: Logs reception, extracts and validates `correlationId`.
        *   **JavaScript**:
            javascript
            const logging = {/* logging_helpers.js content */};
            const wfInstance = $execution;
            const nodeName = $currentNode.name;
            const body = items[0].json.body; // Webhook body

            if (!body.correlation_id) {
                logging.logError(wfInstance, nodeName, null, "Main Workflow: Missing correlation_id in Odoo request.", { requestBody: body });
                // Optionally, could send an immediate error response here if Webhook response mode allows
                throw new Error("Missing correlation_id");
            }
            const correlationId = body.correlation_id;
            items[0].json.correlationId = correlationId; // Ensure it's top-level for easy access

            logging.logInfo(wfInstance, nodeName, correlationId, "Main Workflow: AI Image Generation request received from Odoo.", { odooPayload: body });
            return items;
            
    3.  **Input Validation & Preparation Node**:
        *   **Type**: Function
        *   **Purpose**: Validates essential inputs from Odoo (e.g., presence of prompt, model_preference). Prepares data for the AI service adapter using `data_transformation_helpers.prepareAIServiceRequest`.
        *   **JavaScript**:
            javascript
            const transform = {/* data_transformation_helpers.js content */};
            const logging = {/* logging_helpers.js content */};
            const wfInstance = $execution;
            const nodeName = $currentNode.name;
            const odooPayload = items[0].json.body;
            const correlationId = items[0].json.correlationId;

            if (!odooPayload.prompt || !odooPayload.model_preference) {
                logging.logError(wfInstance, nodeName, correlationId, "Main Workflow: Missing prompt or model_preference.", { payload: odooPayload });
                items[0].json.error = {
                    status: "error",
                    errorCode: "INPUT_VALIDATION_ERROR",
                    errorMessage: "Missing required fields: prompt or model_preference."
                };
                // This error will be routed to the error handling branch
                return items;
            }

            // Example AI Service Config determination (can be more dynamic)
            const aiServiceConfig = {
                model_type: odooPayload.model_preference.includes('Flux') ? 'FluxLoRA' : 'Other', // Simplified logic
                // This could come from an N8N 'Variables' node or another lookup based on model_preference
                api_credential_name: $env.AI_SERVICE_FLUX_LORA_API_KEY_CREDENTIAL_NAME, // Example
                ai_service_base_url: $env.AI_SERVICE_FLUX_LORA_API_BASE_URL, // Example
                adapter_workflow_id: $env.AI_SERVICE_ADAPTER_SUBWORKFLOW_ID_FLUX_LORA // Example
            };

            const adapterInput = transform.prepareAIServiceRequest(odooPayload, aiServiceConfig);
            adapterInput.correlationId = correlationId; // Ensure correlationId is passed to sub-workflow
            adapterInput.api_credential_name = aiServiceConfig.api_credential_name;
            adapterInput.ai_service_base_url = aiServiceConfig.ai_service_base_url;
            // Pass the specific adapter workflow ID
            items[0].json.adapterWorkflowId = aiServiceConfig.adapter_workflow_id;
            items[0].json.adapterInput = adapterInput;
            items[0].json.originalOdooRequest = odooPayload; // Keep for callback formatting

            logging.logInfo(wfInstance, nodeName, correlationId, "Main Workflow: Input validated and prepared for AI adapter.", { adapterInput: adapterInput });
            return items;
            
    4.  **Error Route Check (After Input Validation)**:
        *   **Type**: IF Node
        *   **Purpose**: Checks if `items[0].json.error` exists from the previous node.
        *   **Condition**: `{{ $json.error != null }}`
        *   **Output**: True (to Error Handling Branch), False (to Execute AI Service Adapter Node)
    5.  **Execute AI Service Adapter Node**:
        *   **Type**: Execute Workflow
        *   **Purpose**: Calls the appropriate AI service adapter sub-workflow (REQ-IL-006).
        *   **Configuration**:
            *   **Workflow ID**: `{{ $json.adapterWorkflowId }}` (Dynamically set based on `model_preference`)
            *   **Input Data**: `{{ $json.adapterInput }}`
            *   **Options**:
                *   `Wait for Sub-Workflow`: True.
                *   `Retry on Fail`: Enabled.
                    *   `Retries`: 3 (Configurable via $env.N8N_ADAPTER_CALL_RETRIES).
                    *   `Retry Interval`: e.g., 60000 ms (1 min), with exponential backoff option enabled. (REQ-IL-009). This handles transient errors from the adapter (which itself might retry AI service calls).
        *   **Error Handling**: If this node fails after retries, workflow execution goes to its error output, which should be connected to the main Error Handling Branch.
    6.  **Process Adapter Response Node**:
        *   **Type**: Function
        *   **Purpose**: Processes the standardized response from the adapter sub-workflow. Prepares the payload for the Odoo callback using `data_transformation_helpers.formatOdooCallbackPayload`.
        *   **JavaScript**:
            javascript
            const transform = {/* data_transformation_helpers.js content */};
            const logging = {/* logging_helpers.js content */};
            const wfInstance = $execution;
            const nodeName = $currentNode.name;

            const adapterResponse = items[0].json; // Output from Execute Workflow
            const originalOdooRequest = items[0].json.originalOdooRequest; // Passed along
            const correlationId = items[0].json.correlationId; // Passed along

            const isSuccess = adapterResponse.status === "success";
            const odooCallbackPayload = transform.formatOdooCallbackPayload(adapterResponse, originalOdooRequest, isSuccess);
            odooCallbackPayload.correlationId = correlationId; // Ensure this is always present

            if(isSuccess) {
                logging.logInfo(wfInstance, nodeName, correlationId, "Main Workflow: AI Service Adapter successful. Prepared Odoo callback.", { callbackPayload: odooCallbackPayload });
            } else {
                logging.logError(wfInstance, nodeName, correlationId, "Main Workflow: AI Service Adapter failed. Prepared Odoo error callback.", { errorPayload: odooCallbackPayload, adapterResponse: adapterResponse });
            }
            items[0].json.odooCallbackPayload = odooCallbackPayload;
            return items;
            
    7.  **Odoo Callback Node**:
        *   **Type**: HTTP Request
        *   **Purpose**: Sends the result (success or formatted error) back to the Odoo callback API endpoint (REQ-IL-003).
        *   **Configuration**:
            *   **URL**: `{{ $env.ODOO_CALLBACK_BASE_URL + $env.ODOO_CALLBACK_IMAGE_RESULT_ENDPOINT }}`
            *   **Method**: POST
            *   **Authentication**: Generic Credential Type -> Header Auth (using N8N credential named e.g., `{{ $env.ODOO_CALLBACK_API_KEY_CREDENTIAL_NAME }}`).
            *   **Body Type**: JSON
            *   **JSON Body**: `{{ JSON.stringify($json.odooCallbackPayload) }}`
            *   **Options**:
                *   `Send / Receive Timeout`: Configurable (e.g., 30000 ms).
                *   `SSL/TLS Verification`: Enabled (REQ-IL-007).
                *   `Retry on Fail`: Enabled (e.g., 2 retries, 30s interval) for transient Odoo callback issues. (REQ-IL-009).
        *   **Error Handling**: If this node fails after retries, workflow execution goes to its error output, connected to a final logging node.
    8.  **Log Odoo Callback Success Node**:
        *   **Type**: Function
        *   **Purpose**: Logs successful callback to Odoo.
        *   **JavaScript**:
            javascript
            const logging = {/* logging_helpers.js content */};
            const wfInstance = $execution;
            const nodeName = $currentNode.name;
            const correlationId = items[0].json.correlationId;
            logging.logInfo(wfInstance, nodeName, correlationId, "Main Workflow: Successfully sent callback to Odoo.", { response: items[0].json.response });
            return items;
            
    9.  **Error Handling Branch (Merge Point for Errors)**:
        *   This branch starts from the error output of "Execute AI Service Adapter Node", the "True" output of "Error Route Check", and potentially the error output of "Odoo Webhook Trigger Node" (if authentication fails before Initial Log node).
        *   **Error Formatting Node (if not already formatted by Input Validation)**:
            *   **Type**: Function
            *   **Purpose**: If the error comes from Execute AI Service Adapter or other unhandled exceptions, format a standard error payload for Odoo.
            *   **JavaScript**:
                javascript
                const transform = {/* data_transformation_helpers.js content */};
                const logging = {/* logging_helpers.js content */};
                const wfInstance = $execution;
                const nodeName = $currentNode.name;

                const errorData = items[0].json; // Contains error information
                const originalOdooRequest = items[0].json.originalOdooRequest || items[0].json.body || {}; // Attempt to get original for correlationId
                const correlationId = items[0].json.correlationId || originalOdooRequest.correlation_id || "UNKNOWN_CORRELATION_ID";

                let errorMessage = "An unexpected error occurred during AI image generation.";
                let errorCode = "N8N_WORKFLOW_ERROR";

                if(errorData.error && errorData.error.message) { // error from Input Validation
                    errorMessage = errorData.error.errorMessage;
                    errorCode = errorData.error.errorCode;
                } else if (errorData.status === 'error') { // error from adapter passed through
                     errorMessage = errorData.errorMessage;
                     errorCode = errorData.errorCode;
                } else if (errorData.message) { // Generic N8N error
                    errorMessage = errorData.message;
                }

                const odooErrorPayload = transform.formatOdooCallbackPayload(
                    { errorCode: errorCode, errorMessage: errorMessage },
                    originalOdooRequest,
                    false
                );
                odooErrorPayload.correlationId = correlationId;

                logging.logError(wfInstance, nodeName, correlationId, `Main Workflow: Error processing request - ${errorMessage}`, { error: errorData, odooPayload: odooErrorPayload });
                items[0].json.odooCallbackPayload = odooErrorPayload;
                return items;
                
        *   Connects to the **Odoo Callback Node** to send the error details to Odoo.
    10. **Final Log Failure Node (after Odoo Callback Node error output)**:
        *   **Type**: Function
        *   **Purpose**: Logs critical failure if even the Odoo error callback fails.
        *   **JavaScript**:
            javascript
            const logging = {/* logging_helpers.js content */};
            const wfInstance = $execution;
            const nodeName = $currentNode.name;
            const correlationId = items[0].json.correlationId || "UNKNOWN_CORRELATION_ID";
            logging.logError(wfInstance, nodeName, correlationId, "Main Workflow: CRITICAL - Failed to send callback to Odoo after processing error.", { errorDetails: items[0].json });
            return items; // End workflow
            
*   **Workflow Structure**:
    *   Webhook Trigger -> Initial Log & Correlation ID -> Input Validation & Prep -> Error Route Check
    *   Error Route Check (False) -> Execute AI Adapter -> Process Adapter Response -> Odoo Callback -> Log Odoo Callback Success
    *   Error Route Check (True) -> Error Formatting -> Odoo Callback -> Log Odoo Callback Success (even for error callback)
    *   Error Output of Execute AI Adapter -> Error Formatting -> Odoo Callback -> Log Odoo Callback Success
    *   Error Output of Odoo Callback -> Final Log Failure
*   **Logging**: Extensive logging at each significant step using `logging_helpers.js`, including `correlationId` (REQ-ATEL-010).
*   **Security**: Webhook authentication, HTTPS for all external calls (AI Service via Adapter, Odoo Callback) (REQ-IL-007). Credentials managed by N8N.
*   **Retry Logic**: Implemented on "Execute AI Service Adapter Node" and "Odoo Callback Node" (REQ-IL-009).

## 5. Data Structures (Payloads Summary)

Detailed payload structures are implicitly defined within the node descriptions above. Key aspects:
*   **Odoo to N8N**: JSON, must include `correlation_id`, prompt, and all necessary generation parameters.
*   **N8N (Main) to N8N (Adapter)**: Standardized JSON, includes `correlationId` and all parameters needed by the specific AI service.
*   **N8N (Adapter) to AI Service**: Service-specific JSON.
*   **AI Service to N8N (Adapter)**: Service-specific JSON response.
*   **N8N (Adapter) to N8N (Main)**: Standardized JSON for success (image details) or error.
*   **N8N to Odoo Callback**: JSON, includes `correlationId`, status ("success"/"error"), and relevant data (image details or error message/code).

## 6. Interfaces

*   **Odoo -> N8N AI Image Generation Webhook**:
    *   **Endpoint**: `{{ $env.N8N_WEBHOOK_BASE_URL }}/webhook/{{ $env.N8N_WEBHOOK_PATH_AI_IMAGE }}` (e.g., `https://n8n.example.com/webhook/influencegen/ai/image_generate`)
    *   **Method**: POST
    *   **Authentication**: Header-based API Key/Bearer Token (managed via N8N Webhook node auth setting).
    *   **Request Body**: JSON (as per `ai_image_generation_workflow` input).
    *   **Response Body (Immediate ACK)**: `{"status": "received", "message": "AI image generation request queued.", "correlationId": "..."}`
*   **N8N -> Odoo Image Result Callback API**:
    *   **Endpoint**: `{{ $env.ODOO_CALLBACK_BASE_URL + $env.ODOO_CALLBACK_IMAGE_RESULT_ENDPOINT }}` (e.g., `https://odoo.example.com/api/influencegen/image_result_callback`)
    *   **Method**: POST
    *   **Authentication**: Header-based API Key/Bearer Token (N8N uses credential `{{ $env.ODOO_CALLBACK_API_KEY_CREDENTIAL_NAME }}`).
    *   **Request Body**: JSON (as per `ai_image_generation_workflow` output to Odoo).
    *   **Response Body (from Odoo)**: Expected `{"status": "ok"}` or an error object if Odoo callback processing fails.
*   **N8N (Adapter) -> Flux LoRA AI Service API**:
    *   **Endpoint**: `{{ $env.AI_SERVICE_FLUX_LORA_API_BASE_URL }}/generate` (or service-specific endpoint)
    *   **Method**: POST
    *   **Authentication**: Service-specific (e.g., API Key in header, managed by N8N credential `{{ $env.AI_SERVICE_FLUX_LORA_API_KEY_CREDENTIAL_NAME }}`).
    *   **Request Body**: JSON (specific to Flux LoRA service).
    *   **Response Body**: JSON (specific from Flux LoRA service, containing image data/URL or error).

## 7. Configuration Management (REQ-DDSI-005 related)

N8N workflows will utilize the following environment variables and N8N credentials for configuration:

*   **Environment Variables (accessible in N8N via `$env` in Function nodes or expressions)**:
    *   `N8N_ENCRYPTION_KEY`: For N8N internal credential encryption. (N8N System Level)
    *   `N8N_WEBHOOK_BASE_URL`: Base URL for N8N webhooks if not default.
    *   `N8N_WEBHOOK_PATH_AI_IMAGE`: Specific path for the AI image generation webhook (e.g., `influencegen/ai/image_generate`).
    *   `ODOO_CALLBACK_BASE_URL`: Base URL for Odoo callback API (e.g., `https://odoo.influencegen.com/api/influencegen`).
    *   `ODOO_CALLBACK_IMAGE_RESULT_ENDPOINT`: Specific path for Odoo image result callback (e.g., `image_result_callback`).
    *   `AI_SERVICE_FLUX_LORA_API_BASE_URL`: Base URL for the Flux LoRA AI service.
    *   `AI_SERVICE_ADAPTER_SUBWORKFLOW_ID_FLUX_LORA`: N8N Workflow ID of the `ai_service_flux_lora_adapter.n8n.json` sub-workflow.
    *   `N8N_ADAPTER_CALL_RETRIES`: Number of retries for Execute Workflow node (e.g., "3").
    *   `N8N_ODOO_CALLBACK_RETRIES`: Number of retries for Odoo callback HTTP Request node (e.g., "2").
    *   `N8N_LOG_LEVEL`: Default logging level for helper functions (e.g., "INFO", "DEBUG").
    *   `CENTRAL_LOGGING_WEBHOOK_URL` (Optional): If logs are pushed to an external aggregator webhook directly from Function nodes.
    *   `N8N_EXECUTIONS_DATA_PRUNE_MAX_AGE`: For N8N's internal execution log retention (e.g., "720h" for 30 days).
*   **N8N Credentials**:
    *   `N8N_WEBHOOK_AUTH_ODOO`: Header Auth credential for securing the Odoo->N8N webhook. Contains the shared secret/API key.
    *   `ODOO_CALLBACK_API_KEY_CREDENTIAL_NAME`: Header Auth credential for N8N->Odoo callback API. Contains the API key Odoo expects. (Value would be e.g., `odoo-callback-api-key`)
    *   `AI_SERVICE_FLUX_LORA_API_KEY_CREDENTIAL_NAME`: Credential (e.g., API Key, Bearer Token) for authenticating with the Flux LoRA AI service. (Value would be e.g., `flux-lora-service-api-key`)
    *   (Future AI Services): Similar credential names for other AI service adapters.

## 8. Deployment Considerations

*   N8N workflows (`.n8n.json` files) will be version-controlled (REQ-DDSI-002).
*   Deployment to different N8N environments (Dev, Staging, Prod - REQ-DDSI-005) will involve importing these workflow JSON files and configuring the necessary environment variables and N8N credentials for each environment.
*   Helper JavaScript code will be embedded within the Function nodes of the N8N workflow JSONs. While they are designed as separate `.js` files for clarity in this SDS and development, N8N typically embeds this code directly or allows referencing from its user data folder if N8N is self-hosted and configured for it. For simplicity of deployment via JSON import/export, embedding is assumed.
*   Secure communication (HTTPS) for all external endpoints (Odoo, AI Service) is mandatory (REQ-IL-007).

---
# AI Instructions for Code Generation

## General Instructions for AI:

1.  You are generating components for an N8N-based orchestration layer.
2.  The primary language for custom logic within N8N Function nodes is JavaScript (ES2022).
3.  N8N workflows are defined in JSON format.
4.  Adhere strictly to the provided SDS for component names, function signatures, logic descriptions, and N8N node configurations.
5.  Implement comprehensive error handling and structured JSON logging as specified.
6.  Use N8N expressions (`{{ }}`) for accessing environment variables (`$env.VARIABLE_NAME`), N8N credentials (`$credentials.CREDENTIAL_NAME.PROPERTY`), and data from previous nodes (`$json.PROPERTY`, `items[0].json.PROPERTY`).
7.  Ensure all external HTTP communications (to AI services, to Odoo callback) use HTTPS.
8.  Pay close attention to the `correlationId` and ensure it's passed through workflows and included in logs for distributed tracing.

## AI Instructions for Specific Files:

### 1. For `n8n_workflows/utils/logging_helpers.js`

*   **Instruction**: "Generate the JavaScript code for the `logging_helpers.js` utility module as described in the SDS. This module will provide functions for structured JSON logging within N8N Function nodes. Implement `formatLogEntry`, `logInfo`, and `logError` functions. Ensure `formatLogEntry` creates a JSON object including UTC timestamp, level, message, executionId, workflowId, nodeName, correlationId, and custom context. `logInfo` and `logError` should use `formatLogEntry` and output the log (e.g., `console.log(JSON.stringify(logEntry))`)."
*   **Context**: Provide the SDS section for `logging_helpers.js`.

### 2. For `n8n_workflows/utils/data_transformation_helpers.js`

*   **Instruction**: "Generate the JavaScript code for the `data_transformation_helpers.js` utility module as described in the SDS. Implement `prepareAIServiceRequest`, `formatOdooCallbackPayload`, and `extractImageDetails` functions. `prepareAIServiceRequest` should map Odoo's input to a standardized format for AI adapters. `formatOdooCallbackPayload` should create the JSON payload for Odoo callbacks (success/error), including the `correlationId`. `extractImageDetails` should parse an AI service adapter's response to get image URL/data."
*   **Context**: Provide the SDS section for `data_transformation_helpers.js` and examples of input/output JSON structures if helpful.

### 3. For `n8n_workflows/workflows/sub_workflows/ai_service_flux_lora_adapter.n8n.json`

*   **Instruction**: "Generate the N8N workflow JSON for the `ai_service_flux_lora_adapter.n8n.json` sub-workflow as detailed in the SDS.
    *   **Trigger**: Start Node (receives input from parent).
    *   **Nodes**:
        1.  **Log Request Received Node (Function Node)**: Use `logging_helpers.logInfo`.
        2.  **Parameter Mapping Node (Function Node)**: Map standardized input to Flux LoRA service specific format (provide example mapping if complex, or instruct AI to create a plausible one).
        3.  **Call Flux LoRA AI Service Node (HTTP Request Node)**: Configure URL (from input `ai_service_base_url`), method (POST), authentication (using input `api_credential_name`), JSON body (from Parameter Mapping Node), timeout, and HTTPS.
        4.  **Process AI Service Response Node (Function Node)**: Parse AI service response. If successful, extract image URL/data and format a success output. If error, format an error output. Use `logging_helpers` for logging success/failure. Output fields should be `status`, `imageUrl`, `imageData`, `contentType`, `metadata` for success; `status`, `errorCode`, `errorMessage` for error.
    *   **Connections**: Define logical flow between nodes.
    *   **Error Handling**: Errors from the HTTP Request node or Function nodes should result in the 'error' output structure being passed to the parent workflow.
    *   **Logging**: Integrate logging using `logging_helpers.js` snippets within Function nodes.
    *   **Input/Output**: Define expected input structure (as per SDS) and the standardized output structure (success/error for parent workflow).
    *   Assume helper JavaScript code (`logging_helpers.js`) is embedded/available in Function nodes."
*   **Context**: Provide the SDS section for `ai_service_flux_lora_adapter.n8n.json`, including input/output structures.

### 4. For `n8n_workflows/workflows/ai_image_generation_workflow.n8n.json`

*   **Instruction**: "Generate the N8N workflow JSON for the main `ai_image_generation_workflow.n8n.json` as detailed in the SDS.
    *   **Trigger**: **Odoo Webhook Trigger Node**. Configure path (e.g., `/influencegen/ai/image_generate`), method (POST), Header Auth (using N8N credential `N8N_WEBHOOK_AUTH_ODOO`), and response mode (`On Received` with an ACK JSON: `{\"status\": \"received\", \"message\": \"AI image generation request queued.\", \"correlationId\": \"{{$json.body.correlation_id}}\"}`).
    *   **Nodes**:
        1.  **Initial Log & Correlation ID Node (Function Node)**: Extract `correlation_id` from webhook body. Log request reception using `logging_helpers.logInfo`. Store `correlationId` in item JSON for later use. Throw error if `correlation_id` is missing.
        2.  **Input Validation & Preparation Node (Function Node)**: Validate required fields (prompt, model_preference). Use `data_transformation_helpers.prepareAIServiceRequest` to prepare input for the adapter. Determine `adapterWorkflowId` based on `model_preference` (e.g., if `model_preference` contains 'Flux', use `$env.AI_SERVICE_ADAPTER_SUBWORKFLOW_ID_FLUX_LORA`). Log preparation. If validation fails, set an `error` object in the item JSON.
        3.  **Error Route Check Node (IF Node)**: Condition: `{{ $json.error != null }}`. True output to error handling branch, False output to Execute AI Adapter.
        4.  **Execute AI Service Adapter Node (Execute Workflow Node)**: Call sub-workflow using `{{ $json.adapterWorkflowId }}`. Pass `{{ $json.adapterInput }}`. Configure `Wait for Sub-Workflow: True`. Implement **Retry on Fail** (e.g., 3 retries, 60s interval, exponential backoff, using `$env.N8N_ADAPTER_CALL_RETRIES`). Connect error output to the main error handling branch.
        5.  **Process Adapter Response Node (Function Node)**: Use `data_transformation_helpers.formatOdooCallbackPayload` to prepare the payload for Odoo based on the adapter's response (success or error). Log outcome.
        6.  **Odoo Callback Node (HTTP Request Node)**: POST to Odoo callback URL (`{{ $env.ODOO_CALLBACK_BASE_URL + $env.ODOO_CALLBACK_IMAGE_RESULT_ENDPOINT }}`). Use Header Auth (credential `{{ $env.ODOO_CALLBACK_API_KEY_CREDENTIAL_NAME }}`). Body is `{{ $json.odooCallbackPayload }}`. Implement **Retry on Fail** (e.g., 2 retries, 30s interval, using `$env.N8N_ODOO_CALLBACK_RETRIES`). Connect error output to Final Log Failure Node.
        7.  **Log Odoo Callback Success Node (Function Node)**: Log successful callback using `logging_helpers.logInfo`.
        8.  **Error Formatting Node (Function Node - in error branch)**: If error originated before `Process Adapter Response`, use this node to create a standard error payload for Odoo using `data_transformation_helpers.formatOdooCallbackPayload` with `isSuccess=false`. Log the error using `logging_helpers.logError`. This node receives input from the "True" output of "Error Route Check" and the error output of "Execute AI Service Adapter Node". Its output connects to "Odoo Callback Node".
        9.  **Final Log Failure Node (Function Node)**: If "Odoo Callback Node" fails after retries (even when sending an error), log this critical failure using `logging_helpers.logError`.
    *   **Connections**: Define logical flow, including main success path and error handling branches that eventually merge back to call the Odoo Callback Node (to inform Odoo of the error).
    *   **Error Handling**: Implement a robust error handling branch.
    *   **Logging**: Integrate extensive logging using `logging_helpers.js` snippets.
    *   **Configuration**: Refer to environment variables for URLs, endpoint paths, credential names, and retry counts.
    *   Assume helper JavaScript code (`logging_helpers.js`, `data_transformation_helpers.js`) is embedded/available."
*   **Context**: Provide the SDS section for `ai_image_generation_workflow.n8n.json`, including input/output structures and workflow logic diagram if available. Emphasize the need for clear separation of success and error paths, eventually leading to the Odoo Callback node.