# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class KYCVerificationResponse:
    """
    DTO for the response from a KYC identity verification service.
    Fields depend on the specific third-party KYC service API.
    REQ-IOKYC-005, REQ-IL-011
    """
    transaction_id: str # Unique ID for the verification attempt, provided by the external service
    status: str  # e.g., 'VERIFIED', 'REJECTED', 'PENDING_REVIEW', 'ACTION_REQUIRED'. Values are service-specific.
    reason: Optional[str] = None # Human-readable reason or message accompanying the status
    reason_code: Optional[str] = None # Service-specific code for the reason/status
    extracted_data: Optional[Dict[str, Any]] = field(default_factory=dict) # PII extracted from document (e.g., name, DOB, document number)
    
    # Optional fields that some KYC services might return
    kyc_score: Optional[float] = None # A numeric score indicating confidence or risk
    document_validity: Optional[str] = None # e.g., 'VALID', 'EXPIRED', 'SUSPICIOUS'
    face_match_score: Optional[float] = None # If face verification was part of the process
    
    original_response: Optional[Dict[str, Any]] = field(default_factory=dict) # Store the full original JSON response for auditing/debugging