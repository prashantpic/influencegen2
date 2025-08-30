# Specification

# 1. Files

- **Path:** odoo_modules/influence_gen_shared_core/__manifest__.py  
**Description:** Odoo module manifest file for InfluenceGen Shared Core Utilities. Defines module metadata, dependencies, and data files.  
**Template:** Odoo Manifest Template  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Configuration  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    
**Requirement Ids:**
    
    
**Purpose:** Declares the Odoo module, its version, author, dependencies on other Odoo modules (e.g. base), and lists data files to load.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'category', 'depends', 'data', 'installable', 'application'. 'depends' should include 'base'.  
**Documentation:**
    
    - **Summary:** Standard Odoo manifest file. Specifies dependencies, version, and identifies the module to Odoo.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** ModuleConfiguration
    
- **Path:** odoo_modules/influence_gen_shared_core/__init__.py  
**Description:** Root __init__.py file for the InfluenceGen Shared Core Utilities Odoo module. Imports sub-packages like const, exceptions, models, and utils.  
**Template:** Python Package Init  
**Dependancy Level:** 3  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** __init__.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'influence_gen_shared_core' Python package, making its sub-modules and utilities accessible.  
**Logic Description:** Contains import statements for the 'const', 'exceptions', 'models', and 'utils' sub-packages. For example: from . import const; from . import exceptions; from . import models; from . import utils.  
**Documentation:**
    
    - **Summary:** Initializes the main Odoo module package, making sub-packages available for import by other modules.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_shared_core/const/__init__.py  
**Description:** __init__.py for the 'const' sub-package. Imports constants defined within this package.  
**Template:** Python Package Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** const/__init__.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Constants Package Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'const' sub-package, making constant definitions available.  
**Logic Description:** Imports specific constants or modules from within the 'const' package. For example: from . import influence_gen_constants.  
**Documentation:**
    
    - **Summary:** Makes constants defined in the 'const' sub-package accessible.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.const  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_shared_core/const/influence_gen_constants.py  
**Description:** Defines shared constants for the InfluenceGen platform. Includes business-specific statuses, rule identifiers, or common string literals.  
**Template:** Python Constants Module  
**Dependancy Level:** 0  
**Name:** influence_gen_constants  
**Type:** Constants  
**Relative Path:** const/influence_gen_constants.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** KYC_STATUS_PENDING  
**Type:** str  
**Attributes:** final  
    - **Name:** KYC_STATUS_APPROVED  
**Type:** str  
**Attributes:** final  
    - **Name:** LOG_SEVERITY_INFO  
**Type:** str  
**Attributes:** final  
    - **Name:** DEFAULT_CORRELATION_ID_HEADER  
**Type:** str  
**Attributes:** final  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Shared Constants Definition
    
**Requirement Ids:**
    
    
**Purpose:** Provides a centralized location for platform-wide constants, promoting consistency and avoiding magic strings/numbers.  
**Logic Description:** Defines various constants as Python variables. For example: KYC_STATUS_PENDING = 'pending'; DEFAULT_AI_IMAGE_RESOLUTION = '1024x1024'. Use descriptive names reflecting ubiquitous language.  
**Documentation:**
    
    - **Summary:** Contains global constants used across InfluenceGen modules, such as KYC statuses, campaign statuses, default values, etc.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.const  
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** odoo_modules/influence_gen_shared_core/exceptions/__init__.py  
**Description:** __init__.py for the 'exceptions' sub-package. Imports custom exception classes.  
**Template:** Python Package Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** exceptions/__init__.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Exceptions Package Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'exceptions' sub-package, making custom exception classes available.  
**Logic Description:** Imports custom exception classes defined within this package. For example: from .custom_exceptions import ValidationException, IntegrationException.  
**Documentation:**
    
    - **Summary:** Makes custom exception classes defined in the 'exceptions' sub-package accessible.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.exceptions  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_shared_core/exceptions/custom_exceptions.py  
**Description:** Defines custom exception classes for the InfluenceGen platform to handle specific error conditions.  
**Template:** Python Exceptions Module  
**Dependancy Level:** 0  
**Name:** custom_exceptions  
**Type:** Exception  
**Relative Path:** exceptions/custom_exceptions.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Error Handling
    
