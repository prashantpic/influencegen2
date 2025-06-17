# Software Design Specification: InfluenceGen.Odoo.External.Integrations.Endpoints

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the `InfluenceGen.Odoo.External.Integrations.Endpoints` Odoo module. This module is responsible for managing Odoo's outbound integration points with various third-party services, including Know Your Customer (KYC) identity verification, bank account verification, and internal integration with Odoo's Accounting module for influencer payments. It aims to abstract the complexities of external API interactions, providing a clean interface for other InfluenceGen modules.

### 1.2 Scope
The scope of this module includes:
-   Secure management and retrieval of API credentials for external services.
-   Implementation of API client services to interact with:
    -   Third-party KYC identity verification services (optional, if chosen over manual).
    -   Third-party bank account verification services (optional, if chosen over manual).
    -   Future third-party payment gateways (architectural preparedness).
-   Integration service for creating vendor bills in Odoo's native Accounting module.
-   Definition of Data Transfer Objects (DTOs) for request and response payloads of external APIs.
-   Custom exception handling for integration-related errors.
-   A standardized HTTP client wrapper for external API calls.

### 1.3 Definitions, Acronyms, and Abbreviations
-   **SDS**: Software Design Specification
-   **KYC**: Know Your Customer
-   **API**: Application Programming Interface
-   **DTO**: Data Transfer Object
-   **ORM**: Object-Relational Mapper
-   **HTTP**: Hypertext Transfer Protocol
-   **JSON**: JavaScript Object Notation
-   **REST**: Representational State Transfer
-   **IaC**: Infrastructure as Code
-   **PII**: Personally Identifiable Information
-   **UAT**: User Acceptance Testing
-   **ETL**: Extract, Transform, Load

## 2. System Overview
The `InfluenceGen.Odoo.External.Integrations.Endpoints` module acts as an infrastructure and integration services layer within the larger InfluenceGen Odoo platform. It sits between the core business logic layer of InfluenceGen and external third-party services or Odoo's own core modules like Accounting. Its primary function is to encapsulate the communication details, authentication, and data mapping required to interact with these external dependencies.

## 3. Design Considerations

### 3.1 General Design Principles
-   **Modularity:** The module will be structured with clear separation of concerns (configuration, DTOs, clients, exceptions).
-   **Abstraction:** External service intricacies will be hidden behind well-defined service client interfaces.
-   **Security:** Secure handling of API keys and sensitive data is paramount. All external communications will use HTTPS.
-   **Extensibility:** The design will facilitate the addition of new external service integrations with minimal impact (e.g., new payment gateways).
-   **Error Handling:** Robust error handling with custom, specific exceptions will be implemented for better diagnostics.
-   **Testability:** Service clients and utility components will be designed for unit testability.
-   **Odoo Best Practices:** Adherence to Odoo 18 development guidelines, including ORM usage for accounting integration and configuration parameter management.
-   **Python Best Practices:** Code will follow PEP 8 and other relevant Python coding standards.

### 3.2 Technology Stack
-   **Odoo Version:** 18.0
-   **Programming Language:** Python 3.11+
-   **Framework:** Odoo 18 Module Development Framework
-   **Data Exchange Format:** JSON for external APIs
-   **Communication Protocol:** HTTP/1.1 (primarily RESTful APIs)
-   **Key Libraries:**
    -   `requests`: For making HTTP calls to external services.
    -   Odoo ORM: For interacting with Odoo's accounting module.
    -   Odoo `ir.config_parameter`: For storing non-sensitive configuration. Secure storage for sensitive keys.

## 4. Detailed Component Design

This section details the design of each file within the `influence_gen_external_integrations` Odoo module.

### 4.1 Module Initialization

#### 4.1.1 `odoo_modules/influence_gen_external_integrations/__init__.py`
-   **Purpose:** Standard Odoo module initializer. Imports sub-packages and modules to make their components accessible.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import config
    from . import exceptions
    from . import utils
    from . import models # DTOs
    from . import services
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations`

#### 4.1.2 `odoo_modules/influence_gen_external_integrations/__manifest__.py`
-   **Purpose:** Odoo manifest file. Defines module metadata, dependencies, and data files.
-   **Logic (Illustrative Content):**
    python
    # -*- coding: utf-8 -*-
    {
        'name': 'InfluenceGen External Integrations',
        'version': '18.0.1.0.0',
        'summary': 'Handles integrations with external KYC, bank verification, and payment services for InfluenceGen.',
        'author': 'SSS-AI',
        'website': 'https://www.example.com', # Replace with actual website
        'category': 'InfluenceGen/Integrations',
        'depends': [
            'base',         # Core Odoo dependency
            'account',      # For Odoo Accounting integration (REQ-IPF-006)
            # Add other InfluenceGen core module dependencies if services are directly called by them
            # e.g., 'influence_gen_core' if it exists and calls these services.
        ],
        'data': [
            # Security files if any specific models are created for secure config
            # 'security/ir.model.access.csv',
            # Data files (e.g., for default configurations, although ir.config_parameter is preferred for settings)
        ],
        'installable': True,
        'application': False, # This is a supporting module, not a standalone application
        'auto_install': False,
        'license': 'LGPL-3', # Or appropriate license
    }
    
-   **Key Dependencies:** `account` module is critical for REQ-IPF-006 and REQ-2-014.

### 4.2 Configuration (`config/`)

#### 4.2.1 `odoo_modules/influence_gen_external_integrations/config/__init__.py`
-   **Purpose:** Initializes the `config` Python package.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import integration_settings
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.config`

