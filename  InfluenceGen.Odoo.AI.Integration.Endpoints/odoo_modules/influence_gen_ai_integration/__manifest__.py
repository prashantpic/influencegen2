# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'InfluenceGen AI Integration Endpoints',
    'version': '18.0.1.0.0',
    'summary': 'Manages Odoo-side integration with N8N for AI image generation.',
    'author': 'SSS-AI',
    'website': 'https://www.example.com', # Replace with actual
    'category': 'InfluenceGen/Integrations',
    'license': 'AGPL-3', # Or your chosen license
    'depends': [
        'base',
        'web',
        'mail', # For potential notifications on success/failure
        # Add dependency to the module defining AIImageGenerationRequest, GeneratedImage, etc.
        # e.g., 'influence_gen_base_models' (REPO-IGBM-002)
        # This dependency ensures that the models this module interacts with are loaded.
        'influence_gen_base_models', 
    ],
    'data': [
        'security/ir.model.access.csv', # If new models are defined here or for service access
        'security/data/ir_config_parameter_data.xml',
        # Add views if any specific backend configurations are managed through UI
    ],
    'installable': True,
    'application': False, # This is likely a technical/connector module
    'auto_install': False,
}