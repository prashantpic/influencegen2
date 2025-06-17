```javascript
/**
 * lib/ai_service_adapter.js
 * Helper JavaScript module for adapting requests to various AI service APIs.
 * Assumes this code is "prepended" to N8N Function nodes, making the
 * ai_service_adapter object globally available.
 */

function _formatForComfyUI(odooRequestParams, modelName) {
    // This is a highly simplified placeholder.
    // A real ComfyUI adapter would load a workflow template JSON and inject parameters.
    const { prompt, negativePrompt, resolution, seed, steps, cfgScale } = odooRequestParams;
    let width = 1024, height = 1024; // Default
    if (resolution && resolution.includes('x')) {
        [width, height] = resolution.split('x').map(Number);
    }

    // Example: A very basic ComfyUI API prompt structure.
    // Node IDs (e.g., "3", "6", "7") are specific to a pre-defined ComfyUI workflow.
    const workflow = {
        "3": { // KSampler
            "inputs": {
                "seed": seed || Math.floor(Math.random() * 10000000000),
                "steps": steps || 20,
                "cfg": cfgScale || 8.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["4", 0], // Link to CheckpointLoaderSimple
                "positive": ["6", 0], // Link to CLIPTextEncode (Positive)
                "negative": ["7", 0], // Link to CLIPTextEncode (Negative)
                "latent_image": ["5", 0] // Link to EmptyLatentImage
            },
            "class_type": "KSampler"
        },
        "4": { // CheckpointLoaderSimple
            "inputs": { "ckpt_name": modelName || "sd_xl_base_1.0.safetensors" }, // modelName should map to a checkpoint file
            "class_type": "CheckpointLoaderSimple"
        },
        "5": { // EmptyLatentImage
            "inputs": { "width": width, "height": height, "batch_size": 1 },
            "class_type": "EmptyLatentImage"
        },
        "6": { // CLIPTextEncode (Positive)
            "inputs": { "text": prompt, "clip": ["4", 1] },
            "class_type": "CLIPTextEncode"
        },
        "7": { // CLIPTextEncode (Negative)
            "inputs": { "text": negativePrompt || "", "clip": ["4", 1] },
            "class_type": "CLIPTextEncode"
        },
        "8": { // VAEDecode
             "inputs": { "samples": ["3", 0], "vae": ["4", 2] },
             "class_type": "VAEDecode"
        },
        "9": { // SaveImage or PreviewImage (PreviewImage is often used for API)
            "inputs": { "images": ["8", 0] }, // Output from VAEDecode
            "class_type": "PreviewImage" // Or SaveImage, depending on ComfyUI setup
        }
    };
    return { prompt: workflow, client_id: `n8n-influencegen-${new Date().getTime()}` };
}

function _formatForStabilityAI(odooRequestParams, modelName) {
    // Based on Stability AI API v1 text-to-image, adjust for v2 or specific model requirements (e.g. SD3)
    const { prompt, negativePrompt, resolution, aspectRatio, seed, steps, cfgScale } = odooRequestParams;
    let width = 1024, height = 1024; // Default

    if (resolution && resolution.includes('x')) {
        [width, height] = resolution.split('x').map(Number);
    } else if (aspectRatio) {
        // Simple aspect ratio handling, might need more robust logic
        const [arW, arH] = aspectRatio.split(':').map(Number);
        if (arW === 1 && arH === 1) { width = 1024; height = 1024; }
        else if (arW === 16 && arH === 9) { width = 1344; height = 768; } // Example for 16:9
        else if (arW === 9 && arH === 16) { width = 768; height = 1344; } // Example for 9:16
        // Add more aspect ratios or calculate based on a fixed area
    }
    
    const text_prompts = [{ text: prompt, weight: 1.0 }];
    if (negativePrompt) {
        text_prompts.push({ text: negativePrompt, weight: -1.0 });
    }

    const payload = {
        text_prompts: text_prompts,
        cfg_scale: cfgScale || 7,
        steps: steps || 30, // For SD3, 30-50 is typical.
        seed: seed || 0, // 0 for random
        // For SD v1/v2
        // height: height,
        // width: width,
        // samples: 1,
        // For SD3, use aspect_ratio parameter or width/height if model supports it
        // model: modelName || "sd3-medium", // or sd3-large, sd3-large-turbo
        aspect_ratio: aspectRatio || `${width}:${height}`, // SD3 prefers aspect_ratio
    };
    
    // If modelName explicitly states SD3 or other specific model, adjust payload keys
    // For example, SD3 might take 'model' in payload or use a different endpoint
    // This example payload is more generic or for SD1.5/SDXL via Stability API.
    // For a specific model like 'stable-image-generate-sd3', the payload might be different:
    // payload.model = modelName; (e.g. "sd3-medium")
    // delete payload.height; delete payload.width; if aspect_ratio is used.

    return payload;
}

const ai_service_adapter = {
    adaptToAIService: function(odooRequestParams, targetAIServiceType, modelName) {
        const serviceTypeUpper = targetAIServiceType.toUpperCase();
        switch (serviceTypeUpper) {
            case 'COMFY_UI':
                return _formatForComfyUI(odooRequestParams, modelName);
            case 'STABILITY_AI':
                return _formatForStabilityAI(odooRequestParams, modelName);
            // Add other AI services here
            default:
                // Fallback to a generic structure or throw error
                // For now, let's try a generic approach similar to StabilityAI
                // but this should ideally throw an error.
                // throw new Error(`Unsupported AI service type for adaptation: ${targetAIServiceType}`);
                console.warn(`[AI ADAPTER] Unsupported AI service type '${targetAIServiceType}', attempting generic StabilityAI format.`);
                return _formatForStabilityAI(odooRequestParams, modelName);
        }
    },

    getAIServiceEndpoint: function(targetAIServiceType, modelName) {
        // Base URLs should come from environment variables in a real setup
        const serviceTypeUpper = targetAIServiceType.toUpperCase();
        switch (serviceTypeUpper) {
            case 'COMFY_UI':
                // return process.env.AI_SERVICE_ENDPOINT_COMFY_UI || 'http://localhost:8188/prompt';
                 return (typeof process !== 'undefined' && process.env && process.env.AI_SERVICE_ENDPOINT_COMFY_UI) || 'http://localhost:8188/prompt';

            case 'STABILITY_AI':
                // Example for SD3. Adjust if using other models/versions.
                // return process.env.AI_SERVICE_ENDPOINT_STABILITY_AI || `https://api.stability.ai/v2beta/stable-image/generate/sd3`;
                // More general v1 endpoint:
                // return (typeof process !== 'undefined' && process.env && process.env.AI_SERVICE_ENDPOINT_STABILITY_AI) || `https://api.stability.ai/v1/generation/${modelName || 'stable-diffusion-xl-1024-v1-0'}`;
                 return (typeof process !== 'undefined' && process.env && process.env.AI_SERVICE_ENDPOINT_STABILITY_AI) || `https://api.stability.ai/v2beta/stable-image/generate/${modelName || 'sd3-medium'}`;

            default:
                throw new Error(`Unknown AI service type for endpoint: ${targetAIServiceType}`);
        }
    },

    getAIServiceAuthHeaders: function(targetAIServiceType, credentialsObject) {
        // This function is less critical if N8N's HTTP Request node handles auth directly via credentials.
        // It's useful if complex header construction is needed beyond standard auth types.
        const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' };
        const serviceTypeUpper = targetAIServiceType.toUpperCase();

        switch (serviceTypeUpper) {
            case 'STABILITY_AI':
                if (credentialsObject && credentialsObject.apiKey) { // Assuming N8N credential has 'apiKey'
                    headers['Authorization'] = `Bearer ${credentialsObject.apiKey}`;
                } else {
                    // Fallback to env var if no credential object or apiKey field (less secure)
                    // const apiKey = process.env.STABILITY_API_KEY;
                    // if (apiKey) headers['Authorization'] = `Bearer ${apiKey}`;
                    // else console.warn('[AI ADAPTER] Stability AI API key not found in credentials or environment.');
                    console.warn('[AI ADAPTER] Stability AI API key not configured in credential object properly.');
                }
                break;
            case 'COMFY_UI':
                // ComfyUI usually doesn't require auth by default if exposed directly,
                // but can be secured with a proxy or custom components.
                // Add auth headers if your ComfyUI setup requires them.
                // Example: if (credentialsObject && credentialsObject.comfyApiKey) {
                //    headers['X-Comfy-Api-Key'] = credentialsObject.comfyApiKey;
                // }
                break;
            default:
                // No specific auth headers for unknown services by default
                break;
        }
        return headers;
    }
};
```