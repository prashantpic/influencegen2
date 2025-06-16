# -*- coding: utf-8 -*-
{
    'name': 'InfluenceGen AI Integration Endpoints',
    'version': '18.0.1.0.0',
    'summary': 'Manages Odoo-side integration with N8N for AI image generation.',
    'author': 'SSS-AI',
    'website': 'https_your_company_website.com', # Replace with actual
    'category': 'InfluenceGen/Integrations',
    'license': 'AGPL-3', # Or your chosen license
    'depends': [
        'base',
        'web',
        'mail',
        'influence_gen_base_models', # Defines AIImageGenerationRequest, GeneratedImage etc.
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/data/ir_config_parameter_data.xml',
    ],
    'installable': True,
    'application': False, # This is a technical/connector module
    'auto_install': False,
}