**Requirement Ids:**
    
    
**Purpose:** Provides a set of domain-specific exceptions for improved error handling and clarity across modules.  
**Logic Description:** Define custom exception classes inheriting from Python's base `Exception` or more specific Odoo exceptions like `UserError`. Examples: class InfluenceGenValidationException(UserError): pass; class InfluenceGenIntegrationException(Exception): pass.  
**Documentation:**
    
    - **Summary:** Contains custom exception classes like ValidationException, APICallException, etc., used for standardized error reporting.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.exceptions  
**Metadata:**
    
    - **Category:** ErrorHandling
    
- **Path:** odoo_modules/influence_gen_shared_core/utils/__init__.py  
**Description:** __init__.py for the 'utils' sub-package. Imports utility modules for validation, logging, etc.  
**Template:** Python Package Init  
**Dependancy Level:** 1  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** utils/__init__.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Utilities Package Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'utils' sub-package, making various utility functions available.  
**Logic Description:** Imports utility modules like validation_utils, logging_utils, etc. For example: from . import validation_utils; from . import logging_utils.  
**Documentation:**
    
    - **Summary:** Makes utility modules defined in the 'utils' sub-package accessible.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.utils  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_shared_core/utils/validation_utils.py  
**Description:** Provides reusable data validation utility functions beyond standard Odoo constraints. Implements format, range, and length validations.  
**Template:** Python Utility Module  
**Dependancy Level:** 1  
**Name:** validation_utils  
**Type:** Utility  
**Relative Path:** utils/validation_utils.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** is_valid_email  
**Parameters:**
    
    - email_string: str
    
**Return Type:** bool  
**Attributes:** public static  
    - **Name:** is_valid_url  
**Parameters:**
    
    - url_string: str
    - schemes: list = None
    
**Return Type:** bool  
**Attributes:** public static  
    - **Name:** is_valid_phone_number  
**Parameters:**
    
    - phone_string: str
    - country_code: str = None
    
**Return Type:** bool  
**Attributes:** public static  
    - **Name:** is_valid_date_format  
**Parameters:**
    
    - date_string: str
    - date_format: str
    
**Return Type:** bool  
**Attributes:** public static  
    - **Name:** is_within_range  
**Parameters:**
    
    - value: Union[int, float]
    - min_val: Union[int, float, None]
    - max_val: Union[int, float, None]
    
**Return Type:** bool  
**Attributes:** public static  
    - **Name:** is_valid_length  
**Parameters:**
    
    - text: str
    - min_len: int = None
    - max_len: int = None
    
**Return Type:** bool  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Email Validation
    - URL Validation
    - Phone Number Validation
    - Date Format Validation
    - Numeric Range Validation
    - String Length Validation
    
**Requirement Ids:**
    
    - REQ-DMG-014
    
**Purpose:** Offers common data validation routines to ensure data integrity across various InfluenceGen modules.  
**Logic Description:** Implement functions using regular expressions or Python libraries (e.g., 'validators', 'phonenumbers') for format checks. Range and length checks are straightforward comparisons. Functions should return boolean and not raise exceptions directly, allowing calling code to handle validation failures as needed (or raise specific custom exceptions from exceptions.py).  
**Documentation:**
    
    - **Summary:** Contains helper functions for validating common data formats (email, URL, phone), numeric ranges, and string lengths as per REQ-DMG-014.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_shared_core/utils/logging_utils.py  
**Description:** Provides standardized logging wrappers to ensure consistent log formats, context propagation (correlation IDs), and structured logging (JSON).  
**Template:** Python Utility Module  
**Dependancy Level:** 1  
**Name:** logging_utils  
**Type:** Utility  
**Relative Path:** utils/logging_utils.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_logger  
**Parameters:**
    
    - name: str
    
**Return Type:** logging.Logger  
**Attributes:** public static  
    - **Name:** format_log_message_json  
**Parameters:**
    
    - message: str
    - level: str
    - user_id: int = None
    - request_id: str = None
    - correlation_id: str = None
    - extra_context: dict = None
    
