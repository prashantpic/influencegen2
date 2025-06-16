{
    'name': 'InfluenceGen Portal',
    'version': '18.0.1.0.0',
    'category': 'InfluenceGen/Portal',
    'summary': 'Influencer facing portal for the InfluenceGen platform.',
    'description': """
Exposes all User Interface (UI) functionalities for influencers.
Includes:
- Influencer Onboarding (Registration, KYC, Social/Bank Accounts, ToS)
- Campaign Management (Discovery, Application, Content Submission)
- AI Image Generation Interface
- Profile Management (Dashboard, Payments, Performance)
""",
    'author': 'SSS-AI',
    'website': 'https://www.example.com', # Replace with actual website
    'depends': [
        'portal',
        'website',
        'mail',
        'influence_gen_business_services', # Assumed name for REPO-IGBS-003
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/influence_gen_portal_security.xml',
        'views/portal_layout_templates.xml',
        'views/portal_dashboard_templates.xml',
        'views/portal_profile_templates.xml',
        'views/portal_onboarding_templates.xml',
        'views/portal_campaign_discovery_templates.xml',
        'views/portal_campaign_details_templates.xml',
        'views/portal_campaign_application_templates.xml',
        'views/portal_content_submission_templates.xml',
        'views/portal_ai_image_generator_templates.xml',
        'views/portal_performance_templates.xml',
        'views/portal_accessibility_snippets.xml',
        'views/portal_error_templates.xml',
        'views/portal_guidance_templates.xml',
        'views/assets.xml', # Asset definitions moved here as per Odoo best practices
        'data/ir_ui_menu_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'influence_gen_portal/static/src/scss/portal_main.scss',
            'influence_gen_portal/static/src/scss/accessibility.scss',
            'influence_gen_portal/static/src/scss/responsive.scss',
            # JS Services
            'influence_gen_portal/static/src/js/services/portal_service.js',
            'influence_gen_portal/static/src/js/services/ai_image_service.js',
            # JS Utilities
            'influence_gen_portal/static/src/js/utils/accessibility_utils.js',
            'influence_gen_portal/static/src/js/utils/localization_utils.js',
            # OWL Components
            'influence_gen_portal/static/src/js/components/abstract_form_component.js',
            'influence_gen_portal/static/src/js/components/file_uploader_component.js',
            'influence_gen_portal/static/src/js/components/ai_image_generator_component.js',
            # Main portal JS file if any orchestrating logic
            'influence_gen_portal/static/src/js/portal_main.js',
        ],
        'web.assets_qweb': [
            'influence_gen_portal/static/src/xml/components/abstract_form_component.xml',
            'influence_gen_portal/static/src/xml/components/file_uploader_component.xml',
            'influence_gen_portal/static/src/xml/components/ai_image_generator_component.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OEEL-1',
}