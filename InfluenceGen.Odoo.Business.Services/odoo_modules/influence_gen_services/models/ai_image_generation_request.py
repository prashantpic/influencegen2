from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
import json

_logger = logging.getLogger(__name__)

class AiImageGenerationRequest(models.Model):
    """
    Represents a single request made by a user to generate an AI image.
    This model records all parameters of the request, tracks its status through
    the generation pipeline (including interaction with N8N), and links to
    the resulting generated images. It also plays a role in quota enforcement.
    """
    _name = 'influence_gen.ai_image_generation_request'
    _description = 'AI Image Generation Request'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'influence_gen.base_audit_mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string="Request Name", compute='_compute_name', store=True, help="Computed name for easy identification.")
    user_id = fields.Many2one(
        'res.users',
        string='Requested By User',
        required=True,
        ondelete='restrict',
        index=True,
        tracking=True,
        default=lambda self: self.env.user,
        help="The Odoo user who initiated this AI image generation request."
    )
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string='Influencer Profile',
        required=True, # Assuming requests are always tied to an influencer profile
        ondelete='cascade',
        index=True,
        tracking=True,
        help="The influencer profile associated with this request (for quota, context)."
    )
    campaign_id = fields.Many2one(
        'influence_gen.campaign',
        string='Campaign',
        ondelete='set null',
        index=True,
        tracking=True,
        help="Optional campaign this image generation request is associated with."
    )
    prompt = fields.Text(
        string='Prompt',
        required=True,
        tracking=True,
        help="The main text prompt used for image generation."
    )
    negative_prompt = fields.Text(
        string='Negative Prompt',
        tracking=True,
        help="Text prompt describing what to avoid in the image."
    )
    model_id = fields.Many2one(
        'influence_gen.ai_image_model',
        string='AI Model Used',
        required=True,
        ondelete='restrict', # Prevent deleting a model if it's been used
        tracking=True,
        help="The specific AI image generation model selected for this request."
    )
    resolution = fields.Char(
        string='Resolution',
        default='1024x1024',
        tracking=True,
        help="Requested image resolution, e.g., '512x512', '1024x1024'."
    )
    aspect_ratio = fields.Char(
        string='Aspect Ratio',
        default='1:1',
        tracking=True,
        help="Requested aspect ratio, e.g., '1:1', '16:9', '4:3'."
    )
    seed = fields.Integer(
        string='Seed',
        tracking=True,
        help="Seed value for reproducibility. 0 or -1 usually means random."
    )
    inference_steps = fields.Integer(
        string='Inference Steps',
        default=30,
        tracking=True,
        help="Number of inference steps for the generation process."
    )
    cfg_scale = fields.Float(
        string='CFG Scale',
        default=7.0,
        tracking=True,
        help="Classifier-Free Guidance scale, controlling prompt adherence."
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('queued', 'Queued'),
        ('processing_validation', 'Processing (Validation)'),
        ('processing_n8n', 'Processing (N8N Workflow)'),
        ('processing_ai', 'Processing (AI Generation)'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True, tracking=True, index=True, copy=False,
       help="Current status of the AI image generation request.")
    intended_use = fields.Selection([
        ('personal', 'Personal Use'),
        ('campaign_content', 'Campaign Content'),
        ('platform_asset', 'Platform Asset'),
        ('other', 'Other')
    ], string='Intended Use', default='personal', required=True, tracking=True,
       help="The intended use of the generated image(s), affects retention policies.")
    error_details = fields.Text(
        string='Error Details',
        readonly=True,
        tracking=True,
        copy=False,
        help="Details of any error that occurred during processing."
    )
    n8n_execution_id = fields.Char(
        string='N8N Execution ID',
        readonly=True,
        copy=False,
        tracking=True,
        index=True,
        help="Identifier for the corresponding N8N workflow execution."
    )
    generated_image_ids = fields.One2many(
        'influence_gen.generated_image',
        'request_id',
        string='Generated Images',
        readonly=True,
        copy=False,
        help="Images generated as a result of this request."
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        readonly=True
    )
    num_images_requested = fields.Integer(
        string='Number of Images Requested', 
        default=1, 
        tracking=True,
        help="How many images are expected from this request."
    )


    @api.depends('prompt', 'create_date')
    def _compute_name(self):
        for record in self:
            ts = fields.Datetime.to_string(record.create_date) if record.create_date else 'NoDate'
            prompt_snip = (record.prompt[:30] + '...') if record.prompt and len(record.prompt) > 30 else record.prompt
            record.name = f"AI Request ({prompt_snip}) - {ts}"

    @api.constrains('prompt')
    def _validate_prompt_initial(self):
        """ REQ-AIGS-003: Basic prompt validation (e.g., not empty) """
        for record in self:
            if not record.prompt or not record.prompt.strip():
                raise ValidationError(_("The prompt cannot be empty."))
            # More complex validation (content moderation) handled by service before submission

    def _check_quota(self):
        """
        Checks if the user has enough AI generation quota.
        This is a placeholder; actual call to service.
        REQ-AIGS-002: Enforce AI image generation quotas
        Returns: True if quota available, False otherwise.
        """
        self.ensure_one()
        # This should ideally call the AiIntegrationService
        # For now, simulate a call or assume service handles it before `action_submit_to_n8n`
        has_quota, reason = self.env['influence_gen.services.ai_integration'].check_user_ai_quota(self.influencer_profile_id.id, images_to_generate=self.num_images_requested)
        if not has_quota:
            self.error_details = reason or _("Quota exceeded or unavailable.")
            self.status = 'failed' # Or a specific status like 'quota_exceeded'
            self.message_post(body=_("Quota check failed: %s") % self.error_details)
            return False
        return True

    def action_submit_request(self):
        """
        Validates the request, checks quota, and submits it to the AI Integration Service.
        REQ-AIGS-001: Initiate AI Image Generation
        """
        for record in self:
            if record.status != 'draft':
                raise UserError(_("Only draft requests can be submitted."))

            record.status = 'processing_validation'
            
            # 1. Validate prompt (more advanced validation)
            is_valid, reason = self.env['influence_gen.services.ai_integration'].validate_ai_prompt(record.prompt)
            if not is_valid:
                record.write({
                    'status': 'failed',
                    'error_details': _("Prompt validation failed: %s") % reason
                })
                record.message_post(body=_("Prompt validation failed: %s") % reason)
                continue # next record

            # 2. Check quota
            if not record._check_quota(): # _check_quota already updates status and posts message if failed
                continue # next record

            # 3. Initiate generation via service
            try:
                # REQ-AIGS-004: Select AI model and parameters (already set on record)
                # The service will create AiImageGenerationRequest if not done from UI first
                # Here, we assume the record exists and is being processed.
                # The service might update this record with N8N execution ID etc.
                self.env['influence_gen.services.ai_integration'].initiate_ai_image_generation(
                    user_id=record.user_id.id,
                    influencer_profile_id=record.influencer_profile_id.id,
                    request_id=record.id, # Pass existing request ID
                    prompt_data={'prompt': record.prompt, 'negative_prompt': record.negative_prompt},
                    generation_params={
                        'model_id': record.model_id.id,
                        'model_external_id': record.model_id.external_model_id,
                        'resolution': record.resolution,
                        'aspect_ratio': record.aspect_ratio,
                        'seed': record.seed,
                        'inference_steps': record.inference_steps,
                        'cfg_scale': record.cfg_scale,
                        'num_images': record.num_images_requested,
                    },
                    campaign_id=record.campaign_id.id if record.campaign_id else None,
                    intended_use=record.intended_use
                )
                # Service should update status to 'queued' or 'processing_n8n'
                # For safety, if service doesn't throw error, assume it's at least queued.
                if record.status == 'processing_validation': # If service didn't update status
                    record.status = 'queued' 
                record.message_post(body=_("Request submitted for AI image generation."))
                _logger.info(f"AI Image Generation Request ID {record.id} submitted by user ID {record.user_id.id}.")
            except Exception as e:
                _logger.error(f"Failed to submit AI Image Generation Request ID {record.id}: {e}")
                record.write({
                    'status': 'failed',
                    'error_details': str(e)
                })
                record.message_post(body=_("Failed to submit request: %s") % str(e))
        return True

    def action_cancel_request(self):
        """Cancels a queued or processing request if possible."""
        for record in self:
            if record.status not in ['draft', 'queued', 'processing_validation']: # Add other cancellable states
                raise UserError(_("This request cannot be cancelled in its current state: %s.") % record.status)
            
            # Potentially call a service method to attempt cancellation in N8N if already sent
            # For now, just mark as cancelled
            record.write({
                'status': 'cancelled',
                'error_details': _("Request cancelled by user %s.") % self.env.user.name
            })
            record.message_post(body=_("AI image generation request cancelled."))
            _logger.info(f"AI Image Generation Request ID {record.id} cancelled by user ID {self.env.user.id}.")
        return True

    def process_n8n_callback_success(self, image_data_list, n8n_execution_id_cb):
        """
        Processes a successful callback from N8N. Called by AiIntegrationService.
        REQ-AIGS-001, REQ-AIGS-006, REQ-AIGS-010
        """
        self.ensure_one()
        if self.status not in ['processing_n8n', 'processing_ai']: # Should be in one of these states
             _logger.warning(f"Received N8N success callback for request {self.id} but status is {self.status}. Ignoring.")
             # Potentially raise an error or handle differently
             return

        generated_images_vals = []
        for img_data in image_data_list:
            # Assuming img_data is a dict with keys like 'storage_url', 'file_format', 'file_size', 'width', 'height', 'hash_value'
            # and 'attachment_id' if attachment was created by adapter/service
            img_vals = {
                'request_id': self.id,
                'storage_url': img_data.get('storage_url'),
                'image_attachment_id': img_data.get('attachment_id'), # Link to ir.attachment
                'file_format': img_data.get('file_format'),
                'file_size': img_data.get('file_size'),
                'width': img_data.get('width'),
                'height': img_data.get('height'),
                'hash_value': img_data.get('hash_value'),
                'retention_category': self.env['influence_gen.services.ai_integration'].determine_retention_category(self), # REQ-AIGS-010
                'usage_rights': self.campaign_id.usage_rights if self.campaign_id else _("As per platform policy for %s use.") % self.intended_use,
                'is_campaign_asset': self.intended_use == 'campaign_content',
            }
            generated_images_vals.append((0, 0, img_vals))

        self.write({
            'status': 'completed',
            'generated_image_ids': generated_images_vals,
            'error_details': False, # Clear previous errors
            'n8n_execution_id': self.n8n_execution_id or n8n_execution_id_cb # Update if it was missing
        })
        self.message_post(body=_("AI image generation completed successfully. %s image(s) generated.") % len(image_data_list))
        _logger.info(f"AI Image Generation Request ID {self.id} completed. {len(image_data_list)} images processed.")

        # REQ-AIGS-002: Decrement quota (handled by service after successful generation)
        # REQ-AIGS-007: Log AI usage (handled by service)
        # Service will call these based on the successful processing of this callback.

    def process_n8n_callback_failure(self, error_message, n8n_execution_id_cb):
        """
        Processes a failure callback from N8N. Called by AiIntegrationService.
        REQ-AIGS-001
        """
        self.ensure_one()
        # Even if status is already 'failed', update with potentially more specific N8N error
        self.write({
            'status': 'failed',
            'error_details': error_message,
            'n8n_execution_id': self.n8n_execution_id or n8n_execution_id_cb
        })
        self.message_post(body=_("AI image generation failed. Details: %s") % error_message)
        _logger.error(f"AI Image Generation Request ID {self.id} failed. Error: {error_message}")
        # Send notification of failure (REQ-AIGS-001 implies notification on failure)
        # This could be handled by AiIntegrationService or a mail template triggered here.

    @api.model
    def create(self, vals):
        # REQ-DMG-007: Record AI Image Request
        # REQ-AIGS-012: Audit trail (handled by BaseAuditMixin)
        if 'influencer_profile_id' not in vals and 'user_id' in vals:
            user = self.env['res.users'].browse(vals['user_id'])
            influencer_profile = self.env['influence_gen.influencer_profile'].search([('user_id', '=', user.id)], limit=1)
            if influencer_profile:
                vals['influencer_profile_id'] = influencer_profile.id
            else:
                raise UserError(_("Cannot create AI request: No influencer profile found for user %s.") % user.name)
        
        if 'influencer_profile_id' in vals and not vals.get('user_id'):
            influencer = self.env['influence_gen.influencer_profile'].browse(vals['influencer_profile_id'])
            if influencer.user_id:
                 vals['user_id'] = influencer.user_id.id
            else:
                # This case should ideally not happen if influencer always has a user_id
                _logger.warning(f"AI Request for influencer {influencer.id} has no linked user_id.")


        return super(AiImageGenerationRequest, self).create(vals)

    def write(self, vals):
        # REQ-AIGS-012: Audit trail (handled by BaseAuditMixin)
        return super(AiImageGenerationRequest, self).write(vals)