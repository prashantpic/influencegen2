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
    # The SDS states "Actual encryption handled by utilities/infra layer"
    # For Odoo ORM, these are stored as Char. The service layer/UI would ensure they are encrypted before storing.
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
    is_primary = fields.Boolean(string="Primary Account", default=False, help="Is this the primary account for payouts?")

    @api.constrains('influencer_profile_id', 'is_primary')
    def _check_single_primary_account(self):
        """Ensure an influencer has only one primary bank account."""
        for record in self:
            if record.is_primary:
                domain = [
                    ('influencer_profile_id', '=', record.influencer_profile_id.id),
                    ('is_primary', '=', True),
                    ('id', '!=', record.id)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(_("An influencer can only have one primary bank account."))

    def action_set_as_primary(self):
        """Sets this bank account as primary, ensuring others are not."""
        self.ensure_one()
        other_accounts = self.env['influence_gen.bank_account'].search([
            ('influencer_profile_id', '=', self.influencer_profile_id.id),
            ('id', '!=', self.id),
            ('is_primary', '=', True)
        ])
        if other_accounts:
            other_accounts.write({'is_primary': False})
        if not self.is_primary:
            self.write({'is_primary': True})

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_ACCOUNT_SET_PRIMARY',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
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

        # If method is 'micro_deposit', trigger external process (via infra layer)
        if method == 'micro_deposit':
            # infra_service = self.env['influence_gen.infrastructure.payment_service'] # Example
            # if hasattr(infra_service, 'send_micro_deposits'):
            #     infra_service.send_micro_deposits(self.id)
            pass # Placeholder for infra call

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_ACCOUNT_VERIFICATION_INITIATED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
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

        # Based on verification_method (micro-deposit amounts, third-party API response, manual review)
        if self.verification_method == 'micro_deposit':
            # infra_service = self.env['influence_gen.infrastructure.payment_service'] # Example
            # if hasattr(infra_service, 'verify_micro_deposit_amounts'):
            #     success = infra_service.verify_micro_deposit_amounts(self.id, verification_input)
            # else:
            #     success = True # Placeholder for actual infra call and check
            if verification_input and isinstance(verification_input, list) and len(verification_input) == 2: # Example
                 success = True # Simplified
            else:
                 audit_details['failure_reason'] = 'Micro-deposit amounts incorrect or not provided.'
        elif self.verification_method == 'third_party_api':
            if isinstance(verification_input, dict) and verification_input.get('status') == 'success':
                success = True
            else:
                audit_details['failure_reason'] = 'Third-party API verification failed.'
        elif self.verification_method == 'manual_document':
            success = True # Assumes admin marks as verified

        if success:
            self.write({'verification_status': 'verified'})
            if self.influencer_profile_id:
                self.influencer_profile_id.update_onboarding_step_status('bank_submitted', True) # Or 'bank_verified'
                self.influencer_profile_id.update_onboarding_step_status('bank_verified', True)
        else:
            self.write({'verification_status': 'failed'})

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_ACCOUNT_VERIFICATION_CONFIRMED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            outcome='success' if success else 'failure',
            failure_reason=audit_details.get('failure_reason'),
            details_dict=audit_details
        )
        return success