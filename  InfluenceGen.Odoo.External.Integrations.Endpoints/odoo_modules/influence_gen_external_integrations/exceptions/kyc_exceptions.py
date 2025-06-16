# -*- coding: utf-8 -*-
from .common_exceptions import ExternalServiceError

class KYCServiceError(ExternalServiceError):
    """Base class for KYC service specific errors. REQ-IOKYC-005, REQ-IL-011"""
    def __init__(self, message, original_exception=None):
        super().__init__(message, service_name="KYCService", original_exception=original_exception)
        # self.message is already set by super().__init__


class KYCVerificationFailedError(KYCServiceError):
    """Raised when KYC verification explicitly fails according to the service. REQ-IOKYC-005, REQ-IL-011"""
    def __init__(self, message, reason_code=None, original_exception=None):
        super().__init__(message, original_exception=original_exception)
        self.reason_code = reason_code
        # self.message is already set by super().__init__

    def __str__(self):
        base_str = super().__str__()
        if self.reason_code:
            return f"{base_str} (Reason Code: {self.reason_code})"
        return base_str

class KYCDocumentInvalidError(KYCServiceError):
    """Raised when the KYC service deems the submitted document invalid. REQ-IOKYC-005, REQ-IL-011"""
    # Inherits __init__ and __str__ from KYCServiceError, message passed to super is sufficient.
    pass