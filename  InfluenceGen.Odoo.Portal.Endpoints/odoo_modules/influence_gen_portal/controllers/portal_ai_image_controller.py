from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, AccessError
import werkzeug
import json # For error responses if not handled by Odoo's json type

class InfluenceGenPortalAIImage(http.Controller):
    """
    Controller for AJAX interactions related to AI Image Generation.
    """

    def _get_influencer_profile(self):
        """Helper to get the current user's influencer profile."""
        user = request.env.user
        influencer_profile = request.env['influence_gen.influencer_profile'].sudo().search([('user_id', '=', user.id)], limit=1)
        if not influencer_profile:
            # For JSON endpoints, return a JSON error
            return {'error': _("Influencer profile not found."), 'status_code': 403}
        # Add checks for KYC/Account status if AI generation is restricted
        # if influencer_profile.kyc_status != 'approved' or influencer_profile.account_status != 'active':
        #     return {'error': _("AI Image Generation requires a verified and active profile."), 'status_code': 403}
        return influencer_profile

    @http.route('/my/ai/generate', type='json', auth="user", methods=['POST'], csrf=True)
    def initiate_ai_image_generation(self, **params):
        """
        Initiates AI image generation.
        Receives prompt, parameters via JSON POST.
        Calls business service to trigger N8N webhook asynchronously.
        Returns a unique request_id.
        """
        influencer_or_error = self._get_influencer_profile()
        if isinstance(influencer_or_error, dict) and 'error' in influencer_or_error:
            request.jsonrequest['error'] = influencer_or_error # Let Odoo handle JSON error response
            return influencer_or_error


        influencer = influencer_or_error
        
        # Extract parameters from params (which is request.jsonrequest)
        # prompt = params.get('prompt')
        # negative_prompt = params.get('negative_prompt')
        # ... other params ...
        
        # Basic validation of required params
        if not params.get('prompt'):
            return {'error': _("Prompt is required."), 'status_code': 400}

        try:
            # result = request.env['influence_gen.ai_image_service'].sudo().initiate_generation_request(
            #     user_id=request.env.user.id, # Or influencer.id if service expects that
            #     params=params
            # )
            # if not result.get('success'):
            #     return {'error': result.get('message', _("Failed to initiate generation.")), 'status_code': result.get('status_code', 500)}
            
            # Placeholder success
            import uuid
            request_id = str(uuid.uuid4())
            # Simulate call to business service which would then create `influence_gen.ai_image_generation_request`
            # request.env['influence_gen.ai_image_generation_request'].sudo().create({
            #    'id': request_id, # If ID is external UUID
            #    'user_id': request.env.user.id,
            #    'influencer_profile_id': influencer.id,
            #    'prompt': params.get('prompt'),
            #    'status': 'queued',
            #    # ... other params ...
            # })

            return {'request_id': request_id, 'status': 'queued'}
        except UserError as e: # Validation errors from business layer
            return {'error': str(e), 'status_code': 400}
        except Exception as e:
            # Log error
            return {'error': _("An unexpected error occurred."), 'status_code': 500}


    @http.route('/my/ai/generate/status', type='json', auth="user", methods=['GET'])
    def get_ai_image_generation_status(self, request_id=None, **kw):
        """
        Fetches the status and potentially image URL(s) for a given AI image generation request_id.
        """
        influencer_or_error = self._get_influencer_profile()
        if isinstance(influencer_or_error, dict) and 'error' in influencer_or_error:
            return influencer_or_error
        
        if not request_id:
            return {'error': _("Request ID is required."), 'status_code': 400}

        try:
            # result = request.env['influence_gen.ai_image_service'].sudo().get_generation_status(
            #     request_id=request_id,
            #     user_id=request.env.user.id # For security/ownership check
            # )
            # if not result: # Or if result indicates an error/not found
            #    return {'error': _("Status not found or access denied."), 'status_code': 404}
            # return result

            # Placeholder logic
            # gen_request = request.env['influence_gen.ai_image_generation_request'].sudo().search([
            #    ('id', '=', request_id), # If ID is external UUID and model has that field
            #    ('user_id', '=', request.env.user.id) # Ensure user owns this request
            # ], limit=1)
            # if not gen_request:
            #    return {'error': _("Request not found or access denied."), 'status_code': 404}

            # Simulate different statuses for testing
            import random
            statuses = ['processing', 'completed', 'failed']
            current_status = random.choice(statuses)
            
            response = {'request_id': request_id, 'status': current_status}
            if current_status == 'completed':
                response['images'] = [{'id': 'img_uuid_1', 'url': '/influence_gen_portal/static/img/placeholder_ai_image.png'}] # Placeholder URL
                response['quota_update'] = {'used': 5, 'total': 100} # Example quota update
            elif current_status == 'failed':
                response['error_message'] = _("Generation failed due to an unexpected issue.")
            
            return response

        except Exception as e:
            # Log error
            return {'error': _("An unexpected error occurred while fetching status."), 'status_code': 500}

    @http.route('/my/ai/models', type='json', auth="user", methods=['GET'])
    def get_available_ai_models(self, **kw):
        """
        Fetches the list of available AI models for generation.
        """
        influencer_or_error = self._get_influencer_profile()
        if isinstance(influencer_or_error, dict) and 'error' in influencer_or_error:
            return influencer_or_error
        
        try:
            # models = request.env['influence_gen.ai_image_service'].sudo().get_available_models_for_portal()
            # Placeholder:
            models = [
                {'id': 'model_1', 'name': _('Standard Model Alpha'), 'description': _('Good for general purpose images.')},
                {'id': 'model_2', 'name': _('Artistic Model Beta'), 'description': _('Creates stylized artistic images.')}
            ]
            return models
        except Exception as e:
            # Log error
            return {'error': _("Failed to load AI models."), 'status_code': 500}

    @http.route('/my/ai/prompts/saved', type='json', auth="user", methods=['GET'])
    def get_saved_ai_prompts(self, **kw):
        """
        Fetches the user's saved AI prompts.
        """
        influencer_or_error = self._get_influencer_profile()
        if isinstance(influencer_or_error, dict) and 'error' in influencer_or_error:
            return influencer_or_error
        influencer = influencer_or_error
        
        try:
            # saved_prompts = request.env['influence_gen.ai_image_service'].sudo().get_user_saved_prompts(influencer.id)
            # Placeholder
            saved_prompts = [
                {'id': 'prompt_1', 'text': _('A cat wearing a wizard hat')},
                {'id': 'prompt_2', 'text': _('Cyberpunk cityscape at night, neon lights, rain')}
            ]
            return saved_prompts
        except Exception as e:
            # Log error
            return {'error': _("Failed to load saved prompts."), 'status_code': 500}

    @http.route('/my/ai/prompts/save', type='json', auth="user", methods=['POST'], csrf=True)
    def save_user_ai_prompt(self, **params):
        """
        Saves a new AI prompt for the user.
        """
        influencer_or_error = self._get_influencer_profile()
        if isinstance(influencer_or_error, dict) and 'error' in influencer_or_error:
            return influencer_or_error
        influencer = influencer_or_error

        prompt_text = params.get('prompt')
        if not prompt_text or len(prompt_text) < 5: # Basic validation
            return {'error': _("Prompt text is too short or missing."), 'status_code': 400}
        
        try:
            # result = request.env['influence_gen.ai_image_service'].sudo().save_user_prompt(influencer.id, prompt_text)
            # if not result.get('success'):
            #     return {'error': result.get('message', _("Failed to save prompt.")), 'status_code': 500}
            # return {'success': True, 'prompt_id': result.get('prompt_id')}
            # Placeholder
            return {'success': True, 'prompt_id': 'new_prompt_id_placeholder'}
        except UserError as e:
            return {'error': str(e), 'status_code': 400}
        except Exception as e:
            # Log error
            return {'error': _("Failed to save prompt due to an unexpected error."), 'status_code': 500}