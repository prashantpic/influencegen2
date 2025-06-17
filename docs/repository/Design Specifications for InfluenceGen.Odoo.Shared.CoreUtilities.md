# Software Design Specification: InfluenceGen.Odoo.Shared.CoreUtilities

## 1. Introduction

### 1.1. Purpose
This document provides a detailed software design specification for the `InfluenceGen.Odoo.Shared.CoreUtilities` Odoo module. This module serves as a centralized library of core utility functions, constants, base classes, and common helper methods. Its primary goal is to promote code reusability (DRY principle), ensure consistency in common operations, and simplify the development of other backend modules within the InfluenceGen platform.

### 1.2. Scope
The scope of this module includes:
*   Shared constants for platform-wide use.
*   Custom exception classes for domain-specific error handling.
*   Reusable data validation utility functions.
*   Standardized logging wrappers for consistent, structured logging with context propagation.
*   Common data transformation utilities.
*   Security-related utility functions.
*   Miscellaneous general-purpose utilities.
*   Base model mixins providing common fields and methods for InfluenceGen Odoo models.

This module is designed to be a dependency for other InfluenceGen Odoo modules, providing them with a common toolkit.

### 1.3. Definitions, Acronyms, and Abbreviations
*   **DRY:** Don't Repeat Yourself
*   **ORM:** Object-Relational Mapper
*   **KYC:** Know Your Customer
*   **PII:** Personally Identifiable Information
*   **SDS:** Software Design Specification
*   **UTC:** Coordinated Universal Time
*   **UUID:** Universally Unique Identifier
*   **JSON:** JavaScript Object Notation
*   **API:** Application Programming Interface
*   **UAT:** User Acceptance Testing

## 2. System Overview
The `InfluenceGen.Odoo.Shared.CoreUtilities` module is an integral part of the InfluenceGen Odoo Integration Platform. It does not provide end-user facing UI on its own but offers essential backend services and tools consumed by other modules like `InfluenceGen.Odoo.Business.Services`, `InfluenceGen.Odoo.Integration.Adapters`, and backend controllers.

## 3. Design Considerations

### 3.1. Assumptions and Dependencies
*   The module is developed for Odoo Version 18.
*   The primary programming language is Python 3.11.9.
*   Odoo's standard libraries and ORM are available and utilized.
*   Dependent modules will correctly import and use the utilities provided.
*   For libraries like `phonenumbers` or `email_validator`, it's assumed they will be added as Python dependencies to the Odoo environment if chosen for implementation.

### 3.2. General Constraints
*   Code must adhere to Odoo development best practices and organizational coding standards (REQ-DDSI-003).
*   Utilities should be generic enough for broad applicability across InfluenceGen modules.
*   Performance impact of utility functions must be minimal.
*   Security considerations are paramount for utilities handling sensitive data or operations.

### 3.3. Goals and Guidelines
*   **Reusability:** Maximize code reuse to reduce redundancy.
*   **Consistency:** Ensure common operations are handled uniformly.
*   **Maintainability:** Code should be well-documented, modular, and easy to understand.
*   **Testability:** Utilities should be designed for easy unit testing.
*   **Clarity:** Provide clear and specific error handling and logging.

## 4. System Architecture
This module adheres to the overall Layered Architecture of the InfluenceGen platform, providing foundational utilities used by the Business Logic and Infrastructure & Integration Services Layers of other modules.

## 5. Detailed Design

### 5.1. Module Structure
The module `influence_gen_shared_core` will have the following structure:


influence_gen_shared_core/
├── __manifest__.py
├── __init__.py
├── const/
│   ├── __init__.py
│   └── influence_gen_constants.py
├── exceptions/
│   ├── __init__.py
│   └── custom_exceptions.py
├── models/
│   ├── __init__.py
│   └── base_model_mixin.py
└── utils/
    ├── __init__.py
    ├── validation_utils.py
    ├── logging_utils.py
    ├── data_transformation_utils.py
    ├── security_utils.py
    └── misc_utils.py


### 5.2. File Specifications

#### 5.2.1. `__manifest__.py`
*   **Description:** Odoo module manifest file.
*   **Purpose:** Declares the Odoo module, its version, author, category, dependencies, and other metadata.
*   **Logic:**
    python
    {
        'name': 'InfluenceGen Shared Core Utilities',
        'version': '18.0.1.0.0',
        'summary': 'Core utility functions, constants, and base classes for the InfluenceGen platform.',
        'author': 'SSS-AI',
        'website': 'https://www.example.com', # Replace with actual website
        'category': 'InfluenceGen/Core',
        'depends': ['base', 'mail'], # mail for mail.message in mixin
        'data': [], # No XML data views for this utility module typically
        'installable': True,
        'application': False,
        'auto_install': False,
        'license': 'LGPL-3', # Or appropriate license
    }
    

