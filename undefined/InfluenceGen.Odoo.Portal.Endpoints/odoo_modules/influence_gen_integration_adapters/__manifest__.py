# odoo_modules/influence_gen_integration_adapters/__manifest__.py
{
    'name': 'InfluenceGen Integration Adapters',
    'version': '18.0.1.0.0',
    'summary': 'Manages technical communication between Odoo and external systems like N8N and third-party APIs for InfluenceGen.',
    'author': 'SSS-AI',
    'website': 'https://www.example.com', # Replace with actual
    'category': 'InfluenceGen/Integrations',
    'license': 'LGPL-3', # Or appropriate license
    'depends': [
        'base',
        'web',
        'mail', # For logging/notifications if needed directly, or used by business services
        # 'influence_gen_shared_utilities', # Dependency on REPO-IGSCU-007 (if directly used)
        # 'influence_gen_business_services', # If directly invoking service interfaces, or for type hints (if directly used)
    ],
    'data': [
        # No XML views typically in this backend-focused module, unless for config
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}