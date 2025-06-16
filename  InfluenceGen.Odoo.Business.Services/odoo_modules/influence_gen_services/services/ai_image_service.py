# -*- coding: utf-8 -*-
import logging
import json
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class AIImageService(models.AbstractModel):
    _name = 'influence_gen.ai.image.service'
    _description = 'InfluenceGen AI Image Service'

    def __init__(self, env):
        super(AIImageService, self).__init__(env)
        self.env = env

    def prepare_ai_generation_request(self, user_id, prompt, negative_prompt=None, model_id=None, 
                                      campaign_id=None, intended_use='personal_exploration', **params):
        """
        Prepares and initiates an AI image generation request.
        REQ-AIGS-003, REQ-AIGS-004.
        :param user_id: ID of res.users requesting
        :param prompt: string, the main prompt
        :param negative_prompt: string, optional negative prompt
        :param model_id: ID of influence_gen.ai_image_model
        :param campaign_id: ID of influence_gen.campaign, optional
        :param intended_use: string, 'personal_exploration' or 'campaign_specific'
        :param params: dict, other AI parameters (resolution_width, resolution_height, aspect_ratio, seed, inference_steps, cfg_scale)
        :return: influence_gen.ai_image_generation_request record or raises UserError
        """
        user = self.env['res.users'].browse(user_id)
        if not user.exists():
            raise UserError(f"User with ID {user_id} not found.")

        influencer_profile = self.env['influence_gen.influencer_profile'].search([('user_id', '=', user.id)], limit=1)
        if not influencer_profile.exists():
            raise UserError(f"Influencer profile not found for user {user.name}.")
        
        if not prompt:
            raise UserError("Prompt is required for AI image generation.")

        # REQ-AIGS-003: Prompt Content Moderation (simplified example)
        prompt_moderation_enabled = self.env['influence_gen.platform_setting'].get_param('influence_gen.ai_image_prompt_moderation_enabled', False)
        if prompt_moderation_enabled:
            # This would typically call an external service or a more complex internal check
            # For simplicity, let's assume a basic keyword check from PlatformSetting
            forbidden_keywords_json = self.env['influence_gen.platform_setting'].get_param('influence_gen.ai_image_forbidden_keywords_json', '[]')
            try:
                forbidden_keywords = json.loads(forbidden_keywords_json)
                if any(keyword.lower() in prompt.lower() for keyword in forbidden_keywords):
                    raise UserError("Your prompt contains restricted content. Please revise.")
            except json.JSONDecodeError:
                _logger.error("Invalid JSON for forbidden_keywords platform setting.")


        # REQ-AIGS-004: Validate parameters against PlatformSetting defaults/ranges
        # Example for inference_steps
        steps_range_json = self.env['influence_gen.platform_setting'].get_param('influence_gen.ai_image_param_range_inference_steps', '{"min": 10, "max": 50}')
        try:
            steps_range = json.loads(steps_range_json)
            inference_steps = params.get('inference_steps', steps_range.get('default', 20)) # Get default if not provided
            if not (steps_range.get('min', 0) <= inference_steps <= steps_range.get('max', 100)):
                 raise UserError(f"Inference steps must be between {steps_range.get('min',0)} and {steps_range.get('max',100)}.")
            params['inference_steps'] = inference_steps # Ensure it's in params
        except json.JSONDecodeError:
            _logger.error("Invalid JSON for inference_steps range platform setting.")
            params.setdefault('inference_steps', 20) # Fallback default
        
        # Similar validation for resolution, cfg_scale etc.
        # For resolution, width and height might come from 'resolution' string or width/height params
        default_resolution_str = self.env['influence_gen.platform_setting'].get_param('influence_gen.ai_image_param_default_resolution', "1024x1024")
        if 'resolution_width' not in params or 'resolution_height' not in params:
            try:
                width_str, height_str = default_resolution_str.split('x')
                params.setdefault('resolution_width', int(width_str))
                params.setdefault('resolution_height', int(height_str))
            except ValueError:
                 _logger.error(f"Invalid default resolution format: {default_resolution_str}")
                 params.setdefault('resolution_width', 1024)
                 params.setdefault('resolution_height', 1024)


        # REQ-AIGS-002: Check user's AI generation quota
        quota_status = self.get_user_ai_quota_status(user.id)
        if quota_status.get('remaining', 0) <= 0:
            raise UserError("You have exceeded your AI image generation quota for this period.")

        if not model_id:
            # Select a default active model or raise error
            default_model = self.env['influence_gen.ai_image_model'].search([('is_active', '=', True)], limit=1, order='id asc') # Simplistic default
            if not default_model:
                raise UserError("No active AI models configured. Please contact administrator.")
            model_id = default_model.id
        else:
            chosen_model = self.env['influence_gen.ai_image_model'].browse(model_id)
            if not chosen_model.exists() or not chosen_model.is_active:
                raise UserError("The selected AI model is not available or not active.")


        request_vals = {
            'user_id': user.id,
            'influencer_profile_id': influencer_profile.id, # Computed field will also set this
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'model_id': model_id,
            'campaign_id': campaign_id if campaign_id else False,
            'intended_use': intended_use,
            'resolution_width': params.get('resolution_width'),
            'resolution_height': params.get('resolution_height'),
            'aspect_ratio': params.get('aspect_ratio'), # This should ideally be calculated or validated against width/height
            'seed': params.get('seed'),
            'inference_steps': params.get('inference_steps'),
            'cfg_scale': params.get('cfg_scale'),
            'status': 'queued',
        }

        ai_request = self.env['influence_gen.ai_image_generation_request'].create(request_vals)

        # REQ-AIGS-007: Decrement user quota (or pre-authorize) - simplified log for now
        # Actual decrement might happen upon successful generation or be more complex (e.g. credits)
        # For now, we log usage for quota tracking.
        ai_request._log_usage(event_type="request_created", details={'prompt': prompt, 'model_id': model_id})
        
        # Trigger webhook to N8N via Infrastructure Integration Service
        payload_to_n8n = {
            'request_id': ai_request.id,
            'prompt': ai_request.prompt,
            'negative_prompt': ai_request.negative_prompt,
            'model_external_id': ai_request.model_id.external_model_id, # Or other model identifier N8N needs
            'width': ai_request.resolution_width,
            'height': ai_request.resolution_height,
            'seed': ai_request.seed,
            'inference_steps': ai_request.inference_steps,
            'cfg_scale': ai_request.cfg_scale,
            # Add other N8N specific parameters
        }
        try:
            n8n_response = self.env['influence_gen.infrastructure.integration.service'].trigger_n8n_webhook_image_generation(payload_to_n8n)
            # Store N8N execution ID if returned immediately, or update later via callback
            if n8n_response and n8n_response.get('n8n_execution_id'):
                ai_request.write({'n8n_execution_id': n8n_response.get('n8n_execution_id')})
            ai_request.write({'status': 'processing'}) # Assume N8N acknowledged
        except Exception as e:
            _logger.error(f"Failed to trigger N8N webhook for AI request {ai_request.id}: {e}")
            ai_request.write({'status': 'failed', 'error_details': f"N8N trigger failed: {str(e)}"})
            # Revert quota if applicable / log failure appropriately
            ai_request._log_usage(event_type="request_failed_n8n_trigger", details={'error': str(e)})
            raise UserError(f"Could not submit AI generation request to processing queue: {e}")

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='AI_IMAGE_REQUEST_CREATED',
            actor_user_id=user.id,
            action_performed='CREATE',
            target_object=ai_request,
            details_dict=request_vals
        )
        return ai_request

    def process_ai_generation_callback(self, request_id, image_binary_data_or_url, n8n_execution_id, success=True, error_details=None):
        """
        Processes the callback from N8N after AI image generation.
        REQ-AIGS-006, REQ-AIGS-010.
        :param request_id: ID of influence_gen.ai_image_generation_request
        :param image_binary_data_or_url: base64 binary data of the image or a URL to it
        :param n8n_execution_id: string, N8N's execution ID for tracing
        :param success: boolean, True if generation succeeded
        :param error_details: string, error message if generation failed
        :return: influence_gen.generated_image record if successful, or updates request status
        """
        ai_request = self.env['influence_gen.ai_image_generation_request'].browse(request_id)
        if not ai_request.exists():
            _logger.error(f"AI Generation Callback: Request ID {request_id} not found.")
            # How to handle this? Maybe create a log or an alert for admin.
            return False # Or raise error if N8N expects a certain response

        ai_request.write({'n8n_execution_id': n8n_execution_id}) # Ensure it's updated

        if success:
            image_binary_data = None
            if isinstance(image_binary_data_or_url, str) and image_binary_data_or_url.startswith(('http://', 'https://')):
                try:
                    image_binary_data = self.env['influence_gen.infrastructure.integration.service'].download_file_from_url(image_binary_data_or_url)
                except Exception as e:
                    _logger.error(f"Failed to download image from URL {image_binary_data_or_url} for request {request_id}: {e}")
                    ai_request.write({'status': 'failed', 'error_details': f"Image download failed: {str(e)}"})
                    ai_request._log_usage(event_type="generation_failed_download", details={'error': str(e)})
                    # Potentially notify user
                    return False
            else: # Assuming it's base64 binary data
                image_binary_data = image_binary_data_or_url

            if not image_binary_data:
                ai_request.write({'status': 'failed', 'error_details': "No image data received from generation process."})
                ai_request._log_usage(event_type="generation_failed_no_data")
                return False

            try:
                # Create ir.attachment
                attachment_name = f"ai_img_{request_id}_{fields.Datetime.now().strftime('%Y%m%d%H%M%S')}.png" # Assuming PNG, N8N should tell format
                attachment = self.env['ir.attachment'].create({
                    'name': attachment_name,
                    'datas': image_binary_data, # Expects base64
                    'res_model': 'influence_gen.generated_image', 
                    # res_id will be set when GeneratedImage is created and linked
                })
                
                # Create GeneratedImage record
                generated_image = self.env['influence_gen.generated_image'].create_from_generation(
                    request_id=ai_request.id,
                    attachment_id=attachment.id,
                    image_binary_data=image_binary_data # For hash calculation
                )
                attachment.write({'res_id': generated_image.id}) # Link attachment back

                ai_request.write({'status': 'completed'})
                ai_request._log_usage(event_type="generation_completed", details={'generated_image_id': generated_image.id})
                
                self.env['influence_gen.audit_log_entry'].create_log(
                    event_type='AI_IMAGE_GENERATED',
                    actor_user_id=ai_request.user_id.id, # Or system if N8N is system
                    action_performed='CREATE',
                    target_object=generated_image,
                    details_dict={'request_id': ai_request.id}
                )

                # Trigger UI update/notification to user
                if ai_request.user_id:
                     try:
                        self.env['influence_gen.infrastructure.integration.service'].send_notification(
                            recipient_user_ids=[ai_request.user_id.id],
                            subject="Your AI Image is Ready!",
                            body_html=f"<p>Dear {ai_request.user_id.name},</p><p>Your AI image generation request '{ai_request.prompt[:50]}...' is complete. You can view it in your gallery.</p>"
                            # Ideally include a link or the image itself if email client supports
                        )
                     except Exception as e:
                        _logger.error(f"Failed to send AI image ready notification: {e}")

                return generated_image

            except Exception as e:
                _logger.error(f"Error processing successful AI generation for request {request_id}: {e}")
                ai_request.write({'status': 'failed', 'error_details': f"Processing error: {str(e)}"})
                ai_request._log_usage(event_type="generation_failed_processing", details={'error': str(e)})
                # If attachment was created, consider cleaning it up
                return False
        else:
            ai_request.write({'status': 'failed', 'error_details': error_details or "Generation failed with unspecified error."})
            ai_request._log_usage(event_type="generation_failed_external", details={'error': error_details})
            # Revert quota decrement if applicable (more complex logic needed here)
            # For example, if quota was a "credit hold", release it. If it was a hard decrement, add one back.
            # This needs careful design based on how quota is managed.
            # platform_setting_monthly_quota = self.env['influence_gen.platform_setting'].get_param(f'influence_gen.ai_image_default_quota_per_user_monthly', 10)
            _logger.info(f"AI Generation failed for request {request_id}. Quota adjustment might be needed.")

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='AI_IMAGE_GENERATION_FAILED',
                actor_user_id=ai_request.user_id.id, # Or system
                action_performed='UPDATE',
                target_object=ai_request,
                details_dict={'error': error_details}
            )
            # Notify user of failure
            if ai_request.user_id:
                try:
                    self.env['influence_gen.infrastructure.integration.service'].send_notification(
                        recipient_user_ids=[ai_request.user_id.id],
                        subject="AI Image Generation Failed",
                        body_html=f"<p>Dear {ai_request.user_id.name},</p><p>Your AI image generation request '{ai_request.prompt[:50]}...' failed. Details: {error_details}</p>"
                    )
                except Exception as e:
                    _logger.error(f"Failed to send AI image failure notification: {e}")
            return False

    def get_user_ai_quota_status(self, user_id):
        """
        Gets the user's AI generation quota status. REQ-AIGS-002, REQ-AIGS-007.
        :param user_id: ID of res.users
        :return: dict with keys like 'limit', 'used', 'remaining'
        """
        user = self.env['res.users'].browse(user_id)
        if not user.exists():
            raise UserError(f"User with ID {user_id} not found.")

        # This is a simplified monthly quota example. Real system might be more complex (roles, plans).
        default_monthly_quota = self.env['influence_gen.platform_setting'].get_param(
            'influence_gen.ai_image_default_quota_per_user_monthly', 
            default=0  # Default to 0 if not set, effectively disabling if not configured
        )
        if not isinstance(default_monthly_quota, int): # Ensure it's an int
            try:
                default_monthly_quota = int(default_monthly_quota)
            except ValueError:
                _logger.error(f"Invalid platform setting for monthly quota: {default_monthly_quota}. Defaulting to 0.")
                default_monthly_quota = 0


        # Calculate usage for the current period (e.g., current month)
        # This requires UsageTrackingLog model which is not defined in this SDS.
        # Placeholder for where UsageTrackingLog would be queried:
        # current_month_start = fields.Date.today().replace(day=1)
        # used_this_month = self.env['influence_gen.usage_tracking_log'].search_count([
        # ('user_id', '=', user_id),
        # ('event_type', 'in', ['request_created', 'generation_completed']), # Count successful or attempted
        # ('timestamp', '>=', fields.Datetime.to_string(current_month_start))
        # ])
        used_this_month = 0 # Placeholder since UsageTrackingLog model is not in this file set
        
        # Search for AIImageGenerationRequest records created this month by the user
        # A more accurate count might come from a dedicated UsageTrackingLog model
        # Counting 'request_created' or 'generation_completed' based on desired quota rule
        current_month_start_dt = fields.Datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Count requests that were at least queued or processing, or completed.
        # Failed requests might or might not count against quota depending on policy.
        # For simplicity, let's count all non-cancelled requests initiated by the user this month.
        # A more precise way would be to use a dedicated usage_tracking_log if it tracks "quota units consumed".
        used_this_month = self.env['influence_gen.ai_image_generation_request'].search_count([
            ('user_id', '=', user_id),
            ('create_date', '>=', current_month_start_dt),
            ('status', '!=', 'cancelled') # Don't count cancelled ones against quota perhaps
        ])
        # This is still an approximation. A dedicated `UsageTrackingLog` is better.
        # For REQ-AIGS-007, the log helps track this.

        remaining_quota = default_monthly_quota - used_this_month
        return {
            'limit': default_monthly_quota,
            'used': used_this_month,
            'remaining': remaining_quota if remaining_quota > 0 else 0,
        }

    def manage_ai_model_configurations(self, action, model_data=None, model_id=None):
        """
        Manages AI Model Configurations (CRUD). REQ-AIGS-004.
        :param action: 'create', 'update', or 'archive' (instead of deactivate for Odoo context)
        :param model_data: dict, data for create/update
        :param model_id: int, ID for update/archive
        :return: recordset or boolean
        """
        ai_model_model = self.env['influence_gen.ai_image_model']
        
        if action == 'create':
            if not model_data or not model_data.get('name'):
                raise UserError("Model name is required to create an AI model configuration.")
            model = ai_model_model.create(model_data)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='AI_MODEL_CONFIG_CREATED',
                actor_user_id=self.env.user.id,
                action_performed='CREATE',
                target_object=model,
                details_dict=model_data
            )
            return model
        elif action == 'update':
            if not model_id or not model_data:
                raise UserError("Model ID and data are required for update.")
            model = ai_model_model.browse(model_id)
            if not model.exists():
                raise UserError(f"AI Model with ID {model_id} not found.")
            model.write(model_data)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='AI_MODEL_CONFIG_UPDATED',
                actor_user_id=self.env.user.id,
                action_performed='WRITE',
                target_object=model,
                details_dict=model_data
            )
            return model
        elif action == 'archive': # Using Odoo's active/archive mechanism
            if not model_id:
                raise UserError("Model ID is required to archive.")
            model = ai_model_model.browse(model_id)
            if not model.exists():
                raise UserError(f"AI Model with ID {model_id} not found.")
            # This toggles the 'active' field. Standard Odoo behavior.
            model.action_archive() # if model inherits from 'archive.mixin'
            # Or directly: model.write({'is_active': False}) if it's a custom field like 'is_active'
            model.write({'is_active': False}) # As per SDS model field

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='AI_MODEL_CONFIG_DEACTIVATED', # or ARCHIVED
                actor_user_id=self.env.user.id,
                action_performed='WRITE', # or custom action
                target_object=model,
                details_dict={'is_active': False}
            )
            return True
        elif action == 'unarchive':
             if not model_id:
                raise UserError("Model ID is required to unarchive.")
             model = ai_model_model.browse(model_id)
             if not model.exists():
                raise UserError(f"AI Model with ID {model_id} not found.")
             model.write({'is_active': True})
             self.env['influence_gen.audit_log_entry'].create_log(
                event_type='AI_MODEL_CONFIG_ACTIVATED', # or UNARCHIVED
                actor_user_id=self.env.user.id,
                action_performed='WRITE',
                target_object=model,
                details_dict={'is_active': True}
            )
             return True
        else:
            raise UserError(f"Unsupported action: {action}")