#### 4.2.2 `odoo_modules/influence_gen_external_integrations/config/integration_settings.py`
-   **Purpose:** Centralizes retrieval of external service credentials and configurations. Implements REQ-IL-008.
-   **Logic:**
    -   Uses `self.env['ir.config_parameter'].sudo().get_param('influence_gen.kyc_api_key', default=False)` pattern.
    -   Consider logging warnings if critical settings are missing.
    -   For highly sensitive keys, if Odoo 18 offers a more secure vault-like mechanism than `ir.config_parameter` for addon-specific keys, that should be preferred. Otherwise, `ir.config_parameter` combined with proper server file permissions for Odoo config files is the standard approach.
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.config`
-   **Class `IntegrationSettings` (Conceptual - might be static methods or a service):**
    python
    # -*- coding: utf-8 -*-
    import logging
    from odoo import api, models, _ # if using a model for settings
    from odoo.exceptions import UserError # if using a model for settings

    _logger = logging.getLogger(__name__)

    class IntegrationSettings:
        """
        Utility class to retrieve integration settings.
        Settings are expected to be stored as system parameters (ir.config_parameter).
        """

        @staticmethod
        def _get_param(env, key, default=None):
            """Helper to get system parameter."""
            value = env['ir.config_parameter'].sudo().get_param(key)
            if not value and default is not None:
                return default
            if not value:
                _logger.warning(f"Configuration parameter '{key}' not found and no default provided.")
                # Depending on criticality, could raise ConfigurationError here
            return value

        @staticmethod
        def get_kyc_service_api_key(env):
            """Retrieves the API key for the KYC service. REQ-IL-008"""
            return IntegrationSettings._get_param(env, 'influence_gen.kyc_service.api_key')

        @staticmethod
        def get_kyc_service_base_url(env):
            """Retrieves the base URL for the KYC service."""
            return IntegrationSettings._get_param(env, 'influence_gen.kyc_service.base_url')

        @staticmethod
        def get_bank_verification_api_key(env):
            """Retrieves the API key for the bank verification service. REQ-IL-008"""
            return IntegrationSettings._get_param(env, 'influence_gen.bank_verification.api_key')

        @staticmethod
        def get_bank_verification_base_url(env):
            """Retrieves the base URL for the bank verification service."""
            return IntegrationSettings._get_param(env, 'influence_gen.bank_verification.base_url')

        @staticmethod
        def get_payment_gateway_api_key(env, gateway_name: str):
            """Retrieves the API key for a specific payment gateway. REQ-IL-008, REQ-IPF-012"""
            # Example for a generic gateway, specific gateways might have different param names
            return IntegrationSettings._get_param(env, f'influence_gen.payment_gateway.{gateway_name}.api_key')

        @staticmethod
        def get_payment_gateway_base_url(env, gateway_name: str):
            """Retrieves the base URL for a specific payment gateway. REQ-IPF-012"""
            return IntegrationSettings._get_param(env, f'influence_gen.payment_gateway.{gateway_name}.base_url')

    # Example: To use in a service:
    # from odoo import api, fields, models
    # class MyService(models.AbstractModel):
    #     _name = 'my.service'
    #     _description = 'My Service'
    #
    #     def some_method(self):
    #         api_key = IntegrationSettings.get_kyc_service_api_key(self.env)
    #         # ... use api_key
    

### 4.3 Exceptions (`exceptions/`)

#### 4.3.1 `odoo_modules/influence_gen_external_integrations/exceptions/__init__.py`
-   **Purpose:** Initializes the `exceptions` Python package.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import common_exceptions
    from . import kyc_exceptions
    from . import bank_verification_exceptions
    from . import payment_gateway_exceptions
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.exceptions`

#### 4.3.2 `odoo_modules/influence_gen_external_integrations/exceptions/common_exceptions.py`
-   **Purpose:** Defines base and common custom exceptions.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-

    class ExternalServiceError(Exception):
        """Base class for errors related to external services."""
        def __init__(self, message, service_name=None, original_exception=None):
            super().__init__(message)
            self.service_name = service_name
            self.original_exception = original_exception

    class ConfigurationError(ExternalServiceError):
        """Raised when there's an issue with external service configuration."""
        def __init__(self, message, setting_key=None):
            super().__init__(message, service_name="Configuration")
            self.setting_key = setting_key

    class ApiCommunicationError(ExternalServiceError):
        """Raised for network issues or non-2xx HTTP responses during API communication."""
        def __init__(self, message, service_name=None, status_code=None, response_content=None, original_exception=None):
            super().__init__(message, service_name=service_name, original_exception=original_exception)
            self.status_code = status_code
            self.response_content = response_content
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.exceptions`

#### 4.3.3 `odoo_modules/influence_gen_external_integrations/exceptions/kyc_exceptions.py`
-   **Purpose:** Defines custom exceptions for KYC service integrations. Implements REQ-IOKYC-005, REQ-IL-011.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from .common_exceptions import ExternalServiceError

    class KYCServiceError(ExternalServiceError):
        """Base class for KYC service specific errors."""
        def __init__(self, message, original_exception=None):
            super().__init__(message, service_name="KYCService", original_exception=original_exception)

    class KYCVerificationFailedError(KYCServiceError):
        """Raised when KYC verification explicitly fails according to the service."""
        def __init__(self, message, reason_code=None, original_exception=None):
            super().__init__(message, original_exception=original_exception)
            self.reason_code = reason_code

    class KYCDocumentInvalidError(KYCServiceError):
        """Raised when the KYC service deems the submitted document invalid."""
        pass
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.exceptions`

#### 4.3.4 `odoo_modules/influence_gen_external_integrations/exceptions/bank_verification_exceptions.py`
-   **Purpose:** Defines custom exceptions for bank account verification. Implements REQ-IOKYC-008, REQ-IPF-002.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from .common_exceptions import ExternalServiceError

    class BankVerificationServiceError(ExternalServiceError):
        """Base class for bank verification service specific errors."""
        def __init__(self, message, original_exception=None):
            super().__init__(message, service_name="BankVerificationService", original_exception=original_exception)

    class BankAccountInvalidError(BankVerificationServiceError):
        """Raised when the bank account details are considered invalid by the service."""
        pass

    class BankVerificationFailedError(BankVerificationServiceError):
        """Raised when bank account verification explicitly fails."""
        def __init__(self, message, reason_code=None, original_exception=None):
            super().__init__(message, original_exception=original_exception)
            self.reason_code = reason_code
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.exceptions`

#### 4.3.5 `odoo_modules/influence_gen_external_integrations/exceptions/payment_gateway_exceptions.py`
-   **Purpose:** Defines custom exceptions for future payment gateway integrations. Implements REQ-IPF-012.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from .common_exceptions import ExternalServiceError

    class PaymentGatewayError(ExternalServiceError):
        """Base class for payment gateway specific errors."""
        def __init__(self, message, gateway_name=None, original_exception=None):
            super().__init__(message, service_name=f"PaymentGateway({gateway_name})", original_exception=original_exception)
            self.gateway_name = gateway_name

    class PaymentProcessingError(PaymentGatewayError):
        """Raised when a payment processing attempt fails at the gateway."""
        def __init__(self, message, gateway_name=None, error_code=None, original_exception=None):
            super().__init__(message, gateway_name=gateway_name, original_exception=original_exception)
            self.error_code = error_code

    class PaymentConfigurationError(PaymentGatewayError):
        """Raised for configuration issues related to a payment gateway."""
        pass
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.exceptions`

