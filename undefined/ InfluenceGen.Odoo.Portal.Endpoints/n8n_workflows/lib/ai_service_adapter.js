/**
 * lib/ai_service_adapter.js
 * Helper JavaScript module for adapting requests to various AI service APIs.
 */

/**
 * Adapts the parsed Odoo request parameters to the specific API format of the target AI service.
 * @param {object} odooRequestParams - Parsed parameters from Odoo (e.g., prompt, negativePrompt, seed, steps, resolution, width, height, cfgScale, specificModelIdentifierFromOdoo).
 * @param {string} targetAIServiceType - Identifier for the AI service (e.g., 'COMFY_UI', 'STABILITY_AI').
 * @param {string} modelName - Specific model/LoRA identifier for the AI service (e.g. externalModelId from AIImageModel table).
 * @returns {object} The payload formatted for the target AI service API.
 * @throws {Error} If the AI service type is unknown or adaptation fails.
 */
function adaptToAIService(odooRequestParams, targetAIServiceType, modelName) {
    // Ensure modelName from Odoo payload (which is AIImageModel.name) is used if externalModelId is not present or relevant.
    // The modelName parameter here typically refers to AIImageModel.externalModelId if the AI service uses its own ID,
    // or AIImageModel.name if that's what the AI service expects (e.g., ComfyUI checkpoint file name).

    switch (targetAIServiceType.toUpperCase()) {
        case 'STABILITY_AI':
            return _formatForStabilityAI(odooRequestParams, modelName); // modelName here would be Stability's model ID
        case 'COMFY_UI':
            return _formatForComfyUI(odooRequestParams, modelName); // modelName here would be the ComfyUI checkpoint/workflow name
        // Add cases for other AI services here
        default:
            throw new Error(`Unsupported AI service type: ${targetAIServiceType}`);
    }
}

/**
 * Returns the full API endpoint URL for the AI service.
 * @param {string} targetAIServiceType - Identifier for the AI service.
 * @param {string} [modelName] - Optional, specific model identifier if it affects the endpoint (e.g., part of the path for some Stability AI models).
 * @returns {string} The full API endpoint URL.
 * @throws {Error} If the AI service type is unknown or the endpoint is not configured.
 */
function getAIServiceEndpoint(targetAIServiceType, modelName) {
    let baseUrl;
    let path = '';

    switch (targetAIServiceType.toUpperCase()) {
        case 'STABILITY_AI':
            baseUrl = process.env.AI_SERVICE_ENDPOINT_STABILITY_AI; // e.g., "https://api.stability.ai"
            // Example path for Stability AI v2 text-to-image (Stable Image Core)
            // modelName here could be 'stable-image-core' or a specific fine-tuned model ID
            path = `/v2beta/stable-image/generate/core`;
            // If modelName implies a different endpoint, adjust path:
            // if (modelName === 'sd3-turbo') path = `/v2beta/stable-image/generate/sd3`;
            break;
        case 'COMFY_UI':
            baseUrl = process.env.AI_SERVICE_ENDPOINT_COMFY_UI; // e.g., "http://localhost:8188"
            path = `/prompt`; // Standard ComfyUI API endpoint for submitting workflows
            break;
        default:
            throw new Error(`Unsupported AI service type: ${targetAIServiceType} for endpoint retrieval.`);
    }

    if (!baseUrl) {
        throw new Error(`AI service endpoint base URL not configured for type: ${targetAIServiceType} (check environment variable AI_SERVICE_ENDPOINT_${targetAIServiceType.toUpperCase()}).`);
    }

    // Ensure baseUrl does not end with / if path starts with /
    if (baseUrl.endsWith('/') && path.startsWith('/')) {
        return `${baseUrl.slice(0, -1)}${path}`;
    }
    if (!baseUrl.endsWith('/') && !path.startsWith('/')) {
         return `${baseUrl}/${path}`;
    }
    return `${baseUrl}${path}`;
}

/**
 * Constructs HTTP headers for authentication for the AI service.
 * This function is less critical if N8N's HTTP Request node's built-in credential handling is sufficient.
 * It's provided for completeness or if specific header construction is needed beyond simple API key injection.
 * @param {string} targetAIServiceType - Identifier for the AI service.
 * @param {object} credentialsObject - N8N credentials object for the service (e.g., from $credentials).
 * @returns {object} HTTP headers object.
 */
