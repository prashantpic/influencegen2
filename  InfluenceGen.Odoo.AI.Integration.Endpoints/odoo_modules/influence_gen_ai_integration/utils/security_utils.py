# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hmac
import logging

_logger = logging.getLogger(__name__)

def validate_n8n_callback_token(odoo_env, received_token):
    """
    Validates the N8N callback token.
    REQ-IL-016: Secure handling of API keys and tokens for communication.
    REQ-IL-008: Secure credential storage (token fetched from ir.config_parameter).
    """
    try:
        expected_token = odoo_env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_callback_token')

        if not expected_token:
            _logger.error("N8N callback token ('influence_gen.n8n_callback_token') is not configured in Odoo system parameters.")
            return False

        if received_token is None:
            _logger.warning("No token received in N8N callback.")
            return False

        # Use hmac.compare_digest for constant-time comparison to mitigate timing attacks
        is_valid = hmac.compare_digest(
            str(received_token).encode('utf-8'),
            str(expected_token).encode('utf-8')
        )

        if not is_valid:
            _logger.warning("Invalid N8N callback token received.")
        else:
            _logger.info("N8N callback token validated successfully.")
        return is_valid

    except Exception as e:
        _logger.exception("Error during N8N callback token validation: %s", e)
        return False