#### 5.2.2. `__init__.py` (root)
*   **Description:** Root `__init__.py` for the module.
*   **Purpose:** Initializes the Python package and imports sub-packages.
*   **Logic:**
    python
    from . import const
    from . import exceptions
    from . import models
    from . import utils
    

#### 5.2.3. `const/__init__.py`
*   **Description:** `__init__.py` for the `const` sub-package.
*   **Purpose:** Makes constants defined in this package accessible.
*   **Logic:**
    python
    from . import influence_gen_constants
    

#### 5.2.4. `const/influence_gen_constants.py`
*   **Description:** Defines shared constants for the InfluenceGen platform.
*   **Purpose:** Centralizes platform-wide constants.
*   **Logic:**
    python
    # KYC Statuses
    KYC_STATUS_PENDING = 'pending'
    KYC_STATUS_IN_REVIEW = 'in_review'
    KYC_STATUS_APPROVED = 'approved'
    KYC_STATUS_REJECTED = 'rejected'
    KYC_STATUS_MORE_INFO_REQUIRED = 'more_info_required'

    # Campaign Statuses (Example - actual statuses might be in campaign module,
    # but common ones could be here if used by multiple core processes)
    CAMPAIGN_STATUS_DRAFT = 'draft'
    CAMPAIGN_STATUS_PUBLISHED = 'published'
    CAMPAIGN_STATUS_ACTIVE = 'active' # Or 'in_progress'
    CAMPAIGN_STATUS_COMPLETED = 'completed'
    CAMPAIGN_STATUS_ARCHIVED = 'archived'
    CAMPAIGN_STATUS_CANCELLED = 'cancelled'

    # Log Severities (align with Python logging levels if possible for consistency)
    LOG_SEVERITY_DEBUG = 'DEBUG'
    LOG_SEVERITY_INFO = 'INFO'
    LOG_SEVERITY_WARNING = 'WARNING'
    LOG_SEVERITY_ERROR = 'ERROR'
    LOG_SEVERITY_CRITICAL = 'CRITICAL'

    # HTTP Headers
    DEFAULT_CORRELATION_ID_HEADER = 'X-Correlation-ID'
    REQUEST_ID_HEADER = 'X-Request-ID' # Example, if used

    # Default Values
    DEFAULT_AI_IMAGE_RESOLUTION = '1024x1024' # Example
    DEFAULT_PAGE_LIMIT = 20

    # File Types
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
    ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx']
    MAX_IMAGE_FILE_SIZE_MB = 5
    MAX_DOCUMENT_FILE_SIZE_MB = 10

    # Social Media Platforms (Example)
    PLATFORM_INSTAGRAM = 'instagram'
    PLATFORM_TIKTOK = 'tiktok'
    PLATFORM_YOUTUBE = 'youtube'
    PLATFORM_X = 'x' # formerly Twitter
    

#### 5.2.5. `exceptions/__init__.py`
*   **Description:** `__init__.py` for the `exceptions` sub-package.
*   **Purpose:** Makes custom exception classes accessible.
*   **Logic:**
    python
    from .custom_exceptions import (
        InfluenceGenValidationException,
        InfluenceGenIntegrationException,
        InfluenceGenConfigurationError,
        InfluenceGenSecurityException,
        InfluenceGenProcessingError,
    )
    

#### 5.2.6. `exceptions/custom_exceptions.py`
*   **Description:** Defines custom exception classes.
*   **Purpose:** Provides domain-specific exceptions for improved error handling.
*   **Logic:**
    python
    from odoo.exceptions import UserError, ValidationError

    class InfluenceGenBaseException(Exception):
        """Base exception for InfluenceGen specific errors not intended for direct UI display."""
        def __init__(self, message, original_exception=None):
            super().__init__(message)
            self.original_exception = original_exception

    class InfluenceGenValidationException(ValidationError):
        """Custom validation exception, typically for UI display."""
        def __init__(self, message, *args):
            super().__init__(message, *args)

    class InfluenceGenIntegrationException(InfluenceGenBaseException):
        """Exception for errors during integration with external services (N8N, AI APIs, etc.)."""
        pass

    class InfluenceGenConfigurationError(InfluenceGenBaseException):
        """Exception for errors related to misconfiguration of the platform."""
        pass

    class InfluenceGenSecurityException(InfluenceGenBaseException):
        """Exception for security-related violations or issues."""
        pass

    class InfluenceGenProcessingError(InfluenceGenBaseException):
        """General exception for errors during internal processing tasks."""
        pass

    # UserError is a good base for messages that should be shown to the end-user directly.
    # ValidationError is a specific type of UserError for data validation issues.
    

#### 5.2.7. `utils/__init__.py`
*   **Description:** `__init__.py` for the `utils` sub-package.
*   **Purpose:** Makes utility modules accessible.
*   **Logic:**
    python
    from . import validation_utils
    from . import logging_utils
    from . import data_transformation_utils
    from . import security_utils
    from . import misc_utils
    

