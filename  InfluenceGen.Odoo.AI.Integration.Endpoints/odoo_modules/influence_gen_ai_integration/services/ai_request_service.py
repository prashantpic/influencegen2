# -*- coding: utf-8 -*-
import logging
import requests
from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AIRequestService(models.AbstractModel):
    _name = 'influence_gen.ai_request_service'
    _description = 'Service to initiate AI Image Generation Requests to N8N'

    def _get_n8n_webhook_url(self):
        """Retrieves the N8N webhook URL from system parameters."""
        webhook_url = self.env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_webhook_url')
        if not webhook_url or webhook_url.startswith('PLACEHOLDER_'):
            _logger.error("N8N webhook URL ('influence_gen.n8n_webhook_url') is not configured or is a placeholder.")
            raise UserError(_("N8N webhook URL is not configured. Please contact system administrator."))
        return webhook_url

    def _get_n8n_api_key(self):
        """Retrieves the N8N API key from system parameters."""
        api_key = self.env['ir.config_parameter'].sudo().get_param('influence_gen.n8n_api_key')
        if not api_key or api_key.startswith('PLACEHOLDER_'):
            _logger.error("N8N API key ('influence_gen.n8n_api_key') is not configured or is a placeholder.")
            raise UserError(_("N8N API key is not configured. Please contact system administrator."))
        return api_key

    def initiate_ai_image_generation(self, ai_generation_request_id, generation_params):
        """
        Initiates an AI image generation request to N8N.

        :param ai_generation_request_id: int, ID of the influence_gen.ai_image_request record.
        :param generation_params: dict, Parameters for the AI image generation.
        :return: bool, True if initiation was successful, False otherwise.
        """
        AIImageRequest = self.env['influence_gen.ai_image_request']
        request_record = AIImageRequest.sudo().browse(ai_generation_request_id)

        if not request_record.exists():
            _logger.error(f"AIImageGenerationRequest record with ID {ai_generation_request_id} not found.")
            return False

        try:
            n8n_webhook_url = self._get_n8n_webhook_url()
            n8n_api_key = self._get_n8n_api_key()

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            if not base_url:
                _logger.error("System parameter 'web.base.url' is not configured.")
                request_record.write({
                    'status': 'initiation_failed',
                    'error_details': _("System base URL not configured.")
                })
                return False
            
            odoo_callback_url = f"{base_url}/influence_gen/ai/callback/image_result"
            
            odoo_to_n8n_token = self.env['ir.config_parameter'].sudo().get_param('influence_gen.odoo_to_n8n_secret_token')
            if not odoo_to_n8n_token or odoo_to_n8n_token.startswith('PLACEHOLDER_'):
                _logger.error("Odoo to N8N secret token ('influence_gen.odoo_to_n8n_secret_token') is not configured.")
                request_record.write({
                    'status': 'initiation_failed',
                    'error_details': _("Odoo to N8N security token not configured.")
                })
                return False

            payload = {
                'ai_generation_request_id': str(request_record.id),
                'params': generation_params,
                'odoo_callback_url': odoo_callback_url,
                'security_token': odoo_to_n8n_token
            }

            headers = {
                'Content-Type': 'application/json',
                'X-N8N-Api-Key': n8n_api_key
            }

            _logger.info(f"Initiating AI image generation request ID {request_record.id} to N8N. URL: {n8n_webhook_url}")
            
            response = requests.post(n8n_webhook_url, json=payload, headers=headers, timeout=30)

            if 200 <= response.status_code < 300:
                _logger.info(f"Successfully initiated AI request {request_record.id} to N8N. Status: {response.status_code}")
                request_record.write({'status': 'processing'}) # Or 'sent_to_n8n'
                return True
            else:
                error_msg = f"Failed to initiate AI request {request_record.id} to N8N. Status: {response.status_code}, Response: {response.text}"
                _logger.error(error_msg)
                request_record.write({
                    'status': 'initiation_failed',
                    'error_details': error_msg
                })
                return False

        except UserError as e: # Configuration errors
            _logger.error(f"Configuration error for AI request {request_record.id}: {e}")
            request_record.write({
                'status': 'initiation_failed',
                'error_details': str(e)
            })
            return False
        except requests.exceptions.Timeout:
            error_msg = f"Timeout while initiating AI request {request_record.id} to N8N."
            _logger.error(error_msg)
            request_record.write({
                'status': 'initiation_failed',
                'error_details': error_msg
            })
            return False
        except requests.exceptions.ConnectionError:
            error_msg = f"Connection error while initiating AI request {request_record.id} to N8N."
            _logger.error(error_msg)
            request_record.write({
                'status': 'initiation_failed',
                'error_details': error_msg
            })
            return False
        except requests.exceptions.RequestException as e:
            error_msg = f"General request exception for AI request {request_record.id}: {e}"
            _logger.exception(error_msg) # Log full exception
            request_record.write({
                'status': 'initiation_failed',
                'error_details': error_msg
            })
            return False
        except Exception as e:
            error_msg = f"Unexpected error during AI request initiation for {request_record.id}: {e}"
            _logger.exception(error_msg)
            request_record.write({
                'status': 'initiation_failed',
                'error_details': _("An unexpected error occurred during request initiation.")
            })
            return False