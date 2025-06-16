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
        ondelete='restrict', # Keep request even if user is deleted (or cascade if preferred)
        index=True
    )
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Associated Influencer Profile",
        compute='_compute_influencer_profile',
        store=True,
        readonly=True, # Should be readonly if computed and stored correctly
        index=True
    )
    campaign_id = fields.Many2one(
        'influence_gen.campaign',
        string="Associated Campaign",
        ondelete='set null', # Request can exist without campaign
        index=True
    )
    prompt = fields.Text(string="Prompt", required=True)
    negative_prompt = fields.Text(string="Negative Prompt")
    model_id = fields.Many2one(
        'influence_gen.ai_image_model',
        string="AI Model Used",
        required=True,
        ondelete='restrict' # Don't delete request if model is deleted
    )
    resolution_width = fields.Integer(string="Width (px)")
    resolution_height = fields.Integer(string="Height (px)")
    aspect_ratio = fields.Char(string="Aspect Ratio", help="e.g., '1:1', '16:9'")
    seed = fields.Integer(string="Seed")
    inference_steps = fields.Integer(string="Inference Steps")
    cfg_scale = fields.Float(string="CFG Scale", digits=(3, 1)) # Precision 3, Scale 1
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
    # The SDS shows 'influence_gen.usage_tracking_log' but this model is not defined in the files to be generated.
    # For now, I will comment it out. If the model is added later, this can be uncommented.
    # usage_tracking_log_ids = fields.One2many(
    #     'influence_gen.usage_tracking_log', # This model is not in the provided file list
    #     'ai_request_id',
    #     string="Usage Logs"
    # )

    @api.depends('user_id')
    def _compute_influencer_profile(self):
        for record in self:
            if record.user_id:
                # Assuming one user is linked to one influencer profile
                profile = self.env['influence_gen.influencer_profile'].search([
                    ('user_id', '=', record.user_id.id)
                ], limit=1)
                record.influencer_profile_id = profile.id
            else:
                record.influencer_profile_id = False

    def action_cancel_request(self):
        """Cancels the AI image generation request if possible."""
        # For N8N integration, cancelling might involve an API call to N8N if processing started
        for record in self:
            if record.status in ['queued', 'processing']: # Check if N8N allows cancellation of 'processing'
                old_status = record.status
                record.status = 'cancelled'
                self.env['influence_gen.audit_log_entry'].create_log(
                    event_type='AI_REQUEST_CANCELLED',
                    actor_user_id=self.env.user.id,
                    action_performed='UPDATE',
                    target_object=record,
                    details_dict={'old_status': old_status}
                )
                # Potentially notify N8N if processing (via infra layer)
                # infra_service = self.env['influence_gen.infrastructure.n8n_service']
                # if old_status == 'processing' and hasattr(infra_service, 'cancel_n8n_workflow'):
                #     infra_service.cancel_n8n_workflow(record.n8n_execution_id)

                # Revert quota if applicable (handled by AIImageService typically)
            elif record.status in ['completed', 'failed', 'cancelled']:
                raise UserError(_("Cannot cancel a request that is already '%s'.") % record.status)
        return True

    def _log_usage(self, event_type="request_created", details=None):
        """Internal helper to create UsageTrackingLog entries. REQ-AIGS-007."""
        # This method relies on 'influence_gen.usage_tracking_log' which is not in the list of files to generate.
        # If UsageTrackingLog model is added, this can be implemented.
        # For now, this will be a placeholder or call audit log if it's a substitute.
        
        # Example if UsageTrackingLog existed:
        # for record in self:
        #     log_vals = {
        #         'user_id': record.user_id.id,
        #         'influencer_profile_id': record.influencer_profile_id.id,
        #         'ai_request_id': record.id,
        #         'event_type': event_type,
        #         'details_json': json.dumps(details) if details else None,
        #         # Add other relevant fields like quota_consumed, timestamp etc.
        #     }
        #     self.env['influence_gen.usage_tracking_log'].create(log_vals)
        
        # Fallback to audit log if usage log is not present (less ideal for specific quota tracking)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type=f'AI_USAGE_EVENT_{event_type.upper()}',
            actor_user_id=self.user_id.id,
            action_performed='USAGE_LOG', # Custom action type
            target_object=self,
            details_dict=details
        )
        return True