# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import hmac
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

N8N_CALLBACK_AUTH_TOKEN_PARAM = 'influence_gen.n8n_callback_auth_token'
N8N_SIGNATURE_HEADER = 'X-N8N-Signature' # As per SDS section 4.7.1 and 4.6.2


def verify_n8n_request(odoo_request: http.Request) -> bool:
    """
    Verifies the authenticity of an incoming N8N callback request.

    This function checks for a shared secret token in the request headers
    against a configured value in Odoo's system parameters. It uses
    `hmac.compare_digest` for secure, constant-time string comparison
    to mitigate timing attacks.

    REQ-IL-004: Implement secure authentication for N8N callbacks.
    REQ-IL-016: Use shared secret/token for N8N callback authentication.
    REQ-PAC-017: Retrieve N8N callback token from system parameters.

    :param odoo_request: The Odoo `http.Request` object representing the
                         incoming HTTP request from N8N.
    :type odoo_request: odoo.http.Request
    :return: `True` if the request is authentic, `False` otherwise.
    :rtype: bool
    """
    config_parameter_sudo = request.env['ir.config_parameter'].sudo()
    expected_token = config_parameter_sudo.get_param(N8N_CALLBACK_AUTH_TOKEN_PARAM)

    if not expected_token:
        _logger.critical(
            "N8N callback authentication failed: The system parameter '%s' is not configured. "
            "Cannot authenticate N8N callbacks.",
            N8N_CALLBACK_AUTH_TOKEN_PARAM
        )
        return False

    provided_token = odoo_request.httprequest.headers.get(N8N_SIGNATURE_HEADER)

    if not provided_token:
        _logger.warning(
            "N8N callback authentication failed: Missing '%s' header in the request.",
            N8N_SIGNATURE_HEADER
        )
        return False

    # Ensure both tokens are encoded to bytes for hmac.compare_digest
    try:
        expected_token_bytes = expected_token.encode('utf-8')
        provided_token_bytes = provided_token.encode('utf-8')
    except AttributeError:
        _logger.error(
            "N8N callback authentication failed: Error encoding tokens to bytes. "
            "Ensure tokens are strings."
        )
        return False


    if hmac.compare_digest(expected_token_bytes, provided_token_bytes):
        _logger.info("N8N callback authentication successful.")
        return True
    else:
        _logger.warning(
            "N8N callback authentication failed: Invalid token provided in '%s' header. "
            "Provided token (first 5 chars): %s...",
            N8N_SIGNATURE_HEADER,
            provided_token[:5] # Log a snippet for debugging, avoid logging full token
        )
        return False