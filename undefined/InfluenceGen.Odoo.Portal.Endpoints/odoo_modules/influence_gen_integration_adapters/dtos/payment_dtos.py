# odoo_modules/influence_gen_integration_adapters/dtos/payment_dtos.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class BankAccountDetailsDto:
    """
    Data Transfer Object for bank account details.
    """
    account_holder_name: str
    account_number: str # Potentially tokenized or reference ID
    bank_name: Optional[str] = None
    routing_number: Optional[str] = None
    iban: Optional[str] = None
    swift_code: Optional[str] = None
    # Other fields as needed by the specific gateway

@dataclass
class BankAccountVerificationRequestDto:
    """
    Data Transfer Object for initiating a bank account verification request.
    """
    bank_account_id: int # Odoo BankAccount record ID
    influencer_profile_id: int
    bank_details: BankAccountDetailsDto
    # Micro-deposit amounts if applicable for verification step
    micro_deposit_amounts: Optional[List[float]] = None

@dataclass
class BankAccountVerificationResultDto:
    """
    Data Transfer Object for the result of a bank account verification.
    """
    bank_account_id: int
    external_verification_id: Optional[str] = None
    status: str # e.g., "verified", "pending", "failed", "micro_deposits_sent"
    reason_message: Optional[str] = None

@dataclass
class PaymentInitiationRequestDto:
    """
    Data Transfer Object for initiating a payment.
    """
    payment_record_id: int # Odoo PaymentRecord ID
    influencer_profile_id: int
    amount: float
    currency: str # ISO 4217
    bank_details_reference_id: Optional[str] = None # If gateway uses a token/ID for stored bank details
    bank_details: Optional[BankAccountDetailsDto] = None # Or provide full details if not stored/tokenized
    description: Optional[str] = "InfluenceGen Payout"

@dataclass
class PaymentResultDto:
    """
    Data Transfer Object for the result of a payment initiation.
    """
    payment_record_id: int
    external_transaction_id: Optional[str] = None
    status: str # e.g., "succeeded", "pending", "failed", "requires_action"
    reason_code: Optional[str] = None
    reason_message: Optional[str] = None
    paid_at: Optional[str] = None # ISO 8601 timestamp