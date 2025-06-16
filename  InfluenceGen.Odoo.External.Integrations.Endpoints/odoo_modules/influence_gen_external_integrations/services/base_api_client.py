# -*- coding: utf-8 -*-
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import requests # For type hinting requests.Response

from odoo import api, models
from odoo.addons.influence_gen_external_integrations.utils.http_client_wrapper import HttpClientWrapper
# Correct import for IntegrationSettings service
# from odoo.addons.influence_gen_external_integrations.config.integration_settings import IntegrationSettings
from odoo.addons.influence_gen_external_integrations.exceptions.common_exceptions import ConfigurationError, ApiCommunicationError, ExternalServiceError

_logger = logging.getLogger(__name__)

# Inherit from models.AbstractModel to get access to self.env
class BaseAPIClient(models.AbstractModel):
    _name = 'influence_gen.base.api.client'
    _description = 'Base API Client for External Services'

    # These would be set by subclasses
    SERVICE_NAME: str = "GenericService"
    BASE_URL_PARAM: str = "influence_gen.generic_service.base_url" # e.g., 'influence_gen.kyc_service.base_url'
    API_KEY_PARAM: Optional[str] = "influence_gen.generic_service.api_key" # e.g., 'influence_gen.kyc_service.api_key', can be None if no API key

    @api.model
    def _get_service_config(self) -> tuple[str, Optional[str]]:
        """
        Retrieves base URL and API key for the service from Odoo parameters
        using the IntegrationSettings service.

        :return: A tuple (base_url, api_key).
        :raises ConfigurationError: If critical configuration is missing.
        """
        settings_service = self.env['influence_gen.integration.settings']

        base_url = settings_service._get_param(self.BASE_URL_PARAM)

        api_key = None
        if self.API_KEY_PARAM: # Only try to get API key if param name is defined for the service
            api_key = settings_service._get_param(self.API_KEY_PARAM, default=None)

        if not base_url:
            _logger.error(f"Base URL for {self.SERVICE_NAME} not configured (param: {self.BASE_URL_PARAM}).")
            raise ConfigurationError(
                message=f"Base URL for {self.SERVICE_NAME} is not configured.",
                service_name=self.SERVICE_NAME,
                setting_key=self.BASE_URL_PARAM
            )

        # API key check: Warn if API_KEY_PARAM is defined but no key is found.
        # Specific services can raise ConfigurationError in their _get_default_headers if key is mandatory.
        if self.API_KEY_PARAM and not api_key:
             _logger.warning(f"API Key for {self.SERVICE_NAME} not configured (param: {self.API_KEY_PARAM}). Service calls might fail if API key is required.")

        return base_url, api_key

    @api.model
    def _get_default_headers(self, api_key: Optional[str] = None) -> Dict[str, str]:
        """
        Provides default headers for API requests.
        Subclasses must override to add service-specific authentication headers.

        :param api_key: The API key, if applicable for the service.
        :return: Dictionary of default headers.
        """
        headers = {
            'Accept': 'application/json',
            # Note: 'Content-Type': 'application/json' is typically added by HttpClientWrapper
            # when json_data is provided.
        }
        # Subclasses should add specific auth headers here, e.g.:
        # if api_key:
        #     headers['Authorization'] = f'Bearer {api_key}'
        # or
        #     headers['X-API-KEY'] = api_key
        return headers

    @api.model
    def _get_sensitive_headers_to_mask(self) -> List[str]:
        """
        Returns a list of header names whose values should be masked in logs.
        Subclasses should override this to include their specific sensitive headers.
        Example: ['Authorization', 'X-Api-Key']
        """
        return ['Authorization', 'X-Api-Key', 'Api-Key'] # Common sensitive headers

    @api.model
    def _get_sensitive_json_fields_to_mask(self) -> List[str]:
        """
        Returns a list of JSON field names (top-level) whose values should be masked
        if JSON request/response bodies are logged.
        Subclasses should override this.
        Example: ['password', 'access_token', 'document_image_b64']
        """
        return ['password', 'token', 'secret', 'key'] # Common sensitive fields

    @api.model
    def _handle_api_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handles the API response, parsing JSON.
        This method is called *after* HttpClientWrapper.request has checked for non-2xx status.

        :param response: The requests.Response object.
        :return: Parsed JSON dictionary.
        :raises ApiCommunicationError: If JSON parsing fails.
        """
        try:
            # Check if response content is empty before trying to parse JSON
            if not response.content:
                _logger.info(f"Response from {self.SERVICE_NAME} has no content. Returning empty dict.")
                return {}
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            _logger.error(
                f"Failed to decode JSON response from {self.SERVICE_NAME}. "
                f"Status: {response.status_code}, URL: {response.url}. "
                f"Response text: {response.text[:500]}{'...' if len(response.text) > 500 else ''}"
            )
            raise ApiCommunicationError(
                message=f"Invalid JSON response from {self.SERVICE_NAME}.",
                service_name=self.SERVICE_NAME,
                status_code=response.status_code,
                response_content=response.text,
                original_exception=e
            )

    @api.model
    def _make_request(self, method: str, endpoint: str,
                      headers_override: Optional[Dict[str, str]] = None,
                      json_data: Optional[Dict[str, Any]] = None,
                      params: Optional[Dict[str, Any]] = None,
                      data: Any = None
                     ) -> Dict[str, Any]:
        """
        Helper method to make a request to the service using HttpClientWrapper.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param endpoint: API endpoint path (e.g., '/users/1').
        :param headers_override: Dictionary of headers to add or override default ones.
        :param json_data: Dictionary to be sent as JSON in the request body.
        :param params: Dictionary of URL parameters for GET requests.
        :param data: Data for form-encoded POST requests.
        :return: Parsed JSON response as a dictionary.
        :raises ConfigurationError: If service configuration is missing.
        :raises ApiCommunicationError: For network issues or non-2xx HTTP responses.
        :raises ExternalServiceError: For other unexpected errors during the process.
        """
        base_url, api_key = self._get_service_config() # Can raise ConfigurationError

        # Ensure base_url ends without / and endpoint starts with / (or is empty)
        full_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/') if endpoint else ''}"

        final_headers = self._get_default_headers(api_key) # Can raise ConfigurationError if API key mandatory and missing
        if headers_override:
            final_headers.update(headers_override)

        try:
            _logger.debug(
                f"Making {method} request to {self.SERVICE_NAME}: URL={full_url}, Params={params}, "
                f"Headers (before masking for HttpClientWrapper)={final_headers}, "
                f"JSONData provided: {'Yes' if json_data is not None else 'No'}, "
                f"Data provided: {'Yes' if data is not None else 'No'}"
            )
            response_obj = HttpClientWrapper.request(
                method=method,
                url=full_url,
                headers=final_headers,
                json_data=json_data,
                params=params,
                data=data,
                service_name=self.SERVICE_NAME,
                mask_sensitive_headers=self._get_sensitive_headers_to_mask(),
                mask_sensitive_json_fields=self._get_sensitive_json_fields_to_mask()
            )
            return self._handle_api_response(response_obj)
        except ApiCommunicationError: # Already logged by HttpClientWrapper, re-raise
            raise
        except ConfigurationError: # Raised by _get_service_config or _get_default_headers
            raise
        except Exception as e: # Catch any other unexpected errors
            _logger.exception(f"Unexpected error during API request preparation or handling to {self.SERVICE_NAME} at {endpoint}: {e}")
            raise ExternalServiceError(
                message=f"Unexpected error interacting with {self.SERVICE_NAME}.",
                service_name=self.SERVICE_NAME,
                original_exception=e
            )