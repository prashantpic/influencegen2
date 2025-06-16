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

    def action_activate_account(self):
        self.ensure_one()
        if self.kyc_status != 'approved':
            raise UserError(_("KYC must be approved before activating the account."))
        if not self.check_onboarding_completion():
            raise UserError(_("All required onboarding steps must be completed before activating the account."))

        self.write({'account_status': 'active'})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='ACCOUNT_ACTIVATED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'old_status': self.account_status, 'new_status': 'active'}
        )
        # Trigger notification "Account Activated" via notification service (REPO-IGOII-004)
        # This typically would be:
        # self.env['influence_gen.infrastructure.integration.service'].send_notification(
        #     user_id=self.user_id.id,
        #     message_type='account_activated',
        #     message_params={'influencer_name': self.name}
        # )
        # Placeholder for actual notification call to infra layer
        self.message_post(body=_("Account activated."))
        return True

    def action_deactivate_account(self, reason="Administrative action"):
        self.ensure_one()
        old_status = self.account_status
        self.write({'account_status': 'suspended'}) # Or 'inactive' based on more specific logic
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='ACCOUNT_DEACTIVATED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'old_status': old_status, 'new_status': self.account_status, 'reason': reason}
        )
        # Trigger notification "Account Deactivated/Suspended"
        # self.env['influence_gen.infrastructure.integration.service'].send_notification(
        #     user_id=self.user_id.id,
        #     message_type='account_deactivated',
        #     message_params={'influencer_name': self.name, 'reason': reason}
        # )
        self.message_post(body=_("Account deactivated/suspended. Reason: %s", reason))
        return True

    def update_kyc_status(self, new_status, notes=None):
        self.ensure_one()
        old_status = self.kyc_status
        self.write({'kyc_status': new_status})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_STATUS_UPDATED',
            actor_user_id=self.env.user.id, # Or system if automated
            action_performed='UPDATE',
            target_object=self,
            details_dict={'old_status': old_status, 'new_status': new_status, 'notes': notes or ''}
        )
        if new_status == 'approved':
            if self.check_onboarding_completion(): # Check if other steps are also done
                 self.action_activate_account()
        # Notification is expected to be triggered by the calling service (e.g., OnboardingService)
        # or the specific KYCData action method.

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError(_("Invalid email address format: %s", record.email))

    def check_onboarding_completion(self):
        self.ensure_one()
        if self.kyc_status != 'approved':
            return False
        if not self.bank_account_ids.filtered(lambda b: b.verification_status == 'verified'):
            return False
        latest_consent = self.get_latest_terms_consent()
        if not latest_consent: # Basic check, version check would be more robust
            return False
        # Add version check against PlatformSetting for current ToS/Privacy versions if needed
        # current_tos_version = self.env['influence_gen.platform_setting'].get_param('influence_gen.default_tos_version')
        # current_privacy_version = self.env['influence_gen.platform_setting'].get_param('influence_gen.default_privacy_policy_version')
        # if latest_consent.tos_version != current_tos_version or latest_consent.privacy_policy_version != current_privacy_version:
        #     return False

        if not self.social_media_profile_ids.filtered(lambda s: s.verification_status == 'verified'):
            return False
        
        # Check from JSON checklist as well
        try:
            checklist = json.loads(self.onboarding_checklist_json or '{}')
            if not checklist.get('kyc_submitted') or \
               not checklist.get('bank_submitted') or \
               not checklist.get('tos_agreed') or \
               not checklist.get('social_media_verified'): # Assuming a key for overall social media verification
                return False
        except json.JSONDecodeError:
            return False # Invalid JSON means checklist is not properly maintained

        return True

    def get_latest_terms_consent(self):
        self.ensure_one()
        return self.env['influence_gen.terms_consent'].search([
            ('influencer_profile_id', '=', self.id)
        ], order='consent_date desc', limit=1)

    def update_onboarding_step_status(self, step_key, status=True):
        self.ensure_one()
        try:
            checklist = json.loads(self.onboarding_checklist_json or '{}')
        except json.JSONDecodeError:
            checklist = {}
        
        checklist[step_key] = status
        self.onboarding_checklist_json = json.dumps(checklist)

    def get_primary_bank_account(self):
        self.ensure_one()
        return self.bank_account_ids.filtered(lambda b: b.is_primary)