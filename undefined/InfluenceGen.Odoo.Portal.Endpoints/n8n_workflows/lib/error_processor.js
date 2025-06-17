/**
 * lib/error_processor.js
 * Helper JavaScript module for standardizing error objects.
 */

/**
 * Normalizes a raw error response from an AI service into a standard format.
 * @param {object|string} rawErrorFromAIService - The raw error response from the AI service. This could be the JSON body of an HTTP error response, or a string.
 * @param {string} serviceType - Identifier for the AI service (e.g., 'COMFY_UI', 'STABILITY_AI').
 * @returns {object} `{ message: string, code: string, details: any }`.
 */
function normalizeAIServiceError(rawErrorFromAIService, serviceType) {
    let message = "An unknown error occurred with the AI service.";
    let code = `AI_SERVICE_ERROR_UNKNOWN_${serviceType.toUpperCase()}`;
    let details = rawErrorFromAIService; // Default to including the raw error for debugging

    try {
        if (typeof rawErrorFromAIService === 'string') {
            // If the error is just a string, use it as the message
            message = `AI Service Error (${serviceType}): ${rawErrorFromAIService}`;
            // Attempt to parse if it's a JSON string
            try {
                const parsedJsonError = JSON.parse(rawErrorFromAIService);
                rawErrorFromAIService = parsedJsonError; // Continue to object processing
            } catch (e) {
                // Not a JSON string, keep as is
            }
        }

        if (typeof rawErrorFromAIService === 'object' && rawErrorFromAIService !== null) {
            details = { ...rawErrorFromAIService }; // Copy details

            switch (serviceType.toUpperCase()) {
                case 'STABILITY_AI':
                    // Stability AI errors typically have a `message` and `name` or `errors` array.
                    // Example: { "id": "stable-image-core_error_...", "name": "content_moderation", "message": "Prompt triggered content moderation filter", "errors": ["Prompt triggered content moderation filter"] }
                    // Example: { "message": "invalid_api_key", "errors": ["API key is invalid"] }
                    if (rawErrorFromAIService.message) {
                        message = `Stability AI Error: ${rawErrorFromAIService.message}`;
                    }
                    if (rawErrorFromAIService.name) {
                        code = `AI_STABILITY_${rawErrorFromAIService.name.toUpperCase().replace(/\s+/g, '_')}`;
                    } else if (rawErrorFromAIService.errors && Array.isArray(rawErrorFromAIService.errors) && rawErrorFromAIService.errors.length > 0) {
                        message = `Stability AI Error: ${rawErrorFromAIService.errors.join('; ')}`;
                        // Try to make a code from the first error if no general name
                        if (!rawErrorFromAIService.name) {
                             code = `AI_STABILITY_ERROR_DETAIL_${rawErrorFromAIService.errors[0].substring(0,20).toUpperCase().replace(/\s+/g, '_')}`;
                        }
                    }
                    break;

                case 'COMFY_UI':
                    // ComfyUI errors can vary. Common patterns:
                    // { "error": "Error message string", "node_errors": { ... } }
                    // { "type": "execution_error", "message": "...", "details": "...", "node_id": "..." }
                    if (rawErrorFromAIService.error && typeof rawErrorFromAIService.error === 'string') {
                        message = `ComfyUI Error: ${rawErrorFromAIService.error}`;
                        if (rawErrorFromAIService.node_errors) {
                            details.node_errors = rawErrorFromAIService.node_errors; // Keep node-specific errors
                            const firstNodeErrorKey = Object.keys(rawErrorFromAIService.node_errors)[0];
                            if (firstNodeErrorKey) {
                                const firstNodeErrorInfo = rawErrorFromAIService.node_errors[firstNodeErrorKey];
                                if(firstNodeErrorInfo.errors && firstNodeErrorInfo.errors.length > 0){
                                    message += ` (Node ${firstNodeErrorKey}: ${firstNodeErrorInfo.errors[0].message || 'Unknown node error'})`;
                                }
                            }
                        }
                        code = 'AI_COMFY_EXECUTION_ERROR';
                    } else if (rawErrorFromAIService.message && rawErrorFromAIService.type) {
                        message = `ComfyUI Error (${rawErrorFromAIService.type}): ${rawErrorFromAIService.message}`;
                        code = `AI_COMFY_${rawErrorFromAIService.type.toUpperCase().replace(/\s+/g, '_')}`;
                        if (rawErrorFromAIService.node_id) details.node_id = rawErrorFromAIService.node_id;
                    }
                    break;

                // Add cases for other AI services here
                default:
                    // Generic attempt to find a message
                    if (rawErrorFromAIService.message && typeof rawErrorFromAIService.message === 'string') {
                        message = `AI Service Error (${serviceType}): ${rawErrorFromAIService.message}`;
                    } else if (rawErrorFromAIService.error && typeof rawErrorFromAIService.error === 'string') {
                        message = `AI Service Error (${serviceType}): ${rawErrorFromAIService.error}`;
                    } else if (rawErrorFromAIService.detail && typeof rawErrorFromAIService.detail === 'string') {
                        message = `AI Service Error (${serviceType}): ${rawErrorFromAIService.detail}`;
                    }
                    // Generic attempt to find a code
                    if (rawErrorFromAIService.code && typeof rawErrorFromAIService.code === 'string') {
                        code = `AI_SERVICE_${serviceType.toUpperCase()}_${rawErrorFromAIService.code.toUpperCase().replace(/\s+/g, '_')}`;
                    }
                    break;
            }
        }
    } catch (e) {
        // Error during error normalization itself
        console.error(`[CRITICAL] Error while normalizing AI service error for ${serviceType}: ${e.message}`, e, rawErrorFromAIService);
        message = `Failed to normalize error from AI Service ${serviceType}. Raw error: ${JSON.stringify(rawErrorFromAIService).substring(0, 200)}...`;
        code = `ERROR_NORMALIZATION_FAILURE_${serviceType.toUpperCase()}`;
        details = { rawError: rawErrorFromAIService, normalizationError: e.message };
    }

    return {
        message: message,
        code: code,
        details: details // Include processed or raw details for further inspection
    };
}

