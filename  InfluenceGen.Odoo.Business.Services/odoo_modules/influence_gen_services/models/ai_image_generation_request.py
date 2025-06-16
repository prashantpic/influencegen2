# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InfluenceGenAiImageGenerationRequest(models.Model):
    _name = 'influence_gen.ai_image_generation_request'
    _description = "AI Image Generation Request"
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one(
        'res.users',
        string="Requesting User",
        required=True,
        ondelete='restrict', # Don't delete request if user is deleted, keep history
        index=True,
        default=lambda self: self.env.user
    )
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Associated Influencer Profile",
        compute='_compute_influencer_profile',
        store=True,
        readonly=True,
        index=True
    )
    campaign_id = fields.Many2one(
        'influence_gen.campaign',
        string="Associated Campaign",
        ondelete='set null', # Keep request if campaign deleted
        index=True
    )
    prompt = fields.Text(string="Prompt", required=True)
    negative_prompt = fields.Text(string="Negative Prompt")
    model_id = fields.Many2one(
        'influence_gen.ai_image_model',
        string="AI Model Used",
        required=True,
        ondelete='restrict', # Don't allow deleting model if requests used it
        domain="[('is_active', '=', True)]"
    )
    resolution_width = fields.Integer(string="Width (px)")
    resolution_height = fields.Integer(string="Height (px)")
    aspect_ratio = fields.Char(string="Aspect Ratio", help="e.g., '1:1', '16:9'") # Store as string, can be computed or set
    seed = fields.Integer(string="Seed")
    inference_steps = fields.Integer(string="Inference Steps")
    cfg_scale = fields.Float(string="CFG Scale", digits=(3,1)) # e.g., 7.5

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
    n8n_execution_id = fields.Char(string="N8N Execution ID", readonly=True, index=True, copy=False)
    
    generated_image_ids = fields.One2many(
        'influence_gen.generated_image',
        'request_id',
        string="Generated Images"
    )
    # This field was defined in SDS, but `_log_usage` method logs to `audit_log_entry`
    # If a separate usage log specific to AI is needed, a new model `influence_gen.usage_tracking_log`
    # would be required. For now, assuming audit log covers usage tracking as per REQ-AIGS-007.
    # usage_tracking_log_ids = fields.One2many('influence_gen.usage_tracking_log', 'ai_request_id', string="Usage Logs")

    @api.depends('user_id')
    def _compute_influencer_profile(self) -> None:
        for request in self:
            if request.user_id:
                # Assuming one influencer profile per user for simplicity here.
                # Adjust if a user can be linked to multiple profiles or no profile.
                profile = self.env['influence_gen.influencer_profile'].search([
                    ('user_id', '=', request.user_id.id)
                ], limit=1)
                request.influencer_profile_id = profile.id
            else:
                request.influencer_profile_id = False

    def action_cancel_request(self) -> None:
        """
        Cancels the AI generation request.
        """
        for record in self:
            if record.status not in ['queued', 'processing']:
                raise UserError(_("Only requests in 'Queued' or 'Processing' status can be cancelled."))
            
            # If 'processing', attempt to notify N8N to cancel (via infra layer)
            if record.status == 'processing' and record.n8n_execution_id:
                # self.env['influence_gen_integration.n8n_service'].cancel_workflow(record.n8n_execution_id)
                pass # Placeholder for infra call

            record.write({'status': 'cancelled'})
            record._log_usage(event_type='AI_REQUEST_CANCELLED', details={'reason': 'User cancelled'})
            
            # Revert quota if it was pre-authorized/decremented. This logic would be in AIImageService.
            # For now, just logging.
            # self.env['influence_gen.services.ai_image_service'](self.env).revert_quota_for_request(record.id)


    def _log_usage(self, event_type: str = "AI_REQUEST_CREATED", details: dict = None) -> None:
        """
        Internal helper to create AuditLogEntry entries for AI usage. REQ-AIGS-007.
        """
        self.ensure_one()
        log_details = {
            'prompt_length': len(self.prompt or ''),
            'model_used': self.model_id.name,
            'status': self.status,
        }
        if self.campaign_id:
            log_details['campaign_id'] = self.campaign_id.id
            log_details['campaign_name'] = self.campaign_id.name
        if details:
            log_details.update(details)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type=event_type, # e.g., 'AI_REQUEST_CREATED', 'AI_GENERATION_SUCCESS', 'AI_GENERATION_FAILED'
            actor_user_id=self.user_id.id,
            action_performed='AI_USAGE_EVENT',
            target_object=self,
            details_dict=log_details,
            outcome='success' if self.status == 'completed' else ('failure' if self.status == 'failed' else None) # Outcome more relevant on completion
        )

    # Note: Methods like validate_prompt_and_params, check_user_quota, decrement_user_quota,
    # and process_generation_result are typically part of the AIImageService as per SDS,
    # not directly on the model, as they orchestrate logic beyond simple model state.
    # This model primarily stores the data and simple state transitions like cancel.
    # The _log_usage is a helper called by the service or upon specific model actions.