# -*- coding: utf-8 -*-
import hashlib
from typing import Optional, Any
import odoo # For accessing odoo.env

# As per SDS 5.2.11 for _logger initialization
# This relies on the module 'influence_gen_shared_core' being in odoo.addons path
# and its utils.logging_utils being importable this way.
# A more common relative import would be `from ..utils import logging_utils`
# then `_logger = logging_utils.get_logger(__name__)`.
# Following SDS strictly:
try:
    _logger = odoo.addons.influence_gen_shared_core.utils.logging_utils.get_logger(__name__)
except AttributeError:
    # Fallback if the above path is not immediately resolvable during module loading phase
    # or if odoo.addons is not yet fully populated.
    import logging
    _logger = logging.getLogger(__name__)
    _logger.warning(
        "Could not initialize logger via odoo.addons path in security_utils.py. Using standard logger."
    )


def get_config_parameter(param_name: str, default_value: Optional[Any] = None) -> Optional[Any]:
    """
    Securely retrieves a configuration parameter from Odoo's ir.config_parameter.
    It is recommended to use this for non-secret parameters. For secrets, use Odoo's
    secrets management or an external vault. This function acts as a wrapper.
    """
    try:
        # Odoo's get_param is the standard way.
        # Ensure this utility is used within an Odoo environment context.
        if hasattr(odoo, 'env') and odoo.env and 'ir.config_parameter' in odoo.env:
            # sudo() might be needed if access rights are an issue for certain params
            # but generally not for read if the param is system-wide.
            # Use with caution if sudo() is applied.
            # The SDS specifies sudo(), so we adhere to it.
            value = odoo.env['ir.config_parameter'].sudo().get_param(param_name, default_value)
            return value
        else:
            # Fallback or error if not in Odoo env context
            _logger.warning(f"Odoo environment or ir.config_parameter model not available for get_config_parameter: {param_name}") # NOSONAR
            return default_value
    except Exception as e:
        _logger.error(f"Error retrieving config parameter '{param_name}': {e}", exc_info=True) # NOSONAR
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
    _logger.info(f"Attempting to retrieve secret: {secret_name}") # NOSONAR - Logging intent to retrieve
    # Ensure the return type is Optional[str] as per type hint
    value = get_config_parameter(secret_name, default_value)
    if value is not None and not isinstance(value, str):
        _logger.warning(f"Secret '{secret_name}' retrieved was not a string, converting. Type: {type(value)}")
        try:
            return str(value)
        except Exception:
            _logger.error(f"Could not convert secret '{secret_name}' to string.")
            return default_value # Or raise an error
    return value


def hash_data_sha256(data: str) -> str:
    """Hashes a string using SHA-256."""
    if not isinstance(data, str):
        # As per SDS, raise TypeError.
        # Alternatively, could log and return a default or attempt conversion.
        raise TypeError("Input data must be a string for SHA-256 hashing.")
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Note: Password verification should almost always use Odoo's built-in mechanisms
# which handle salt and hashing specifics (e.g., self.env.user._check_password(password)
# or tools.verify_password). Avoid reimplementing password verification.