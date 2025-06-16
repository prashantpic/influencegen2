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
        ('user_id_uniq', 'unique(user_id)', 'An Odoo user can only be linked to one influencer profile!'),
    ]

    def _compute_display_name(self):
        """Standard Odoo method if needed.
        By default, Odoo uses the 'name' field for display_name if it exists.
        If a custom display_name computation is needed, implement it here.
        For now, relying on the default behavior.
        """
        for record in self:
            record.display_name = record.name # Or any other logic

    def action_activate_account(self):
        """Activates the influencer's account. REQ-IOKYC-012."""
        self.ensure_one()
        if not self.check_onboarding_completion():
            raise UserError(_("Cannot activate account. All onboarding prerequisites are not met. KYC must be approved, bank account verified, terms agreed, and at least one social media profile verified."))

        if self.kyc_status != 'approved':
            raise UserError(_("Cannot activate account. KYC status is not 'Approved'."))

        self.write({'account_status': 'active'})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='ACCOUNT_ACTIVATED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'old_status': self.account_status, 'new_status': 'active'}
        )
        # Trigger notification "Account Activated" via notification service (REPO-IGOII-004)
        # Assuming a service named 'infrastructure.notification' from the integration module
        notification_service = self.env['influence_gen.infrastructure.integration.services'].sudo()
        if hasattr(notification_service, 'send_notification'):
             notification_service.send_notification(
                user_ids=self.user_id.ids,
                notification_type='account_activated',
                title=_("Your InfluenceGen Account is Active!"),
                message=_("Congratulations! Your InfluenceGen account has been activated. You can now participate in campaigns."),
                target_model=self._name,
                target_res_id=self.id
            )
        return True

    def action_deactivate_account(self, reason="Administrative action"):
        """Deactivates or suspends the influencer's account."""
        self.ensure_one()
        # Decide if 'suspended' or 'inactive'. For now, let's use 'suspended'.
        old_status = self.account_status
        self.write({'account_status': 'suspended'})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='ACCOUNT_DEACTIVATED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'old_status': old_status, 'new_status': 'suspended', 'reason': reason}
        )
        # Trigger notification "Account Deactivated/Suspended"
        notification_service = self.env['influence_gen.infrastructure.integration.services'].sudo()
        if hasattr(notification_service, 'send_notification'):
            notification_service.send_notification(
                user_ids=self.user_id.ids,
                notification_type='account_deactivated',
                title=_("Your InfluenceGen Account Status Update"),
                message=_("Your InfluenceGen account has been %s. Reason: %s", self.account_status, reason),
                target_model=self._name,
                target_res_id=self.id
            )
        return True

    def update_kyc_status(self, new_status, notes=None):
        """Updates the overall KYC status of the influencer."""
        self.ensure_one()
        old_status = self.kyc_status
        self.write({'kyc_status': new_status})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_STATUS_UPDATED',
            actor_user_id=self.env.user.id, # Or system if called by system process
            action_performed='UPDATE',
            target_object=self,
            details_dict={'old_status': old_status, 'new_status': new_status, 'notes': notes}
        )
        if new_status == 'approved':
            self.update_onboarding_step_status('kyc_approved', True)
            # Attempt to activate account if other conditions might be met
            # This is often better handled by a specific call from OnboardingService after KYC approval
            # For now, let's keep it simple as the original SDS implied
            if self.check_onboarding_completion():
                 try:
                    self.action_activate_account()
                 except UserError:
                    pass # Activation will be re-attempted later or requires manual trigger

    @api.constrains('email')
    def _check_email_format(self):
        """Validate email format. REQ-DMG-014."""
        for record in self:
            if record.email:
                # Basic regex for email validation
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError(_("Invalid email address format: %s", record.email))

    def check_onboarding_completion(self):
        """Internal method to check if all mandatory onboarding steps are complete."""
        self.ensure_one()
        if self.kyc_status != 'approved':
            return False

        verified_bank_account = self.bank_account_ids.filtered(lambda b: b.verification_status == 'verified')
        if not verified_bank_account:
            return False

        latest_consent = self.get_latest_terms_consent()
        if not latest_consent: # Basic check, version check might be needed
            return False
        # Add logic here to check against current active ToS/Privacy versions from PlatformSetting if needed
        # platform_tos_version = self.env['influence_gen.platform_setting'].get_param('influence_gen.default_tos_version')
        # platform_privacy_version = self.env['influence_gen.platform_setting'].get_param('influence_gen.default_privacy_policy_version')
        # if latest_consent.tos_version != platform_tos_version or latest_consent.privacy_policy_version != platform_privacy_version:
        #     return False


        verified_social_profile = self.social_media_profile_ids.filtered(lambda s: s.verification_status == 'verified')
        if not verified_social_profile:
            return False
            
        # Check onboarding_checklist_json for completion
        try:
            checklist = json.loads(self.onboarding_checklist_json or '{}')
            if not checklist.get('kyc_submitted') or \
               not checklist.get('bank_submitted') or \
               not checklist.get('tos_agreed') or \
               not checklist.get('social_media_verified'): # Simplified example, more granular checks can be added
                return False
        except json.JSONDecodeError:
            return False # Invalid JSON means incomplete

        return True

    def get_latest_terms_consent(self):
        """Fetches the most recent terms consent record for the influencer."""
        self.ensure_one()
        return self.env['influence_gen.terms_consent'].search([
            ('influencer_profile_id', '=', self.id)
        ], order='consent_date desc', limit=1)

    def update_onboarding_step_status(self, step_key, status=True):
        """Updates the onboarding_checklist_json for a given step."""
        self.ensure_one()
        try:
            checklist = json.loads(self.onboarding_checklist_json or '{}')
        except json.JSONDecodeError:
            checklist = {}
        checklist[step_key] = status
        self.onboarding_checklist_json = json.dumps(checklist)

    def get_primary_bank_account(self):
        """Returns the primary bank account for payouts."""
        self.ensure_one()
        return self.bank_account_ids.filtered(lambda b: b.is_primary)