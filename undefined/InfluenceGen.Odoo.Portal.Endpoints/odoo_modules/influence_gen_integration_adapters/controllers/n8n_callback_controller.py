import logging
import json

from odoo import http
from odoo.http import request, Response

from ..dtos.n8n_dtos import N8nAiGenerationResultDto, GeneratedImageDataDto # Ensure DTOs are correctly imported

_logger = logging.getLogger(__name__)

class N8NCallbackController(http.Controller):
    """
    Handles incoming HTTP POST callbacks from N8N, primarily for AI image generation results.
    """

    @http.route('/influence_gen/n8n/ai_callback', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def handle_ai_image_result(self, **kwargs):
        """
        Handles the AI image generation result callback from N8N.

        Args:
            **kwargs: The JSON payload automatically parsed by Odoo from the request body.

        Returns:
            werkzeug.wrappers.Response: A JSON response indicating success or failure.
                                        Odoo's jsonrpc handling will typically manage the
                                        response structure for 200 OK. For explicit error
                                        responses, werkzeug.Response is constructed.
        """
        _logger.info("Received N8N AI image result callback. Payload: %s", kwargs)

        # 1. Authentication
        try:
            # Assuming 'influence_gen.api.auth' is a model/service registered in the environment
            # and 'verify_n8n_request' is a method on it.
            if not request.env['influence_gen.api.auth'].verify_n8n_request(request):
                _logger.warning("N8N callback authentication failed for request: %s", request.httprequest.headers.get('X-N8N-Signature'))
                error_body = json.dumps({"error": "Authentication failed", "message": "Invalid or missing authentication token."})
                return Response(error_body, status=401, mimetype='application/json')
        except Exception as e:
            _logger.error("Error during N8N callback authentication: %s", e, exc_info=True)
            error_body = json.dumps({"error": "Authentication error", "message": "An error occurred during authentication."})
            return Response(error_body, status=500, mimetype='application/json')

        # 2. Payload Parsing & Validation
        try:
            # Reconstruct GeneratedImageDataDto if present
            if 'images' in kwargs and kwargs['images']:
                images_data = []
                for img_data in kwargs['images']:
                    images_data.append(GeneratedImageDataDto(**img_data))
                kwargs['images'] = images_data
            
            # The `kwargs` is already the parsed JSON payload because of `type='json'`
            # Instantiate DTO for validation (dataclasses handle basic type checks)
            ai_result_dto = N8nAiGenerationResultDto(**kwargs)

            # Additional structural validation if needed (e.g., specific fields)
            if not all([ai_result_dto.request_id, ai_result_dto.status]):
                 _logger.warning("N8N callback payload validation failed: Missing required fields (request_id, status). Payload: %s", kwargs)
                 error_body = json.dumps({"error": "Validation error", "message": "Missing required fields in payload (request_id, status)."})
                 return Response(error_body, status=400, mimetype='application/json')

        except (TypeError, ValueError) as e:
            _logger.warning("N8N callback payload parsing/validation failed: %s. Payload: %s", e, kwargs, exc_info=True)
            error_body = json.dumps({"error": "Validation error", "message": f"Invalid payload structure or types: {str(e)}"})
            return Response(error_body, status=400, mimetype='application/json')
        except Exception as e: # Catch any other DTO instantiation errors
            _logger.error("Unexpected error during N8N DTO instantiation: %s. Payload: %s", e, kwargs, exc_info=True)
            error_body = json.dumps({"error": "DTO Instantiation Error", "message": "Could not process the provided data."})
            return Response(error_body, status=400, mimetype='application/json')

        _logger.info("N8N callback payload successfully parsed and validated for request_id: %s", ai_result_dto.request_id)

        # 3. Data Dispatching
        try:
            # Assuming 'influence_gen.ai.image.service' is a business service model
            # registered in the Odoo environment.
            ai_image_service = request.env['influence_gen.ai.image.service']
            
            # Call the business service method to process the result
            # This method in the business service should handle its own errors and logic
            ai_image_service.process_n8n_ai_result(ai_result_dto)

            _logger.info("Successfully dispatched N8N AI result for request_id: %s to business service.", ai_result_dto.request_id)
            # Odoo's json type route implicitly returns 200 OK with the dict as JSON
            return {"status": "success", "message": "Callback processed successfully."}

        except Exception as e:
            # This catches exceptions from the business service call
            _logger.error("Error dispatching N8N AI result (request_id: %s) to business service: %s",
                          ai_result_dto.request_id, e, exc_info=True)
            error_body = json.dumps({
                "error": "Processing error",
                "message": "An error occurred while processing the AI generation result."
            })
            return Response(error_body, status=500, mimetype='application/json')