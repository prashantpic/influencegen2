# -*- coding: utf-8 -*-
import logging
from odoo import api, models, _
# from odoo.exceptions import UserError # Not used directly, ConfigurationError is custom

_logger = logging.getLogger(__name__)

class IntegrationSettings(models.AbstractModel):
    """
    Utility class, registered as an Odoo AbstractModel service, 
    to retrieve integration settings securely stored as system parameters (ir.config_parameter).
    REQ-IL-008
    """
    _name = 'influence_gen.integration.settings'
    _description = 'Integration Settings Retrieval Service'

    @api.model
    def _get_param(self, key, default=None):
        """
        Helper method to retrieve a system parameter.
        Accessing ir.config_parameter requires sudo privileges.
        """
        value = self.env['ir.config_parameter'].sudo().get_param(key)
        if not value:
            if default is not None:
                _logger.debug(f"Configuration parameter '{key}' not found, using default value.")
                return default
            _logger.warning(f"Configuration parameter '{key}' not found and no default provided.")
            # Depending on criticality, a ConfigurationError could be raised here by calling code
            # or by the specific getter methods if the parameter is mandatory.
        return value

    @api.model
    def get_kyc_service_api_key(self):
        """Retrieves the API key for the KYC service. REQ-IL-008"""
        key = 'influence_gen.kyc_service.api_key'
        api_key = self._get_param(key)
        if not api_key:
            _logger.error(f"CRITICAL: KYC Service API Key ('{key}') is not configured.")
            # Consider raising ConfigurationError if this is absolutely critical for module function
        return api_key

    @api.model
    def get_kyc_service_base_url(self):
        """Retrieves the base URL for the KYC service."""
        key = 'influence_gen.kyc_service.base_url'
        base_url = self._get_param(key)
        if not base_url:
            _logger.error(f"CRITICAL: KYC Service Base URL ('{key}') is not configured.")
        return base_url

    @api.model
    def get_bank_verification_api_key(self):
        """Retrieves the API key for the bank verification service. REQ-IL-008"""
        key = 'influence_gen.bank_verification.api_key'
        api_key = self._get_param(key)
        if not api_key:
            _logger.error(f"CRITICAL: Bank Verification Service API Key ('{key}') is not configured.")
        return api_key

    @api.model
    def get_bank_verification_base_url(self):
        """Retrieves the base URL for the bank verification service."""
        key = 'influence_gen.bank_verification.base_url'
        base_url = self._get_param(key)
        if not base_url:
            _logger.error(f"CRITICAL: Bank Verification Service Base URL ('{key}') is not configured.")
        return base_url

    @api.model
    def get_payment_gateway_api_key(self, gateway_name: str):
        """
        Retrieves the API key for a specific payment gateway. 
        REQ-IL-008, REQ-IPF-012
        """
        if not gateway_name:
            _logger.error("Gateway name cannot be empty when fetching payment gateway API key.")
            return None
        key = f'influence_gen.payment_gateway.{gateway_name}.api_key'
        api_key = self._get_param(key)
        if not api_key:
            # This might be a warning as not all gateways might be configured or used.
            _logger.warning(f"Payment Gateway API Key for '{gateway_name}' ('{key}') is not configured.")
        return api_key

    @api.model
    def get_payment_gateway_base_url(self, gateway_name: str):
        """
        Retrieves the base URL for a specific payment gateway. 
        REQ-IPF-012
        """
        if not gateway_name:
            _logger.error("Gateway name cannot be empty when fetching payment gateway base URL.")
            return None
        key = f'influence_gen.payment_gateway.{gateway_name}.base_url'
        base_url = self._get_param(key)
        if not base_url:
            _logger.warning(f"Payment Gateway Base URL for '{gateway_name}' ('{key}') is not configured.")
        return base_url