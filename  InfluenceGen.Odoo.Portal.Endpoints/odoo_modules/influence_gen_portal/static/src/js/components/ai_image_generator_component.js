odoo.define('influence_gen_portal.AIImageGeneratorComponent', function (require) {
'use strict';

const { Component, useState, onWillStart, onWillUnmount, useRef } = owl;
const { _t } = require("@web/core/l10n/translation");
const rpc = require('web.rpc'); // Using Odoo's rpc for service calls
// Assuming ai_image_service is registered and accessible via env or RPC.
// For simplicity, direct RPC calls will be made to controller endpoints defined for ai_image_service.

class AIImageGeneratorComponent extends Component {
    static template = "influence_gen_portal.AIImageGeneratorComponentTemplate";

    static props = {
        initialQuota: { type: Object, optional: true }, // { used: number, total: number }
        defaultParams: { type: Object, optional: true }, // Default generation parameters
        paramRanges: { type: Object, optional: true }, // Allowed ranges/options for parameters
    };

    static defaultProps = {
        initialQuota: { used: 0, total: 0 },
        defaultParams: {
            resolution: "1024x1024",
            aspect_ratio: "1:1",
            model_id: null, // This should be set after fetching models
            seed: -1, // -1 often means random
            steps: 30,
            cfg_scale: 7.5,
            intended_use: "personal",
            campaign_id: null,
        },
        paramRanges: { // Example ranges, should be fetched or configured
            steps: { min: 10, max: 150, step: 1 },
            cfg_scale: { min: 1.0, max: 20.0, step: 0.5 },
            // resolutions: ["512x512", "1024x1024", "1024x1536", "1536x1024"],
            // aspect_ratios: ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]
        },
    };

    setup() {
        this.state = useState({
            prompt: "",
            negativePrompt: "",
            generationParams: { ...AIImageGeneratorComponent.defaultProps.defaultParams, ...(this.props.defaultParams || {}) },
            availableModels: [], // { id: 'uuid', name: 'Model Name' }
            generatedImages: [], // { id: 'img_uuid', url: '...', requestId: 'req_uuid', status: 'completed' }
            isLoading: false,
            errorMessage: "",
            quotaStatus: { ...AIImageGeneratorComponent.defaultProps.initialQuota, ...(this.props.initialQuota || {}) },
            savedPrompts: [], // { id: 'uuid', text: 'Prompt text' }
            templatePrompts: [], // { id: 'uuid', text: 'Prompt text' }
            activeRequestId: null,
            pollingAttempt: 0,
            currentJobStatus: "", // e.g. "Queued", "Processing: 20%", "Completed"
        });

        this.pollingInterval = 5000; // 5 seconds
        this.maxPollingAttempts = 24; // 2 minutes total
        this.pollingTimeoutId = null;

        this.imageGalleryRef = useRef("imageGallery");

        onWillStart(async () => {
            await this._loadInitialData();
        });

        onWillUnmount(() => {
            if (this.pollingTimeoutId) {
                clearTimeout(this.pollingTimeoutId);
            }
        });
    }

    async _loadInitialData() {
        this.state.isLoading = true;
        try {
            const [models, savedPrompts, templatePrompts] = await Promise.all([
                rpc.query({ route: '/my/ai/models', method: 'GET' }),
                rpc.query({ route: '/my/ai/prompts/saved', method: 'GET' }),
                rpc.query({ route: '/my/ai/prompts/templates', method: 'GET' }) // Assuming this endpoint exists
            ]);

            this.state.availableModels = models || [];
            if (this.state.availableModels.length > 0 && !this.state.generationParams.model_id) {
                this.state.generationParams.model_id = this.state.availableModels[0].id;
            }
            this.state.savedPrompts = savedPrompts || [];
            this.state.templatePrompts = templatePrompts || [];

        } catch (error) {
            console.error("Error loading initial AI generator data:", error);
            this.state.errorMessage = _t("Failed to load initial configuration. Please try again later.");
            this.env.services.notification.add(this.state.errorMessage, { type: 'danger' });
        } finally {
            this.state.isLoading = false;
        }
    }

    _clientSidePromptCheck(promptText) {
        // Basic client-side check for obviously problematic content.
        // The main validation and moderation is server-side.
        const forbiddenKeywords = ["explicit_word1", "harmful_topic_x"]; // Example
        for (const keyword of forbiddenKeywords) {
            if (promptText.toLowerCase().includes(keyword)) {
                return _t("Your prompt may contain restricted content. Please revise it. Server-side validation will also apply.");
            }
        }
        return null;
    }

    async generateImage() {
        this.state.isLoading = true;
        this.state.errorMessage = "";
        this.state.generatedImages = [];
        this.state.activeRequestId = null;
        this.state.pollingAttempt = 0;
        this.state.currentJobStatus = _t("Initiating generation...");

        const moderationWarning = this._clientSidePromptCheck(this.state.prompt);
        if (moderationWarning) {
            this.state.errorMessage = moderationWarning;
            this.env.services.notification.add(this.state.errorMessage, { type: 'warning', sticky: true });
            this.state.isLoading = false;
            this.state.currentJobStatus = "";
            return;
        }

        if (!this.state.generationParams.model_id && this.state.availableModels.length > 0) {
             this.state.generationParams.model_id = this.state.availableModels[0].id;
        } else if (!this.state.generationParams.model_id) {
            this.state.errorMessage = _t("No AI model selected or available.");
            this.env.services.notification.add(this.state.errorMessage, { type: 'danger' });
            this.state.isLoading = false;
            this.state.currentJobStatus = "";
            return;
        }


        const params = {
            prompt: this.state.prompt,
            negative_prompt: this.state.negativePrompt,
            ...this.state.generationParams,
        };

        try {
            const result = await rpc.query({
                route: '/my/ai/generate',
                method: 'POST',
                params: params,
            });

            if (result.error) {
                this._handleGenerationError(result.error);
            } else if (result.request_id) {
                this.state.activeRequestId = result.request_id;
                this.state.currentJobStatus = _t("Request queued (ID: %s)", result.request_id);
                this._pollGenerationStatus();
            } else {
                 this._handleGenerationError({ message: _t("Unknown error during initiation.") });
            }
        } catch (error) {
            console.error("Error initiating AI image generation:", error);
            this._handleGenerationError(error.data || error, _t("Failed to initiate image generation."));
        }
    }

    async _pollGenerationStatus() {
        if (!this.state.activeRequestId) return;
        if (this.pollingTimeoutId) clearTimeout(this.pollingTimeoutId);

        this.state.pollingAttempt++;
        if (this.state.pollingAttempt > this.maxPollingAttempts) {
            this._handleGenerationError({ message: _t("Image generation timed out. Please check your gallery later or try again.") });
            return;
        }
        
        try {
            const statusResult = await rpc.query({
                route: '/my/ai/generate/status',
                method: 'GET',
                params: { request_id: this.state.activeRequestId },
            });

            if (statusResult.error) {
                 this._handleGenerationError(statusResult.error);
            } else {
                this.state.currentJobStatus = _t("Status: %s", statusResult.status_message || statusResult.status);
                switch (statusResult.status) {
                    case 'completed':
                        this._handleGenerationResult(statusResult);
                        break;
                    case 'failed':
                        this._handleGenerationError(statusResult);
                        break;
                    case 'processing':
                    case 'queued':
                        this.pollingTimeoutId = setTimeout(() => this._pollGenerationStatus(), this.pollingInterval);
                        break;
                    default:
                        console.warn("Unknown generation status:", statusResult.status);
                        this.pollingTimeoutId = setTimeout(() => this._pollGenerationStatus(), this.pollingInterval);
                }
                 if (statusResult.quota) {
                    this.state.quotaStatus = statusResult.quota;
                }
            }
        } catch (error) {
            console.error("Error polling generation status:", error);
            // Don't call _handleGenerationError directly to avoid stopping polling on transient network issues
            // unless it's a specific "request not found" type error from backend.
            // For now, continue polling on generic catch.
            this.pollingTimeoutId = setTimeout(() => this._pollGenerationStatus(), this.pollingInterval * 2); // Longer delay on error
        }
    }

    _handleGenerationResult(result) {
        this.state.isLoading = false;
        this.state.generatedImages = result.images || [];
        if (result.quota) {
            this.state.quotaStatus = result.quota;
        }
        this.state.currentJobStatus = _t("Generation completed!");
        this.env.services.notification.add(_t("Image generation successful!"), { type: 'success' });
        if (this.imageGalleryRef.el) {
            this.imageGalleryRef.el.scrollIntoView({ behavior: 'smooth' });
        }
    }

    _handleGenerationError(errorData, customMessage = null) {
        this.state.isLoading = false;
        const message = customMessage || errorData.message || errorData.error_message || _t("Image generation failed. Please try again.");
        this.state.errorMessage = message;
        this.state.currentJobStatus = _t("Failed: %s", message);
        this.env.services.notification.add(message, { type: 'danger', sticky: true });
        this.state.activeRequestId = null; // Stop polling
    }

    downloadImage(imageUrl, imageName = 'generated_image.png') {
        const link = document.createElement('a');
        link.href = imageUrl;
        link.setAttribute('download', imageName);
        link.setAttribute('target', '_blank'); // Open in new tab might be better for some browsers/setups
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    useImageInCampaign(image) {
        // This function will emit an event that parent components or pages can listen to.
        // The actual logic of associating the image with a campaign might involve opening a modal,
        // navigating to a submission form with the image pre-selected, etc.
        this.trigger('use-image-in-campaign', { image: image });
        this.env.services.notification.add(_t("Functionality to use image '%s' in a campaign to be implemented.", image.id), { type: 'info' });
        // console.log("Use image in campaign:", image);
        // TODO: Further integration with campaign content submission may involve calling a service or navigating.
    }

    async savePrompt() {
        if (!this.state.prompt.trim()) {
            this.env.services.notification.add(_t("Prompt cannot be empty."), { type: 'warning' });
            return;
        }
        try {
            const newPrompt = await rpc.query({
                route: '/my/ai/prompts/save',
                method: 'POST',
                params: { prompt: this.state.prompt },
            });
            if(newPrompt) {
                this.state.savedPrompts.push(newPrompt); // Assuming backend returns the saved prompt object with ID
                 this.env.services.notification.add(_t("Prompt saved successfully!"), { type: 'success' });
            } else {
                this.env.services.notification.add(_t("Failed to save prompt. Backend did not return prompt."), { type: 'warning' });
            }

        } catch (error) {
            console.error("Error saving prompt:", error);
            const message = error.data?.message || _t("Failed to save prompt.");
            this.env.services.notification.add(message, { type: 'danger' });
        }
    }

    reusePrompt(promptText) {
        this.state.prompt = promptText;
        this.env.services.notification.add(_t("Prompt loaded into input field."), { type: 'info' });
    }

    _updateParam(paramName, value) {
        // Type coercion for numbers if input type is "number"
        const inputElement = this.el.querySelector(`[data-param="${paramName}"]`);
        if (inputElement && inputElement.type === "number") {
             if (value === "") { // Allow clearing number fields if appropriate
                this.state.generationParams[paramName] = null; // Or some default like 0 or props.defaultParams[paramName]
                return;
            }
            const numValue = parseFloat(value);
            if (!isNaN(numValue)) {
                 // Enforce min/max from paramRanges if available
                if (this.props.paramRanges && this.props.paramRanges[paramName]) {
                    const range = this.props.paramRanges[paramName];
                    if (numValue < range.min) {
                        this.state.generationParams[paramName] = range.min;
                        this.env.services.notification.add(_t("%s cannot be less than %s.", paramName, range.min), { type: 'warning' });
                        return;
                    }
                    if (numValue > range.max) {
                        this.state.generationParams[paramName] = range.max;
                        this.env.services.notification.add(_t("%s cannot be more than %s.", paramName, range.max), { type: 'warning' });
                        return;
                    }
                }
                this.state.generationParams[paramName] = numValue;
                return;
            }
        }
        this.state.generationParams[paramName] = value;
    }

    get quotaPercentage() {
        if (this.state.quotaStatus.total > 0) {
            return (this.state.quotaStatus.used / this.state.quotaStatus.total) * 100;
        }
        return 0;
    }
}

return AIImageGeneratorComponent;
});