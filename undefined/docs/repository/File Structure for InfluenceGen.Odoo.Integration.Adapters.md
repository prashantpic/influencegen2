# Specification

# 1. Files

- **Path:** odoo_modules/influence_gen_integration_adapters/__init__.py  
**Description:** Initializes the Python package for Odoo, importing submodules like controllers and adapters so they are recognized by Odoo.  
**Template:** Odoo Module Init Template  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes Python modules within this Odoo addon importable.  
**Logic Description:** Contains import statements for 'controllers', 'adapters', 'dtos', and 'utils' sub-packages.  
**Documentation:**
    
    - **Summary:** Standard Odoo module Python package initializer.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_integration_adapters/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata like name, version, author, dependencies, and data files to load.  
**Template:** Odoo Manifest Template  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** ModuleManifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    
**Requirement Ids:**
    
    
**Purpose:** Describes the Odoo module to the Odoo framework, including its dependencies on other Odoo modules like 'base', 'web', and potentially 'influence_gen_shared_utilities' (REPO-IGSCU-007) and 'influence_gen_business_services' (REPO-IGBS-003) if service interfaces are directly invoked.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'category', 'depends' (listing 'base', 'web', 'mail', and potentially 'influence_gen_shared_utilities', 'influence_gen_business_services'), 'data' (listing XML view files if any, though this repo is primarily backend controllers/adapters), 'installable', 'application', 'auto_install'.  
**Documentation:**
    
    - **Summary:** Defines the 'InfluenceGen Integration Adapters' Odoo module and its metadata.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** odoo_modules/influence_gen_integration_adapters/controllers/__init__.py  
**Description:** Initializes the Python package for Odoo controllers within this module.  
**Template:** Odoo Package Init Template  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** controllers/__init__.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Controller Aggregation
    
**Requirement Ids:**
    
    
**Purpose:** Makes controller classes available to the Odoo framework.  
**Logic Description:** Contains import statements for all controller files in this directory, e.g., 'from . import n8n_callback_controller'.  
**Documentation:**
    
    - **Summary:** Initializes the controllers sub-package.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.controllers  
**Metadata:**
    
    - **Category:** Controller
    
- **Path:** odoo_modules/influence_gen_integration_adapters/controllers/n8n_callback_controller.py  
**Description:** Odoo HTTP controller to handle incoming callbacks from N8N, primarily for AI image generation results. It validates requests and dispatches data to business services.  
**Template:** Odoo Controller Template  
**Dependancy Level:** 3  
**Name:** N8NCallbackController  
**Type:** Controller  
**Relative Path:** controllers/n8n_callback_controller.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    - MVC Controller
    - WebhookIntegration
    
**Members:**
    
    - **Name:** _logger  
**Type:** logging.Logger  
**Attributes:** private|static  
    
**Methods:**
    
    - **Name:** handle_ai_image_result  
**Parameters:**
    
    - self
    - http.request request_data
    
**Return Type:** werkzeug.wrappers.Response  
**Attributes:** public|@http.route('/influence_gen/n8n/ai_callback', type='json', auth='public', methods=['POST'], csrf=False, cors='*')  
    
**Implemented Features:**
    
    - N8N Callback Handling
    - Request Validation
    - Data Dispatching
    - Error Handling for Callbacks
    - API Security
    
**Requirement Ids:**
    
    - REQ-IL-003
    - REQ-IL-004
    - REQ-IL-010
    - REQ-IL-016
    - REQ-AIGS-001
    
**Purpose:** Serves as the secure endpoint for N8N to send AI image generation results (success/failure) to Odoo. Validates the callback and passes data to the appropriate business service for processing.  
**Logic Description:** The `handle_ai_image_result` method will: 1. Authenticate the incoming request from N8N (e.g., using a shared secret/token via `utils.api_auth.verify_n8n_request`). 2. Parse the JSON payload into a structured DTO (e.g., `N8nAiGenerationResultDto`). 3. Perform basic validation on the payload structure. 4. Log the incoming callback request (REQ-IL-013). 5. If successful, invoke a method on a business service (e.g., `request.env['influence_gen.ai_image_service'].process_n8n_ai_result(parsed_dto)`) from REPO-IGBS-003. 6. Handle potential errors during parsing or dispatching, logging them and returning appropriate HTTP error responses. 7. Ensure rate limiting mechanisms are applied if configured (REQ-IL-015).  
**Documentation:**
    
    - **Summary:** Receives and processes AI image generation results from N8N. Inputs: JSON payload from N8N. Outputs: HTTP response (200 OK on success, error codes on failure).
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.controllers.n8n_callback_controller  
**Metadata:**
    
    - **Category:** Controller
    
