/** @odoo-module */

import { Service } from "@web/core/webclient/service";
// No direct useService here, it's a class to be instantiated by the registry
// However, its methods will use the portalService which in turn uses core services.

class AiImageService extends Service {
     // The portalService dependency is injected by the service registry
     get portalService() {
         return this.env.services["influence_gen_portal.services.portal"];
     }

    /**
     * Initiates an AI image generation request.
     * @param {Object} params - Generation parameters (prompt, negativePrompt, model_id, etc.).
     * @returns {Promise<{request_id: string, status: string}>} - Promise resolving with the request ID and initial status.
     * @throws {Error} - Throws an error if the initiation fails (e.g., validation error from backend).
     */
    async initiateGeneration(params) {
        return this.portalService.rpc('/my/ai/generate', params);
    }

    /**
     * Checks the status of an AI image generation request.
     * @param {string} requestId - The unique ID of the generation request.
     * @returns {Promise<{request_id: string, status: string, images?: Array<Object>, error_message?: string}>} - Promise resolving with the status details.
     * @throws {Error} - Throws an error if the status check fails.
     */
    async checkGenerationStatus(requestId) {
        return this.portalService.rpc('/my/ai/generate/status', { request_id: requestId });
    }

     /**
      * Fetches the list of available AI models.
      * @returns {Promise<Array<{id: any, name: string}>>} - Promise resolving with a list of available models.
      * @throws {Error}
      */
     async getAvailableModels() {
         return this.portalService.rpc('/my/ai/models', {});
     }

     /**
      * Fetches the user's saved prompts.
      * @returns {Promise<Array<{id: any, prompt_text: string}>>} - Promise resolving with a list of saved prompts.
      * @throws {Error}
      */
     async getSavedPrompts() {
         return this.portalService.rpc('/my/ai/prompts/saved', {});
     }

     /**
      * Saves a user's prompt.
      * @param {string} promptText - The prompt text to save.
      * @returns {Promise<void>}
      * @throws {Error}
      */
     async saveUserPrompt(promptText) {
         return this.portalService.rpc('/my/ai/prompts/save', { prompt: promptText });
     }
}

// Register the service
export const aiImageService = {
    dependencies: ["influence_gen_portal.services.portal"], // Declare dependency
    start(env, { portalService }) { // Dependency is injected here
        const serviceInstance = new AiImageService(env);
        // Manually assign dependencies if not using setup() for services (older style)
        // serviceInstance.portalService = portalService;
        return serviceInstance;
    }
};

// Alternative registration for Odoo's core service manager
// import { registry } from "@web/core/registry";
// registry.category("services").add("influence_gen_portal.services.aiImage", aiImageService);