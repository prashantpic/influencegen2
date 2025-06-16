# -*- coding: utf-8 -*-
import json
import logging

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

class InfluenceGenAdminController(http.Controller):

    def _check_admin_access(self):
        """ Checks if the current user has Platform Administrator rights. """
        if not request.env.user.has_group('influence_gen_admin.group_influence_gen_platform_admin'):
            _logger.warning(
                "Unauthorized access attempt to InfluenceGen Admin controller by user %s (ID: %s)",
                request.env.user.name, request.env.user.id
            )
            raise AccessError("You do not have sufficient rights to access this resource.")

    @http.route('/influence_gen/admin/system_health_data', type='json', auth='user', methods=['POST'], csrf=False)
    def get_system_health_data(self, **kwargs):
        self._check_admin_access()
        # Placeholder logic for fetching system health data
        # In a real scenario, this would involve:
        # 1. Querying internal Odoo models (e.g., cron job statuses, specific queue models if they exist)
        # 2. Making API calls to external monitoring systems (Prometheus, Datadog, N8N API for queue length)
        #    - This requires secure credential management.
        # 3. Aggregating this data.

        _logger.info("Fetching system health data for admin dashboard by user %s", request.env.user.name)

        # Example placeholder data structure
        health_data = {
            'api_error_rate': {'value': 0.02, 'unit': '%', 'status': 'normal'}, # Example: 2% error rate
            'n8n_workflow_main_queue_length': {'value': 5, 'unit': 'items', 'status': 'normal'},
            'n8n_workflow_image_gen_queue_length': {'value': 2, 'unit': 'items', 'status': 'normal'},
            'ai_service_stability_ai': {'name': 'Stability AI', 'status': 'operational', 'last_check': '2023-10-27T10:00:00Z'},
            'ai_service_custom_lora': {'name': 'Custom LoRA Service', 'status': 'degraded_performance', 'last_check': '2023-10-27T09:55:00Z'},
            'odoo_server_cpu_avg_1m': {'value': 15, 'unit': '%', 'status': 'normal'},
            'odoo_server_memory_usage': {'value': 60, 'unit': '%', 'status': 'normal'},
            'odoo_db_active_connections': {'value': 25, 'unit': 'connections', 'status': 'normal'},
            'odoo_db_slow_queries_last_hr': {'value': 3, 'unit': 'queries', 'status': 'warning'},
            'disk_space_app_server_root': {'value': 75, 'unit': '% used', 'status': 'normal'},
            'disk_space_db_server_data': {'value': 85, 'unit': '% used', 'status': 'warning'},
            'failed_cron_jobs_last_24h': {'value': 1, 'unit': 'jobs', 'status': 'warning'},
        }

        # Simulate fetching data, add some dynamic element
        # In a real scenario, you'd integrate with monitoring tools
        # For example, to get N8N queue length, you might call N8N's API if available
        # or check a shared database/queue broker if N8N writes metrics there.
        # For AI service availability, you might ping an endpoint or check a status page.

        return health_data

    @http.route('/influence_gen/admin/performance_dashboard_data', type='json', auth='user', methods=['POST'], csrf=False)
    def get_admin_performance_dashboard_data(self, **kwargs):
        self._check_admin_access()
        _logger.info("Fetching admin performance dashboard data by user %s", request.env.user.name)

        # Fetch data for the admin performance dashboard.
        # This could involve querying:
        # - CampaignPerformanceMV (if it's a model: request.env['influence_gen.campaign.performance.mv'].search_read(...))
        # - Aggregating from influence_gen.campaign, influence_gen.campaign_application, etc.

        # Example: Aggregate campaign statuses
        campaign_obj = request.env['influence_gen.campaign']
        status_counts = campaign_obj.read_group(
            domain=[('active', '=', True)], # Example domain
            fields=['status'],
            groupby=['status'],
            lazy=False
        )
        
        # Example: Total active influencers
        influencer_obj = request.env['influence_gen.influencer_profile']
        active_influencers_count = influencer_obj.search_count([('account_status', '=', 'active')]) # Assuming from SDS

        # Example: Recent KYC approvals
        kyc_data_obj = request.env['influence_gen.kyc_data']
        recent_kyc_approvals = kyc_data_obj.search_count([
            ('verification_status', '=', 'approved'),
            ('reviewed_at', '>=', fields.Datetime.subtract(fields.Datetime.now(), days=7)) # Requires 'fields' import if used
        ])


        # Placeholder data structure
        performance_data = {
            'total_campaigns': campaign_obj.search_count([]),
            'campaign_statuses': [{'status': s['status'], 'count': s['status_count']} for s in status_counts],
            'active_influencers': active_influencers_count,
            'kyc_approvals_last_7_days': recent_kyc_approvals,
            'total_payments_processed_mtd': {'amount': 12500.00, 'currency': 'USD', 'count': 15}, # Example
            'ai_images_generated_mtd': {'count': 1200}, # Example
            # Add more aggregated data as per REQ-2-012
            'aggregated_campaign_performance': [
                {'campaign_name': 'Summer Splash', 'goal_completion': 0.85, 'budget_vs_actual': 0.9},
                {'campaign_name': 'Winter Warmup', 'goal_completion': 0.70, 'budget_vs_actual': 1.1},
            ], # Placeholder
            'influencer_contribution_summary': [
                {'influencer_name': 'Influencer A', 'approved_submissions': 10, 'total_engagement': 5000},
                {'influencer_name': 'Influencer B', 'approved_submissions': 8, 'total_engagement': 4200},
            ] # Placeholder
        }
        return performance_data