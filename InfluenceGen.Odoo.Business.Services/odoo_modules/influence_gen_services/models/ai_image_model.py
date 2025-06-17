# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AiImageModel(models.Model):
    """
    AI Image Generation Model
    Represents an AI image generation model that can be selected by users.
    This model defines and manages the list of AI image generation models
    (e.g., Flux LoRA models) available to users.
    Managed by Platform Administrators. Inherits from BaseAuditMixin.
    REQ-DMG-007, REQ-AIGS-004
    """
    _name = 'influence_gen.ai_image_model'
    _description = 'AI Image Generation Model'
    _inherit = ['influence_gen.base_audit_mixin']
    _order = 'name'

    name = fields.Char(
        string='Name', 
        required=True, 
        index=True,
        help="Unique and descriptive name of the AI model (e.g., 'Stable Diffusion XL', 'Flux Style A LoRA')."
    )
    description = fields.Text(
        string='Description',
        help="Detailed description of the AI model, its capabilities, and typical use cases."
    )
    trigger_keywords = fields.Char(
        string='Trigger Keywords', 
        help="Comma-separated keywords that might be associated with this model or used to invoke it (e.g., for specific styles or LoRAs)."
    )
    is_active = fields.Boolean(
        string='Active', 
        default=True, 
        index=True,
        help="Indicates if the model is currently active and available for users to select for generation."
    )
    external_model_id = fields.Char(
        string='External Model ID', 
        help="Identifier used by the external AI service or API (e.g., N8N workflow parameter, specific model name in an AI backend)."
    )
    parameters_template_json = fields.Text(
        string='Default Parameters (JSON)',
        help="A JSON string defining default parameters or a template for this model, "
             "e.g., default resolution, steps, CFG scale. This can guide UI or API calls."
    )
    notes = fields.Text(
        string="Internal Notes",
        help="Any internal notes or configuration details for administrators regarding this model."
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The AI model name must be unique.')
    ]

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name