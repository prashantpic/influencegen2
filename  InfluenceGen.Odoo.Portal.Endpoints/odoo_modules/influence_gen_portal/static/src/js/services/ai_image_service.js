odoo.define('influence_gen_portal.services.aiImage', function (require) {
    'usestrict';

    const portalService = require('influence_gen_portal.services.portal');

    const aiImageService = {
        /**
         * Initiates AI image generation.
         * @param {Object} params - Parameters for generation (prompt, negativePrompt, modelId, etc.)
         * @returns {Promise<Object>} Promise resolving to {request_id, status}
         */
        async initiateGeneration(params) {
            return portalService.rpc('/my/ai/generate', params, 'POST');
        },

        /**
         * Checks the status of an ongoing AI image generation request.
         * @param {string} requestId - The ID of the generation request.
         * @returns {Promise<Object>} Promise resolving to {request_id, status, images?, error_message?}
         */
        async checkGenerationStatus(requestId) {
            return portalService.rpc('/my/ai/generate/status', { request_id: requestId }, 'GET');
        },

        /**
         * Fetches available AI models.
         * @returns {Promise<Array>} Promise resolving to an array of model objects.
         */
        async getAvailableModels() {
            // This route needs to be implemented in portal_ai_image_controller.py
            return portalService.rpc('/my/ai/models', {}, 'GET');
        },

        /**
         * Fetches the current user's saved prompts.
         * @returns {Promise<Array>} Promise resolving to an array of prompt strings or objects.
         */
        async getSavedPrompts() {
            // This route needs to be implemented in portal_ai_image_controller.py or a dedicated prompt controller
            return portalService.rpc('/my/ai/prompts/saved', {}, 'GET');
        },

        /**
         * Saves a prompt for the current user.
         * @param {string} promptText - The prompt text to save.
         * @returns {Promise<void>}
         */
        async saveUserPrompt(promptText) {
            // This route needs to be implemented
            return portalService.rpc('/my/ai/prompts/save', { prompt: promptText }, 'POST');
        },
        
        /**
         * Fetches admin-defined template prompts.
         * @returns {Promise<Array>} Promise resolving to an array of template prompt strings or objects.
         */
        async getTemplatePrompts() {
            // This route needs to be implemented
            return portalService.rpc('/my/ai/prompts/templates', {}, 'GET');
        }
    };

    return aiImageService;
});