### 4.4 Utilities (`utils/`)

#### 4.4.1 `odoo_modules/influence_gen_external_integrations/utils/__init__.py`
-   **Purpose:** Initializes the `utils` Python package.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import http_client_wrapper
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.utils`

#### 4.4.2 `odoo_modules/influence_gen_external_integrations/utils/http_client_wrapper.py`
-   **Purpose:** A wrapper for the `requests` library to standardize HTTP calls.
-   **Logic:**
    -   Uses `requests` library.
    -   Provides a static `request` method.
    -   Handles common headers (e.g., `Content-Type: application/json`, `Accept: application/json`).
    -   Implements configurable default timeout (e.g., 30 seconds), overridable per call.
    -   Logs request details (URL, method, masked headers/payload for sensitive data) and response status/summary.
    -   Raises `ApiCommunicationError` for network errors or HTTP status codes >= 400, unless handled by a more specific exception in the calling client.
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.utils`
-   **Class `HttpClientWrapper`:**
    python
    # -*- coding: utf-8 -*-
    import requests
    import logging
    from odoo.addons.influence_gen_external_integrations.exceptions.common_exceptions import ApiCommunicationError

    _logger = logging.getLogger(__name__)

    DEFAULT_TIMEOUT = 30  # seconds

    class HttpClientWrapper:

        @staticmethod
        def request(method: str, url: str, headers: dict = None,
                    json_data: dict = None, params: dict = None,
                    data: dict = None, # for form data
                    timeout: int = None, service_name: str = "ExternalService"):
            """
            Makes an HTTP request using the requests library.

            :param method: HTTP method (GET, POST, PUT, DELETE, etc.)
            :param url: URL for the request
            :param headers: Dictionary of headers
            :param json_data: Dictionary to be sent as JSON in the request body
            :param params: Dictionary of URL parameters
            :param data: Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request (for form-data)
            :param timeout: Request timeout in seconds
            :param service_name: Name of the service being called (for logging/error context)
            :return: requests.Response object
            :raises ApiCommunicationError: if the request fails or returns an error status code.
            """
            effective_timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
            effective_headers = headers if headers else {}
            
            # Common headers, can be extended
            if json_data and 'Content-Type' not in effective_headers:
                effective_headers['Content-Type'] = 'application/json'
            if 'Accept' not in effective_headers:
                 effective_headers['Accept'] = 'application/json'

            _logger.info(
                f"Sending HTTP {method} request to {service_name} at {url} "
                f"with params: {params}, headers: {effective_headers}"
            )
            # Consider masking sensitive data if logging json_data or data directly

            try:
                response = requests.request(
                    method=method.upper(),
                    url=url,
                    headers=effective_headers,
                    json=json_data,
                    params=params,
                    data=data,
                    timeout=effective_timeout
                )
                _logger.info(
                    f"Received HTTP {response.status_code} response from {service_name} for {url}. "
                    f"Content length: {len(response.content) if response.content else 0} bytes."
                )
                response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
                return response
            except requests.exceptions.HTTPError as e:
                _logger.error(
                    f"HTTP error from {service_name} for {url}: {e.response.status_code} - {e.response.text[:500]}"
                )
                raise ApiCommunicationError(
                    message=f"HTTP error {e.response.status_code} from {service_name}: {e.response.text[:200]}",
                    service_name=service_name,
                    status_code=e.response.status_code,
                    response_content=e.response.text,
                    original_exception=e
                )
            except requests.exceptions.Timeout as e:
                _logger.error(f"Timeout connecting to {service_name} at {url}: {e}")
                raise ApiCommunicationError(
                    message=f"Timeout connecting to {service_name}.",
                    service_name=service_name,
                    original_exception=e
                )
            except requests.exceptions.RequestException as e:
                _logger.error(f"Request exception for {service_name} at {url}: {e}")
                raise ApiCommunicationError(
                    message=f"Communication error with {service_name}: {str(e)}",
                    service_name=service_name,
                    original_exception=e
                )
    

### 4.5 Data Transfer Objects (DTOs) (`models/`)

#### 4.5.1 `odoo_modules/influence_gen_external_integrations/models/__init__.py`
-   **Purpose:** Initializes the `models` Python package for DTOs.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import kyc
    from . import bank_verification
    from . import accounting
    from . import payment_gateway # For future use
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.models`

#### 4.5.2 KYC DTOs (`models/kyc/`)

##### 4.5.2.1 `odoo_modules/influence_gen_external_integrations/models/kyc/__init__.py`
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import kyc_verification_request
    from . import kyc_verification_response
    

##### 4.5.2.2 `odoo_modules/influence_gen_external_integrations/models/kyc/kyc_verification_request.py`
-   **Purpose:** DTO for KYC identity verification request. Implements REQ-IOKYC-005, REQ-IL-011.
-   **Logic (using `dataclasses` for simplicity):**
    python
    # -*- coding: utf-8 -*-
    from dataclasses import dataclass, field
    from typing import Optional, Dict, Any

    @dataclass
    class KYCVerificationRequest:
        """
        DTO for submitting KYC identity verification data.
        Fields depend on the specific third-party KYC service API.
        """
        document_image_front_b64: str  # Base64 encoded image
        document_image_back_b64: Optional[str] = None # Base64 encoded image
        document_type: str  # e.g., 'PASSPORT', 'DRIVING_LICENSE'
        influencer_id: str # Internal influencer ID for callback matching
        # Add other fields as required by the specific KYC provider
        # e.g., first_name, last_name, dob, address if not extracted from document
        # callback_url: Optional[str] = None # If service supports async callbacks
        metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.models.kyc`

