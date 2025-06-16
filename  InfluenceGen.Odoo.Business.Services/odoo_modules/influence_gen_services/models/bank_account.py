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

    # Note: Actual encryption/decryption logic is outside the scope of this model's ORM fields.
    # The fields *_encrypted store the already encrypted string.
    # Accessing decrypted values would typically be done via a service or helper method
    # that calls an infrastructure utility for decryption, and such access should be highly restricted.

    @api.constrains('influencer_profile_id', 'is_primary')
    def _check_single_primary_account(self):
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
        self.ensure_one()
        if not self.influencer_profile_id:
            raise UserError(_("This bank account is not linked to any influencer."))

        other_primary_accounts = self.env['influence_gen.bank_account'].search([
            ('influencer_profile_id', '=', self.influencer_profile_id.id),
            ('is_primary', '=', True),
            ('id', '!=', self.id)
        ])
        other_primary_accounts.write({'is_primary': False})
        self.write({'is_primary': True})

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_ACCOUNT_SET_PRIMARY',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'bank_account_id': self.id}
        )
        return True

    def action_initiate_verification(self, method):
        self.ensure_one()
        if self.verification_status == 'verified':
            raise UserError(_("This bank account is already verified."))

        vals = {
            'verification_method': method,
            'verification_status': 'verification_initiated'
        }
        verification_details = {}

        if method == 'micro_deposit':
            # Trigger external process via infra layer
            # self.env['influence_gen.infrastructure.integration.service'].initiate_micro_deposits(self.id)
            verification_details['instructions'] = _("Micro-deposits will be sent. Please verify amounts once received.")
            self.influencer_profile_id.update_onboarding_step_status('bank_submitted', True)


        self.write(vals)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='BANK_ACCOUNT_VERIFICATION_INITIATED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'method': method, 'bank_account_id': self.id}
        )
        return verification_details

    def action_confirm_verification(self, verification_input=None):
        self.ensure_one()
        if self.verification_status == 'verified':
            return True

        success = False
        if self.verification_method == 'micro_deposit':
            # Requires external check or input of amounts
            # E.g., verification_input could be {'amount1': 0.05, 'amount2': 0.12}
            # success = self.env['influence_gen.infrastructure.integration.service'].confirm_micro_deposits(self.id, verification_input)
            if verification_input is True: # Simplified for now
                success = True
        elif self.verification_method == 'third_party_api':
            # Result from API call
            if verification_input and verification_input.get('status') == 'success':
                success = True
        elif self.verification_method == 'manual_document':
            # Admin marks as verified
            success = True


        if success:
            self.write({'verification_status': 'verified'})
            self.influencer_profile_id.update_onboarding_step_status('bank_verified', True)

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='BANK_ACCOUNT_VERIFICATION_CONFIRMED',
                actor_user_id=self.env.user.id,
                action_performed='UPDATE',
                target_object=self,
                details_dict={'bank_account_id': self.id, 'status': 'verified'}
            )
        else:
            self.write({'verification_status': 'failed'})
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='BANK_ACCOUNT_VERIFICATION_FAILED',
                actor_user_id=self.env.user.id,
                action_performed='UPDATE',
                target_object=self,
                details_dict={'bank_account_id': self.id, 'status': 'failed', 'reason': verification_input}
            )
        return success