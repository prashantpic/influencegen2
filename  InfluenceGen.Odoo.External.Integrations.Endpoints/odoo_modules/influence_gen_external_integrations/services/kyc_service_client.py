# -*- coding: utf-8 -*-
import logging
from typing import Dict, Any, List
from odoo import api, models, _
# from odoo.exceptions import UserError # Not directly used here, but good practice

from .base_api_client import BaseAPIClient
from ..models.kyc.kyc_verification_request import KYCVerificationRequest
from ..models.kyc.kyc_verification_response import KYCVerificationResponse
from ..exceptions.kyc_exceptions import KYCServiceError, KYCVerificationFailedError, KYCDocumentInvalidError
from ..exceptions.common_exceptions import ApiCommunicationError, ConfigurationError, ExternalServiceError

_logger = logging.getLogger(__name__)

class KYCServiceClient(BaseAPIClient):
    _name = 'influence_gen.kyc.service.client'
    _description = 'Client for Third-Party KYC Identity Verification Service'

    SERVICE_NAME = "KYCService"
    BASE_URL_PARAM = "influence_gen.kyc_service.base_url"
    API_KEY_PARAM = "influence_gen.kyc_service.api_key" # Name of the ir.config_parameter key

    @api.model
    def _get_default_headers(self, api_key: str) -> Dict[str, str]:
        """
        Provides KYC-specific default headers, including API key authentication.
        This method should be adapted based on the specific KYC service's authentication requirements.
        """
        headers = super()._get_default_headers(api_key) # Gets basic headers like 'Accept'
        if not api_key:
             # API key is typically critical for KYC services
             _logger.error(f"API Key for {self.SERVICE_NAME} is not configured (param: {self.API_KEY_PARAM}). This is required.")
             raise ConfigurationError(
                 f"API Key for {self.SERVICE_NAME} is not configured.",
                 service_name=self.SERVICE_NAME,
                 setting_key=self.API_KEY_PARAM
            )
        # Example: many services use 'X-API-KEY' or 'Authorization: Bearer <token>'
        # Please adapt this to the chosen KYC service's API documentation.
        headers['X-API-KEY'] = api_key
        # OR headers['Authorization'] = f'Bearer {api_key}'
        return headers

    @api.model
    def _get_sensitive_headers_to_mask(self) -> List[str]:
        """Specifies headers to mask for KYC service logs."""
        return super()._get_sensitive_headers_to_mask() + ['X-API-KEY'] # Add service-specific auth header

    @api.model
    def _get_sensitive_json_fields_to_mask(self) -> List[str]:
        """Specifies JSON fields to mask for KYC service logs (if logging request/response bodies)."""
        return super()._get_sensitive_json_fields_to_mask() + [
            'document_image_front_b64',
            'document_image_back_b64',
            'first_name',
            'last_name',
            'dob',
            'address', # Potentially entire address object
            # Any fields in extracted_data that are PII
        ]

    @api.model
    def verify_identity_document(self, request_data: KYCVerificationRequest) -> KYCVerificationResponse:
        """
        Submits identity document for verification to the third-party KYC service.
        REQ-IOKYC-005, REQ-IL-011

        :param request_data: DTO containing data for the verification request.
        :return: DTO containing the response details from the KYC service.
        :raises KYCServiceError: For general communication or service-specific errors.
        :raises KYCVerificationFailedError: If the service explicitly returns a 'failed' or 'rejected' status.
        :raises KYCDocumentInvalidError: If the service indicates the submitted document is invalid.
        :raises ConfigurationError: If essential configuration (URL, API Key) is missing.
        """
        _logger.info(f"Attempting to verify identity for influencer ID (ref): {request_data.influencer_id} via {self.SERVICE_NAME}")

        # Construct the payload based on the specific KYC service API requirements.
        # This is an example and likely needs adjustment.
        payload = {
            "document_front_b64": request_data.document_image_front_b64,
            "document_back_b64": request_data.document_image_back_b64, # May be optional
            "document_type": request_data.document_type,
            "influencer_reference": str(request_data.influencer_id), # Ensure it's a string if API expects that
            "first_name": request_data.first_name,
            "last_name": request_data.last_name,
            "date_of_birth": request_data.dob, # API might expect 'date_of_birth' or similar
            "address": request_data.address,   # This could be a nested dictionary
            "country": request_data.country_code, # API might expect 'country'
            "metadata": request_data.metadata,
            # "callback_url": "your_odoo_instance_callback_url" # If using async callbacks
        }
        # Remove None or empty values from payload for a cleaner request, if the API prefers this
        payload = {k: v for k, v in payload.items() if v is not None and v != {} and v != ""}

        try:
            # The API endpoint is an example; replace with the actual KYC service endpoint.
            response_json = self._make_request(
                method='POST',
                endpoint='/v1/verifications/identity', # Example endpoint
                json_data=payload
            )

            # Map JSON response from the service to the KYCVerificationResponse DTO.
            # This mapping is highly dependent on the specific KYC service's response structure.
            response_dto = KYCVerificationResponse(
                transaction_id=response_json.get('transaction_id', response_json.get('id')), # Common alternatives
                status=str(response_json.get('status', 'UNKNOWN')).upper(), # Normalize status
                reason=response_json.get('reason', response_json.get('message')), # Common alternatives
                reason_code=str(response_json.get('reason_code', response_json.get('code', ''))), # Common alternatives
                extracted_data=response_json.get('extracted_data', response_json.get('data', {})), # Common alternatives
                kyc_score=float(response_json.get('score')) if response_json.get('score') is not None else None,
                document_validity=str(response_json.get('document_validity','')),
                face_match_score=float(response_json.get('face_match_score')) if response_json.get('face_match_score') is not None else None,
                original_response=response_json # Store the full original response for auditing/debugging
            )

            # Handle specific failure statuses from the KYC service
            # These status strings are examples and must match the actual service's responses.
            if response_dto.status in ['REJECTED', 'FAILED', 'DENIED']:
                 _logger.warning(
                     f"{self.SERVICE_NAME} verification failed for influencer (ref) {request_data.influencer_id}, "
                     f"transaction {response_dto.transaction_id}. Status: {response_dto.status}, Reason: {response_dto.reason}"
                 )
                 raise KYCVerificationFailedError(
                     message=f"KYC verification explicitly failed: {response_dto.reason or 'No specific reason provided by service.'}",
                     reason_code=response_dto.reason_code,
                     original_exception=response_json # Pass original response for context
                 )
            elif response_dto.status in ['INVALID_DOCUMENT', 'DOCUMENT_ERROR', 'UNSUPPORTED_DOCUMENT']:
                 _logger.warning(
                     f"{self.SERVICE_NAME} reported invalid document for influencer (ref) {request_data.influencer_id}, "
                     f"transaction {response_dto.transaction_id}. Status: {response_dto.status}, Reason: {response_dto.reason}"
                 )
                 raise KYCDocumentInvalidError(
                     message=f"KYC service reported document issue: {response_dto.reason or 'Document considered invalid or unprocessable.'}",
                     original_exception=response_json # Pass original response for context
                 )
            elif response_dto.status in ['PENDING', 'IN_REVIEW', 'PROCESSING', 'ACTION_REQUIRED']:
                 _logger.info(
                     f"{self.SERVICE_NAME} verification pending/in review for influencer (ref) {request_data.influencer_id}, "
                     f"transaction {response_dto.transaction_id}. Status: {response_dto.status}"
                 )
                 # This is not an error; the calling code should handle these statuses.

            _logger.info(
                f"{self.SERVICE_NAME} verification processed for influencer (ref) {request_data.influencer_id}, "
                f"transaction {response_dto.transaction_id}. Final Status: {response_dto.status}"
            )
            return response_dto

        except (ApiCommunicationError, ConfigurationError) as e:
            _logger.error(f"{self.SERVICE_NAME} API communication or configuration error for influencer (ref) {request_data.influencer_id}: {e}")
            raise KYCServiceError(
                f"Failed to communicate with or configure {self.SERVICE_NAME}: {e.message}",
                original_exception=e
            )
        except (KYCVerificationFailedError, KYCDocumentInvalidError) as e: # Re-raise specific exceptions
             raise
        except Exception as e: # Catch other unexpected errors during processing
            _logger.exception(f"Unexpected error during {self.SERVICE_NAME} verification for influencer (ref) {request_data.influencer_id}: {e}")
            raise KYCServiceError(
                f"An unexpected error occurred during {self.SERVICE_NAME} verification: {str(e)}",
                original_exception=e
            )

    @api.model
    def get_verification_status(self, transaction_id: str) -> KYCVerificationResponse:
        """
        Retrieves the status of a previous KYC verification attempt from the third-party service.
        REQ-IOKYC-005

        :param transaction_id: The external service's transaction ID for the verification.
        :return: DTO containing the latest status details.
        :raises KYCServiceError: For communication or service-specific errors.
        :raises ConfigurationError: If essential configuration is missing.
        :raises ValueError: If transaction_id is not provided.
        """
        if not transaction_id:
             _logger.error(f"{self.SERVICE_NAME}: Get verification status called without a transaction ID.")
             raise ValueError("Transaction ID is required to fetch KYC verification status.")

        _logger.info(f"Fetching {self.SERVICE_NAME} verification status for transaction: {transaction_id}")

        try:
            # The API endpoint is an example; replace with the actual KYC service endpoint.
            response_json = self._make_request(
                method='GET',
                endpoint=f'/v1/verifications/identity/{transaction_id}' # Example endpoint
            )

            # Map JSON response to DTO (similar to verify_identity_document response mapping)
            response_dto = KYCVerificationResponse(
                transaction_id=response_json.get('transaction_id', transaction_id), # Fallback to passed ID
                status=str(response_json.get('status', 'UNKNOWN')).upper(),
                reason=response_json.get('reason', response_json.get('message')),
                reason_code=str(response_json.get('reason_code', response_json.get('code', ''))),
                extracted_data=response_json.get('extracted_data', response_json.get('data', {})),
                kyc_score=float(response_json.get('score')) if response_json.get('score') is not None else None,
                document_validity=str(response_json.get('document_validity','')),
                face_match_score=float(response_json.get('face_match_score')) if response_json.get('face_match_score') is not None else None,
                original_response=response_json
            )
            _logger.info(f"Fetched {self.SERVICE_NAME} verification status for transaction {transaction_id}: {response_dto.status}")
            return response_dto

        except (ApiCommunicationError, ConfigurationError) as e:
            _logger.error(f"{self.SERVICE_NAME} API communication or configuration error fetching status for transaction {transaction_id}: {e}")
            raise KYCServiceError(
                f"Failed to fetch {self.SERVICE_NAME} status for {transaction_id}: {e.message}",
                original_exception=e
            )
        except Exception as e:
            _logger.exception(f"Unexpected error fetching {self.SERVICE_NAME} status for transaction {transaction_id}: {e}")
            raise KYCServiceError(
                f"An unexpected error occurred fetching {self.SERVICE_NAME} status for {transaction_id}: {str(e)}",
                original_exception=e
            )