- **Path:** odoo_modules/influence_gen_integration_adapters/adapters/__init__.py  
**Description:** Initializes the Python package for integration adapters within this module.  
**Template:** Odoo Package Init Template  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** adapters/__init__.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Adapter Aggregation
    
**Requirement Ids:**
    
    
**Purpose:** Makes adapter classes available for use within the module.  
**Logic Description:** Contains import statements for all adapter files in this directory, e.g., 'from . import n8n_ai_adapter, kyc_service_adapter_base'.  
**Documentation:**
    
    - **Summary:** Initializes the adapters sub-package.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.adapters  
**Metadata:**
    
    - **Category:** Adapter
    
- **Path:** odoo_modules/influence_gen_integration_adapters/adapters/n8n_ai_adapter.py  
**Description:** Client/Adapter for initiating AI image generation requests to the N8N webhook. Handles request construction, authentication, and basic error handling.  
**Template:** Python Service/Client Template  
**Dependancy Level:** 2  
**Name:** N8nAiAdapter  
**Type:** Adapter  
**Relative Path:** adapters/n8n_ai_adapter.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    - AdapterPattern
    - WebhookIntegration
    
**Members:**
    
    - **Name:** _logger  
**Type:** logging.Logger  
**Attributes:** private|static  
    - **Name:** n8n_webhook_url  
**Type:** str  
**Attributes:** private  
    - **Name:** n8n_auth_token  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** initiate_ai_image_generation  
**Parameters:**
    
    - self
    - generation_request_dto: N8nAiGenerationRequestDto
    
**Return Type:** dict  
**Attributes:** public  
    
**Implemented Features:**
    
    - N8N Webhook Invocation
    - AI Request Construction
    - External API Authentication
    - Error Handling and Retries for N8N calls
    
**Requirement Ids:**
    
    - REQ-IL-002
    - REQ-AIGS-001
    - REQ-IL-009
    - REQ-IL-013
    - REQ-IL-015
    
**Purpose:** Provides a method to securely call the N8N webhook to trigger an AI image generation workflow, passing necessary prompts and parameters.  
**Logic Description:** The `__init__` method will fetch N8N webhook URL and auth token from Odoo's configuration parameters (REQ-PAC-017, REQ-IL-008), potentially using utilities from REPO-IGSCU-007 for secure retrieval. The `initiate_ai_image_generation` method will: 1. Construct the JSON payload using the input `generation_request_dto`. 2. Make an HTTP POST request to the N8N webhook URL using the 'requests' library. 3. Include necessary authentication headers (e.g., bearer token). 4. Implement error handling for network issues, HTTP errors from N8N. 5. Implement basic retry logic for transient failures (REQ-IL-009). 6. Log the request initiation and outcome (REQ-IL-013). 7. Handle potential rate limiting responses from N8N (REQ-IL-015). 8. Return a success/failure indicator or N8N's immediate response.  
**Documentation:**
    
    - **Summary:** Client to trigger AI image generation workflows in N8N. Inputs: N8nAiGenerationRequestDto. Outputs: Dictionary with N8N webhook call status.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.adapters.n8n_ai_adapter  
**Metadata:**
    
    - **Category:** Adapter
    
- **Path:** odoo_modules/influence_gen_integration_adapters/adapters/kyc_service_adapter_base.py  
**Description:** Abstract base class or interface for KYC service adapters. Defines the contract for interacting with different KYC verification services.  
**Template:** Python Abstract Class/Interface Template  
**Dependancy Level:** 1  
**Name:** KycServiceAdapterBase  
**Type:** AdapterInterface  
**Relative Path:** adapters/kyc_service_adapter_base.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    - AdapterPattern
    - StrategyPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** verify_identity  
**Parameters:**
    
    - self
    - kyc_request_dto: KycVerificationRequestDto
    
**Return Type:** KycVerificationResultDto  
**Attributes:** public|abstractmethod  
    
**Implemented Features:**
    
    - KYC Service Abstraction
    
**Requirement Ids:**
    
    - REQ-IL-011
    - REQ-IOKYC-005
    
**Purpose:** Provides a common interface for different KYC service implementations, allowing for flexibility in choosing or switching KYC providers.  
**Logic Description:** Defines abstract methods like `verify_identity` that concrete KYC adapters must implement. May include common helper methods if applicable.  
**Documentation:**
    
    - **Summary:** Abstract base for KYC service adapters.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.adapters.kyc_service_adapter_base  
**Metadata:**
    
    - **Category:** Adapter
    
