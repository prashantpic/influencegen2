from odoo import models, fields, api, _
from odoo.exceptions import UserError

# Assuming UsageTrackingLog model exists or will be created elsewhere
# For now, we'll log its creation intent.

class InfluenceGenAiImageGenerationRequest(models.Model):
    _name = 'influence_gen.ai_image_generation_request'
    _description = "AI Image Generation Request"
    _order = 'create_date desc'

    user_id = fields.Many2one('res.users', string="Requesting User", required=True, ondelete='restrict', index=True)
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Associated Influencer Profile",
        compute='_compute_influencer_profile',
        store=True,
        readonly=True,
        index=True
    )
    campaign_id = fields.Many2one('influence_gen.campaign', string="Associated Campaign", ondelete='set null', index=True)
    prompt = fields.Text(string="Prompt", required=True)
    negative_prompt = fields.Text(string="Negative Prompt")
    model_id = fields.Many2one('influence_gen.ai_image_model', string="AI Model Used", required=True, ondelete='restrict')
    resolution_width = fields.Integer(string="Width (px)")
    resolution_height = fields.Integer(string="Height (px)")
    aspect_ratio = fields.Char(string="Aspect Ratio", help="e.g., '1:1', '16:9'")
    seed = fields.Integer(string="Seed")
    inference_steps = fields.Integer(string="Inference Steps")
    cfg_scale = fields.Float(string="CFG Scale", digits=(3, 1)) # (total_digits, decimal_places)
    status = fields.Selection([
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='queued', required=True, tracking=True, index=True)
    intended_use = fields.Selection([
        ('personal_exploration', 'Personal Exploration'),
        ('campaign_specific', 'Campaign Specific')
    ], string="Intended Use", default='personal_exploration', required=True)
    error_details = fields.Text(string="Error Details", readonly=True)
    n8n_execution_id = fields.Char(string="N8N Execution ID", readonly=True, index=True)
    generated_image_ids = fields.One2many('influence_gen.generated_image', 'request_id', string="Generated Images")
    
    # Assuming usage_tracking_log_ids is a One2many to a dedicated UsageTrackingLog model
    # For now, it's mentioned in SDS but the model itself is not detailed for creation in this file.
    # We will log usage via the _log_usage helper.
    # usage_tracking_log_ids = fields.One2many('influence_gen.usage_tracking_log', 'ai_request_id', string="Usage Logs")


    @api.depends('user_id')
    def _compute_influencer_profile(self):
        for record in self:
            if record.user_id:
                profile = self.env['influence_gen.influencer_profile'].search([('user_id', '=', record.user_id.id)], limit=1)
                record.influencer_profile_id = profile.id
            else:
                record.influencer_profile_id = False

    def action_cancel_request(self):
        for record in self:
            if record.status not in ('queued', 'processing'):
                raise UserError(_("Request cannot be cancelled as it is already %s.", record.status))
            
            # Potentially notify N8N if 'processing' to attempt cancellation there
            # if record.status == 'processing' and record.n8n_execution_id:
            #     self.env['influence_gen.infrastructure.integration.service'].cancel_n8n_workflow(record.n8n_execution_id)

            record.status = 'cancelled'
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='AI_REQUEST_CANCELLED',
                actor_user_id=self.env.user.id,
                action_performed='UPDATE',
                target_object=record,
                details_dict={'request_id': record.id}
            )
            # Revert quota if applicable (handled by AIImageService or a dedicated quota service)
        return True

    def _log_usage(self, event_type="request_created", details=None):
        """
        Internal helper to create UsageTrackingLog entries. REQ-AIGS-007.
        This is a placeholder for interaction with a dedicated 'influence_gen.usage_tracking_log' model.
        The actual creation would be:
        self.env['influence_gen.usage_tracking_log'].create({
            'user_id': self.user_id.id,
            'influencer_profile_id': self.influencer_profile_id.id,
            'ai_request_id': self.id,
            'event_type': event_type, # e.g., 'request_created', 'generation_success', 'generation_failure'
            'usage_units': 1, # or based on parameters
            'details_json': json.dumps(details) if details else None,
        })
        """
        self.ensure_one()
        # For now, we'll log an audit entry indicating usage logging intent
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='AI_USAGE_LOG_INTENT', # Placeholder
            actor_user_id=self.user_id.id,
            action_performed='LOG',
            target_object=self,
            details_dict={
                'request_id': self.id,
                'usage_event_type': event_type,
                'usage_details': details or {}
            }
        )