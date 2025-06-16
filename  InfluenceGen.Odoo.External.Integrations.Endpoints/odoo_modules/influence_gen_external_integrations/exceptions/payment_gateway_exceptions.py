# -*- coding: utf-8 -*-
from .common_exceptions import ExternalServiceError

class PaymentGatewayError(ExternalServiceError):
    """Base class for payment gateway specific errors. REQ-IPF-012"""
    def __init__(self, message, gateway_name=None, original_exception=None):
        super().__init__(message, service_name=f"PaymentGateway({gateway_name or 'Unknown'})", original_exception=original_exception)
        self.gateway_name = gateway_name
        # self.message is already set by super().__init__


class PaymentProcessingError(PaymentGatewayError):
    """Raised when a payment processing attempt fails at the gateway. REQ-IPF-012"""
    def __init__(self, message, gateway_name=None, error_code=None, original_exception=None):
        super().__init__(message, gateway_name=gateway_name, original_exception=original_exception)
        self.error_code = error_code
        # self.message is already set by super().__init__

    def __str__(self):
        base_str = super().__str__()
        if self.error_code:
            return f"{base_str} (Error Code: {self.error_code})"
        return base_str


class PaymentConfigurationError(PaymentGatewayError):
    """Raised for configuration issues related to a payment gateway. REQ-IPF-012"""
    def __init__(self, message, gateway_name=None, setting_key=None, original_exception=None):
         super().__init__(message, gateway_name=gateway_name, original_exception=original_exception)
         self.setting_key = setting_key
         # self.message is already set by super().__init__

    def __str__(self):
        base_str = super().__str__()
        if self.setting_key:
            return f"{base_str} (Setting key: {self.setting_key})"
        return base_str