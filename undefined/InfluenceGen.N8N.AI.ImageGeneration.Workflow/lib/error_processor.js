```javascript
/**
 * lib/error_processor.js
 * Helper JavaScript module for standardizing error objects.
 * Assumes this code is "prepended" to N8N Function nodes, making the
 * error_processor object globally available.
 */

const error_processor = {
    normalizeAIServiceError: function(rawErrorFromAIService, serviceType) {
        let message = "An error occurred with the AI service.";
        let code = `AI_SERVICE_ERROR_UNKNOWN_${serviceType ? serviceType.toUpperCase() : 'GENERIC'}`;
        let details = rawErrorFromAIService;

        if (typeof rawErrorFromAIService === 'object' && rawErrorFromAIService !== null) {
            // Example for Stability AI (often has 'errors' array or 'message' field)
            if (serviceType && serviceType.toUpperCase() === 'STABILITY_AI') {
                if (Array.isArray(rawErrorFromAIService.errors) && rawErrorFromAIService.errors.length > 0) {
                    message = `Stability AI Error: ${rawErrorFromAIService.errors.join(', ')}`;
                    code = 'AI_STABILITY_API_ERROR';
                } else if (rawErrorFromAIService.message) {
                    message = `Stability AI Error: ${rawErrorFromAIService.message}`;
                    code = `AI_STABILITY_API_${rawErrorFromAIService.name ? rawErrorFromAIService.name.toUpperCase() : 'ERROR'}`;
                } else {
                    message = `Stability AI returned an unrecognized error structure.`;
                }
            }
            // Example for ComfyUI (errors might be in various forms, often a simple message or a structured error)
            else if (serviceType && serviceType.toUpperCase() === 'COMFY_UI') {
                 if (rawErrorFromAIService.error && typeof rawErrorFromAIService.error === 'string') {
                    message = `ComfyUI Error: ${rawErrorFromAIService.error}`;
                    code = 'AI_COMFY_ERROR_STRING';
                } else if (rawErrorFromAIService.error && rawErrorFromAIService.error.message) {
                    message = `ComfyUI Error: ${rawErrorFromAIService.error.message} (Type: ${rawErrorFromAIService.error.type || 'N/A'})`;
                    code = `AI_COMFY_${rawErrorFromAIService.error.type ? rawErrorFromAIService.error.type.toUpperCase() : 'ERROR'}`;
                    details = rawErrorFromAIService.error.details || rawErrorFromAIService.error.traceback;
                } else if (rawErrorFromAIService.node_errors && Object.keys(rawErrorFromAIService.node_errors).length > 0) {
                    // Handle complex ComfyUI node errors
                    const firstErrorNode = Object.keys(rawErrorFromAIService.node_errors)[0];
                    const errorDetails = rawErrorFromAIService.node_errors[firstErrorNode];
                    message = `ComfyUI Node Error in ${firstErrorNode}: ${errorDetails.errors && errorDetails.errors.length > 0 ? errorDetails.errors[0].message : 'Unknown node error'}`;
                    code = `AI_COMFY_NODE_ERROR_${firstErrorNode}`;
                    details = errorDetails;
                } else if (rawErrorFromAIService.message) {
                    message = `ComfyUI Error: ${rawErrorFromAIService.message}`;
                    code = 'AI_COMFY_GENERIC_ERROR';
                } else {
                     message = `ComfyUI returned an unrecognized error structure.`;
                }
            }
            // Generic attempt
            else if (rawErrorFromAIService.message) {
                message = `AI Service (${serviceType || 'Unknown'}) Error: ${rawErrorFromAIService.message}`;
                if(rawErrorFromAIService.code) code = `AI_SERVICE_${rawErrorFromAIService.code}`;
            } else if (rawErrorFromAIService.error && typeof rawErrorFromAIService.error === 'string') {
                 message = `AI Service (${serviceType || 'Unknown'}) Error: ${rawErrorFromAIService.error}`;
            } else if (rawErrorFromAIService.error && rawErrorFromAIService.error.message) {
                 message = `AI Service (${serviceType || 'Unknown'}) Error: ${rawErrorFromAIService.error.message}`;
            } else {
                 message = `AI Service (${serviceType || 'Unknown'}) returned an unrecognized object error structure.`;
            }
        } else if (typeof rawErrorFromAIService === 'string') {
            message = `AI Service (${serviceType || 'Unknown'}) Error: ${rawErrorFromAIService}`;
        }

        return {
            message: message,
            code: code,
            details: details // Keep raw details for debugging
        };
    },

    createWorkflowErrorObject: function(errorMessage, stepName, internalErrorCode) {
        return {
            message: `Workflow Error at step '${stepName || "UNKNOWN_STEP"}': ${errorMessage}`,
            code: internalErrorCode || "N8N_WORKFLOW_INTERNAL_ERROR",
            step: stepName || "UNKNOWN_STEP"
            // requestId should be added to this object by the caller if available
        };
    }
};
```