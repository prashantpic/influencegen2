# Software Design Specification: InfluenceGen.N8N.AI.ImageGeneration.Workflow

## 1. Introduction

### 1.1 Purpose
This document provides a detailed software design specification for the `InfluenceGen.N8N.AI.ImageGeneration.Workflow` repository. This repository is responsible for defining and managing the N8N workflow(s) that orchestrate the AI image generation process. It acts as an intermediary between the Odoo platform and external AI image generation services. The specifications herein will guide the development and configuration of these N8N workflows and their associated helper scripts.

### 1.2 Scope
The scope of this SDS covers:
*   The main N8N workflow (`main_ai_image_generation_workflow.json`) for handling AI image generation requests.
*   JavaScript helper modules (`lib/*.js`) used within N8N Function nodes for tasks like API adaptation, payload handling, error processing, and custom logging.
*   Configuration for JavaScript development tooling (`package.json`).

This SDS focuses on the N8N components and their interactions as defined by the repository description and mapped requirements. It assumes that Odoo provides necessary webhook triggers and callback API endpoints, and that external AI services offer stable REST APIs.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **N8N**: A free and open fair-code distributed workflow automation tool.
*   **AI**: Artificial Intelligence.
*   **API**: Application Programming Interface.
*   **Flux LoRA**: A specific type of AI model architecture.
*   **JSON**: JavaScript Object Notation.
*   **ETL**: Extract, Transform, Load. (Mentioned in general requirements, but this repo focuses on orchestration).
*   **SDS**: Software Design Specification.
*   **UI**: User Interface.
*   **ORM**: Object-Relational Mapper.
*   **HTTP**: Hypertext Transfer Protocol.
*   **HTTPS**: HTTP Secure.
*   **TLS**: Transport Layer Security.
*   **CRUD**: Create, Read, Update, Delete.
*   **ComfyUI / StabilityAI**: Examples of AI image generation services/platforms.
*   **ESLint**: A tool for identifying and reporting on patterns found in ECMAScript/JavaScript code.
*   **Prettier**: An opinionated code formatter.

### 1.4 References
*   InfluenceGen System Requirements Specification (SRS) document (specifically sections related to REQ-IL-XXX, REQ-AIGS-XXX, REQ-ATEL-XXX, REQ-DDSI-XXX).
*   InfluenceGen Architecture Design Document.
*   N8N Documentation (Version 1.45.1 or latest stable).
*   API documentation for the selected AI image generation service(s).
*   Odoo API documentation (for callback endpoint).

## 2. System Overview
The `InfluenceGen.N8N.AI.ImageGeneration.Workflow` repository provides the N8N workflows that act as the orchestration engine for AI image generation. It listens for requests from Odoo, communicates with external AI services, processes responses, and sends results back to Odoo. This system is designed for asynchronous operation, adaptability to various AI backends, and robust error handling.

**Key functionalities:**
*   Receive and parse AI image generation requests from Odoo via webhook.
*   Adapt requests to the specific format of the target AI service API.
*   Securely call the AI service API, handling authentication.
*   Process successful image generation responses (extracting image data/URL).
*   Handle errors from the AI service, implementing retry logic for transient issues.
*   Format results (success or error) for Odoo.
*   Securely call the Odoo callback API to deliver results.
*   Log critical steps and errors for traceability.

## 3. Design Considerations

### 3.1 Architectural Style
The primary N8N workflow (`main_ai_image_generation_workflow.json`) follows a **Pipes and Filters** architectural style, where data flows through a series of processing nodes. It also incorporates:
*   **Webhook Integration**: For receiving requests from Odoo.
*   **Asynchronous Task Processing**: The entire workflow is designed to be asynchronous from Odoo's perspective.
*   **Adapter Pattern**: Implemented via JavaScript helpers (`ai_service_adapter.js`) to support different AI service APIs with minimal workflow changes.

