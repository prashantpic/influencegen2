# -*- coding: utf-8 -*-
import re
import uuid
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class InfluenceGenSocialMediaProfile(models.Model):
    _name = 'influence_gen.social_media_profile'
    _description = "Influencer Social Media Profile"

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Influencer Profile",
        required=True,
        ondelete='cascade',
        index=True
    )
    platform = fields.Selection([
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('twitter_x', 'Twitter/X'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('other', 'Other')
    ], string="Platform", required=True)
    platform_other = fields.Char(string="Other Platform Name")
    handle = fields.Char(string="Handle/Username", required=True)
    url = fields.Char(string="Profile URL")
    verification_status = fields.Selection([
        ('pending', 'Pending'),
        ('verification_initiated', 'Verification Initiated'),
        ('verified', 'Verified'),
        ('failed', 'Failed')
    ], string="Ownership Verification Status", default='pending', required=True, tracking=True, index=True)
    verification_method = fields.Selection([
        ('oauth', 'OAuth'),
        ('code_in_bio', 'Code in Bio/Post'),
        ('manual', 'Manual Review'),
        ('api_insights', 'API Insights')
    ], string="Verification Method")
    verification_code = fields.Char(string="System-Generated Verification Code", copy=False) # For 'code_in_bio' method
    verified_at = fields.Datetime(string="Verified At", readonly=True)
    audience_metrics_json = fields.Text(string="Audience Metrics (JSON)", help="e.g., follower_count, engagement_rate")
    last_fetched_at = fields.Datetime(string="Metrics Last Fetched At")

    _sql_constraints = [
        ('platform_handle_influencer_uniq',
         'unique(platform, handle, influencer_profile_id)',
         'This social media handle is already registered for this platform by the influencer.')
    ]

    @api.constrains('url', 'platform')
    def _check_url_format(self) -> None:
        """
        Validate URL format based on platform. REQ-DMG-015.
        """
        for record in self:
            if record.url:
                # Basic URL check
                if not re.match(r"^https?://[^\s/$.?#].[^\s]*$", record.url):
                    raise ValidationError(_("Invalid URL format for %s.", record.url))
                # Platform specific checks (examples)
                if record.platform == 'instagram' and 'instagram.com' not in record.url:
                    raise ValidationError(_("Instagram URL does not seem valid."))
                if record.platform == 'tiktok' and 'tiktok.com' not in record.url:
                    raise ValidationError(_("TikTok URL does not seem valid."))
                # Add more platform specific regex if needed

    def action_initiate_verification(self, method: str) -> dict:
        """
        Called by OnboardingService to start a verification process. REQ-IOKYC-006.
        """
        self.ensure_one()
        self.verification_method = method
        details = {}

        if method == 'code_in_bio':
            # Generate a unique verification_code
            self.verification_code = str(uuid.uuid4())[:8] # Example: 8 char code
            details['verification_code'] = self.verification_code
            details['instructions'] = _("Please place the code '%s' in your %s profile bio or a new post.", self.verification_code, self.platform)
        
        self.verification_status = 'verification_initiated'
        
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='SOCIAL_MEDIA_VERIFICATION_INITIATED',
            actor_user_id=self.env.user.id,
            action_performed='INITIATE_VERIFICATION',
            target_object=self,
            details_dict={'method': method, 'code_generated': self.verification_code if method == 'code_in_bio' else None}
        )
        return details

    def action_confirm_verification(self, verification_input: str = None) -> bool:
        """
        Called by OnboardingService to confirm verification. REQ-IOKYC-006.
        """
        self.ensure_one()
        success = False
        audit_details = {'method': self.verification_method, 'input_provided': bool(verification_input)}

        if self.verification_method == 'code_in_bio':
            # External check simulated here or confirmed by admin through UI
            # For simulation, assume verification_input is the code found by system/admin
            if verification_input and self.verification_code and verification_input.strip() == self.verification_code.strip():
                success = True
            else:
                audit_details['failure_reason'] = 'Code mismatch or not found'
        elif self.verification_method == 'oauth':
            # This implies an external OAuth flow, result passed via verification_input (e.g., token or success flag)
            # For simulation:
            if verification_input == 'oauth_success_token': # Placeholder
                success = True
            else:
                audit_details['failure_reason'] = 'OAuth failed or token invalid'
        elif self.verification_method == 'manual':
            # Admin marks as verified directly, no input needed here usually other than admin action
            success = True # Assuming this method is called by an admin confirming it
        elif self.verification_method == 'api_insights':
            # Infrastructure layer would typically confirm this via API call
            if verification_input == 'api_verified': # Placeholder
                success = True
            else:
                audit_details['failure_reason'] = 'API insights could not verify ownership'
        else:
            raise UserError(_("Unknown verification method: %s", self.verification_method))

        if success:
            self.write({
                'verification_status': 'verified',
                'verified_at': fields.Datetime.now(),
            })
            self.influencer_profile_id.update_onboarding_step_status('social_media_verified', True) # Example key
            audit_details['outcome'] = 'verified'
        else:
            self.write({'verification_status': 'failed'})
            audit_details['outcome'] = 'failed'

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='SOCIAL_MEDIA_VERIFICATION_CONFIRMED',
            actor_user_id=self.env.user.id,
            action_performed='CONFIRM_VERIFICATION',
            target_object=self,
            details_dict=audit_details,
            outcome='success' if success else 'failure'
        )
        return success

    def fetch_audience_metrics(self) -> None:
        """
        Placeholder for potential future enhancement to fetch metrics from social media APIs.
        """
        self.ensure_one()
        # This would call an external service via the infrastructure layer.
        # e.g., self.env['influence_gen_integration.social_api_service'].fetch_metrics(self.platform, self.handle)
        # and then update self.audience_metrics_json and self.last_fetched_at
        _logger.info(f"Placeholder: Fetching audience metrics for {self.platform} - {self.handle}")
        # For now, simulate some data or leave for manual input
        self.write({
            'audience_metrics_json': json.dumps({'followers': 1000, 'engagement_rate': 0.05}),
            'last_fetched_at': fields.Datetime.now()
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='SOCIAL_MEDIA_METRICS_FETCHED',
            actor_user_id=self.env.user.id, # or system
            action_performed='FETCH_METRICS',
            target_object=self
        )

    @api.onchange('platform')
    def _onchange_platform(self):
        if self.platform != 'other':
            self.platform_other = False