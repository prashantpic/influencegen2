# Specification

# 1. Files

- **Path:** odoo_modules/influence_gen_ai_integration/__init__.py  
**Description:** Initializes the Python package for the Odoo AI Integration Endpoints module, importing submodules like controllers and services.  
**Template:** Odoo Module Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes the directory a Python package and imports its main components.  
**Logic Description:** Import the 'controllers' and 'services' submodules.  
**Documentation:**
    
    - **Summary:** Standard Odoo module initializer. Imports necessary sub-packages for the module to be recognized and functional within Odoo.
    
**Namespace:** odoo.addons.influence_gen_ai_integration  
**Metadata:**
    
    - **Category:** Core
    
- **Path:** odoo_modules/influence_gen_ai_integration/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata, dependencies, and data files for the AI Integration Endpoints.  
**Template:** Odoo Manifest  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Configuration  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    - ModularDesign
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    
**Requirement Ids:**
    
    
**Purpose:** Declares the Odoo module, its name, version, dependencies, and data files to be loaded.  
**Logic Description:** Define module properties such as 'name', 'version', 'summary', 'author', 'category', 'depends' (e.g., ['base', 'web', 'mail', 'influence_gen_base_models']), and 'data' (e.g., ['security/ir_config_parameter_data.xml']). The 'application' flag should be set appropriately, likely False as this is an integration module.  
**Documentation:**
    
    - **Summary:** Provides metadata for the Odoo module system, including dependencies like 'base', 'web', and other InfluenceGen core modules if they exist.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Core
    
- **Path:** odoo_modules/influence_gen_ai_integration/controllers/__init__.py  
**Description:** Initializes the Python package for controllers within the AI Integration Endpoints module.  
**Template:** Odoo Controller Package Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** controllers/__init__.py  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Controller Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'controllers' directory a Python package and imports controller classes.  
**Logic Description:** Import the 'ai_integration_controller' module.  
**Documentation:**
    
    - **Summary:** Initializes the controllers sub-package, making controller classes available to the Odoo framework.
    
**Namespace:** odoo.addons.influence_gen_ai_integration.controllers  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_ai_integration/controllers/ai_integration_controller.py  
**Description:** Defines Odoo HTTP controllers for handling AI integration endpoints, specifically the callback from N8N for AI image generation results.  
**Template:** Odoo Controller  
**Dependancy Level:** 2  
**Name:** ai_integration_controller  
**Type:** Controller  
**Relative Path:** controllers/ai_integration_controller.py  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    - MVC
    - WebhookIntegration
    
**Members:**
    
    
**Methods:**
    
    - **Name:** handle_n8n_image_result_callback  
**Parameters:**
    
    - self
    - Http.request
    - string ai_generation_request_id
    - dict payload
    
**Return Type:** werkzeug.wrappers.Response  
**Attributes:** public  
    
**Implemented Features:**
    
    - N8N Callback Handling
    - API Endpoint Security
    - JSON Payload Processing
    
**Requirement Ids:**
    
    - REQ-IL-003
    - REQ-IL-004
    - REQ-IL-016
    - REQ-AIGS-001
    - REQ-DDSI-009
    
**Purpose:** Provides a secure REST API endpoint for N8N to send AI image generation results (success/failure) back to Odoo.  
**Logic Description:** Inherit from 'odoo.http.Controller'. Define a method, e.g., 'handle_n8n_image_result_callback', decorated with '@http.route' to expose '/influence_gen/ai/callback/image_result'. Route type should be 'json', method 'POST', auth 'public' (with custom token validation), csrf=False. Validate a secret token from request headers/payload against a securely stored token (using 'security_utils'). Parse the incoming JSON payload from N8N. Delegate processing of the parsed data to 'ai_result_service.process_n8n_callback'. Return an appropriate HTTP JSON response (e.g., {'status': 'success'} or {'status': 'error', 'message': '...'}) to N8N. Implement robust error handling for invalid requests or processing failures. Log callback reception and outcome.  
**Documentation:**
    
    - **Summary:** This controller exposes a JSON-based REST endpoint for N8N to call back with AI image generation results. It authenticates the request, parses the payload, and invokes a service to process the results.
    
**Namespace:** odoo.addons.influence_gen_ai_integration.controllers.ai_integration_controller  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** odoo_modules/influence_gen_ai_integration/services/__init__.py  
**Description:** Initializes the Python package for services within the AI Integration Endpoints module.  
**Template:** Odoo Service Package Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** services/__init__.py  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'services' directory a Python package and imports service classes.  
**Logic Description:** Import 'ai_request_service' and 'ai_result_service' modules.  
**Documentation:**
    
    - **Summary:** Initializes the services sub-package, making service classes available for use by controllers and other parts of the module.
    
