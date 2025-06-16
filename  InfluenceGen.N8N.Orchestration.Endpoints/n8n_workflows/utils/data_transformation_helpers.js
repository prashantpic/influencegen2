/**
 * @namespace InfluenceGen.N8N.Utils.Transformation
 * Provides JavaScript helper functions for common data transformations between Odoo, N8N, and external AI services.
 */
const InfluenceGenN8NUtilsTransformation = {
  /**
   * Prepares the request payload for a standardized AI service adapter sub-workflow.
   * @param {object} odooPayload - The payload received from Odoo.
   *   Expected fields: prompt, negative_prompt, resolution, aspect_ratio, seed,
   *   inference_steps, cfg_scale, model_preference, correlation_id.
   * @param {object} aiServiceConfig - Configuration specific to the target AI service adapter.
   *   May contain model mapping keys or default parameters.
   * @returns {object} - The request payload formatted for the AI service adapter.
   */
  prepareAIServiceRequest: function(odooPayload, aiServiceConfig) {
    const standardizedRequest = {
      prompt: odooPayload.prompt,
      negative_prompt: odooPayload.negative_prompt || null, // Ensure null if not provided
      model_identifier: odooPayload.model_preference, // Default mapping, can be refined by aiServiceConfig
      resolution: odooPayload.resolution,
      aspect_ratio: odooPayload.aspect_ratio,
      seed: odooPayload.seed !== undefined ? Number(odooPayload.seed) : null,
      inference_steps: odooPayload.inference_steps !== undefined ? Number(odooPayload.inference_steps) : null,
      cfg_scale: odooPayload.cfg_scale !== undefined ? Number(odooPayload.cfg_scale) : null,
      correlationId: odooPayload.correlation_id || odooPayload.correlationId, // Handle both _id and Id
      // Add any other parameters that are considered standard for adapters
    };

    // Apply specific transformations or defaults based on aiServiceConfig
    if (aiServiceConfig) {
      if (aiServiceConfig.modelMapping && odooPayload.model_preference) {
        standardizedRequest.model_identifier = aiServiceConfig.modelMapping[odooPayload.model_preference] || odooPayload.model_preference;
      }
      // Example: if aiServiceConfig has default steps and odooPayload doesn't provide it
      if (aiServiceConfig.default_inference_steps && standardizedRequest.inference_steps === null) {
        standardizedRequest.inference_steps = aiServiceConfig.default_inference_steps;
      }
      // Add other config-driven transformations here
    }
    
    // Ensure numeric fields are numbers or null
    const numericFields = ['seed', 'inference_steps', 'cfg_scale'];
    numericFields.forEach(field => {
        if (standardizedRequest[field] !== null && isNaN(Number(standardizedRequest[field]))) {
            // Handle invalid non-numeric values for numeric fields if necessary, or let them be null
            console.warn(`prepareAIServiceRequest: Non-numeric value for ${field} - ${standardizedRequest[field]}. Setting to null.`);
            standardizedRequest[field] = null;
        } else if (standardizedRequest[field] !== null) {
             standardizedRequest[field] = Number(standardizedRequest[field]);
        }
    });


    return standardizedRequest;
  },

  /**
   * Formats the payload for the Odoo callback API.
   * @param {object} aiServiceResponse - The standardized response from the AI service adapter sub-workflow.
   *   Success: { status: "success", imageUrl, imageData, contentType, metadata }
   *   Error: { status: "error", errorCode, errorMessage }
   * @param {object} originalRequest - The initial Odoo request payload (to retrieve correlationId and other context).
   *   Expected to have `correlationId` (or `correlation_id` to be safe).
   * @param {boolean} isSuccess - Flag indicating if the AI generation was successful.
   * @returns {object} - The payload formatted for the Odoo callback API.
   */
  formatOdooCallbackPayload: function(aiServiceResponse, originalRequest, isSuccess) {
    const callbackPayload = {
      correlationId: originalRequest.correlationId || originalRequest.correlation_id, // Prefer correlationId if normalized
      status: isSuccess ? "success" : "error",
    };

    if (isSuccess) {
      callbackPayload.imageUrl = aiServiceResponse.imageUrl || null;
      callbackPayload.imageData = aiServiceResponse.imageData || null; // Base64 encoded image
      callbackPayload.contentType = aiServiceResponse.contentType || (aiServiceResponse.imageData ? 'image/png_base64' : (aiServiceResponse.imageUrl ? 'image/url_reference' : null) ); // Default based on what's available
      callbackPayload.metadata = aiServiceResponse.metadata || {};
    } else {
      callbackPayload.errorCode = aiServiceResponse.errorCode || "UNKNOWN_AI_SERVICE_ERROR";
      callbackPayload.errorMessage = aiServiceResponse.errorMessage || "An unspecified error occurred with the AI service.";
      if (aiServiceResponse.details) { // Include more details if adapter provided them
        callbackPayload.errorDetails = aiServiceResponse.details;
      }
    }

    return callbackPayload;
  },

  /**
   * Extracts image details from a standardized AI service adapter response.
   * @param {object} aiServiceAdapterResponse - The standardized response from the AI service adapter.
   *   Expected structure: { status: "success", imageUrl?: "...", imageData?: "...", contentType?: "...", metadata?: {...} }
   *                        or { status: "error", ... }
   * @returns {object|null} - An object containing extracted image details
   *   (e.g., { imageUrl, imageData, contentType, metadata }) or null if not successful or details are missing.
   */
  extractImageDetails: function(aiServiceAdapterResponse) {
    if (aiServiceAdapterResponse && aiServiceAdapterResponse.status === "success") {
      const details = {
        imageUrl: aiServiceAdapterResponse.imageUrl || null,
        imageData: aiServiceAdapterResponse.imageData || null,
        contentType: aiServiceAdapterResponse.contentType || null,
        metadata: aiServiceAdapterResponse.metadata || {},
      };
      // If neither imageUrl nor imageData is present, it's not a successful image response
      if (!details.imageUrl && !details.imageData) {
        return null; // Or return an object indicating missing image data
      }
      return details;
    }
    return null; // Indicates failure or no image details to extract
  }
};

// For direct use in N8N Function nodes:
// const transform = InfluenceGenN8NUtilsTransformation;
// transform.prepareAIServiceRequest(...);
// Or if embedding:
// const prepareAIServiceRequest = function(...) { ... };
// const formatOdooCallbackPayload = function(...) { ... };
// const extractImageDetails = function(...) { ... };