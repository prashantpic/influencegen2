# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class InfluenceGenAiImageGenerationRequest(models.Model):
    _name = 'influence_gen.ai_image_generation_request'
    _description = "AI Image Generation Request"
    _order = 'create_date desc'

    user_id = fields.Many2one(
        'res.users', string="Requesting User",
        required=True, ondelete='restrict', index=True
    )
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string="Associated Influencer Profile",
        compute='_compute_influencer_profile', store=True, readonly=True, index=True
    )
    campaign_id = fields.Many2one(
        'influence_gen.campaign', string="Associated Campaign",
        ondelete='set null', index=True
    )
    prompt = fields.Text(string="Prompt", required=True)
    negative_prompt = fields.Text(string="Negative Prompt")
    model_id = fields.Many2one(
        'influence_gen.ai_image_model', string="AI Model Used",
        required=True, ondelete='restrict'
    )
    resolution_width = fields.Integer(string="Width (px)")
    resolution_height = fields.Integer(string="Height (px)")
    aspect_ratio = fields.Char(string="Aspect Ratio", help="e.g., '1:1', '16:9'")
    seed = fields.Integer(string="Seed")
    inference_steps = fields.Integer(string="Inference Steps")
    cfg_scale = fields.Float(string="CFG Scale", digits=(3, 1))
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
    generated_image_ids = fields.One2many(
        'influence_gen.generated_image', 'request_id', string="Generated Images"
    )
    # usage_tracking_log_ids: This field is mentioned in the SDS text but not in the field list for this specific model.
    # It seems to be a One2many from UsageTrackingLog to this model, so it would be defined on UsageTrackingLog.
    # If it was intended here it would be:
    # usage_tracking_log_ids = fields.One2many('influence_gen.usage_tracking_log', 'ai_request_id', string="Usage Logs")
    # For now, assuming it's on UsageTrackingLog as 'ai_request_id' Many2one.

    @api.depends('user_id')
    def _compute_influencer_profile(self):
        for request in self:
            if request.user_id:
                profile = self.env['influence_gen.influencer_profile'].search([
                    ('user_id', '=', request.user_id.id)
                ], limit=1)
                request.influencer_profile_id = profile.id
            else:
                request.influencer_profile_id = False

    def action_cancel_request(self):
        """Cancels the AI image generation request if possible."""
        for request in self:
            if request.status not in ('queued', 'processing'):
                raise UserError(_("Only queued or processing requests can be cancelled. Current status: %s", request.status))
            
            # If 'processing', might need to notify N8N to attempt to stop the job
            if request.status == 'processing' and request.n8n_execution_id:
                try:
                    # self.env['influence_gen.infrastructure.integration.services'].cancel_n8n_workflow(request.n8n_execution_id)
                    _logger.info("N8N workflow cancellation attempted for %s (Placeholder)", request.n8n_execution_id)
                except Exception as e:
                    _logger.error("Failed to signal N8N for cancellation of request %s: %s", request.id, e)
                    # Potentially raise UserError if strict cancellation is required or proceed with local cancellation.

            request.write({'status': 'cancelled'})
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='AI_REQUEST_CANCELLED',
                actor_user_id=self.env.user.id,
                action_performed='CANCEL_REQUEST',
                target_object=request
            )
            
            # Revert quota if applicable (handled by AIImageService typically)
            # self.env['influence_gen.ai_image_service'].revert_quota_for_request(request.id)
        return True

    def _log_usage(self, event_type="request_created", details=None):
        """Internal helper to create UsageTrackingLog entries. REQ-AIGS-007."""
        # Assuming UsageTrackingLog model exists and has an 'ai_request_id' field.
        # This method is primarily called by AIImageService.
        # For direct calls from this model (if any), ensure all fields are correctly populated.
        self.ensure_one()
        # Example:
        # self.env['influence_gen.usage_tracking_log'].create({
        #     'user_id': self.user_id.id,
        #     'influencer_profile_id': self.influencer_profile_id.id,
        #     'ai_request_id': self.id,
        #     'event_type': event_type, # e.g., 'ai_generation_initiated', 'ai_generation_completed', 'ai_generation_failed'
        #     'quantity_consumed': 1, # or based on number of images, complexity, etc.
        #     'details': json.dumps(details) if details else None,
        # })
        _logger.info(f"Usage log to be created for AI Request {self.id}, Event: {event_type}. (Actual creation by AIImageService)")
        return True