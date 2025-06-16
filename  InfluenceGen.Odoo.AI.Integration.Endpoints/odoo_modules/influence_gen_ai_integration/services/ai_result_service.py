# -*- coding: utf-8 -*-
import base64
import hashlib
import logging
import requests
from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AIResultService(models.AbstractModel):
    _name = 'influence_gen.ai_result_service'
    _description = 'Service to process AI Image Generation Results from N8N'

    def _download_and_store_image(self, image_url, request_record, image_metadata):
        """
        Downloads an image from a URL and stores it as an ir.attachment,
        then creates a influence_gen.generated_image record.
        """
        GeneratedImage = self.env['influence_gen.generated_image']
        Attachment = self.env['ir.attachment']

        try:
            _logger.info(f"Downloading image for request {request_record.id} from {image_url}")
            response = requests.get(image_url, stream=True, timeout=60)
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)

            image_content = response.content
            hash_value = hashlib.sha256(image_content).hexdigest()

            # Determine retention_category (simplified logic for now)
            retention_category = 'personal_generation'
            if request_record.campaign_id and request_record.intended_use == 'campaign':
                # Example: retention_category = f"campaign_{request_record.campaign_id.id}"
                retention_category = 'campaign_asset' # Adjust as per actual logic in base models/requirements
            elif request_record.intended_use:
                 retention_category = request_record.intended_use


            attachment_vals = {
                'name': f"ai_gen_req_{request_record.id}_{image_metadata.get('file_format', 'bin')}",
                'datas': base64.b64encode(image_content),
                'res_model': GeneratedImage._name,
                # res_id will be linked after GeneratedImage record is created
                'mimetype': image_metadata.get('mimetype', 'application/octet-stream'),
            }
            attachment = Attachment.sudo().create(attachment_vals)
            _logger.info(f"Created attachment {attachment.id} for request {request_record.id}")

            image_vals = {
                'request_id': request_record.id,
                'storage_identifier': str(attachment.id),
                'storage_type': 'ir.attachment',
                'file_format': image_metadata.get('file_format'),
                'file_size': image_metadata.get('file_size', len(image_content)),
                'width': image_metadata.get('width'),
                'height': image_metadata.get('height'),
                'hash_value': hash_value,
                'retention_category': retention_category,
            }
            generated_image_record = GeneratedImage.sudo().create(image_vals)
            _logger.info(f"Created GeneratedImage record {generated_image_record.id} for request {request_record.id}")

            attachment.sudo().write({'res_id': generated_image_record.id})
            _logger.info(f"Linked attachment {attachment.id} to GeneratedImage {generated_image_record.id}")

            return generated_image_record

        except requests.exceptions.HTTPError as e:
            _logger.error(f"HTTP error downloading image for request {request_record.id}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error downloading image for request {request_record.id}: {e}")
            return None
        except Exception as e:
            _logger.exception(f"Unexpected error storing image for request {request_record.id}:")
            return None

    def _handle_direct_image_data(self, image_data_b64, request_record, image_metadata):
        """Handles base64 encoded image data, stores it, and creates records."""
        GeneratedImage = self.env['influence_gen.generated_image']
        Attachment = self.env['ir.attachment']
        try:
            image_content = base64.b64decode(image_data_b64)
            hash_value = hashlib.sha256(image_content).hexdigest()

            retention_category = 'personal_generation'
            if request_record.campaign_id and request_record.intended_use == 'campaign':
                retention_category = 'campaign_asset'
            elif request_record.intended_use:
                 retention_category = request_record.intended_use

            attachment_vals = {
                'name': f"ai_gen_req_{request_record.id}_direct_{image_metadata.get('file_format', 'bin')}",
                'datas': image_data_b64, # Already base64 encoded
                'res_model': GeneratedImage._name,
                'mimetype': image_metadata.get('mimetype', 'application/octet-stream'),
            }
            attachment = Attachment.sudo().create(attachment_vals)
            _logger.info(f"Created attachment {attachment.id} for request {request_record.id} from direct data")

            image_vals = {
                'request_id': request_record.id,
                'storage_identifier': str(attachment.id),
                'storage_type': 'ir.attachment',
                'file_format': image_metadata.get('file_format'),
                'file_size': image_metadata.get('file_size', len(image_content)),
                'width': image_metadata.get('width'),
                'height': image_metadata.get('height'),
                'hash_value': hash_value,
                'retention_category': retention_category,
            }
            generated_image_record = GeneratedImage.sudo().create(image_vals)
            _logger.info(f"Created GeneratedImage record {generated_image_record.id} for request {request_record.id} from direct data")

            attachment.sudo().write({'res_id': generated_image_record.id})
            _logger.info(f"Linked attachment {attachment.id} to GeneratedImage {generated_image_record.id} from direct data")
            return generated_image_record

        except base64.binascii.Error as e:
            _logger.error(f"Base64 decoding error for request {request_record.id}: {e}")
            return None
        except Exception as e:
            _logger.exception(f"Unexpected error storing direct image data for request {request_record.id}:")
            return None


    def _handle_successful_generation(self, request_record, success_data):
        """Handles the successful generation payload from N8N."""
        _logger.info(f"Handling successful generation for request ID: {request_record.id}")
        
        image_url = success_data.get('image_url')
        image_data_b64 = success_data.get('image_data') # Base64 encoded image
        
        generated_image_record = None

        if image_url:
            generated_image_record = self._download_and_store_image(image_url, request_record, success_data)
        elif image_data_b64:
            generated_image_record = self._handle_direct_image_data(image_data_b64, request_record, success_data)
        else:
            _logger.error(f"No image_url or image_data found in success payload for request {request_record.id}")
            request_record.sudo().write({
                'status': 'failed',
                'error_details': _("Image data missing in N8N success callback.")
            })
            return

        if generated_image_record:
            request_record.sudo().write({
                'status': 'completed',
                'generated_image_id': generated_image_record.id,
                'error_details': False # Clear previous errors
            })
            _logger.info(f"Request {request_record.id} marked as completed, linked to image {generated_image_record.id}")
        else:
            request_record.sudo().write({
                'status': 'failed',
                'error_details': _("Image processing/storage failed after successful generation report from N8N.")
            })
            _logger.error(f"Image storage failed for request {request_record.id} despite N8N reporting success.")

    def _handle_failed_generation(self, request_record, error_data):
        """Handles the failed generation payload from N8N."""
        _logger.info(f"Handling failed generation for request ID: {request_record.id}")
        
        error_message = error_data.get('message', _("Unknown error from N8N/AI service."))
        error_details = error_data.get('details', '')
        
        full_error = error_message
        if error_details:
            full_error += f" | Details: {error_details}"
            
        _logger.error(f"AI Generation failed for request {request_record.id}. Error: {full_error}")
        
        request_record.sudo().write({
            'status': 'failed',
            'error_details': full_error
        })

    def process_n8n_callback(self, ai_generation_request_id_str, n8n_payload):
        """
        Processes the callback from N8N containing AI generation results.
        :param ai_generation_request_id_str: str, The ID of the AIImageGenerationRequest record.
        :param n8n_payload: dict, The parsed JSON payload from N8N.
        """
        _logger.info(f"Processing N8N callback for request ID string: {ai_generation_request_id_str}")
        AIImageRequest = self.env['influence_gen.ai_image_request']
        request_record = None

        try:
            try:
                request_id_int = int(ai_generation_request_id_str)
            except ValueError:
                _logger.error(f"Invalid AI Generation Request ID format: {ai_generation_request_id_str}. Expected an integer.")
                # Potentially search by a UUID field if that's the case. For now, assume integer ID.
                # If using UUIDs:
                # request_record = AIImageRequest.sudo().search([('uuid_field_name', '=', ai_generation_request_id_str)], limit=1)
                return

            request_record = AIImageRequest.sudo().browse(request_id_int)

            if not request_record.exists():
                _logger.error(f"AIImageGenerationRequest not found for ID: {request_id_int}")
                return

            if not n8n_payload or 'status' not in n8n_payload:
                _logger.error(f"Invalid N8N payload for request {request_record.id}: Missing 'status' key.")
                self._handle_failed_generation(request_record, {'message': _("Invalid payload from N8N: Missing status.")})
                return

            status = n8n_payload.get('status')
            _logger.info(f"N8N callback status for request {request_record.id}: {status}")

            if status == 'success':
                success_data = n8n_payload.get('data', {})
                self._handle_successful_generation(request_record, success_data)
            elif status == 'failure':
                error_data = n8n_payload.get('error_data', {})
                self._handle_failed_generation(request_record, error_data)
            else:
                _logger.warning(f"Unknown status '{status}' in N8N callback for request {request_record.id}")
                self._handle_failed_generation(request_record, {'message': _(f"Unknown status '{status}' received from N8N.")})

        except Exception as e:
            _logger.exception(f"Error processing N8N callback for request ID string {ai_generation_request_id_str}:")
            if request_record and request_record.exists():
                try:
                    request_record.sudo().write({
                        'status': 'failed',
                        'error_details': _("Internal error processing N8N callback.") + f" Details: {str(e)}"
                    })
                except Exception as write_e:
                    _logger.error(f"Failed to update request record {request_record.id} after callback processing error: {write_e}")
            # Do not re-raise, as this is typically called from a controller that should return a 200 OK to N8N.