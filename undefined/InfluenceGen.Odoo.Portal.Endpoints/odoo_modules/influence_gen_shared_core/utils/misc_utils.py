# -*- coding: utf-8 -*-
import random
import string
from typing import List, Generator, Any, Optional
import os # For environment variable access
import json

def generate_unique_code(length: int = 8,
                         chars: str = string.ascii_uppercase + string.digits) -> str:
    """
    Generates a random unique code of specified length from given characters.
    Note: "Unique" here means randomly generated, not guaranteed globally unique
    without further checks against existing codes in a database.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer.")
    if not isinstance(chars, str) or not chars:
        raise ValueError("Characters string 'chars' cannot be empty.")
    return ''.join(random.choices(chars, k=length))

def get_env_variable(env_key: str, default_value: Optional[Any] = None) -> Optional[Any]:
    """Retrieves an environment variable, returning a default value if not found."""
    if not isinstance(env_key, str):
        # Or log a warning and return default_value
        raise TypeError("Environment variable key 'env_key' must be a string.")
    return os.environ.get(env_key, default_value)

def chunk_list(input_list: List[Any], chunk_size: int) -> Generator[List[Any], None, None]:
    """Yields successive n-sized chunks from input_list."""
    if not isinstance(input_list, list):
        raise TypeError("Input 'input_list' must be a list.")
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer.")
    
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]

def safe_json_loads(json_string: Optional[str], default_value: Optional[Any] = None) -> Optional[Any]:
    """
    Safely loads a JSON string, returning default_value on error.
    Handles None input gracefully.
    """
    if json_string is None:
        return default_value
    if not isinstance(json_string, str):
        # Consider logging a warning if type is unexpected
        # For now, per SDS, try to proceed which will likely fail in json.loads
        # or return default if json.loads raises TypeError.
        pass

    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError) as e:
        # Log the error for diagnostics if needed
        # import logging
        # _logger = logging.getLogger(__name__)
        # _logger.debug(f"Failed to parse JSON string: '{json_string}'. Error: {e}")
        return default_value