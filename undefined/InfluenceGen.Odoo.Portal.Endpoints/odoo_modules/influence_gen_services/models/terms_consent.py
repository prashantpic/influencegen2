import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TermsConsent(models.Model):
    """
    Records an influencer's agreement to a specific version of Terms of Service and Privacy Policy.
    REQ-DMG-002, REQ-IOKYC-009, REQ-ATEL-005
    """
    _name = 'influence_gen.terms_consent'
    _description = 'Terms Consent Record'
    _inherit = ['influence_gen.base_audit_mixin'] # Audit for creation
    _order = 'consent_date desc'

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string='Influencer Profile',
        required=True, ondelete='cascade', index=True, tracking=True
    )
    tos_version = fields.Char(string='Terms of Service Version', required=True, tracking=True)
    privacy_policy_version = fields.Char(string='Privacy Policy Version', required=True, tracking=True)
    consent_date = fields.Datetime(
        string='Consent Date', required=True, default=fields.Datetime.now,
        readonly=True, tracking=True,
        help="Timestamp when the consent was given."
    )
    ip_address = fields.Char(string='IP Address of Consent', readonly=True, tracking=True, copy=False)
    user_agent = fields.Text(string='User Agent of Consent', readonly=True, tracking=True, copy=False)

    company_id = fields.Many2one(related='influencer_profile_id.company_id', store=True)

    @api.model
    def create(self, vals):
        # Potentially capture IP and User Agent if available in request context
        # This is more reliably done in a controller or service layer that calls this create.
        # For example:
        # if self.env.context.get('request_ip'):
        #     vals['ip_address'] = self.env.context.get('request_ip')
        # if self.env.context.get('request_user_agent'):
        #     vals['user_agent'] = self.env.context.get('request_user_agent')
        
        record = super(TermsConsent, self).create(vals)
        _logger.info(f"Terms consent record {record.id} created for influencer {record.influencer_profile_id.id} "
                     f"(ToS: {record.tos_version}, PP: {record.privacy_policy_version}).")
        
        # Check if this consent completes onboarding
        if record.influencer_profile_id.account_status == 'pending_verification':
            record.influencer_profile_id.check_onboarding_completion()
        return record