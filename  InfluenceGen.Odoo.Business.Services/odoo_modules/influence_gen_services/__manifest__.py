# -*- coding: utf-8 -*-
{
    'name': 'InfluenceGen Business Services',
    'version': '18.0.1.0.0',
    'summary': 'Core business logic and domain services for the InfluenceGen platform.',
    'author': 'SSS-AI',
    'website': 'https://www.example.com', # Replace with actual website
    'category': 'Services/InfluenceGen',
    'depends': [
        'base',
        'mail',
        'account', # For payment integration
        # 'portal', # if directly extending portal features here - example, not explicitly required by SDS for this module yet
        'influence_gen_infrastructure_integration', # Dependency for REPO-IGOII-004
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/influence_gen_security_groups.xml', # Define security groups if not in a base module
        # Data files for models
        'data/area_of_influence_data.xml',
        'data/platform_setting_data.xml',
        'data/data_retention_policy_data.xml',
        # Wizard views
        'wizards/data_retention_execution_wizard_views.xml',
        'wizards/legal_hold_management_wizard_views.xml',
        # Model views
        'views/influencer_profile_views.xml',
        'views/campaign_views.xml',
        'views/ai_image_model_views.xml',
        'views/platform_setting_views.xml',
        'views/data_retention_policy_views.xml',
        'views/menu_items.xml', # To access admin configurations for this module
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'description': """
This module encapsulates the core business logic for the InfluenceGen platform, including:
- Influencer Onboarding & KYC Processing
- Campaign Management & Lifecycle
- AI Image Generation Request Handling
- Influencer Payment Calculation
- Data Validation and Business Rule Enforcement
- Data Retention and Legal Hold Management
""",
}