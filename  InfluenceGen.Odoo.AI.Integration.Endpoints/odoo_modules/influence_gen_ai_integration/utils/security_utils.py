# -*- coding: utf-8 -*-
import logging
import hmac
import odoo

_logger = logging.getLogger(__name__)

def validate_n8n_callback_token(odoo_env, received_token):
    """
    Validates the token received in an N8N callback against the expected secret.

    Uses hmac.compare_digest for secure comparison against timing attacks.

    :param odoo_env: Odoo environment (e.g., http.request.env or self.env).
    :param received_token: The token string received from N8N.
    :return: True if tokens match, False otherwise.
    """
    try:
        # Access ir.config_parameter using sudo as it's a system setting
        expected_token = odoo_env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_callback_token')

        if not expected_token or 'PLACEHOLDER' in expected_token:
            _logger.error("N8N callback token is not configured or is a placeholder in Odoo settings.")
            return False

        if not isinstance(received_token, str) or not received_token:
             _logger.warning("Received N8N callback token is empty or not a string.")
             # Use a dummy comparison to avoid timing leaks if received_token is invalid type/value
             dummy_received_token = "" if received_token is None else str(received_token)
             # Encode expected_token only once
             expected_token_bytes = expected_token.encode('utf-8')
             return hmac.compare_digest(dummy_received_token.encode('utf-8'), expected_token_bytes)


        # Secure comparison
        # Ensure both strings are encoded bytes before comparison
        expected_token_bytes = expected_token.encode('utf-8')
        received_token_bytes = received_token.encode('utf-8')
        is_valid = hmac.compare_digest(received_token_bytes, expected_token_bytes)

        if not is_valid:
             _logger.warning("N8N callback token validation failed.")
        else:
             _logger.debug("N8N callback token validation successful.")

        return is_valid

    except Exception as e:
        _logger.exception("An error occurred during N8N callback token validation.")
        return False