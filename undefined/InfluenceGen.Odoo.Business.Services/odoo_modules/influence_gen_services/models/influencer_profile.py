import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class InfluencerProfile(models.Model):
    """
    Represents an influencer on the platform, centralizing their personal,
    professional, and platform-specific data.
    REQ-DMG-002, REQ-IOKYC-002, REQ-IOKYC-009, REQ-IOKYC-012, REQ-IOKYC-014,
    REQ-IOKYC-016, REQ-DMG-020, REQ-DMG-021
    """
    _name = 'influence_gen.influencer_profile'
    _description = 'Influencer Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'influence_gen.base_audit_mixin']

    user_id = fields.Many2one(
        'res.users', string='Odoo User', required=True, ondelete='cascade',
        index=True, copy=False,
        help="System user associated with this influencer profile."
    )
    full_name = fields.Char(string='Full Name', required=True, tracking=True)
    email = fields.Char(
        string='Email Address', required=True, tracking=True,
        help="Primary email for communication and login."
    )
    phone = fields.Char(string='Phone Number', tracking=True)
    residential_address = fields.Text(string='Residential Address', tracking=True)

    social_media_profile_ids = fields.One2many(
        'influence_gen.social_media_profile', 'influencer_profile_id',
        string='Social Media Profiles'
    )
    area_of_influence_ids = fields.Many2many(
        'influence_gen.area_of_influence',
        'influencer_area_of_influence_rel',
        'influencer_id', 'area_id', string='Areas of Influence'
    )
    audience_demographics = fields.Json(
        string='Audience Demographics (JSON)',
        help="Self-declared audience demographics, stored as JSON."
    )

    kyc_status = fields.Selection([
        ('pending', 'Pending Submission'),
        ('submitted', 'Submitted, Awaiting Review'),
        ('in_review', 'In Review'),
        ('requires_more_info', 'Requires More Info'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='KYC Status', default='pending', required=True, tracking=True, index=True)

    kyc_data_ids = fields.One2many(
        'influence_gen.kyc_data', 'influencer_profile_id', string='KYC Submissions'
    )
    bank_account_ids = fields.One2many(
        'influence_gen.bank_account', 'influencer_profile_id', string='Bank Accounts'
    )
    terms_consent_ids = fields.One2many(
        'influence_gen.terms_consent', 'influencer_profile_id', string='Terms Consents'
    )

    account_status = fields.Selection([
        ('pending_verification', 'Pending Verification'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended')
    ], string='Account Status', default='pending_verification', required=True, tracking=True, index=True)
    activation_date = fields.Datetime(string='Activation Date', readonly=True, tracking=True)

    is_gdpr_erasure_requested = fields.Boolean(
        string='GDPR Erasure Requested', default=False, tracking=True
    )
    legal_hold_status = fields.Boolean(
        string='Legal Hold Active', default=False, tracking=True,
        help="Indicates if this profile is under a legal hold, preventing deletion."
    )
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company
    )

    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'The email address must be unique across all influencers.'),
        ('user_id_unique', 'UNIQUE(user_id)', 'An Odoo user can only be linked to one influencer profile.')
    ]

    def name_get(self):
        """Override to return full_name or email as display name."""
        result = []
        for record in self:
            name = record.full_name or record.email
            result.append((record.id, name))
        return result

    def action_activate_account(self):
        """
        Sets account_status to 'active' and activation_date.
        Ensures all onboarding prerequisites are met. Logs event. Sends notification.
        REQ-IOKYC-012
        """
        self.ensure_one()
        if self.check_onboarding_completion():
            self.write({
                'account_status': 'active',
                'activation_date': fields.Datetime.now()
            })
            # _logger.info(f"Influencer account {self.id} activated.")
            # self.message_post(body=_("Account activated.")) # Handled by mixin for audit
            # Call notification service or send email template
            # Example: self.env['mail.template']._render_template(...)
            return True
        else:
            raise ValidationError(_("Cannot activate account. Onboarding prerequisites not met."))
        return False

    def action_deactivate_account(self):
        """Sets account_status to 'inactive'. Logs event."""
        self.ensure_one()
        self.write({'account_status': 'inactive'})
        # _logger.info(f"Influencer account {self.id} deactivated.")
        # self.message_post(body=_("Account deactivated."))
        return True

    def action_suspend_account(self):
        """Sets account_status to 'suspended'. Logs event."""
        self.ensure_one()
        self.write({'account_status': 'suspended'})
        # _logger.info(f"Influencer account {self.id} suspended.")
        # self.message_post(body=_("Account suspended."))
        return True

    def action_request_data_erasure(self):
        """
        Sets is_gdpr_erasure_requested to True. Triggers admin review. Logs event.
        REQ-DMG-021
        """
        self.ensure_one()
        self.write({'is_gdpr_erasure_requested': True})
        # _logger.info(f"GDPR data erasure requested for influencer {self.id}.")
        # self.message_post(body=_("GDPR data erasure requested."))
        # Create activity for admin
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            summary=_('Review GDPR Erasure Request'),
            note=_('Influencer %s has requested data erasure.') % self.display_name,
            user_id=self.env.ref('base.user_admin').id # Or a specific admin group
        )
        # Service call for REQ-DRH-003, REQ-DRH-004 might be triggered here or by the admin activity
        # self.env['influence_gen.services.retention_and_legal_hold'].process_manual_erasure_request(...)
        return True

    def get_latest_consent(self):
        """
        Searches terms_consent_ids and returns the latest record based on consent_date.
        REQ-IOKYC-009
        """
        self.ensure_one()
        latest_consent = self.env['influence_gen.terms_consent'].search([
            ('influencer_profile_id', '=', self.id)
        ], order='consent_date desc', limit=1)
        return latest_consent

    def update_kyc_status(self, new_status, reviewer_id=None, notes=None):
        """
        Updates kyc_status. If 'approved' and other conditions met, may trigger activation.
        Sends notification.
        """
        self.ensure_one()
        old_status = self.kyc_status
        self.write({'kyc_status': new_status})
        log_message = _("KYC status changed from %s to %s.") % (old_status, new_status)
        if notes:
            log_message += _(" Reviewer notes: %s") % notes
        self.message_post(body=log_message)

        # Send notification (e.g. using mail.template)
        # self.env['influence_gen.services.onboarding']._send_kyc_status_notification(self, new_status)

        if new_status == 'approved' and self.account_status == 'pending_verification':
            if self.check_onboarding_completion():
                 _logger.info(f"KYC approved for {self.id}, attempting to activate account.")
                 self.action_activate_account()
            else:
                 _logger.info(f"KYC approved for {self.id}, but other onboarding steps pending.")

    def check_onboarding_completion(self):
        """
        Checks if KYC is approved, at least one bank account is verified and primary,
        and latest ToS/PP are consented.
        REQ-IOKYC-012
        """
        self.ensure_one()
        if self.kyc_status != 'approved':
            _logger.debug(f"Onboarding check failed for {self.id}: KYC not approved ({self.kyc_status})")
            return False

        primary_verified_bank_account = self.bank_account_ids.filtered(
            lambda b: b.is_primary and b.verification_status == 'verified'
        )
        if not primary_verified_bank_account:
            _logger.debug(f"Onboarding check failed for {self.id}: No primary verified bank account.")
            return False

        latest_consent = self.get_latest_consent()
        if not latest_consent: # Or check specific versions if required
            _logger.debug(f"Onboarding check failed for {self.id}: No terms consent found.")
            return False
        # Add logic to check if latest_consent.tos_version and .privacy_policy_version
        # match current required versions (e.g., from PlatformSetting)

        _logger.info(f"Onboarding completion check passed for {self.id}.")
        return True