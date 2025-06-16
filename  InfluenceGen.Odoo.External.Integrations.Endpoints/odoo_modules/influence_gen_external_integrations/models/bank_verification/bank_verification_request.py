# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional

@dataclass
class BankVerificationRequest:
    """
    DTO for submitting bank account details for verification.
    Fields depend on the specific third-party service API.
    REQ-IOKYC-008, REQ-IPF-002
    """
    account_holder_name: str
    account_number: str # The bank account number
    routing_number: Optional[str] = None # For ACH/US bank accounts (ABA number)
    iban: Optional[str] = None # For SEPA/International bank accounts
    swift_code: Optional[str] = None # (BIC) For International bank accounts
    bank_name: Optional[str] = None # Name of the bank, sometimes useful
    country_code: str # ISO 3166-1 alpha-2 country code where the bank account is held
    currency_code: Optional[str] = None # ISO 4217 currency code of the account (e.g., 'USD', 'EUR'), if relevant for verification
    influencer_id: int # Internal influencer ID (e.g., res.partner ID) for logging/reference
    
    # Add other fields as required by the specific bank verification provider
    # E.g., address of account holder, type of account (checking/savings)
    # account_type: Optional[str] = None # e.g., 'CHECKING', 'SAVINGS'
    # bank_address: Optional[Dict[str, Any]] = None