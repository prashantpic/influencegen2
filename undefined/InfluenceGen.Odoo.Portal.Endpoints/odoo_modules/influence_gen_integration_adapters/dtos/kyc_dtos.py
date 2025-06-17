# odoo_modules/influence_gen_integration_adapters/dtos/kyc_dtos.py
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class KycDocumentDto:
    """
    Data Transfer Object for KYC document details.
    """
    document_type: str # e.g., 'passport', 'driver_license'
    file_url_front: str # URL to the uploaded document (front)
    file_url_back: Optional[str] = None # URL to the uploaded document (back)

@dataclass
class KycVerificationRequestDto:
    """
    Data Transfer Object for initiating a KYC verification request.
    """
    kyc_data_id: int # Odoo KYCData record ID
    influencer_profile_id: int # Odoo InfluencerProfile ID
    documents: List[KycDocumentDto]
    # Add other PII as required by the KYC provider
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None # ISO 8601 format
    address_details: Optional[Dict[str, str]] = None # e.g., street, city, zip, country

@dataclass
class KycVerificationResultDto:
    """
    Data Transfer Object for the result of a KYC verification.
    """
    kyc_data_id: int # Odoo KYCData record ID
    external_verification_id: Optional[str] = None # ID from the KYC provider
    status: str # e.g., "approved", "rejected", "pending_review", "needs_more_info"
    reason_code: Optional[str] = None # Provider-specific reason code
    reason_message: Optional[str] = None
    vendor_specific_data: Optional[Dict[str, Any]] = None # Raw response or extra data