# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class InfluenceGenAiImageModel(models.Model):
    _name = 'influence_gen.ai_image_model'
    _description = "AI Image Generation Model Configuration"

    name = fields.Char(string="Model Name", required=True, unique=True, index=True)
    description = fields.Text(string="Description")
    trigger_keywords = fields.Char(
        string="Trigger Keywords (comma-separated)",
        help="Keywords that may be used to identify or suggest this model."
    )
    is_active = fields.Boolean(string="Active", default=True, index=True)
    external_model_id = fields.Char(
        string="External Model ID (for AI Service)",
        help="Identifier used by the external AI generation service (e.g., N8N workflow or specific API model ID)."
    )
    notes = fields.Text(string="Internal Notes")

    # Example of how an admin might set this up via UI:
    # They would create records of this model.
    # The `AIImageService` would then use these records.

    # No specific methods defined in SDS for this model, mainly data storage for configuration.
    # CRUD operations handled by Odoo framework or by AIImageService methods.