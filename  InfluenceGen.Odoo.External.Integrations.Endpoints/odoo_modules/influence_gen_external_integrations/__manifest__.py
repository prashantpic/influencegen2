# -*- coding: utf-8 -*-
{
    'name': 'InfluenceGen External Integrations',
    'version': '18.0.1.0.0',
    'summary': 'Handles integrations with external KYC, bank verification, and payment services for InfluenceGen.',
    'author': 'SSS-AI',
    'website': 'https://www.example.com', # Replace with actual website
    'category': 'InfluenceGen/Integrations',
    'depends': [
        'base',         # Core Odoo dependency
        'account',      # For Odoo Accounting integration (REQ-IPF-006)
        # Add other InfluenceGen core module dependencies if services are directly called by them
        # e.g., 'influence_gen_core' if it exists and calls these services.
    ],
    'data': [
        # Security files if any specific models are created for secure config
        # 'security/ir.model.access.csv',
        # Data files (e.g., for default configurations, although ir.config_parameter is preferred for settings)
    ],
    'installable': True,
    'application': False, # This is a supporting module, not a standalone application
    'auto_install': False,
    'license': 'LGPL-3', # Or appropriate license
}