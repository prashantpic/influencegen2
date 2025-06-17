# -*- coding: utf-8 -*-

# KYC Statuses
KYC_STATUS_PENDING = 'pending'
KYC_STATUS_IN_REVIEW = 'in_review'
KYC_STATUS_APPROVED = 'approved'
KYC_STATUS_REJECTED = 'rejected'
KYC_STATUS_MORE_INFO_REQUIRED = 'more_info_required'

# Campaign Statuses (Example - actual statuses might be in campaign module,
# but common ones could be here if used by multiple core processes)
CAMPAIGN_STATUS_DRAFT = 'draft'
CAMPAIGN_STATUS_PUBLISHED = 'published'
CAMPAIGN_STATUS_ACTIVE = 'active' # Or 'in_progress'
CAMPAIGN_STATUS_COMPLETED = 'completed'
CAMPAIGN_STATUS_ARCHIVED = 'archived'
CAMPAIGN_STATUS_CANCELLED = 'cancelled'

# Log Severities (align with Python logging levels if possible for consistency)
LOG_SEVERITY_DEBUG = 'DEBUG'
LOG_SEVERITY_INFO = 'INFO'
LOG_SEVERITY_WARNING = 'WARNING'
LOG_SEVERITY_ERROR = 'ERROR'
LOG_SEVERITY_CRITICAL = 'CRITICAL'

# HTTP Headers
DEFAULT_CORRELATION_ID_HEADER = 'X-Correlation-ID'
REQUEST_ID_HEADER = 'X-Request-ID' # Example, if used

# Default Values
DEFAULT_AI_IMAGE_RESOLUTION = '1024x1024' # Example
DEFAULT_PAGE_LIMIT = 20

# File Types
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx']
MAX_IMAGE_FILE_SIZE_MB = 5
MAX_DOCUMENT_FILE_SIZE_MB = 10

# Social Media Platforms (Example)
PLATFORM_INSTAGRAM = 'instagram'
PLATFORM_TIKTOK = 'tiktok'
PLATFORM_YOUTUBE = 'youtube'
PLATFORM_X = 'x' # formerly Twitter