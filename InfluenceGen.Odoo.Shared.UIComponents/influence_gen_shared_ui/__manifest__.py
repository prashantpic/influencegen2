# -*- coding: utf-8 -*-
{
    'name': 'InfluenceGen Shared UI Components',
    'version': '18.0.1.0.0',
    'summary': 'Centralized library of reusable UI components for the InfluenceGen platform.',
    'description': """
This module provides a collection of custom, reusable User Interface (UI) components
built using Odoo's Web Library (OWL) and QWeb templates. These components are
intended for use across different InfluenceGen Odoo frontend modules to promote
UI consistency, reduce code duplication, and accelerate frontend development.

Key Features:
- Shared SCSS styling infrastructure (variables, mixins, global styles).
- Shared JavaScript utility functions.
- Reusable OWL components:
    - CampaignCard
    - MetricTile
    - DataChartWrapper
    - LoadingIndicator
    - StatusBadge
    - ProfileSnippet
    """,
    'author': 'SSS-AI',
    'website': 'https://www.example.com', # To be replaced with actual website
    'category': 'InfluenceGen/User Interface',
    'license': 'OEEL-1', # Or other appropriate Odoo license
    'depends': [
        'web', # Core Odoo web framework dependency
    ],
    'data': [
        # No XML views to load directly in 'data' for this type of module typically
        # Security rules or other data files would be listed here if applicable
    ],
    'assets': {
        'web.assets_common': [
            # Shared SCSS (compiled by Odoo's asset pipeline)
            'influence_gen_shared_ui/static/src/scss/shared_variables.scss',
            'influence_gen_shared_ui/static/src/scss/shared_mixins.scss',
            'influence_gen_shared_ui/static/src/scss/shared_global.scss',
            'influence_gen_shared_ui/static/src/scss/components.scss', # This imports all component-specific SCSS
            # Shared JS Utilities
            'influence_gen_shared_ui/static/src/js/utils/ui_helpers.js',
        ],
        'web.assets_backend': [
            # OWL Components for Backend
            # The glob pattern includes all .js and .xml files within the components directory and its subdirectories.
            'influence_gen_shared_ui/static/src/components/**/*.js',
            'influence_gen_shared_ui/static/src/components/**/*.xml',
            # Note: component-specific SCSS is imported via components.scss listed in web.assets_common
        ],
        'web.assets_frontend': [
            # OWL Components for Frontend/Portal
            # The glob pattern includes all .js and .xml files within the components directory and its subdirectories.
            'influence_gen_shared_ui/static/src/components/**/*.js',
            'influence_gen_shared_ui/static/src/components/**/*.xml',
            # Note: component-specific SCSS is imported via components.scss listed in web.assets_common
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}