#### 5.2.8. `utils/validation_utils.py`
*   **Description:** Provides reusable data validation utility functions. (REQ-DMG-014)
*   **Purpose:** Ensures data integrity across modules.
*   **Logic:**
    python
    import re
    from typing import Union, Optional, List
    from datetime import datetime
    # Consider adding 'validators' and 'phonenumbers' to Odoo's Python environment dependencies
    # import validators # (Example, if used)
    # import phonenumbers # (Example, if used)
    from odoo.tools import email_split,টিয়_phone_format # Odoo's built-in tools

    def is_valid_email(email_string: str) -> bool:
        """Validates an email address string."""
        if not email_string or not isinstance(email_string, str):
            return False
        # Odoo's email_split is robust
        if not email_split(email_string):
             return False
        # Basic regex for common patterns, can be enhanced
        # Or use a dedicated library like `email_validator`
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email_string))

    def is_valid_url(url_string: str, schemes: Optional[List[str]] = None) -> bool:
        """Validates a URL string.
           Optionally checks if the URL scheme is in the provided list.
        """
        if not url_string or not isinstance(url_string, str):
            return False
        # Using a library like 'validators' is recommended for comprehensive validation
        # For a basic check:
        try:
            # Simple check, can be improved with `validators` library
            # result = validators.url(url_string)
            # if result:
            #     if schemes:
            #         parsed_url = urllib.parse.urlparse(url_string)
            #         return parsed_url.scheme in schemes
            #     return True
            # return False
            # Basic regex as a placeholder
            pattern = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https:// or ftp:// or ftps://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if not re.match(pattern, url_string):
                return False
            if schemes:
                from urllib.parse import urlparse
                parsed_url = urlparse(url_string)
                return parsed_url.scheme in schemes
            return True

        except Exception: # NOSONAR
            return False


    def is_valid_phone_number(phone_string: str, country_code: Optional[str] = None) -> bool:
        """Validates a phone number string, optionally for a specific country.
           Uses Odoo's phone_validation.phone_format which internally might use phonenumbers.
        """
        if not phone_string or not isinstance(phone_string, str):
            return False
        try:
            # Odoo's tiy_phone_format can validate and format.
            # For pure validation, phonenumbers library is more direct.
            # formatted_number = tiy_phone_format(phone_string, country_code=country_code, raise_exception=False)
            # return bool(formatted_number)
            # Placeholder if phonenumbers library is not directly used/available or for more control
            # This is a very basic regex and should be replaced by a robust library like 'phonenumbers'
            if country_code: # If country code is provided, regex needs to be country specific
                 # Example for US, very simplified:
                if country_code.upper() == 'US':
                    pattern = r"^\+?1?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
                    return bool(re.match(pattern, phone_string))
            # Generic pattern for international numbers (very basic)
            pattern = r"^\+?[1-9]\d{1,14}$"
            return bool(re.match(pattern, phone_string))

        except Exception: # NOSONAR
            return False

    def is_valid_date_format(date_string: str, date_f: str) -> bool:
        """Checks if a string matches a given date format."""
        if not date_string or not isinstance(date_string, str):
            return False
        try:
            datetime.strptime(date_string, date_f)
            return True
        except ValueError:
            return False

    def is_within_range(value: Union[int, float],
                        min_val: Optional[Union[int, float]] = None,
                        max_val: Optional[Union[int, float]] = None) -> bool:
        """Checks if a numeric value is within an optional min/max range."""
        if not isinstance(value, (int, float)):
            return False # Or raise TypeError
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True

    def is_valid_length(text: str,
                        min_len: Optional[int] = None,
                        max_len: Optional[int] = None) -> bool:
        """Checks if a string's length is within an optional min/max range."""
        if not isinstance(text, str):
            return False # Or raise TypeError
        text_len = len(text)
        if min_len is not None and text_len < min_len:
            return False
        if max_len is not None and text_len > max_len:
            return False
        return True

    def is_valid_social_media_handle(handle: str, platform: str) -> bool:
        """Validates social media handle based on platform conventions (basic)."""
        if not handle or not isinstance(handle, str):
            return False
        # Example basic checks, can be expanded with platform-specific regex
        if platform in ['instagram', 'x', 'tiktok']:
            # Common: alphanumeric, underscores, no leading/trailing special chars
            # This is a simplified regex. Each platform has its own rules.
            pattern = r"^[a-zA-Z0-9_.]+$"
            if not re.match(pattern, handle):
                return False
            if len(handle) < 1 or len(handle) > 30: # General length constraint
                 return False
        # Add more platform specific rules if needed
        return True

    def is_valid_file_type(file_name: str, allowed_extensions: List[str]) -> bool:
        """Checks if the file extension is in the list of allowed extensions."""
        if not file_name or not isinstance(file_name, str) or not allowed_extensions:
            return False
        return any(file_name.lower().endswith(ext.lower()) for ext in allowed_extensions)

    def is_valid_file_size(file_size_bytes: int, max_size_bytes: int) -> bool:
        """Checks if the file size is within the maximum allowed size."""
        if not isinstance(file_size_bytes, int) or not isinstance(max_size_bytes, int):
            return False
        return 0 < file_size_bytes <= max_size_bytes
    

