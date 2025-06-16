import logging
import json
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class AIImageService:
    """
    Manages AI image generation business logic.
    """

    def __init__(self, env):
        self.env = env

    def _validate_prompt(self, prompt):
        """
        Internal: Validates prompt against content moderation rules.
        REQ-AIGS-003
        """
        moderation_enabled = self.env['influence_gen.platform_setting'].get_param(
            'influence_gen.ai_image_prompt_moderation_enabled', False
        )
        if moderation_enabled:
            # Placeholder for actual moderation logic (e.g., call external API via infra layer)
            # For now, just a basic check
            forbidden_keywords = self.env['influence_gen.platform_setting'].get_param(
                'influence_gen.ai_image_prompt_forbidden_keywords', [] # Expects a list from setting if JSON
            )
            if isinstance(forbidden_keywords, str): # If it's a comma separated string
                forbidden_keywords = [kw.strip() for kw in forbidden_keywords.split(',')]

            if any(keyword.lower() in prompt.lower() for keyword in forbidden_keywords if keyword):
                _logger.warning("Prompt validation failed due to forbidden keyword: %s", prompt)
                raise UserError(_("Your prompt contains restricted content. Please revise."))
        return True


    def _validate_parameters(self, params):
        """
        Internal: Validates generation parameters against platform settings.
        REQ-AIGS-004
        """
        # Example validation for inference_steps
        min_steps, max_steps = 10, 50 # defaults
        range_setting = self.env['influence_gen.platform_setting'].get_param(
            'influence_gen.ai_image_param_range_inference_steps'
        )
        if range_setting:
            try:
                range_dict = json.loads(range_setting) if isinstance(range_setting, str) else range_setting
                min_steps = int(range_dict.get('min', min_steps))
                max_steps = int(range_dict.get('max', max_steps))
            except (json.JSONDecodeError, ValueError) as e:
                _logger.error("Invalid format for 'influence_gen.ai_image_param_range_inference_steps' setting: %s", e)
        
        if 'inference_steps' in params:
            steps = params['inference_steps']
            if not (min_steps <= steps <= max_steps):
                raise UserError(_("Inference steps must be between %s and %s.") % (min_steps, max_steps))
        
        # Add more parameter validations as needed (resolution, cfg_scale, etc.)
        return True


    def get_user_ai_quota_status(self, user_id):
        """
        Gets the user's AI generation quota status.
        REQ-AIGS-002, REQ-AIGS-007
        """
        user = self.env['res.users'].browse(user_id)
        if not user.exists():
            raise UserError(_("User not found."))

        # Default quota from PlatformSetting
        # Assuming monthly quota for simplicity. More complex logic (daily, specific roles) can be added.
        default_quota_monthly = int(self.env['influence_gen.platform_setting'].get_param(
            'influence_gen.ai_image_default_quota_per_user_monthly', 0
        ))

        # Fetch user's usage from UsageTrackingLog (Placeholder - UsageTrackingLog model is not fully defined in SDS models list)
        # For now, we'll simulate this part. Once UsageTrackingLog is defined:
        # today = fields.Date.context_today(self.env.user)
        # start_of_month = today.replace(day=1)
        # usage_count = self.env['influence_gen.usage_tracking_log'].search_count([
        # ('user_id', '=', user.id),
        # ('event_type', '=', 'ai_image_generated_successfully'), # Or count 'request_created' that are not 'failed'
        # ('timestamp', '>=', fields.Datetime.to_string(start_of_month))
        # ])
        # This part requires UsageTrackingLog model to be fully defined.
        # Assuming a placeholder for usage_count for now.
        usage_count_this_period = 0 # Placeholder for actual usage tracking query
        
        # Example: Link to influencer profile for specific quotas, if any
        influencer_profile = self.env['influence_gen.influencer_profile'].search([('user_id', '=', user.id)], limit=1)
        # if influencer_profile and influencer_profile.custom_ai_quota:
        # default_quota_monthly = influencer_profile.custom_ai_quota

        remaining_quota = default_quota_monthly - usage_count_this_period
        
        return {
            'limit': default_quota_monthly,
            'used': usage_count_this_period,
            'remaining': remaining_quota if remaining_quota > 0 else 0
        }

    def prepare_ai_generation_request(self, user_id, prompt, negative_prompt=None, model_id=None, campaign_id=None, intended_use='personal_exploration', **params):
        """
        Prepares and submits an AI image generation request.
        REQ-AIGS-003, REQ-AIGS-004
        `params` can include resolution_width, resolution_height, aspect_ratio, seed, inference_steps, cfg_scale
        """
        _logger.info("Preparing AI generation request for user ID: %s", user_id)
        user = self.env['res.users'].browse(user_id)
        if not user.exists():
            raise UserError(_("Requesting user not found."))
        
        influencer_profile = self.env['influence_gen.influencer_profile'].search([('user_id', '=', user.id)], limit=1)
        if not influencer_profile.exists():
            raise UserError(_("Associated influencer profile not found for user."))
            
        # 1. Validate prompt
        self._validate_prompt(prompt)

        # 2. Validate params
        self._validate_parameters(params)
        
        # 3. Check user's AI generation quota
        quota_status = self.get_user_ai_quota_status(user.id)
        if quota_status['remaining'] <= 0:
            raise UserError(_("You have reached your AI image generation quota for this period."))

        # Determine AI Model
        ai_model = None
        if model_id:
            ai_model = self.env['influence_gen.ai_image_model'].browse(model_id)
            if not ai_model.exists() or not ai_model.is_active:
                raise UserError(_("Specified AI Model is not valid or not active."))
        else:
            # Select a default active model if none specified
            ai_model = self.env['influence_gen.ai_image_model'].search([('is_active', '=', True)], limit=1, order='id asc') # Simplistic default
            if not ai_model:
                 raise UserError(_("No active AI Models are configured. Please contact support."))
        
        # Default parameters from platform settings if not provided
        default_resolution_str = self.env['influence_gen.platform_setting'].get_param('influence_gen.ai_image_param_default_resolution', '1024x1024')
        try:
            default_w_str, default_h_str = default_resolution_str.split('x')
            default_w, default_h = int(default_w_str), int(default_h_str)
        except ValueError:
            default_w, default_h = 1024, 1024
            _logger.warning("Invalid default resolution format '%s', using 1024x1024.", default_resolution_str)


        request_vals = {
            'user_id': user.id,
            # 'influencer_profile_id': influencer_profile.id, # Computed field
            'campaign_id': campaign_id or False,
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'model_id': ai_model.id,
            'resolution_width': params.get('resolution_width', default_w),
            'resolution_height': params.get('resolution_height', default_h),
            'aspect_ratio': params.get('aspect_ratio', f"{params.get('resolution_width', default_w)}:{params.get('resolution_height', default_h)}"), # TODO: Calculate or get from params
            'seed': params.get('seed'),
            'inference_steps': params.get('inference_steps', 25), # Default value
            'cfg_scale': params.get('cfg_scale', 7.0), # Default value
            'status': 'queued',
            'intended_use': intended_use,
        }
        
        # 4. Create AIImageGenerationRequest record
        request_record = self.env['influence_gen.ai_image_generation_request'].create(request_vals)
        _logger.info("AI Image Generation Request ID: %s created.", request_record.id)

        # 5. Decrement user quota (or pre-authorize) - Actual decrement might happen on success
        # For now, let's assume quota is checked, actual decrement/logging on success/failure in callback.
        # Alternatively, log a "quota_reserved" entry.

        # 6. Log UsageTrackingLog for request initiation
        # request_record._log_usage(event_type="ai_request_created_quota_checked") # Assuming UsageTrackingLog model exists and has this method

        # 7. Trigger webhook to N8N
        n8n_payload = {
            'request_id': request_record.id,
            'prompt': request_record.prompt,
            'negative_prompt': request_record.negative_prompt,
            'model_external_id': ai_model.external_model_id or ai_model.name, # N8N needs an identifier for the model
            'width': request_record.resolution_width,
            'height': request_record.resolution_height,
            'seed': request_record.seed,
            'inference_steps': request_record.inference_steps,
            'cfg_scale': request_record.cfg_scale,
            # Add other necessary parameters for N8N
        }
        try:
            # Assume infra service has a method like trigger_n8n_ai_image_generation
            n8n_response = self.env['influence_gen.infrastructure.integration.services'].trigger_webhook(
                webhook_name='n8n_ai_image_generation_start', # Configurable name
                payload=n8n_payload
            )
            # Store N8N initial execution ID if returned synchronously
            if n8n_response and n8n_response.get('n8n_execution_id'):
                request_record.write({'n8n_execution_id': n8n_response.get('n8n_execution_id'), 'status': 'processing'})
            else:
                # If N8N call is async and doesn't return ID immediately, status might remain 'queued'
                # or N8N updates it to 'processing' via another callback.
                # For now, assume it might update to 'processing' if call is accepted.
                request_record.write({'status': 'processing'})


        except Exception as e:
            _logger.error("Failed to trigger N8N for AI request %s: %s", request_record.id, e)
            request_record.write({'status': 'failed', 'error_details': _("Failed to initiate generation process: %s") % e})
            # Revert quota if it was pre-authorized/decremented here
            # request_record._log_usage(event_type="ai_request_failed_n8n_trigger", details={"error": str(e)})
            raise UserError(_("Could not start image generation process. Please try again later."))

        # 8. Log audit
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='AI_IMAGE_REQUEST_CREATED',
            actor_user_id=user.id,
            action_performed='CREATE',
            target_object=request_record,
            details_dict={'prompt': prompt, 'model_id': ai_model.id}
        )
        return request_record

    def process_ai_generation_callback(self, request_id, image_binary_data_or_url, n8n_execution_id, success=True, error_details=None):
        """
        Processes the callback from N8N after AI image generation.
        REQ-AIGS-006, REQ-AIGS-010
        image_binary_data_or_url: if URL, infra layer should download it.
                                  Here, we assume if it's a URL, it's passed for `ir.attachment` `url` field
                                  or if binary, it's base64 `datas`.
        """
        _logger.info("Processing AI generation callback for request ID: %s, Success: %s", request_id, success)
        request_record = self.env['influence_gen.ai_image_generation_request'].browse(request_id)
        if not request_record.exists():
            _logger.error("AI Generation Request ID %s not found for callback.", request_id)
            # This is an orphaned callback, difficult to raise UserError
            return False # Or raise specific system error

        request_record.write({'n8n_execution_id': n8n_execution_id}) # Update with final/specific execution ID

        if success:
            if not image_binary_data_or_url:
                request_record.write({
                    'status': 'failed',
                    'error_details': _("Generation successful but no image data received.")
                })
                # request_record._log_usage(event_type="ai_request_failed_no_image_data")
                return False

            attachment_vals = {
                'name': f"ai_gen_{request_record.id}_{fields.Datetime.now().strftime('%Y%m%d%H%M%S')}.png", # Default name
                'res_model': 'influence_gen.generated_image', # Will be linked later
                'access_token': self.env['ir.attachment']._generate_access_token(),
            }
            image_binary_data = None

            if isinstance(image_binary_data_or_url, str) and image_binary_data_or_url.startswith(('http://', 'https://')):
                # If it's a URL, infra layer should download it.
                # Here, we'll assume the infra layer is called or the ir.attachment can handle it.
                # For simplicity, we assume if URL, it's downloadable by ir.attachment if `url` field is supported for creation
                # Odoo's ir.attachment typically expects 'datas' (base64) or a local 'path'.
                # Let's assume the infra layer is responsible for converting URL to base64 `datas`.
                # If this service receives a URL, it should ideally call an infra service to fetch and encode.
                # Placeholder:
                _logger.info("Received image URL: %s. Assuming infra layer handles download to base64.", image_binary_data_or_url)
                # For this example, if it's a URL, we can't directly create attachment with it using 'datas'
                # This needs clarification or an infra service call.
                # Assuming `image_binary_data_or_url` is ALREADY base64 encoded binary data string if not a URL.
                # For this example, let's assume it's base64 encoded 'datas'
                attachment_vals['datas'] = image_binary_data_or_url # if it's already base64
                image_binary_data = image_binary_data_or_url # For hash calculation if it's base64
            else: # Assuming it's already base64 binary data
                attachment_vals['datas'] = image_binary_data_or_url
                image_binary_data = image_binary_data_or_url


            try:
                attachment = self.env['ir.attachment'].create(attachment_vals)
                
                # Call GeneratedImage.create_from_generation
                generated_image = self.env['influence_gen.generated_image'].create_from_generation(
                    request_id=request_record.id,
                    attachment_id=attachment.id,
                    image_binary_data=image_binary_data # Pass the base64 data for hashing
                )
                attachment.write({'res_id': generated_image.id}) # Link attachment to the generated image record

                request_record.write({'status': 'completed'})
                # request_record._log_usage(event_type="ai_image_generated_successfully") # Placeholder
                _logger.info("Generated image ID %s created for request %s.", generated_image.id, request_record.id)

                # Trigger UI update/notification to user
                try:
                    self.env['influence_gen.infrastructure.integration.services'].send_notification(
                        recipient_user_ids=[request_record.user_id.id],
                        template_name='ai_image_generation_completed',
                        context={
                            'request_prompt': request_record.prompt,
                            'image_url': generated_image.storage_attachment_id.local_url # or public_url
                        }
                    )
                except Exception as e:
                    _logger.error("Failed to send AI generation completion notification for req %s: %s", request_record.id, e)

                self.env['influence_gen.audit_log_entry'].create_log(
                    event_type='AI_IMAGE_GENERATION_COMPLETED',
                    actor_user_id=request_record.user_id.id, # Or system if N8N is actor
                    action_performed='UPDATE', # Update of request status, creation of image
                    target_object=request_record,
                    details_dict={'generated_image_id': generated_image.id}
                )
                return generated_image

            except Exception as e:
                _logger.error("Error processing successful AI generation callback for request %s: %s", request_id, e)
                request_record.write({'status': 'failed', 'error_details': _("Error storing generated image: %s") % e})
                # request_record._log_usage(event_type="ai_request_failed_storage_error", details={"error": str(e)})
                return False
        else:
            request_record.write({
                'status': 'failed',
                'error_details': error_details or _("Generation failed due to an unknown error.")
            })
            # Revert quota decrement if applicable
            # request_record._log_usage(event_type="ai_request_failed_external", details={"error": error_details})
            _logger.warning("AI generation failed for request %s: %s", request_id, error_details)
            
            try:
                self.env['influence_gen.infrastructure.integration.services'].send_notification(
                    recipient_user_ids=[request_record.user_id.id],
                    template_name='ai_image_generation_failed',
                    context={'request_prompt': request_record.prompt, 'error_details': error_details}
                )
            except Exception as e:
                _logger.error("Failed to send AI generation failure notification for req %s: %s", request_record.id, e)

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='AI_IMAGE_GENERATION_FAILED',
                actor_user_id=request_record.user_id.id, # Or system
                action_performed='UPDATE',
                target_object=request_record,
                details_dict={'error': error_details},
                outcome='failure',
                failure_reason=error_details
            )
            return False


    def manage_ai_model_configurations(self, action, model_data=None, model_id=None):
        """
        Manages AI Model configurations (CRUD operations).
        REQ-AIGS-004
        action: 'create', 'update', 'archive' (instead of deactivate for Odoo context)
        model_data: dict of values for create/update
        model_id: ID for update/archive
        """
        _logger.info("Managing AI Model config: Action: %s, Model ID: %s", action, model_id)
        AuditLog = self.env['influence_gen.audit_log_entry']
        actor_user_id = self.env.user.id
        
        if action == 'create':
            if not model_data or not model_data.get('name'):
                raise UserError(_("Model name is required for creation."))
            try:
                model = self.env['influence_gen.ai_image_model'].create(model_data)
                AuditLog.create_log('AI_MODEL_CONFIG_CREATED', actor_user_id, 'CREATE', model, model_data)
                return model
            except Exception as e:
                _logger.error("Error creating AI Model: %s", e)
                raise UserError(_("Could not create AI Model: %s") % e)
        
        elif action in ['update', 'archive', 'activate']:
            if not model_id:
                raise UserError(_("Model ID is required for %s action.") % action)
            model = self.env['influence_gen.ai_image_model'].browse(model_id)
            if not model.exists():
                raise UserError(_("AI Model not found."))

            if action == 'update':
                if not model_data:
                    raise UserError(_("No data provided for update."))
                try:
                    model.write(model_data)
                    AuditLog.create_log('AI_MODEL_CONFIG_UPDATED', actor_user_id, 'WRITE', model, model_data)
                    return model
                except Exception as e:
                    _logger.error("Error updating AI Model %s: %s", model_id, e)
                    raise UserError(_("Could not update AI Model: %s") % e)
            
            elif action == 'archive': # Deactivate by archiving
                try:
                    model.write({'is_active': False})
                    AuditLog.create_log('AI_MODEL_CONFIG_ARCHIVED', actor_user_id, 'WRITE', model, {'is_active': False})
                    return True
                except Exception as e:
                    _logger.error("Error archiving AI Model %s: %s", model_id, e)
                    raise UserError(_("Could not archive AI Model: %s") % e)
            elif action == 'activate':
                try:
                    model.write({'is_active': True})
                    AuditLog.create_log('AI_MODEL_CONFIG_ACTIVATED', actor_user_id, 'WRITE', model, {'is_active': True})
                    return True
                except Exception as e:
                    _logger.error("Error activating AI Model %s: %s", model_id, e)
                    raise UserError(_("Could not activate AI Model: %s") % e)
        else:
            raise UserError(_("Unsupported action for AI Model management: %s") % action)