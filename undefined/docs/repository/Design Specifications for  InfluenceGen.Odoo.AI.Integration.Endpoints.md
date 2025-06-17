# Software Design Specification: InfluenceGen.Odoo.AI.Integration.Endpoints

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the `InfluenceGen.Odoo.AI.Integration.Endpoints` repository (REPO-IGOII-004). This Odoo module is responsible for managing the Odoo-side integration points for the AI Image Generation workflow, facilitating asynchronous communication with an N8N orchestration layer. It handles the initiation of AI image generation requests from Odoo to N8N and processes the results sent back by N8N.

### 1.2 Scope
The scope of this SDS covers:
-   Definition of Odoo controllers to expose a REST API endpoint for N8N callbacks.
-   Definition of Odoo services to initiate requests to N8N webhooks.
-   Logic for parsing N8N responses, storing generated image metadata or error details.
-   Updating the status of AI generation requests within Odoo.
-   Secure handling of API keys and tokens for communication.
-   Adherence to defined API contracts (JSON payloads).

### 1.3 Definitions, Acronyms, and Abbreviations
-   **AI:** Artificial Intelligence
-   **API:** Application Programming Interface
-   **CSRF:** Cross-Site Request Forgery
-   **ETL:** Extract, Transform, Load
-   **HTTP:** Hypertext Transfer Protocol
-   **JSON:** JavaScript Object Notation
-   **N8N:** A free and open-source workflow automation tool.
-   **ORM:** Object-Relational Mapper
-   **OWL:** Odoo Web Library
-   **PII:** Personally Identifiable Information
-   **REST:** Representational State Transfer
-   **SDS:** Software Design Specification
-   **UI:** User Interface
-   **UX:** User Experience
-   **UUID:** Universally Unique Identifier
-   **WCAG:** Web Content Accessibility Guidelines

### 1.4 References
-   Project Requirements Document (Implicitly, via requirement IDs)
-   System Architecture Document (Implicitly, via layer IDs and architectural style)
-   Sequence Diagrams (Specifically `SEQ-AIGS-001` for AI Image Generation Flow, although not explicitly provided here, its logic is inferred from requirements)
-   Odoo 18 Developer Documentation

### 1.5 Overview
This SDS details the design of the Odoo module responsible for AI integration. Section 2 describes the system architecture. Section 3 outlines the detailed design of each component (file) within the repository. Section 4 details API contracts and data structures. Section 5 covers security considerations. Section 6 discusses error handling and logging.

## 2. System Architecture
This module adheres to Odoo's layered architecture and the overall system's LayeredArchitecture style.

-   **Presentation/API Layer:**
    -   `controllers/ai_integration_controller.py`: Exposes REST API endpoints for N8N callbacks.
-   **Business Logic/Service Layer:**
    -   `services/ai_request_service.py`: Handles logic for initiating requests to N8N.
    -   `services/ai_result_service.py`: Handles logic for processing results from N8N.
-   **Utility Layer:**
    -   `utils/security_utils.py`: Provides security-related helper functions.
-   **Configuration:**
    -   `__manifest__.py`: Module definition.
    -   `security/data/ir_config_parameter_data.xml`: Placeholders for system parameters.

This module integrates with an external N8N Orchestration Layer (`REPO-N8NO-005`) and relies on base Odoo models and services, potentially including custom models from `REPO-IGBM-002` (InfluenceGen.Odoo.Base.Models) for entities like `AIImageGenerationRequest` and `GeneratedImage`.

## 3. Detailed Design

### 3.1 `__init__.py`
-   **Purpose:** Initializes the Python package for the Odoo module.
-   **Logic:**
    python
    # odoo_modules/influence_gen_ai_integration/__init__.py
    from . import controllers
    from . import services
    from . import utils 
    # Assuming base models are in a separate module and this one might define its own models or extend them.
    # If this module defines models directly:
    # from . import models 
    
-   **Requirements:** Module Initialization

### 3.2 `__manifest__.py`
-   **Purpose:** Declares the Odoo module, its metadata, dependencies, and data files.
-   **Logic:**
    python
    # odoo_modules/influence_gen_ai_integration/__manifest__.py
    {
        'name': 'InfluenceGen AI Integration Endpoints',
        'version': '18.0.1.0.0',
        'summary': 'Manages Odoo-side integration with N8N for AI image generation.',
        'author': 'SSS-AI',
        'website': 'https_your_company_website.com', # Replace with actual
        'category': 'InfluenceGen/Integrations',
        'license': 'AGPL-3', # Or your chosen license
        'depends': [
            'base',
            'web',
            'mail', # For potential notifications on success/failure
            # Add dependency to the module defining AIImageGenerationRequest, GeneratedImage, etc.
            # e.g., 'influence_gen_base_models' (REPO-IGBM-002)
            # This dependency ensures that the models this module interacts with are loaded.
            # Replace 'influence_gen_base_models' with the actual name of your base models module.
            'influence_gen_base_models', 
        ],
        'data': [
            'security/ir.model.access.csv', # If new models are defined here or for service access
            'security/data/ir_config_parameter_data.xml',
            # Add views if any specific backend configurations are managed through UI
        ],
        'installable': True,
        'application': False, # This is likely a technical/connector module
        'auto_install': False,
    }
    
