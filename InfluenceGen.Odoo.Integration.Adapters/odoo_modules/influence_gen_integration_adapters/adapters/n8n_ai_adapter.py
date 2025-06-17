```python
import logging
import dataclasses
import requests
import time # For basic retry if tenacity is not used, but tenacity is preferred
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from odoo import models, api
from odoo.exceptions import UserError

from ..dtos.n8n_dtos import N8nAiGenerationRequestDto
from ..utils.integration_error_handler import (
    handle_external_api_error,
    IntegrationServiceError,
    TransientIntegrationError,
    PermanentIntegrationError,
    AuthenticationError,
    RateLimitError,
)

_logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_RETRY_ATTEMPTS = 3
RETRY_WAIT_MULTIPLIER = 1
RETRY_WAIT_MIN_SECONDS = 2
RETRY_WAIT_MAX_SECONDS = 10

class N8nAiAdapter(models.AbstractModel):
    _name = 'influence_gen.n8n.ai.adapter'
    _description = 'N8N AI Service Adapter'

    def _get_config_params(self):
        """Fetches N8N configuration parameters."""
        IrConfigParameter = self.env['ir.config_parameter'].sudo()
        n8n_webhook_url = IrConfigParameter.get_param('influence_gen.n8n_ai_webhook_url')
        n8n_auth_token = IrConfigParameter.get_param('influence_gen.n8n_ai_auth_token')
        return n8n_webhook_url, n8n_auth_token

    def initiate_ai_image_generation(self, generation_request_dto: N8nAiGenerationRequestDto) -> dict:
        """
        Initiates AI image generation by calling the N8N webhook.

        Args:
            generation_request_dto: DTO containing the request parameters.

        Returns:
            A dictionary indicating success or failure and relevant details.
            e.g., {"success": True/False, "message": "...", "n8n_response_status": 200/None, "data": ...}
        """
        n8n_webhook_url, n8n_auth_token = self._get_config_params()

        if not n8n_webhook_url:
            _logger.error("N8N AI Webhook URL ('influence_gen.n8n_ai_webhook_url') is not configured.")
            return {"success": False, "message": "N8N webhook URL not configured.", "n8n_response_status": None}
        if not n8n_auth_token:
            _logger.error("N8N AI Auth Token ('influence_gen.n8n_ai_auth_token') is not configured.")
            return {"success": False, "message": "N8N auth token not configured.", "n8n_response_status": None}

        payload = dataclasses.asdict(generation_request_dto)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {n8n_auth_token}'
        }

        # Mask sensitive data for logging
        log_payload_summary = {k: v for k, v in payload.items() if k != 'prompt'}
        log_payload_summary['prompt_length'] = len(payload.get('prompt', ''))
        
        _logger.info(
            f"Initiating AI image generation for request ID: {generation_request_dto.request_id}. "
            f"Payload summary: {log_payload_summary}"
        )

        service_name = "N8N AI Service"

        @retry(
            stop=stop_after_attempt(DEFAULT_RETRY_ATTEMPTS),
            wait=wait_exponential(multiplier=RETRY_WAIT_MULTIPLIER, min=RETRY_WAIT_MIN_SECONDS, max=RETRY_WAIT_MAX_SECONDS),
            retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError, TransientIntegrationError)),
            reraise=True
        )
        def _do_request_with_retries():
            _logger.debug(f"Attempting POST to {n8n_webhook_url} for request ID {generation_request_dto.request_id}")
            try:
                response = requests.post(n8n_webhook_url, json=payload, headers=headers, timeout=DEFAULT_TIMEOUT_SECONDS)
                
                if not response.ok: # Handles 4xx and 5xx errors
                    # This will raise an appropriate IntegrationError (Transient or Permanent)
                    handle_external_api_error(response, service_name) 
                
                _logger.info(f"Successfully called N8N for request ID {generation_request_dto.request_id}. Status: {response.status_code}")
                return response
            except requests.exceptions.Timeout as e:
                _logger.warning(f"Timeout calling {service_name} at {n8n_webhook_url} for request ID {generation_request_dto.request_id}: {e}")
                raise TransientIntegrationError(f"Timeout calling {service_name}: {e}") from e
            except requests.exceptions.ConnectionError as e:
                _logger.warning(f"Connection error calling {service_name} at {n8n_webhook_url} for request ID {generation_request_dto.request_id}: {e}")
                raise TransientIntegrationError(f"Connection error calling {service_name}: {e}") from e
            except requests.exceptions.RequestException as e:
                _logger.error(f"RequestException calling {service_name} at {n8n_webhook_url} for request ID {generation_request_dto.request_id}: {e}")
                if e.response is not None:
                    handle_external_api_error(e.response, service_name) # This will raise
                raise PermanentIntegrationError(f"Unhandled RequestException for {service_name}: {e}") from e

        try:
            response = _do_request_with_retries()
            return {
                "success": True,
                "message": "N8N AI image generation request successfully sent.",
                "n8n_response_status": response.status_code,
                "data": response.json() if response.content else None,
            }
        except AuthenticationError as e:
            _logger.error(f"Authentication error with {service_name} for request ID {generation_request_dto.request_id}: {e}")
            return {"success": False, "message": str(e), "n8n_response_status": getattr(e, 'status_code', None)}
        except RateLimitError as e:
            _logger.error(f"Rate limit exceeded for {service_name} for request ID {generation_request_dto.request_id}: {e}")
            return {"success": False, "message": str(e), "n8n_response_status": getattr(e, 'status_code', None)}
        except PermanentIntegrationError as e:
            _logger.error(f"Permanent error with {service_name} for request ID {generation_request_dto.request_id}: {e}")
            return {"success": False, "message": str(e), "n8n_response_status": getattr(e, 'status_code', None)}
        except TransientIntegrationError as e: # This means retries failed
            _logger.error(f"Transient error with {service_name} after retries for request ID {generation_request_dto.request_id}: {e}")
            return {"success": False, "message": str(e), "n8n_response_status": getattr(e, 'status_code', None)}
        except Exception as e:
            _logger.exception(f"Unexpected error during N8N AI image generation for request ID {generation_request_dto.request_id}.")
            return {"success": False, "message": f"Unexpected error: {str(e)}", "n8n_response_status": None}

```