- **Path:** odoo_modules/influence_gen_integration_adapters/adapters/example_kyc_adapter.py  
**Description:** Example concrete implementation of a KYC service adapter for a hypothetical 'ExampleKYCProvider'.  
**Template:** Python Service/Client Template  
**Dependancy Level:** 2  
**Name:** ExampleKycAdapter  
**Type:** Adapter  
**Relative Path:** adapters/example_kyc_adapter.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** _logger  
**Type:** logging.Logger  
**Attributes:** private|static  
    - **Name:** api_endpoint  
**Type:** str  
**Attributes:** private  
    - **Name:** api_key  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** verify_identity  
**Parameters:**
    
    - self
    - kyc_request_dto: KycVerificationRequestDto
    
**Return Type:** KycVerificationResultDto  
**Attributes:** public  
    
**Implemented Features:**
    
    - Specific KYC Service Integration
    - API Call Logic
    - Error Handling for KYC Service
    
**Requirement Ids:**
    
    - REQ-IL-011
    - REQ-IOKYC-005
    - REQ-IL-009
    - REQ-IL-013
    
**Purpose:** Connects to a specific third-party KYC verification service, sends verification requests, and processes responses.  
**Logic Description:** Inherits from `KycServiceAdapterBase`. `__init__` fetches API endpoint and key from Odoo config (REQ-PAC-017, REQ-IL-008). `verify_identity` method constructs the request for 'ExampleKYCProvider' API, makes the HTTP call using 'requests', handles API-specific authentication, parses the response into `KycVerificationResultDto`, implements error handling and retry logic for this specific service (REQ-IL-009), and logs interactions (REQ-IL-013).  
**Documentation:**
    
    - **Summary:** Adapter for 'ExampleKYCProvider'. Inputs: KycVerificationRequestDto. Outputs: KycVerificationResultDto.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.adapters.example_kyc_adapter  
**Metadata:**
    
    - **Category:** Adapter
    
- **Path:** odoo_modules/influence_gen_integration_adapters/adapters/payment_gateway_adapter_base.py  
**Description:** Abstract base class or interface for payment gateway adapters.  
**Template:** Python Abstract Class/Interface Template  
**Dependancy Level:** 1  
**Name:** PaymentGatewayAdapterBase  
**Type:** AdapterInterface  
**Relative Path:** adapters/payment_gateway_adapter_base.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    - AdapterPattern
    - StrategyPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initiate_payment  
**Parameters:**
    
    - self
    - payment_request_dto: PaymentInitiationRequestDto
    
**Return Type:** PaymentResultDto  
**Attributes:** public|abstractmethod  
    - **Name:** verify_bank_account  
**Parameters:**
    
    - self
    - bank_details_dto: BankAccountVerificationRequestDto
    
**Return Type:** BankAccountVerificationResultDto  
**Attributes:** public|abstractmethod  
    
**Implemented Features:**
    
    - Payment Gateway Abstraction
    - Bank Account Verification Abstraction
    
**Requirement Ids:**
    
    - REQ-IL-012
    - REQ-IOKYC-008
    
**Purpose:** Defines a common contract for interacting with different payment gateways and bank verification services.  
**Logic Description:** Defines abstract methods like `initiate_payment` and `verify_bank_account`.  
**Documentation:**
    
    - **Summary:** Abstract base for payment gateway and bank verification adapters.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.adapters.payment_gateway_adapter_base  
**Metadata:**
    
    - **Category:** Adapter
    
- **Path:** odoo_modules/influence_gen_integration_adapters/adapters/example_payment_adapter.py  
**Description:** Example concrete implementation for a hypothetical 'ExamplePaymentGateway' that might also offer bank account verification.  
**Template:** Python Service/Client Template  
**Dependancy Level:** 2  
**Name:** ExamplePaymentAdapter  
**Type:** Adapter  
**Relative Path:** adapters/example_payment_adapter.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    - AdapterPattern
    
**Members:**
    
    - **Name:** _logger  
**Type:** logging.Logger  
**Attributes:** private|static  
    - **Name:** api_endpoint  
**Type:** str  
**Attributes:** private  
    - **Name:** api_key  
**Type:** str  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    - env
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** initiate_payment  
**Parameters:**
    
    - self
    - payment_request_dto: PaymentInitiationRequestDto
    
**Return Type:** PaymentResultDto  
**Attributes:** public  
    - **Name:** verify_bank_account  
**Parameters:**
    
    - self
    - bank_details_dto: BankAccountVerificationRequestDto
    
**Return Type:** BankAccountVerificationResultDto  
**Attributes:** public  
    
