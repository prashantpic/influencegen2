{
    'name': 'InfluenceGen Core Services',
    'version': '18.0.1.0.0',
    'summary': 'Core business logic, data models, and services for the InfluenceGen platform.',
    'author': 'SSS-AI',
    'website': 'https://www.example.com', # Replace with actual website
    'category': 'Services/InfluenceGen',
    'license': 'AGPL-3', # Or appropriate license
    'depends': [
        'base',
        'mail',       # For mail.thread, mail.activity.mixin, mail.template
        'account',    # For integration with accounting (vendor bills, payments)
        'iap',        # If any Odoo IAP services are planned for use (e.g., for 3rd party integrations)
    ],
    'data': [
        # Security files
        'security/ir.model.access.csv',
        'security/influence_gen_security.xml',
        # Data files
        'data/platform_setting_data.xml',
        'data/mail_template_data.xml',
        'data/scheduled_actions_data.xml',
        # Wizard views (if any are defined directly in XML, otherwise wizard actions)
        # Model views (if any specific backend views are defined in this module, typically minimal for a service module)
    ],
    'installable': True,
    'application': False, # This is a backend services module, not a standalone application
    'auto_install': False,
    'description': """
Core backend business logic and service operations for the InfluenceGen platform.
This module includes:
- Data models for Influencer Profiles, Campaigns, KYC, AI Image Generation, Payments.
- Business rules for onboarding, campaign management, AI integration, and payments.
- Service layer for orchestrating complex operations.
    """,
}