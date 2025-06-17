{
    'name': 'InfluenceGen Administration Backend',
    'version': '18.0.1.0.0',
    'summary': 'Administrative backend for the InfluenceGen Platform.',
    'description': """
        Provides all backend User Interface (UI) functionalities for Platform Administrators 
        managing the InfluenceGen system within Odoo. This includes interfaces for:
        - User management (influencers, roles, permissions)
        - Campaign creation and lifecycle management
        - KYC submission review and approval/rejection
        - Content moderation
        - System configuration (AI models, quotas, email templates, business rules)
        - Payment oversight
        - Viewing audit logs and system health dashboards
    """,
    'author': 'SSS-AI',
    'website': 'https://www.example.com', # Replace with actual website
    'category': 'InfluenceGen/Administration',
    'depends': [
        'base',
        'mail',
        'account', # For payment related configurations (e.g., journal selection)
        'influence_gen_services', # REPO-IGBS-003
        # 'influence_gen_shared_ui', # REPO-IGSUC-006 (if backend shared components are used)
        # 'influence_gen_shared_core', # REPO-IGSCU-007 (if utilities are used here)
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/influence_gen_admin_groups.xml',
        # Data
        'data/influence_gen_admin_groups_data.xml', # For module category
        # Wizards
        'wizards/broadcast_notification_wizard_view.xml',
        'wizards/kyc_request_info_wizard_view.xml',
        # Views
        'views/influence_gen_admin_menus.xml',
        'views/platform_config_settings_views.xml',
        'views/user_management_views.xml', # Extensions to Odoo user/group views
        'views/kyc_submission_views.xml',
        'views/campaign_management_views.xml', # Covers campaign, application, submission admin views
        'views/ai_model_config_views.xml',
        'views/ai_usage_tracking_views.xml',
        'views/payment_management_views.xml',
        'views/legal_document_version_views.xml',
        'views/maintenance_window_views.xml',
        'views/legal_hold_management_views.xml',
        'views/audit_log_viewer_views.xml',
        'views/system_health_dashboard_views.xml', # Placeholder, may need controller
        'views/performance_dashboard_views.xml', # Placeholder, may need controller
    ],
    'installable': True,
    'application': True, # If it's a main application entry point
    'auto_install': False,
    'icon': 'influence_gen_admin/static/description/icon.png', # Requires an icon file
    'license': 'LGPL-3', # Or appropriate license
}