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
    verification_code = fields.Char(string="System-Generated Verification Code", copy=False)
    verified_at = fields.Datetime(string="Verified At", readonly=True)
    audience_metrics_json = fields.Text(string="Audience Metrics (JSON)")
    last_fetched_at = fields.Datetime(string="Metrics Last Fetched At")

    _sql_constraints = [
        (
            'platform_handle_influencer_uniq',
            'unique(platform, handle, influencer_profile_id)',
            'This social media handle is already registered for this platform by the influencer.'
        )
    ]

    @api.constrains('url', 'platform')
    def _check_url_format(self):
        """Validate URL format based on platform. REQ-DMG-015."""
        for record in self:
            if record.url:
                if record.platform == 'instagram' and not re.match(r"^(https?://)?(www\.)?instagram\.com/.+", record.url):
                    raise ValidationError(_("Invalid Instagram URL format for %s.", record.handle))
                elif record.platform == 'tiktok' and not re.match(r"^(https?://)?(www\.)?tiktok\.com/@.+", record.url):
                    raise ValidationError(_("Invalid TikTok URL format for %s.", record.handle))
                elif record.platform == 'youtube' and not re.match(r"^(https?://)?(www\.)?youtube\.com/(user/|channel/|c/).+", record.url):
                     raise ValidationError(_("Invalid YouTube URL format for %s. Expected format like youtube.com/channel/..., youtube.com/user/..., or youtube.com/c/...", record.handle))
                elif record.platform == 'twitter_x' and not re.match(r"^(https?://)?(www\.)?(twitter\.com|x\.com)/.+", record.url):
                    raise ValidationError(_("Invalid Twitter/X URL format for %s.", record.handle))
                # Add more platform-specific regex checks as needed

    def action_initiate_verification(self, method):
        """Called by OnboardingService to start a verification process. REQ-IOKYC-006."""
        self.ensure_one()
        vals = {
            'verification_method': method,
            'verification_status': 'verification_initiated'
        }
        if method == 'code_in_bio':
            vals['verification_code'] = str(uuid.uuid4())[:8] # Generate a simple unique code

        self.write(vals)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='SOCIAL_MEDIA_VERIFICATION_INITIATED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'method': method, 'verification_code': vals.get('verification_code')}
        )
        return {'verification_code': vals.get('verification_code')} if method == 'code_in_bio' else True

    def action_confirm_verification(self, verification_input=None):
        """Called by OnboardingService to confirm verification. REQ-IOKYC-006."""
        self.ensure_one()
        # Actual verification logic would depend on the method and external checks
        # This is a simplified confirmation step.
        success = False
        audit_details = {'method': self.verification_method, 'input': verification_input}

        if self.verification_method == 'code_in_bio':
            # This would typically involve an admin checking the bio or an automated system
            # For simulation, we assume verification_input contains the code found.
            if verification_input and self.verification_code and verification_input == self.verification_code:
                success = True
            else:
                audit_details['failure_reason'] = 'Verification code mismatch or not found.'
        elif self.verification_method == 'oauth':
            # This implies an external OAuth flow, result passed via verification_input (e.g., {'status': 'success'})
            if isinstance(verification_input, dict) and verification_input.get('status') == 'success':
                success = True
            else:
                audit_details['failure_reason'] = 'OAuth verification failed or was not confirmed.'
        elif self.verification_method == 'manual':
            # Admin marks as verified directly via UI calling this
            success = True # Assuming verification_input signifies admin approval
        elif self.verification_method == 'api_insights':
            # Assume verification_input confirms API access and metrics retrieval
            if isinstance(verification_input, dict) and verification_input.get('status') == 'success':
                success = True
            else:
                audit_details['failure_reason'] = 'API Insights verification failed.'
        else:
            raise UserError(_("Unknown verification method: %s", self.verification_method))

        if success:
            self.write({
                'verification_status': 'verified',
                'verified_at': fields.Datetime.now()
            })
            if self.influencer_profile_id:
                self.influencer_profile_id.update_onboarding_step_status('social_media_verified', True)
        else:
            self.write({'verification_status': 'failed'})

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='SOCIAL_MEDIA_VERIFICATION_CONFIRMED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            outcome='success' if success else 'failure',
            failure_reason=audit_details.get('failure_reason'),
            details_dict=audit_details
        )
        return success

    def fetch_audience_metrics(self):
        """Placeholder for potential future enhancement to fetch metrics from social media APIs."""
        self.ensure_one()
        # This would call an external service via the infrastructure layer.
        # Example:
        # infra_service = self.env['influence_gen.infrastructure.social_api_service']
        # metrics = infra_service.get_metrics(self.platform, self.handle)
        # if metrics:
        #     self.write({
        #         'audience_metrics_json': json.dumps(metrics),
        #         'last_fetched_at': fields.Datetime.now()
        #     })
        # self.env['influence_gen.audit_log_entry'].create_log(
        #     event_type='SOCIAL_MEDIA_METRICS_FETCHED',
        #     actor_user_id=self.env.user.id, # Or system
        #     action_performed='READ_EXTERNAL',
        #     target_object=self
        # )
        raise NotImplementedError(_("Fetching audience metrics is not yet implemented."))