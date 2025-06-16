# -*- coding: utf-8 -*-
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, AccessError
from werkzeug.exceptions import Forbidden, BadRequest

_logger = logging.getLogger(__name__)

class InfluenceGenPortalAIImage(http.Controller):

    def _get_influencer_profile_or_raise_json(self):
        user = request.env.user
        influencer_profile = user.influencer_profile_id if hasattr(user, 'influencer_profile_id') else False
        if not influencer_profile:
            # For JSON endpoints, return structured error
            raise BadRequest(_("Influencer profile not found or not configured."))
        return influencer_profile

    @http.route('/my/ai/generate', type='json', auth='user', methods=['POST'], website=True, csrf=True)
    def initiate_ai_image_generation(self, **params):
        """
        JSON endpoint to initiate AI image generation request.
        Receives parameters from the OWL component's JSON request body.
        `params` will be the deserialized JSON payload.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise_json()
            ai_image_service = request.env['influence_gen.ai.image.service'] # Specific AI Image service

            # Parameters are directly available in `params` dict
            required_params = ['prompt', 'model_id', 'resolution', 'aspect_ratio', 'intended_use']
            missing_params = [p for p in required_params if p not in params or not params[p]]
            if missing_params:
                raise BadRequest(_("Missing required parameters: %s") % ", ".join(missing_params))

            request_id_result = ai_image_service.sudo(influencer_profile.user_id.id).initiate_generation_request(
                influencer_profile.id,
                params # Pass the whole params dict to the service for validation and processing
            )
            # Service should return {'request_id': '...', 'status': 'queued', 'quota_status': {...}}
            return request_id_result
        except UserError as e: # Business logic errors from the service
            _logger.warning("AI image generation initiation failed (UserError) for %s: %s", request.env.user.login, str(e))
            return {'error': str(e), 'type': 'user_error'}
        except BadRequest as e: # For missing params or validation errors from this controller
             _logger.warning("AI image generation initiation failed (BadRequest) for %s: %s", request.env.user.login, str(e))
             return {'error': str(e.description), 'type': 'bad_request'}
        except Exception as e:
            _logger.error("Error initiating AI image generation for user %s: %s", request.env.user.login, e, exc_info=True)
            return {'error': _("An unexpected error occurred during image generation initiation."), 'type': 'server_error'}

    @http.route('/my/ai/generate/status', type='json', auth='user', methods=['POST'], website=True, csrf=True) # Using POST for JSON body
    def get_ai_image_generation_status(self, **params): # request_id will be in params
        """
        JSON endpoint to check the status of an AI image generation request.
        Receives request_id in the JSON request body.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise_json()
            ai_image_service = request.env['influence_gen.ai.image.service']
            
            request_id = params.get('request_id')
            if not request_id:
                raise BadRequest(_("Request ID is required."))

            status_data = ai_image_service.sudo(influencer_profile.user_id.id).check_generation_status(
                request_id,
                influencer_profile.id
            )
            # Service should return {'request_id': '...', 'status': '...', 'images': [...], 'error_message': '...', 'quota_status': {...}}
            return status_data
        except UserError as e:
            _logger.warning("AI image generation status check failed (UserError) for %s (req %s): %s", request.env.user.login, params.get('request_id'), str(e))
            return {'error': str(e), 'type': 'user_error'}
        except BadRequest as e:
            _logger.warning("AI image generation status check failed (BadRequest) for %s (req %s): %s", request.env.user.login, params.get('request_id'), str(e))
            return {'error': str(e.description), 'type': 'bad_request'}
        except Exception as e:
            _logger.error("Error checking AI generation status for request %s (user %s): %s", params.get('request_id'), request.env.user.login, e, exc_info=True)
            return {'error': _("An unexpected error occurred while checking status."), 'type': 'server_error'}

    # Additional endpoints for AI service as per SDS 4.4.5 (getAvailableModels, getSavedPrompts, saveUserPrompt)
    @http.route('/my/ai/models', type='json', auth='user', methods=['POST'], website=True, csrf=True) # Using POST for consistency with JSON
    def get_ai_available_models(self, **kw):
        try:
            influencer_profile = self._get_influencer_profile_or_raise_json()
            ai_image_service = request.env['influence_gen.ai.image.service']
            models = ai_image_service.sudo(influencer_profile.user_id.id).get_available_models_for_portal()
            return models
        except BadRequest as e:
             return {'error': str(e.description), 'type': 'bad_request'}
        except Exception as e:
            _logger.error("Error fetching AI models for user %s: %s", request.env.user.login, e, exc_info=True)
            return {'error': _("Could not fetch AI models."), 'type': 'server_error'}

    @http.route('/my/ai/prompts/saved', type='json', auth='user', methods=['POST'], website=True, csrf=True)
    def get_ai_saved_prompts(self, **kw):
        try:
            influencer_profile = self._get_influencer_profile_or_raise_json()
            ai_image_service = request.env['influence_gen.ai.image.service']
            prompts = ai_image_service.sudo(influencer_profile.user_id.id).get_influencer_saved_prompts(influencer_profile.id)
            return prompts
        except BadRequest as e:
             return {'error': str(e.description), 'type': 'bad_request'}
        except Exception as e:
            _logger.error("Error fetching saved prompts for user %s: %s", request.env.user.login, e, exc_info=True)
            return {'error': _("Could not fetch saved prompts."), 'type': 'server_error'}

    @http.route('/my/ai/prompts/save', type='json', auth='user', methods=['POST'], website=True, csrf=True)
    def save_ai_user_prompt(self, **params):
        try:
            influencer_profile = self._get_influencer_profile_or_raise_json()
            ai_image_service = request.env['influence_gen.ai.image.service']
            
            prompt_text = params.get('prompt')
            if not prompt_text:
                raise BadRequest(_("Prompt text is required to save."))
            
            ai_image_service.sudo(influencer_profile.user_id.id).save_influencer_prompt(influencer_profile.id, prompt_text)
            return {'success': True, 'message': _("Prompt saved successfully.")}
        except UserError as e:
             return {'error': str(e), 'type': 'user_error'}
        except BadRequest as e:
             return {'error': str(e.description), 'type': 'bad_request'}
        except Exception as e:
            _logger.error("Error saving prompt for user %s: %s", request.env.user.login, e, exc_info=True)
            return {'error': _("An error occurred while saving the prompt."), 'type': 'server_error'}