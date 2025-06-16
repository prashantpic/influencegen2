from odoo import models, fields, api, _

class InfluenceGenTermsConsent(models.Model):
    _name = 'influence_gen.terms_consent'
    _description = "Influencer Terms and Policy Consent"
    _order = 'consent_date desc'

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Influencer Profile",
        required=True,
        ondelete='cascade',
        index=True
    )
    tos_version = fields.Char(string="Terms of Service Version", required=True)
    privacy_policy_version = fields.Char(string="Privacy Policy Version", required=True)
    consent_date = fields.Datetime(string="Consent Date", default=fields.Datetime.now, required=True, readonly=True)
    ip_address = fields.Char(string="IP Address of Consent")

    @api.model
    def create_consent(cls, influencer_id, tos_version, privacy_policy_version, ip_address=None):
        if not influencer_id or not tos_version or not privacy_policy_version:
            # Consider raising UserError or ValidationError
            return cls.env['influence_gen.terms_consent']

        influencer_profile = cls.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            # Consider raising UserError or ValidationError
            return cls.env['influence_gen.terms_consent']

        vals = {
            'influencer_profile_id': influencer_id,
            'tos_version': tos_version,
            'privacy_policy_version': privacy_policy_version,
            'ip_address': ip_address,
            'consent_date': fields.Datetime.now(), # Ensure it's set on creation
        }
        consent_record = cls.create(vals)

        influencer_profile.update_onboarding_step_status('tos_agreed', True)

        cls.env['influence_gen.audit_log_entry'].create_log(
            event_type='TERMS_CONSENT_CREATED',
            actor_user_id=influencer_profile.user_id.id, # Assumes influencer is logged in
            action_performed='CREATE',
            target_object=consent_record,
            details_dict={
                'influencer_id': influencer_id,
                'tos_version': tos_version,
                'privacy_policy_version': privacy_policy_version,
                'ip_address': ip_address
            }
        )
        return consent_record