function getAIServiceAuthHeaders(targetAIServiceType, credentialsObject) {
    const headers = {
        'Content-Type': 'application/json', // Default, many AI APIs use JSON
        'Accept': 'application/json', // Default, expect JSON response
    };

    switch (targetAIServiceType.toUpperCase()) {
        case 'STABILITY_AI':
            if (credentialsObject && credentialsObject.apiKey) {
                headers['Authorization'] = `Bearer ${credentialsObject.apiKey}`;
                // Stability AI might prefer 'image/*' or 'application/json' based on endpoint
                // For generate/core, 'application/json' or 'multipart/form-data' for request, 'image/*' or 'application/json' for accept.
                // Assuming JSON request for this example, Accept header is important for response type.
                headers['Accept'] = 'application/json; type=image/png'; // Request PNG image, can also be 'image/*'
            } else {
                console.warn(`[WARN] Stability AI credentials (apiKey) not found in credentialsObject for ${targetAIServiceType}.`);
            }
            break;
        case 'COMFY_UI':
            // ComfyUI usually does not require authentication for its basic API if exposed directly on a trusted network.
            // If authentication is implemented (e.g., via a proxy or custom ComfyUI nodes), add headers here.
            // Example: if (credentialsObject && credentialsObject.apiKey) { headers['X-Comfy-Api-Key'] = credentialsObject.apiKey; }
            break;
        default:
            // No specific auth headers defined for this service type
            break;
    }
    return headers;
}

// --- Internal Helper Functions for Payload Formatting ---

/**
 * Internal helper to format payload for Stability AI (Stable Image Core).
 * @param {object} params - Odoo request parameters from parseAndValidateOdooWebhook.
 * @param {string} modelName - Specific model identifier (Stability's model ID, e.g., 'stable-image-core').
 * @returns {object} Stability AI API payload (multipart/form-data structure).
 */
function _formatForStabilityAI(params, modelName) {
    // Stability AI Stable Image Core API uses multipart/form-data
    // This function will return an object that N8N's HTTP Request node
    // can use when "Body Content Type" is "Form-Data (Multipart)".
    // N8N Function nodes cannot directly create multipart/form-data bodies with binary data easily.
    // The HTTP Request node should handle this. This function prepares the fields.

    const formData = {
        prompt: params.prompt,
    };

    if (params.negativePrompt) {
        formData.negative_prompt = params.negativePrompt;
    }

    // Resolution and Aspect Ratio:
    // Stability AI uses aspect_ratio string (e.g., "1:1", "16:9")
    // or explicit width/height for some models/endpoints.
    // For Stable Image Core, aspect_ratio is preferred.
    if (params.aspectRatio) {
        formData.aspect_ratio = params.aspectRatio;
    } else if (params.resolution) { // Fallback if aspectRatio not directly provided by Odoo
        const [width, height] = params.resolution.split('x').map(Number);
        // Convert to common aspect ratios if possible or pass width/height if API supports
        // This is a simplification; a more robust mapping might be needed.
        if (width === height) formData.aspect_ratio = "1:1";
        else if (width / height === 16 / 9) formData.aspect_ratio = "16:9";
        // ... other common ratios
        // Note: For Stable Image Core, width/height are not direct top-level params.
        // It primarily uses aspect_ratio. If exact resolution is needed, a different model/endpoint or
        // post-generation scaling might be required.
    }


    if (params.seed !== undefined && params.seed !== null) {
        formData.seed = parseInt(params.seed, 10);
    }
    if (params.steps !== undefined && params.steps !== null) {
        // Stability's 'steps' is under model-specific settings or inferred.
        // For /core, it's not a direct top-level param. Adjust if using other endpoints.
        // formData.steps = parseInt(params.steps, 10);
    }
    if (params.cfgScale !== undefined && params.cfgScale !== null) {
        formData.cfg_scale = parseFloat(params.cfgScale);
    }

    // modelName is usually part of the URL for Stability AI or implicit to the endpoint
    // formData.model = modelName; // Only if API expects model in body

    // Output format: e.g., 'png', 'jpeg', 'webp'
    formData.output_format = 'png'; // Or 'jpeg' for smaller files, 'webp'

    // This is a simplified representation. For multipart/form-data, N8N's HTTP node
    // would take these as fields. If binary data (like init_image) were involved,
    // it would need special handling in N8N.
    // Since this is text-to-image, the payload is simpler.
    return formData; // N8N will send this as multipart/form-data fields
}