**Implemented Features:**
    
    - Specific Payment Gateway Integration
    - Specific Bank Account Verification
    - API Call Logic
    
**Requirement Ids:**
    
    - REQ-IL-012
    - REQ-IOKYC-008
    - REQ-IL-009
    - REQ-IL-013
    
**Purpose:** Connects to 'ExamplePaymentGateway' to process payments and verify bank accounts.  
**Logic Description:** Inherits from `PaymentGatewayAdapterBase`. `__init__` fetches API details from Odoo config. Methods implement calls to the gateway's API, handle responses, errors, retries, and logging.  
**Documentation:**
    
    - **Summary:** Adapter for 'ExamplePaymentGateway'. Handles payments and bank verification.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.adapters.example_payment_adapter  
**Metadata:**
    
    - **Category:** Adapter
    
- **Path:** odoo_modules/influence_gen_integration_adapters/dtos/__init__.py  
**Description:** Initializes the Python package for Data Transfer Objects (DTOs).  
**Template:** Odoo Package Init Template  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** dtos/__init__.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - DTO Aggregation
    
**Requirement Ids:**
    
    
**Purpose:** Makes DTO classes available for use within the module.  
**Logic Description:** Contains import statements for all DTO files in this directory, e.g., 'from . import n8n_dtos, kyc_dtos'.  
**Documentation:**
    
    - **Summary:** Initializes the DTOs sub-package.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.dtos  
**Metadata:**
    
    - **Category:** DTO
    
- **Path:** odoo_modules/influence_gen_integration_adapters/dtos/n8n_dtos.py  
**Description:** Defines Data Transfer Objects for communication with N8N regarding AI image generation.  
**Template:** Python DataClass Template  
**Dependancy Level:** 0  
**Name:** n8n_dtos  
**Type:** DTO  
**Relative Path:** dtos/n8n_dtos.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N AI Request DTO
    - N8N AI Result DTO
    
**Requirement Ids:**
    
    - REQ-IL-002
    - REQ-IL-003
    - REQ-AIGS-001
    
**Purpose:** Provides structured data classes for N8N AI request payloads and N8N AI result callbacks.  
**Logic Description:** Contains Python data classes (e.g., using `@dataclass`): `N8nAiGenerationRequestDto` (fields: prompt, negative_prompt, model_id, resolution, aspect_ratio, seed, steps, cfg_scale, user_id, request_id, campaign_id_optional, etc.) and `N8nAiGenerationResultDto` (fields: request_id, status_success_or_fail, image_url_or_data_optional, error_message_optional, generation_metadata_optional).  
**Documentation:**
    
    - **Summary:** DTOs for N8N AI image generation requests and results.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.dtos.n8n_dtos  
**Metadata:**
    
    - **Category:** DTO
    
- **Path:** odoo_modules/influence_gen_integration_adapters/dtos/kyc_dtos.py  
**Description:** Defines DTOs for interacting with KYC verification services.  
**Template:** Python DataClass Template  
**Dependancy Level:** 0  
**Name:** kyc_dtos  
**Type:** DTO  
**Relative Path:** dtos/kyc_dtos.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - KYC Request DTO
    - KYC Result DTO
    
**Requirement Ids:**
    
    - REQ-IL-011
    
**Purpose:** Structured data for KYC verification requests and responses.  
**Logic Description:** Contains Python data classes: `KycVerificationRequestDto` (fields: influencer_id, document_front_url, document_back_url_optional, document_type, etc.) and `KycVerificationResultDto` (fields: verification_id, status, reason_optional, vendor_specific_data_optional).  
**Documentation:**
    
    - **Summary:** DTOs for KYC service interactions.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.dtos.kyc_dtos  
**Metadata:**
    
    - **Category:** DTO
    
- **Path:** odoo_modules/influence_gen_integration_adapters/dtos/payment_dtos.py  
**Description:** Defines DTOs for payment gateway interactions and bank account verification.  
**Template:** Python DataClass Template  
**Dependancy Level:** 0  
**Name:** payment_dtos  
**Type:** DTO  
**Relative Path:** dtos/payment_dtos.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Payment Request DTO
    - Payment Result DTO
    - Bank Verification Request DTO
    - Bank Verification Result DTO
    
**Requirement Ids:**
    
    - REQ-IL-012
    - REQ-IOKYC-008
    
