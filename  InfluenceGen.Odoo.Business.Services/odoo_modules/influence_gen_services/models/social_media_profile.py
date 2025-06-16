import uuid
import re
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
        for record in self:
            if record.url:
                # Basic URL validation
                if not re.match(r"^https?://[^\s/$.?#].[^\s]*$", record.url):
                    raise ValidationError(_("Invalid URL format for %s.", record.platform))
                # Platform specific checks (examples)
                if record.platform == 'instagram' and 'instagram.com/' not in record.url:
                    raise ValidationError(_("Instagram URL does not seem valid."))
                if record.platform == 'tiktok' and 'tiktok.com/' not in record.url:
                    raise ValidationError(_("TikTok URL does not seem valid."))
                # Add more platform-specific regex if needed

    def action_initiate_verification(self, method):
        self.ensure_one()
        if self.verification_status == 'verified':
            raise UserError(_("This profile is already verified."))

        vals = {
            'verification_method': method,
            'verification_status': 'verification_initiated'
        }
        verification_details = {}

        if method == 'code_in_bio':
            code = str(uuid.uuid4())[:8].upper() # Generate a simple code
            vals['verification_code'] = code
            verification_details['code'] = code
            verification_details['instructions'] = _("Please place the code '%s' in your profile bio or a new post.", code)

        self.write(vals)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='SOCIAL_MEDIA_VERIFICATION_INITIATED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'method': method, 'profile_id': self.id}
        )
        return verification_details

    def action_confirm_verification(self, verification_input=None):
        self.ensure_one()
        if self.verification_status == 'verified':
            return True # Already verified

        success = False
        if self.verification_method == 'code_in_bio':
            # This part requires an external check.
            # Assume verification_input is True if admin/system confirmed code is present.
            if verification_input is True: # Or compare verification_input (code found) with self.verification_code
                success = True
            elif isinstance(verification_input, str) and verification_input == self.verification_code: # for automated check
                 success = True

        elif self.verification_method == 'oauth':
            # OAuth flow result would be passed in verification_input (e.g., token or success flag)
            if verification_input and verification_input.get('status') == 'success':
                success = True
        elif self.verification_method == 'manual':
            # Admin manually marks as verified, so input is implicitly True
            success = True
        elif self.verification_method == 'api_insights':
            # If metrics can be fetched successfully as proof
            if verification_input and verification_input.get('metrics_fetched') is True:
                success = True


        if success:
            self.write({
                'verification_status': 'verified',
                'verified_at': fields.Datetime.now()
            })
            self.influencer_profile_id.update_onboarding_step_status('social_media_verified', True) # General flag
            self.influencer_profile_id.update_onboarding_step_status(f'social_media_{self.platform}_verified', True) # Specific flag

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='SOCIAL_MEDIA_VERIFICATION_CONFIRMED',
                actor_user_id=self.env.user.id,
                action_performed='UPDATE',
                target_object=self,
                details_dict={'profile_id': self.id, 'status': 'verified'}
            )
        else:
            self.write({'verification_status': 'failed'})
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='SOCIAL_MEDIA_VERIFICATION_FAILED',
                actor_user_id=self.env.user.id,
                action_performed='UPDATE',
                target_object=self,
                details_dict={'profile_id': self.id, 'status': 'failed', 'reason': verification_input}
            )
        return success

    def fetch_audience_metrics(self):
        # Placeholder for future enhancement.
        # This would typically call an infrastructure service.
        # self.env['influence_gen.infrastructure.integration.service'].fetch_social_metrics(self.id)
        self.ensure_one()
        _logger.info(f"Placeholder: Fetching audience metrics for social media profile {self.id}")
        # Example update:
        # self.write({
        #     'audience_metrics_json': json.dumps({'followers': 1000, 'engagement_rate': 0.05}),
        #     'last_fetched_at': fields.Datetime.now()
        # })
        return False