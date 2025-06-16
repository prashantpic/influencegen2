import pytest
import uuid
# Assuming APIClientBase is in tests.shared.utils.api_client_base
# from tests.shared.utils.api_client_base import APIClientBase
# Assuming common_fixtures.py provides odoo_api_client_function and environment_config
# from tests.shared.fixtures.common_fixtures import odoo_api_client_function, environment_config

# Placeholder for odoo_test_utils if used for verification
# from tests.shared.utils.odoo_test_utils import get_ai_request_status, get_generated_image_details

@pytest.mark.integration
@pytest.mark.api
class TestN8NCallbackAPI:
    """
    Integration tests for the Odoo API endpoint that receives AI image generation results from N8N.
    Validates API authentication, request/response format, and processing of callback data.
    """

    CALLBACK_ENDPOINT = "/influence_gen/n8n/ai_image_callback" # As per SDS

    @pytest.fixture
    def sample_ai_request_id(self):
        """Generates a sample UUID for AI request ID."""
        return str(uuid.uuid4())

    @pytest.fixture
    def successful_image_payload(self, sample_ai_request_id):
        """Payload for a successful image generation callback."""
        return {
            "request_id": sample_ai_request_id,
            "status": "completed",
            "image_url": f"https://cdn.example.com/images/{sample_ai_request_id}.png",
            "image_metadata": {
                "width": 1024,
                "height": 1024,
                "format": "png",
                "seed": 1234567890
            }
        }

    @pytest.fixture
    def failed_image_payload(self, sample_ai_request_id):
        """Payload for a failed image generation callback."""
        return {
            "request_id": sample_ai_request_id,
            "status": "failed",
            "error_message": "AI model timeout during generation."
        }

    @pytest.fixture
    def malformed_payload(self, sample_ai_request_id):
        """Malformed payload missing required fields."""
        return {
            "request_id": sample_ai_request_id
            # Missing 'status'
        }

    # @pytest.fixture
    # def setup_ai_request_in_odoo(self, sample_ai_request_id):
    #     """
    #     Placeholder fixture: In a real scenario, this would ensure an
    #     AIImageGenerationRequest record exists in Odoo with the sample_ai_request_id
    #     and is in a 'processing' state. This might involve direct DB interaction
    #     or using odoo_test_utils if tests are run within Odoo context or via an Odoo client lib.
    #     For now, we assume the endpoint can handle a valid request_id without pre-setup for basic tests.
    #     """
    #     print(f"Simulating setup for AI Request ID: {sample_ai_request_id} in Odoo.")
    #     # Example: odoo_test_utils.create_ai_request(sample_ai_request_id, status='processing')
    #     return sample_ai_request_id


    def test_successful_image_result_callback(self, odoo_api_client_function, successful_image_payload, environment_config):
        """
        Tests REQ-DTS-003: Ensures the Odoo callback API for N8N functions correctly for successful image results.
        Verifies that a successful image generation callback is processed correctly by Odoo.
        """
        # Prerequisite: An AIImageGenerationRequest with successful_image_payload['request_id'] should exist
        # in a 'processing' state in Odoo. This might be handled by a setup fixture.
        # For simplicity, we assume the endpoint handles new request_ids appropriately or a fixture would manage this.

        response = odoo_api_client_function.post(self.CALLBACK_ENDPOINT, json_payload=successful_image_payload)

        assert response.status_code == 200, \
            f"Expected HTTP 200 OK, but got {response.status_code}. Response: {response.text}"
        
        response_json = response.json()
        assert response_json.get("status") == "success"
        assert "message" in response_json

        # Verification step (conceptual):
        # In a full test environment, you would verify the Odoo backend:
        # 1. AIImageGenerationRequest status updated to 'completed'.
        # 2. GeneratedImage record created with correct details (image_url, metadata).
        # Example:
        # assert get_ai_request_status(successful_image_payload['request_id']) == 'completed'
        # image_details = get_generated_image_details(successful_image_payload['request_id'])
        # assert image_details is not None
        # assert image_details['url'] == successful_image_payload['image_url']


    def test_failed_image_generation_callback(self, odoo_api_client_function, failed_image_payload, environment_config):
        """
        Tests REQ-DTS-003: Ensures the Odoo callback API for N8N functions correctly for failed image generation.
        Verifies that a failed image generation callback is processed correctly by Odoo.
        """
        # Prerequisite: Similar to the success case, a corresponding AIImageGenerationRequest record setup.

        response = odoo_api_client_function.post(self.CALLBACK_ENDPOINT, json_payload=failed_image_payload)

        assert response.status_code == 200, \
            f"Expected HTTP 200 OK for failure callback, but got {response.status_code}. Response: {response.text}"
        
        response_json = response.json()
        assert response_json.get("status") == "success" # Assuming the API itself returns success for processing the callback
        assert "message" in response_json

        # Verification step (conceptual):
        # 1. AIImageGenerationRequest status updated to 'failed'.
        # 2. Error message logged/stored correctly.
        # Example:
        # assert get_ai_request_status(failed_image_payload['request_id']) == 'failed'
        # assert get_ai_request_error_message(failed_image_payload['request_id']) == failed_image_payload['error_message']

    def test_unauthenticated_callback_rejection(self, odoo_api_client_function, successful_image_payload, environment_config):
        """
        Tests that an unauthenticated attempt to call the callback API is rejected.
        """
        # Create a new client instance without authentication for this test
        unauth_client = odoo_api_client_function
        unauth_client.set_auth_token(None) # Ensure no auth token is set for this client instance
        
        # Odoo's default for unauthenticated JSON controller endpoints is often a 200 with an error JSON,
        # or a 404/redirect if not found or no public access. If specific auth is enforced (e.g. API key header),
        # it might be 401/403. This depends on how the Odoo controller is implemented.
        # For this example, we assume it might return a 200 with an error payload if it's a public endpoint
        # that internally checks a secret, or a 401/403 if using standard Odoo session/API key auth.
        # Let's assume the endpoint is protected and expects a specific auth mechanism not provided here.
        # The APIClientBase might need a way to send requests *without* its default session auth
        # or we'd need a separate unauthenticated client fixture.

        # This test needs to be adjusted based on the actual auth mechanism of the callback endpoint.
        # If it uses a pre-shared key in the payload or a specific header token, this test needs to simulate its absence.
        
        # For now, let's assume it should return 401 if it's a standard protected Odoo API endpoint.
        # We need a client that truly makes an unauthenticated call.
        # The current fixture might still pick up session cookies from a previous auth.
        # A more robust way would be to instantiate a raw requests.post or a new APIClientBase.
        
        import requests
        headers = {'Content-Type': 'application/json'}
        url = f"{unauth_client.base_url.rstrip('/')}/{self.CALLBACK_ENDPOINT.lstrip('/')}"
        
        try:
            response = requests.post(url, json=successful_image_payload, headers=headers)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {e}")

        # Odoo might return 200 with an error JSON for unauthenticated access to some controllers
        # or 401/403 if strict API authentication is in place.
        # Adjust based on expected behavior. If it's webhook validation (e.g., secret in header),
        # this test would omit that secret.
        assert response.status_code in [401, 403, 404], \
            f"Expected HTTP 401/403/404 for unauthenticated access, but got {response.status_code}. Response: {response.text}"
        # If 200 with error, then:
        # response_json = response.json()
        # assert response_json.get("error") and response_json["error"].get("message") == "Authentication required"

    def test_callback_with_invalid_request_id(self, odoo_api_client_function, successful_image_payload, environment_config):
        """
        Tests the callback API's response when provided with a non-existent request_id.
        """
        payload_with_invalid_id = successful_image_payload.copy()
        payload_with_invalid_id["request_id"] = str(uuid.uuid4()) # A new, likely non-existent UUID

        response = odoo_api_client_function.post(self.CALLBACK_ENDPOINT, json_payload=payload_with_invalid_id)
        
        # The expected behavior could be HTTP 404 Not Found if the request_id is not found,
        # or HTTP 400 Bad Request if it's considered an invalid reference,
        # or HTTP 200 with an error message in the JSON body.
        # This depends on the specific implementation of the Odoo controller.
        assert response.status_code in [200, 400, 404], \
             f"Expected HTTP 200 (with error), 400 or 404 for invalid request_id, but got {response.status_code}. Response: {response.text}"

        if response.status_code == 200:
            response_json = response.json()
            assert response_json.get("status") == "error" or "error" in response_json # Check for an error indicator in the JSON
            assert "message" in response_json or "error" in response_json.get("data", {})
        elif response.status_code == 400 or response.status_code == 404:
            # Check for appropriate error message if any
            pass


    def test_callback_with_malformed_payload(self, odoo_api_client_function, malformed_payload, environment_config):
        """
        Tests the callback API's response to a malformed payload (e.g., missing required fields).
        """
        response = odoo_api_client_function.post(self.CALLBACK_ENDPOINT, json_payload=malformed_payload)

        assert response.status_code == 400, \
            f"Expected HTTP 400 Bad Request for malformed payload, but got {response.status_code}. Response: {response.text}"
        
        response_json = response.json()
        assert "error" in response_json or response_json.get("status") == "error" # Check for error indicator
        # Optionally, check for a specific error message related to missing fields.
        # e.g., assert "Missing required field: status" in response_json.get("message", "").lower()