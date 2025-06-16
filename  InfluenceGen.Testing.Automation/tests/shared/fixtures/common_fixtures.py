import pytest
import os
import json
import uuid
import logging
from dotenv import load_dotenv
from tests.shared.utils.api_client_base import APIClientBase # Assuming api_client_base.py is in tests/shared/utils/

# Configure logging
logger = logging.getLogger(__name__)

@pytest.fixture(scope='session', autouse=True)
def load_env_vars():
    """
    pytest fixture to automatically load environment variables from a .env file
    at the beginning of the test session.
    """
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env') # Path to root .env
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        logger.info(f".env file loaded from {env_path}")
    else:
        # Fallback to current directory or default dotenv behavior if root .env not found
        load_dotenv() 
        logger.info(".env file loaded using default dotenv behavior (or not found in root, trying local).")


@pytest.fixture(scope='session')
def environment_config():
    """
    pytest fixture to load environment-specific configuration from a JSON file.
    The environment is determined by the TEST_ENV environment variable.
    Placeholders in the JSON config (ending with _PLACEHOLDER) are replaced
    by actual values from environment variables.

    Returns:
        dict: A dictionary containing the loaded and resolved environment configuration.

    Raises:
        pytest.fail: If the configuration file is not found or cannot be parsed,
                     or if a placeholder variable is not found in the environment.
    """
    env_name = os.getenv("TEST_ENV", "staging")  # Default to 'staging' if TEST_ENV is not set
    logger.info(f"Loading environment configuration for TEST_ENV='{env_name}'")
    
    # Construct path relative to this fixtures file: ../../config/environments/{env_name}_config.json
    # Assuming this file is in tests/shared/fixtures/
    config_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'environments')
    config_file_path = os.path.join(config_dir, f"{env_name}_config.json")

    if not os.path.exists(config_file_path):
        error_msg = f"Environment configuration file not found: {config_file_path}"
        logger.error(error_msg)
        pytest.fail(error_msg)
        return {} # Should not reach here due to pytest.fail

    try:
        with open(config_file_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        error_msg = f"Error decoding JSON from environment configuration file {config_file_path}: {e}"
        logger.error(error_msg)
        pytest.fail(error_msg)
        return {} # Should not reach here

    resolved_config = {}
    missing_placeholders = []
    for key, value in config.items():
        if isinstance(value, str) and value.endswith("_PLACEHOLDER"):
            env_var_name = value.replace("_PLACEHOLDER", "")
            env_var_value = os.getenv(env_var_name)
            if env_var_value is None:
                logger.warning(f"Environment variable for placeholder '{value}' (i.e., '{env_var_name}') not set.")
                # Option: Fail test or use a default marker, or allow it to be None
                # For now, let's mark it as missing and proceed, tests using it might fail or handle None
                missing_placeholders.append(env_var_name)
                resolved_config[key] = f"MISSING_ENV_VAR_{env_var_name}" # Or None
            else:
                resolved_config[key] = env_var_value
        else:
            resolved_config[key] = value
    
    if missing_placeholders:
        logger.warning(f"Some placeholder environment variables were not found: {', '.join(missing_placeholders)}")
        # Decide if this should be a failure:
        # pytest.fail(f"Missing environment variables for placeholders: {', '.join(missing_placeholders)}")


    logger.info(f"Environment configuration loaded successfully for '{env_name}'.")
    return resolved_config


@pytest.fixture(scope='session')
def odoo_api_client_session(environment_config: dict):
    """
    pytest fixture to provide an APIClientBase instance configured for Odoo API,
    scoped for the entire test session.
    The base URL is taken from the 'odoo_api_base_url' key in the environment_config.
    Authentication token might be set if 'default_test_api_token' is in config.
    """
    base_url_key = "odoo_api_base_url" # Key as defined in staging_config.json
    default_token_key = "default_test_api_token" # Example key for a potential default token

    base_url = environment_config.get(base_url_key)
    if not base_url or base_url.startswith("MISSING_ENV_VAR_"):
        pytest.fail(f"'{base_url_key}' not found or placeholder unresolved in environment configuration for Odoo API client.")
        return None # Should not reach

    client = APIClientBase(default_base_url=base_url) # Pass loaded base_url as default to constructor

    # Example: Attempt to set a default auth token if provided in config
    # This assumes the token itself is the value, not another placeholder for the token
    api_token = environment_config.get(default_token_key)
    if api_token and not api_token.startswith("MISSING_ENV_VAR_"):
        client.set_auth_token(api_token)
    elif api_token and api_token.startswith("MISSING_ENV_VAR_"):
        logger.warning(f"Default API token key '{default_token_key}' was a placeholder but its env var was not found.")
    
    logger.info(f"Odoo API client (session scope) initialized for base URL: {client.base_url}")
    return client

@pytest.fixture(scope='function')
def odoo_api_client_function(environment_config: dict):
    """
    pytest fixture to provide a new APIClientBase instance for each test function.
    Useful if tests modify client state (e.g., auth token) and need isolation.
    """
    base_url_key = "odoo_api_base_url"
    default_token_key = "default_test_api_token"

    base_url = environment_config.get(base_url_key)
    if not base_url or base_url.startswith("MISSING_ENV_VAR_"):
        pytest.fail(f"'{base_url_key}' not found or placeholder unresolved in environment configuration for Odoo API client.")
        return None

    client = APIClientBase(default_base_url=base_url)

    api_token = environment_config.get(default_token_key)
    if api_token and not api_token.startswith("MISSING_ENV_VAR_"):
        client.set_auth_token(api_token)
    elif api_token and api_token.startswith("MISSING_ENV_VAR_"):
        logger.warning(f"Default API token key '{default_token_key}' was a placeholder but its env var was not found.")

    logger.debug(f"Odoo API client (function scope) initialized for base URL: {client.base_url}")
    return client

@pytest.fixture
def generate_random_email() -> str:
    """
    pytest fixture to generate a random email address for test purposes.
    Ensures uniqueness for creating new user accounts.
    """
    return f"test.user.{uuid.uuid4().hex[:8]}@influencegen-test.com"

@pytest.fixture
def generate_random_string(length: int = 10) -> str:
    """
    pytest fixture to generate a random string of a given length.
    Can be used for names, passwords, etc.
    """
    return uuid.uuid4().hex[:length]

# Example Playwright-specific fixture if using PyTest as a runner for Playwright tests
# This would typically be in a Playwright-specific conftest.py or common_fixtures.py
# if using PyTest to orchestrate Playwright.

# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args, environment_config):
#     """
#     Example fixture to extend Playwright's browser_context_args.
#     Sets the baseURL for Playwright page fixtures.
#     """
#     base_url = environment_config.get("odoo_app_url")
#     if not base_url or base_url.startswith("MISSING_ENV_VAR_"):
#         pytest.fail("'odoo_app_url' not found or placeholder unresolved for Playwright baseURL.")
    
#     return {
#         **browser_context_args,
#         "base_url": base_url,
#         # Add other context args like viewport, locale, timezone, etc. if needed
#         # "viewport": {"width": 1920, "height": 1080},
#     }

# Note: For Playwright's native test runner (not via PyTest), fixtures are often
# defined within the Playwright test files themselves or through its own config.
# This file is primarily for PyTest-driven fixtures.