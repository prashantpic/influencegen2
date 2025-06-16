# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# REQ-ModuleDefinition: Declares the Odoo module, its properties, dependencies, and data files.
{
    'name': "InfluenceGen Platform Administration",
    'version': "18.0.1.0.0",
    'summary': "Administrative interface for managing the InfluenceGen platform.",
    'author': "SSS-AI",
    'category': "InfluenceGen/Administration",
    'license': "AGPL-3",
    'depends': [
        'base',
        'mail',
        'board', # For dashboards
        'account', # For payment integration aspects
        'influence_gen_services', # Technical name for REPO-IGBS-003
    ],
    'data': [
        # REQ-PAC-001: Security definitions
        'security/influence_gen_security.xml',
        'security/ir.model.access.csv',

        # REQ-UIUX-003, REQ-UIUX-015, REQ-PAC-014: Menu definitions
        'views/influence_gen_admin_menus.xml',

        # Admin Views
        'views/influencer_profile_admin_views.xml', # REQ-IOKYC-011
        'views/kyc_data_admin_views.xml', # REQ-IOKYC-011
        'views/campaign_admin_views.xml', # REQ-2-001, REQ-2-002, REQ-2-003
        'views/campaign_application_admin_views.xml', # REQ-2-007
        'views/content_submission_admin_views.xml', # REQ-2-010
        'views/payment_record_admin_views.xml', # REQ-PAC-015
        'views/audit_log_admin_views.xml', # REQ-PAC-016, REQ-ATEL-008, REQ-UIUX-016
        'views/admin_dashboard_views.xml', # REQ-2-012, REQ-PAC-016, REQ-UIUX-019, REQ-12-007, REQ-PAC-014
        'views/config_settings_views.xml', # REQ-PAC-003, REQ-PAC-007, REQ-AIGS-002, REQ-AIGS-003, REQ-AIGS-004, REQ-PAC-005, REQ-PAC-004, REQ-PAC-009, REQ-PAC-010, REQ-PAC-011, REQ-PAC-015, REQ-PAC-017, REQ-UIUX-022
        'views/ai_model_admin_views.xml', # REQ-AIGS-004, REQ-PAC-005
        'views/ai_prompt_template_admin_views.xml', # REQ-AIGS-003, REQ-PAC-005, REQ-UIUX-021
        'views/ai_moderation_rule_admin_views.xml', # REQ-AIGS-003, REQ-PAC-009
        'views/data_retention_policy_admin_views.xml', # REQ-DRH-008
        'views/legal_hold_admin_views.xml', # REQ-DRH-008, REQ-DRH-009
        'views/alert_rule_admin_views.xml', # REQ-PAC-011
        'views/maintenance_window_admin_views.xml', # REQ-PAC-012
        'views/tos_management_admin_views.xml', # REQ-PAC-006
        'views/ai_usage_log_admin_views.xml', # REQ-AIGS-007

        # Wizard Views
        'wizard/kyc_management_wizard_views.xml', # REQ-IOKYC-011
        'wizard/campaign_management_wizard_views.xml', # REQ-2-007, REQ-2-010

        # Data files
        'data/initial_config_data.xml', # REQ-PAC-001, REQ-PAC-010
    ],
    'assets': {
        'web.assets_backend': [
            'influence_gen_admin/static/src/css/admin_backend_styles.css', # REQ-UIUX-003
            'influence_gen_admin/static/src/js/custom_admin_dashboard.js', # REQ-2-012, REQ-PAC-016, REQ-UIUX-019, REQ-12-007
            'influence_gen_admin/static/src/xml/dashboard_templates.xml', # For OWL components
        ],
    },
    'installable': True,
    'application': True, # Provides a main admin interface for a business application
    'auto_install': False,
}