# Software Design Specification: InfluenceGen.Odoo.Integration.Adapters (REPO-IGIA-004)

## 1. Introduction

This document outlines the software design specification for the `InfluenceGen.Odoo.Integration.Adapters` Odoo module. This module is responsible for managing the technical aspects of communication between the InfluenceGen Odoo platform and external systems, primarily N8N for AI image generation, and potentially other third-party services for KYC and payments. It abstracts the complexities of external communication, providing a clear interface for the business logic layer.

### 1.1. Purpose

The primary purposes of this module are:
*   To implement client logic for securely invoking external services (e.g., N8N webhooks).
*   To provide secure Odoo HTTP controller endpoints for receiving callbacks from external services (e.g., N8N).
*   To encapsulate adapter logic for various third-party integrations (KYC, Payment Gateways).
*   To ensure that integration logic is decoupled from core business services.

### 1.2. Scope

This SDS covers the design of:
*   Odoo controllers for handling incoming API calls (callbacks).
*   Adapter classes for initiating outgoing API calls.
*   Data Transfer Objects (DTOs) for structured data exchange with external systems.
*   Internal utility functions for authentication and error handling specific to integrations.
*   OpenAPI specification for the N8N callback endpoint.

### 1.3. Definitions, Acronyms, and Abbreviations

*   **AI:** Artificial Intelligence
*   **API:** Application Programming Interface
*   **CSRF:** Cross-Site Request Forgery
*   **DTO:** Data Transfer Object
*   **ETL:** Extract, Transform, Load
*   **HTTP:** Hypertext Transfer Protocol
*   **JSON:** JavaScript Object Notation
*   **KYC:** Know Your Customer
*   **N8N:** A free and open node-based Workflow Automation Tool.
*   **ORM:** Object-Relational Mapper
*   **OWL:** Odoo Web Library
*   **PII:** Personally Identifiable Information
*   **REST:** Representational State Transfer
*   **SDS:** Software Design Specification
*   **UI:** User Interface
*   **UX:** User Experience
*   **WCAG:** Web Content Accessibility Guidelines
*   **YAML:** YAML Ain't Markup Language

## 2. System Overview

The `InfluenceGen.Odoo.Integration.Adapters` module sits within the "InfluenceGen Odoo Infrastructure & Integration Services Layer" of the overall InfluenceGen platform architecture. It acts as a bridge between Odoo's business logic layer (`InfluenceGen.Odoo.Business.Services` - REPO-IGBS-003) and external systems.

Key interactions include:
*   **Outbound:** Odoo (via an adapter in this module) calls an N8N webhook to initiate AI image generation.
*   **Inbound:** N8N calls an Odoo HTTP controller (in this module) to deliver AI image generation results.
*   **Outbound (Future):** Adapters in this module may call external KYC or payment gateway APIs.

This module will heavily rely on Odoo 18 framework features, Python's `requests` library for HTTP communication, and RESTful API principles. Secure credential management and logging are critical aspects.

## 3. Design Considerations

### 3.1. Assumptions

*   Odoo 18 environment is correctly set up.
*   N8N instance is deployed and accessible from the Odoo server.
*   External third-party services (AI, KYC, Payment) provide stable REST APIs.
*   Secure mechanisms for storing and retrieving API keys and sensitive configurations are available within Odoo (e.g., `ir.config_parameter` or a dedicated secrets management utility from REPO-IGSCU-007).
*   The business logic layer (REPO-IGBS-003) defines clear service interfaces for this module to interact with (e.g., for dispatching N8N callback data).

### 3.2. Constraints

*   Must be developed for Odoo Version 18.
*   Primary language is Python 3.11.
*   Must adhere to Odoo development best practices and organizational coding standards.
*   All external communication must use HTTPS/TLS 1.2+ (REQ-IL-007).
*   Sensitive credentials must not be hardcoded (REQ-IL-008).
*   Rate limiting considerations for both inbound and outbound API calls (REQ-IL-015).

### 3.3. Architectural Approach

This module follows a layered approach within the Odoo ecosystem.
*   **Controllers:** Handle inbound HTTP requests (callbacks).
*   **Adapters:** Encapsulate logic for outbound HTTP requests to specific external services. This promotes the Adapter Pattern, allowing for easier changes or additions of external service integrations.
*   **DTOs:** Ensure structured and type-safe data exchange.
*   **Utils:** Provide focused, reusable helper functions for tasks like authentication and error handling specific to integrations.

## 4. Module Structure and Detailed Design

The module `influence_gen_integration_adapters` will have the following structure and components:

