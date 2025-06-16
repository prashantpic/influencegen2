# -*- coding: utf-8 -*-
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from odoo import api, models

_logger = logging.getLogger(__name__)

# --- Placeholder DTOs for Payment Gateway Interactions ---
# These are conceptual structures. Concrete gateway implementations will define or use more specific DTOs.

class PaymentInitiationRequestDTO:
    """
    Conceptual DTO for initiating a payment.
    Actual fields will vary significantly by payment gateway.
    """
    def __init__(self,
                 amount: float,
                 currency: str, # ISO 4217 currency code (e.g., 'USD', 'EUR')
                 recipient_details: Dict[str, Any], # e.g., bank account ID, card token, email for PayPal
                 payment_method_type: str, # e.g., 'bank_transfer', 'card', 'paypal'
                 reference: str, # Internal Odoo payment reference or vendor bill ID
                 description: Optional[str] = None,
                 metadata: Optional[Dict[str, Any]] = None, # For additional gateway-specific data
                 **kwargs):
        self.amount = amount
        self.currency = currency
        self.recipient_details = recipient_details # Potentially sensitive, handle with care
        self.payment_method_type = payment_method_type
        self.reference = reference
        self.description = description
        self.metadata = metadata if metadata is not None else {}
        self.__dict__.update(kwargs) # Allow for other gateway-specific fields

class PaymentStatusResponseDTO:
    """
    Conceptual DTO for representing the status of a payment.
    Actual fields will vary.
    """
    def __init__(self,
                 transaction_id: str, # Gateway's unique transaction ID
                 status: str, # Gateway-specific status (e.g., 'succeeded', 'pending', 'failed', 'requires_action')
                 amount: Optional[float] = None,
                 currency: Optional[str] = None,
                 error_code: Optional[str] = None, # Gateway's error code if failed
                 error_message: Optional[str] = None, # Human-readable error message
                 processed_at: Optional[str] = None, # ISO 8601 timestamp when processed
                 original_response: Optional[Dict[str, Any]] = None, # Full raw response from gateway
                 **kwargs):
        self.transaction_id = transaction_id
        self.status = status
        self.amount = amount
        self.currency = currency
        self.error_code = error_code
        self.error_message = error_message
        self.processed_at = processed_at
        self.original_response = original_response if original_response is not None else {}
        self.__dict__.update(kwargs)

# --- Abstract Base Class for Payment Gateway Clients ---