### 3.2 Technology Stack
*   **N8N Version**: 1.45.1 (or latest stable at time of implementation)
*   **Workflow Definition**: JSON (N8N's native format)
*   **Custom Logic (Function Nodes)**: JavaScript (ES2022 compatible with N8N's environment)
*   **Communication Protocols**: HTTP/HTTPS, RESTful APIs, Webhooks
*   **Development Tooling (for JS helpers)**: Node.js, NPM, ESLint, Prettier

### 3.3 Security
*   **Secure Communication**: All external communication (Odoo to N8N, N8N to AI service, N8N to Odoo callback) must use HTTPS/TLS (REQ-IL-007).
*   **Credential Management**: API keys and other sensitive credentials for AI services and the Odoo callback API will be stored and managed securely using N8N's built-in credential management system (N8N vault) (REQ-IL-008). No credentials will be hardcoded.
*   **Input Validation**: Incoming webhook payloads from Odoo will be validated (REQ-AIGS-001, `odoo_payload_handler.js`).
*   **N8N Instance Security**: Access to the N8N instance itself (UI, API) must be strictly controlled and audited as per organizational policies (REQ-IL-017).
*   **Sensitive Data Handling**: N8N workflows will be designed to minimize exposure of sensitive data in logs or intermediate steps (REQ-IL-017).

### 3.4 Error Handling and Resilience
*   **Retry Logic**: HTTP Request nodes calling external AI services will be configured with retry mechanisms (e.g., exponential backoff) for transient network errors or rate limits (REQ-IL-009).
*   **Error Normalization**: Errors from AI services and internal workflow errors will be processed and standardized by `error_processor.js` for consistent logging and reporting back to Odoo (REQ-IL-009).
*   **Dead Letter Queues (Conceptual)**: While N8N doesn't have native DLQs like message brokers, persistent failures will result in an error payload being sent to Odoo, and comprehensive logging. Odoo or the centralized logging system can then implement alerting for manual intervention.
*   **Failure Notifications**: Odoo will be notified of processing failures through the callback API.

### 3.5 Logging and Monitoring
*   **Structured Logging**: Custom logging within N8N Function nodes (`custom_logger.js`) will produce structured JSON logs (REQ-ATEL-010, REQ-ATEL-002 from SRS 9.1).
*   **Correlation IDs**: A correlation ID (e.g., `odoo_request_id`) will be passed from Odoo and included in all N8N logs and communications to facilitate tracing (REQ-ATEL-002 from SRS 9.1).
*   **Centralized Logging**: N8N execution logs and custom logs should be configured to be ingested by a centralized logging solution (REQ-ATEL-010, REQ-ATEL-004 from SRS 9.1).
*   **Key Events Logged**:
    *   Webhook received from Odoo (with sanitized payload summary).
    *   Request parameters parsed and validated.
    *   AI service API call initiated (endpoint, sanitized request summary).
    *   AI service API response received (status, sanitized response summary).
    *   Image processing (if any).
    *   Odoo callback API call initiated (endpoint, sanitized payload summary).
    *   Odoo callback API response received (status).
    *   Errors at any stage, including retry attempts.

### 3.6 Adaptability
*   The `ai_service_adapter.js` module is key to achieving adaptability for different AI service APIs (REQ-IL-006). New AI services can be supported by adding new formatting functions to this adapter and updating configuration if needed, without major changes to the main workflow structure.

## 4. Detailed Component Design

### 4.1 `main_ai_image_generation_workflow.json`
This file defines the primary N8N workflow.

*   **Name**: `InfluenceGen AI Image Generation Orchestrator`
*   **Trigger**: Webhook Node
    *   **Path**: `/webhook/influencegen/ai-image-generate` (configurable, to be secured)
    *   **HTTP Method**: POST
    *   **Authentication**: Recommended: Basic Auth or Header Auth (using N8N's webhook node authentication options). Credentials managed by Odoo.
    *   **Response Mode**: `Respond when workflow finishes` or `Respond immediately` (if Odoo doesn't need an immediate ack beyond HTTP 200 from the webhook itself). Given the async nature, "Respond immediately" after basic validation, and Odoo relies on the callback.
*   **Nodes and Logic Flow**:

    1.  **Start Node**: Default N8N start node.
    2.  **Webhook Trigger (`receiveOdooRequest`)**:
        *   Configuration: As defined above.
        *   Output: `{$json}` (entire incoming Odoo request payload).
    3.  **Function Node (`parseAndValidateRequest`)**:
        *   Purpose: Parses the incoming Odoo request, validates required fields, and extracts key parameters. Uses `odoo_payload_handler.js`.
        *   Inputs: `{$json}` from `receiveOdooRequest`.
        *   JavaScript Code:
            javascript
            // Assuming odoo_payload_handler.js content is available or injected
            // const odooHandler = require('./lib/odoo_payload_handler.js'); // For conceptual clarity
            // const logger = require('./lib/custom_logger.js'); // For conceptual clarity

            try {
                const odooRequest = items[0].json;
                // Call: logger.logEvent('INFO', 'Received Odoo Webhook', { requestId: odooRequest.request_id, triggerNode: 'receiveOdooRequest' });

                const parsedRequest = odoo_payload_handler.parseAndValidateOdooWebhook(odooRequest);
                if (parsedRequest.error) {
                    // Call: logger.logEvent('ERROR', 'Invalid Odoo Request', { error: parsedRequest.error, requestId: odooRequest.request_id });
                    // Potentially set data for an error path or use Error Trigger node
                    // For now, let's assume it throws, to be caught by an Error Trigger Node
                    throw new Error(parsedRequest.error.message);
                }
                // Call: logger.logEvent('INFO', 'Parsed and Validated Odoo Request', { requestId: parsedRequest.requestId, params: parsedRequest.params });
                return [{ json: parsedRequest }]; // Contains { requestId, params, aiServiceType, etc. }
            } catch (error) {
                // Call: logger.logEvent('ERROR', 'Error in parseAndValidateRequest', { error: error.message, stack: error.stack, input: items[0].json });
                // This error should be caught by a global Error Trigger node in N8N
                throw error; // Re-throw to trigger N8N's error handling / Error Trigger node
            }
            
        *   Outputs: Parsed and validated request object.
    4.  **Function Node (`adaptToAIService`)**:
        *   Purpose: Adapts the parsed Odoo request parameters to the specific API format of the target AI service. Uses `ai_service_adapter.js`.
        *   Inputs: Output from `parseAndValidateRequest`.
        *   JavaScript Code:
            javascript
            // const aiAdapter = require('./lib/ai_service_adapter.js');
            // const logger = require('./lib/custom_logger.js');

            try {
                const { requestId, params, aiServiceType, modelName } = items[0].json;
                const aiServiceApiPayload = ai_service_adapter.adaptToAIService(params, aiServiceType, modelName); // modelName might be part of params
                const endpoint = ai_service_adapter.getAIServiceEndpoint(aiServiceType, modelName); // modelName might be part of params

                // Call: logger.logEvent('INFO', 'Request Adapted for AI Service', { requestId, aiServiceType, endpoint });
                return [{ json: { requestId, endpoint, aiServiceApiPayload, aiServiceType } }];
            } catch (error) {
                // Call: logger.logEvent('ERROR', 'Error in adaptToAIService', { error: error.message, stack: error.stack, input: items[0].json });
                throw error;
            }
            
        *   Outputs: AI service endpoint, API payload, and service type.
    5.  **HTTP Request Node (`callAIService`)**:
        *   Purpose: Calls the external AI image generation service.
        *   Inputs: `endpoint`, `aiServiceApiPayload`, `aiServiceType` from `adaptToAIService`.
        *   Configuration:
            *   **Method**: POST (or as required by the AI service).
            *   **URL**: `{{ $json.endpoint }}`
            *   **Authentication**: Generic Credential Type (e.g., Header Auth, API Key Auth). N8N credentials will be selected here (e.g., `ComfyUICredentials`, `StabilityAICredentials`).
            *   **Body**: `{{ $json.aiServiceApiPayload }}` (Send as JSON or as required by AI service).
            *   **Headers**: Configured as needed, potentially using `ai_service_adapter.getAIServiceAuthHeaders` if complex.
            *   **Options -> Retry on Fail**: Enabled.
                *   Retries: 3 (configurable)
                *   Retry Interval: 5000ms (configurable, consider exponential backoff if N8N supports it directly or via a loop construct for more complex retry)
        *   Outputs: AI service API response.
    6.  **Function Node (`processAIServiceResponse`)**:
        *   Purpose: Processes the response from the AI service. Distinguishes success from failure. Extracts image URL/data or error details. Uses `error_processor.js` for error normalization.
        *   Inputs: Response from `callAIService`. The `runIndex` property can be used to check if this is a result of a retry.
        *   JavaScript Code:
            javascript
            // const errorProcessor = require('./lib/error_processor.js');
            // const logger =require('./lib/custom_logger.js');
            const { requestId } = $('adaptToAIService').item.json; // Get original request ID

            try {
                const aiResponse = items[0].json; // Or .binary for image data directly
                const httpNodeInfo = items[0].pairedItem; // Contains info about the HTTP call, including statusCode

                // Call: logger.logEvent('INFO', 'Received AI Service Response', { requestId, statusCode: httpNodeInfo.response.statusCode });

                if (httpNodeInfo.response.statusCode >= 200 && httpNodeInfo.response.statusCode < 300) {
                    // Success Case
                    let imageUrl = null; // Extract actual image URL or base64 data from aiResponse
                    // Example: imageUrl = aiResponse.outputs[0].images[0].url; (This is highly dependent on AI service)
                    // If image data is binary, it might be in items[0].binaryData and need base64 encoding
                    if (items[0].binaryData) {
                         // Handle binary data if AI service returns it directly
                         // For example, convert to base64 string or prepare for direct passthrough if Odoo supports it
                         // For this example, assume we get a URL or can construct one from the response
                    } else {
                        // Logic to extract image URL or data from JSON response
                        // This is pseudo-code, actual extraction logic depends on the AI service's response structure
                        if (aiResponse.artifacts && aiResponse.artifacts.length > 0 && aiResponse.artifacts[0].base64) {
                             imageUrl = `data:image/png;base64,${aiResponse.artifacts[0].base64}`; // Example for Stability AI
                        } else if (aiResponse.data && aiResponse.data.images && aiResponse.data.images.length > 0) {
                            imageUrl = aiResponse.data.images[0]; // Example for other services
                        } else {
                            throw new Error('Image URL or data not found in AI service response');
                        }
                    }

                    // Call: logger.logEvent('INFO', 'AI Image Generation Successful', { requestId, imageUrlPresent: !!imageUrl });
                    return [{ json: { status: 'success', result: { imageUrl }, requestId } }];
                } else {
                    // Error Case
                    const normalizedError = error_processor.normalizeAIServiceError(aiResponse, $('adaptToAIService').item.json.aiServiceType);
                    // Call: logger.logEvent('ERROR', 'AI Service Returned Error', { requestId, error: normalizedError, statusCode: httpNodeInfo.response.statusCode });
                    return [{ json: { status: 'error', error: normalizedError, requestId } }];
                }
            } catch (error) {
                // Call: logger.logEvent('ERROR', 'Error processing AI Service Response', { requestId, error: error.message, stack: error.stack, input: items[0].json });
                const workflowError = error_processor.createWorkflowErrorObject(error.message, 'processAIServiceResponse', 'INTERNAL_PROCESSING_ERROR');
                return [{ json: { status: 'error', error: workflowError, requestId } }]; // Ensure requestId is passed
            }
            
        *   Outputs: Object with `{ status: 'success'/'error', result: { imageUrl } or error: { message, code }, requestId }`.
    7.  **Function Node (`formatOdooCallback`)**:
        *   Purpose: Formats the payload to be sent back to Odoo's callback API. Uses `odoo_payload_handler.js`.
        *   Inputs: Output from `processAIServiceResponse`.
        *   JavaScript Code:
            javascript
            // const odooHandler = require('./lib/odoo_payload_handler.js');
            // const logger = require('./lib/custom_logger.js');
            const { status, result, error, requestId } = items[0].json;

            let callbackPayload;
            if (status === 'success') {
                // Assuming result contains { imageUrl }
                // Add other metadata if needed, e.g., seed used, dimensions, passed from AI response
                const generationMetadata = { /* e.g., seed: result.seed, width: result.width */ };
                callbackPayload = odoo_payload_handler.formatSuccessCallback(result.imageUrl, requestId, generationMetadata);
                // Call: logger.logEvent('INFO', 'Formatted Success Callback for Odoo', { requestId });
            } else {
                // Assuming error contains { message, code }
                callbackPayload = odoo_handler.formatErrorCallback(error.message, error.code, requestId);
                // Call: logger.logEvent('ERROR', 'Formatted Error Callback for Odoo', { requestId, error: error.message });
            }
            return [{ json: callbackPayload }];
            
        *   Outputs: JSON payload for Odoo callback.
    8.  **HTTP Request Node (`sendToOdooCallback`)**:
        *   Purpose: Sends the result/error back to the Odoo callback API.
        *   Inputs: Output from `formatOdooCallback`.
        *   Configuration:
            *   **Method**: POST.
            *   **URL**: `{{ $env.ODOO_CALLBACK_URL }}` (Set as N8N environment variable).
            *   **Authentication**: Generic Credential Type (e.g., Header Auth with a secret API key). N8N credentials for Odoo callback.
            *   **Body Type**: JSON.
            *   **Body**: `{{ $json }}`
            *   **Options -> Retry on Fail**: Enabled (for transient Odoo availability issues).
        *   Outputs: Response from Odoo callback (typically just an acknowledgement).
    9.  **Function Node (`logFinalStatus`)** (Optional, or part of `sendToOdooCallback`'s "Executed" branch):
        *   Purpose: Logs the final outcome of the callback to Odoo.
        *   Inputs: Response from `sendToOdooCallback`.
        *   JavaScript Code:
            javascript
            // const logger = require('./lib/custom_logger.js');
            const odooResponse = items[0].json;
            const originalRequestId = $('formatOdooCallback').item.json.request_id; // Access the request_id from the payload sent to Odoo
            // Call: logger.logEvent('INFO', 'Odoo Callback Completed', { requestId: originalRequestId, odooResponseStatus: items[0].pairedItem.response.statusCode, odooResponseBody: odooResponse });
            return items;
            
    10. **Error Trigger Node (`workflowErrorTrigger`)**:
        *   Purpose: Catches unhandled errors from any node in the main flow.
        *   Configuration: Connect "error" output of nodes like `parseAndValidateRequest`, `adaptToAIService`, `callAIService` (if retry fails), `processAIServiceResponse` to this node.
        *   Flow: This node should lead to a simplified version of `formatOdooCallback` (specifically for workflow errors) and then to `sendToOdooCallback` to inform Odoo about the N8N-side failure.
        *   It's crucial to ensure that the `requestId` from the initial Odoo payload is captured and passed along this error path. This can be done by setting a workflow-level variable or ensuring it's part of the error object passed to the Error Trigger node.
        *   **Simplified Error Formatting for Workflow Errors**:
            *   **Function Node (`formatWorkflowErrorForOdoo`)**:
                *   Inputs: Error object from Error Trigger. It needs access to the original `requestId`. This might require careful structuring of how `requestId` is passed to or made available to the error flow. One way is to have an initial "Set" node after the Webhook that stores `requestId` in a globally accessible way for the execution, or ensure all functions that can throw errors pass `requestId` along.
                *   JavaScript Code (conceptual):
                    javascript
                    // const odooHandler = require('./lib/odoo_payload_handler.js');
                    // const logger = require('./lib/custom_logger.js');
                    // Assume errorData = items[0].json; and originalRequestId is somehow available
                    // e.g. by accessing an earlier node's data if error routing allows:
                    // const originalRequestId = $('parseAndValidateRequest').item.json.requestId || 'UNKNOWN_REQUEST_ID';
                    // A robust way: The webhook trigger node data (items[0].json.request_id) could be merged into the error data flow if N8N allows
                    // For this example, let's assume originalRequestId is made available

                    const errorInput = items[0].json; // This is the error data from the Error Trigger
                    // Attempt to get requestId. This is tricky with N8N error flows.
                    // Best practice: Odoo passes request_id, parseAndValidateRequest extracts it.
                    // If subsequent nodes fail, they should ideally pass this requestId in their error context.
                    // If that's not directly possible, the Error Trigger node might need to look up data from the trigger node.
                    // For simplicity, we'll assume it can be retrieved.
                    let requestId = "UNKNOWN_REQUEST_ID";
                    try {
                        // Attempt to retrieve from initial payload if Error Trigger allows access
                        // This depends on N8N version and how error outputs are handled
                        // A common pattern is to merge initial data into the flow.
                        // If using a workflow variable set at the start:
                        // requestId = $workflow.get('initialRequestId');
                        // Or if the parseAndValidateRequest output is accessible via error path:
                        // requestId = $('parseAndValidateRequest').item.json.requestId;
                        // For this example, assume it's passed through or globally set
                        requestId = $vars.initialOdooRequestId || "UNKNOWN_REQUEST_ID_FALLBACK";

                    } catch (e) { /* ignore, fallback used */ }

                    const errorMessage = errorInput.error ? errorInput.error.message : "N8N workflow execution error";
                    const errorCode = errorInput.error && errorInput.error.code ? errorInput.error.code : "N8N_WORKFLOW_FAILURE";

                    // Call: logger.logEvent('CRITICAL', 'N8N Workflow Failed, Notifying Odoo', { requestId, error: errorMessage, errorCode });
                    const callbackPayload = odoo_handler.formatErrorCallback(errorMessage, errorCode, requestId);
                    return [{ json: callbackPayload }];
                    
                *   This then connects to `sendToOdooCallback`.
*   **Settings**:
    *   Error Workflow: Set to `workflowErrorTrigger` to handle unexpected errors.
    *   Save Execution Progress: Enabled.
    *   Save Execution Data: `On Error Only` or `Always` (depending on debugging needs and data sensitivity).
    *   Execution Order: `executeNodeOnce`.
*   **Environment Variables (to be configured in N8N environment)**:
    *   `ODOO_CALLBACK_URL`: The URL for Odoo's callback API endpoint.
    *   `ODOO_CALLBACK_API_KEY`: Secret key for authenticating N8N with Odoo's callback.
    *   `AI_SERVICE_API_KEY_[SERVICE_TYPE]`: API keys for different AI services, though preferably managed via N8N's credential store.
    *   `AI_SERVICE_ENDPOINT_[SERVICE_TYPE]`: Base URLs for different AI services.
    *   `LOG_LEVEL`: (e.g., 'INFO', 'DEBUG') for `custom_logger.js`.

### 4.2 `lib/ai_service_adapter.js`
Helper JavaScript module for adapting requests to various AI service APIs.

*   **Purpose**: Encapsulate AI service-specific request formatting and endpoint/auth logic. (REQ-IL-006)
*   **Functions**:
    *   `adaptToAIService(odooRequestParams, targetAIServiceType, modelName)`:
        *   **Parameters**:
            *   `odooRequestParams` (Object): Parsed parameters from Odoo (e.g., prompt, negativePrompt, seed, steps, resolution, width, height, cfgScale, specificModelIdentifierFromOdoo).
            *   `targetAIServiceType` (String): Identifier for the AI service (e.g., 'COMFY_UI', 'STABILITY_AI').
            *   `modelName` (String): Specific model/LoRA identifier for the AI service (e.g. externalModelId from AIImageModel table).
        *   **Returns**: (Object) The payload formatted for the target AI service API.
        *   **Logic**:
            1.  Switch statement or if-else chain based on `targetAIServiceType`.
            2.  For each service type, call a private helper function (e.g., `_formatForComfyUI`, `_formatForStabilityAI`).
            3.  Private helper functions:
                *   Map `odooRequestParams` to the AI service's expected field names and structures.
                *   Handle resolution/aspect ratio conversions if needed.
                *   Incorporate `modelName` or `specificModelIdentifierFromOdoo` into the payload as required by the AI service (e.g., selecting a checkpoint, LoRA, workflow in ComfyUI, or model ID for Stability AI).
                *   Return the AI service-specific payload.
            4.  If `targetAIServiceType` is unknown, throw an error.
    *   `getAIServiceEndpoint(targetAIServiceType, modelName)`:
        *   **Parameters**:
            *   `targetAIServiceType` (String): Identifier for the AI service.
            *   `modelName` (String): Optional, specific model identifier if it affects the endpoint.
        *   **Returns**: (String) The full API endpoint URL for the AI service.
        *   **Logic**:
            1.  Retrieve base URL from N8N environment variables (e.g., `process.env.AI_SERVICE_ENDPOINT_COMFY_UI`).
            2.  Append any necessary paths based on `targetAIServiceType` and `modelName`.
            3.  Return the complete endpoint URL.
            4.  If `targetAIServiceType` is unknown, throw an error.
    *   `getAIServiceAuthHeaders(targetAIServiceType, credentialsObject)`:
        *   **Parameters**:
            *   `targetAIServiceType` (String): Identifier for the AI service.
            *   `credentialsObject` (Object): N8N credentials object for the service.
        *   **Returns**: (Object) HTTP headers for authentication.
        *   **Logic**:
            1.  Construct authentication headers based on `targetAIServiceType` and `credentialsObject`.
            2.  Example: For API Key auth: `{ "Authorization": "Bearer " + credentialsObject.apiKey }`.
            3.  Return the headers object. This function primarily relies on N8N's HTTP Request node handling credentials directly. This helper is for more complex auth schemes if needed.

### 4.3 `lib/odoo_payload_handler.js`
Helper JavaScript module for Odoo webhook parsing and callback formatting.

*   **Purpose**: Ensure consistent data contracts with Odoo. (REQ-AIGS-001)
*   **Functions**:
    *   `parseAndValidateOdooWebhook(webhookBody)`:
        *   **Parameters**:
            *   `webhookBody` (Object): The JSON payload received from Odoo's webhook.
        *   **Returns**: (Object) `{ requestId: string, params: object, aiServiceType: string, modelName: string }` on success, or `{ error: { message: string, code: string } }` on validation failure.
        *   **Logic**:
            1.  Check for presence of mandatory fields: `request_id`, `prompt`, `ai_service_type`, `model_name` (or `model_id`), `resolution`, `aspect_ratio`.
            2.  Validate data types if necessary (e.g., `steps` is a number).
            3.  Map Odoo field names to internal N8N parameter names if different (e.g., `request_id` to `requestId`).
            4.  If validation fails, return an error object.
            5.  Return the parsed and validated data.
    *   `formatSuccessCallback(imageUrlOrData, originalRequestId, generationMetadata)`:
        *   **Parameters**:
            *   `imageUrlOrData` (String): URL of the generated image or base64 encoded image data.
            *   `originalRequestId` (String): The `request_id` from the initial Odoo request.
            *   `generationMetadata` (Object): Optional. Additional metadata about the generation (e.g., seed used, actual dimensions, model used).
        *   **Returns**: (Object) JSON payload for Odoo callback on success.
        *   **Logic**:
            1.  Construct payload:
                json
                {
                  "request_id": originalRequestId,
                  "status": "completed",
                  "image_url": imageUrlOrData, // or "image_data": base64ImageData
                  "metadata": generationMetadata
                }
                
    *   `formatErrorCallback(errorMessage, errorCode, originalRequestId)`:
        *   **Parameters**:
            *   `errorMessage` (String): Description of the error.
            *   `errorCode` (String): A code identifying the error type (optional).
            *   `originalRequestId` (String): The `request_id` from the initial Odoo request.
        *   **Returns**: (Object) JSON payload for Odoo callback on failure.
        *   **Logic**:
            1.  Construct payload:
                json
                {
                  "request_id": originalRequestId,
                  "status": "failed",
                  "error": {
                    "message": errorMessage,
                    "code": errorCode
                  }
                }
                

### 4.4 `lib/error_processor.js`
Helper JavaScript module for standardizing error objects.

*   **Purpose**: Create consistent error messages for logging and Odoo callback. (REQ-IL-009)
*   **Functions**:
    *   `normalizeAIServiceError(rawErrorFromAIService, serviceType)`:
        *   **Parameters**:
            *   `rawErrorFromAIService` (Object/String): The raw error response from the AI service.
            *   `serviceType` (String): Identifier for the AI service.
        *   **Returns**: (Object) `{ message: string, code: string, details: any }`.
        *   **Logic**:
            1.  Parse `rawErrorFromAIService` based on `serviceType` (as different services have different error formats).
            2.  Extract a user-friendly `message`, a service-specific `code` (if available), and any relevant `details`.
            3.  Return the standardized error object.
    *   `createWorkflowErrorObject(errorMessage, stepName, internalErrorCode)`:
        *   **Parameters**:
            *   `errorMessage` (String): Description of the internal workflow error.
            *   `stepName` (String): Name of the N8N node/step where the error occurred.
            *   `internalErrorCode` (String): A custom internal error code.
        *   **Returns**: (Object) `{ message: string, code: string, step: string }`.
        *   **Logic**:
            1.  Construct the error object:
                javascript
                {
                  message: errorMessage,
                  code: internalErrorCode,
                  step: stepName
                }
                

### 4.5 `lib/custom_logger.js`
Helper JavaScript module for custom, structured logging.

*   **Purpose**: Facilitate detailed, structured, and traceable logging within N8N Function nodes. (REQ-ATEL-010)
*   **Functions**:
    *   `logEvent(level, message, contextData)`:
        *   **Parameters**:
            *   `level` (String): Log level (e.g., 'INFO', 'ERROR', 'DEBUG', 'WARN', 'CRITICAL').
            *   `message` (String): The log message.
            *   `contextData` (Object): Additional contextual data (e.g., `requestId`, `payload`, `stepName`).
        *   **Returns**: `void`.
        *   **Logic**:
            1.  Retrieve correlation ID using `getCorrelationId()`.
            2.  Construct a JSON log object:
                javascript
                {
                  timestamp: new Date().toISOString(),
                  level: level.toUpperCase(),
                  message: message,
                  correlationId: getCorrelationId(contextData.n8nExecutionData || $execution), // Pass N8N execution context if available
                  workflowName: $workflow.name, // N8N global variable
                  executionId: $execution.id,   // N8N global variable
                  nodeName: $node.name,         // N8N global variable for current node
                  ...contextData // Spread additional context
                }
                
            3.  Output the JSON string using `console.log(JSON.stringify(logObject));`. This allows N8N to capture it in its execution log, which can then be forwarded to a centralized logging system.
            4.  Respect `LOG_LEVEL` environment variable: only log if `level` meets or exceeds configured `LOG_LEVEL`.
    *   `getCorrelationId(n8nExecutionData)`:
        *   **Parameters**:
            *   `n8nExecutionData` (Object): The N8N execution context object, or data from the initial webhook.
        *   **Returns**: (String) The correlation ID.
        *   **Logic**:
            1.  Attempt to extract `request_id` from the initial webhook payload (which should be passed through the workflow or stored in a workflow variable).
            2.  If not found, fall back to N8N's own execution ID (`$execution.id`).
            3.  Return the determined correlation ID.

### 4.6 `package.json`
NPM package file for managing JavaScript helper development dependencies.

*   **Purpose**: Configure development tools for JS helpers. (REQ-DDSI-003)
*   **Content**:
    json
    {
      "name": "influencegen-n8n-workflow-helpers",
      "version": "1.0.0",
      "description": "Helper scripts for InfluenceGen N8N AI Image Generation Workflow",
      "private": true,
      "scripts": {
        "lint": "eslint lib/**/*.js",
        "format": "prettier --write lib/**/*.js"
      },
      "devDependencies": {
        "eslint": "^8.0.0", // Specify appropriate version
        "prettier": "^2.0.0", // Specify appropriate version
        // Add any other ESLint plugins/configs (e.g., eslint-config-airbnb-base)
      }
    }
    

## 5. Data Design
This repository does not directly manage a database. It processes data flowing between Odoo and AI services. The data structures are defined by:
*   **Odoo Webhook Payload**: Defined by Odoo, parsed by `odoo_payload_handler.js`. Expected fields: `request_id`, `prompt`, `negative_prompt` (optional), `ai_service_type`, `model_name` (or `model_id`), `resolution`, `aspect_ratio`, `seed` (optional), `steps` (optional), `cfg_scale` (optional), and any other necessary parameters.
*   **AI Service API Payloads**: Defined by the respective AI services, constructed by `ai_service_adapter.js`.
*   **Odoo Callback API Payload**: Defined by Odoo's callback endpoint requirements, formatted by `odoo_payload_handler.js`. Expected fields: `request_id`, `status` ('completed' or 'failed'), `image_url` or `image_data` (on success), `metadata` (on success, optional), `error` object (on failure, with `message` and `code`).

## 6. Interface Design

### 6.1 Odoo to N8N Webhook Interface
*   **Endpoint (N8N side)**: `/webhook/influencegen/ai-image-generate` (Path on N8N Webhook node).
*   **Method**: POST.
*   **Request Body (JSON)**:
    json
    {
      "request_id": "unique_odoo_request_identifier_string",
      "prompt": "string",
      "negative_prompt": "string (optional)",
      "ai_service_type": "string (e.g., 'COMFY_UI', 'STABILITY_AI')",
      "model_name": "string (identifier for the AI model/LoRA/workflow)",
      "resolution": "string (e.g., '1024x1024')",
      "aspect_ratio": "string (e.g., '1:1')",
      "seed": "integer (optional)",
      "steps": "integer (optional, e.g., 20-50)",
      "cfg_scale": "number (optional, e.g., 7.5)",
      // Other parameters specific to Odoo's needs or AI service capabilities
      "user_id": "odoo_user_id_string (for quotas/tracking, optional if N8N uses a generic identity)",
      "campaign_id": "campaign_identifier_string (optional)"
    }
    
*   **Authentication**: Basic Auth or Header Auth, configured on N8N webhook node.
*   **Response (from N8N Webhook Node)**: HTTP 200 OK (if "Respond Immediately" is chosen) or the final workflow output (if "Respond When Workflow Finishes" and Odoo expects a synchronous-like response from the webhook itself, which is less likely for long tasks).

### 6.2 N8N to AI Service API Interface
*   **Endpoint (AI Service side)**: Varies per AI service. Determined by `ai_service_adapter.js`.
*   **Method**: Typically POST.
*   **Request Body (JSON or other)**: Varies per AI service. Formatted by `ai_service_adapter.js`.
*   **Authentication**: Varies per AI service (e.g., API Key in header, OAuth). Handled by N8N HTTP Request node using stored credentials.
*   **Response (from AI Service)**: Varies per AI service. JSON containing image URLs/data or error details, or direct binary image data.

### 6.3 N8N to Odoo Callback API Interface
*   **Endpoint (Odoo side)**: `{$env.ODOO_CALLBACK_URL}` (e.g., `https://odoo.influencegen.com/api/influencegen/ai_image_callback`).
*   **Method**: POST.
*   **Request Body (JSON)**: Formatted by `odoo_payload_handler.js`.
    *   Success:
        json
        {
          "request_id": "unique_odoo_request_identifier_string",
          "status": "completed",
          "image_url": "url_to_image_or_base64_data_string",
          "metadata": {
            "seed_used": 12345,
            "actual_width": 1024,
            "actual_height": 1024,
            "model_used_identifier": "..."
            // other relevant metadata from AI service
          }
        }
        
    *   Failure:
        json
        {
          "request_id": "unique_odoo_request_identifier_string",
          "status": "failed",
          "error": {
            "message": "Error message string",
            "code": "ERROR_CODE_STRING (optional)"
          }
        }
        
*   **Authentication**: E.g., API Key in header. Handled by N8N HTTP Request node using stored credentials for Odoo.
*   **Response (from Odoo Callback API)**: HTTP 200 OK or 202 Accepted for successful processing. Error status codes for issues on Odoo's side.

## 7. Deployment Considerations
*   **N8N Instance**: A dedicated N8N instance (self-hosted or cloud) is required.
*   **Workflow Deployment**: The `main_ai_image_generation_workflow.json` file will be imported into the N8N instance.
*   **Helper Scripts**: The JavaScript code from `lib/*.js` files will be embedded into the relevant N8N Function nodes within the main workflow. There is no separate "deployment" for these scripts other than being part of the workflow JSON, unless N8N supports external script referencing in the chosen version, which is less common for simple helpers. For maintainability, the JS code should be developed and version-controlled in these separate files and then copied into Function nodes.
*   **Environment Variables**: `ODOO_CALLBACK_URL`, `ODOO_CALLBACK_API_KEY`, and AI service-specific variables must be configured in the N8N environment.
*   **Credentials**: AI service API keys and Odoo callback API keys must be configured in N8N's credential store.
*   **Version Control**: The workflow JSON and JS helper source files must be stored in version control (Git) (REQ-DDSI-002).
*   **Scalability**: The N8N instance should be configured to handle the expected load of AI generation requests (e.g., appropriate execution modes like `queue` if self-hosting with worker processes).

## 8. Testing Considerations
*   **Unit Testing (JS Helpers)**: While N8N Function nodes are hard to unit test externally, the logic within `lib/*.js` files can be structured to be testable with a standard JavaScript testing framework (e.g., Jest, Mocha) if extracted and run in a Node.js environment. This is primarily for development-time validation of the helper logic.
*   **Workflow Testing (N8N)**:
    *   Manual execution of the workflow in the N8N editor with sample input data.
    *   Testing different paths (success, AI service errors, Odoo callback errors).
    *   Verifying retry logic.
    *   Checking logs for correctness and completeness.
*   **Integration Testing**: End-to-end testing initiated from Odoo, through N8N, to the AI service, and back to Odoo's callback.
    *   Test with mock AI services to isolate N8N workflow logic.
    *   Test with actual AI services (in a non-production environment if possible).
    *   Verify correct handling of various Odoo request parameters.
    *   Verify correct image/error delivery to Odoo.

## 9. Future Considerations / Extensibility
*   **New AI Services**: Add new formatting functions to `ai_service_adapter.js` and update workflow configuration/logic to select the new adapter.
*   **More Complex Retry/Error Handling**: If N8N's built-in retry is insufficient, custom looping and conditional logic can be built within the workflow.
*   **Workflow Versioning**: N8N supports workflow versioning internally. External JSON file should also be version controlled.
*   **Advanced Logging**: If `console.log` is insufficient for centralized logging, an HTTP Request node could be added to the logger function to send logs to a dedicated logging API endpoint.

This SDS provides a comprehensive blueprint for the N8N AI image generation workflow and its supporting components. Adherence to these specifications will ensure a robust, secure, and maintainable solution.