**Purpose:** Structured data for payment initiation/results and bank account verification requests/responses.  
**Logic Description:** Contains Python data classes: `PaymentInitiationRequestDto`, `PaymentResultDto`, `BankAccountVerificationRequestDto`, `BankAccountVerificationResultDto` with relevant fields for amounts, currencies, account details, statuses, transaction IDs etc.  
**Documentation:**
    
    - **Summary:** DTOs for payment gateway and bank verification service interactions.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.dtos.payment_dtos  
**Metadata:**
    
    - **Category:** DTO
    
- **Path:** odoo_modules/influence_gen_integration_adapters/utils/__init__.py  
**Description:** Initializes the Python package for utility functions specific to this integration adapters module.  
**Template:** Odoo Package Init Template  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** utils/__init__.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Utility Aggregation
    
**Requirement Ids:**
    
    
**Purpose:** Makes utility functions available for use within the module.  
**Logic Description:** Contains import statements for all utility files in this directory, e.g., 'from . import api_auth'.  
**Documentation:**
    
    - **Summary:** Initializes the internal utilities sub-package.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_integration_adapters/utils/api_auth.py  
**Description:** Provides utility functions for API authentication, particularly for securing the N8N callback endpoint.  
**Template:** Python Utility Module Template  
**Dependancy Level:** 1  
**Name:** api_auth  
**Type:** Utility  
**Relative Path:** utils/api_auth.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** verify_n8n_request  
**Parameters:**
    
    - request: http.request
    
**Return Type:** bool  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - Callback Authentication
    
**Requirement Ids:**
    
    - REQ-IL-004
    - REQ-IL-016
    
**Purpose:** Contains logic to authenticate incoming requests to the N8N callback controller, e.g., by verifying a shared secret or token.  
**Logic Description:** The `verify_n8n_request` function will: 1. Retrieve the expected secret/token from Odoo's configuration parameters (REQ-PAC-017). 2. Extract the token from the incoming request's headers or payload. 3. Compare the tokens securely (e.g., using `hmac.compare_digest`). 4. Return True if valid, False otherwise. Log failed attempts.  
**Documentation:**
    
    - **Summary:** Utilities for authenticating API requests, specifically for the N8N callback.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.utils.api_auth  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_integration_adapters/utils/integration_error_handler.py  
**Description:** Provides utility functions or custom exceptions for handling and mapping errors from external integrations.  
**Template:** Python Utility Module Template  
**Dependancy Level:** 0  
**Name:** integration_error_handler  
**Type:** Utility  
**Relative Path:** utils/integration_error_handler.py  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** handle_external_api_error  
**Parameters:**
    
    - response: requests.Response
    - service_name: str
    
**Return Type:** void  
**Attributes:** public|static  
    
**Implemented Features:**
    
    - External Error Mapping
    - Custom Integration Exceptions
    
**Requirement Ids:**
    
    - REQ-IL-009
    
**Purpose:** Centralizes common error handling logic for external API calls, such as mapping HTTP status codes to specific exceptions or standardized error messages.  
**Logic Description:** Defines custom exception classes like `IntegrationServiceError`, `TransientIntegrationError`, `PermanentIntegrationError`. The `handle_external_api_error` function could take a `requests.Response` object, log detailed error information, and raise an appropriate custom exception. This helps in standardizing error handling across different adapters.  
**Documentation:**
    
    - **Summary:** Utilities for handling errors from external service integrations.
    
**Namespace:** odoo.addons.influence_gen_integration_adapters.utils.integration_error_handler  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_integration_adapters/doc/openapi/n8n_callback_v1.yaml  
**Description:** OpenAPI (Swagger) specification for the N8N callback API endpoint exposed by Odoo.  
**Template:** OpenAPI Specification File  
**Dependancy Level:** 0  
**Name:** n8n_callback_v1  
**Type:** APISpecification  
**Relative Path:** doc/openapi/n8n_callback_v1.yaml  
**Repository Id:** REPO-IGIA-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Documentation
    
**Requirement Ids:**
    
    - REQ-DDSI-009
    - REQ-IL-004
    
**Purpose:** Provides a formal definition of the N8N callback API, including request/response schemas, authentication methods, and endpoint details.  
**Logic Description:** A YAML file following OpenAPI 3.x specification. Defines the path `/influence_gen/n8n/ai_callback`, method POST. Specifies request body schema (referencing `N8nAiGenerationResultDto` concept) and response schemas (e.g., 200 OK, 400 Bad Request, 401 Unauthorized, 500 Internal Server Error). Describes security schemes (e.g., API key in header).  
**Documentation:**
    
    - **Summary:** OpenAPI specification for the N8N to Odoo callback API.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Documentation
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableExampleKYCAdapter
  - EnableExamplePaymentAdapter
  
- **Database Configs:**
  
  


---

