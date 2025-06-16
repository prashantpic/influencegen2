# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class InfluenceGenBankAccount(models.Model):
    _name = 'influence_gen.bank_account'
    _description = "Influencer Bank Account"

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string="Influencer Profile",
        required=True, ondelete='cascade', index=True
    )
    account_holder_name = fields.Char(string="Account Holder Name", required=True)
    account_number_encrypted = fields.Char(string="Account Number (Encrypted)", required=True)
    bank_name = fields.Char(string="Bank Name", required=True)
    routing_number_encrypted = fields.Char(string="Routing Number (Encrypted)")
    iban_encrypted = fields.Char(string="IBAN (Encrypted)")
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
    is_primary = fields.Boolean(
        string="Primary Account", default=False,
        help="Is this the primary account for payouts?"
    )

    @api.constrains('influencer_profile_id', 'is_primary')
    def _check_single_primary_account(self):
        """Ensure an influencer has only one primary bank account."""
        for record in self.filtered(lambda r: r.is_primary):
            other_primary_accounts = self.search([
                ('influencer_profile_id', '=', record.influencer_profile_id.id),
                ('is_primary', '=', True),
                ('id', '!=', record.id)
            ])
            if other_primary_accounts:
                raise ValidationError(_("An influencer can only have one primary bank account."))

    def action_set_as_primary(self):
        """Sets this bank account as primary, ensuring others are not."""
        self.ensure_one()
        other_accounts = self.search([
            ('influencer_profile_id', '=', self.influencer_profile_id.id),
            ('id', '!=', self.id),
            ('is_primary', '=', True)
        ])
        other_accounts.write({'is_primary': False})
        self.write({'is_primary': True})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_ACCOUNT_SET_PRIMARY',
            actor_user_id=self.env.user.id,
            action_performed='SET_PRIMARY',
            target_object=self
        )
        return True

    def action_initiate_verification(self, method):
        """Called by OnboardingService to start bank verification. REQ-IOKYC-008."""
        self.ensure_one()
        self.write({
            'verification_method': method,
            'verification_status': 'verification_initiated'
        })

        if method == 'micro_deposit':
            # Trigger external process (via infra layer) to send micro-deposits
            # self.env['influence_gen.infrastructure.integration.services'].initiate_micro_deposits(self.id)
            _logger.info("Micro-deposit verification initiated for BankAccount %s (Placeholder)", self.id)
        
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_ACCOUNT_VERIFICATION_INITIATED',
            actor_user_id=self.env.user.id,
            action_performed='INITIATE_VERIFICATION',
            target_object=self,
            details_dict={'method': method}
        )
        # Return details if needed (e.g., instructions for influencer)
        return {'message': _("Bank account verification initiated using %s method.", method)}

    def action_confirm_verification(self, verification_input=None):
        """Called by OnboardingService to confirm bank verification. REQ-IOKYC-008."""
        self.ensure_one()
        success = False
        audit_details = {'method': self.verification_method, 'input': verification_input}

        # Logic based on verification_method
        if self.verification_method == 'micro_deposit':
            # E.g., verification_input = {'amount1': 0.05, 'amount2': 0.12}
            # Compare with expected amounts (placeholder logic)
            # expected_amounts = self.env['influence_gen.infrastructure.integration.services'].get_micro_deposit_amounts(self.id)
            # if verification_input and expected_amounts and \
            #    verification_input.get('amount1') == expected_amounts.get('amount1') and \
            #    verification_input.get('amount2') == expected_amounts.get('amount2'):
            #    success = True
            # For SDS, simplified:
            if verification_input and verification_input.get('status') == 'confirmed':
                 success = True

        elif self.verification_method == 'third_party_api':
            # E.g., verification_input = {'api_response_status': 'verified'}
            if verification_input and verification_input.get('status') == 'verified':
                success = True
        elif self.verification_method == 'manual_document':
            # Admin manually confirms
            success = True # Assuming this action is called by an admin marking it as verified
        else:
            raise UserError(_("Unknown bank account verification method: %s", self.verification_method))

        if success:
            self.write({'verification_status': 'verified'})
            self.influencer_profile_id.update_onboarding_step_status('bank_account_verified', True)
            audit_outcome = 'success'
        else:
            self.write({'verification_status': 'failed'})
            audit_outcome = 'failure'
            
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_ACCOUNT_VERIFICATION_CONFIRMED',
            actor_user_id=self.env.user.id,
            action_performed='CONFIRM_VERIFICATION',
            target_object=self,
            details_dict=audit_details,
            outcome=audit_outcome
        )
        return success
    
    # Placeholder for decryption, actual decryption would be handled by infra/utility layer
    # These compute methods are illustrative and would need secure context/permissions
    def _get_decrypted_value(self, encrypted_field_name):
        # In a real scenario, this would call an encryption service
        # For SDS, we assume fields are just stored. This is a conceptual placeholder.
        # self.ensure_one()
        # return self.env['encryption.service'].decrypt(self[encrypted_field_name])
        return f"Decrypted value of {encrypted_field_name}"

    # Example of how one might provide access to decrypted values if needed (use with extreme caution)
    # def get_decrypted_account_number(self):
    #     self.ensure_one()
    #     # Check permissions here
    #     return self._get_decrypted_value('account_number_encrypted')