/**
 * Internal helper to format payload for ComfyUI.
 * @param {object} params - Odoo request parameters from parseAndValidateOdooWebhook.
 * @param {string} modelName - Specific model/workflow identifier (e.g., checkpoint file name like "sd_xl_base_1.0.safetensors").
 * @returns {object} ComfyUI API payload (workflow JSON wrapped).
 */
function _formatForComfyUI(params, modelName) {
    // This is a placeholder for a minimal ComfyUI workflow.
    // A real implementation would:
    // 1. Load a template workflow JSON (from a file, env variable, or hardcoded).
    // 2. Dynamically update specific node parameters within that template.
    // Node IDs (e.g., "3", "6", "7") are specific to a ComfyUI workflow JSON.

    // Example minimal workflow structure (highly simplified):
    const workflow = {
        // Checkpoint Loader Node (ID: 4)
        "4": {
            "inputs": { "ckpt_name": modelName }, // modelName is the checkpoint filename
            "class_type": "CheckpointLoaderSimple",
            "_meta": { "title": "Load Checkpoint" }
        },
        // Positive Prompt Node (ID: 6)
        "6": {
            "inputs": { "text": params.prompt, "clip": ["4", 1] }, // "clip" from CheckpointLoaderSimple
            "class_type": "CLIPTextEncode",
            "_meta": { "title": "Positive Prompt" }
        },
        // Negative Prompt Node (ID: 7)
        "7": {
            "inputs": { "text": params.negativePrompt || "", "clip": ["4", 1] },
            "class_type": "CLIPTextEncode",
            "_meta": { "title": "Negative Prompt" }
        },
        // Empty Latent Image Node (ID: 5)
        "5": {
            "inputs": {
                "width": 1024, // Default, will be updated
                "height": 1024, // Default, will be updated
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage",
            "_meta": { "title": "Empty Latent Image" }
        },
        // KSampler Node (ID: 3)
        "3": {
            "inputs": {
                "model": ["4", 0], // "model" from CheckpointLoaderSimple
                "positive": ["6", 0], // "CONDITIONING" from Positive Prompt
                "negative": ["7", 0], // "CONDITIONING" from Negative Prompt
                "latent_image": ["5", 0], // "LATENT" from EmptyLatentImage
                "seed": params.seed !== undefined ? parseInt(params.seed, 10) : Math.floor(Math.random() * 10000000000000000),
                "steps": params.steps !== undefined ? parseInt(params.steps, 10) : 25,
                "cfg": params.cfgScale !== undefined ? parseFloat(params.cfgScale) : 7.0,
                "sampler_name": "euler", // Or other samplers
                "scheduler": "normal", // Or other schedulers
                "denoise": 1.0,
            },
            "class_type": "KSampler",
            "_meta": { "title": "KSampler" }
        },
        // VAE Decode Node (ID: 8)
        "8": {
            "inputs": { "samples": ["3", 0], "vae": ["4", 2] }, // "samples" from KSampler, "vae" from CheckpointLoaderSimple
            "class_type": "VAEDecode",
            "_meta": { "title": "VAE Decode" }
        },
        // Save Image Node (ID: 9) - This node determines the output.
        // For API usage, a node like "APIOutput" or "PreviewImage" (if it returns data) might be better
        // than "SaveImage" which writes to disk on the ComfyUI server.
        // For this example, we'll assume "SaveImage" node, and the ComfyUI API provides output info.
        "9": {
            "inputs": { "images": ["8", 0], "filename_prefix": "N8N_InfluenceGen" }, // "images" from VAEDecode
            "class_type": "SaveImage", // Or "PreviewImage" if you want base64 data directly in response (sometimes)
            "_meta": { "title": "Save Image (Output)" }
        }
    };

    // Update width and height in EmptyLatentImage node (ID: 5) based on Odoo's resolution
    if (params.resolution) {
        const [width, height] = params.resolution.split('x').map(Number);
        if (!isNaN(width) && !isNaN(height) && workflow["5"]) {
            workflow["5"].inputs.width = width;
            workflow["5"].inputs.height = height;
        }
    } else if (params.width && params.height && workflow["5"]) { // If Odoo sends width/height separately
         workflow["5"].inputs.width = parseInt(params.width, 10);
         workflow["5"].inputs.height = parseInt(params.height, 10);
    }


    // The actual payload for ComfyUI's /prompt endpoint
    const payload = {
        prompt: workflow,
        client_id: `n8n-influencegen-${new Date().getTime()}` // Optional: A unique client ID for tracking
        // 'extra_data': { 'status_endpoint': '...' } // If using ComfyUI-Manager or similar for progress
    };

    return payload;
}