#### 5.2.9. `utils/logging_utils.py`
*   **Description:** Provides standardized logging wrappers. (REQ-ATEL-002)
*   **Purpose:** Enforces consistent, structured logging.
*   **Logic:**
    python
    import logging
    import json
    import uuid
    from datetime import datetime, timezone
    from typing import Optional, Dict, Any
    import odoo # For accessing odoo.http.request if available
    from ..const import influence_gen_constants

    _logger = logging.getLogger(__name__) # Logger for this utility module itself

    def get_logger(name: str) -> logging.Logger:
        """Returns a logger instance for the given name."""
        return logging.getLogger(name)

    def get_correlation_id(request_opt: Optional[Any] = None) -> str:
        """
        Retrieves or generates a correlation ID.
        Tries to get it from Odoo request headers or context, otherwise generates a new UUID.
        """
        correlation_id = None
        # Try from odoo.http.request if available (e.g., in a controller context)
        if hasattr(odoo, 'http') and odoo.http.request:
            correlation_id = odoo.http.request.httprequest.headers.get(
                influence_gen_constants.DEFAULT_CORRELATION_ID_HEADER
            )
        # Try from passed request_opt (e.g., Odoo's self.env.context in a model method)
        if not correlation_id and request_opt:
            if hasattr(request_opt, 'context') and isinstance(request_opt.context, dict):
                correlation_id = request_opt.context.get('correlation_id')
            elif isinstance(request_opt, dict): # if request_opt is already a context dict
                correlation_id = request_opt.get('correlation_id')


        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        return correlation_id

    def inject_correlation_id_to_context(context: Optional[Dict], correlation_id: Optional[str] = None) -> Dict:
        """Injects correlation_id into context if not present."""
        if context is None:
            context = {}
        if 'correlation_id' not in context:
            context['correlation_id'] = correlation_id or get_correlation_id()
        return context

    def _format_log_message_json(
        message: str,
        level: str,
        logger_name: str,
        user_id: Optional[int] = None,
        request_id_val: Optional[str] = None, # Renamed to avoid conflict with odoo.http.request
        correlation_id_val: Optional[str] = None, # Renamed
        extra_context: Optional[Dict] = None
    ) -> str:
        """Constructs a JSON log message with UTC timestamp and contextual IDs."""
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': level,
            'logger': logger_name,
            'message': message,
        }
        # Attempt to get current Odoo user if not provided
        uid_to_log = user_id
        if uid_to_log is None and hasattr(odoo, 'SUPERUSER_ID'): # Check if odoo global is available
            try:
                # This might fail if not in an Odoo environment with an active env
                if odoo.env:
                     uid_to_log = odoo.env.uid
            except Exception: # NOSONAR
                pass # Keep uid_to_log as None

        if uid_to_log is not None:
            log_entry['user_id'] = uid_to_log

        # Use provided correlation_id_val or try to get it
        final_correlation_id = correlation_id_val or get_correlation_id(
            request_opt=odoo.http.request if hasattr(odoo, 'http') and odoo.http.request else None
        )
        if final_correlation_id:
            log_entry['correlation_id'] = final_correlation_id

        if request_id_val: # If a specific request_id is passed
            log_entry['request_id'] = request_id_val
        elif hasattr(odoo, 'http') and odoo.http.request and hasattr(odoo.http.request, 'session') and odoo.http.request.session.sid:
            # Use Odoo session ID as a form of request identifier if no specific one is provided
            log_entry['session_id'] = odoo.http.request.session.sid


        if extra_context:
            log_entry.update(extra_context)

        return json.dumps(log_entry)

    def _log_structured(
        logger_instance: logging.Logger,
        level_name: str, # e.g., "INFO", "ERROR"
        logging_level_int: int, # e.g., logging.INFO, logging.ERROR
        message: str,
        user_id: Optional[int] = None,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        exc_info_flag: bool = False,
        extra_context: Optional[Dict] = None
    ):
        """Helper function to log structured messages."""
        if logger_instance.isEnabledFor(logging_level_int):
            json_message = _format_log_message_json(
                message, level_name, logger_instance.name, user_id, request_id, correlation_id, extra_context
            )
            logger_instance.log(logging_level_int, json_message, exc_info=exc_info_flag)

    def log_info_structured(
        logger_instance: logging.Logger,
        message: str,
        user_id: Optional[int] = None,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        extra_context: Optional[Dict] = None
    ):
        _log_structured(logger_instance, "INFO", logging.INFO, message,
                        user_id, request_id, correlation_id, False, extra_context)

    def log_error_structured(
        logger_instance: logging.Logger,
        message: str,
        exc_info: bool = False, # Pass True to include exception info
        user_id: Optional[int] = None,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        extra_context: Optional[Dict] = None
    ):
        _log_structured(logger_instance, "ERROR", logging.ERROR, message,
                        user_id, request_id, correlation_id, exc_info, extra_context)

    def log_warning_structured(
        logger_instance: logging.Logger,
        message: str,
        user_id: Optional[int] = None,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        extra_context: Optional[Dict] = None
    ):
        _log_structured(logger_instance, "WARNING", logging.WARNING, message,
                        user_id, request_id, correlation_id, False, extra_context)

    def log_debug_structured(
        logger_instance: logging.Logger,
        message: str,
        user_id: Optional[int] = None,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        extra_context: Optional[Dict] = None
    ):
        _log_structured(logger_instance, "DEBUG", logging.DEBUG, message,
                        user_id, request_id, correlation_id, False, extra_context)

    def log_critical_structured(
        logger_instance: logging.Logger,
        message: str,
        exc_info: bool = False,
        user_id: Optional[int] = None,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        extra_context: Optional[Dict] = None
    ):
        _log_structured(logger_instance, "CRITICAL", logging.CRITICAL, message,
                        user_id, request_id, correlation_id, exc_info, extra_context)

    

