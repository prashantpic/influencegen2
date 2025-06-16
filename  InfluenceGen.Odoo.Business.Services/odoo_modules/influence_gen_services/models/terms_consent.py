# -*- coding: utf-8 -*-
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
    consent_date = fields.Datetime(
        string="Consent Date",
        default=fields.Datetime.now,
        required=True,
        readonly=True
    )
    ip_address = fields.Char(string="IP Address of Consent")

    @api.model
    def create_consent(self, influencer_id: int, tos_version: str, privacy_policy_version: str, ip_address: str = None) -> models.Model:
        """
        Logs a new consent record. REQ-IOKYC-009.
        """
        if not influencer_id or not tos_version or not privacy_policy_version:
            raise ValueError(_("Influencer ID, ToS version, and Privacy Policy version are required to log consent."))

        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            raise ValueError(_("Influencer profile with ID %s not found.", influencer_id))

        consent_data = {
            'influencer_profile_id': influencer_id,
            'tos_version': tos_version,
            'privacy_policy_version': privacy_policy_version,
            'consent_date': fields.Datetime.now(),
            'ip_address': ip_address,
        }
        consent_record = self.create(consent_data)

        influencer_profile.update_onboarding_step_status('terms_agreed', True)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='TERMS_CONSENT_LOGGED',
            actor_user_id=influencer_profile.user_id.id, # Action by influencer
            action_performed='LOG_CONSENT',
            target_object=consent_record,
            details_dict={
                'tos_version': tos_version,
                'privacy_policy_version': privacy_policy_version,
                'ip_address': ip_address
            }
        )
        return consent_record