class PaymentGatewayClientBase(models.AbstractModel, ABC):
    """
    Abstract Base Class for Payment Gateway Clients.
    Defines a common interface for initiating payments and checking their status.
    Concrete implementations for specific gateways (e.g., Stripe, PayPal) will inherit this.
    REQ-IPF-012
    """
    _name = 'influence_gen.payment.gateway.client.base'
    _description = 'Abstract Base for Payment Gateway Clients'

    # To be defined by concrete gateway client implementations
    GATEWAY_NAME: str = "AbstractPaymentGateway"

    # Configuration parameter keys for base URL and API key.
    # Concrete clients should override these with their specific param names.
    BASE_URL_PARAM: Optional[str] = None # e.g., "influence_gen.payment_gateway.stripe.base_url"
    API_KEY_PARAM: Optional[str] = None  # e.g., "influence_gen.payment_gateway.stripe.api_key"

    # Note: Odoo AbstractModels get `self.env` automatically in methods decorated with @api.model etc.
    # No explicit __init__(self, env) is typically used for services.

    @abstractmethod
    @api.model
    def initiate_payment(self, payment_request: PaymentInitiationRequestDTO) -> PaymentStatusResponseDTO:
        """
        Initiates a payment through the specific payment gateway.

        :param payment_request: A DTO containing all necessary details for the payment.
                                The structure of this DTO will be highly gateway-specific.
        :return: A DTO representing the initial status of the payment attempt from the gateway.
        :raises PaymentGatewayError: or a more specific subclass (e.g., PaymentProcessingError,
                                    PaymentConfigurationError) if the initiation fails.
        :raises ConfigurationError: if gateway configuration is missing/invalid.
        """
        _logger.info(f"[{self.GATEWAY_NAME}] Abstract initiate_payment called for reference: {payment_request.reference}")
        # Concrete implementations will:
        # 1. Retrieve configurations (API keys, URLs) using self._get_service_config() (if inheriting BaseAPIClient)
        #    or similar logic.
        # 2. Map PaymentInitiationRequestDTO to the gateway's specific API request format.
        # 3. Make the API call using HttpClientWrapper or gateway's SDK.
        # 4. Handle API responses, map to PaymentStatusResponseDTO.
        # 5. Raise appropriate exceptions on failure.
        raise NotImplementedError("Concrete payment gateway client must implement 'initiate_payment'.")

    @abstractmethod
    @api.model
    def get_payment_status(self, transaction_id: str,
                           metadata: Optional[Dict[str, Any]] = None) -> PaymentStatusResponseDTO:
        """
        Retrieves the status of a previously initiated payment from the gateway.

        :param transaction_id: The payment gateway's unique transaction identifier.
        :param metadata: Optional additional data needed by some gateways to fetch status.
        :return: A DTO representing the current status of the payment.
        :raises PaymentGatewayError: or a subclass if status retrieval fails.
        :raises ConfigurationError: if gateway configuration is missing/invalid.
        """
        _logger.info(f"[{self.GATEWAY_NAME}] Abstract get_payment_status called for transaction ID: {transaction_id}")
        # Concrete implementations will:
        # 1. Retrieve configurations.
        # 2. Make an API call to the gateway's status endpoint.
        # 3. Handle API responses, map to PaymentStatusResponseDTO.
        # 4. Raise appropriate exceptions on failure.
        raise NotImplementedError("Concrete payment gateway client must implement 'get_payment_status'.")

    # Optional: Common helper methods for concrete clients, if applicable.
    # For example, if many gateways use similar auth, it could be part of a shared base,
    # or concrete clients might also inherit from `BaseAPIClient`.

    @api.model
    def _get_sensitive_headers_to_mask(self) -> List[str]:
        """
        Returns a list of header names whose values should be masked in logs.
        Concrete payment gateways should override and extend this.
        """
        headers_to_mask = ['Authorization', 'X-Api-Key', 'Api-Key', 'Client-Secret']
        if self.API_KEY_PARAM: # Assuming API_KEY_PARAM stores the actual header name or part of it
            # This is a basic attempt; concrete classes need to be more specific.
             header_name_from_param = self.API_KEY_PARAM.split('.')[-1].replace('_', '-').title()
             if header_name_from_param not in headers_to_mask:
                 headers_to_mask.append(header_name_from_param)
        return headers_to_mask

    @api.model
    def _get_sensitive_json_fields_to_mask(self) -> List[str]:
        """
        Returns a list of JSON field names whose values should be masked in logs.
        Concrete payment gateways should override and extend this to include fields
        like 'account_number', 'card_number', 'cvv', 'token', etc.
        """
        return ['token', 'secret', 'key', 'access_token', 'refresh_token',
                'account_number', 'card_number', 'cvc', 'cvv', 'card_expiry',
                'bank_account_token', 'card_token']

    # Example of how a concrete client might be structured if it also uses BaseAPIClient:
    #
    # class StripePaymentClient(BaseAPIClient, PaymentGatewayClientBase): # Multiple inheritance
    #     _name = 'influence_gen.stripe.payment.client'
    #     _description = 'Stripe Payment Gateway Client'
    #
    #     GATEWAY_NAME = "Stripe"
    #     BASE_URL_PARAM = "influence_gen.payment_gateway.stripe.base_url" # e.g., "https://api.stripe.com"
    #     API_KEY_PARAM = "influence_gen.payment_gateway.stripe.secret_key"
    #
    #     @api.model
    #     def _get_default_headers(self, api_key: Optional[str] = None) -> Dict[str, str]:
    #         headers = super()._get_default_headers(api_key) # Gets Accept from BaseAPIClient
    #         if not api_key:
    #             raise ConfigurationError("Stripe API Secret Key is not configured.", self.GATEWAY_NAME, self.API_KEY_PARAM)
    #         headers['Authorization'] = f'Bearer {api_key}'
    #         headers['Stripe-Version'] = '2020-08-27' # Example Stripe API version
    #         return headers
    #
    #     @api.model
    #     def initiate_payment(self, payment_request: PaymentInitiationRequestDTO) -> PaymentStatusResponseDTO:
    #         # ... implementation using self._make_request ...
    #         pass
    #
    #     @api.model
    #     def get_payment_status(self, transaction_id: str, metadata: Optional[Dict[str, Any]] = None) -> PaymentStatusResponseDTO:
    #         # ... implementation using self._make_request ...
    #         pass