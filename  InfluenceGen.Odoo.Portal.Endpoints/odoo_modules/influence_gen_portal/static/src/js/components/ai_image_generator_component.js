/** @odoo-module */

import { Component, useState, useRef, onWillStart, useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

const POLLING_INTERVAL = 3000; // Poll status every 3 seconds
const MAX_POLLING_ATTEMPTS = 60; // Stop polling after 3 minutes

export class AIImageGeneratorComponent extends Component {
    setup() {
        this.aiImageService = useService("influence_gen_portal.services.aiImage");
        this.notification = useService("notification");
        this.rpc = useService("rpc"); // Use Odoo's RPC for fetching initial data if not in props
        this.router = useService("router");


        this.state = useState({
            prompt: "",
            negativePrompt: "",
            generationParams: {
                 model_id: null, // Needs to be set from availableModels
                 resolution: "512x512", // Default, should come from props.defaultParams
                 aspect_ratio: "1:1",   // Default, should come from props.defaultParams
                 seed: -1,             // Default, should come from props.defaultParams
                 inference_steps: 30,  // Default, should come from props.defaultParams
                 cfg_scale: 7.0,       // Default, should come from props.defaultParams
                 intended_use: 'general', // Default
                 campaign_id: null,      // Optional, if linked to a campaign
            },
            availableModels: [],
            generatedImages: [], // [{ id, url, requestId, status, prompt_used }]
            isLoading: false,
            errorMessage: null,
            quotaStatus: { used: 0, total: 0, remaining: 0 }, // Initialize
            savedPrompts: [],
            templatePrompts: [], // Admin defined
            activeRequestId: null,
            pollingIntervalId: null,
            pollingAttempts: 0,
        });

        // Initialize generationParams from props
        if (this.props.defaultParams) {
            Object.assign(this.state.generationParams, this.props.defaultParams);
        }
        // Initialize quotaStatus from props
        if (this.props.initialQuota) {
            Object.assign(this.state.quotaStatus, this.props.initialQuota);
        }


        // Load initial data (models, prompts) when component starts
        onWillStart(async () => {
            await this._loadInitialData();
        });

        // Effect to manage polling when activeRequestId changes
        useEffect(() => {
            if (this.state.activeRequestId && !this.state.pollingIntervalId) {
                this._startPolling();
            } else if (!this.state.activeRequestId && this.state.pollingIntervalId) {
                this._stopPolling();
            }
             // Cleanup function to stop polling when component is unmounted or activeRequestId becomes null
            return () => this._stopPolling();
        }, () => [this.state.activeRequestId]); // Re-run effect when activeRequestId changes


         // Optional: Use effect to handle state changes from props if props can update dynamically
         useEffect(() => {
             if (this.props.initialQuota) {
                 Object.assign(this.state.quotaStatus, this.props.initialQuota);
             }
             if (this.props.defaultParams) {
                  Object.assign(this.state.generationParams, this.props.defaultParams);
             }
         }, () => [this.props.initialQuota, this.props.defaultParams, this.props.paramRanges]);
    }

    /**
     * Fetches initial data required for the component (models, prompts).
     */
    async _loadInitialData() {
         try {
             // Fetch available models
             const models = await this.aiImageService.getAvailableModels();
             this.state.availableModels = models;
             // Set default model if available
             if (models && models.length > 0 && !this.state.generationParams.model_id) {
                 this.state.generationParams.model_id = models[0].id;
             }

             // Fetch user's saved prompts
             const savedPromptsResult = await this.aiImageService.getSavedPrompts();
             this.state.savedPrompts = savedPromptsResult.map(p => p.prompt_text); // Assuming prompts come as objects with prompt_text

             // Fetch admin template prompts (needs a service method and backend controller)
             // const templatePrompts = await this.aiImageService.getTemplatePrompts();
             // this.state.templatePrompts = templatePrompts.map(p => p.prompt_text);

         } catch (error) {
             console.error("Error loading initial AI data:", error);
             this.notification.add(_t("Could not load AI models or prompts."), { type: 'danger' });
         }
    }

    /**
     * Initiates the image generation process.
     */
    async generateImage() {
        if (this.state.isLoading) {
            return; // Prevent double clicks
        }

         // Client-side prompt validation (e.g., not empty)
        if (!this.state.prompt || this.state.prompt.trim() === "") {
             this.state.errorMessage = _t("Prompt cannot be empty.");
             this.notification.add(this.state.errorMessage, { type: 'warning' });
             return;
        }

        // Check quota
        if (this.state.quotaStatus.remaining <= 0) {
            this.state.errorMessage = _t("You have no remaining image generation quota.");
            this.notification.add(this.state.errorMessage, { type: 'warning' });
            return;
        }

        this.state.errorMessage = null; // Clear previous error

        this.state.isLoading = true;
        this.state.generatedImages = []; // Clear previous results
        this.state.activeRequestId = null; // Clear previous request ID
        this.state.pollingAttempts = 0;

        try {
            // Call the AI image service to initiate generation
            const result = await this.aiImageService.initiateGeneration({
                prompt: this.state.prompt,
                negativePrompt: this.state.negativePrompt,
                 ...this.state.generationParams,
                // Add any other parameters needed by the backend
            });

            if (result && result.request_id) {
                this.state.activeRequestId = result.request_id;
                 // Polling starts via the useEffect hook
                this.notification.add(_t("Image generation request queued."), { type: 'info' });

            } else {
                 throw new Error(result.error || _t("Failed to queue image generation."));
            }

        } catch (error) {
             this._handleGenerationError(error);
        }
    }

    /**
     * Starts the polling process to check generation status.
     */
    _startPolling() {
         if (this.state.pollingIntervalId) {
              this._stopPolling(); // Ensure no duplicate intervals
         }
          console.info("Starting polling for AI generation request:", this.state.activeRequestId);
         this.state.pollingAttempts = 0;
         this.state.pollingIntervalId = setInterval(this._pollGenerationStatus.bind(this), POLLING_INTERVAL);
          // Perform initial check immediately
         this._pollGenerationStatus();
    }

    /**
     * Stops the polling process.
     */
    _stopPolling() {
         if (this.state.pollingIntervalId) {
              console.info("Stopping polling for AI generation request:", this.state.activeRequestId);
              clearInterval(this.state.pollingIntervalId);
              this.state.pollingIntervalId = null;
         }
          this.state.isLoading = false; // Generation finished (success/fail) or stopped
          // Do not reset activeRequestId here, it might be useful to show context if error occurred
          // this.state.activeRequestId = null;
          this.state.pollingAttempts = 0;
    }

    /**
     * Polls the backend service for the status of the active generation request.
     */
    async _pollGenerationStatus() {
         if (!this.state.activeRequestId) {
              this._stopPolling();
              return;
         }

         this.state.pollingAttempts++;
          console.debug("Polling status for request", this.state.activeRequestId, "Attempt", this.state.pollingAttempts);


         if (this.state.pollingAttempts > MAX_POLLING_ATTEMPTS) {
              this._handleGenerationError({ message: _t("Generation status check timed out.") });
              return;
         }

         try {
              const statusResult = await this.aiImageService.checkGenerationStatus(this.state.activeRequestId);

              if (statusResult && statusResult.status) {
                   if (statusResult.status === 'completed') {
                        this._handleGenerationResult(statusResult);
                   } else if (statusResult.status === 'failed') {
                        this._handleGenerationError(statusResult);
                   } else {
                        // Status is 'processing' or other interim state, continue polling
                         // Optional: Update UI with statusResult.progress if provided by backend
                         // this.state.progress = statusResult.progress;
                   }
              } else if (statusResult && statusResult.error) {
                  // If status result itself indicates an error
                  this._handleGenerationError(statusResult);
              } else {
                   // Unexpected response structure, treat as error? Or log and continue?
                   console.warn("Unexpected status response for request", this.state.activeRequestId, statusResult);
              }

         } catch (error) {
              // Handle polling error (e.g., network issues)
              console.error("Polling error for request", this.state.activeRequestId, error);
             this._handleGenerationError(error);
         }
    }


    /**
     * Handles a successful generation result.
     * @param {Object} result - The result object from the backend status check.
     */
    _handleGenerationResult(result) {
         console.info("AI Generation Completed:", result.request_id);
        this.state.generatedImages = result.images || []; // Expected: Array of { id, url, ... }
         // Update quota status if provided in the result
         if (result.quota_status) {
             Object.assign(this.state.quotaStatus, result.quota_status);
         }
         this.notification.add(_t("Image generation completed successfully!"), { type: 'success' });
        this._stopPolling(); // Stop polling on success
    }

    /**
     * Handles a generation error.
     * @param {Error|Object} error - The error object or status result with error details.
     */
    _handleGenerationError(error) {
         console.error("AI Generation Failed:", error);
        const errorMsg = error.error || error.error_message || error.message || _t("Image generation failed.");
        this.state.errorMessage = errorMsg;
        // this.state.generatedImages = []; // Keep previous images displayed if needed
        this.notification.add(errorMsg, { type: 'danger' });
        this._stopPolling(); // Stop polling on failure
    }

    /**
     * Triggers the download of a generated image.
     * @param {string} imageUrl
     * @param {string} imageName - Optional name for the downloaded file.
     */
    downloadImage(imageUrl, imageName = 'generated_image.png') {
        // Use the native browser download mechanism
        const link = document.createElement('a');
        link.href = imageUrl;
        link.download = imageName; // Suggest filename
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    /**
     * Handles the action to use an image in a campaign.
     * This might involve navigating or triggering an event.
     * @param {Object} image - The image object from generatedImages.
     */
    useImageInCampaign(image) {
        // This action depends on UI flow. Example: Redirect to a generic content submission page or a campaign-specific one
        // For now, emit an event or navigate to a placeholder.
        // If a specific campaign is active, use its ID.
        // Let's assume a generic message for now, specific routing is complex without more context.
        this.notification.add(_t("Using image in campaign... (Action to be defined)"), { type: 'info' });
        console.log("Use image in campaign clicked:", image);
        // This could trigger a custom event or use the router service.
        // Example: this.router.navigate(`/my/campaigns/submit?ai_image_id=${image.id}`);
        // Or if within a specific campaign context:
        // this.router.navigate(`/my/campaigns/submit/${this.state.generationParams.campaign_id}?ai_image_id=${image.id}`);
    }

     /**
      * Saves the current prompt for future use.
      */
     async savePrompt() {
          if (!this.state.prompt || this.state.prompt.trim() === "") {
              this.notification.add(_t("Cannot save an empty prompt."), { type: 'warning' });
              return;
          }
           // Prevent saving duplicate prompts (case-insensitive, trim)
          const normalizedPrompt = this.state.prompt.trim().toLowerCase();
          if (this.state.savedPrompts.some(p => p.trim().toLowerCase() === normalizedPrompt)) {
              this.notification.add(_t("This prompt is already saved."), { type: 'info' });
              return;
          }

         try {
             await this.aiImageService.saveUserPrompt(this.state.prompt);
             this.state.savedPrompts.push(this.state.prompt); // Add to local state
             this.notification.add(_t("Prompt saved successfully!"), { type: 'success' });
         } catch (error) {
              console.error("Error saving prompt:", error);
             this.notification.add(error.error || _t("Failed to save prompt."), { type: 'danger' });
         }
     }

     /**
      * Loads a saved or template prompt into the prompt input.
      * @param {string} promptText
      */
     reusePrompt(promptText) {
         this.state.prompt = promptText;
     }

     /**
      * Updates a generation parameter in the state.
      * @param {string} paramName
      * @param {*} value
      */
     _updateParam(paramName, value) {
         // Basic type conversion if necessary (e.g., string input to number)
         if (['seed', 'inference_steps'].includes(paramName)) {
             value = parseInt(value, 10);
             if (isNaN(value)) {
                // Try to get default from props, otherwise keep current or set to a sensible default
                value = this.props.defaultParams?.[paramName] ?? (paramName === 'seed' ? -1 : 30);
             }
         } else if (['cfg_scale'].includes(paramName)) {
             value = parseFloat(value);
              if (isNaN(value)) {
                value = this.props.defaultParams?.[paramName] ?? 7.0;
              }
         }

         // Optional: Add validation against props.paramRanges here
         if (this.props.paramRanges && this.props.paramRanges[paramName]) {
             const range = this.props.paramRanges[paramName];
             if (range.min !== undefined && value < range.min) value = range.min;
             if (range.max !== undefined && value > range.max) value = range.max;
         }

         this.state.generationParams[paramName] = value;
     }
}

AIImageGeneratorComponent.template = "influence_gen_portal.AIImageGeneratorComponentTemplate";
AIImageGeneratorComponent.props = {
    initialQuota: { type: Object, shape: { used: Number, total: Number, remaining: Number }, optional: true, default: () => ({used:0, total:0, remaining:0}) },
    defaultParams: {
         type: Object,
         optional: true,
         default: () => ({
             model_id: null,
             resolution: "512x512",
             aspect_ratio: "1:1",
             seed: -1,
             inference_steps: 30,
             cfg_scale: 7.0,
             intended_use: 'general',
             campaign_id: null,
         }),
         shape: {
             model_id: [Number, String, { value: null }],
             resolution: String,
             aspect_ratio: String,
             seed: Number,
             inference_steps: Number,
             cfg_scale: Number,
             intended_use: String,
             campaign_id: [Number, { value: null }], // Can be null if not linked
         }
    },
    paramRanges: { type: Object, optional: true, default: () => ({}) }, // e.g., { inference_steps: { min: 10, max: 100, step: 1 }, ... }
};

// Define dependencies on other services
AIImageGeneratorComponent.services = ["influence_gen_portal.services.aiImage", "notification", "rpc", "router"];

// Register as an Odoo JS module if needed outside of OWL app context
// odoo.define('influence_gen_portal.AIImageGeneratorComponent', function (require) {
//     'use strict';
//     return AIImageGeneratorComponent;
// });