-   **Requirements:** Module Definition, `REQ-IL-008` (for data file inclusion)

### 3.3 `controllers/__init__.py`
-   **Purpose:** Initializes the Python package for controllers.
-   **Logic:**
    python
    # odoo_modules/influence_gen_ai_integration/controllers/__init__.py
    from . import ai_integration_controller
    
-   **Requirements:** Controller Initialization

### 3.4 `controllers/ai_integration_controller.py`
-   **Purpose:** Handles inbound N8N callback for AI image generation results.
-   **Class:** `AIIntegrationController`
    -   Inherits: `odoo.http.Controller`
-   **Methods:**
    -   `handle_n8n_image_result_callback(self, **kwargs)`
        -   **Decorator:** `@http.route('/influence_gen/ai/callback/image_result', type='json', auth='public', methods=['POST'], csrf=False)`
        -   **Parameters:** `**kwargs` (Odoo typically populates this from the JSON payload if `type='json'`). Alternatively, `http.request.jsonrequest` can be used.
        -   **Returns:** `werkzeug.wrappers.Response` (implicitly via Odoo's JSON response handling)
        -   **Logic:**
            1.  Log reception of the callback with `_logger.info()`.
            2.  Retrieve the N8N callback token from request headers (e.g., `X-N8N-Webhook-Token`) or from the payload itself.
                python
                # Example: Get token from header
                # received_token = http.request.httprequest.headers.get('X-N8N-Webhook-Token')
                # Or from payload if agreed upon
                received_token = kwargs.get('security_token') 
                
            3.  Validate the token using `odoo.addons.influence_gen_ai_integration.utils.security_utils.validate_n8n_callback_token(http.request.env, received_token)`.
            4.  If token is invalid:
                -   Log security warning.
                -   Return `{'status': 'error', 'message': 'Authentication failed'}`, and an appropriate HTTP status code (e.g., 401 or 403, though Odoo's JSON controller might default to 200 with error in body). Explicitly: `return werkzeug.wrappers.Response(json.dumps({'status': 'error', 'message': 'Authentication failed'}), status=401, mimetype='application/json')`.
            5.  Extract `ai_generation_request_id` and the actual result `payload` from `kwargs` (or `http.request.jsonrequest`).
                python
                ai_generation_request_id = kwargs.get('ai_generation_request_id')
                n8n_result_payload = kwargs.get('result_payload') # This should contain status, data/error_data
                if not ai_generation_request_id or not n8n_result_payload:
                    _logger.error("Missing ai_generation_request_id or result_payload in N8N callback.")
                    return {'status': 'error', 'message': 'Missing required fields in callback payload'}
                
            6.  Call the `AIResultService`: `http.request.env['influence_gen.ai_result_service'].sudo().process_n8n_callback(ai_generation_request_id, n8n_result_payload)`. Use `sudo()` if the service needs broader permissions for updates, ensuring security context is managed carefully.
            7.  Log successful processing.
            8.  Return `{'status': 'success'}`.
        -   **Error Handling:**
            -   Use `try...except` blocks for parsing errors, service call errors.
            -   Log detailed errors with `_logger.exception()`.
            -   Return appropriate error responses to N8N (e.g., `{'status': 'error', 'message': 'Internal server error'}`).
-   **Imports:** `odoo.http`, `odoo.addons.influence_gen_ai_integration.utils.security_utils`, `logging`, `json`, `werkzeug`
-   **Logging:** Initialize `_logger = logging.getLogger(__name__)`.
-   **Requirements:** `REQ-IL-003`, `REQ-IL-004`, `REQ-IL-016`, `REQ-AIGS-001`, `REQ-DDSI-009`

### 3.5 `services/__init__.py`
-   **Purpose:** Initializes the Python package for services.
-   **Logic:**
    python
    # odoo_modules/influence_gen_ai_integration/services/__init__.py
    from . import ai_request_service
    from . import ai_result_service
    
-   **Requirements:** Service Initialization

### 3.6 `services/ai_request_service.py`
-   **Purpose:** Initiates AI image generation requests from Odoo to N8N.
-   **Class:** `AIRequestService`
    -   Inherits: `models.AbstractModel`
    -   `_name = 'influence_gen.ai_request_service'`
    -   `_description = 'Service to initiate AI Image Generation Requests to N8N'`
-   **Methods:**
    -   `_get_n8n_webhook_url(self)`:
        -   **Returns:** `str`
        -   **Logic:**
            1.  Retrieve URL from `self.env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_webhook_url')`.
            2.  If not found, log error and raise `UserError` or return `None`.
    -   `_get_n8n_api_key(self)`:
        -   **Returns:** `str`
        -   **Logic:**
            1.  Retrieve API key from `self.env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_api_key')`.
            2.  If not found, log error and raise `UserError` or return `None`.
    -   `initiate_ai_image_generation(self, ai_generation_request_id, generation_params)`:
        -   **Parameters:**
            -   `ai_generation_request_id`: `int` (ID of the `AIImageGenerationRequest` Odoo model record)
            -   `generation_params`: `dict` (containing prompt, negative_prompt, model_id, resolution, etc.)
        -   **Returns:** `bool` (True on successful initiation, False otherwise)
        -   **Logic:**
            1.  Fetch `AIImageGenerationRequest` record: `request_record = self.env['influence_gen.ai_image_request'].sudo().browse(ai_generation_request_id)`. Check if `request_record` exists.
            2.  Get N8N webhook URL and API key using helper methods. If not configured, log error, update `request_record` status to 'initiation_failed', and return `False`.
            3.  Construct Odoo callback URL. This could be a system parameter or constructed dynamically:
                python
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                odoo_callback_url = f"{base_url}/influence_gen/ai/callback/image_result"
                
            4.  Construct JSON payload:
                python
                payload = {
                    'ai_generation_request_id': str(request_record.id), # Ensure it's the UUID if ID is UUID, or int if int
                    'params': generation_params,
                    'odoo_callback_url': odoo_callback_url,
                    'security_token': self.env['ir.config_parameter'].sudo().get_param('influence_gen.odoo_to_n8n_secret_token') # A token Odoo sends that N8N can optionally validate
                }
                
            5.  Prepare headers:
                python
                headers = {
                    'Content-Type': 'application/json',
                    'X-N8N-Api-Key': n8n_api_key # Or other header N8N expects for its webhook auth
                }
                
            6.  Use `requests.post(n8n_webhook_url, json=payload, headers=headers, timeout=10)` (adjust timeout).
            7.  Handle response:
                -   If `response.status_code` is successful (e.g., 200, 202):
                    -   Log successful initiation: `_logger.info(f"Successfully initiated AI request {request_record.id} to N8N.")`
                    -   Update `request_record` status to 'processing' or 'sent_to_n8n'.
                    -   Return `True`.
                -   Else (HTTP error):
                    -   Log error: `_logger.error(f"Failed to initiate AI request {request_record.id} to N8N. Status: {response.status_code}, Response: {response.text}")`
                    -   Update `request_record` status to 'initiation_failed' with error details.
                    -   Return `False`.
            8.  Handle `requests.exceptions.RequestException` (timeout, connection error):
                -   Log error.
                -   Update `request_record` status to 'initiation_failed'.
                -   Return `False`.
-   **Imports:** `odoo.models`, `odoo.exceptions.UserError`, `requests`, `logging`
-   **Logging:** Initialize `_logger = logging.getLogger(__name__)`.
-   **Requirements:** `REQ-IL-002`, `REQ-IL-008`, `REQ-AIGS-001`

### 3.7 `services/ai_result_service.py`
-   **Purpose:** Processes AI image generation results received from N8N.
-   **Class:** `AIResultService`
    -   Inherits: `models.AbstractModel`
    -   `_name = 'influence_gen.ai_result_service'`
    -   `_description = 'Service to process AI Image Generation Results from N8N'`
-   **Methods:**
    -   `_download_and_store_image(self, image_url, request_record, image_metadata)`:
        -   **Parameters:**
            -   `image_url`: `str`
            -   `request_record`: Odoo record of `influence_gen.ai_image_request`
            -   `image_metadata`: `dict` (containing file_format, file_size, width, height from N8N if available)
        -   **Returns:** Odoo record of `influence_gen.generated_image` or `None`
        -   **Logic:**
            1.  Use `requests.get(image_url, stream=True, timeout=60)` (adjust timeout).
            2.  If successful:
                -   Get image content: `image_content = response.content`.
                -   Calculate hash (e.g., SHA256) of `image_content`.
                -   Create `influence_gen.generated_image` record:
                    python
                    # Assuming influence_gen_base_models defines 'influence_gen.generated_image'
                    GeneratedImage = self.env['influence_gen.generated_image'].sudo()
                    # Determine retention_category based on request_record.intendedUse and campaign usage rights if applicable
                    retention_category = 'personal_generation' # Default, adjust based on logic
                    if request_record.campaign_id and request_record.campaign_id.usage_rights:
                        # Logic to determine retention based on campaign usage rights
                        # e.g., retention_category = f"campaign_asset_{request_record.campaign_id.id}" 
                        pass

                    # Store image using ir.attachment (Odoo's standard way)
                    attachment_vals = {
                        'name': f"ai_gen_{request_record.id}_{image_metadata.get('file_format', 'img')}",
                        'datas': base64.b64encode(image_content),
                        'res_model': 'influence_gen.generated_image', 
                        # res_id will be set after GeneratedImage is created, or link differently
                        'mimetype': image_metadata.get('mimetype', 'application/octet-stream'),
                    }
                    attachment = self.env['ir.attachment'].sudo().create(attachment_vals)

                    image_vals = {
                        'request_id': request_record.id,
                        'storage_identifier': str(attachment.id), # Store attachment ID as identifier
                        'storage_type': 'ir.attachment', # Indicate storage method
                        'file_format': image_metadata.get('file_format'),
                        'file_size': image_metadata.get('file_size', len(image_content)),
                        'width': image_metadata.get('width'),
                        'height': image_metadata.get('height'),
                        'hash_value': hashlib.sha256(image_content).hexdigest(),
                        'retention_category': retention_category, 
                        # 'usage_rights': ... derived from campaign or default
                    }
                    generated_image_record = GeneratedImage.create(image_vals)
                    attachment.write({'res_id': generated_image_record.id}) # Link attachment to the image record
                    _logger.info(f"Image stored for request {request_record.id}, attachment ID: {attachment.id}")
                    return generated_image_record
                    
            3.  If download fails, log error and return `None`.
    -   `_handle_successful_generation(self, request_record, success_data)`:
        -   **Logic:**
            1.  Extract `image_url`, `image_data` (if direct binary), `file_format`, `file_size`, `width`, `height` from `success_data`.
            2.  If `image_url`:
                -   `generated_image_record = self._download_and_store_image(image_url, request_record, success_data)`
            3.  Else if `image_data` (base64 encoded binary):
                -   Decode `image_data`.
                -   Create `GeneratedImage` record and `ir.attachment` similarly to `_download_and_store_image`.
            4.  If `generated_image_record`:
                -   Update `request_record` status to 'completed', link `generated_image_id = generated_image_record.id`.
            5.  Else (image storage failed):
                -   Update `request_record` status to 'failed' with error "Image processing/storage failed".
    -   `_handle_failed_generation(self, request_record, error_data)`:
        -   **Logic:**
            1.  Extract error message/details from `error_data`.
            2.  Log the detailed error.
            3.  Update `request_record` status to 'failed', storing a user-friendly error summary in `request_record.error_details`.
    -   `process_n8n_callback(self, ai_generation_request_id_str, n8n_payload)`:
        -   **Parameters:**
            -   `ai_generation_request_id_str`: `str` (UUID or ID of the `AIImageGenerationRequest` record)
            -   `n8n_payload`: `dict` (parsed JSON from N8N)
        -   **Logic:**
            1.  Find `AIImageGenerationRequest` record:
                python
                # Assuming ID is stored as a string UUID in N8N payload
                # If your model's ID is an integer, adjust accordingly
                try:
                    # If request ID from N8N is an integer
                    # request_id_int = int(ai_generation_request_id_str)
                    # request_record = self.env['influence_gen.ai_image_request'].sudo().browse(request_id_int)

                    # If request ID is a UUID string (assuming model uses UUIDs or has a specific field for it)
                    # Example: find by a custom UUID field if not Odoo's default int ID
                    request_record = self.env['influence_gen.ai_image_request'].sudo().search([('uuid_field_name', '=', ai_generation_request_id_str)], limit=1)
                    # OR if the ai_generation_request_id_str is the Odoo integer ID passed as string
                    # request_record = self.env['influence_gen.ai_image_request'].sudo().browse(int(ai_generation_request_id_str))

                except ValueError: # Handle if ID is not convertible to int, if applicable
                    _logger.error(f"Invalid ai_generation_request_id format: {ai_generation_request_id_str}")
                    return # Or raise error

                if not request_record:
                    _logger.error(f"AIImageGenerationRequest not found for ID: {ai_generation_request_id_str}")
                    return # Or raise specific error
                
            2.  Validate `n8n_payload` structure (presence of 'status', 'data' or 'error_data').
            3.  If `n8n_payload.get('status') == 'success'`:
                -   Call `self._handle_successful_generation(request_record, n8n_payload.get('data', {}))`.
            4.  Else (status is 'failure' or unknown):
                -   Call `self._handle_failed_generation(request_record, n8n_payload.get('error_data', {}))`.
            5.  Consider sending a notification to the user via Odoo Bus or `mail.thread` post_message on `request_record`.
-   **Imports:** `odoo.models`, `requests`, `base64`, `hashlib`, `logging`
-   **Logging:** Initialize `_logger = logging.getLogger(__name__)`.
-   **Requirements:** `REQ-IL-003`, `REQ-IL-010`, `REQ-AIGS-001`

### 3.8 `utils/__init__.py`
-   **Purpose:** Initializes the Python package for utility functions.
-   **Logic:**
    python
    # odoo_modules/influence_gen_ai_integration/utils/__init__.py
    from . import security_utils
    
-   **Requirements:** Utility Initialization

### 3.9 `utils/security_utils.py`
-   **Purpose:** Provides security-related utility functions.
-   **Methods:**
    -   `validate_n8n_callback_token(odoo_env, received_token)`:
        -   **Parameters:**
            -   `odoo_env`: Odoo environment object (`self.env` from a model/service or `http.request.env` from controller).
            -   `received_token`: `str`
        -   **Returns:** `bool`
        -   **Logic:**
            1.  Fetch expected token: `expected_token = odoo_env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_callback_token')`.
            2.  If `expected_token` is not configured or `received_token` is `None`, log error and return `False`.
            3.  Use `hmac.compare_digest(str(received_token).encode('utf-8'), str(expected_token).encode('utf-8'))` for secure comparison.
            4.  Log validation attempt result (success/failure, but not the tokens themselves in case of failure if too verbose).
            5.  Return comparison result.
-   **Imports:** `hmac`, `logging`
-   **Logging:** Initialize `_logger = logging.getLogger(__name__)`.
-   **Requirements:** `REQ-IL-016`, `REQ-IL-008`

### 3.10 `security/data/ir_config_parameter_data.xml`
-   **Purpose:** Example data for Odoo system parameters for N8N integration.
-   **Logic:**
    xml
    <!-- odoo_modules/influence_gen_ai_integration/security/data/ir_config_parameter_data.xml -->
    <odoo>
        <data noupdate="1"> <!-- noupdate="1" to prevent overriding on module update after initial setup -->
            
            <!-- 
                IMPORTANT: These are placeholders. In a production environment,
                these sensitive values should be set via environment variables,
                Odoo's secrets management, or an external vault, NOT committed
                to version control with real values. This file serves as a template
                for required configuration keys.
                REQ-IL-008 mandates secure credential storage.
            -->

            <record id="n8n_webhook_url_param" model="ir.config_parameter">
                <field name="key">influence_gen.n8n_webhook_url</field>
                <field name="value">PLACEHOLDER_YOUR_N8N_WEBHOOK_URL_FOR_AI_GENERATION</field>
            </record>

            <record id="n8n_api_key_param" model="ir.config_parameter">
                <field name="key">influence_gen.n8n_api_key</field>
                <field name="value">PLACEHOLDER_YOUR_N8N_API_KEY_FOR_ODOO_TO_CALL_N8N</field>
            </record>

            <record id="n8n_callback_token_param" model="ir.config_parameter">
                <field name="key">influence_gen.n8n_callback_token</field>
                <field name="value">PLACEHOLDER_A_STRONG_SHARED_SECRET_FOR_N8N_TO_CALL_ODOO</field>
            </record>

             <record id="odoo_to_n8n_secret_token_param" model="ir.config_parameter">
                <field name="key">influence_gen.odoo_to_n8n_secret_token</field>
                <field name="value">PLACEHOLDER_A_STRONG_SHARED_SECRET_FOR_ODOO_TO_CALL_N8N_WEBHOOKS</field>
            </record>

        </data>
    </odoo>
    
-   **Requirements:** `REQ-IL-008` (as a placeholder mechanism)

### 3.11 `security/ir.model.access.csv` (New File)
-   **Purpose:** Defines access rights for any models or services this module might expose if not purely abstract. For abstract services, access is typically handled by the calling code's permissions. However, if specific groups need to trigger AI requests or manage configurations through UI exposed by this module, ACLs would be needed. Given the current design focuses on backend services and a public callback, direct model ACLs might be minimal for this specific module unless it defines its own non-abstract models. Service models (`models.AbstractModel`) don't typically require `ir.model.access.csv` entries themselves, as their methods are called programmatically by other Odoo components (controllers, other models) which have their own security context.
-   **Example (if there were configuration models managed via UI):**
    csv
    id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
    # access_influence_gen_ai_config_admin,influence_gen.ai.config.admin,model_influence_gen_ai_config,base.group_system,1,1,1,1 
    
-   **Note:** Based on the current file structure, this module primarily provides services and controllers. If `AIImageGenerationRequest` and `GeneratedImage` are defined in `influence_gen_base_models`, their ACLs would be there. Access to `ir.config_parameter` is typically restricted to `base.group_system`. The public callback endpoint has custom token auth. The services are called internally.

## 4. API Contracts and Data Structures

### 4.1 Odoo to N8N (Request Initiation)
-   **Endpoint:** N8N Webhook URL (fetched from `influence_gen.n8n_webhook_url`)
-   **Method:** POST
-   **Headers:**
    -   `Content-Type: application/json`
    -   `X-N8N-Api-Key: <n8n_api_key>` (or other N8N-defined auth header)
-   **Body (JSON):**
    json
    {
        "ai_generation_request_id": "string (Odoo's AIImageGenerationRequest record ID/UUID)",
        "params": {
            "prompt": "string",
            "negative_prompt": "string (optional)",
            "model_id": "string (identifier for the AI model, e.g., AIImageModel record ID/UUID or external ID)",
            "resolution": "string (e.g., '1024x1024')",
            "aspect_ratio": "string (e.g., '1:1')",
            "seed": "integer (optional)",
            "inference_steps": "integer (optional)",
            "cfg_scale": "float (optional)"
            // ... any other parameters supported by the AI service
        },
        "odoo_callback_url": "string (URL for N8N to call back, e.g., https://your.odoo.instance/influence_gen/ai/callback/image_result)",
        "security_token": "string (A secret token Odoo sends to N8N for optional validation by N8N if N8N webhook is public but wants to verify source)"
    }
    

### 4.2 N8N to Odoo (Result Callback)
-   **Endpoint:** `/influence_gen/ai/callback/image_result` (on Odoo instance)
-   **Method:** POST
-   **Headers:**
    -   `Content-Type: application/json`
    -   `X-N8N-Webhook-Token: <shared_secret_token>` (or token in payload)
-   **Body (JSON):**
    json
    // Success Case
    {
        "ai_generation_request_id": "string (Odoo's AIImageGenerationRequest record ID/UUID)",
        "security_token": "string (shared secret for Odoo to validate the callback)",
        "result_payload": {
            "status": "success",
            "data": {
                "image_url": "string (URL to the generated image, if N8N provides a temporary link)", 
                // OR "image_data": "string (base64 encoded image binary, if N8N sends data directly)"
                "file_format": "string (e.g., 'png', 'jpeg')",
                "file_size": "integer (bytes, optional if URL provided and Odoo fetches size)",
                "width": "integer (pixels, optional)",
                "height": "integer (pixels, optional)",
                "mimetype": "string (e.g., 'image/png')"
                // ... any other relevant metadata from AI service
            }
        }
    }

    // Failure Case
    {
        "ai_generation_request_id": "string (Odoo's AIImageGenerationRequest record ID/UUID)",
        "security_token": "string (shared secret for Odoo to validate the callback)",
        "result_payload": {
            "status": "failure",
            "error_data": {
                "message": "string (Error message from AI service or N8N workflow)",
                "details": "string (Optional additional error details)"
            }
        }
    }
    

## 5. Security Considerations

-   **N8N Webhook Authentication (Odoo to N8N):** The N8N webhook called by Odoo should be secured. This is typically done by N8N requiring an API key or a specific header that Odoo includes in its request. This key (`influence_gen.n8n_api_key`) must be stored securely in Odoo.
-   **Odoo Callback Authentication (N8N to Odoo):** The Odoo callback endpoint (`/influence_gen/ai/callback/image_result`) is `auth='public'` but implements custom token validation (`security_utils.validate_n8n_callback_token`). This shared secret (`influence_gen.n8n_callback_token`) must be strong and known only to Odoo and the N8N workflow.
-   **Secure Credential Storage (`REQ-IL-008`):**
    -   `ir.config_parameter` is used as a placeholder mechanism as per the file structure.
    -   **Production Mandate:** In production, these parameters (`influence_gen.n8n_webhook_url`, `influence_gen.n8n_api_key`, `influence_gen.n8n_callback_token`, `influence_gen.odoo_to_n8n_secret_token`) **MUST NOT** store actual secrets if the `ir_config_parameter_data.xml` is part of the committed code. They should be overridden by environment variables or Odoo's enterprise secrets management features. The code accessing these parameters should be able to fall back to environment variables if `ir.config_parameter` yields a placeholder.
-   **Input Validation:** The N8N callback controller should validate the presence of expected fields in the JSON payload.
-   **HTTPS:** All communication between Odoo, N8N, and AI services must use HTTPS/TLS (`REQ-IL-007`, though enforced at infrastructure level).
-   **CSRF Protection:** Disabled for the JSON callback endpoint (`csrf=False`) as it's an API endpoint, not a form submission from a browser session. Token authentication serves a similar purpose for API-to-API calls.

## 6. Error Handling and Logging

-   **`ai_request_service.py`:**
    -   Log initiation attempts, payload (mask sensitive data if logged), and N8N's immediate HTTP response.
    -   Handle `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, and other `requests.exceptions.RequestException`.
    -   Handle non-2xx HTTP responses from N8N.
    -   Update `AIImageGenerationRequest` status to 'initiation_failed' with error details.
-   **`ai_integration_controller.py`:**
    -   Log all incoming callback requests (headers can be selectively logged for debugging, but be cautious with tokens).
    -   Log token validation failures.
    -   Catch exceptions during payload parsing or calls to `ai_result_service`.
    -   Return structured JSON error responses to N8N.
-   **`ai_result_service.py`:**
    -   Log processing of successful and failed generation results.
    -   Handle errors during image download (`requests` exceptions), file processing (e.g., base64 decoding, hashing), and database operations (ORM errors).
    -   Update `AIImageGenerationRequest` status to 'failed' with appropriate error messages stored in the record.
-   **General Logging:**
    -   Use Odoo's standard `logging` module: `_logger = logging.getLogger(__name__)`.
    -   Include contextual information in logs (e.g., `ai_generation_request_id`).

## 7. Dependencies on Other Repositories/Modules
-   **`REPO-IGBM-002` (InfluenceGen.Odoo.Base.Models) (Assumed):** This module relies on models like `influence_gen.ai_image_request` and `influence_gen.generated_image` being defined in a base models module. The manifest `depends` section should list this base module.
-   **`REPO-N8NO-005` (InfluenceGen.N8N.Orchestration.Workflows):** This module defines the N8N-side workflows that this Odoo module interacts with. API contracts and authentication mechanisms must be aligned.

## 8. Data Storage for Images (`REQ-IL-010`)
-   The `ai_result_service` will handle storing the image.
-   The primary method described is using Odoo's standard `ir.attachment` model.
    -   `datas`: Base64 encoded image content.
    -   `name`: Generated name for the attachment.
    -   `res_model`: `'influence_gen.generated_image'`
    -   `res_id`: ID of the `influence_gen.generated_image` record.
    -   `mimetype`: Image MIME type.
-   The `influence_gen.generated_image` record will store metadata and a reference (`storage_identifier` = attachment ID, `storage_type` = `'ir.attachment'`) to this `ir.attachment`.
-   This approach leverages Odoo's built-in file storage capabilities (which can be configured to use database or S3-like external storage at the Odoo infrastructure level).

## 9. Configuration Parameters
The following system parameters (`ir.config_parameter`) are used:
-   `influence_gen.n8n_webhook_url`: URL of the N8N webhook for Odoo to initiate AI generation.
-   `influence_gen.n8n_api_key`: API key for Odoo to authenticate with the N8N webhook (if N8N webhook is secured this way).
-   `influence_gen.n8n_callback_token`: Shared secret for N8N to include in callbacks, validated by Odoo.
-   `influence_gen.odoo_to_n8n_secret_token`: Shared secret for Odoo to include in its call to N8N webhook, for N8N to optionally validate. (Added for symmetry and enhanced security).

As per `REQ-IL-008`, these should be placeholders in the XML and actual values set securely in production.

# AI Instructions for Code Generation

1.  **General Instructions:**
    *   Generate code for Odoo 18 using Python 3.11.9.
    *   Ensure all Python files include `_logger = logging.getLogger(__name__)` for logging.
    *   Adhere to Odoo development guidelines (e.g., use of ORM, service layers, controller patterns).
    *   Implement comprehensive error handling using `try...except` blocks and log exceptions.
    *   All user-facing strings that might need translation should be wrapped (e.g., `_("Message")` in Python, `t-esc` in QWeb if views were involved, though this module is backend-focused).
    *   Generate necessary import statements in all Python files.
    *   Assume models `influence_gen.ai_image_request` and `influence_gen.generated_image` are defined in a prerequisite module like `influence_gen_base_models` and are accessible via `self.env['model.name']`. The `AIImageGenerationRequest` model should have fields like `status` (selection: queued, processing, completed, failed, initiation_failed), `error_details` (Text), `generated_image_id` (Many2one to `influence_gen.generated_image`), `campaign_id` (Many2one), `intended_use` (Selection). The `GeneratedImage` model should have fields as described in `ai_result_service._download_and_store_image`.

2.  **File: `__init__.py`**
    *   Generate the content as specified in SDS 3.1.

3.  **File: `__manifest__.py`**
    *   Generate the content as specified in SDS 3.2. Ensure the `depends` key includes `'influence_gen_base_models'` (or the correct name of the module defining the core AI request/result models).
    *   Include `security/ir.model.access.csv` in the `data` list if it becomes necessary (though likely not for this specific service-oriented module if it defines no new user-interactable models).
    *   Add `security/data/ir_config_parameter_data.xml` to the `data` list.

4.  **File: `controllers/__init__.py`**
    *   Generate the content as specified in SDS 3.3.

5.  **File: `controllers/ai_integration_controller.py`**
    *   Implement the `AIIntegrationController` class as detailed in SDS 3.4.
    *   Pay close attention to the route definition, `auth='public'`, `type='json'`, `csrf=False`, and `methods=['POST']`.
    *   Implement the token validation logic by calling `security_utils.validate_n8n_callback_token`.
    *   Ensure the JSON response structure to N8N is `{'status': 'success'}` or `{'status': 'error', 'message': '...'}`.
    *   Use `http.request.env['influence_gen.ai_result_service'].sudo().process_n8n_callback(...)`.

6.  **File: `services/__init__.py`**
    *   Generate the content as specified in SDS 3.5.

7.  **File: `services/ai_request_service.py`**
    *   Implement the `AIRequestService` class (`models.AbstractModel`) as detailed in SDS 3.6.
    *   Implement `_get_n8n_webhook_url` and `_get_n8n_api_key` to fetch from `ir.config_parameter`.
    *   In `initiate_ai_image_generation`:
        *   Fetch the `influence_gen.ai_image_request` record.
        *   Construct the Odoo callback URL dynamically using `web.base.url`.
        *   Construct the JSON payload as specified in SDS 4.1, including a `security_token` for N8N (fetched from `influence_gen.odoo_to_n8n_secret_token`).
        *   Use the `requests` library for the POST call, including headers.
        *   Handle timeouts (`requests.exceptions.Timeout`) and connection errors (`requests.exceptions.ConnectionError`).
        *   Update the status of the `influence_gen.ai_image_request` record appropriately (`processing`, `initiation_failed`).

8.  **File: `services/ai_result_service.py`**
    *   Implement the `AIResultService` class (`models.AbstractModel`) as detailed in SDS 3.7.
    *   In `process_n8n_callback`:
        *   Correctly look up the `influence_gen.ai_image_request` record using the provided `ai_generation_request_id_str`. Adapt search/browse based on whether the ID is an integer or a string UUID.
        *   Delegate to `_handle_successful_generation` or `_handle_failed_generation` based on `n8n_payload['status']`.
    *   In `_handle_successful_generation`:
        *   Parse `success_data` for image details.
        *   Call `_download_and_store_image` if `image_url` is present. If `image_data` (base64 binary) is present, decode and store directly.
        *   Link the created `influence_gen.generated_image` record to the `request_record`.
        *   Update `request_record.status` to `'completed'`.
    *   In `_download_and_store_image`:
        *   Use `requests.get()` to download.
        *   Create an `ir.attachment` record for the image.
        *   Create a `influence_gen.generated_image` record, storing the `attachment.id` in `storage_identifier` and `storage_type = 'ir.attachment'`. Also store `hash_value`, `file_format`, `file_size`, `width`, `height`, and `retention_category`.
        *   Link the `ir.attachment` to the `influence_gen.generated_image` record by setting `res_model` and `res_id` on the attachment.
    *   In `_handle_failed_generation`:
        *   Update `request_record.status` to `'failed'` and store `error_data['message']` in `request_record.error_details`.

9.  **File: `utils/__init__.py`**
    *   Generate the content as specified in SDS 3.8.

10. **File: `utils/security_utils.py`**
    *   Implement `validate_n8n_callback_token` as detailed in SDS 3.9.
    *   Use `hmac.compare_digest` for token comparison.
    *   Fetch the expected token from `odoo_env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_callback_token')`.

11. **File: `security/data/ir_config_parameter_data.xml`**
    *   Generate the XML content as specified in SDS 3.10, including placeholders for `influence_gen.n8n_webhook_url`, `influence_gen.n8n_api_key`, `influence_gen.n8n_callback_token`, and `influence_gen.odoo_to_n8n_secret_token`.
    *   Include prominent comments about production security for these parameters.
    *   Use `noupdate="1"` for the `<data>` tag.

12. **File: `security/ir.model.access.csv` (Optional - create if needed)**
    *   If any new, non-abstract models are defined directly within this module that require specific user group access via the UI (unlikely given the service nature), create this file. For now, assume it's not strictly needed for the described service/controller structure. If services need to be callable by specific groups via XML-RPC or other means, specific access rules might be defined elsewhere or through `ir.rule`. For internal service calls, the calling user's permissions usually apply. The public controller has its own auth. System parameters are typically admin-only.