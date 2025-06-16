# -*- coding: utf-8 -*-

class ExternalServiceError(Exception):
    """Base class for errors related to external services."""
    def __init__(self, message, service_name=None, original_exception=None):
        super().__init__(message)
        self.message = message # Store message for easier access by __str__ and callers
        self.service_name = service_name
        self.original_exception = original_exception

    def __str__(self):
        parts = []
        if self.service_name:
            parts.append(f"[{self.service_name}]")
        parts.append(str(self.message)) # Use the stored message attribute
        if self.original_exception:
            parts.append(f"(Original error: {type(self.original_exception).__name__}: {str(self.original_exception)})")
        return " ".join(parts)


class ConfigurationError(ExternalServiceError):
    """Raised when there's an issue with external service configuration."""
    def __init__(self, message, service_name=None, setting_key=None, original_exception=None):
        super().__init__(message, service_name=(service_name or "Configuration"), original_exception=original_exception)
        self.setting_key = setting_key
        # self.message is already set by super().__init__

    def __str__(self):
        base_str = super().__str__()
        if self.setting_key:
            return f"{base_str} (Setting key: {self.setting_key})"
        return base_str


class ApiCommunicationError(ExternalServiceError):
    """Raised for network issues or non-2xx HTTP responses during API communication."""
    def __init__(self, message, service_name=None, status_code=None, response_content=None, original_exception=None):
        super().__init__(message, service_name=service_name, original_exception=original_exception)
        self.status_code = status_code
        self.response_content = response_content
        # self.message is already set by super().__init__

    def __str__(self):
        base_str = super().__str__()
        parts = [base_str]
        if self.status_code:
            parts.append(f"(Status Code: {self.status_code})")
        
        # Avoid overly long response content in string representation
        if self.response_content:
            content_preview = str(self.response_content)
            if len(content_preview) > 200:
                content_preview = content_preview[:200] + "..."
            parts.append(f"(Response: {content_preview})")
        return " ".join(parts)