#### 5.2.10. `utils/data_transformation_utils.py`
*   **Description:** Helper functions for common data transformations.
*   **Purpose:** Ensures consistency in data cleaning and normalization.
*   **Logic:**
    python
    from typing import Union, Optional
    from datetime import datetime, date, timezone
    # from dateutil import parser # If more robust date parsing is needed

    def clean_text_input(text: Optional[str]) -> Optional[str]:
        """Removes leading/trailing whitespace and reduces multiple spaces to one."""
        if text is None:
            return None
        if not isinstance(text, str):
            # Or raise TypeError("Input must be a string")
            return str(text) # Attempt conversion
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    def normalize_social_media_handle(handle: Optional[str], platform: Optional[str] = None) -> Optional[str]:
        """Normalizes social media handles (e.g., removes '@', converts to lowercase)."""
        if handle is None:
            return None
        cleaned_handle = clean_text_input(handle)
        if not cleaned_handle:
            return None

        if cleaned_handle.startswith('@'):
            cleaned_handle = cleaned_handle[1:]

        # Platform-specific normalization (example)
        # if platform and platform.lower() in ['x', 'instagram', 'tiktok']:
        #     cleaned_handle = cleaned_handle.lower()
        return cleaned_handle

    def convert_to_utc_datetime(dt_value: Union[str, date, datetime, None],
                                date_format: Optional[str] = None) -> Optional[datetime]:
        """Converts various date/datetime inputs to a timezone-aware UTC datetime object."""
        if dt_value is None:
            return None

        if isinstance(dt_value, datetime):
            if dt_value.tzinfo is None:
                # Assume naive datetime is UTC, or local and convert. For simplicity, assume UTC.
                # For local time conversion:
                # local_tz = get_localzone() # from tzlocal library
                # dt_value = local_tz.localize(dt_value, is_dst=None)
                return dt_value.replace(tzinfo=timezone.utc)
            return dt_value.astimezone(timezone.utc)
        elif isinstance(dt_value, date):
            return datetime(dt_value.year, dt_value.month, dt_value.day, tzinfo=timezone.utc)
        elif isinstance(dt_value, str):
            try:
                if date_format:
                    dt_obj = datetime.strptime(dt_value, date_format)
                else:
                    # Try common ISO format or use dateutil.parser for more flexibility
                    # dt_obj = parser.parse(dt_value) # Requires `python-dateutil`
                    dt_obj = datetime.fromisoformat(dt_value.replace('Z', '+00:00')) # Handles ISO 8601 with Z
                
                if dt_obj.tzinfo is None:
                    return dt_obj.replace(tzinfo=timezone.utc)
                return dt_obj.astimezone(timezone.utc)
            except ValueError:
                # Consider logging a warning or raising a custom exception
                return None
        return None # Should not reach here if types are handled

    def mask_sensitive_data(data: Optional[str], visible_chars_start: int = 0, visible_chars_end: int = 4, mask_char: str = '*') -> Optional[str]:
        """Masks a string, showing only a few characters at the start and/or end."""
        if data is None:
            return None
        if not isinstance(data, str):
            data = str(data) # Attempt conversion

        data_len = len(data)
        if data_len == 0:
            return ""

        if visible_chars_start < 0: visible_chars_start = 0
        if visible_chars_end < 0: visible_chars_end = 0

        if visible_chars_start + visible_chars_end >= data_len:
            return data # Not enough characters to mask effectively, or show all

        masked_part_len = data_len - visible_chars_start - visible_chars_end
        masked_part = mask_char * masked_part_len

        return data[:visible_chars_start] + masked_part + data[data_len-visible_chars_end:]
    

