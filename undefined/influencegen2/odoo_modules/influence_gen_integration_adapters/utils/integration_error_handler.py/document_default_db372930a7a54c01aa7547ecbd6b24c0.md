# odoo_modules/influence_gen_integration_adapters/utils/integration_error_handler.py
import logging
import requests

_logger = logging.getLogger(__name__)

class IntegrationServiceError(Exception):
    """Base class for errors related to external integration services."""
    def __init__(self, message, status_code=None, service_name=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.service_name = service_name
        self.response_text = response_text

class TransientIntegrationError(IntegrationServiceError):
    """For temporary errors that might be resolved by retrying."""
    pass

class PermanentIntegrationError(IntegrationServiceError):
    """For errors unlikely to be resolved by retrying the same request."""
    pass

class AuthenticationError(PermanentIntegrationError):
    """Specific for authentication failures (401, 403) with external services."""
    pass

class RateLimitError(TransientIntegrationError):
    """Specific for rate limit responses (429) from external services."""
    pass

class BadRequestError(PermanentIntegrationError):
    """Specific for bad request errors (4xx) from external services, indicating an issue with the request."""
    pass


def handle_external_api_error(response: requests.Response, service_name: str):
    """
    Handles errors from external API calls based on the HTTP response.

    Args:
        response: The `requests.Response` object from the API call.
        service_name: A string identifying the external service (e.g., "N8N AI Service").

    Raises:
        AuthenticationError: For 401 or 403 status codes.
        RateLimitError: For 429 status code.
        TransientIntegrationError: For 500, 502, 503, 504 status codes.
        BadRequestError: For other 4xx status codes indicating client-side errors.
        PermanentIntegrationError: For other 5xx status codes or unhandled errors.
    
    Returns:
        None if the response status code is 2xx (successful).
    """
    if response.ok: # Covers 2xx status codes
        return

    error_message_template = (
        f"Error calling {service_name}. "
        f"Status: {response.status_code}. "
        f"Response: {response.text[:500]}" # Log a snippet of the response
    )
    _logger.error(error_message_template)

    status_code = response.status_code
    error_details = {
        "status_code": status_code,
        "service_name": service_name,
        "response_text": response.text,
    }

    if status_code in (401, 403):
        raise AuthenticationError(
            f"Authentication failed with {service_name}. Status: {status_code}.",
            **error_details
        )
    elif status_code == 429:
        raise RateLimitError(
            f"Rate limit exceeded for {service_name}. Status: {status_code}.",
            **error_details
        )
    elif status_code in (500, 502, 503, 504):
        raise TransientIntegrationError(
            f"Transient error from {service_name}. Status: {status_code}. Retry may succeed.",
            **error_details
        )
    elif 400 <= status_code < 500:
        raise BadRequestError(
            f"Bad request to {service_name}. Status: {status_code}. Check request payload/parameters.",
            **error_details
        )
    elif 500 <= status_code < 600: # Other 5xx errors
        raise PermanentIntegrationError(
            f"Permanent server-side error from {service_name}. Status: {status_code}.",
            **error_details
        )
    else: # Should not happen if response.ok is false, but as a fallback
        raise IntegrationServiceError(
            f"Unhandled error from {service_name}. Status: {status_code}.",
            **error_details
        )