**Namespace:** odoo.addons.influence_gen_ai_integration.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_ai_integration/services/ai_request_service.py  
**Description:** Service responsible for initiating AI image generation requests from Odoo to N8N via webhook calls.  
**Template:** Odoo Service  
**Dependancy Level:** 1  
**Name:** ai_request_service  
**Type:** Service  
**Relative Path:** services/ai_request_service.py  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    - ServiceLayer
    - WebhookIntegration
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    
**Methods:**
    
    - **Name:** initiate_ai_image_generation  
**Parameters:**
    
    - self
    - int ai_generation_request_model_id
    - dict generation_params
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** _get_n8n_webhook_url  
**Parameters:**
    
    - self
    
**Return Type:** str  
**Attributes:** private  
    - **Name:** _get_n8n_api_key  
**Parameters:**
    
    - self
    
**Return Type:** str  
**Attributes:** private  
    
**Implemented Features:**
    
    - N8N Webhook Invocation
    - Secure Credential Retrieval
    - Request Payload Construction
    
**Requirement Ids:**
    
    - REQ-IL-002
    - REQ-IL-008
    - REQ-AIGS-001
    
**Purpose:** Orchestrates sending AI image generation requests from Odoo to N8N.  
**Logic Description:** Define as an 'models.AbstractModel'. Implement 'initiate_ai_image_generation' method. This method will: Fetch the 'AIImageGenerationRequest' record. Retrieve N8N webhook URL and API key securely from Odoo configuration (e.g., 'ir.config_parameter' or environment variables, using private helper methods like '_get_n8n_webhook_url' and '_get_n8n_api_key'). Construct the JSON payload containing 'ai_generation_request_model_id', 'generation_params' (prompt, negative_prompt, model_id, resolution, aspect_ratio, seed, etc.) and a callback_url for N8N. Use the 'requests' library to make an asynchronous POST request to the N8N webhook URL, including the API key in headers for authentication if N8N webhook is secured. Handle HTTP errors and timeouts from the webhook call. Log the request initiation, payload (masking sensitive parts if any), and N8N's immediate response (e.g., acknowledgement). Update the status of the 'AIImageGenerationRequest' record (e.g., 'processing', 'initiation_failed').  
**Documentation:**
    
    - **Summary:** This service sends requests to N8N to start AI image generation. It securely fetches N8N endpoint details and API keys, constructs the request payload, and makes the HTTP call.
    
**Namespace:** odoo.addons.influence_gen_ai_integration.services.ai_request_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_ai_integration/services/ai_result_service.py  
**Description:** Service responsible for processing the AI image generation results received from N8N via callback.  
**Template:** Odoo Service  
**Dependancy Level:** 1  
**Name:** ai_result_service  
**Type:** Service  
**Relative Path:** services/ai_result_service.py  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    - ServiceLayer
    - WebhookIntegration
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private|static  
    
**Methods:**
    
    - **Name:** process_n8n_callback  
**Parameters:**
    
    - self
    - dict n8n_payload
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** _handle_successful_generation  
**Parameters:**
    
    - self
    - AIImageGenerationRequest request_record
    - dict success_data
    
**Return Type:** None  
**Attributes:** private  
    - **Name:** _handle_failed_generation  
**Parameters:**
    
    - self
    - AIImageGenerationRequest request_record
    - dict error_data
    
**Return Type:** None  
**Attributes:** private  
    - **Name:** _download_and_store_image  
**Parameters:**
    
    - self
    - str image_url
    - AIImageGenerationRequest request_record
    
**Return Type:** GeneratedImage record or None  
**Attributes:** private  
    
**Implemented Features:**
    
    - N8N Callback Processing
    - Image Data Handling
    - Image Storage
    - AI Request Status Update
    
**Requirement Ids:**
    
    - REQ-IL-003
    - REQ-IL-010
    - REQ-AIGS-001
    
