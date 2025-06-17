from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class UsageTrackingLog(models.Model):
    """
    Logs instances of platform feature usage for tracking, analytics, quota management,
    and resource planning. Particularly important for AI image generation (REQ-AIGS-007).
    """
    _name = 'influence_gen.usage_tracking_log'
    _description = 'Platform Feature Usage Tracking Log'
    # No BaseAuditMixin here to avoid recursive logging if audit logs itself generate usage.
    # Creation is typically done by services and is an audit-worthy event in itself logged by the service.
    _order = 'timestamp desc, id desc'

    user_id = fields.Many2one(
        'res.users',
        string='User',
        ondelete='set null', # Keep log even if user is deleted
        index=True,
        help="The user who performed the action leading to this usage."
    )
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string='Influencer Profile',
        ondelete='set null', # Keep log even if profile is deleted
        index=True,
        help="The influencer profile associated with this usage, if applicable."
    )
    feature_name = fields.Char(
        string='Feature Name',
        required=True,
        index=True,
        help="Identifier for the platform feature used, e.g., 'ai_image_generation', 'campaign_application_submission'."
    )
    timestamp = fields.Datetime(
        string='Timestamp (UTC)',
        required=True,
        default=fields.Datetime.now,
        index=True,
        help="Timestamp when the usage occurred."
    )
    campaign_id = fields.Many2one(
        'influence_gen.campaign',
        string='Campaign Context',
        ondelete='set null',
        index=True,
        help="Campaign associated with this usage, if applicable (e.g., AI image for a campaign)."
    )
    details_json = fields.Text(
        string='Details (JSON)',
        help="JSON string containing feature-specific usage details. "
             "For AI: {'model_id': X, 'num_images': Y, 'parameters': {...}, 'api_calls': Z}."
             "For general features: {'record_id': X, 'action': 'create'}"
    )
    # Consider adding a 'unit_cost' or 'units_consumed' if applicable for chargebacks or detailed quota.
    # For AI, 'units_consumed' could be number of images generated or API credits.
    units_consumed = fields.Integer(
        string='Units Consumed',
        default=0,
        help="Number of units consumed for this feature usage, e.g., images generated, API calls."
    )
    request_id = fields.Many2one(
        'influence_gen.ai_image_generation_request',
        string="AI Request Reference",
        ondelete='set null',
        index=True,
        help="Reference to the AI Image Generation Request if this log entry is related to it."
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        readonly=True
    )

    @api.model
    def log_usage(self, user_id, feature_name, influencer_profile_id=None, campaign_id=None, details=None, units_consumed=0, request_id=None):
        """
        Helper method to create a usage log entry.
        Called by various services.
        REQ-DMG-023: Log platform feature usage
        REQ-AIGS-007: Log AI usage details
        """
        log_vals = {
            'user_id': user_id,
            'feature_name': feature_name,
            'influencer_profile_id': influencer_profile_id,
            'campaign_id': campaign_id,
            'details_json': details if isinstance(details, str) else (None if details is None else వివరాలు), # Ensure details is JSON string
            'units_consumed': units_consumed,
            'request_id': request_id,
            'timestamp': fields.Datetime.now(), # Ensure fresh timestamp
        }
        try:
            usage_log = self.create(log_vals)
            _logger.info(f"Usage logged for feature '{feature_name}' by user ID {user_id}: Log ID {usage_log.id}")
            return usage_log
        except Exception as e:
            _logger.error(f"Failed to log usage for feature '{feature_name}': {e}. Vals: {log_vals}")
            return None

    # No specific methods needed beyond creation, which is handled by services.
    # Access to this model should be restricted for reporting/admin purposes.
    # Security rules will prevent direct write/unlink by most users.