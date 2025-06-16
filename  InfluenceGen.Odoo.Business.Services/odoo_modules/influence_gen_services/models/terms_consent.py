# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class InfluenceGenTermsConsent(models.Model):
    _name = 'influence_gen.terms_consent'
    _description = "Influencer Terms and Policy Consent"
    _order = 'consent_date desc'

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string="Influencer Profile",
        required=True, ondelete='cascade', index=True
    )
    tos_version = fields.Char(string="Terms of Service Version", required=True)
    privacy_policy_version = fields.Char(string="Privacy Policy Version", required=True)
    consent_date = fields.Datetime(
        string="Consent Date", default=fields.Datetime.now,
        required=True, readonly=True
    )
    ip_address = fields.Char(string="IP Address of Consent")

    @api.model
    def create_consent(cls, influencer_id, tos_version, privacy_policy_version, ip_address=None):
        """Logs a new consent record. REQ-IOKYC-009."""
        influencer = cls.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer.exists():
            # This case should ideally be caught by the service layer
            raise ValueError(_("Influencer with ID %s not found.", influencer_id))

        consent_data = {
            'influencer_profile_id': influencer_id,
            'tos_version': tos_version,
            'privacy_policy_version': privacy_policy_version,
            'ip_address': ip_address,
            'consent_date': fields.Datetime.now(), # Ensure it's set at creation
        }
        consent = cls.create(consent_data)

        influencer.update_onboarding_step_status('terms_agreed', True)
        
        cls.env['influence_gen.audit_log_entry'].create_log(
            event_type='TERMS_CONSENT_CREATED',
            actor_user_id=influencer.user_id.id, # Action by the influencer
            action_performed='CREATE_CONSENT',
            target_object=consent,
            details_dict={
                'tos_version': tos_version,
                'privacy_policy_version': privacy_policy_version,
                'ip_address': ip_address
            }
        )
        return consent