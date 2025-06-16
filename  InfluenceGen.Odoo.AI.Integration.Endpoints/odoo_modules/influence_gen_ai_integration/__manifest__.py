# -*- coding: utf-8 -*-
{
    'name': 'InfluenceGen AI Integration Endpoints',
    'version': '18.0.1.0.0',
    'summary': 'Manages Odoo-side integration with N8N for AI image generation.',
    'author': 'SSS-AI',
    'website': 'https://your_company_website.com',
    'category': 'InfluenceGen/Integrations',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
        'influence_gen_base_models',
    ],
    'data': [
        'security/data/ir_config_parameter_data.xml',
        # 'security/ir.model.access.csv', # Add if new models with UI access are defined
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}