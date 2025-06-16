# -*- coding: utf-8 -*-
import hmac
import logging

_logger = logging.getLogger(__name__)

def validate_n8n_callback_token(odoo_env, received_token):
    """
    Validates the N8N callback token.
    :param odoo_env: Odoo environment object
    :param received_token: The token received in the callback request
    :return: True if valid, False otherwise
    """
    # THINK:
    # 1. Get the expected token from system parameters.
    # 2. Handle cases where expected token is not configured.
    # 3. Handle cases where received token is None or empty.
    # 4. Perform constant-time comparison using hmac.compare_digest.
    # 5. Log the validation attempt outcome (carefully, not logging tokens in failure cases if too verbose).
    # 6. Return the boolean result.

    expected_token = odoo_env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_callback_token')

    if not expected_token:
        _logger.error("N8N callback token ('influence_gen.n8n_callback_token') is not configured in Odoo system parameters.")
        return False

    if not received_token:
        _logger.warning("Received an empty N8N callback token for validation.")
        return False

    try:
        # Ensure both tokens are strings before encoding
        is_valid = hmac.compare_digest(
            str(received_token).encode('utf-8'),
            str(expected_token).encode('utf-8')
        )
    except Exception as e:
        _logger.exception("Error during token comparison: %s", e)
        return False

    if is_valid:
        _logger.info("N8N callback token validation: Success.")
    else:
        _logger.warning("N8N callback token validation: Failed. Mismatch.")
        # Avoid logging the received_token directly in production logs on failure
        # unless strict security and log access controls are in place.

    return is_valid