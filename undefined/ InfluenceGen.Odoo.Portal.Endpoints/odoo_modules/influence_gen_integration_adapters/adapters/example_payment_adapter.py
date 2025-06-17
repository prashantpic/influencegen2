```python
import logging
import dataclasses
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from odoo import models, api

from ..dtos.payment_dtos import (
    PaymentInitiationRequestDto, PaymentResultDto,
    BankAccountVerificationRequestDto, BankAccountVerificationResultDto
)
from ..utils.integration_error_handler import (
    handle_external_api_error,
    IntegrationServiceError,
    TransientIntegrationError,
    PermanentIntegrationError,
    AuthenticationError,
    RateLimitError,
)
from .payment_gateway_adapter_base import PaymentGatewayAdapterBase # For type hinting if needed

_logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = 45 
DEFAULT_RETRY_ATTEMPTS = 3
RETRY_WAIT_MULTIPLIER = 1
RETRY_WAIT_MIN_SECONDS = 2
RETRY_WAIT_MAX_SECONDS = 10
SERVICE_NAME = "Example Payment Gateway"

class ExamplePaymentAdapter(models.AbstractModel):
    _name = 'influence_gen.example.payment.adapter'
    _inherit = 'influence_gen.payment.gateway.adapter.base'
    _description = 'Example Payment Gateway Adapter'

    def _get_config_params(self):
        """Fetches Example Payment Gateway configuration parameters."""
        IrConfigParameter = self.env['ir.config_parameter'].sudo()
        # Assuming similar naming convention for payment gateway config
        api_url = IrConfigParameter.get_param('influence_gen.example_payment.api_url')
        api_key = IrConfigParameter.get_param('influence_gen.example_payment.api_key')
        return api_url, api_key

    def _common_request_logic(self, endpoint_path: str, request_dto, log_identifier: str, result_dto_class, success_log_message: str):
        api_url_base, api_key = self._get_config_params()

        if not api_url_base:
            _logger.error(f"{SERVICE_NAME} API URL ('influence_gen.example_payment.api_url') is not configured.")
            return result_dto_class(id_field=log_identifier, status="error_config", reason_message=f"{SERVICE_NAME} API URL not configured.") # Assuming DTOs have a common ID field for logging
        if not api_key:
            _logger.error(f"{SERVICE_NAME} API Key ('influence_gen.example_payment.api_key') is not configured.")
            return result_dto_class(id_field=log_identifier, status="error_config", reason_message=f"{SERVICE_NAME} API Key not configured.")
        
        api_url = f"{api_url_base.rstrip('/')}/{endpoint_path.lstrip('/')}"
        payload = dataclasses.asdict(request_dto)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}' # Example auth
        }
        
        _logger.info(f"Initiating request for {log_identifier} to {SERVICE_NAME} at {api_url}.")

        @retry(
            stop=stop_after_attempt(DEFAULT_RETRY_ATTEMPTS),
            wait=wait_exponential(multiplier=RETRY_WAIT_MULTIPLIER, min=RETRY_WAIT_MIN_SECONDS, max=RETRY_WAIT_MAX_SECONDS),
            retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError, TransientIntegrationError)),
            reraise=True
        )
        def _do_request_with_retries():
            _logger.debug(f"Attempting POST to {api_url} for {log_identifier}")
            try:
                response = requests.post(api_url, json=payload, headers=headers, timeout=DEFAULT_TIMEOUT_SECONDS)
                if not response.ok:
                    handle_external_api_error(response, SERVICE_NAME)
                
                _logger.info(f"Successfully called {SERVICE_NAME} for {log_identifier}. Status: {response.status_code}")
                return response
            except requests.exceptions.Timeout as e:
                _logger.warning(f"Timeout calling {SERVICE_NAME} at {api_url} for {log_identifier}: {e}")
                raise TransientIntegrationError(f"Timeout calling {SERVICE_NAME}: {e}") from e
            except requests.exceptions.ConnectionError as e:
                _logger.warning(f"Connection error calling {SERVICE_NAME} at {api_url} for {log_identifier}: {e}")
                raise TransientIntegrationError(f"Connection error calling {SERVICE_NAME}: {e}") from e
            except requests.exceptions.RequestException as e:
                _logger.error(f"RequestException calling {SERVICE_NAME} at {api_url} for {log_identifier}: {e}")
                if e.response is not None:
                    handle_external_api_error(e.response, SERVICE_NAME)
                raise PermanentIntegrationError(f"Unhandled RequestException for {SERVICE_NAME}: {e}") from e
        
        id_field_name = None
        if hasattr(request_dto, 'payment_record_id'):
            id_field_name = 'payment_record_id'
        elif hasattr(request_dto, 'bank_account_id'):
             id_field_name = 'bank_account_id'


        try:
            response = _do_request_with_retries()
            response_data = response.json()
            
            # Dynamically create DTO, assuming constructor matches keys or specific mapping
            # This is a simplification; real mapping might be more complex
            constructor_args = {id_field_name: getattr(request_dto, id_field_name) if id_field_name else None}
            constructor_args.update(response_data) 
            # Filter args to only those expected by the DTO constructor
            valid_args = {k: v for k, v in constructor_args.items() if k in result_dto_class.__dataclass_fields__}
            
            result = result_dto_class(**valid_args)
            _logger.info(success_log_message.format(id=log_identifier, status=result.status))
            return result
        except AuthenticationError as e:
            _logger.error(f"Authentication error with {SERVICE_NAME} for {log_identifier}: {e}")
            return result_dto_class(**{id_field_name: getattr(request_dto, id_field_name), 'status': "error_auth", 'reason_message': str(e)})
        except RateLimitError as e:
            _logger.error(f"Rate limit exceeded for {SERVICE_NAME} for {log_identifier}: {e}")
            return result_dto_class(**{id_field_name: getattr(request_dto, id_field_name), 'status': "error_rate_limit", 'reason_message': str(e)})
        except PermanentIntegrationError as e:
            _logger.error(f"Permanent error with {SERVICE_NAME} for {log_identifier}: {e}")
            return result_dto_class(**{id_field_name: getattr(request_dto, id_field_name), 'status': "error_permanent", 'reason_message': str(e)})
        except TransientIntegrationError as e: # Retries failed
            _logger.error(f"Transient error with {SERVICE_NAME} after retries for {log_identifier}: {e}")
            return result_dto_class(**{id_field_name: getattr(request_dto, id_field_name), 'status': "error_transient", 'reason_message': str(e)})
        except requests.exceptions.JSONDecodeError as e:
            _logger.error(f"Failed to decode JSON response from {SERVICE_NAME} for {log_identifier}: {e}")
            return result_dto_class(**{id_field_name: getattr(request_dto, id_field_name), 'status': "error_response_format", 'reason_message': "Invalid response format."})

        except Exception as e:
            _logger.exception(f"Unexpected error during operation for {log_identifier} with {SERVICE_NAME}.")
            return result_dto_class(**{id_field_name: getattr(request_dto, id_field_name), 'status': "error_unexpected", 'reason_message': f"Unexpected error: {str(e)}"})


    def initiate_payment(self, payment_request_dto: PaymentInitiationRequestDto) -> PaymentResultDto:
        return self._common_request_logic(
            endpoint_path="payments/initiate", # Example endpoint
            request_dto=payment_request_dto,
            log_identifier=f"payment_record_id {payment_request_dto.payment_record_id}",
            result_dto_class=PaymentResultDto,
            success_log_message="Payment initiation for {id} completed with status: {status}"
        )

    def verify_bank_account(self, bank_details_dto: BankAccountVerificationRequestDto) -> BankAccountVerificationResultDto:
        return self._common_request_logic(
            endpoint_path="bankaccounts/verify", # Example endpoint
            request_dto=bank_details_dto,
            log_identifier=f"bank_account_id {bank_details_dto.bank_account_id}",
            result_dto_class=BankAccountVerificationResultDto,
            success_log_message="Bank account verification for {id} completed with status: {status}"
        )

```