#### 5.2.11. `utils/security_utils.py`
*   **Description:** Utility functions related to security.
*   **Purpose:** Centralizes security-sensitive operations.
*   **Logic:**
    python
    import hashlib
    from typing import Optional, Dict, Any
    import odoo # For accessing odoo.env

    _logger = odoo.addons.influence_gen_shared_core.utils.logging_utils.get_logger(__name__)


    def get_config_parameter(param_name: str, default_value: Optional[Any] = None) -> Optional[Any]:
        """
        Securely retrieves a configuration parameter from Odoo's ir.config_parameter.
        It is recommended to use this for non-secret parameters. For secrets, use Odoo's
        secrets management or an external vault. This function acts as a wrapper.
        """
        try:
            # Odoo's get_param is the standard way.
            # Ensure this utility is used within an Odoo environment context.
            if hasattr(odoo, 'env') and odoo.env:
                # sudo() might be needed if access rights are an issue for certain params
                # but generally not for read if the param is system-wide.
                # Use with caution if sudo() is applied.
                value = odoo.env['ir.config_parameter'].sudo().get_param(param_name, default_value)
                return value
            else:
                # Fallback or error if not in Odoo env context
                _logger.warning(f"Odoo environment not available for get_config_parameter: {param_name}") # NOSONAR
                return default_value
        except Exception as e:
            _logger.error(f"Error retrieving config parameter '{param_name}': {e}") # NOSONAR
            return default_value

    def get_secret_from_config(secret_name: str, default_value: Optional[str] = None) -> Optional[str]:
        """
        Retrieves a secret. Placeholder for integration with Odoo's secrets management
        or an external vault. For now, it can be a wrapper around get_config_parameter
        with the expectation that the parameter is stored securely (e.g., encrypted if Odoo supports it,
        or the key refers to a vault entry).
        IMPORTANT: Odoo itself does not encrypt ir.config_parameter values by default.
        True secret management requires an external vault or Odoo Enterprise's vault features.
        This function name implies stronger security than ir.config_parameter alone might provide.
        """
        # This is a simplified version. Real secret management would involve
        # Odoo's vault features (Enterprise) or an external vault integration.
        _logger.info(f"Attempting to retrieve secret: {secret_name}") # NOSONAR
        return get_config_parameter(secret_name, default_value)


    def hash_data_sha256(data: str) -> str:
        """Hashes a string using SHA-256."""
        if not isinstance(data, str):
            raise TypeError("Input data must be a string for SHA-256 hashing.")
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    # Note: Password verification should almost always use Odoo's built-in mechanisms
    # which handle salt and hashing specifics (e.g., self.env.user._check_password(password)).
    # Avoid reimplementing password verification.
    

#### 5.2.12. `utils/misc_utils.py`
*   **Description:** Collection of miscellaneous general-purpose utilities.
*   **Purpose:** Provides helpers for common tasks not fitting other categories.
*   **Logic:**
    python
    import random
    import string
    from typing import List, Generator, Any, Optional
    import os # For environment variable access

    def generate_unique_code(length: int = 8,
                             chars: str = string.ascii_uppercase + string.digits) -> str:
        """Generates a random unique code of specified length from given characters."""
        if length <= 0:
            raise ValueError("Length must be a positive integer.")
        return ''.join(random.choices(chars, k=length))

    def get_env_variable(env_key: str, default_value: Optional[Any] = None) -> Optional[Any]:
        """Retrieves an environment variable, returning a default value if not found."""
        return os.environ.get(env_key, default_value)

    def chunk_list(input_list: List[Any], chunk_size: int) -> Generator[List[Any], None, None]:
        """Yields successive n-sized chunks from input_list."""
        if chunk_size <= 0:
            raise ValueError("Chunk size must be a positive integer.")
        for i in range(0, len(input_list), chunk_size):
            yield input_list[i:i + chunk_size]

    # Example: Safely parse JSON string
    import json
    def safe_json_loads(json_string: Optional[str], default_value: Optional[Any] = None) -> Optional[Any]:
        """Safely loads a JSON string, returning default_value on error."""
        if json_string is None:
            return default_value
        try:
            return json.loads(json_string)
        except (json.JSONDecodeError, TypeError):
            return default_value
    

#### 5.2.13. `models/__init__.py`
*   **Description:** `__init__.py` for the `models` sub-package.
*   **Purpose:** Makes base model mixins accessible.
*   **Logic:**
    python
    from . import base_model_mixin
    

