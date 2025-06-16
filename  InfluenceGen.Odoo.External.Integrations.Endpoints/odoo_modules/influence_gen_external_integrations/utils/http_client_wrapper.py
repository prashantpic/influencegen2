# -*- coding: utf-8 -*-
import requests
import logging
from typing import Dict, Any, Optional, List # List added for mask_sensitive_headers

from odoo.addons.influence_gen_external_integrations.exceptions.common_exceptions import ApiCommunicationError

_logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 30  # seconds

class HttpClientWrapper:
    """
    A wrapper for the requests library to standardize HTTP calls, headers, timeouts,
    and basic error handling for external API communications.
    """

    @staticmethod
    def request(method: str, url: str, headers: Optional[Dict[str, str]] = None,
                json_data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None,
                data: Any = None, # requests data parameter for form-data etc.
                timeout: Optional[int] = None, service_name: str = "ExternalService",
                mask_sensitive_headers: Optional[List[str]] = None,
                mask_sensitive_json_fields: Optional[List[str]] = None): # Parameter added as per SDS
        """
        Makes an HTTP request using the requests library.

        :param method: HTTP method (GET, POST, PUT, DELETE, etc.)
        :param url: URL for the request
        :param headers: Dictionary of headers
        :param json_data: Dictionary to be sent as JSON in the request body
        :param params: Dictionary of URL parameters
        :param data: Dictionary, list of tuples, bytes, or file-like object to send in the body (for form-data)
        :param timeout: Request timeout in seconds. Defaults to DEFAULT_TIMEOUT.
        :param service_name: Name of the service being called (for logging/error context).
        :param mask_sensitive_headers: List of header keys whose values should be masked in logs.
        :param mask_sensitive_json_fields: List of JSON field keys whose values should be masked in logs (if body is logged).
        :return: requests.Response object
        :raises ApiCommunicationError: if the request fails due to network issues or returns an HTTP error status code (4xx or 5xx).
        """
        effective_timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        effective_headers = headers.copy() if headers else {} # Use a copy to avoid modifying original

        # Common headers: ensure Content-Type for JSON, and a default Accept header.
        if json_data is not None and 'Content-Type' not in effective_headers:
            effective_headers['Content-Type'] = 'application/json'
        if 'Accept' not in effective_headers:
             effective_headers['Accept'] = 'application/json'

        # Prepare headers for logging, masking sensitive ones
        log_headers = effective_headers.copy()
        if mask_sensitive_headers:
            for key_to_mask in mask_sensitive_headers:
                # Case-insensitive check for header keys
                for h_key in list(log_headers.keys()): # Iterate over a copy of keys for modification
                    if h_key.lower() == key_to_mask.lower():
                        log_headers[h_key] = '***MASKED***'
        
        # Prepare JSON data for logging, masking sensitive fields (if body logging were implemented)
        # For now, as per SDS, body logging is omitted by default for PII safety.
        # If json_data were logged, a similar masking logic would apply using mask_sensitive_json_fields.

        _logger.info(
            f"Sending HTTP {method.upper()} request to {service_name} at {url} "
            f"with params: {params}, headers: {log_headers}"
        )
        # If detailed request body logging is needed for debugging (with masking):
        # if json_data and _logger.isEnabledFor(logging.DEBUG):
        #     log_json_data = {k: (v if k not in (mask_sensitive_json_fields or []) else '***MASKED***') 
        #                      for k,v in json_data.items()}
        #     _logger.debug(f"Request JSON body (masked): {log_json_data}")
        # elif data and _logger.isEnabledFor(logging.DEBUG):
        #     _logger.debug(f"Request data (form/other): Type {type(data)}") # Avoid logging raw form data directly

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=effective_headers,
                json=json_data,
                params=params,
                data=data,
                timeout=effective_timeout
            )
            _logger.info(
                f"Received HTTP {response.status_code} response from {service_name} for {url}. "
                f"Content length: {len(response.content) if response.content else 0} bytes."
            )
            # Raises requests.exceptions.HTTPError for 4xx/5xx responses
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            # Log the error with response details before raising custom exception
            response_text_preview = e.response.text[:500] + ('...' if len(e.response.text) > 500 else '')
            _logger.error(
                f"HTTP error {e.response.status_code} from {service_name} for {url}. Response: {response_text_preview}"
            )
            raise ApiCommunicationError(
                message=f"HTTP error {e.response.status_code} from {service_name}",
                service_name=service_name,
                status_code=e.response.status_code,
                response_content=e.response.text, # Full content for the exception object
                original_exception=e
            )
        except requests.exceptions.Timeout as e:
            _logger.error(f"Timeout connecting to {service_name} at {url}: {e}")
            raise ApiCommunicationError(
                message=f"Timeout connecting to {service_name}.",
                service_name=service_name,
                original_exception=e
            )
        except requests.exceptions.ConnectionError as e:
            _logger.error(f"Connection error with {service_name} at {url}: {e}")
            raise ApiCommunicationError(
                message=f"Connection error with {service_name}.",
                service_name=service_name,
                original_exception=e
            )
        except requests.exceptions.RequestException as e: # Catch other requests-related exceptions
            _logger.error(f"Request exception for {service_name} at {url}: {e}")
            raise ApiCommunicationError(
                message=f"Communication error with {service_name}: {str(e)}",
                service_name=service_name,
                original_exception=e
            )