# -*- coding: utf-8 -*-
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
    # It returns a list of local parts if valid, or an empty list.
    # However, email_split itself doesn't do full validation, primarily splits.
    # We should use it in conjunction with a regex or library.
    # For stricter validation, use a library like `email_validator`.
    # The SDS check `if not email_split(email_string): return False` might be too simplistic
    # as email_split might return something even for partially valid looking emails.
    # Let's refine based on how email_split behaves - it usually returns the local part.
    try:
        local_part = email_split(email_string)
        if not local_part or not local_part[0]: # email_split returns list of local parts
            return False
    except: # Catches errors from email_split if input is malformed.
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
        # import validators # (Example, if used and available)
        # result = validators.url(url_string)
        # if result:
        #     if schemes:
        #         from urllib.parse import urlparse # Import here to keep it conditional
        #         parsed_url = urlparse(url_string)
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
            from urllib.parse import urlparse # Import here as it's optional
            parsed_url = urlparse(url_string)
            return parsed_url.scheme in schemes
        return True

    except Exception: # NOSONAR - Catch any exception during parsing or regex
        return False


def is_valid_phone_number(phone_string: str, country_code: Optional[str] = None) -> bool:
    """Validates a phone number string, optionally for a specific country.
       Uses Odoo's phone_validation.phone_format which internally might use phonenumbers.
    """
    if not phone_string or not isinstance(phone_string, str):
        return False
    try:
        # Odoo's tiy_phone_format can validate and format.
        # For pure validation, phonenumbers library is more direct if available and preferred.
        # Example of using tiy_phone_format for validation (it formats or returns empty):
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
        pattern = r"^\+?[1-9]\d{1,14}$" # E.164-like basic check
        return bool(re.match(pattern, phone_string))

    except Exception: # NOSONAR - Catch any exception during processing
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
        # Consider raising TypeError if strict type checking is needed,
        # or logging a warning. For now, following SDS to return False.
        return False
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
        # Consider raising TypeError or logging. Following SDS to return False.
        return False
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
    if platform in ['instagram', 'x', 'tiktok']: # Using common known platforms
        # Common: alphanumeric, underscores, periods. No leading/trailing special chars typically.
        # This is a simplified regex. Each platform has its own detailed rules for length,
        # allowed characters, and reserved names.
        pattern = r"^[a-zA-Z0-9_.]+$" # Allows letters, numbers, underscore, period
        if not re.match(pattern, handle):
            return False
        if handle.startswith('.') or handle.endswith('.'): # Cannot start or end with period
             return False
        if '..' in handle: # Cannot have consecutive periods (common rule)
            return False

        # General length constraint, often around 1-30 characters.
        # Instagram: Max 30. TikTok: 2-24. X (Twitter): 4-15.
        # Using a general range here. Specific checks would be better.
        if len(handle) < 1 or len(handle) > 30:
             return False
    # Add more platform specific rules if needed, e.g., for YouTube channel names, Facebook, etc.
    # else:
    #     # For unknown platforms, perhaps return True or apply a very generic check.
    #     # For now, if platform is not in the list, assume it's not a handled validation.
    #     return False # Or True, depending on desired behavior for unlisted platforms.
    # The SDS implies True if not specifically handled and passes basic checks.
    # The current logic will return True if platform is not in the list and handle is not empty str.
    # To be stricter, if platform is not in the list, one might return False.
    # Let's assume for now, it must be a known platform for this validation to apply.
    # If the platform is not in the list, it means we don't have rules for it.
    # The SDS shows `if platform in [...]` then checks, implies if not in, it passes or needs more rules.
    # The structure suggests the function returns true if no specific rule makes it false.

    return True

def is_valid_file_type(file_name: str, allowed_extensions: List[str]) -> bool:
    """Checks if the file extension is in the list of allowed extensions."""
    if not file_name or not isinstance(file_name, str) or not allowed_extensions:
        return False
    # Ensure extensions in allowed_extensions start with a dot for consistency
    normalized_allowed_extensions = [
        ext.lower() if ext.startswith('.') else f".{ext.lower()}"
        for ext in allowed_extensions
    ]
    file_name_lower = file_name.lower()
    return any(file_name_lower.endswith(ext) for ext in normalized_allowed_extensions)

def is_valid_file_size(file_size_bytes: int, max_size_bytes: int) -> bool:
    """Checks if the file size is within the maximum allowed size."""
    if not isinstance(file_size_bytes, int) or not isinstance(max_size_bytes, int):
        return False # Or raise TypeError
    return 0 < file_size_bytes <= max_size_bytes