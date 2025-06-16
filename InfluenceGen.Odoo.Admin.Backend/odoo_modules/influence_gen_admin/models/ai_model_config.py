from odoo import api, fields, models

class AiModelConfig(models.Model):
    _name = 'influence_gen.ai_model_config'
    _description = "InfluenceGen AI Model Configuration"

    name = fields.Char(
        required=True,
        string='Model Name'
    )
    description = fields.Text(
        string='Description'
    )
    model_type = fields.Selection(
        selection=[
            ('flux_lora', 'Flux LoRA'),
            ('stable_diffusion_xl', 'Stable Diffusion XL'),
            ('other', 'Other')
        ],
        required=True,
        string='Model Type',
        default='flux_lora'
    )
    trigger_keywords = fields.Char(
        string='Trigger Keywords',
        help="Comma-separated keywords specific to this model/LoRA."
    )
    api_endpoint_info = fields.Char(
        string='API Endpoint/Identifier',
        help="Identifier for N8N/AI service to use this model."
    )
    is_active = fields.Boolean(
        string='Active',
        default=True,
        index=True
    )
    default_params_json = fields.Text(
        string='Default Parameters (JSON)',
        help="JSON string for default parameters like sampler, scheduler if model-specific."
    )