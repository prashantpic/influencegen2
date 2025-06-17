# -*- coding: utf-8 -*-
import logging
import json
from odoo import _, api
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class AiIntegrationService:
    """
    Service class for managing AI image generation requests, N8N interaction,
    and quota management.
    """

    def __init__(self, env):
        """
        Initializes the service with the Odoo environment.
        :param env: Odoo Environment
        """
        self.env = env

    def initiate_ai_image_generation(self, user_id, influencer_profile_id, prompt_data, generation_params, campaign_id=None, intended_use='personal'):
        """
        Initiates an AI image generation request.
        - Validates prompt.
        - Checks user quota.
        - Creates AiImageGenerationRequest record.
        - Calls REPO-IGIA-004 (N8N adapter) to trigger workflow.
        - Updates request status.
        :param user_id: int, ID of res.users initiating
        :param influencer_profile_id: int, ID of influence_gen.influencer_profile for quota/context
        :param prompt_data: dict, e.g., {'prompt': 'A cat astronaut', 'negative_prompt': 'ugly, blurry'}
        :param generation_params: dict, e.g., {'model_id': X, 'resolution': '1024x1024', 'aspect_ratio': '1:1', ...}
        :param campaign_id: int, optional ID of influence_gen.campaign
        :param intended_use: str, 'personal' or 'campaign'
        :return: recordset of the created influence_gen.ai_image_generation_request
        REQ-AIGS-001, REQ-AIGS-004
        """
        _logger.info(f"Initiating AI image generation for user {user_id}, prompt: {prompt_data.get('prompt')}")

        # Validate prompt (REQ-AIGS-003)
        is_valid_prompt, reason = self.validate_ai_prompt(prompt_data.get('prompt', ''))
        if not is_valid_prompt:
            raise UserError(_("Prompt validation failed: %s") % reason)

        # Check user quota (REQ-AIGS-002)
        if not self.check_user_ai_quota(influencer_profile_id): # Pass influencer_profile_id
            raise UserError(_("AI image generation quota exceeded for this period."))

        if not generation_params.get('model_id'):
            raise UserError(_("AI Model ID is required for generation."))
        
        ai_model = self.env['influence_gen.ai_image_model'].browse(generation_params['model_id'])
        if not ai_model.exists() or not ai_model.is_active:
            raise UserError(_("Invalid or inactive AI Model selected."))

        request_vals = {
            'user_id': user_id,
            'influencer_profile_id': influencer_profile_id,
            'campaign_id': campaign_id,
            'prompt': prompt_data.get('prompt'),
            'negative_prompt': prompt_data.get('negative_prompt'),
            'model_id': generation_params['model_id'],
            'resolution': generation_params.get('resolution', '1024x1024'),
            'aspect_ratio': generation_params.get('aspect_ratio', '1:1'),
            'seed': generation_params.get('seed'),
            'inference_steps': generation_params.get('inference_steps'),
            'cfg_scale': generation_params.get('cfg_scale'),
            'status': 'queued',
            'intended_use': intended_use,
        }
        ai_request = self.env['influence_gen.ai_image_generation_request'].create(request_vals)
        _logger.info(f"Created AI Image Generation Request ID: {ai_request.id}")

        # Prepare payload for N8N adapter
        n8n_payload = {
            'request_id': ai_request.id, # Odoo request ID for callback
            'prompt': ai_request.prompt,
            'negative_prompt': ai_request.negative_prompt,
            'model_external_id': ai_model.external_model_id or ai_model.name, # ID known to N8N/AI service
            'resolution': ai_request.resolution,
            'aspect_ratio': ai_request.aspect_ratio,
            'seed': ai_request.seed,
            'inference_steps': ai_request.inference_steps,
            'cfg_scale': ai_request.cfg_scale,
            'callback_url_success': f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/influence_gen/ai_callback/success",
            'callback_url_error': f"{self.env['ir.config_parameter'].sudo().get_param('web.base.url')}/influence_gen/ai_callback/error",
        }

        try:
            # Call REPO-IGIA-004 (Integration Adapter for N8N)
            # This is a placeholder for the actual adapter call
            # n8n_execution_id = self.env['influence_gen.integration.adapter'].trigger_ai_generation_workflow(n8n_payload)
            # _logger.info(f"Triggered N8N workflow. Execution ID (placeholder): {n8n_execution_id}")
            # ai_request.write({'status': 'processing_n8n', 'n8n_execution_id': n8n_execution_id})
            
            # Placeholder for direct call simulation if adapter not available
            _logger.warning("N8N Integration Adapter call is a placeholder. Simulating call.")
            # For testing, one might directly call handle_n8n_image_result_callback or error_callback
            # For now, just set to processing_n8n
            ai_request.write({'status': 'processing_n8n', 'n8n_execution_id': f'simulated_n8n_exec_{ai_request.id}'})

        except Exception as e:
            _logger.error(f"Failed to trigger N8N workflow for request {ai_request.id}: {e}")
            ai_request.write({'status': 'failed', 'error_details': str(e)})
            raise UserError(_("Failed to initiate AI image generation with external service: %s") % str(e))
            
        return ai_request

    def handle_n8n_image_result_callback(self, request_id, image_results_list, n8n_execution_id):
        """
        Handles successful image generation results from N8N callback.
        - Finds AiImageGenerationRequest.
        - Creates ir.attachment and GeneratedImage records.
        - Calculates hash, sets retention category.
        - Updates request status to 'completed'.
        - Decrements quota and logs usage.
        :param request_id: int, ID of influence_gen.ai_image_generation_request
        :param image_results_list: list of dicts, each with image data (e.g., 'image_base64', 'file_name', 'format', 'size', 'width', 'height', 'external_url')
        :param n8n_execution_id: str, N8N execution ID for tracing
        REQ-AIGS-001, REQ-AIGS-006, REQ-AIGS-010
        """
        _logger.info(f"Handling N8N image result callback for request ID: {request_id}, N8N Exec ID: {n8n_execution_id}")
        ai_request = self.env['influence_gen.ai_image_generation_request'].browse(request_id)
        if not ai_request.exists():
            _logger.error(f"AI Generation Request ID {request_id} not found for N8N callback.")
            return False # Or raise error to N8N if it expects a specific response

        GeneratedImage = self.env['influence_gen.generated_image']
        Attachment = self.env['ir.attachment']
        images_generated_count = 0

        for img_data in image_results_list:
            # Handle image data (direct base64 or download from URL via REPO-IGIA-004)
            attachment_id = None
            storage_url = img_data.get('external_url')
            
            if img_data.get('image_base64'):
                # Store as ir.attachment
                try:
                    attachment = Attachment.create({
                        'name': img_data.get('file_name', f"ai_image_{ai_request.id}_{images_generated_count + 1}.{img_data.get('format', 'png')}"),
                        'datas': img_data['image_base64'],
                        'res_model': 'influence_gen.generated_image', # Link to the generated image record
                        # res_id will be set after generated_image record is created
                    })
                    attachment_id = attachment.id
                    _logger.info(f"Created ir.attachment {attachment_id} for image from request {ai_request.id}")
                except Exception as e:
                    _logger.error(f"Failed to create attachment for request {ai_request.id}: {e}")
                    continue # Skip this image
            elif storage_url:
                _logger.info(f"Image for request {ai_request.id} is at external URL: {storage_url}")
            else:
                _logger.warning(f"No image data or URL provided for an image in request {ai_request.id}")
                continue

            # Calculate hash (placeholder, actual hashing library needed)
            # REQ-AIGS-010
            # import hashlib
            # image_bytes = base64.b64decode(img_data['image_base64']) if img_data.get('image_base64') else b''
            # hash_value = hashlib.sha256(image_bytes).hexdigest() if image_bytes else None
            hash_value = f"simulated_hash_{ai_request.id}_{images_generated_count + 1}" # Placeholder

            # Determine retention category
            # REQ-AIGS-011
            retention_category = 'personal_generation'
            usage_rights_text = _("Standard personal use rights.")
            if ai_request.intended_use == 'campaign' and ai_request.campaign_id:
                retention_category = 'campaign_asset_standard' # Default, could be more specific
                usage_rights_text = ai_request.campaign_id.usage_rights or _("Standard campaign usage rights.")
            
            gen_image = GeneratedImage.create({
                'request_id': ai_request.id,
                'image_attachment_id': attachment_id,
                'storage_url': storage_url,
                'file_format': img_data.get('format', 'png'),
                'file_size': img_data.get('size'),
                'width': img_data.get('width'),
                'height': img_data.get('height'),
                'hash_value': hash_value,
                'retention_category': retention_category,
                'usage_rights': usage_rights_text,
                'is_campaign_asset': True if ai_request.intended_use == 'campaign' else False,
            })
            if attachment_id: # Link attachment to the generated image record
                self.env['ir.attachment'].browse(attachment_id).write({'res_id': gen_image.id})

            _logger.info(f"Created GeneratedImage record ID {gen_image.id} for request {ai_request.id}")
            images_generated_count += 1

        if images_generated_count > 0:
            ai_request.write({
                'status': 'completed',
                'n8n_execution_id': n8n_execution_id, # Update if changed/confirmed by N8N
                'error_details': None,
            })
            self.decrement_user_ai_quota(ai_request.influencer_profile_id.id, images_generated_count) # REQ-AIGS-002
            self.log_ai_usage(ai_request.id, images_generated_count, api_calls_to_ai_service=1) # REQ-AIGS-007
            _logger.info(f"AI Request ID {ai_request.id} completed with {images_generated_count} images.")
        else:
            # If no images were successfully processed from callback, mark as failed.
            ai_request.write({
                'status': 'failed',
                'n8n_execution_id': n8n_execution_id,
                'error_details': _("N8N callback received but no valid image data processed."),
            })
            _logger.warning(f"AI Request ID {ai_request.id} processed callback but generated 0 images successfully.")
        return True

    def handle_n8n_image_error_callback(self, request_id, error_message, n8n_execution_id):
        """
        Handles error callback from N8N.
        - Finds AiImageGenerationRequest.
        - Updates status to 'failed', stores error_message.
        - Logs. Sends failure notification (conceptual).
        :param request_id: int, ID of influence_gen.ai_image_generation_request
        :param error_message: str, error details from N8N
        :param n8n_execution_id: str, N8N execution ID for tracing
        REQ-AIGS-001
        """
        _logger.error(f"Handling N8N image error callback for request ID: {request_id}. Error: {error_message}")
        ai_request = self.env['influence_gen.ai_image_generation_request'].browse(request_id)
        if not ai_request.exists():
            _logger.error(f"AI Generation Request ID {request_id} not found for N8N error callback.")
            return False

        ai_request.write({
            'status': 'failed',
            'error_details': error_message,
            'n8n_execution_id': n8n_execution_id,
        })
        _logger.info(f"AI Request ID {ai_request.id} marked as failed due to N8N error.")
        
        # Send failure notification (conceptual, could be an Odoo activity or email)
        # REQ-AIGS-015 for notifications
        # Example:
        # ai_request.message_post(body=_("AI image generation failed. Details: %s") % error_message)
        
        return True

    def check_user_ai_quota(self, influencer_profile_id):
        """
        Checks if the user has available AI generation quota.
        Reads quota settings (from PlatformSetting or user/role config)
        and current usage (from UsageTrackingLog for the current period).
        :param influencer_profile_id: int, ID of influence_gen.influencer_profile
        :return: bool (True if quota available)
        REQ-AIGS-002
        """
        PlatformSetting = self.env['influence_gen.platform_setting']
        influencer = self.env['influence_gen.influencer_profile'].browse(influencer_profile_id)
        if not influencer.exists():
            _logger.warning(f"Influencer profile {influencer_profile_id} not found for quota check.")
            return False

        # Get default monthly quota
        default_quota_str = PlatformSetting.get_setting('ai.image_generation.default_monthly_quota', default='100')
        try:
            monthly_quota = int(default_quota_str)
        except ValueError:
            monthly_quota = 100 # Fallback
            _logger.warning(f"Could not parse 'ai.image_generation.default_monthly_quota'. Using fallback {monthly_quota}.")

        # Calculate usage for the current month
        # This requires UsageTrackingLog to store 'quantity_used' or similar.
        # Assuming UsageTrackingLog stores one record per image generated for simplicity.
        from datetime import datetime, date
        from dateutil.relativedelta import relativedelta
        
        today = date.today()
        start_of_month = today.replace(day=1)
        # Convert to datetime for Odoo search
        start_of_month_dt = datetime.combine(start_of_month, datetime.min.time())

        usage_count = self.env['influence_gen.usage_tracking_log'].search_count([
            ('influencer_profile_id', '=', influencer_profile_id),
            ('feature_name', '=', 'ai_image_generation'),
            ('timestamp', '>=', start_of_month_dt),
        ])
        
        _logger.info(f"Quota check for influencer {influencer_profile_id}: Quota={monthly_quota}, Used={usage_count}")
        return usage_count < monthly_quota

    def decrement_user_ai_quota(self, influencer_profile_id, images_generated=1):
        """
        Conceptually decrements user's AI quota. In this implementation, this means
        the next call to check_user_ai_quota will reflect this usage because
        log_ai_usage creates the records that check_user_ai_quota counts.
        :param influencer_profile_id: int, ID of influence_gen.influencer_profile
        :param images_generated: int, number of images generated in this request
        REQ-AIGS-002
        """
        # This method is effectively a no-op if log_ai_usage is called correctly,
        # as quota is checked based on logged usage.
        # It's kept for conceptual clarity.
        _logger.info(f"Quota conceptually decremented for influencer {influencer_profile_id} by {images_generated} images (usage logged separately).")
        pass

    def log_ai_usage(self, request_id, images_generated, api_calls_to_ai_service=0):
        """
        Logs AI usage for a specific generation request.
        :param request_id: int, ID of influence_gen.ai_image_generation_request
        :param images_generated: int, number of images successfully generated
        :param api_calls_to_ai_service: int, number of direct calls made to the AI service (if tracked)
        REQ-AIGS-007
        """
        ai_request = self.env['influence_gen.ai_image_generation_request'].browse(request_id)
        if not ai_request.exists():
            _logger.error(f"Cannot log AI usage: AI Request ID {request_id} not found.")
            return

        for _i in range(images_generated): # Create one log entry per image for simple monthly counting
            self.env['influence_gen.usage_tracking_log'].create({
                'user_id': ai_request.user_id.id,
                'influencer_profile_id': ai_request.influencer_profile_id.id,
                'feature_name': 'ai_image_generation',
                'timestamp': fields.Datetime.now(),
                'campaign_id': ai_request.campaign_id.id if ai_request.campaign_id else None,
                'details_json': json.dumps({
                    'request_id': ai_request.id,
                    'model_id': ai_request.model_id.id,
                    'prompt_length': len(ai_request.prompt or ""),
                    'images_in_batch': images_generated, # Total for this one request
                    'api_calls': api_calls_to_ai_service, # If relevant
                }),
            })
        _logger.info(f"Logged {images_generated} AI usage events for request ID {ai_request.id}")


    def validate_ai_prompt(self, prompt_text):
        """
        Validates AI prompt against content moderation rules.
        (e.g., denylist from PlatformSetting, or calls external moderation API via REPO-IGIA-004)
        :param prompt_text: str, the prompt to validate
        :return: tuple (is_valid: bool, reason: str or None)
        REQ-AIGS-003
        """
        if not prompt_text or len(prompt_text.strip()) == 0:
            return False, _("Prompt cannot be empty.")
        
        # Denylist from PlatformSetting
        denylist_str = self.env['influence_gen.platform_setting'].get_setting('ai.prompt.denylist_keywords', default='[]')
        try:
            denylist_keywords = json.loads(denylist_str)
            if not isinstance(denylist_keywords, list):
                denylist_keywords = []
        except json.JSONDecodeError:
            denylist_keywords = []
            _logger.warning("Could not parse 'ai.prompt.denylist_keywords'. Using empty denylist.")

        for keyword in denylist_keywords:
            if keyword.lower() in prompt_text.lower():
                _logger.warning(f"Prompt validation failed due to denylisted keyword: {keyword}")
                return False, _("Prompt contains restricted content (%s).") % keyword
        
        # Placeholder for external moderation API call via REPO-IGIA-004
        # try:
        #     is_safe, reason = self.env['influence_gen.integration.adapter'].moderate_text(prompt_text)
        #     if not is_safe:
        #         return False, reason or _("Prompt failed external content moderation.")
        # except Exception as e:
        #     _logger.error(f"Error calling external prompt moderation: {e}")
        #     # Fail open or closed depending on policy. Failing closed for safety.
        #     return False, _("Could not verify prompt with external moderation service.")

        return True, None

    def reset_monthly_quotas_for_all_users(self):
        """
        CRON JOB METHOD: Resets monthly AI quotas.
        In the current design (quota checked against logs), this method might not do anything directly
        to user records, as the "reset" is implicit by the time window of the log query.
        However, it could be used to:
        - Send notifications about quota reset.
        - Archive old usage logs if needed (though retention service is better for that).
        - Pre-calculate or cache quota statuses if performance becomes an issue.
        REQ-AIGS-002 (quota reset)
        """
        _logger.info("Executing cron job: Reset Monthly AI Quotas (Conceptual).")
        # For now, this is a conceptual reset. If quotas were stored directly on user/profile,
        # this method would update those records. With log-based checking, the new month automatically
        # starts a fresh count.
        
        # Example: Send notification to all active influencers about quota reset
        # active_influencers = self.env['influence_gen.influencer_profile'].search([('account_status', '=', 'active')])
        # template = self.env.ref('influence_gen_services.email_template_ai_quota_reset', raise_if_not_found=False)
        # if template:
        #     for influencer in active_influencers:
        #         try:
        #             template.send_mail(influencer.id, force_send=True)
        #         except Exception as e:
        #             _logger.error(f"Failed to send quota reset email to {influencer.email}: {e}")
        _logger.info("Monthly AI Quota reset cycle completed (log-based, no direct data change needed for reset itself).")
        return True