/**
 * Creates a standardized error object for internal N8N workflow errors.
 * @param {string} errorMessage - Description of the internal workflow error.
 *   This can be a direct message or a JSON stringified object from a previous error.
 * @param {string} stepName - Name of the N8N node/step where the error occurred.
 * @param {string} internalErrorCode - A custom internal error code (e.g., 'VALIDATION_ERROR', 'ADAPTATION_FAILURE').
 * @returns {object} `{ message: string, code: string, step: string, originalError?: any }`.
 */
function createWorkflowErrorObject(errorMessage, stepName, internalErrorCode) {
    let finalErrorMessage = errorMessage;
    let originalErrorDetails = null;

    // Check if errorMessage is a JSON stringified error object (e.g., from a previous createWorkflowErrorObject call)
    try {
        if (typeof errorMessage === 'string' && errorMessage.startsWith('{') && errorMessage.endsWith('}')) {
            const parsedError = JSON.parse(errorMessage);
            if (parsedError && parsedError.message && parsedError.code) { // It's likely one of our structured errors
                finalErrorMessage = parsedError.message; // Use the message from the nested error
                internalErrorCode = parsedError.code || internalErrorCode; // Prefer nested code
                stepName = parsedError.step || stepName; // Prefer nested step
                originalErrorDetails = parsedError.details || parsedError.originalError || parsedError; // Capture details
            }
        }
    } catch (e) {
        // Not a JSON string or not our format, use errorMessage as is.
    }

    const errorObject = {
        message: `N8N Workflow Error at step '${stepName}': ${finalErrorMessage}`,
        code: internalErrorCode || "N8N_WORKFLOW_GENERIC_ERROR",
        step: stepName || "UNKNOWN_STEP"
    };

    if (originalErrorDetails) {
        errorObject.originalError = originalErrorDetails;
    }

    return errorObject;
}