**Return Type:** str  
**Attributes:** public static  
    - **Name:** log_info_structured  
**Parameters:**
    
    - logger: logging.Logger
    - message: str
    - user_id: int = None
    - request_id: str = None
    - correlation_id: str = None
    - extra_context: dict = None
    
**Return Type:** void  
**Attributes:** public static  
    - **Name:** log_error_structured  
**Parameters:**
    
    - logger: logging.Logger
    - message: str
    - exc_info: bool = False
    - user_id: int = None
    - request_id: str = None
    - correlation_id: str = None
    - extra_context: dict = None
    
**Return Type:** void  
**Attributes:** public static  
    - **Name:** get_correlation_id  
**Parameters:**
    
    - request_opt = None
    
**Return Type:** str  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Structured JSON Logging
    - Correlation ID Handling
    - Contextual Logging
    
**Requirement Ids:**
    
    - REQ-ATEL-002
    
**Purpose:** Encapsulates logging logic to enforce standardized, structured logging practices across all InfluenceGen modules.  
**Logic Description:** The `get_logger` method should return a standard Python logger. `format_log_message_json` constructs a JSON string with UTC timestamp, level, message, and all contextual IDs. `log_info_structured` and `log_error_structured` use this formatter to log. `get_correlation_id` attempts to retrieve a correlation ID from the current request context (e.g., Odoo request headers or environment) or generates a new one if not found. Ensure UTC timestamps are used by default in loggers.  
**Documentation:**
    
    - **Summary:** Contains utility functions for creating structured (JSON) log messages including UTC timestamps, correlation IDs, user IDs, and other context as per REQ-ATEL-002.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_shared_core/utils/data_transformation_utils.py  
**Description:** Contains helper functions for specific, common data transformations required across InfluenceGen modules.  
**Template:** Python Utility Module  
**Dependancy Level:** 1  
**Name:** data_transformation_utils  
**Type:** Utility  
**Relative Path:** utils/data_transformation_utils.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** clean_text_input  
**Parameters:**
    
    - text: str
    
**Return Type:** str  
**Attributes:** public static  
    - **Name:** normalize_social_media_handle  
**Parameters:**
    
    - handle: str
    - platform: str
    
**Return Type:** str  
**Attributes:** public static  
    - **Name:** convert_to_utc_datetime  
**Parameters:**
    
    - dt_value: Union[str, datetime.date, datetime.datetime]
    
**Return Type:** datetime.datetime  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Text Cleaning
    - Social Media Handle Normalization
    - Datetime UTC Conversion
    
**Requirement Ids:**
    
    
**Purpose:** Provides reusable functions for common data cleaning, normalization, or conversion tasks.  
**Logic Description:** `clean_text_input` could remove leading/trailing whitespace, excessive spaces. `normalize_social_media_handle` might remove '@' symbols or convert to lowercase depending on platform conventions. `convert_to_utc_datetime` ensures datetime objects are in UTC.  
**Documentation:**
    
    - **Summary:** Offers helper functions for common data transformations, such as text cleaning or date conversions, to maintain consistency.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_shared_core/utils/security_utils.py  
**Description:** Provides utility functions related to security, such as secure credential retrieval wrappers.  
**Template:** Python Utility Module  
**Dependancy Level:** 1  
**Name:** security_utils  
**Type:** Utility  
**Relative Path:** utils/security_utils.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** get_secret_from_vault  
**Parameters:**
    
    - secret_name: str
    - vault_config: dict = None
    
**Return Type:** Optional[str]  
**Attributes:** public static  
    - **Name:** hash_data_sha256  
**Parameters:**
    
    - data: str
    
**Return Type:** str  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Secure Credential Retrieval
    - Data Hashing
    
**Requirement Ids:**
    
    
**Purpose:** Centralizes security-related utility functions, promoting secure practices for accessing sensitive information.  
**Logic Description:** `get_secret_from_vault` acts as a wrapper to retrieve secrets from Odoo's `ir.config_parameter` (if encrypted there) or an external vault if integrated. It should abstract the specific retrieval mechanism. `hash_data_sha256` provides a consistent way to hash data.  
**Documentation:**
    
    - **Summary:** Contains utility functions for security-sensitive operations, like wrappers for securely retrieving API keys or other credentials from Odoo's configuration or a secrets vault.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_shared_core/utils/misc_utils.py  
