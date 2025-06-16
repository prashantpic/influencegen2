# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class KYCVerificationRequest:
    """
    DTO for submitting KYC identity verification data.
    Fields depend on the specific third-party KYC service API.
    REQ-IOKYC-005, REQ-IL-011
    """
    document_image_front_b64: str  # Base64 encoded image
    document_image_back_b64: Optional[str] = None # Base64 encoded image, optional for some documents/services
    document_type: str  # e.g., 'PASSPORT', 'DRIVING_LICENSE', 'ID_CARD'. Must match service's expected values.
    influencer_id: int # Internal influencer ID (e.g., res.partner ID or custom model ID) for callback matching/logging.
    
    # Optional fields that might be required or beneficial for some KYC providers
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None # Date of Birth, e.g., 'YYYY-MM-DD'
    address: Optional[Dict[str, Any]] = None # Structured address, e.g., {"street": "...", "city": "...", "zip": "...", "country": "US"}
    country_code: Optional[str] = None # ISO 3166-1 alpha-2 country code of the document issuer or influencer nationality
    
    # callback_url: Optional[str] = None # If the service supports asynchronous callbacks for verification results
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict) # For any additional data to pass through or specific to the request