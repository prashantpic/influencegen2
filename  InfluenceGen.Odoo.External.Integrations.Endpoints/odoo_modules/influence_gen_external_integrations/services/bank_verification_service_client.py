# -*- coding: utf-8 -*-
import logging
from typing import Dict, Any, List
from odoo import api, models, _
# from odoo.exceptions import UserError

from .base_api_client import BaseAPIClient
from ..models.bank_verification.bank_verification_request import BankVerificationRequest
from ..models.bank_verification.bank_verification_response import BankVerificationResponse
from ..exceptions.bank_verification_exceptions import BankVerificationServiceError, BankAccountInvalidError, BankVerificationFailedError
from ..exceptions.common_exceptions import ApiCommunicationError, ConfigurationError, ExternalServiceError

_logger = logging.getLogger(__name__)

class BankVerificationServiceClient(BaseAPIClient):
    _name = 'influence_gen.bank.verification.service.client'
    _description = 'Client for Third-Party Bank Account Verification Service'

    SERVICE_NAME = "BankVerificationService"
    BASE_URL_PARAM = "influence_gen.bank_verification.base_url"
    API_KEY_PARAM = "influence_gen.bank_verification.api_key"

    @api.model
    def _get_default_headers(self, api_key: str) -> Dict[str, str]:
        """
        Provides bank verification specific default headers, including API key authentication.
        Adapt based on the specific bank verification service's API documentation.
        """
        headers = super()._get_default_headers(api_key)
        if not api_key:
             _logger.error(f"API Key for {self.SERVICE_NAME} is not configured (param: {self.API_KEY_PARAM}). This is required.")
             raise ConfigurationError(
                 f"API Key for {self.SERVICE_NAME} is not configured.",
                 service_name=self.SERVICE_NAME,
                 setting_key=self.API_KEY_PARAM
            )
        # Example: many services use 'X-API-KEY'
        headers['X-API-KEY'] = api_key
        return headers

    @api.model
    def _get_sensitive_headers_to_mask(self) -> List[str]:
        """Specifies headers to mask for bank verification service logs."""
        return super()._get_sensitive_headers_to_mask() + ['X-API-KEY']

    @api.model
    def _get_sensitive_json_fields_to_mask(self) -> List[str]:
        """Specifies JSON fields to mask for bank verification logs."""
        return super()._get_sensitive_json_fields_to_mask() + [
            'account_number', 'iban', 'routing_number', 'swift_code'
        ]

    @api.model
    def verify_bank_account(self, request_data: BankVerificationRequest) -> BankVerificationResponse:
        """
        Submits bank account details for verification to the third-party service.
        REQ-IOKYC-008, REQ-IPF-002

        :param request_data: DTO containing bank account data.
        :return: DTO containing the response details from the bank verification service.
        :raises BankVerificationServiceError: For general communication or service-specific errors.
        :raises BankAccountInvalidError: If the service indicates the submitted account details are invalid.
        :raises BankVerificationFailedError: If the service explicitly returns a 'failed' or 'rejected' status.
        :raises ConfigurationError: If essential configuration is missing.
        """
        _logger.info(f"Attempting bank account verification for influencer ID (ref): {request_data.influencer_id} via {self.SERVICE_NAME}")

        # Construct payload based on specific API requirements. This is an example.
        payload = {
            "account_holder_name": request_data.account_holder_name,
            "account_number": request_data.account_number,
            "routing_number": request_data.routing_number, # Or sort_code for UK, etc.
            "iban": request_data.iban,
            "swift_bic": request_data.swift_code, # API might expect 'swift_bic'
            "bank_name": request_data.bank_name,
            "country_code": request_data.country_code, # ISO 3166-1 Alpha-2
            "currency": request_data.currency_code, # ISO 4217, if required by API
            "external_reference_id": str(request_data.influencer_id), # Ensure string if API expects that
            # Some services might require account type (checking, savings)
        }
        payload = {k: v for k, v in payload.items() if v is not None and v != ""}

        try:
            # API endpoint is an example.
            response_json = self._make_request(
                method='POST',
                endpoint='/v1/bank-accounts/verify', # Example endpoint
                json_data=payload
            )

            # Map JSON response to DTO. Highly dependent on service's response.
            response_dto = BankVerificationResponse(
                transaction_id=response_json.get('transaction_id', response_json.get('id')),
                status=str(response_json.get('status', 'UNKNOWN')).upper(),
                reason=response_json.get('reason', response_json.get('message')),
                reason_code=str(response_json.get('reason_code', response_json.get('code', ''))),
                account_holder_name_matched=response_json.get('account_holder_name_matched'), # boolean
                is_valid_account=response_json.get('is_valid_account'), # boolean
                microdeposit_amounts=response_json.get('microdeposit_amounts'), # List of floats if applicable
                original_response=response_json
            )

            # Handle specific failure statuses
            if response_dto.status in ['FAILED', 'REJECTED', 'ERROR']:
                 _logger.warning(
                     f"{self.SERVICE_NAME} bank verification failed for influencer (ref) {request_data.influencer_id}, "
                     f"transaction {response_dto.transaction_id}. Status: {response_dto.status}, Reason: {response_dto.reason}"
                 )
                 raise BankVerificationFailedError(
                     message=f"Bank verification explicitly failed: {response_dto.reason or 'No specific reason provided.'}",
                     reason_code=response_dto.reason_code,
                     original_exception=response_json
                 )
            elif response_dto.status in ['INVALID_ACCOUNT_DETAILS', 'INVALID_BANK_CODE', 'ACCOUNT_NOT_FOUND']:
                 _logger.warning(
                     f"{self.SERVICE_NAME} reported invalid bank account details for influencer (ref) {request_data.influencer_id}, "
                     f"transaction {response_dto.transaction_id}. Status: {response_dto.status}, Reason: {response_dto.reason}"
                 )
                 raise BankAccountInvalidError(
                     message=f"Bank verification service reported invalid account details: {response_dto.reason or 'Details considered invalid.'}",
                     original_exception=response_json
                 )
            elif response_dto.status in ['PENDING', 'PROCESSING', 'MICRODEPOSIT_INITIATED', 'AWAITING_VERIFICATION']:
                 _logger.info(
                     f"{self.SERVICE_NAME} bank verification pending/processing for influencer (ref) {request_data.influencer_id}, "
                     f"transaction {response_dto.transaction_id}. Status: {response_dto.status}"
                 )
                 # Not an error.

            _logger.info(
                f"{self.SERVICE_NAME} bank verification processed for influencer (ref) {request_data.influencer_id}, "
                f"transaction {response_dto.transaction_id}. Final Status: {response_dto.status}"
            )
            return response_dto

        except (ApiCommunicationError, ConfigurationError) as e:
            _logger.error(f"{self.SERVICE_NAME} API communication or configuration error for influencer (ref) {request_data.influencer_id}: {e}")
            raise BankVerificationServiceError(
                f"Failed to communicate with or configure {self.SERVICE_NAME}: {e.message}",
                original_exception=e
            )
        except (BankVerificationFailedError, BankAccountInvalidError) as e: # Re-raise specific
             raise
        except Exception as e:
            _logger.exception(f"Unexpected error during {self.SERVICE_NAME} bank verification for influencer (ref) {request_data.influencer_id}: {e}")
            raise BankVerificationServiceError(
                f"An unexpected error occurred during {self.SERVICE_NAME} bank verification: {str(e)}",
                original_exception=e
            )

    @api.model
    def get_verification_status(self, transaction_id: str) -> BankVerificationResponse:
        """
        Retrieves the status of a previous bank account verification from the third-party service.
        REQ-IOKYC-008

        :param transaction_id: The external service's transaction ID.
        :return: DTO containing the latest status details.
        :raises BankVerificationServiceError: For communication or service-specific errors.
        :raises ConfigurationError: If essential configuration is missing.
        :raises ValueError: If transaction_id is not provided.
        """
        if not transaction_id:
             _logger.error(f"{self.SERVICE_NAME}: Get verification status called without a transaction ID.")
             raise ValueError("Transaction ID is required to fetch bank verification status.")

        _logger.info(f"Fetching {self.SERVICE_NAME} bank verification status for transaction: {transaction_id}")

        try:
            # API endpoint is an example.
            response_json = self._make_request(
                method='GET',
                endpoint=f'/v1/bank-accounts/verify/{transaction_id}' # Example endpoint
            )

            # Map JSON response to DTO (similar to verify_bank_account response mapping)
            response_dto = BankVerificationResponse(
                transaction_id=response_json.get('transaction_id', transaction_id),
                status=str(response_json.get('status', 'UNKNOWN')).upper(),
                reason=response_json.get('reason', response_json.get('message')),
                reason_code=str(response_json.get('reason_code', response_json.get('code', ''))),
                account_holder_name_matched=response_json.get('account_holder_name_matched'),
                is_valid_account=response_json.get('is_valid_account'),
                microdeposit_amounts=response_json.get('microdeposit_amounts'),
                original_response=response_json
            )
            _logger.info(f"Fetched {self.SERVICE_NAME} bank verification status for transaction {transaction_id}: {response_dto.status}")
            return response_dto

        except (ApiCommunicationError, ConfigurationError) as e:
            _logger.error(f"{self.SERVICE_NAME} API communication error fetching status for transaction {transaction_id}: {e}")
            raise BankVerificationServiceError(
                f"Failed to fetch {self.SERVICE_NAME} status for {transaction_id}: {e.message}",
                original_exception=e
            )
        except Exception as e:
            _logger.exception(f"Unexpected error fetching {self.SERVICE_NAME} status for transaction {transaction_id}: {e}")
            raise BankVerificationServiceError(
                f"An unexpected error occurred fetching {self.SERVICE_NAME} status for {transaction_id}: {str(e)}",
                original_exception=e
            )