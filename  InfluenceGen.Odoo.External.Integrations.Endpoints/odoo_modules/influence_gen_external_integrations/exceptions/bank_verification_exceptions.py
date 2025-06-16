# -*- coding: utf-8 -*-
from .common_exceptions import ExternalServiceError

class BankVerificationServiceError(ExternalServiceError):
    """Base class for bank verification service specific errors. REQ-IOKYC-008, REQ-IPF-002"""
    def __init__(self, message, original_exception=None):
        super().__init__(message, service_name="BankVerificationService", original_exception=original_exception)
        # self.message is already set by super().__init__


class BankAccountInvalidError(BankVerificationServiceError):
    """Raised when the bank account details are considered invalid by the service. REQ-IOKYC-008, REQ-IPF-002"""
    # Inherits __init__ and __str__ from BankVerificationServiceError
    pass


class BankVerificationFailedError(BankVerificationServiceError):
    """Raised when bank account verification explicitly fails. REQ-IOKYC-008, REQ-IPF-002"""
    def __init__(self, message, reason_code=None, original_exception=None):
        super().__init__(message, original_exception=original_exception)
        self.reason_code = reason_code
        # self.message is already set by super().__init__

    def __str__(self):
        base_str = super().__str__()
        if self.reason_code:
            return f"{base_str} (Reason Code: {self.reason_code})"
        return base_str