##### 4.5.2.3 `odoo_modules/influence_gen_external_integrations/models/kyc/kyc_verification_response.py`
-   **Purpose:** DTO for KYC identity verification response. Implements REQ-IOKYC-005, REQ-IL-011.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from dataclasses import dataclass, field
    from typing import Optional, Dict, Any

    @dataclass
    class KYCVerificationResponse:
        """
        DTO for the response from a KYC identity verification service.
        Fields depend on the specific third-party KYC service API.
        """
        transaction_id: str
        status: str  # e.g., 'VERIFIED', 'REJECTED', 'PENDING_REVIEW', 'ACTION_REQUIRED'
        reason: Optional[str] = None
        reason_code: Optional[str] = None
        extracted_data: Optional[Dict[str, Any]] = field(default_factory=dict) # e.g., PII
        # Add other fields like score, document_validity, face_match_score etc.
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.models.kyc`

#### 4.5.3 Bank Verification DTOs (`models/bank_verification/`)

##### 4.5.3.1 `odoo_modules/influence_gen_external_integrations/models/bank_verification/__init__.py`
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import bank_verification_request
    from . import bank_verification_response
    

##### 4.5.3.2 `odoo_modules/influence_gen_external_integrations/models/bank_verification/bank_verification_request.py`
-   **Purpose:** DTO for bank account verification request. Implements REQ-IOKYC-008, REQ-IPF-002.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from dataclasses import dataclass
    from typing import Optional

    @dataclass
    class BankVerificationRequest:
        """
        DTO for submitting bank account details for verification.
        Fields depend on the specific third-party service API.
        """
        account_holder_name: str
        account_number: str
        routing_number: Optional[str] = None # For ACH/US
        iban: Optional[str] = None # For SEPA/International
        swift_code: Optional[str] = None # For International
        bank_name: Optional[str] = None
        country_code: str # ISO 3166-1 alpha-2 country code
        influencer_id: str # Internal influencer ID for callback matching
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.models.bank_verification`

##### 4.5.3.3 `odoo_modules/influence_gen_external_integrations/models/bank_verification/bank_verification_response.py`
-   **Purpose:** DTO for bank account verification response. Implements REQ-IOKYC-008, REQ-IPF-002.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from dataclasses import dataclass
    from typing import Optional

    @dataclass
    class BankVerificationResponse:
        """
        DTO for the response from a bank account verification service.
        """
        transaction_id: str
        status: str  # e.g., 'VERIFIED', 'PENDING', 'FAILED', 'MICRODEPOSIT_SENT'
        reason: Optional[str] = None
        reason_code: Optional[str] = None
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.models.bank_verification`

#### 4.5.4 Accounting DTOs (`models/accounting/`)

##### 4.5.4.1 `odoo_modules/influence_gen_external_integrations/models/accounting/__init__.py`
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import vendor_bill_payload
    

##### 4.5.4.2 `odoo_modules/influence_gen_external_integrations/models/accounting/vendor_bill_payload.py`
-   **Purpose:** DTO for creating Odoo Vendor Bills. Implements REQ-IPF-006, REQ-2-014.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from dataclasses import dataclass
    from typing import Optional, List, Dict, Any
    from datetime import date

    @dataclass
    class VendorBillLinePayload:
        product_id: Optional[int] = None # Odoo product.product ID
        name: str # Description for the bill line
        quantity: float = 1.0
        price_unit: float = 0.0
        account_id: Optional[int] = None # Specific expense account ID
        tax_ids: Optional[List[int]] = None # List of Odoo account.tax IDs
        # Add other relevant analytic account fields if needed
        # analytic_account_id: Optional[int] = None 

    @dataclass
    class VendorBillPayload:
        """
        DTO for creating a Vendor Bill in Odoo Accounting.
        """
        influencer_partner_id: int  # Odoo res.partner ID for the influencer (vendor)
        currency_id: int  # Odoo res.currency ID
        journal_id: int # Odoo account.journal ID
        invoice_date: Optional[date] = None
        date: Optional[date] = None # Accounting date
        invoice_date_due: Optional[date] = None
        narration: Optional[str] = None # Notes for the bill
        campaign_id_internal: Optional[int] = None # Internal reference to InfluenceGen campaign ID (if stored on Odoo model)
        invoice_line_ids: List[VendorBillLinePayload] = None # List of bill lines
        # Reference to campaign or content submission that triggered this payment
        payment_reference: Optional[str] = None 
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.models.accounting`

#### 4.5.5 Payment Gateway DTOs (`models/payment_gateway/`) (Future Use)

##### 4.5.5.1 `odoo_modules/influence_gen_external_integrations/models/payment_gateway/__init__.py`
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    # Placeholder for future payment gateway DTOs
    # from . import payment_initiation_request (example)
    # from . import payment_status_response (example)
    
-   **Note:** DTOs here will be defined if/when REQ-IPF-012 is implemented.

### 4.6 Service Clients (`services/`)

