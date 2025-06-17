# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError

class InfluenceGenBaseException(Exception):
    """Base exception for InfluenceGen specific errors not intended for direct UI display."""
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception

class InfluenceGenValidationException(ValidationError):
    """Custom validation exception, typically for UI display."""
    def __init__(self, message, *args):
        super().__init__(message, *args)

class InfluenceGenIntegrationException(InfluenceGenBaseException):
    """Exception for errors during integration with external services (N8N, AI APIs, etc.)."""
    pass

class InfluenceGenConfigurationError(InfluenceGenBaseException):
    """Exception for errors related to misconfiguration of the platform."""
    pass

class InfluenceGenSecurityException(InfluenceGenBaseException):
    """Exception for security-related violations or issues."""
    pass

class InfluenceGenProcessingError(InfluenceGenBaseException):
    """General exception for errors during internal processing tasks."""
    pass

# UserError is a good base for messages that should be shown to the end-user directly.
# ValidationError is a specific type of UserError for data validation issues.