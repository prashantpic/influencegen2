# -*- coding: utf-8 -*-
from typing import Union, Optional, Any
from datetime import datetime, date, timezone
import re
# from dateutil import parser # If more robust date parsing is needed, add to dependencies

def clean_text_input(text: Optional[str]) -> Optional[str]:
    """Removes leading/trailing whitespace and reduces multiple spaces to one."""
    if text is None:
        return None
    if not isinstance(text, str):
        # Or raise TypeError("Input must be a string")
        return str(text) # Attempt conversion as per SDS
    text = text.strip()
    text = re.sub(r'\s+', ' ', text) # Replace multiple whitespace chars with a single space
    return text

def normalize_social_media_handle(handle: Optional[str], platform: Optional[str] = None) -> Optional[str]:
    """Normalizes social media handles (e.g., removes '@', converts to lowercase)."""
    if handle is None:
        return None
    cleaned_handle = clean_text_input(handle) # Use the cleaning function
    if not cleaned_handle: # clean_text_input might return empty string
        return None

    if cleaned_handle.startswith('@'):
        cleaned_handle = cleaned_handle[1:]

    # Platform-specific normalization (example)
    # SDS: "# if platform and platform.lower() in ['x', 'instagram', 'tiktok']:"
    # This implies that if platform is not specified or not in the list, lowercase is not applied.
    # For broader normalization, one might always lowercase, or have more specific rules.
    # Following SDS:
    if platform and platform.lower() in ['x', 'instagram', 'tiktok']:
        cleaned_handle = cleaned_handle.lower()
    
    return cleaned_handle

def convert_to_utc_datetime(
    dt_value: Union[str, date, datetime, None],
    date_format: Optional[str] = None
) -> Optional[datetime]:
    """
    Converts various date/datetime inputs to a timezone-aware UTC datetime object.
    Handles:
    - datetime objects: Converts naive to UTC (assuming UTC), or aware to UTC.
    - date objects: Converts to datetime at midnight UTC.
    - string objects:
        - If date_format is provided, uses strptime.
        - Otherwise, attempts to parse as ISO 8601 (handling 'Z' for UTC).
          For more flexible string parsing, `python-dateutil` library's `parser.parse` could be used.
    Returns None if conversion fails or input is None.
    """
    if dt_value is None:
        return None

    dt_obj: Optional[datetime] = None

    if isinstance(dt_value, datetime):
        dt_obj = dt_value
    elif isinstance(dt_value, date):
        dt_obj = datetime(dt_value.year, dt_value.month, dt_value.day)
    elif isinstance(dt_value, str):
        try:
            if date_format:
                dt_obj = datetime.strptime(dt_value, date_format)
            else:
                # Try ISO 8601 format, supporting 'Z' for UTC
                # Python's fromisoformat is strict. Replace 'Z' for wider compatibility.
                # It handles timezone offsets like +00:00 directly.
                if dt_value.endswith('Z'):
                    dt_obj = datetime.fromisoformat(dt_value[:-1] + '+00:00')
                else:
                    dt_obj = datetime.fromisoformat(dt_value)
                # If more robust parsing is needed (e.g. from dateutil import parser):
                # dt_obj = parser.parse(dt_value)
        except ValueError:
            # Consider logging a warning or raising a custom exception for unparseable strings
            _logger = logging.getLogger(__name__) # Local logger for this specific case
            _logger.warning(f"Could not parse date string: '{dt_value}' with format '{date_format}' or as ISO.")
            return None
    else:
        # Input type is not supported
        _logger = logging.getLogger(__name__) # Local logger
        _logger.warning(f"Unsupported type for date conversion: {type(dt_value)}")
        return None

    if dt_obj is None: # Should not happen if logic is correct, but as a safeguard
        return None

    # Ensure the datetime object is timezone-aware and converted to UTC
    if dt_obj.tzinfo is None:
        # Assume naive datetime is UTC, as per SDS suggestion for simplicity.
        # For local time conversion to UTC:
        # from tzlocal import get_localzone # Requires tzlocal library
        # local_tz = get_localzone()
        # dt_obj = local_tz.localize(dt_obj, is_dst=None).astimezone(timezone.utc)
        return dt_obj.replace(tzinfo=timezone.utc)
    else:
        return dt_obj.astimezone(timezone.utc)

def mask_sensitive_data(
    data: Optional[str],
    visible_chars_start: int = 0,
    visible_chars_end: int = 4,
    mask_char: str = '*'
) -> Optional[str]:
    """Masks a string, showing only a few characters at the start and/or end."""
    if data is None:
        return None
    if not isinstance(data, str):
        data = str(data) # Attempt conversion as per SDS

    data_len = len(data)
    if data_len == 0:
        return "" # Return empty string if input is empty string

    if not isinstance(visible_chars_start, int) or visible_chars_start < 0:
        visible_chars_start = 0
    if not isinstance(visible_chars_end, int) or visible_chars_end < 0:
        visible_chars_end = 0
    if not isinstance(mask_char, str) or len(mask_char) != 1:
        mask_char = '*' # Default to '*' if invalid mask_char

    if visible_chars_start + visible_chars_end >= data_len:
        # Not enough characters to mask effectively according to parameters, or show all
        return data

    masked_part_len = data_len - visible_chars_start - visible_chars_end
    # Ensure masked_part_len is not negative if params are misconfigured relative to len
    masked_part_len = max(0, masked_part_len)
    
    masked_part = mask_char * masked_part_len

    # Construct the masked string
    start_str = data[:visible_chars_start]
    # Ensure end_str slicing is correct, especially if visible_chars_end is 0
    end_str = data[data_len - visible_chars_end:] if visible_chars_end > 0 else ""
    
    return start_str + masked_part + end_str