#### 4.6.1 `odoo_modules/influence_gen_external_integrations/services/__init__.py`
-   **Purpose:** Initializes the `services` Python package.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    from . import base_api_client
    from . import kyc_service_client
    from . import bank_verification_service_client
    from . import odoo_accounting_service
    from . import payment_gateway_client_base # For future use
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.services`

#### 4.6.2 `odoo_modules/influence_gen_external_integrations/services/base_api_client.py`
-   **Purpose:** Abstract base class for external API clients.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    import logging
    from abc import ABC, abstractmethod
    from typing import Optional, Dict, Any
    import requests # For type hinting if needed, actual calls via wrapper

    from odoo import api, models # if this needs to be an Odoo AbstractModel for env access
    from odoo.addons.influence_gen_external_integrations.utils.http_client_wrapper import HttpClientWrapper
    from odoo.addons.influence_gen_external_integrations.config.integration_settings import IntegrationSettings
    from odoo.addons.influence_gen_external_integrations.exceptions.common_exceptions import ConfigurationError, ApiCommunicationError

    _logger = logging.getLogger(__name__)

    class BaseAPIClient(models.AbstractModel): # Inherit from models.AbstractModel to get self.env
        _name = 'influence_gen.base.api.client' # Needs a _name if it's an AbstractModel
        _description = 'Base API Client for External Services'

        # These would be set by subclasses or fetched dynamically
        SERVICE_NAME = "GenericService" 
        BASE_URL_PARAM = "influence_gen.generic_service.base_url"
        API_KEY_PARAM = "influence_gen.generic_service.api_key"


        def __init__(self, env): # Odoo services are typically not instantiated directly with __init__
                               # Instead, self.env is available if inheriting from models.AbstractModel
                               # For pure Python classes, env would be passed.
                               # Let's assume this is an Odoo AbstractModel.
            super().__init__(env) # Call super if it's an Odoo model
            # self.env is automatically available
            
        def _get_service_config(self):
            base_url = IntegrationSettings._get_param(self.env, self.BASE_URL_PARAM)
            api_key = IntegrationSettings._get_param(self.env, self.API_KEY_PARAM, default=None) # API key might be optional

            if not base_url:
                _logger.error(f"Base URL for {self.SERVICE_NAME} not configured (param: {self.BASE_URL_PARAM}).")
                raise ConfigurationError(
                    message=f"Base URL for {self.SERVICE_NAME} is not configured.",
                    setting_key=self.BASE_URL_PARAM
                )
            # API key check might be more nuanced (e.g. some endpoints don't need it)
            # For now, assume if API_KEY_PARAM is defined for the service, it's needed.
            if self.API_KEY_PARAM and not api_key and self.API_KEY_PARAM != "influence_gen.generic_service.api_key": # Avoid generic check
                 _logger.warning(f"API Key for {self.SERVICE_NAME} not configured (param: {self.API_KEY_PARAM}). Service might fail.")
                 # Depending on strictness, could raise ConfigurationError here too
            return base_url, api_key

        def _get_default_headers(self, api_key: Optional[str] = None) -> Dict[str, str]:
            """
            Provides default headers for API requests.
            Subclasses can override to add service-specific headers.
            """
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            # Example for Bearer token auth, adapt per service
            # if api_key:
            #     headers['Authorization'] = f'Bearer {api_key}' 
            return headers

        def _handle_api_response(self, response: requests.Response) -> Dict[str, Any]:
            """
            Handles the API response, checking for errors and parsing JSON.
            Subclasses might override for more specific error handling.
            """
            try:
                response.raise_for_status() # This is already done in HttpClientWrapper, but can be here for client-specific logic
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                _logger.error(f"Failed to decode JSON response from {self.SERVICE_NAME}: {e}. Response text: {response.text[:500]}")
                raise ApiCommunicationError(
                    message=f"Invalid JSON response from {self.SERVICE_NAME}.",
                    service_name=self.SERVICE_NAME,
                    response_content=response.text,
                    original_exception=e
                )
            # HTTPError is caught by HttpClientWrapper, re-raising ApiCommunicationError

        def _make_request(self, method: str, endpoint: str,
                          headers_override: Optional[Dict[str, str]] = None,
                          json_data: Optional[Dict[str, Any]] = None,
                          params: Optional[Dict[str, Any]] = None,
                          data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """
            Helper method to make a request to the service.
            """
            base_url, api_key = self._get_service_config()
            full_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            
            final_headers = self._get_default_headers(api_key)
            if headers_override:
                final_headers.update(headers_override)

            try:
                response_obj = HttpClientWrapper.request(
                    method=method,
                    url=full_url,
                    headers=final_headers,
                    json_data=json_data,
                    params=params,
                    data=data,
                    service_name=self.SERVICE_NAME
                )
                return self._handle_api_response(response_obj) # This will parse JSON if successful
            except ApiCommunicationError: # Already logged by HttpClientWrapper
                raise # Re-raise to be caught by the calling service method or business logic
            except Exception as e: # Catch any other unexpected errors
                _logger.exception(f"Unexpected error during API request to {self.SERVICE_NAME} at {endpoint}: {e}")
                raise ApiCommunicationError(
                    message=f"Unexpected error communicating with {self.SERVICE_NAME}.",
                    service_name=self.SERVICE_NAME,
                    original_exception=e
                )
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.services`

