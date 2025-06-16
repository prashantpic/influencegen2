# -*- coding: utf-8 -*-
import re
import uuid
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class InfluenceGenSocialMediaProfile(models.Model):
    _name = 'influence_gen.social_media_profile'
    _description = "Influencer Social Media Profile"

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string="Influencer Profile",
        required=True, ondelete='cascade', index=True
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
    verification_code = fields.Char(string="System-Generated Verification Code")
    verified_at = fields.Datetime(string="Verified At", readonly=True)
    audience_metrics_json = fields.Text(string="Audience Metrics (JSON)")
    last_fetched_at = fields.Datetime(string="Metrics Last Fetched At")

    _sql_constraints = [
        ('platform_handle_influencer_uniq',
         'unique(platform, handle, influencer_profile_id)',
         'This social media handle is already registered for this platform by the influencer.')
    ]

    @api.constrains('url', 'platform')
    def _check_url_format(self):
        """Validate URL format based on platform. REQ-DMG-015."""
        for record in self:
            if record.url:
                # Basic URL validation
                if not re.match(r"^https?://[^\s/$.?#].[^\s]*$", record.url):
                    raise ValidationError(_("Invalid URL format for %s.", record.url))
                # Platform specific checks (examples)
                if record.platform == 'instagram' and 'instagram.com/' not in record.url:
                    raise ValidationError(_("Instagram URL should contain 'instagram.com/'."))
                if record.platform == 'tiktok' and 'tiktok.com/' not in record.url:
                     raise ValidationError(_("TikTok URL should contain 'tiktok.com/'."))
                # Add more platform specific regex if needed

    def action_initiate_verification(self, method):
        """Called by OnboardingService to start a verification process. REQ-IOKYC-006."""
        self.ensure_one()
        vals = {
            'verification_method': method,
            'verification_status': 'verification_initiated',
        }
        if method == 'code_in_bio':
            vals['verification_code'] = str(uuid.uuid4())[:8] # Generate a simple code
        
        self.write(vals)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='SOCIAL_MEDIA_VERIFICATION_INITIATED',
            actor_user_id=self.env.user.id,
            action_performed='INITIATE_VERIFICATION',
            target_object=self,
            details_dict={'method': method}
        )
        return {'verification_code': vals.get('verification_code')}

    def action_confirm_verification(self, verification_input=None):
        """Called by OnboardingService to confirm verification. REQ-IOKYC-006."""
        self.ensure_one()
        success = False
        audit_details = {'method': self.verification_method, 'input': verification_input}

        if self.verification_method == 'code_in_bio':
            # This part usually involves an admin or automated system checking the bio/post
            # For simulation, we assume verification_input is the code found
            if self.verification_code and verification_input == self.verification_code:
                success = True
        elif self.verification_method == 'oauth':
            # OAuth flow would set verification_input to a success token or flag
            if verification_input == 'oauth_success_token': # Placeholder
                success = True
        elif self.verification_method == 'manual':
            # Admin manually confirms
            success = True # Assuming this action is called by an admin marking it as verified
        elif self.verification_method == 'api_insights':
             # API Insights verification would set verification_input to a success flag
            if verification_input == 'api_insights_verified': # Placeholder
                success = True
        else:
            raise UserError(_("Unknown verification method: %s", self.verification_method))

        if success:
            self.write({
                'verification_status': 'verified',
                'verified_at': fields.Datetime.now()
            })
            self.influencer_profile_id.update_onboarding_step_status('social_media_verified', True)
            audit_outcome = 'success'
        else:
            self.write({'verification_status': 'failed'})
            audit_outcome = 'failure'

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='SOCIAL_MEDIA_VERIFICATION_CONFIRMED',
            actor_user_id=self.env.user.id,
            action_performed='CONFIRM_VERIFICATION',
            target_object=self,
            details_dict=audit_details,
            outcome=audit_outcome
        )
        return success

    def fetch_audience_metrics(self):
        """Placeholder for potential future enhancement to fetch metrics from social media APIs."""
        # This would call an external service via the infrastructure layer.
        # e.g., self.env['influence_gen.infrastructure.integration.services'].fetch_social_metrics(self.id)
        # For now, it's a placeholder.
        _logger.info("fetch_audience_metrics called for SocialMediaProfile %s (Not Implemented)", self.id)
        return False