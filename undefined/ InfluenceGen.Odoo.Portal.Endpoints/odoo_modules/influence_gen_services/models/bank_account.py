import logging
import base64
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

# Placeholder for actual encryption/decryption utilities
# In a real scenario, these would come from REPO-IGSCU-007 or a secure library
def _encrypt_data(data_str):
    if not data_str:
        return None
    # This is NOT real encryption, just a placeholder
    return base64.b64encode(data_str.encode('utf-8'))

def _decrypt_data(data_bytes):
    if not data_bytes:
        return None
    # This is NOT real decryption
    try:
        return base64.b64decode(data_bytes).decode('utf-8')
    except Exception:
        return "Error Decrypting"


class BankAccount(models.Model):
    """
    Represents an influencer's bank account for receiving payouts.
    REQ-DMG-002, REQ-IPF-001, REQ-IPF-002, REQ-IOKYC-007, REQ-IOKYC-008, REQ-IPF-011
    """
    _name = 'influence_gen.bank_account'
    _description = 'Influencer Bank Account'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'influence_gen.base_audit_mixin']

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string='Influencer Profile',
        required=True, ondelete='cascade', index=True, tracking=True
    )
    account_holder_name = fields.Char(string='Account Holder Name', required=True, tracking=True)

    # Storing encrypted data as Binary as per SDS.
    # Actual encryption/decryption would happen before setting/getting these fields.
    account_number_encrypted = fields.Binary(string='Encrypted Account Number', attachment=False, tracking=True)
    routing_number_encrypted = fields.Binary(string='Encrypted Routing Number', attachment=False, tracking=True)
    iban_encrypted = fields.Binary(string='Encrypted IBAN', attachment=False, tracking=True)
    swift_code_encrypted = fields.Binary(string='Encrypted SWIFT/BIC', attachment=False, tracking=True)

    # Display fields (masked)
    account_number_display = fields.Char(string='Account Number (Masked)', compute='_compute_display_fields', store=False)
    # Add other display fields if needed for routing, IBAN, SWIFT

    bank_name = fields.Char(string='Bank Name', required=True, tracking=True)

    verification_status = fields.Selection([
        ('pending', 'Pending Verification'),
        ('verification_initiated', 'Verification Initiated'), # e.g. micro-deposit sent
        ('verified', 'Verified'),
        ('failed', 'Verification Failed'),
        ('requires_manual_review', 'Requires Manual Review')
    ], string='Verification Status', default='pending', required=True, tracking=True, index=True)

    verification_method = fields.Selection([
        ('manual', 'Manual Admin Verification'),
        ('micro_deposit', 'Micro-Deposit Verification'),
        ('third_party_api', 'Third-Party API (e.g., Plaid)'),
        ('document_upload', 'Document Upload (Bank Statement)')
    ], string='Verification Method', tracking=True)

    is_primary = fields.Boolean(string='Primary Account', default=False, tracking=True,
                                help="Is this the primary bank account for payouts?")
    
    company_id = fields.Many2one(related='influencer_profile_id.company_id', store=True)

    @api.constrains('is_primary', 'influencer_profile_id')
    def _check_one_primary_account(self):
        for record in self:
            if record.is_primary:
                domain = [
                    ('id', '!=', record.id),
                    ('influencer_profile_id', '=', record.influencer_profile_id.id),
                    ('is_primary', '=', True)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(_("An influencer can only have one primary bank account."))

    @api.depends('account_number_encrypted')
    def _compute_display_fields(self):
        for record in self:
            acc_num = _decrypt_data(record.account_number_encrypted)
            if acc_num and len(acc_num) > 4:
                record.account_number_display = '****' + acc_num[-4:]
            elif acc_num:
                record.account_number_display = '****' # Mask if too short
            else:
                record.account_number_display = ''
    
    # Example of how encrypted fields might be set if not using compute/inverse
    # This would typically be handled in create/write or via a service to ensure encryption
    # @api.model
    # def create(self, vals):
    #     if 'account_number' in vals: # Assuming a transient field 'account_number'
    #         vals['account_number_encrypted'] = _encrypt_data(vals.pop('account_number'))
    #     # Similar for other encrypted fields
    #     return super(BankAccount, self).create(vals)

    # def write(self, vals):
    #     if 'account_number' in vals:
    #         vals['account_number_encrypted'] = _encrypt_data(vals.pop('account_number'))
    #     # Similar for other encrypted fields
    #     return super(BankAccount, self).write(vals)


    def action_verify_manually(self, reviewer_id=None):
        """Manually verifies the bank account, typically by an admin."""
        self.ensure_one()
        user = self.env['res.users'].browse(reviewer_id) if reviewer_id else self.env.user
        self.write({
            'verification_status': 'verified',
            'verification_method': 'manual', # Or confirm existing
        })
        self.message_post(body=_("Bank account manually verified by %s.") % user.name)
        _logger.info(f"Bank account {self.id} manually verified for influencer {self.influencer_profile_id.id} by {user.name}.")
        self.influencer_profile_id.check_onboarding_completion()

    def action_initiate_micro_deposit(self):
        """Initiates the micro-deposit verification process."""
        self.ensure_one()
        if self.verification_status != 'pending':
             raise UserError(_("Micro-deposit can only be initiated for accounts pending verification."))
        # This would call a service (e.g., PaymentProcessingService or OnboardingService)
        # to interact with a payment provider to send micro-deposits.
        # For now, simulate by setting status.
        # self.env['influence_gen.services.onboarding_service'].initiate_bank_micro_deposit(self.id)
        self.write({
            'verification_status': 'verification_initiated',
            'verification_method': 'micro_deposit'
        })
        self.message_post(body=_("Micro-deposit verification initiated. Please check your bank account for two small deposits and confirm them here."))
        _logger.info(f"Micro-deposit initiated for bank account {self.id} of influencer {self.influencer_profile_id.id}.")
        return True # Or return action from service

    def action_confirm_micro_deposit(self, amount1, amount2):
        """Confirms micro-deposit amounts provided by the influencer."""
        self.ensure_one()
        if self.verification_status != 'verification_initiated' or self.verification_method != 'micro_deposit':
            raise UserError(_("Micro-deposits can only be confirmed if verification was initiated via micro-deposit method."))

        # This would call a service to verify the amounts against what was sent.
        # success = self.env['influence_gen.services.onboarding_service'].confirm_bank_micro_deposit(self.id, amount1, amount2)
        # For simulation:
        actual_amount1 = self.env['platform.setting'].get_setting(f'bank.micro_deposit.amount1.{self.id}', 0.01) # Mocked
        actual_amount2 = self.env['platform.setting'].get_setting(f'bank.micro_deposit.amount2.{self.id}', 0.05) # Mocked

        # Convert input amounts to float for comparison if they are strings
        try:
            input_amount1 = float(amount1)
            input_amount2 = float(amount2)
        except ValueError:
            self.message_post(body=_("Invalid amount format for micro-deposit confirmation."))
            return False

        if (input_amount1 == actual_amount1 and input_amount2 == actual_amount2) or \
           (input_amount1 == actual_amount2 and input_amount2 == actual_amount1) : # Order might not matter
            self.write({'verification_status': 'verified'})
            self.message_post(body=_("Micro-deposit amounts confirmed successfully. Bank account verified."))
            _logger.info(f"Micro-deposit confirmed for bank account {self.id} of influencer {self.influencer_profile_id.id}.")
            self.influencer_profile_id.check_onboarding_completion()
            return True
        else:
            self.write({'verification_status': 'failed'})
            self.message_post(body=_("Micro-deposit amounts did not match. Verification failed."))
            _logger.warning(f"Micro-deposit confirmation failed for bank account {self.id} of influencer {self.influencer_profile_id.id}.")
            return False

    def get_decrypted_account_number(self):
        """
        Returns the decrypted account number.
        NOTE: This is a placeholder. Actual decryption should be handled securely.
        """
        self.ensure_one()
        if not self.account_number_encrypted:
            return ""
        # In a real system, self.env['ir.config_parameter'].sudo().get_param('encryption.key')
        # or a call to a secure utility service would be used.
        decrypted_val = _decrypt_data(self.account_number_encrypted)
        _logger.info(f"Access attempt for decrypted account number of bank_account {self.id}. User: {self.env.user.login}")
        # Add access control logging/checks here if needed
        return decrypted_val