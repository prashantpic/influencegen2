/**
 * lib/odoo_payload_handler.js
 * Helper JavaScript module for Odoo webhook parsing and callback formatting.
 */

/**
 * Parses and validates the incoming Odoo webhook payload.
 * @param {object} webhookBody - The JSON payload received from Odoo's webhook.
 * @returns {object} `{ requestId: string, params: object, aiServiceType: string, modelName: string }` on success,
 *                   or `{ error: { message: string, code: string } }` on validation failure.
 */
function parseAndValidateOdooWebhook(webhookBody) {
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
                message: `Missing required fields in Odoo webhook payload: ${missingFields.join(', ')}`,
                code: 'VALIDATION_ERROR_MISSING_FIELDS'
            }
        };
    }

    // Basic type validation (can be expanded)
    if (typeof webhookBody.request_id !== 'string') {
        return { error: { message: 'Invalid request_id: must be a string.', code: 'VALIDATION_ERROR_INVALID_REQUEST_ID_TYPE' } };
    }
    if (typeof webhookBody.prompt !== 'string') {
        return { error: { message: 'Invalid prompt: must be a string.', code: 'VALIDATION_ERROR_INVALID_PROMPT_TYPE' } };
    }
    if (typeof webhookBody.ai_service_type !== 'string') {
        return { error: { message: 'Invalid ai_service_type: must be a string.', code: 'VALIDATION_ERROR_INVALID_SERVICE_TYPE' } };
    }
    if (typeof webhookBody.model_name !== 'string') {
        return { error: { message: 'Invalid model_name: must be a string.', code: 'VALIDATION_ERROR_INVALID_MODEL_NAME' } };
    }
    if (typeof webhookBody.resolution !== 'string' || !/^\d+x\d+$/.test(webhookBody.resolution)) {
        return { error: { message: 'Invalid resolution format. Expected "widthxheight" (e.g., "1024x1024").', code: 'VALIDATION_ERROR_INVALID_RESOLUTION' } };
    }
    if (typeof webhookBody.aspect_ratio !== 'string' || !/^\d+:\d+$/.test(webhookBody.aspect_ratio)) { // Allow ratios like 16:9, 1:1
        return { error: { message: 'Invalid aspect_ratio format. Expected "width:height" (e.g., "1:1", "16:9").', code: 'VALIDATION_ERROR_INVALID_ASPECT_RATIO' } };
    }

    // Optional fields validation
    const parsedParams = {
        prompt: webhookBody.prompt,
        negativePrompt: webhookBody.negative_prompt || undefined, // Keep as undefined if not provided
        resolution: webhookBody.resolution,
        aspectRatio: webhookBody.aspect_ratio,
        // Odoo sends model_name which corresponds to AIImageModel.name
        // This is passed directly as modelName to adapter functions.
        // Adapter functions will decide if this modelName is used directly (e.g. ComfyUI checkpoint file)
        // or if it needs to be mapped to an externalModelId (e.g. for StabilityAI).
    };

    // Parse numeric optional fields if they exist
    if (webhookBody.seed !== undefined && webhookBody.seed !== null) {
        const seed = parseInt(webhookBody.seed, 10);
        if (isNaN(seed)) {
            return { error: { message: 'Invalid seed: must be an integer.', code: 'VALIDATION_ERROR_INVALID_SEED' } };
        }
        parsedParams.seed = seed;
    }
    if (webhookBody.steps !== undefined && webhookBody.steps !== null) {
        const steps = parseInt(webhookBody.steps, 10);
        if (isNaN(steps) || steps <= 0) {
            return { error: { message: 'Invalid steps: must be a positive integer.', code: 'VALIDATION_ERROR_INVALID_STEPS' } };
        }
        parsedParams.steps = steps;
    }
    if (webhookBody.cfg_scale !== undefined && webhookBody.cfg_scale !== null) {
        const cfgScale = parseFloat(webhookBody.cfg_scale);
        if (isNaN(cfgScale)) {
            return { error: { message: 'Invalid cfg_scale: must be a number.', code: 'VALIDATION_ERROR_INVALID_CFG_SCALE' } };
        }
        parsedParams.cfgScale = cfgScale;
    }

    // Add other optional parameters from Odoo payload if needed
    if (webhookBody.user_id) parsedParams.userId = webhookBody.user_id;
    if (webhookBody.campaign_id) parsedParams.campaignId = webhookBody.campaign_id;

    // Split resolution into width and height for convenience in adapters, if needed
    const [widthStr, heightStr] = webhookBody.resolution.split('x');
    parsedParams.width = parseInt(widthStr, 10);
    parsedParams.height = parseInt(heightStr, 10);


    return {
        requestId: webhookBody.request_id,
        params: parsedParams,
        aiServiceType: webhookBody.ai_service_type,
        modelName: webhookBody.model_name // This is AIImageModel.name from Odoo
    };
}

/**
 * Formats the payload to be sent back to Odoo's callback API on success.
 * @param {string} imageUrlOrData - URL of the generated image or base64 encoded image data string (e.g., "data:image/png;base64,...").
 * @param {string} originalRequestId - The `request_id` from the initial Odoo request.
 * @param {object} [generationMetadata={}] - Optional. Additional metadata about the generation (e.g., seed_used, actual_width, actual_height, model_used_identifier).
 * @returns {object} JSON payload for Odoo callback on success.
 */
function formatSuccessCallback(imageUrlOrData, originalRequestId, generationMetadata = {}) {
    const payload = {
        request_id: originalRequestId,
        status: "completed",
        metadata: generationMetadata || {} // Ensure metadata is an object even if empty
    };

    if (!imageUrlOrData) {
        // This case should ideally be caught before calling formatSuccessCallback
        console.error(`[ERROR] formatSuccessCallback called with no imageUrlOrData for requestId: ${originalRequestId}`);
        return formatErrorCallback("Image generation reported success but no image URL or data was provided by the workflow.", "INTERNAL_WORKFLOW_NO_IMAGE_ON_SUCCESS", originalRequestId);
    }

    // Determine if it's a base64 data URI or a plain URL
    if (imageUrlOrData.startsWith('data:image')) {
        payload.image_data = imageUrlOrData; // Odoo field for base64 data
    } else {
        payload.image_url = imageUrlOrData; // Odoo field for URL
    }

    return payload;
}

/**
 * Formats the payload to be sent back to Odoo's callback API on failure.
 * @param {string} errorMessage - Description of the error.
 * @param {string} [errorCode='N8N_UNKNOWN_ERROR'] - A code identifying the error type.
 * @param {string} originalRequestId - The `request_id` from the initial Odoo request.
 * @returns {object} JSON payload for Odoo callback on failure.
 */
function formatErrorCallback(errorMessage, errorCode, originalRequestId) {
    return {
        request_id: originalRequestId,
        status: "failed",
        error: {
            message: errorMessage || "An unspecified error occurred in the N8N workflow.",
            code: errorCode || "N8N_UNKNOWN_ERROR"
        }
    };
}