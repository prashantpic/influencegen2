# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class InfluenceGenAiImageModel(models.Model):
    _name = 'influence_gen.ai_image_model'
    _description = "AI Image Generation Model Configuration"

    name = fields.Char(string="Model Name", required=True, unique=True, index=True)
    description = fields.Text(string="Description")
    trigger_keywords = fields.Char(
        string="Trigger Keywords (comma-separated)",
        help="Keywords that might suggest using this model."
    )
    is_active = fields.Boolean(string="Active", default=True, index=True)
    external_model_id = fields.Char(
        string="External Model ID (for AI Service)",
        help="Identifier used by the underlying AI generation service (e.g., N8N workflow or specific API)."
    )
    notes = fields.Text(string="Internal Notes")

    # No specific methods defined in SDS for this model beyond standard CRUD
    # and being used by AIImageGenerationRequest and AIImageService.