#### 5.2.14. `models/base_model_mixin.py`
*   **Description:** Defines base model mixins with common fields/methods. (REQ-ATEL-002)
*   **Purpose:** Promotes DRY and consistency in InfluenceGen Odoo models.
*   **Logic:**
    python
    from odoo import models, fields, api, _
    from odoo.http import request as odoo_request # To access current request if available
    from typing import Optional, Dict
    from ..utils import logging_utils # Use relative import within the module

    _logger = logging_utils.get_logger(__name__)

    class InfluenceGenBaseMixin(models.AbstractModel):
        _name = 'influence.gen.base.mixin'
        _description = 'InfluenceGen Base Mixin for Common Fields and Methods'

        # Common Fields (Example)
        # These fields might be better placed directly on models that need them,
        # or if truly universal, consider their impact carefully.
        # For now, focusing on methods, especially logging.

        # correlation_id = fields.Char(
        #     string="Correlation ID",
        #     readonly=True,
        #     copy=False,
        #     help="Correlation ID for tracing requests related to this record, set on creation if available in context."
        # )

        # Methods
        def _get_current_correlation_id(self) -> Optional[str]:
            """
            Retrieves the correlation ID.
            Tries from self.env.context, then odoo.http.request, then generates a new one.
            """
            correlation_id = self.env.context.get('correlation_id')
            if not correlation_id and odoo_request:
                correlation_id = logging_utils.get_correlation_id(request_opt=odoo_request)
            if not correlation_id: # Generate if still not found
                 correlation_id = logging_utils.get_correlation_id()
            return correlation_id

        def _log_activity_structured(
            self,
            message: str,
            level: str = "INFO",
            log_type_name: Optional[str] = None, # e.g. Odoo's 'mail.message.subtype' name like 'Note' or 'Activity'
            summary: Optional[str] = None, # For mail.activity summary
            note_html: Optional[str] = None, # For mail.message body or mail.activity note
            user_id_to_assign: Optional[int] = None, # For mail.activity assigned user
            date_deadline: Optional[fields.Date] = None, # For mail.activity deadline
            **kwargs # For extra_context in JSON log and potentially other mail.activity fields
        ):
            """
            Logs a structured message using logging_utils and optionally creates an Odoo mail.message or mail.activity.
            Automatically includes model name, record ID, and correlation ID in structured logs.
            """
            logger_instance = logging_utils.get_logger(self._name or 'influence.gen.model')
            correlation_id = self._get_current_correlation_id()

            extra_log_context = {
                'model': self._name,
                'res_id': self.id if self.id else None,
            }
            if kwargs:
                extra_log_context.update(kwargs)

            effective_message = message
            if note_html: # If note_html is provided, it's likely the main message content for mail.message/activity
                effective_message = note_html if isinstance(note_html, str) else "HTML content provided"


            if level.upper() == "INFO":
                logging_utils.log_info_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context)
            elif level.upper() == "ERROR":
                logging_utils.log_error_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context, exc_info=kwargs.get('exc_info', False))
            elif level.upper() == "WARNING":
                logging_utils.log_warning_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context)
            elif level.upper() == "DEBUG":
                logging_utils.log_debug_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context)
            elif level.upper() == "CRITICAL":
                logging_utils.log_critical_structured(logger_instance, effective_message, correlation_id=correlation_id, extra_context=extra_log_context, exc_info=kwargs.get('exc_info', False))
            else:
                logging_utils.log_info_structured(logger_instance, f"({level}) {effective_message}", correlation_id=correlation_id, extra_context=extra_log_context)


            # Optional: Create Odoo Chatter message (mail.message) or Activity (mail.activity)
            # This part requires the 'mail' module dependency in __manifest__.py
            if log_type_name and self.id and hasattr(self, 'message_post'): # Check if model inherits from mail.thread
                try:
                    body_content = note_html or message
                    self.message_post(body=body_content, subject=summary, subtype_xmlid=f"mail.mt_{log_type_name.lower().replace(' ', '_')}") # e.g. mail.mt_note
                    _logger.debug(f"Posted mail.message of type '{log_type_name}' for {self._name}:{self.id}") # NOSONAR
                except Exception as e:
                    _logger.error(f"Failed to post mail.message for {self._name}:{self.id}: {e}") # NOSONAR

            elif log_type_name == 'activity' and self.id and hasattr(self, 'activity_schedule'):
                try:
                    activity_type = self.env['mail.activity.type'].search([('name', '=', summary)], limit=1)
                    if not activity_type: # Create if not exists (or require pre-configuration)
                        activity_type = self.env['mail.activity.type'].create({'name': summary or "Platform Activity"})

                    self.activity_schedule(
                        activity_type_id=activity_type.id,
                        summary=summary or message,
                        note=note_html or message,
                        user_id=user_id_to_assign or self.env.user.id,
                        date_deadline=date_deadline
                    )
                    _logger.debug(f"Scheduled mail.activity for {self._name}:{self.id}") # NOSONAR
                except Exception as e:
                    _logger.error(f"Failed to schedule mail.activity for {self._name}:{self.id}: {e}") # NOSONAR


        # @api.model_create_multi
        # def create(self, vals_list):
        #     """Override create to inject correlation_id and log."""
        #     records = super(InfluenceGenBaseMixin, self.with_context(
        #         logging_utils.inject_correlation_id_to_context(self.env.context)
        #     )).create(vals_list)
            
        #     for record in records:
        #         # Attempt to set correlation_id field if it exists on the concrete model
        #         if hasattr(record, 'correlation_id') and not record.correlation_id:
        #             current_corr_id = record._get_current_correlation_id()
        #             if current_corr_id:
        #                 try:
        #                     # Use a direct SQL update or a non-triggering write if necessary
        #                     # to avoid recursion if 'write' also logs.
        #                     # For simplicity, direct assignment might trigger write if not careful.
        #                     # This is a complex area; Odoo's ORM can be tricky with onchange/compute.
        #                     # Best to set in context and have field compute from context on create.
        #                     # Or, if the field is simple Char, a direct write during create is often fine.
        #                     # For now, assuming correlation_id is set through context or manually.
        #                     pass # record.correlation_id = current_corr_id
        #                 except Exception as e:
        #                     _logger.warning(f"Could not set correlation_id field on {record._name}:{record.id}: {e}")

        #         record._log_activity_structured(
        #             message=f"{record._description or record._name} created.",
        #             level="INFO",
        #             log_type_name="note" # Example: log as a chatter note
        #         )
        #     return records

        # def write(self, vals):
        #     """Override write to log."""
        #     res = super(InfluenceGenBaseMixin, self.with_context(
        #         logging_utils.inject_correlation_id_to_context(self.env.context)
        #     )).write(vals)
            
        #     for record in self:
        #         changed_fields = ", ".join(vals.keys())
        #         record._log_activity_structured(
        #             message=f"{record._description or record._name} updated. Fields changed: {changed_fields}.",
        #             level="INFO",
        #             log_type_name="note" # Example
        #         )
        #     return res
        
        # Note: Overriding create/write in a generic mixin for logging and correlation_id
        # needs careful consideration of performance and potential recursion if not handled correctly.
        # It might be better to call _log_activity_structured explicitly from the concrete models'
        # create/write methods where specific context is richer.
        # For correlation_id, passing it in context during service calls and then to ORM methods
        # is a common pattern, and models can then retrieve it from self.env.context.
    