### 4.1. `__init__.py`
*   **Purpose:** Initializes the Python package for Odoo, importing submodules.
*   **Logic:**
    python
    # odoo_modules/influence_gen_integration_adapters/__init__.py
    from . import controllers
    from . import adapters
    from . import dtos
    from . import utils
    
*   **Requirements:** Module Initialization.

### 4.2. `__manifest__.py`
*   **Purpose:** Odoo module manifest file.
*   **Logic:**
    python
    # odoo_modules/influence_gen_integration_adapters/__manifest__.py
    {
        'name': 'InfluenceGen Integration Adapters',
        'version': '18.0.1.0.0',
        'summary': 'Manages technical communication between Odoo and external systems like N8N and third-party APIs for InfluenceGen.',
        'author': 'SSS-AI',
        'website': 'https://www.example.com', # Replace with actual
        'category': 'InfluenceGen/Integrations',
        'license': 'LGPL-3', # Or appropriate license
        'depends': [
            'base',
            'web',
            'mail', # For logging/notifications if needed directly, or used by business services
            # 'influence_gen_shared_utilities', # Dependency on REPO-IGSCU-007
            # 'influence_gen_business_services', # If directly invoking service interfaces, or for type hints
        ],
        'data': [
            # No XML views typically in this backend-focused module, unless for config
        ],
        'installable': True,
        'application': False,
        'auto_install': False,
    }
    
*   **Note:** The `depends` list should accurately reflect dependencies on other custom modules like `influence_gen_shared_utilities` (REPO-IGSCU-007) once its actual module name is known. Business services from `influence_gen_business_services` (REPO-IGBS-003) will likely be accessed via `request.env` or `self.env`, so a direct manifest dependency might not be strictly required unless interfaces/DTOs are imported directly.
*   **Requirements:** Module Definition, Dependency Management.

### 4.3. `controllers/`

#### 4.3.1. `controllers/__init__.py`
*   **Purpose:** Initializes the Python package for Odoo controllers.
*   **Logic:**
    python
    # odoo_modules/influence_gen_integration_adapters/controllers/__init__.py
    from . import n8n_callback_controller
    
*   **Requirements:** Controller Aggregation.

