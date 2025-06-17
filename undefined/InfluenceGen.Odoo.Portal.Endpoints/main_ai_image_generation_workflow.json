```json
{
  "name": "InfluenceGen AI Image Generation Orchestrator",
  "nodes": [
    {
      "parameters": {},
      "id": "b9e07569-c92c-4a37-8eba-8e4a9e5bd9c1",
      "name": "Start",
      "type": "n8n-nodes-base.start",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    {
      "parameters": {
        "path": "/webhook/influencegen/ai-image-generate",
        "method": "POST",
        "authentication": "basicAuth",
        "responseMode": "onReceived",
        "options": {}
      },
      "id": "e6f4a8e0-1c7b-4d9f-8a3e-7b1f2c0d9e8f",
      "name": "receiveOdooRequest",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        450,
        300
      ],
      "credentials": {
        "httpBasicAuth": {
          "id": "PLACEHOLDER_WEBHOOK_CREDENTIAL_ID",
          "name": "Odoo Webhook Auth"
        }
      }
    },
    {
      "parameters": {
        "functionCode": "/* Assuming odoo_payload_handler, custom_logger, error_processor objects/functions are available */ \n\nconst odooRequest = items[0].json;\n\ntry {\n  logEvent('INFO', 'Received Odoo Webhook', { requestId: odooRequest.request_id, triggerNode: 'receiveOdooRequest', payloadSummary: { promptLength: odooRequest.prompt ? odooRequest.prompt.length : 0, serviceType: odooRequest.ai_service_type } });\n\n  const parsedRequest = odoo_payload_handler.parseAndValidateOdooWebhook(odooRequest);\n\n  if (parsedRequest.error) {\n    logEvent('ERROR', 'Invalid Odoo Request', { error: parsedRequest.error, requestId: odooRequest.request_id });\n    const validationError = error_processor.createWorkflowErrorObject(parsedRequest.error.message, 'parseAndValidateRequest', parsedRequest.error.code);\n    // Add requestId to the error object itself for easier retrieval in error workflow\n    validationError.requestId = odooRequest.request_id;\n    throw new Error(JSON.stringify(validationError)); \n  }\n  \n  // Set $vars.initialOdooRequestId for potential use in general error handler, though specific errors should carry their own requestId.\n  // $vars.initialOdooRequestId = parsedRequest.requestId; \n  // Decided against $vars, error objects will carry requestId or formatWorkflowErrorForOdoo will try to find it.\n\n  logEvent('INFO', 'Parsed and Validated Odoo Request', { requestId: parsedRequest.requestId, paramsSummary: { promptLength: parsedRequest.params.prompt ? parsedRequest.params.prompt.length : 0, modelName: parsedRequest.modelName } });\n  return [{ json: parsedRequest }];\n\n} catch (error) {\n  const errMessage = error.message || 'Unknown error during parseAndValidateRequest';\n  // Check if error is already our structured error string\n  if (errMessage.startsWith('{') && errMessage.endsWith('}')) {\n      throw error; // Re-throw if already a stringified JSON error object\n  }\n  logEvent('ERROR', 'Error in parseAndValidateRequest', { error: errMessage, stack: error.stack, input: odooRequest, requestId: odooRequest.request_id });\n  const workflowError = error_processor.createWorkflowErrorObject(errMessage, 'parseAndValidateRequest', 'INTERNAL_PARSING_ERROR');\n  workflowError.requestId = odooRequest.request_id; // Ensure requestId is part of the error\n  throw new Error(JSON.stringify(workflowError));\n}\n"
      },
      "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "name": "parseAndValidateRequest",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        650,
        300
      ]
    },
    {
      "parameters": {
        "functionCode": "/* Assuming ai_service_adapter, custom_logger, error_processor objects/functions are available */\n\nconst { requestId, params, aiServiceType, modelName } = items[0].json;\n\ntry {\n  const aiServiceApiPayload = ai_service_adapter.adaptToAIService(params, aiServiceType, modelName);\n  const endpoint = ai_service_adapter.getAIServiceEndpoint(aiServiceType, modelName);\n\n  logEvent('INFO', 'Request Adapted for AI Service', { requestId, aiServiceType, endpoint, payloadKeys: Object.keys(aiServiceApiPayload) });\n  return [{ json: { requestId, endpoint, aiServiceApiPayload, aiServiceType, modelName } }];\n\n} catch (error) {\n  logEvent('ERROR', 'Error in adaptToAIService', { error: error.message, stack: error.stack, input: items[0].json, requestId });\n  const workflowError = error_processor.createWorkflowErrorObject(error.message, 'adaptToAIService', 'ADAPTATION_ERROR');\n  workflowError.requestId = requestId;\n  throw new Error(JSON.stringify(workflowError));\n}\n"
      },
      "id": "b2c3d4e5-f6a7-8901-2345-678901abcdef",
      "name": "adaptToAIService",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        850,
        300
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "={{ $json.endpoint }}",
        "sendBody": true,
        "bodyContentType": "json",
        "jsonBody": "={{ $json.aiServiceApiPayload }}",
        "authentication": "genericCredentialType",
        "genericCredentialType": {
          "genericAuthType": " διαφοAI Service API Key"
        },
        "options": {
          "retryOnFail": true,
          "retryCount": 3,
          "retryInterval": 5000
        }
      },
      "id": "c3d4e5f6-a7b8-9012-3456-789012abcdef",
      "name": "callAIService",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [
        1050,
        300
      ],
      "credentials": {
        "genericCredentialType": {
          "id": "AI_SERVICE_CREDENTIAL_ID_PLACEHOLDER",
          "name": "AI Service API Key"
        }
      }
    },
    {
      "parameters": {
        "functionCode": "/* Assuming error_processor, custom_logger objects/functions are available */\n\nconst aiResponse = items[0].json;\nconst httpNodeInfo = $items(\"callAIService\")[0]; // N8N new way to get http response details\nconst { requestId, aiServiceType } = $('adaptToAIService').item.json;\n\ntry {\n  logEvent('INFO', 'Received AI Service Response', { requestId, statusCode: httpNodeInfo.statusCode, serviceType: aiServiceType });\n\n  if (httpNodeInfo.statusCode >= 200 && httpNodeInfo.statusCode < 300) {\n    let imageUrl = null;\n    let generationMetadata = {};\n    // Simplified extraction logic, actual logic depends on AI service response\n    if (aiServiceType.toUpperCase() === 'STABILITY_AI') {\n        if (aiResponse.artifacts && aiResponse.artifacts.length > 0 && aiResponse.artifacts[0].base64) {\n            imageUrl = `data:image/png;base64,${aiResponse.artifacts[0].base64}`;\n            generationMetadata.seed = aiResponse.artifacts[0].seed;\n            generationMetadata.finishReason = aiResponse.artifacts[0].finishReason;\n        }\n    } else if (aiServiceType.toUpperCase() === 'COMFY_UI') {\n        // Example: ComfyUI might return image paths or direct data in 'outputs'\n        if (aiResponse.outputs && Object.keys(aiResponse.outputs).length > 0) {\n            const outputNode = aiResponse.outputs[Object.keys(aiResponse.outputs)[0]];\n            if (outputNode.images && outputNode.images.length > 0) {\n                const imageInfo = outputNode.images[0];\n                // Construct URL if ComfyUI is set up to serve images, or expect base64\n                imageUrl = `http://example.com/comfyui_images/${imageInfo.filename}`; // Placeholder\n                generationMetadata.filename = imageInfo.filename;\n            }\n        }\n    } else {\n        // Generic attempt\n        if (aiResponse.image_url) imageUrl = aiResponse.image_url;\n        else if (aiResponse.images && aiResponse.images.length > 0) imageUrl = aiResponse.images[0];\n        else if (aiResponse.data && aiResponse.data.url) imageUrl = aiResponse.data.url;\n    }\n\n    if (!imageUrl) {\n      logEvent('ERROR', 'Image URL/data not found in AI service success response', { requestId, response: aiResponse });\n      const extractionError = error_processor.createWorkflowErrorObject('Image URL or data not found in AI service response', 'processAIServiceResponse', 'IMAGE_EXTRACTION_FAILURE');\n      extractionError.requestId = requestId;\n      return [{ json: { status: 'error', error: extractionError, requestId } }];\n    }\n\n    logEvent('INFO', 'AI Image Generation Successful', { requestId, imageUrlPresent: !!imageUrl, metadata: generationMetadata });\n    return [{ json: { status: 'success', result: { imageUrl, generationMetadata }, requestId } }];\n  } else {\n    const normalizedError = error_processor.normalizeAIServiceError(aiResponse, aiServiceType);\n    normalizedError.requestId = requestId; // Ensure requestId is part of the error\n    logEvent('ERROR', 'AI Service Returned Error', { requestId, error: normalizedError, statusCode: httpNodeInfo.statusCode });\n    return [{ json: { status: 'error', error: normalizedError, requestId } }];\n  }\n} catch (error) {\n  logEvent('ERROR', 'Error processing AI Service Response', { requestId, error: error.message, stack: error.stack, input: items[0].json });\n  const workflowError = error_processor.createWorkflowErrorObject(error.message, 'processAIServiceResponse', 'INTERNAL_PROCESSING_ERROR');\n  workflowError.requestId = requestId;\n  // Do not throw here, let formatOdooCallback handle this error structure.\n  return [{ json: { status: 'error', error: workflowError, requestId } }]; \n}\n"
      },
      "id": "d4e5f6a7-b8c9-0123-4567-890123abcdef",
      "name": "processAIServiceResponse",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        1250,
        300
      ]
    },
    {
      "parameters": {
        "functionCode": "/* Assuming odoo_payload_handler, custom_logger, error_processor objects/functions are available */\n\nconst { status, result, error, requestId } = items[0].json;\nlet callbackPayload;\n\ntry {\n  if (status === 'success') {\n    const generationMetadata = result.generationMetadata || {};\n    callbackPayload = odoo_payload_handler.formatSuccessCallback(result.imageUrl, requestId, generationMetadata);\n    logEvent('INFO', 'Formatted Success Callback for Odoo', { requestId });\n  } else {\n    // Ensure error object exists and has a message\n    const errorMessage = error && error.message ? error.message : 'Unknown error occurred';\n    const errorCode = error && error.code ? error.code : 'UNKNOWN_ERROR';\n    callbackPayload = odoo_payload_handler.formatErrorCallback(errorMessage, errorCode, requestId);\n    logEvent('ERROR', 'Formatted Error Callback for Odoo', { requestId, error: errorMessage, errorCode });\n  }\n  return [{ json: callbackPayload }];\n} catch (formatError) {\n    logEvent('CRITICAL', 'Failed to format Odoo callback payload', { requestId, initialStatus: status, error: formatError.message, stack: formatError.stack });\n    // Create a fallback error payload if formatting itself fails\n    const fallbackError = error_processor.createWorkflowErrorObject('Critical: Failed to format Odoo callback: ' + formatError.message, 'formatOdooCallback', 'CALLBACK_FORMAT_FAILURE');\n    fallbackError.requestId = requestId || 'UNKNOWN_REQUEST_ID_IN_FORMAT_CATCH';\n    callbackPayload = odoo_payload_handler.formatErrorCallback(fallbackError.message, fallbackError.code, fallbackError.requestId);\n    return [{ json: callbackPayload }];\n}\n"
      },
      "id": "e5f6a7b8-c9d0-1234-5678-901234abcdef",
      "name": "formatOdooCallback",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        1450,
        300
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "={{ $env.ODOO_CALLBACK_URL }}",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            },
            {
              "name": "X-Api-Key",
              "value": "={{ $env.ODOO_CALLBACK_API_KEY }}"
            }
          ]
        },
        "sendBody": true,
        "bodyContentType": "json",
        "jsonBody": "={{ $json }}",
        "options": {
          "retryOnFail": true,
          "retryCount": 3,
          "retryInterval": 5000
        }
      },
      "id": "f6a7b8c9-d0e1-2345-6789-012345abcdef",
      "name": "sendToOdooCallback",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [
        1650,
        300
      ]
    },
    {
      "parameters": {
        "functionCode": "/* Assuming custom_logger functions are available */\n\nconst odooResponseData = items[0].json;\nconst httpNodeInfo = $items(\"sendToOdooCallback\")[0];\n// The request_id was part of the payload sent to Odoo, which is the input to this node's previous node.\nconst originalPayloadToOdoo = $('formatOdooCallback').item.json;\nconst requestId = originalPayloadToOdoo.request_id;\n\ntry {\n  logEvent('INFO', 'Odoo Callback Completed', { \n    requestId: requestId, \n    odooResponseStatus: httpNodeInfo.statusCode, \n    odooResponseBodySummary: JSON.stringify(odooResponseData).substring(0, 200) \n  });\n  return items;\n} catch (error) {\n  // Log errors occurring within the final logging step itself\n  console.error(`[CRITICAL] Error in logFinalStatus for requestId ${requestId}: ${error.message}`, error.stack);\n  // Attempt to use custom logger as a fallback\n  try {\n    logEvent('CRITICAL', 'Error in logFinalStatus', { requestId: requestId, error: error.message, stack: error.stack });\n  } catch (e) { /* ignore secondary logging failure */ }\n  return items; // Don't stop workflow on logging error\n}\n"
      },
      "id": "a7b8c9d0-e1f2-3456-7890-123456abcdef",
      "name": "logFinalStatus",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        1850,
        300
      ]
    },
    {
      "parameters": {
        "id": "workflowErrorTrigger"
      },
      "id": "b8c9d0e1-f2a3-4567-8901-234567abcdef",
      "name": "workflowErrorTrigger",
      "type": "n8n-nodes-base.errorTrigger",
      "typeVersion": 1,
      "position": [
        650,
        500
      ]
    },
    {
      "parameters": {
        "functionCode": "/* Assuming odoo_payload_handler, custom_logger objects/functions are available */\n\nconst errorData = items[0].json; // This is the error object from the Error Trigger node.\nlet requestId = 'UNKNOWN_REQUEST_ID';\nlet errorMessage = 'An unexpected workflow error occurred.';\nlet errorCode = 'N8N_WORKFLOW_FAILURE';\nlet errorSourceStep = errorData.node?.name || 'Unknown Step';\n\n// Try to extract original requestId and structured error details\ntry {\n  if (errorData.error?.message) {\n    // Check if the error message is a stringified JSON from our CreateWorkflowErrorObject\n    try {\n      const parsedErrorMessage = JSON.parse(errorData.error.message);\n      if (parsedErrorMessage.code) {\n        errorMessage = parsedErrorMessage.message;\n        errorCode = parsedErrorMessage.code;\n        if(parsedErrorMessage.step) errorSourceStep = parsedErrorMessage.step;\n        if(parsedErrorMessage.requestId) requestId = parsedErrorMessage.requestId;\n      }\ else {\n        errorMessage = errorData.error.message;\n      }\n    } catch (e) {\n      // Not a JSON string, use as is\n      errorMessage = errorData.error.message;\n    }\n  } else if (errorData.message) {\n    errorMessage = errorData.message;\n  }\n\n  // Fallback for requestId if not in parsed error\n  if (requestId === 'UNKNOWN_REQUEST_ID') {\n    // Attempt to get from the initial webhook data if error occurred after it\n    // This might not always be available or reliable depending on when the error happened.\n    try {\n      requestId = $('receiveOdooRequest').item.json.request_id || requestId;\n    } catch (e) { /* ignore if not found */ }\n    // As a last resort, use execution ID if no request_id can be found.\n    if (requestId === 'UNKNOWN_REQUEST_ID' && typeof $execution !== 'undefined') {\n        requestId = `EXECUTION_ID_${$execution.id}`;\n    }\n  }\n\n} catch (e) {\n  logEvent('CRITICAL', 'Error while parsing error data in formatWorkflowErrorForOdoo', { initialError: errorData, parsingError: e.message });\n  // Use default error message if parsing fails\n}\n\nlogEvent('CRITICAL', 'N8N Workflow Failed, Notifying Odoo', { requestId, error: errorMessage, errorCode, errorSourceStep, originalError: errorData });\nconst callbackPayload = odoo_payload_handler.formatErrorCallback(errorMessage, errorCode, requestId);\n\nreturn [{ json: callbackPayload }];\n"
      },
      "id": "c9d0e1f2-a3b4-5678-9012-345678abcdef",
      "name": "formatWorkflowErrorForOdoo",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        850,
        500
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "={{ $env.ODOO_CALLBACK_URL }}",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            },
            {
              "name": "X-Api-Key",
              "value": "={{ $env.ODOO_CALLBACK_API_KEY }}"
            }
          ]
        },
        "sendBody": true,
        "bodyContentType": "json",
        "jsonBody": "={{ $json }}",
        "options": {
          "retryOnFail": true,
          "retryCount": 3,
          "retryInterval": 5000
        }
      },
      "id": "d0e1f2a3-b4c5-6789-0123-456789abcdef",
      "name": "sendWorkflowErrorToOdoo",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [
        1050,
        500
      ]
    },
    {
      "parameters": {
        "functionCode": "/* Assuming custom_logger functions are available */\n\nconst odooResponseData = items[0].json;\nconst httpNodeInfo = $items(\"sendWorkflowErrorToOdoo\")[0];\nconst originalErrorPayloadToOdoo = $('formatWorkflowErrorForOdoo').item.json;\nconst requestId = originalErrorPayloadToOdoo.request_id;\n\ntry {\n  logEvent('CRITICAL', 'Workflow Error Callback Sent to Odoo', { \n    requestId: requestId, \n    odooResponseStatus: httpNodeInfo.statusCode, \n    odooResponseBodySummary: JSON.stringify(odooResponseData).substring(0, 200) \n  });\n  return items;\n} catch (error) {\n  console.error(`[CRITICAL] Error in logWorkflowErrorSent for requestId ${requestId}: ${error.message}`, error.stack);\n  try {\n    logEvent('CRITICAL', 'Error in logWorkflowErrorSent', { requestId: requestId, error: error.message, stack: error.stack });\n  } catch (e) { /* ignore secondary logging failure */ }\n  return items;\n}\n"
      },
      "id": "e1f2a3b4-c5d6-7890-1234-567890abcdef",
      "name": "logWorkflowErrorSent",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        1250,
        500
      ]
    }
  ],
  "connections": {
    "Start": {
      "main": [
        [
          {
            "node": "receiveOdooRequest",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "receiveOdooRequest": {
      "main": [
        [
          {
            "node": "parseAndValidateRequest",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "parseAndValidateRequest": {
      "main": [
        [
          {
            "node": "adaptToAIService",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "adaptToAIService": {
      "main": [
        [
          {
            "node": "callAIService",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "callAIService": {
      "main": [
        [
          {
            "node": "processAIServiceResponse",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "processAIServiceResponse": {
      "main": [
        [
          {
            "node": "formatOdooCallback",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "formatOdooCallback": {
      "main": [
        [
          {
            "node": "sendToOdooCallback",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "sendToOdooCallback": {
      "main": [
        [
          {
            "node": "logFinalStatus",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "workflowErrorTrigger": {
      "main": [
        [
          {
            "node": "formatWorkflowErrorForOdoo",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "formatWorkflowErrorForOdoo": {
      "main": [
        [
          {
            "node": "sendWorkflowErrorToOdoo",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "sendWorkflowErrorToOdoo": {
      "main": [
        [
          {
            "node": "logWorkflowErrorSent",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {
    "errorWorkflow": "workflowErrorTrigger",
    "executionOrder": "v1"
  },
  "versionId": "f9b8c0a1-7d6e-4f5a-8c3b-2a1d0e9f8c7b",
  "meta": {
    "templateCredsSetupCompleted": true
  }
}
```