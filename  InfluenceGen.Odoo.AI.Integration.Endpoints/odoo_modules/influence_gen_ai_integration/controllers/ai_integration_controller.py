import json
import logging
import werkzeug

from odoo import http
from odoo.http import request
from ..utils import security_utils # Corrected import based on AI instruction structure

_logger = logging.getLogger(__name__)

class AIIntegrationController(http.Controller):
    """
    Handles inbound N8N callback for AI image generation results.
    """

    @http.route('/influence_gen/ai/callback/image_result', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_n8n_image_result_callback(self, **kwargs):
        """
        Handles the callback from N8N with AI image generation results.

        The N8N payload is expected to be a JSON object with:
        - ai_generation_request_id: str (ID of the Odoo AIImageGenerationRequest record)
        - security_token: str (A shared secret for authenticating the callback)
        - result_payload: dict (Contains the actual status and data/error_data from N8N)
            - status: 'success' or 'failure'
            - data: dict (if success, contains image_url, metadata, etc.)
            - error_data: dict (if failure, contains error message and details)

        Returns:
            werkzeug.wrappers.Response: JSON response indicating success or failure of processing.
        """
        _logger.info("Received N8N callback for AI image result.")

        # In type='json' routes, Odoo parses the JSON body into request.jsonrequest
        # kwargs will be empty unless data is sent as form-data, which is not the case here.
        payload = request.jsonrequest

        if not payload:
            _logger.warning("N8N callback received an empty payload.")
            return werkzeug.wrappers.Response(
                json.dumps({'status': 'error', 'message': 'Empty payload received.'}),
                status=400, mimetype='application/json'
            )

        received_token = payload.get('security_token')

        if not security_utils.validate_n8n_callback_token(request.env, received_token):
            _logger.warning("N8N callback: Authentication failed. Invalid or missing token.")
            return werkzeug.wrappers.Response(
                json.dumps({'status': 'error', 'message': 'Authentication failed'}),
                status=401, mimetype='application/json'
            )

        _logger.info("N8N callback: Token validated successfully.")

        try:
            ai_generation_request_id = payload.get('ai_generation_request_id')
            n8n_result_payload = payload.get('result_payload')

            if not ai_generation_request_id or not n8n_result_payload:
                _logger.error(
                    "Missing 'ai_generation_request_id' or 'result_payload' in N8N callback. Payload: %s",
                    payload
                )
                # Odoo's default JSON response will be HTTP 200 with this body
                return {'status': 'error', 'message': 'Missing required fields in callback payload'}

            _logger.info(
                "Processing N8N callback for request ID: %s",
                ai_generation_request_id
            )

            # Use sudo() as the controller is public and the service needs permissions
            # to interact with Odoo models.
            request.env['influence_gen.ai_result_service'].sudo().process_n8n_callback(
                ai_generation_request_id,
                n8n_result_payload
            )

            _logger.info(
                "Successfully processed N8N callback for request ID: %s",
                ai_generation_request_id
            )
            return {'status': 'success'}

        except Exception as e:
            _logger.exception(
                "Error processing N8N callback for request ID '%s': %s",
                payload.get('ai_generation_request_id', 'UNKNOWN'), e
            )
            # Odoo's default JSON response will be HTTP 200 with this body
            return {'status': 'error', 'message': 'Internal server error while processing callback.'}