#### 4.6.3 `odoo_modules/influence_gen_external_integrations/services/kyc_service_client.py`
-   **Purpose:** Client for third-party KYC service. Implements REQ-IOKYC-005, REQ-IL-011.
-   **Logic:**
    -   Inherits from `BaseAPIClient`.
    -   Sets `SERVICE_NAME`, `BASE_URL_PARAM`, `API_KEY_PARAM` specific to KYC.
    -   `__init__(self, env)`: Calls super.
    -   `_get_default_headers(self, api_key)`: Overrides to add KYC-specific auth headers (e.g., `X-Api-Key: api_key` or `Authorization: Bearer api_key` depending on the KYC service).
    -   `verify_identity_document(self, request_data: KYCVerificationRequest) -> KYCVerificationResponse`:
        -   Constructs the API request payload from `request_data` DTO (e.g., may involve multipart/form-data if sending files directly, or JSON if sending base64 encoded images).
        -   Calls `self._make_request('POST', '/verify-identity', json_data=payload_dict)` (endpoint is example).
        -   Parses the JSON response into `KYCVerificationResponse` DTO.
        -   Handles specific `KYCServiceError` or `KYCVerificationFailedError` based on response codes/content.
    -   `get_verification_status(self, transaction_id: str) -> KYCVerificationResponse`:
        -   Calls `self._make_request('GET', f'/verification-status/{transaction_id}')`.
        -   Parses into `KYCVerificationResponse`.
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.services`
    python
    # -*- coding: utf-8 -*-
    import logging
    from typing import Dict, Any
    from odoo import models, _ # Odoo models.AbstractModel for self.env
    from odoo.exceptions import UserError

    from .base_api_client import BaseAPIClient
    from ..models.kyc.kyc_verification_request import KYCVerificationRequest
    from ..models.kyc.kyc_verification_response import KYCVerificationResponse
    from ..exceptions.kyc_exceptions import KYCServiceError, KYCVerificationFailedError, KYCDocumentInvalidError
    from ..exceptions.common_exceptions import ApiCommunicationError

    _logger = logging.getLogger(__name__)

    class KYCServiceClient(BaseAPIClient):
        _name = 'influence_gen.kyc.service.client' # Odoo service name
        _description = 'KYC Service Client'

        SERVICE_NAME = "KYCService" # For logging and error messages
        BASE_URL_PARAM = "influence_gen.kyc_service.base_url"
        API_KEY_PARAM = "influence_gen.kyc_service.api_key" # Key for ir.config_parameter

        # This method should be part of BaseAPIClient or overridden if auth differs
        def _get_default_headers(self, api_key: str) -> Dict[str, str]:
            headers = super()._get_default_headers(api_key)
            if api_key: # Example: many services use X-API-KEY or Authorization Bearer
                headers['X-API-KEY'] = api_key
            # else:
            #     raise ConfigurationError("API Key for KYC Service is not configured.", self.API_KEY_PARAM)
            return headers

        def verify_identity_document(self, request_data: KYCVerificationRequest) -> KYCVerificationResponse:
            """
            Submits identity document for verification. REQ-IOKYC-005, REQ-IL-011
            This example assumes JSON payload with base64 images.
            If the API expects multipart/form-data, _make_request and HttpClientWrapper
            would need to support 'files' parameter.
            """
            _logger.info(f"Attempting to verify identity for influencer: {request_data.influencer_id}")
            
            payload = {
                "document_front_b64": request_data.document_image_front_b64,
                "document_back_b64": request_data.document_image_back_b64,
                "document_type": request_data.document_type,
                "influencer_id": request_data.influencer_id,
                "metadata": request_data.metadata
                # "callback_url": request_data.callback_url # If applicable
            }
            # Remove None values from payload
            payload = {k: v for k, v in payload.items() if v is not None}

            try:
                # Endpoint is an example, replace with actual KYC service endpoint
                response_json = self._make_request(
                    method='POST',
                    endpoint='/verify-identity', # Example endpoint
                    json_data=payload
                )
                # Map JSON response to DTO
                return KYCVerificationResponse(
                    transaction_id=response_json.get('transaction_id'),
                    status=response_json.get('status'),
                    reason=response_json.get('reason'),
                    reason_code=response_json.get('reason_code'),
                    extracted_data=response_json.get('extracted_data')
                )
            except ApiCommunicationError as e:
                _logger.error(f"KYC API communication error for influencer {request_data.influencer_id}: {e}")
                # Re-raise or wrap in KYCServiceError
                raise KYCServiceError(f"Failed to communicate with KYC service: {e}", original_exception=e)
            except Exception as e: # Catch other unexpected errors
                _logger.exception(f"Unexpected error during KYC verification for influencer {request_data.influencer_id}: {e}")
                raise KYCServiceError(f"An unexpected error occurred during KYC verification: {str(e)}", original_exception=e)


        def get_verification_status(self, transaction_id: str) -> KYCVerificationResponse:
            """
            Retrieves the status of a previous KYC verification attempt. REQ-IOKYC-005
            """
            _logger.info(f"Fetching KYC verification status for transaction: {transaction_id}")
            try:
                # Endpoint is an example
                response_json = self._make_request(
                    method='GET',
                    endpoint=f'/verification-status/{transaction_id}' # Example endpoint
                )
                return KYCVerificationResponse(
                    transaction_id=response_json.get('transaction_id', transaction_id), # Fallback to passed ID
                    status=response_json.get('status'),
                    reason=response_json.get('reason'),
                    reason_code=response_json.get('reason_code'),
                    extracted_data=response_json.get('extracted_data')
                )
            except ApiCommunicationError as e:
                _logger.error(f"KYC API communication error fetching status for {transaction_id}: {e}")
                raise KYCServiceError(f"Failed to fetch KYC status: {e}", original_exception=e)
            except Exception as e:
                _logger.exception(f"Unexpected error fetching KYC status for {transaction_id}: {e}")
                raise KYCServiceError(f"An unexpected error occurred fetching KYC status: {str(e)}", original_exception=e)

    

#### 4.6.4 `odoo_modules/influence_gen_external_integrations/services/bank_verification_service_client.py`
-   **Purpose:** Client for third-party bank account verification. Implements REQ-IOKYC-008, REQ-IPF-002.
-   **Logic:**
    -   Similar structure to `KYCServiceClient`.
    -   Inherits from `BaseAPIClient`.
    -   Sets `SERVICE_NAME`, `BASE_URL_PARAM`, `API_KEY_PARAM` specific to bank verification.
    -   `_get_default_headers` overridden if needed for bank service auth.
    -   `verify_bank_account(self, request_data: BankVerificationRequest) -> BankVerificationResponse`:
        -   Constructs payload from `BankVerificationRequest`.
        -   Calls `self._make_request` to the bank verification API endpoint.
        -   Parses response into `BankVerificationResponse`.
        -   Handles specific `BankVerificationServiceError`, `BankAccountInvalidError`.
    -   `get_verification_status(self, transaction_id: str) -> BankVerificationResponse`:
        -   Retrieves status for a given transaction.
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.services`
    python
    # -*- coding: utf-8 -*-
    import logging
    from typing import Dict, Any
    from odoo import models, _

    from .base_api_client import BaseAPIClient
    from ..models.bank_verification.bank_verification_request import BankVerificationRequest
    from ..models.bank_verification.bank_verification_response import BankVerificationResponse
    from ..exceptions.bank_verification_exceptions import BankVerificationServiceError, BankAccountInvalidError, BankVerificationFailedError
    from ..exceptions.common_exceptions import ApiCommunicationError

    _logger = logging.getLogger(__name__)

    class BankVerificationServiceClient(BaseAPIClient):
        _name = 'influence_gen.bank.verification.service.client'
        _description = 'Bank Account Verification Service Client'

        SERVICE_NAME = "BankVerificationService"
        BASE_URL_PARAM = "influence_gen.bank_verification.base_url"
        API_KEY_PARAM = "influence_gen.bank_verification.api_key"

        def _get_default_headers(self, api_key: str) -> Dict[str, str]:
            headers = super()._get_default_headers(api_key)
            if api_key:
                headers['X-API-KEY'] = api_key # Example, adapt to actual service
            return headers

        def verify_bank_account(self, request_data: BankVerificationRequest) -> BankVerificationResponse:
            """
            Submits bank account details for verification. REQ-IOKYC-008, REQ-IPF-002
            """
            _logger.info(f"Attempting bank account verification for influencer: {request_data.influencer_id}")
            
            payload = {
                "account_holder_name": request_data.account_holder_name,
                "account_number": request_data.account_number,
                "routing_number": request_data.routing_number,
                "iban": request_data.iban,
                "swift_code": request_data.swift_code,
                "bank_name": request_data.bank_name,
                "country_code": request_data.country_code,
                "influencer_id": request_data.influencer_id
            }
            payload = {k: v for k, v in payload.items() if v is not None}

            try:
                # Endpoint is an example
                response_json = self._make_request(
                    method='POST',
                    endpoint='/verify-bank-account', # Example endpoint
                    json_data=payload
                )
                return BankVerificationResponse(
                    transaction_id=response_json.get('transaction_id'),
                    status=response_json.get('status'),
                    reason=response_json.get('reason'),
                    reason_code=response_json.get('reason_code')
                )
            except ApiCommunicationError as e:
                _logger.error(f"Bank verification API communication error for influencer {request_data.influencer_id}: {e}")
                raise BankVerificationServiceError(f"Failed to communicate with bank verification service: {e}", original_exception=e)
            except Exception as e:
                _logger.exception(f"Unexpected error during bank verification for influencer {request_data.influencer_id}: {e}")
                raise BankVerificationServiceError(f"An unexpected error occurred during bank verification: {str(e)}", original_exception=e)

        def get_verification_status(self, transaction_id: str) -> BankVerificationResponse:
            """
            Retrieves the status of a previous bank account verification. REQ-IOKYC-008
            """
            _logger.info(f"Fetching bank verification status for transaction: {transaction_id}")
            try:
                # Endpoint is an example
                response_json = self._make_request(
                    method='GET',
                    endpoint=f'/bank-verification-status/{transaction_id}' # Example endpoint
                )
                return BankVerificationResponse(
                    transaction_id=response_json.get('transaction_id', transaction_id),
                    status=response_json.get('status'),
                    reason=response_json.get('reason'),
                    reason_code=response_json.get('reason_code')
                )
            except ApiCommunicationError as e:
                _logger.error(f"Bank verification API communication error fetching status for {transaction_id}: {e}")
                raise BankVerificationServiceError(f"Failed to fetch bank verification status: {e}", original_exception=e)
            except Exception as e:
                _logger.exception(f"Unexpected error fetching bank verification status for {transaction_id}: {e}")
                raise BankVerificationServiceError(f"An unexpected error occurred fetching bank verification status: {str(e)}", original_exception=e)
    

