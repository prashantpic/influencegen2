# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class BankVerificationResponse:
    """
    DTO for the response from a bank account verification service.
    REQ-IOKYC-008, REQ-IPF-002
    """
    transaction_id: str # Unique ID for the verification attempt, provided by the external service
    status: str  # e.g., 'VERIFIED', 'PENDING', 'FAILED', 'MICRODEPOSIT_SENT'. Values are service-specific.
    reason: Optional[str] = None # Human-readable reason or message accompanying the status
    reason_code: Optional[str] = None # Service-specific code for the reason/status
    
    # Optional fields that some bank verification services might return
    account_holder_name_matched: Optional[bool] = None # If name matching was performed and its result
    is_valid_account: Optional[bool] = None # General validity status of the account number/routing combination
    microdeposit_amounts: Optional[List[float]] = None # If micro-deposit verification is used, the amounts sent
    
    original_response: Optional[Dict[str, Any]] = field(default_factory=dict) # Store the full original JSON response