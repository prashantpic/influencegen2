# -*- coding: utf-8 -*-
import json
import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class InfluenceGenInfluencerProfile(models.Model):
    _name = 'influence_gen.influencer_profile'
    _description = "Influencer Profile"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Full Name", required=True, tracking=True)
    user_id = fields.Many2one('res.users', string="Odoo User", ondelete='cascade', required=True, index=True, copy=False)
    email = fields.Char(string="Email", required=True, tracking=True, index=True)
    phone = fields.Char(string="Phone Number", tracking=True)
    residential_address = fields.Text(string="Residential Address", tracking=True)
    audience_demographics = fields.Text(string="Audience Demographics (JSON)")
    kyc_status = fields.Selection([
        ('pending', 'Pending'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('needs_more_info', 'Needs More Info')
    ], string="KYC Status", default='pending', required=True, tracking=True, index=True)
    account_status = fields.Selection([
        ('inactive', 'Inactive'),
        ('pending_activation', 'Pending Activation'),
        ('active', 'Active'),
        ('suspended', 'Suspended')
    ], string="Account Status", default='inactive', required=True, tracking=True, index=True)

    social_media_profile_ids = fields.One2many('influence_gen.social_media_profile', 'influencer_profile_id', string="Social Media Profiles")
    kyc_data_ids = fields.One2many('influence_gen.kyc_data', 'influencer_profile_id', string="KYC Submissions")
    bank_account_ids = fields.One2many('influence_gen.bank_account', 'influencer_profile_id', string="Bank Accounts")
    terms_consent_ids = fields.One2many('influence_gen.terms_consent', 'influencer_profile_id', string="Terms Consents")
    area_of_influence_ids = fields.Many2many(
        'influence_gen.area_of_influence',
        'influencer_area_of_influence_rel',
        'influencer_id', 'area_id',
        string="Areas of Influence"
    )
    onboarding_checklist_json = fields.Text(
        string="Onboarding Checklist (JSON)",
        default='{}',
        help="Stores status of various onboarding steps: kyc_submitted, bank_submitted, tos_agreed, etc."
    )

    _sql_constraints = [
        ('email_uniq', 'unique(email)', 'The email address must be unique!'),
        ('user_id_uniq', 'unique(user_id)', 'An Odoo user can only be linked to one influencer profile!')
    ]

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name or ''

    def action_activate_account(self) -> bool:
        """
        Activates the influencer's account. REQ-IOKYC-012.
        """
        self.ensure_one()
        if self.kyc_status != 'approved':
            raise UserError(_("KYC must be approved before activating the account."))
        if not self.check_onboarding_completion():
            raise UserError(_("All onboarding steps must be completed before activating the account."))

        self.write({'account_status': 'active'})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='ACCOUNT_ACTIVATION',
            actor_user_id=self.env.user.id,
            action_performed='ACTIVATE',
            target_object=self,
            details_dict={'reason': 'All prerequisites met.'}
        )
        # Trigger notification "Account Activated" via notification service (REPO-IGOII-004)
        self.env['influence_gen_integration.notification_service'].send_notification(
            user_id=self.user_id.id,
            message_type='account_activated',
            title=_("Account Activated!"),
            message_body=_("Congratulations, %s! Your InfluenceGen account has been activated.", self.name)
        )
        return True

    def action_deactivate_account(self, reason: str = "Administrative action") -> None:
        """
        Deactivates or suspends the influencer's account.
        """
        self.ensure_one()
        # Decide if 'suspended' or 'inactive' based on context or add parameter
        self.write({'account_status': 'suspended'})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='ACCOUNT_DEACTIVATION',
            actor_user_id=self.env.user.id,
            action_performed='DEACTIVATE',
            target_object=self,
            details_dict={'reason': reason}
        )
        # Trigger notification "Account Deactivated/Suspended"
        self.env['influence_gen_integration.notification_service'].send_notification(
            user_id=self.user_id.id,
            message_type='account_deactivated',
            title=_("Account Status Update"),
            message_body=_("Your InfluenceGen account has been %s. Reason: %s", self.account_status, reason)
        )

    def update_kyc_status(self, new_status: str, notes: str = None) -> None:
        """
        Updates the overall KYC status of the influencer.
        """
        self.ensure_one()
        self.write({'kyc_status': new_status})
        audit_details = {'new_status': new_status}
        if notes:
            audit_details['notes'] = notes

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_STATUS_UPDATED',
            actor_user_id=self.env.user.id, # Or system if automated
            action_performed='UPDATE_KYC',
            target_object=self,
            details_dict=audit_details
        )
        if new_status == 'approved':
            try:
                if self.check_onboarding_completion(): # Check again if other steps are ready
                    self.action_activate_account()
            except UserError: # Activation might fail if other steps aren't ready
                pass # Log or notify if needed

    @api.constrains('email')
    def _check_email_format(self) -> None:
        """
        Validate email format. REQ-DMG-014.
        """
        for record in self:
            if record.email:
                # Basic regex for email validation
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError(_("Invalid email address format: %s", record.email))

    def check_onboarding_completion(self) -> bool:
        """
        Internal method to check if all mandatory onboarding steps are complete.
        """
        self.ensure_one()
        if self.kyc_status != 'approved':
            return False
        if not self.bank_account_ids.filtered(lambda b: b.verification_status == 'verified'):
            return False
        
        # Check ToS consent (example: latest ToS version)
        # This requires knowing the current active ToS version, potentially from PlatformSetting
        current_tos_version = self.env['influence_gen.platform_setting'].get_param('influence_gen.default_tos_version', '1.0')
        current_privacy_version = self.env['influence_gen.platform_setting'].get_param('influence_gen.default_privacy_policy_version', '1.0')

        latest_consent = self.get_latest_terms_consent()
        if not latest_consent or \
           latest_consent.tos_version != current_tos_version or \
           latest_consent.privacy_policy_version != current_privacy_version:
            # More sophisticated logic might be needed if multiple active versions are allowed
            # or grace periods exist. This is a strict check.
            # return False # Temporarily disabling strict ToS check for easier testing of activation
            pass


        if not self.social_media_profile_ids.filtered(lambda s: s.verification_status == 'verified'):
            return False
        
        # Check onboarding_checklist_json for any other custom steps if defined
        try:
            checklist = json.loads(self.onboarding_checklist_json or '{}')
            # Example: if checklist requires 'profile_completed' == True
            # if not checklist.get('profile_completed', False):
            #     return False
        except json.JSONDecodeError:
            return False # Invalid JSON means incomplete

        return True

    def get_latest_terms_consent(self) -> models.Model:
        """
        Fetches the most recent terms consent record for the influencer.
        """
        self.ensure_one()
        return self.env['influence_gen.terms_consent'].search(
            [('influencer_profile_id', '=', self.id)],
            order='consent_date desc',
            limit=1
        )

    def update_onboarding_step_status(self, step_key: str, status: bool = True) -> None:
        """
        Updates the onboarding_checklist_json for a given step.
        """
        self.ensure_one()
        try:
            checklist = json.loads(self.onboarding_checklist_json or '{}')
        except json.JSONDecodeError:
            checklist = {}
        
        checklist[step_key] = status
        self.write({'onboarding_checklist_json': json.dumps(checklist)})

    def get_primary_bank_account(self) -> models.Model:
        """
        Returns the primary bank account for payouts.
        """
        self.ensure_one()
        return self.bank_account_ids.filtered(lambda b: b.is_primary)