**Purpose:** Processes the results of AI image generation sent back by N8N.  
**Logic Description:** Define as an 'models.AbstractModel'. Implement 'process_n8n_callback'. This method will: Retrieve 'ai_generation_request_id' from 'n8n_payload'. Fetch the corresponding 'AIImageGenerationRequest' record. Check 'n8n_payload' for success/failure status. If successful: Call '_handle_successful_generation'. This private method will parse image data (direct binary or temporary URL), file format, size, dimensions. If a URL is provided, call '_download_and_store_image' to download it using 'requests.get()' and store it (e.g., as 'ir.attachment' linked to a new 'GeneratedImage' record or custom storage logic). Update the 'AIImageGenerationRequest' status to 'completed', link to the new 'GeneratedImage' record, and store relevant metadata (hash, etc.). If failed: Call '_handle_failed_generation'. This private method will log error details from N8N and update the 'AIImageGenerationRequest' status to 'failed' with error messages. Implement robust error handling for parsing, image download, and database operations. Consider notifying the user via Odoo bus or email about the outcome.  
**Documentation:**
    
    - **Summary:** This service handles the asynchronous callback from N8N. It parses the response, stores the generated image (or logs errors), and updates the status of the original AI image generation request in Odoo.
    
**Namespace:** odoo.addons.influence_gen_ai_integration.services.ai_result_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** odoo_modules/influence_gen_ai_integration/utils/__init__.py  
**Description:** Initializes the Python package for utility functions within the AI Integration Endpoints module.  
**Template:** Python Package Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** utils/__init__.py  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Utility Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Makes the 'utils' directory a Python package.  
**Logic Description:** Import 'security_utils' or other utility modules if created.  
**Documentation:**
    
    - **Summary:** Initializes the utility sub-package.
    
**Namespace:** odoo.addons.influence_gen_ai_integration.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_ai_integration/utils/security_utils.py  
**Description:** Contains utility functions related to security for the AI integration, such as token validation for N8N callbacks.  
**Template:** Python Utility Module  
**Dependancy Level:** 0  
**Name:** security_utils  
**Type:** Utility  
**Relative Path:** utils/security_utils.py  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** validate_n8n_callback_token  
**Parameters:**
    
    - odoo_env
    - str received_token
    
**Return Type:** bool  
**Attributes:** static  
    
**Implemented Features:**
    
    - Callback Token Validation
    
**Requirement Ids:**
    
    - REQ-IL-016
    - REQ-IL-008
    
**Purpose:** Provides security-related utility functions, primarily for validating callbacks from N8N.  
**Logic Description:** Implement 'validate_n8n_callback_token'. This function will take the Odoo environment ('env') and the token received in the callback request. It will fetch the expected shared secret/token securely from Odoo configuration (e.g., 'ir.config_parameter' named 'influence_gen.n8n_callback_token' or environment variable). Perform a constant-time comparison between the received token and the expected token. Return True if valid, False otherwise. Log validation attempts and failures.  
**Documentation:**
    
    - **Summary:** This utility module offers functions for security aspects of the N8N integration, such as validating tokens for incoming callback requests to ensure authenticity.
    
**Namespace:** odoo.addons.influence_gen_ai_integration.utils.security_utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_ai_integration/security/data/ir_config_parameter_data.xml  
**Description:** Placeholder or example data for Odoo system parameters related to N8N integration (e.g., webhook URL, API key). In a production setup, these should be managed via environment variables or Odoo's secrets management for enhanced security.  
**Template:** Odoo Data XML  
**Dependancy Level:** 0  
**Name:** ir_config_parameter_data  
**Type:** ConfigurationData  
**Relative Path:** security/data/ir_config_parameter_data.xml  
**Repository Id:** REPO-IGOII-004  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N Integration Configuration Placeholders
    
**Requirement Ids:**
    
    - REQ-IL-008
    
**Purpose:** Provides example records for system parameters if 'ir.config_parameter' is used for storing N8N integration secrets. Emphasizes that this method is less secure for production.  
**Logic Description:** This XML file should contain 'ir.config_parameter' records as examples. For example: '<record id="n8n_webhook_url_param" model="ir.config_parameter"><field name="key">influence_gen.n8n_webhook_url</field><field name="value">PLACEHOLDER_N8N_WEBHOOK_URL</field></record>'. Similarly for 'influence_gen.n8n_api_key' and 'influence_gen.n8n_callback_token'. Add comments stressing that these values should be overridden by environment variables or a proper secrets manager in production environments and not committed with real secrets.  
**Documentation:**
    
    - **Summary:** This file is intended as a placeholder to illustrate how N8N integration parameters *could* be stored if using ir.config_parameter. For production, secure secrets management (environment variables, Odoo secrets, or external vault) is mandated by REQ-IL-008.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  - influence_gen.n8n_webhook_url
  - influence_gen.n8n_api_key
  - influence_gen.n8n_callback_token
  


---

