from odoo import models, fields, api, _

class InfluenceGenAiImageModel(models.Model):
    _name = 'influence_gen.ai_image_model'
    _description = "AI Image Generation Model Configuration"

    name = fields.Char(string="Model Name", required=True, unique=True, index=True)
    description = fields.Text(string="Description")
    trigger_keywords = fields.Char(string="Trigger Keywords (comma-separated)", help="Keywords that might suggest using this model.")
    is_active = fields.Boolean(string="Active", default=True, index=True)
    external_model_id = fields.Char(string="External Model ID (for AI Service)", help="Identifier used by the underlying AI generation service/API.")
    notes = fields.Text(string="Internal Notes")

    # Add SQL constraint for name uniqueness if not implicitly handled by unique=True
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'AI Image Model name must be unique!')
    ]