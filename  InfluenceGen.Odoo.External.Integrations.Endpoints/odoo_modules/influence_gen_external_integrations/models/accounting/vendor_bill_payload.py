# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import date as py_date # Use python's date for DTO, Odoo services will convert
# from odoo.fields import Date as OdooDate # This is for Odoo model fields, not ideal for pure DTOs

@dataclass
class VendorBillLinePayload:
    """
    DTO for a single line item on a Vendor Bill.
    """
    product_id: Optional[int] = None # Odoo product.product ID. If provided, name/account/taxes might be derived.
    name: str # Description for the bill line. Mandatory.
    quantity: float = 1.0
    price_unit: float = 0.0 # Price per unit before tax.
    account_id: Optional[int] = None # Specific expense account ID. Overrides product's account if set.
    tax_ids: Optional[List[int]] = field(default_factory=list) # List of Odoo account.tax IDs for this line.
    
    # Add other relevant analytic account fields if needed, structure depends on Odoo version & config
    # analytic_account_id: Optional[int] = None # For Odoo < 14 or simple analytics
    # analytic_distribution: Optional[Dict[int, float]] = None # For Odoo 14+ analytic distribution (account.analytic.line format)
    # e.g. analytic_distribution = {analytic_plan_id: {analytic_account_id: percentage, ...}}
    # For Odoo 16/17, analytic distribution is a dict on account.move.line: {'analytic_account_A_id': 60, 'analytic_account_B_id': 40}
    # For simplicity, if complex analytics are needed, they can be added later or handled by business logic setting defaults.


@dataclass
class VendorBillPayload:
    """
    DTO for creating a Vendor Bill in Odoo Accounting.
    REQ-IPF-006, REQ-2-014
    """
    influencer_partner_id: int  # Odoo res.partner ID for the influencer (vendor). Mandatory.
    currency_id: int  # Odoo res.currency ID. Mandatory.
    journal_id: int # Odoo account.journal ID (must be a 'purchase' type journal). Mandatory.
    
    invoice_date: Optional[py_date] = None # Bill date. Defaults to today if None in service.
    date: Optional[py_date] = None # Accounting date. Defaults to today if None in service.
    invoice_date_due: Optional[py_date] = None # Due date.
    
    narration: Optional[str] = None # Internal notes for the bill (bottom section).
    payment_reference: Optional[str] = None # Vendor Reference field on the bill.
    
    # Optional field for linking to an Influence Gen campaign or other internal reference
    # This would require a custom field on account.move model, e.g., x_influence_gen_campaign_id
    # campaign_id_internal: Optional[int] = None 
    
    invoice_line_ids: List[VendorBillLinePayload] = field(default_factory=list)

    def __post_init__(self):
        if not self.invoice_line_ids:
            raise ValueError("VendorBillPayload must contain at least one invoice line.")
        if not all(isinstance(line, VendorBillLinePayload) for line in self.invoice_line_ids):
            raise TypeError("All items in invoice_line_ids must be VendorBillLinePayload instances.")