#### 4.6.5 `odoo_modules/influence_gen_external_integrations/services/odoo_accounting_service.py`
-   **Purpose:** Integrates with Odoo's Accounting module for payments. Implements REQ-IPF-006, REQ-2-014.
-   **Logic:**
    -   This is an Odoo `models.AbstractModel` service.
    -   `create_vendor_bill_for_influencer_payment(self, payload: VendorBillPayload) -> odoo.models.Model('account.move')`:
        -   Uses `self.env['account.move']` to create a new record.
        -   Maps fields from `VendorBillPayload` DTO to `account.move` fields:
            -   `partner_id`: `payload.influencer_partner_id`
            -   `move_type`: `'in_invoice'` (Vendor Bill)
            -   `currency_id`: `payload.currency_id`
            -   `journal_id`: `payload.journal_id` (or fetch default based on company/type)
            -   `invoice_date`: `payload.invoice_date` or `fields.Date.today()`
            -   `date`: `payload.date` or `fields.Date.today()`
            -   `invoice_date_due`: `payload.invoice_date_due`
            -   `narration`: `payload.narration`
            -   `ref`: `payload.payment_reference`
            -   `invoice_line_ids`: Create `(0, 0, {values})` tuples for each line in `payload.invoice_line_ids`.
                -   `name`: `line.name`
                -   `product_id`: `line.product_id` (optional, if service products are used)
                -   `quantity`: `line.quantity`
                -   `price_unit`: `line.price_unit`
                -   `account_id`: `line.account_id` (expense account for the line)
                -   `tax_ids`: `[(6, 0, line.tax_ids)]` if provided
        -   Handles potential Odoo ORM exceptions.
        -   Optionally calls `action_post()` on the created bill if auto-posting is desired and within policy, or leaves it in draft for manual review.
        -   Returns the created `account.move` record.
    -   `create_payment_batch_vendor_bills(self, batch_payloads: List[VendorBillPayload]) -> List[odoo.models.Model('account.move')]`:
        -   Iterates through `batch_payloads`, calling `create_vendor_bill_for_influencer_payment` for each.
        -   Collects and returns a list of created `account.move` records.
        -   Manages transactions appropriately (e.g., if one bill fails, should others be rolled back or processed individually?).
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.services`
    python
    # -*- coding: utf-8 -*-
    import logging
    from typing import List
    from odoo import api, fields, models, _
    from odoo.exceptions import UserError, ValidationError
    from ..models.accounting.vendor_bill_payload import VendorBillPayload, VendorBillLinePayload

    _logger = logging.getLogger(__name__)

    class OdooAccountingService(models.AbstractModel):
        _name = 'influence_gen.odoo.accounting.service'
        _description = 'Odoo Accounting Integration Service'

        def _prepare_vendor_bill_line_vals(self, line_payload: VendorBillLinePayload) -> dict:
            """Prepares values for a single vendor bill line."""
            if not line_payload.account_id and not line_payload.product_id:
                raise ValidationError(_("Each bill line must have either a product or an expense account specified."))
            
            line_vals = {
                'name': line_payload.name,
                'quantity': line_payload.quantity,
                'price_unit': line_payload.price_unit,
            }
            if line_payload.product_id:
                line_vals['product_id'] = line_payload.product_id
            if line_payload.account_id: # Can override product's account
                line_vals['account_id'] = line_payload.account_id
            if line_payload.tax_ids:
                line_vals['tax_ids'] = [(6, 0, line_payload.tax_ids)]
            # Add analytic accounting if needed
            # if line_payload.analytic_account_id:
            #     line_vals['analytic_account_id'] = line_payload.analytic_account_id
            return line_vals

        def create_vendor_bill_for_influencer_payment(self, payload: VendorBillPayload) -> models.Model: # type: ignore
            """
            Creates a single Vendor Bill in Odoo for an influencer payment.
            REQ-IPF-006, REQ-2-014
            """
            _logger.info(f"Creating vendor bill for influencer partner ID: {payload.influencer_partner_id}")

            if not payload.invoice_line_ids:
                raise ValidationError(_("Cannot create a vendor bill without lines."))

            bill_lines_vals = []
            for line_payload in payload.invoice_line_ids:
                bill_lines_vals.append((0, 0, self._prepare_vendor_bill_line_vals(line_payload)))

            bill_vals = {
                'partner_id': payload.influencer_partner_id,
                'move_type': 'in_invoice',  # Vendor Bill
                'currency_id': payload.currency_id,
                'journal_id': payload.journal_id,
                'invoice_date': payload.invoice_date or fields.Date.context_today(self),
                'date': payload.date or fields.Date.context_today(self), # Accounting Date
                'invoice_date_due': payload.invoice_date_due,
                'narration': payload.narration,
                'ref': payload.payment_reference, # Payment Reference
                'invoice_line_ids': bill_lines_vals,
                # Potentially link to InfluenceGen campaign if custom field exists on account.move
                # 'x_studio_influence_gen_campaign_id': payload.campaign_id_internal, 
            }
            
            try:
                vendor_bill = self.env['account.move'].create(bill_vals)
                _logger.info(f"Vendor bill created with ID: {vendor_bill.id} for partner ID: {payload.influencer_partner_id}")
                
                # Optionally post the bill if business logic dictates direct posting
                # if auto_post_bill:
                #     vendor_bill.action_post()
                #     _logger.info(f"Vendor bill ID: {vendor_bill.id} posted.")

                return vendor_bill
            except (UserError, ValidationError) as e:
                _logger.error(f"Validation error creating vendor bill for partner {payload.influencer_partner_id}: {e}")
                raise
            except Exception as e:
                _logger.exception(f"Unexpected error creating vendor bill for partner {payload.influencer_partner_id}: {e}")
                # Consider wrapping in a custom exception
                raise UserError(_("An unexpected error occurred while creating the vendor bill. Please contact support."))


        def create_payment_batch_vendor_bills(self, batch_payloads: List[VendorBillPayload]) -> List[models.Model]: # type: ignore
            """
            Creates multiple Vendor Bills for a batch of influencer payments.
            REQ-IPF-006, REQ-2-014
            """
            _logger.info(f"Creating batch of {len(batch_payloads)} vendor bills.")
            created_bills = []
            errors = []

            for payload in batch_payloads:
                try:
                    bill = self.create_vendor_bill_for_influencer_payment(payload)
                    created_bills.append(bill)
                except Exception as e: # Catch broadly to report all errors
                    _logger.error(f"Failed to create vendor bill for partner ID {payload.influencer_partner_id} in batch: {e}")
                    errors.append({
                        "influencer_partner_id": payload.influencer_partner_id,
                        "error": str(e)
                    })
            
            if errors:
                # Partial success: some bills created, some failed.
                # How to handle this? Raise an error with details, or return successes and failures separately?
                # For now, raising an error with details.
                error_message = _("Batch vendor bill creation partially failed. Errors:\n")
                for err_detail in errors:
                    error_message += f"- Partner ID {err_detail['influencer_partner_id']}: {err_detail['error']}\n"
                # This might be too disruptive. Consider returning a structured response instead.
                # For simplicity in this SDS, we'll raise. In reality, a more nuanced approach is needed.
                # raise UserError(error_message) 
                _logger.warning(error_message) # Log warning instead of raising UserError for partial success

            _logger.info(f"Successfully created {len(created_bills)} vendor bills from batch.")
            return created_bills # Return successfully created bills even if some failed
    

#### 4.6.6 `odoo_modules/influence_gen_external_integrations/services/payment_gateway_client_base.py`
-   **Purpose:** Abstract base for future payment gateway clients. Implements REQ-IPF-012.
-   **Logic:**
    python
    # -*- coding: utf-8 -*-
    import logging
    from abc import ABC, abstractmethod
    from typing import Any, Dict, Optional
    from odoo import models # For self.env if needed by concrete implementations

    _logger = logging.getLogger(__name__)

    # Placeholder DTOs, these would be defined in models.payment_gateway
    class PaymentInitiationRequestDTO: # Example
        amount: float
        currency: str
        recipient_details: Dict[str, Any]
        reference: str
        # ... other common fields

    class PaymentStatusResponseDTO: # Example
        transaction_id: str
        status: str # e.g., 'succeeded', 'pending', 'failed'
        error_message: Optional[str]
        # ... other common fields

    class PaymentGatewayClientBase(models.AbstractModel): # Or pure Python ABC
        _name = 'influence_gen.payment.gateway.client.base'
        _description = 'Abstract Base Class for Payment Gateway Clients'
        
        # To be set by concrete implementations
        GATEWAY_NAME = "AbstractGateway"

        def __init__(self, env): # Or pass env if pure Python
            super().__init__(env) # if models.AbstractModel

        @abstractmethod
        def initiate_payment(self, payment_request: PaymentInitiationRequestDTO) -> PaymentStatusResponseDTO:
            """
            Initiates a payment through the payment gateway.
            REQ-IPF-012
            :param payment_request: DTO containing payment details.
            :return: DTO containing the initial status of the payment attempt.
            :raises PaymentGatewayError: if initiation fails.
            """
            pass

        @abstractmethod
        def get_payment_status(self, transaction_id: str) -> PaymentStatusResponseDTO:
            """
            Retrieves the status of a previously initiated payment.
            REQ-IPF-012
            :param transaction_id: The gateway's transaction identifier.
            :return: DTO containing the payment status.
            :raises PaymentGatewayError: if status retrieval fails.
            """
            pass
        
        # Concrete implementations might inherit from BaseAPIClient as well if RESTful
    
-   **Namespace:** `odoo.addons.influence_gen_external_integrations.services`

## 5. Security Considerations
-   **Credential Management (REQ-IL-008):** API keys and sensitive credentials for external services will be stored securely using Odoo's system parameters (`ir.config_parameter`) or a more secure vault if Odoo 18 provides one suitable for module-specific keys. They will **never** be hardcoded. Access to these parameters will be restricted.
-   **HTTPS Enforcement:** All communications with external services via `HttpClientWrapper` will enforce HTTPS.
-   **Data Minimization:** Only necessary data will be sent to external services. PII sent to KYC/Bank verification services will be handled according to the service's security protocols and our privacy policy.
-   **Error Handling:** Specific exceptions will be used to prevent leaking sensitive error details from external services to end-users, while providing sufficient information for internal logging and troubleshooting.
-   **Odoo Accounting Integration (REQ-IPF-006):** This integration will leverage Odoo's existing security model. Creation of vendor bills will respect Odoo's access rights and accounting workflows (e.g., bills may be created in draft state for further review and posting by authorized accounting personnel).

## 6. Logging
-   The `HttpClientWrapper` will log basic information about outgoing requests (URL, method) and responses (status code). Sensitive data in payloads/headers will be masked or omitted from logs.
-   Each service client (KYC, Bank Verification, Odoo Accounting) will log key actions, successes, and failures, including relevant identifiers (e.g., influencer ID, transaction ID) for traceability.
-   Errors and exceptions, especially `ApiCommunicationError` and service-specific errors, will be logged with sufficient detail to aid troubleshooting.
-   Log levels will be used appropriately (INFO for standard operations, WARNING for recoverable issues or missing non-critical configs, ERROR for failed operations, EXCEPTION for unexpected errors).

## 7. Future Considerations (REQ-IPF-012)
-   The `PaymentGatewayClientBase` and associated DTOs/exceptions provide an architectural placeholder for future integration with direct payment gateways. When a specific gateway is chosen, a concrete client inheriting from `PaymentGatewayClientBase` (and potentially `BaseAPIClient`) will be implemented.
-   This will involve:
    -   Defining specific DTOs for the chosen gateway's request/response structures.
    -   Implementing authentication methods specific to that gateway.
    -   Mapping InfluenceGen payment data to the gateway's API.
    -   Handling gateway-specific error codes and responses.
    -   Ensuring PCI DSS compliance if cardholder data is ever handled directly by Odoo (though the goal is usually to tokenize or use gateway-hosted fields to avoid this).

This detailed design should provide a solid foundation for the development of the `InfluenceGen.Odoo.External.Integrations.Endpoints` module.