#### 4.3.2. `controllers/n8n_callback_controller.py`
*   **Class:** `N8NCallbackController(http.Controller)`
*   **Purpose:** Handles incoming HTTP POST callbacks from N8N, primarily for AI image generation results.
*   **Requirements:** REQ-IL-003, REQ-IL-004, REQ-IL-010, REQ-IL-016, REQ-AIGS-001.
*   **Logging:** Standard Python `logging` module, `_logger = logging.getLogger(__name__)`.
*   **Methods:**
    *   `handle_ai_image_result(self, **kwargs)`:
        *   **Route:** `@http.route('/influence_gen/n8n/ai_callback', type='json', auth='public', methods=['POST'], csrf=False, cors='*')`
        *   **Parameters:** `kwargs` (Odoo automatically populates this with JSON payload if `type='json'`).
        *   **Return Type:** `werkzeug.wrappers.Response` (implicitly via Odoo's JSONRPC handling or explicitly constructed for custom error responses).
        *   **Logic:**
            1.  Log reception of callback (REQ-IL-013).
            2.  **Authentication (REQ-IL-004, REQ-IL-016):**
                *   Call `request.env['influence_gen.api.auth'].verify_n8n_request(http.request)` (assumes a utility method, see `utils/api_auth.py`).
                *   If authentication fails, log an error and return an HTTP 401 Unauthorized response.
            3.  **Rate Limiting (REQ-IL-015):** Acknowledge that Odoo's infrastructure or a WAF should handle broad rate limiting. If application-level rate limiting specific to this endpoint is needed, it would be implemented here or via a decorator. For now, assume platform-level.
            4.  **Payload Parsing & Validation (REQ-IL-004):**
                *   The `kwargs` will contain the parsed JSON.
                *   Instantiate a DTO, e.g., `N8nAiGenerationResultDto` from `dtos.n8n_dtos`, with the received data.
                *   Perform basic structural validation (e.g., presence of `request_id`, `status`).
                *   If validation fails, log error and return HTTP 400 Bad Request.
            5.  **Data Dispatching (REQ-IL-003, REQ-IL-010, REQ-AIGS-001):**
                *   Obtain the AI Image Service from the business layer: `ai_image_service = request.env['influence_gen.ai.image.service']` (assuming service name from REPO-IGBS-003).
                *   Call a method on the service: `ai_image_service.process_n8n_ai_result(dto_instance)`.
            6.  **Error Handling:**
                *   Wrap the dispatch call in a `try-except` block.
                *   Catch specific exceptions from the business service or DTO instantiation.
                *   Log errors and return appropriate HTTP 500 Internal Server Error or other relevant error codes.
            7.  **Response:**
                *   If successful, return an HTTP 200 OK response, typically an empty JSON object `{}` or `{"status": "success"}`.
*   **Implemented Features:** N8N Callback Handling, Request Validation, Data Dispatching, Error Handling for Callbacks, API Security.

### 4.4. `adapters/`

#### 4.4.1. `adapters/__init__.py`
*   **Purpose:** Initializes the Python package for integration adapters.
*   **Logic:**
    python
    # odoo_modules/influence_gen_integration_adapters/adapters/__init__.py
    from . import n8n_ai_adapter
    from . import kyc_service_adapter_base
    from . import example_kyc_adapter # If enabled
    from . import payment_gateway_adapter_base
    from . import example_payment_adapter # If enabled
    
*   **Requirements:** Adapter Aggregation.

#### 4.4.2. `adapters/n8n_ai_adapter.py`
*   **Class:** `N8nAiAdapter(models.AbstractModel)` (or a plain Python class instantiated as needed by services)
    *   **Model Name (if AbstractModel):** `_name = 'influence_gen.n8n.ai.adapter'`
*   **Purpose:** Client to securely call the N8N webhook for initiating AI image generation.
*   **Requirements:** REQ-IL-002, REQ-AIGS-001, REQ-IL-009 (Error Handling/Retry), REQ-IL-013 (Logging), REQ-IL-015 (Handle N8N Rate Limit), REQ-IL-008, REQ-PAC-017 (Config).
*   **Logging:** Standard Python `logging` module, `_logger = logging.getLogger(__name__)`.
*   **Attributes (if plain class, passed in `__init__` or fetched from env):**
    *   `n8n_webhook_url: str`
    *   `n8n_auth_token: str`
    *   `env` (Odoo environment, if it's not an AbstractModel)
*   **Methods:**
    *   `__init__(self, env)` (if plain class, or `api.model_create_multi` if AbstractModel):
        *   **Logic (REQ-IL-008, REQ-PAC-017):**
            *   Fetch `n8n_webhook_url` from Odoo system parameters: `self.env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_ai_webhook_url')`.
            *   Fetch `n8n_auth_token` securely: `self.env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_ai_auth_token')`.
            *   Store these in instance variables.
            *   Log if configuration is missing.
    *   `initiate_ai_image_generation(self, generation_request_dto: N8nAiGenerationRequestDto) -> dict`:
        *   **Parameters:** `generation_request_dto` (instance of `N8nAiGenerationRequestDto` from `dtos.n8n_dtos`).
        *   **Return Type:** `dict` (e.g., `{"success": True/False, "message": "...", "n8n_response_status": 200/None}`).
        *   **Logic (REQ-IL-002, REQ-AIGS-001):**
            1.  Check if `n8n_webhook_url` and `n8n_auth_token` are configured. If not, log error and return failure.
            2.  Construct JSON payload from `generation_request_dto`. Use `dataclasses.asdict(generation_request_dto)` if DTOs are dataclasses.
            3.  Prepare headers: `{'Content-Type': 'application/json', 'Authorization': f'Bearer {self.n8n_auth_token}'}`.
            4.  Log initiation attempt with partial data (avoid logging full prompt if sensitive) (REQ-IL-013).
            5.  **HTTP Call & Retry Logic (REQ-IL-009):**
                *   Use `requests.post(url, json=payload, headers=headers, timeout=...)`.
                *   Implement retry mechanism (e.g., using `tenacity` library or a custom loop) for transient errors (e.g., network issues, 5xx errors from N8N).
                *   Example: Max 3 retries with exponential backoff.
            6.  **Error Handling (REQ-IL-009, REQ-IL-015):**
                *   `try-except requests.exceptions.Timeout, requests.exceptions.ConnectionError`: Handle network issues.
                *   `try-except requests.exceptions.RequestException`: General request errors.
                *   Check `response.status_code`:
                    *   `2xx`: Success.
                    *   `429 Too Many Requests`: Handle N8N rate limiting (REQ-IL-015). Log and potentially raise a specific exception or return a specific failure status.
                    *   Other `4xx`, `5xx`: Log error, details from response.
                *   Use `utils.integration_error_handler.handle_external_api_error` if defined.
            7.  Log outcome (success/failure, N8N status code) (REQ-IL-013).
            8.  Return a dictionary indicating success or failure, and relevant information.
*   **Implemented Features:** N8N Webhook Invocation, AI Request Construction, External API Authentication, Error Handling and Retries for N8N calls.

#### 4.4.3. `adapters/kyc_service_adapter_base.py`
*   **Class:** `KycServiceAdapterBase(abc.ABC, models.AbstractModel)` (or plain Python ABC)
    *   **Model Name (if AbstractModel):** `_name = 'influence_gen.kyc.service.adapter.base'`
*   **Purpose:** Abstract base class/interface for KYC service adapters.
*   **Requirements:** REQ-IL-011, REQ-IOKYC-005.
*   **Methods:**
    *   `@abc.abstractmethod`
        `verify_identity(self, kyc_request_dto: KycVerificationRequestDto) -> KycVerificationResultDto`:
        *   **Parameters:** `kyc_request_dto` (instance of `KycVerificationRequestDto` from `dtos.kyc_dtos`).
        *   **Return Type:** `KycVerificationResultDto` (instance from `dtos.kyc_dtos`).
        *   **Logic:** This is an abstract method. Concrete implementations will handle the actual API call.
*   **Implemented Features:** KYC Service Abstraction.

#### 4.4.4. `adapters/example_kyc_adapter.py`
*   **Note:** This is an example. Actual implementation will depend on the chosen KYC provider.
*   **Class:** `ExampleKycAdapter(models.AbstractModel)` (or plain Python class inheriting `KycServiceAdapterBase`)
    *   **Model Name (if AbstractModel):** `_name = 'influence_gen.example.kyc.adapter'`
    *   **Inherits:** `KycServiceAdapterBase` (or `self.env['influence_gen.kyc.service.adapter.base']` if using Odoo models).
*   **Purpose:** Concrete adapter for a hypothetical "ExampleKYCProvider".
*   **Requirements:** REQ-IL-011, REQ-IOKYC-005, REQ-IL-009, REQ-IL-013, REQ-IL-008, REQ-PAC-017.
*   **Attributes:**
    *   `api_endpoint: str`
    *   `api_key: str`
*   **Methods:**
    *   `__init__(self, env)`:
        *   Fetch `api_endpoint` and `api_key` for "ExampleKYCProvider" from Odoo config.
    *   `verify_identity(self, kyc_request_dto: KycVerificationRequestDto) -> KycVerificationResultDto`:
        *   Construct API request payload from `kyc_request_dto`.
        *   Make HTTP call to `self.api_endpoint` using `requests` and `self.api_key` for auth.
        *   Handle response, parse into `KycVerificationResultDto`.
        *   Implement error handling, retries (REQ-IL-009) and logging (REQ-IL-013).
*   **Implemented Features:** Specific KYC Service Integration, API Call Logic, Error Handling for KYC Service.

#### 4.4.5. `adapters/payment_gateway_adapter_base.py`
*   **Class:** `PaymentGatewayAdapterBase(abc.ABC, models.AbstractModel)` (or plain Python ABC)
    *   **Model Name (if AbstractModel):** `_name = 'influence_gen.payment.gateway.adapter.base'`
*   **Purpose:** Abstract base class/interface for payment gateway and bank account verification adapters.
*   **Requirements:** REQ-IL-012, REQ-IOKYC-008.
*   **Methods:**
    *   `@abc.abstractmethod`
        `initiate_payment(self, payment_request_dto: PaymentInitiationRequestDto) -> PaymentResultDto`:
        *   **Parameters:** `payment_request_dto` (from `dtos.payment_dtos`).
        *   **Return Type:** `PaymentResultDto` (from `dtos.payment_dtos`).
    *   `@abc.abstractmethod`
        `verify_bank_account(self, bank_details_dto: BankAccountVerificationRequestDto) -> BankAccountVerificationResultDto`:
        *   **Parameters:** `bank_details_dto` (from `dtos.payment_dtos`).
        *   **Return Type:** `BankAccountVerificationResultDto` (from `dtos.payment_dtos`).
*   **Implemented Features:** Payment Gateway Abstraction, Bank Account Verification Abstraction.

#### 4.4.6. `adapters/example_payment_adapter.py`
*   **Note:** Example implementation.
*   **Class:** `ExamplePaymentAdapter(models.AbstractModel)` (or plain Python class inheriting `PaymentGatewayAdapterBase`)
    *   **Model Name (if AbstractModel):** `_name = 'influence_gen.example.payment.adapter'`
    *   **Inherits:** `PaymentGatewayAdapterBase`.
*   **Purpose:** Concrete adapter for a hypothetical "ExamplePaymentGateway".
*   **Requirements:** REQ-IL-012, REQ-IOKYC-008, REQ-IL-009, REQ-IL-013, REQ-IL-008, REQ-PAC-017.
*   **Attributes:** `api_endpoint`, `api_key`.
*   **Methods:**
    *   `__init__(self, env)`: Fetch config.
    *   `initiate_payment(self, payment_request_dto: PaymentInitiationRequestDto) -> PaymentResultDto`: Implement API call.
    *   `verify_bank_account(self, bank_details_dto: BankAccountVerificationRequestDto) -> BankAccountVerificationResultDto`: Implement API call.
    *   Both methods include request construction, auth, HTTP call, response parsing, error handling, retries, and logging.
*   **Implemented Features:** Specific Payment Gateway Integration, Specific Bank Account Verification, API Call Logic.

### 4.5. `dtos/`

#### 4.5.1. `dtos/__init__.py`
*   **Purpose:** Initializes the Python package for DTOs.
*   **Logic:**
    python
    # odoo_modules/influence_gen_integration_adapters/dtos/__init__.py
    from . import n8n_dtos
    from . import kyc_dtos
    from . import payment_dtos
    
*   **Requirements:** DTO Aggregation.

#### 4.5.2. `dtos/n8n_dtos.py`
*   **Purpose:** DTOs for N8N AI image generation.
*   **Requirements:** REQ-IL-002, REQ-IL-003, REQ-AIGS-001.
*   **Logic:**
    python
    # odoo_modules/influence_gen_integration_adapters/dtos/n8n_dtos.py
    from dataclasses import dataclass, field
    from typing import Optional, Dict, Any, List

    @dataclass
    class N8nAiGenerationRequestDto:
        request_id: str # Odoo-generated unique ID for this request
        prompt: str
        user_id: int # Odoo user ID
        influencer_profile_id: int # Odoo influencer_profile ID
        negative_prompt: Optional[str] = None
        model_id: Optional[str] = None # Identifier for the AI model/LoRA
        resolution: Optional[str] = "1024x1024" # e.g., "widthxheight"
        aspect_ratio: Optional[str] = "1:1"
        seed: Optional[int] = None
        inference_steps: Optional[int] = 20
        cfg_scale: Optional[float] = 7.5
        campaign_id: Optional[int] = None # Odoo campaign ID
        # Add any other parameters required by N8N/AI service
        custom_params: Optional[Dict[str, Any]] = field(default_factory=dict)

    @dataclass
    class GeneratedImageDataDto:
        image_url: Optional[str] = None # If N8N returns a temporary URL
        image_data_b64: Optional[str] = None # If N8N returns base64 encoded image data
        filename: Optional[str] = None # Suggested filename
        content_type: Optional[str] = None # e.g., 'image/png'
        metadata: Optional[Dict[str, Any]] = field(default_factory=dict) # Any extra metadata from generation

    @dataclass
    class N8nAiGenerationResultDto:
        request_id: str # Corresponds to the Odoo request_id
        status: str # e.g., "success", "failure"
        images: List[GeneratedImageDataDto] = field(default_factory=list)
        error_message: Optional[str] = None
        error_code: Optional[str] = None # External service error code
        n8n_execution_id: Optional[str] = None # N8N's own execution ID for tracing
    
*   **Implemented Features:** N8N AI Request DTO, N8N AI Result DTO.

#### 4.5.3. `dtos/kyc_dtos.py`
*   **Purpose:** DTOs for KYC verification services.
*   **Requirements:** REQ-IL-011.
*   **Logic:**
    python
    # odoo_modules/influence_gen_integration_adapters/dtos/kyc_dtos.py
    from dataclasses import dataclass
    from typing import Optional, Dict, Any

    @dataclass
    class KycDocumentDto:
        document_type: str # e.g., 'passport', 'driver_license'
        file_url_front: str # URL to the uploaded document (front)
        file_url_back: Optional[str] = None # URL to the uploaded document (back)

    @dataclass
    class KycVerificationRequestDto:
        kyc_data_id: int # Odoo KYCData record ID
        influencer_profile_id: int # Odoo InfluencerProfile ID
        documents: list[KycDocumentDto]
        # Add other PII as required by the KYC provider
        full_name: Optional[str] = None
        date_of_birth: Optional[str] = None # ISO 8601 format
        address_details: Optional[Dict[str, str]] = None # e.g., street, city, zip, country

    @dataclass
    class KycVerificationResultDto:
        kyc_data_id: int # Odoo KYCData record ID
        external_verification_id: Optional[str] = None # ID from the KYC provider
        status: str # e.g., "approved", "rejected", "pending_review", "needs_more_info"
        reason_code: Optional[str] = None # Provider-specific reason code
        reason_message: Optional[str] = None
        vendor_specific_data: Optional[Dict[str, Any]] = None # Raw response or extra data
    
*   **Implemented Features:** KYC Request DTO, KYC Result DTO.

#### 4.5.4. `dtos/payment_dtos.py`
*   **Purpose:** DTOs for payment gateway and bank account verification.
*   **Requirements:** REQ-IL-012, REQ-IOKYC-008.
*   **Logic:**
    python
    # odoo_modules/influence_gen_integration_adapters/dtos/payment_dtos.py
    from dataclasses import dataclass
    from typing import Optional, Dict, Any, List

    @dataclass
    class BankAccountDetailsDto:
        account_holder_name: str
        account_number: str # Potentially tokenized or reference ID
        bank_name: Optional[str] = None
        routing_number: Optional[str] = None
        iban: Optional[str] = None
        swift_code: Optional[str] = None
        # Other fields as needed by the specific gateway

    @dataclass
    class BankAccountVerificationRequestDto:
        bank_account_id: int # Odoo BankAccount record ID
        influencer_profile_id: int
        bank_details: BankAccountDetailsDto
        # Micro-deposit amounts if applicable for verification step
        micro_deposit_amounts: Optional[List[float]] = None

    @dataclass
    class BankAccountVerificationResultDto:
        bank_account_id: int
        external_verification_id: Optional[str] = None
        status: str # e.g., "verified", "pending", "failed", "micro_deposits_sent"
        reason_message: Optional[str] = None

    @dataclass
    class PaymentInitiationRequestDto:
        payment_record_id: int # Odoo PaymentRecord ID
        influencer_profile_id: int
        amount: float
        currency: str # ISO 4217
        bank_details_reference_id: Optional[str] = None # If gateway uses a token/ID for stored bank details
        bank_details: Optional[BankAccountDetailsDto] = None # Or provide full details if not stored/tokenized
        description: Optional[str] = "InfluenceGen Payout"

    @dataclass
    class PaymentResultDto:
        payment_record_id: int
        external_transaction_id: Optional[str] = None
        status: str # e.g., "succeeded", "pending", "failed", "requires_action"
        reason_code: Optional[str] = None
        reason_message: Optional[str] = None
        paid_at: Optional[str] = None # ISO 8601 timestamp
    
*   **Implemented Features:** Payment Request DTO, Payment Result DTO, Bank Verification Request DTO, Bank Verification Result DTO.

### 4.6. `utils/`

#### 4.6.1. `utils/__init__.py`
*   **Purpose:** Initializes the Python package for utility functions.
*   **Logic:**
    python
    # odoo_modules/influence_gen_integration_adapters/utils/__init__.py
    from . import api_auth
    from . import integration_error_handler
    
*   **Requirements:** Utility Aggregation.

#### 4.6.2. `utils/api_auth.py`
*   **Purpose:** Utilities for API authentication, especially for N8N callback.
*   **Requirements:** REQ-IL-004, REQ-IL-016.
*   **Logging:** Standard Python `logging` module, `_logger = logging.getLogger(__name__)`.
*   **Functions:**
    *   `verify_n8n_request(request: http.request) -> bool`:
        *   **Parameters:** `request` (Odoo `http.request` object).
        *   **Return Type:** `bool`.
        *   **Logic (REQ-IL-004, REQ-IL-016, REQ-PAC-017):**
            1.  Retrieve the expected shared secret/token: `expected_token = request.env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_callback_auth_token')`.
            2.  If `expected_token` is not configured, log a critical error and return `False`.
            3.  Extract the provided token from `request.httprequest.headers.get('X-N8N-Signature')` (or another agreed-upon header/mechanism).
            4.  If no token is provided in the request, log an auth failure and return `False`.
            5.  Securely compare the provided token with the `expected_token` (e.g., using `hmac.compare_digest` to prevent timing attacks).
                python
                import hmac
                if not hmac.compare_digest(provided_token, expected_token):
                    _logger.warning("N8N callback authentication failed: Invalid token.")
                    return False
                return True
                
            6.  Log authentication success/failure.
*   **Implemented Features:** Callback Authentication.

#### 4.6.3. `utils/integration_error_handler.py`
*   **Purpose:** Utilities for handling and mapping errors from external integrations.
*   **Requirements:** REQ-IL-009.
*   **Logging:** Standard Python `logging` module, `_logger = logging.getLogger(__name__)`.
*   **Classes (Custom Exceptions):**
    *   `IntegrationServiceError(Exception)`: Base class for integration errors.
    *   `TransientIntegrationError(IntegrationServiceError)`: For temporary errors that might be retried.
    *   `PermanentIntegrationError(IntegrationServiceError)`: For errors unlikely to be resolved by retrying.
    *   `AuthenticationError(PermanentIntegrationError)`: Specific for auth failures.
    *   `RateLimitError(TransientIntegrationError)`: Specific for rate limit responses.
*   **Functions:**
    *   `handle_external_api_error(response: requests.Response, service_name: str)`:
        *   **Parameters:** `response` (from `requests` library), `service_name` (e.g., "N8N AI Service", "ExampleKYCProvider").
        *   **Return Type:** Raises an appropriate custom exception or returns None if handled.
        *   **Logic (REQ-IL-009):**
            1.  Log detailed error: `_logger.error(f"Error calling {service_name}. Status: {response.status_code}. Response: {response.text[:500]}")`.
            2.  Based on `response.status_code`:
                *   `401`, `403`: Raise `AuthenticationError`.
                *   `429`: Raise `RateLimitError`.
                *   `500`, `502`, `503`, `504`: Raise `TransientIntegrationError`.
                *   Other `4xx`: Raise `PermanentIntegrationError` (or a more specific one like `BadRequestError`).
                *   Other `5xx`: Raise `PermanentIntegrationError`.
            3.  Can be extended to parse error messages from `response.json()` or `response.text` for more specific error mapping.
*   **Implemented Features:** External Error Mapping, Custom Integration Exceptions.

### 4.7. `doc/openapi/`

#### 4.7.1. `doc/openapi/n8n_callback_v1.yaml`
*   **Purpose:** OpenAPI (Swagger) specification for the N8N callback API endpoint.
*   **Requirements:** REQ-DDSI-009, REQ-IL-004.
*   **Format:** YAML, OpenAPI 3.x.
*   **Content Outline:**
    yaml
    openapi: 3.0.0
    info:
      title: InfluenceGen N8N Callback API
      version: v1
      description: API endpoint for N8N to send AI image generation results to Odoo.
    servers:
      - url: '{odoo_base_url}' # Variable for Odoo base URL
        variables:
          odoo_base_url:
            default: https://your-odoo-instance.com
    components:
      securitySchemes:
        N8NSharedSecret: # Or APIKeyHeader, etc.
          type: apiKey
          in: header
          name: X-N8N-Signature # Or your chosen header
      schemas:
        GeneratedImageDataDto:
          type: object
          properties:
            image_url:
              type: string
              format: url
              nullable: true
            image_data_b64:
              type: string
              format: byte # base64 encoded
              nullable: true
            filename:
              type: string
              nullable: true
            content_type:
              type: string
              nullable: true # e.g., image/png
            metadata:
              type: object
              additionalProperties: true
              nullable: true
        N8nAiGenerationResult:
          type: object
          required:
            - request_id
            - status
          properties:
            request_id:
              type: string
              description: The Odoo-generated ID of the original image generation request.
            status:
              type: string
              enum: [success, failure]
              description: Status of the image generation.
            images:
              type: array
              items:
                $ref: '#/components/schemas/GeneratedImageDataDto'
              description: List of generated images (data or URLs).
              nullable: true
            error_message:
              type: string
              nullable: true
              description: Error message if status is 'failure'.
            error_code:
              type: string
              nullable: true
              description: External service error code, if applicable.
            n8n_execution_id:
                type: string
                nullable: true
                description: N8N's internal execution ID for this workflow run.
    paths:
      /influence_gen/n8n/ai_callback:
        post:
          summary: Receives AI image generation results from N8N.
          operationId: handleAiImageResult
          security:
            - N8NSharedSecret: []
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/N8nAiGenerationResult'
          responses:
            '200':
              description: Callback successfully processed.
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      status:
                        type: string
                        example: success
            '400':
              description: Bad Request - Invalid payload.
            '401':
              description: Unauthorized - Authentication failed.
            '500':
              description: Internal Server Error - Error processing callback.
    
*   **Implemented Features:** API Documentation.

## 5. Data Model (DTOs)

Refer to section 4.5 (`dtos/`) for detailed DTO specifications:
*   `n8n_dtos.py`: `N8nAiGenerationRequestDto`, `GeneratedImageDataDto`, `N8nAiGenerationResultDto`.
*   `kyc_dtos.py`: `KycDocumentDto`, `KycVerificationRequestDto`, `KycVerificationResultDto`.
*   `payment_dtos.py`: `BankAccountDetailsDto`, `BankAccountVerificationRequestDto`, `BankAccountVerificationResultDto`, `PaymentInitiationRequestDto`, `PaymentResultDto`.

These DTOs define the structure of data exchanged between Odoo and external systems via this adapter layer.

## 6. Security Considerations

*   **Callback Authentication (REQ-IL-004, REQ-IL-016):** The N8N callback endpoint (`/influence_gen/n8n/ai_callback`) will be secured using a shared secret or token passed in a request header (e.g., `X-N8N-Signature`). This will be verified by `utils.api_auth.verify_n8n_request`.
*   **Outbound Authentication (REQ-IL-008):** API keys and tokens for N8N webhooks and other third-party services will be stored securely as Odoo system parameters (`ir.config_parameter`) and fetched at runtime. They must not be hardcoded. REQ-PAC-017 implies administrators manage these via UI, which should store them securely.
*   **HTTPS/TLS (REQ-IL-007):** All communications (Odoo <-> N8N, Adapters <-> Third-Party APIs) must use HTTPS. Adapters will be configured with HTTPS URLs.
*   **Input Validation:** The N8N callback controller will validate the structure of incoming payloads.
*   **Rate Limiting (REQ-IL-015):**
    *   Odoo's callback endpoint should leverage Odoo's or underlying infrastructure's (e.g., WAF) rate-limiting capabilities.
    *   Adapters making outbound calls should be prepared to handle `429 Too Many Requests` responses from external services.
*   **CSRF Protection:** The N8N callback controller has `csrf=False` as it's a server-to-server API endpoint, not a browser-initiated form submission. Authentication via shared secret handles security.
*   **Logging (REQ-IL-013):** Sensitive information (e.g., full API keys, raw PII in transit unless necessary for the specific API call's payload) should be masked or omitted from logs where appropriate. Request IDs and correlation IDs should be logged for traceability.

## 7. Error Handling and Retry Mechanisms (REQ-IL-009)

*   **Adapters (Outbound Calls):**
    *   Will use `try-except` blocks to catch `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, and other `requests.exceptions.RequestException`.
    *   A retry mechanism (e.g., using the `tenacity` library or a custom loop with exponential backoff) will be implemented for transient failures (configurable number of retries).
    *   The `utils.integration_error_handler.py` will define custom exceptions (`TransientIntegrationError`, `PermanentIntegrationError`, `RateLimitError`, `AuthenticationError`) and a helper function to raise them based on HTTP status codes or exception types.
    *   Persistent failures will be logged and an appropriate exception raised to be handled by the calling service in the business logic layer.
*   **Controller (Inbound Callbacks):**
    *   Will use `try-except` blocks to handle errors during payload parsing, DTO instantiation, authentication, or when calling business services.
    *   Detailed errors will be logged.
    *   Appropriate HTTP error responses (400, 401, 500) will be returned to N8N. N8N should have its own error handling for failed callbacks.

## 8. Configuration Management (REQ-PAC-017, REQ-IL-008)

*   **N8N Webhook URL:** Stored as `ir.config_parameter` (key: `influence_gen.n8n_ai_webhook_url`).
*   **N8N Webhook Auth Token:** Stored securely as `ir.config_parameter` (key: `influence_gen.n8n_ai_auth_token`).
*   **N8N Callback Auth Token:** Stored securely as `ir.config_parameter` (key: `influence_gen.n8n_callback_auth_token`).
*   **Third-Party API Keys/Endpoints (KYC, Payment):** Stored securely as `ir.config_parameter` with specific keys (e.g., `influence_gen.example_kyc.api_key`, `influence_gen.example_kyc.api_url`).
*   Retrieval will be done via `self.env['ir.config_parameter'].sudo().get_param('key_name')`.
*   The `Platform Administration & Core Configuration` module (REPO-IGAC-005) would provide the UI for administrators to manage these parameters.

## 9. Logging (REQ-IL-013)

*   All adapter methods making external calls will log:
    *   Initiation of the call (masking sensitive payload data).
    *   Response status code and a summary of the response.
    *   Any errors encountered, including full tracebacks for exceptions.
    *   Retry attempts.
*   The N8N callback controller will log:
    *   Receipt of the callback request (summary of payload).
    *   Authentication success/failure.
    *   Validation success/failure of the payload.
    *   Outcome of dispatching to the business service.
    *   Any errors encountered.
*   Logs will include timestamps, request IDs, and relevant context.
*   The `Audit Trail & Event Logging System` (REPO-IGAL-006) will consume these logs if they are configured as auditable events. Operational logs will go to the centralized logging solution.

## 10. Dependencies

*   **Odoo 18 Framework:** Core framework.
*   **Python `requests` library:** For making HTTP calls.
*   **`influence_gen_shared_utilities` (REPO-IGSCU-007):** Potentially for shared logging utilities, advanced secret management wrappers, or common DTO base classes if defined there. (For now, assuming direct Odoo mechanisms and local utils).
*   **`influence_gen_business_services` (REPO-IGBS-003):** The N8N callback controller will dispatch data to services defined in this module. Adapters might be invoked by services from this module.

This SDS provides a comprehensive plan for developing the `InfluenceGen.Odoo.Integration.Adapters` module, focusing on robust, secure, and maintainable integrations.