## 6. Data Model
This module primarily provides utilities and does not define its own extensive data models beyond the `InfluenceGenBaseMixin` (which is an AbstractModel). Data models for core entities like InfluencerProfile, Campaign, etc., will reside in their respective functional modules but may inherit from `InfluenceGenBaseMixin`.

## 7. Interfaces
This module does not define external API interfaces. It provides Python functions and classes intended for direct import and use by other Odoo modules within the same Odoo instance.

## 8. Security Considerations
*   **Validation Utilities:** Ensure validation utilities (`validation_utils.py`) are robust to prevent injection or bypass, although primary security relies on server-side validation in functional modules.
*   **Logging Utilities:** `logging_utils.py` must avoid logging sensitive PII unless explicitly required and handled with masking or other security measures. Correlation IDs should not leak sensitive information.
*   **Security Utilities:** `security_utils.py` should handle credentials and secrets with utmost care, leveraging Odoo's secure parameter storage or integrating with approved external vault solutions. Hashing functions must use strong, standard algorithms.
*   **Custom Exceptions:** Exceptions should not reveal excessive system details to unauthorized users if they bubble up to the UI. `UserError` and `ValidationError` are generally safe for UI display.

## 9. Testing Considerations
*   **Unit Tests:** Each utility function in `utils/` and method in `models/` must have comprehensive unit tests.
    *   `validation_utils_tests.py`: Test valid and invalid inputs for all validation functions.
    *   `logging_utils_tests.py`: Test log formatting, correlation ID generation/retrieval, and different log levels.
    *   `data_transformation_utils_tests.py`: Test various inputs for transformation functions.
    *   `security_utils_tests.py`: Test hashing. Mock Odoo `ir.config_parameter` for testing `get_config_parameter`.
    *   `misc_utils_tests.py`: Test utility functions with edge cases.
    *   `base_model_mixin_tests.py`: Test logging methods and correlation ID handling within the mixin context (may require mocking Odoo environment).
*   **Code Coverage:** Aim for high code coverage for all utilities.
*   **Linting and Static Analysis:** Integrate Flake8 and Pylint (or other approved tools) into the development/CI process to enforce coding standards (REQ-DDSI-003).

## 10. Deployment Considerations
This module will be deployed as a standard Odoo module. It should be listed as a dependency for any other InfluenceGen Odoo module that utilizes its functionalities.

## 11. Future Considerations / Extensibility
*   More sophisticated validation routines can be added to `validation_utils.py` as needed.
*   Additional platform-wide constants can be added to `influence_gen_constants.py`.
*   The `InfluenceGenBaseMixin` can be extended with more common fields or helper methods if identified.
*   Integration with more advanced secret management systems can be implemented in `security_utils.py`.
*   Error reporting to external services (e.g., Sentry) could be integrated within `logging_utils.py` or custom exception handlers.