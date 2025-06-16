# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class InfluenceGenBankAccount(models.Model):
    _name = 'influence_gen.bank_account'
    _description = "Influencer Bank Account"

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Influencer Profile",
        required=True,
        ondelete='cascade',
        index=True
    )
    account_holder_name = fields.Char(string="Account Holder Name", required=True)
    # Stored encrypted, actual encryption handled by utilities/infra layer
    account_number_encrypted = fields.Char(string="Account Number (Encrypted)", required=True)
    bank_name = fields.Char(string="Bank Name", required=True)
    # Stored encrypted
    routing_number_encrypted = fields.Char(string="Routing Number (Encrypted)")
    # Stored encrypted
    iban_encrypted = fields.Char(string="IBAN (Encrypted)")
    # Stored encrypted
    swift_code_encrypted = fields.Char(string="SWIFT Code (Encrypted)")
    bank_address = fields.Text(string="Bank Address")
    country_id = fields.Many2one('res.country', string="Bank Country")
    verification_status = fields.Selection([
        ('pending', 'Pending'),
        ('verification_initiated', 'Verification Initiated'),
        ('verified', 'Verified'),
        ('failed', 'Failed')
    ], string="Verification Status", default='pending', required=True, tracking=True, index=True)
    verification_method = fields.Selection([
        ('micro_deposit', 'Micro-Deposit'),
        ('third_party_api', 'Third-Party API'),
        ('manual_document', 'Manual Document Review')
    ], string="Verification Method")
    is_primary = fields.Boolean(string="Primary Account", default=False, help="Is this the primary account for payouts?")

    @api.constrains('influencer_profile_id', 'is_primary')
    def _check_single_primary_account(self) -> None:
        """
        Ensure an influencer has only one primary bank account.
        """
        for record in self:
            if record.is_primary:
                other_primary_accounts = self.search([
                    ('influencer_profile_id', '=', record.influencer_profile_id.id),
                    ('is_primary', '=', True),
                    ('id', '!=', record.id)
                ])
                if other_primary_accounts:
                    raise ValidationError(_("An influencer can only have one primary bank account. Please uncheck 'Primary Account' for other accounts first."))

    def action_set_as_primary(self) -> None:
        """
        Sets this bank account as primary, ensuring others are not.
        """
        self.ensure_one()
        # Unset other primary accounts for this influencer
        other_accounts = self.search([
            ('influencer_profile_id', '=', self.influencer_profile_id.id),
            ('is_primary', '=', True),
            ('id', '!=', self.id)
        ])
        other_accounts.write({'is_primary': False})
        
        # Set this one as primary
        self.write({'is_primary': True})
        
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_ACCOUNT_SET_PRIMARY',
            actor_user_id=self.env.user.id,
            action_performed='SET_PRIMARY',
            target_object=self
        )

    def action_initiate_verification(self, method: str) -> dict:
        """
        Called by OnboardingService to start bank verification. REQ-IOKYC-008.
        """
        self.ensure_one()
        self.verification_method = method
        self.verification_status = 'verification_initiated'
        details = {'instructions': ''}

        if method == 'micro_deposit':
            # Trigger external process (via infra layer) to send micro-deposits
            # self.env['influence_gen_integration.payment_gateway_service'].initiate_micro_deposits(self.id)
            details['instructions'] = _("Micro-deposits have been initiated. Please check your bank account in 1-3 business days and confirm the amounts.")
        elif method == 'third_party_api':
            # Potentially call infrastructure layer here if direct API call is needed from Odoo side to start
            # e.g., self.env['influence_gen_integration.bank_verification_api'].start_verification(self.id)
            details['instructions'] = _("Bank account verification has been initiated via our third-party provider.")
        elif method == 'manual_document':
            details['instructions'] = _("Please upload necessary bank statement or document for manual verification.")
        
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_VERIFICATION_INITIATED',
            actor_user_id=self.env.user.id,
            action_performed='INITIATE_VERIFICATION',
            target_object=self,
            details_dict={'method': method}
        )
        return details

    def action_confirm_verification(self, verification_input: str = None) -> bool:
        """
        Called by OnboardingService to confirm bank verification. REQ-IOKYC-008.
        """
        self.ensure_one()
        success = False
        audit_details = {'method': self.verification_method, 'input_provided': bool(verification_input)}

        if self.verification_method == 'micro_deposit':
            # Infrastructure layer would typically handle the verification of amounts
            # micro_deposit_amounts = ... (parse verification_input if it contains amounts)
            # success = self.env['influence_gen_integration.payment_gateway_service'].confirm_micro_deposits(self.id, micro_deposit_amounts)
            # Simulating success for now
            if verification_input == "amounts_match": # Placeholder
                success = True
            else:
                audit_details['failure_reason'] = 'Micro-deposit amounts did not match.'

        elif self.verification_method == 'third_party_api':
            # Callback from third-party or result polling via infra layer would determine success
            # Simulating success
            if verification_input == "api_verified": # Placeholder
                success = True
            else:
                audit_details['failure_reason'] = 'Third-party API could not verify the account.'
        
        elif self.verification_method == 'manual_document':
            # Admin marks as verified directly
            success = True # Assuming this method is called by an admin confirming it

        if success:
            self.write({'verification_status': 'verified'})
            self.influencer_profile_id.update_onboarding_step_status('bank_account_verified', True)
            audit_details['outcome'] = 'verified'
        else:
            self.write({'verification_status': 'failed'})
            audit_details['outcome'] = 'failed'
            
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_VERIFICATION_CONFIRMED',
            actor_user_id=self.env.user.id,
            action_performed='CONFIRM_VERIFICATION',
            target_object=self,
            details_dict=audit_details,
            outcome='success' if success else 'failure'
        )
        return success