import requests
import os
from dotenv import load_dotenv
import logging

# Configure logging
logger = logging.getLogger(__name__)

class APIClientBase:
    """
    Base utility for creating HTTP API clients used in integration and E2E API tests.
    Provides a common foundation for making HTTP requests to various APIs under test.
    Contains methods for common HTTP verbs (GET, POST, PUT, DELETE),
    handling authentication (e.g., token injection), setting common headers,
    and basic response parsing or error handling. Uses the `requests` library.
    """

    def __init__(self, base_url_env_key="BASE_URL", default_base_url="http://localhost:8069"):
        """
        Initializes the APIClientBase.

        Args:
            base_url_env_key (str): The environment variable key for the base URL.
            default_base_url (str): The default base URL if the environment variable is not set.
        """
        load_dotenv()
        self.base_url = os.getenv(base_url_env_key, default_base_url)
        if not self.base_url:
            logger.error(f"Base URL not found for env key {base_url_env_key} and no default was provided.")
            raise ValueError(f"Base URL must be set via environment variable {base_url_env_key} or a default_base_url.")

        self.session = requests.Session()
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.session.headers.update(self.default_headers)
        self.auth_token = None
        # Attempt to load a default token if available from environment
        # This could be a static test user token for example
        default_token = os.getenv("DEFAULT_API_AUTH_TOKEN")
        if default_token:
            self.set_auth_token(default_token)

    def set_auth_token(self, token: str):
        """
        Sets the authentication token for the session.

        Args:
            token (str): The authentication token (e.g., Bearer token).
        """
        if token:
            self.auth_token = token
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            logger.debug("Authentication token set.")
        else:
            self.auth_token = None
            if 'Authorization' in self.session.headers:
                del self.session.headers['Authorization']
            logger.debug("Authentication token removed.")

    def _make_request(self, method: str, endpoint: str, params=None, data=None, json_payload=None, headers=None, **kwargs) -> requests.Response:
        """
        Internal method to make an HTTP request.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): API endpoint path.
            params (dict, optional): URL parameters.
            data (dict, optional): Form data for the request body.
            json_payload (dict, optional): JSON data for the request body.
            headers (dict, optional): Additional request headers.
            **kwargs: Additional keyword arguments to pass to requests.request.

        Returns:
            requests.Response: The HTTP response object.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        merged_headers = self.session.headers.copy()
        if headers:
            merged_headers.update(headers)

        logger.debug(f"Making {method} request to {url} with params={params}, json_payload={json_payload}, headers={merged_headers}")

        try:
            response = self.session.request(
                method,
                url,
                params=params,
                data=data,
                json=json_payload,
                headers=merged_headers,
                **kwargs
            )
            logger.debug(f"Response received: Status {response.status_code}, Body: {response.text[:500]}...") # Log first 500 chars
            # Optionally, raise HTTPError for bad responses (4xx or 5xx) immediately
            # response.raise_for_status() 
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request Failed to {url}: {e}", exc_info=True)
            raise

    def get(self, endpoint: str, params=None, headers=None, **kwargs) -> requests.Response:
        """
        Sends a GET request.
        """
        return self._make_request("GET", endpoint, params=params, headers=headers, **kwargs)

    def post(self, endpoint: str, data=None, json_payload=None, headers=None, **kwargs) -> requests.Response:
        """
        Sends a POST request.
        """
        return self._make_request("POST", endpoint, data=data, json_payload=json_payload, headers=headers, **kwargs)

    def put(self, endpoint: str, data=None, json_payload=None, headers=None, **kwargs) -> requests.Response:
        """
        Sends a PUT request.
        """
        return self._make_request("PUT", endpoint, data=data, json_payload=json_payload, headers=headers, **kwargs)

    def delete(self, endpoint: str, headers=None, **kwargs) -> requests.Response:
        """
        Sends a DELETE request.
        """
        return self._make_request("DELETE", endpoint, headers=headers, **kwargs)

    def patch(self, endpoint: str, data=None, json_payload=None, headers=None, **kwargs) -> requests.Response:
        """
        Sends a PATCH request.
        """
        return self._make_request("PATCH", endpoint, data=data, json_payload=json_payload, headers=headers, **kwargs)