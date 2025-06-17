```javascript
/**
 * lib/odoo_payload_handler.js
 * Helper JavaScript module for Odoo webhook parsing and callback formatting.
 * Assumes this code is "prepended" to N8N Function nodes, making the
 * odoo_payload_handler object globally available.
 */

const odoo_payload_handler = {
    parseAndValidateOdooWebhook: function(webhookBody) {
        if (!webhookBody) {
            return { error: { message: 'Request body is empty or null.', code: 'VALIDATION_ERROR_EMPTY_PAYLOAD' } };
        }

        const requiredFields = ['request_id', 'prompt', 'ai_service_type', 'model_name', 'resolution', 'aspect_ratio'];
        const missingFields = [];
        for (const field of requiredFields) {
            if (webhookBody[field] === undefined || webhookBody[field] === null || webhookBody[field] === '') {
                missingFields.push(field);
            }
        }

        if (missingFields.length > 0) {
            return {
                error: {
                    message: `Missing required fields: ${missingFields.join(', ')}`,
                    code: 'VALIDATION_ERROR_MISSING_FIELDS'
                }
            };
        }

        // Basic type validations
        if (typeof webhookBody.request_id !== 'string') {
            return { error: { message: 'request_id must be a string.', code: 'VALIDATION_ERROR_INVALID_REQUEST_ID_TYPE' } };
        }
        if (typeof webhookBody.prompt !== 'string' || webhookBody.prompt.length < 1) {
            return { error: { message: 'prompt must be a non-empty string.', code: 'VALIDATION_ERROR_INVALID_PROMPT' } };
        }
        if (typeof webhookBody.ai_service_type !== 'string') {
            return { error: { message: 'ai_service_type must be a string.', code: 'VALIDATION_ERROR_INVALID_SERVICE_TYPE' } };
        }
        if (typeof webhookBody.model_name !== 'string') {
            return { error: { message: 'model_name must be a string.', code: 'VALIDATION_ERROR_INVALID_MODEL_NAME' } };
        }
        if (typeof webhookBody.resolution !== 'string' || !/^\d+x\d+$/.test(webhookBody.resolution)) {
            return { error: { message: 'resolution must be in format "WIDTHxHEIGHT" (e.g., "1024x1024").', code: 'VALIDATION_ERROR_INVALID_RESOLUTION' } };
        }
        if (typeof webhookBody.aspect_ratio !== 'string' || !/^\d+:\d+$/.test(webhookBody.aspect_ratio)) {
            return { error: { message: 'aspect_ratio must be in format "W:H" (e.g., "1:1").', code: 'VALIDATION_ERROR_INVALID_ASPECT_RATIO' } };
        }
        if (webhookBody.steps !== undefined && (typeof webhookBody.steps !== 'number' || webhookBody.steps < 1 || webhookBody.steps > 150)) {
            return { error: { message: 'steps must be a number between 1 and 150.', code: 'VALIDATION_ERROR_INVALID_STEPS' } };
        }
        if (webhookBody.cfg_scale !== undefined && (typeof webhookBody.cfg_scale !== 'number' || webhookBody.cfg_scale < 0 || webhookBody.cfg_scale > 30)) {
            return { error: { message: 'cfg_scale must be a number between 0 and 30.', code: 'VALIDATION_ERROR_INVALID_CFG_SCALE' } };
        }
        if (webhookBody.seed !== undefined && (typeof webhookBody.seed !== 'number' || webhookBody.seed < 0)) {
            return { error: { message: 'seed must be a non-negative number.', code: 'VALIDATION_ERROR_INVALID_SEED' } };
        }


        // Passed validation, structure the output
        const params = {
            prompt: webhookBody.prompt,
            negativePrompt: webhookBody.negative_prompt, // Optional
            resolution: webhookBody.resolution,
            aspectRatio: webhookBody.aspect_ratio,
            seed: webhookBody.seed, // Optional
            steps: webhookBody.steps, // Optional
            cfgScale: webhookBody.cfg_scale, // Optional
            // Include other optional params if they exist
            userId: webhookBody.user_id,
            campaignId: webhookBody.campaign_id
        };

        // Remove undefined optional params to keep the object clean
        Object.keys(params).forEach(key => params[key] === undefined && delete params[key]);

        return {
            requestId: webhookBody.request_id,
            params: params,
            aiServiceType: webhookBody.ai_service_type,
            modelName: webhookBody.model_name
        };
    },

    formatSuccessCallback: function(imageUrlOrData, originalRequestId, generationMetadata = {}) {
        const payload = {
            request_id: originalRequestId,
            status: "completed",
            metadata: generationMetadata || {}
        };

        if (imageUrlOrData && typeof imageUrlOrData === 'string') {
            if (imageUrlOrData.startsWith('data:image')) {
                payload.image_data = imageUrlOrData; // Base64 data URI
            } else {
                payload.image_url = imageUrlOrData; // Regular URL
            }
        } else {
            // This case should ideally be prevented by upstream logic ensuring imageUrlOrData is valid on success
            console.error(`[ODoo Payload Handler] formatSuccessCallback called with invalid imageUrlOrData for requestId: ${originalRequestId}`);
            payload.status = "failed";
            payload.error = {
                message: "Internal error: Image data or URL was missing or invalid upon success callback formatting.",
                code: "CALLBACK_FORMATTING_INVALID_IMAGE_DATA_ON_SUCCESS"
            };
            delete payload.image_url;
            delete payload.image_data;
            delete payload.metadata;
        }
        return payload;
    },

    formatErrorCallback: function(errorMessage, errorCode, originalRequestId) {
        if (!originalRequestId) {
            console.error("[ODoo Payload Handler] formatErrorCallback called without originalRequestId. Error:", errorMessage, errorCode);
            // This is a critical issue, but we still need to try to inform Odoo if possible,
            // though without request_id it's less useful.
        }
        return {
            request_id: originalRequestId || "UNKNOWN_REQUEST_ID_IN_ERROR_CALLBACK",
            status: "failed",
            error: {
                message: errorMessage || "An unspecified error occurred in the N8N workflow.",
                code: errorCode || "N8N_WORKFLOW_UNSPECIFIED_ERROR"
            }
        };
    }
};
```