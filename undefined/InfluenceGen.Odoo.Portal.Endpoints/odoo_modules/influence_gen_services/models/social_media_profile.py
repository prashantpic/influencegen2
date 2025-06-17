import logging
import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class SocialMediaProfile(models.Model):
    """
    Represents an influencer's social media account on a specific platform.
    REQ-DMG-002, REQ-IOKYC-002, REQ-IOKYC-003, REQ-IOKYC-006, REQ-IOKYC-014
    """
    _name = 'influence_gen.social_media_profile'
    _description = 'Social Media Profile'
    _inherit = ['influence_gen.base_audit_mixin']

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string='Influencer Profile',
        required=True, ondelete='cascade', index=True
    )
    platform = fields.Selection([
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter / X'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('pinterest', 'Pinterest'),
        ('other', 'Other'),
    ], string='Platform', required=True, index=True)
    handle = fields.Char(string='Handle / Username', required=True, tracking=True)
    url = fields.Char(string='Profile URL', tracking=True)
    verification_status = fields.Selection([
        ('pending', 'Pending'),
        ('verification_initiated', 'Verification Initiated'),
        ('verified', 'Verified'),
        ('failed', 'Failed'),
        ('requires_manual_review', 'Requires Manual Review'),
    ], string='Verification Status', default='pending', required=True, tracking=True, index=True)
    verification_method = fields.Selection([
        ('oauth', 'OAuth'),
        ('code_in_bio', 'Code in Bio/Post'),
        ('manual', 'Manual Admin Verification'),
        ('api_challenge', 'API Challenge'),
        ('not_applicable', 'Not Applicable')
    ], string='Verification Method', tracking=True)
    verification_code = fields.Char(string='Verification Code', tracking=True, copy=False,
                                    help="Code to be placed in bio or provided by influencer.")
    verified_at = fields.Datetime(string='Verified At', readonly=True, tracking=True)
    audience_metrics_json = fields.Json(string='Audience Metrics (JSON)',
                                         help="Fetched or calculated audience metrics like follower count, engagement rate.")

    _sql_constraints = [
        ('platform_handle_influencer_unique',
         'UNIQUE(platform, handle, influencer_profile_id)',
         'The combination of platform, handle, and influencer must be unique.')
    ]

    @api.constrains('url')
    def _check_url_format(self):
        """Validates the URL format."""
        for record in self:
            if record.url:
                # Basic URL validation, can be enhanced
                if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', record.url):
                    raise ValidationError(_("The profile URL '%s' is not valid.") % record.url)

    def action_start_verification(self, method=None):
        """
        Initiates the verification process for this social media profile.
        REQ-IOKYC-006 (partially, service layer orchestrates)
        """
        self.ensure_one()
        if method:
            self.verification_method = method

        if self.verification_method == 'code_in_bio':
            # Generate a unique code
            code = self.env['ir.sequence'].next_by_code('social.media.verification.code') or fields.datetime.now().strftime('%Y%m%d%H%M%S%f')
            self.verification_code = code
            self.verification_status = 'verification_initiated'
            self.message_post(body=_("Verification initiated with method '%s'. Please add code '%s' to your profile bio/description.") % (self.verification_method, code))
        elif self.verification_method == 'oauth':
            self.verification_status = 'verification_initiated'
            self.message_post(body=_("OAuth verification process needs to be started externally for %s.") % self.url)
            # Logic to redirect to OAuth provider or provide link would be in controller/UI
            # This action might just set status and expect callback or further user action
        elif self.verification_method == 'manual':
            self.verification_status = 'requires_manual_review'
            self.message_post(body=_("Profile submitted for manual verification by admin."))
        else:
            self.message_post(body=_("Verification started with method: %s") % self.verification_method)
            self.verification_status = 'verification_initiated'
        
        _logger.info(f"Verification started for social profile {self.id} (Influencer: {self.influencer_profile_id.id}) using method {self.verification_method}")


    def action_confirm_verification(self, input_code=None):
        """
        Confirms the verification based on the method and input.
        REQ-IOKYC-006 (partially, service layer orchestrates)
        """
        self.ensure_one()
        # This method would typically be called by OnboardingService
        # For simplicity in model, direct call assumed for now
        # Call the OnboardingService to handle the actual verification logic
        # service = self.env['influence_gen.services.onboarding_service']
        # result = service.verify_social_media_account(self.id, self.verification_method, verification_input=input_code)
        # For now, simulate success if code matches for 'code_in_bio'
        
        if self.verification_method == 'code_in_bio':
            if self.verification_code and input_code == self.verification_code: # In real scenario, API would check bio
                self.verification_status = 'verified'
                self.verified_at = fields.Datetime.now()
                self.message_post(body=_("Social media profile successfully verified via code."))
                _logger.info(f"Social profile {self.id} verified for influencer {self.influencer_profile_id.id}.")
                self.influencer_profile_id.check_onboarding_completion() # Attempt activation if all set
                return True
            else:
                self.verification_status = 'failed'
                self.message_post(body=_("Social media profile verification failed. Code did not match."))
                _logger.warning(f"Social profile {self.id} verification failed for influencer {self.influencer_profile_id.id}.")
                return False
        # Other methods (OAuth, API Challenge) would have more complex logic, likely handled by services
        # For manual verification, an admin would directly set status to 'verified'
        _logger.info(f"Confirm verification called for {self.id} with method {self.verification_method}.")
        return False # Default for other methods not implemented here