**Description:** A collection of miscellaneous general-purpose utility functions that don't fit into more specific utility modules.  
**Template:** Python Utility Module  
**Dependancy Level:** 1  
**Name:** misc_utils  
**Type:** Utility  
**Relative Path:** utils/misc_utils.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** generate_unique_code  
**Parameters:**
    
    - length: int = 8
    
**Return Type:** str  
**Attributes:** public static  
    - **Name:** get_current_env_value  
**Parameters:**
    
    - env_key: str
    - default_value: Any = None
    
**Return Type:** Any  
**Attributes:** public static  
    
**Implemented Features:**
    
    - Unique Code Generation
    - Environment Variable Access
    
**Requirement Ids:**
    
    
**Purpose:** Provides a collection of small, reusable helper functions for common tasks not covered elsewhere.  
**Logic Description:** `generate_unique_code` could create random alphanumeric codes for various purposes. `get_current_env_value` abstracts access to environment variables or Odoo parameters for configuration that might vary by environment.  
**Documentation:**
    
    - **Summary:** Includes miscellaneous helper functions that are broadly applicable across the InfluenceGen modules.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** odoo_modules/influence_gen_shared_core/models/__init__.py  
**Description:** __init__.py for the 'models' sub-package. Imports base model mixins or abstract models.  
**Template:** Python Package Init  
**Dependancy Level:** 2  
**Name:** __init__  
**Type:** PackageInitializer  
**Relative Path:** models/__init__.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Models Package Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'models' sub-package, making base mixins or abstract models available.  
**Logic Description:** Imports model files from within the 'models' package. For example: from . import base_model_mixin.  
**Documentation:**
    
    - **Summary:** Makes shared Odoo model mixins or abstract base classes defined in the 'models' sub-package accessible.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.models  
**Metadata:**
    
    - **Category:** ModuleStructure
    
- **Path:** odoo_modules/influence_gen_shared_core/models/base_model_mixin.py  
**Description:** Defines base model mixins providing common fields or methods for InfluenceGen Odoo models.  
**Template:** Odoo Model Mixin  
**Dependancy Level:** 2  
**Name:** base_model_mixin  
**Type:** ModelMixin  
**Relative Path:** models/base_model_mixin.py  
**Repository Id:** REPO-IGSCU-007  
**Pattern Ids:**
    
    - MixinPattern
    
**Members:**
    
    - **Name:** correlation_id  
**Type:** fields.Char  
**Attributes:** readonly  
    - **Name:** created_by_influence_gen_user_id  
**Type:** fields.Many2one('res.users')  
**Attributes:** readonly  
    
**Methods:**
    
    - **Name:** _get_current_correlation_id  
**Parameters:**
    
    - self
    
**Return Type:** str  
**Attributes:** protected  
    - **Name:** _log_structured_activity  
**Parameters:**
    
    - self
    - message: str
    - level: str = 'INFO'
    - extra_context: dict = None
    
**Return Type:** void  
**Attributes:** protected  
    
**Implemented Features:**
    
    - Common Model Fields
    - Shared Model Methods
    - Standardized Logging from Models
    
**Requirement Ids:**
    
    - REQ-ATEL-002
    
**Purpose:** Provides reusable model components (fields and methods) to be inherited by other InfluenceGen Odoo models, promoting DRY and consistency.  
**Logic Description:** Define an Odoo AbstractModel. `correlation_id` field could be automatically populated. `_get_current_correlation_id` might retrieve it from context. `_log_structured_activity` provides a convenient way for models to log activities using `logging_utils`, automatically including model context (e.g., self.id, self._name). This helps satisfy structured logging aspects of REQ-ATEL-002 when logging from model methods.  
**Documentation:**
    
    - **Summary:** Provides abstract model mixins with common fields like `correlation_id` or methods like standardized logging helpers, intended for inheritance by concrete InfluenceGen models.
    
**Namespace:** InfluenceGen.Odoo.Shared.Core.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

