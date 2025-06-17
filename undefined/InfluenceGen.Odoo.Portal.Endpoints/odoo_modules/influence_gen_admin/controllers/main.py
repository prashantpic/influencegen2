# -*- coding: utf-8 -*-
import json
import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

class InfluenceGenAdminController(http.Controller):

    def _check_admin_access(self):
        """ Helper method to check if the current user is a Platform Administrator. """
        if not request.env.user.has_group('influence_gen_admin.group_influence_gen_platform_admin'):
            raise AccessError("Access denied. You must be a Platform Administrator to perform this action.")

    @http.route('/influence_gen/admin/system_health_data', type='json', auth='user', methods=['POST'], csrf=False)
    def get_system_health_data(self, **kwargs):
        """
        Fetches system health metrics.
        This is a placeholder and needs actual integration with monitoring systems.
        """
        try:
            self._check_admin_access()
        except AccessError as e:
            return {'error': str(e), 'status': 'access_denied'}
        except Exception as e:
            _logger.error(f"Error checking admin access in get_system_health_data: {e}")
            return {'error': 'Internal server error during access check.', 'status': 'error'}

        # Placeholder data - In a real scenario, this would involve:
        # - Querying internal Odoo models for specific metrics
        # - Making API calls to external monitoring systems (e.g., Prometheus, Datadog)
        # - Checking status of dependent services (e.g., N8N, AI service endpoints)
        
        # Example placeholder data structure
        health_data = {
            'api_status': {
                'overall': 'operational', # or 'degraded', 'outage'
                'error_rate_percentage': 0.1, # Example: 0.1%
                'avg_latency_ms': 150, # Example: 150ms
            },
            'n8n_workflow_status': {
                'queue_length': 5, # Example
                'failed_workflows_last_24h': 1, # Example
                'service_status': 'operational',
            },
            'ai_service_status': {
                'image_generation_api': 'operational',
                'model_loading_time_avg_ms': 5000, # Example
            },
            'database_performance': {
                'active_connections': 25,
                'slow_queries_last_hour': 0,
                'db_size_gb': 10.5, # Example
            },
            'server_resources': {
                'odoo_cpu_usage_percentage': 30,
                'odoo_memory_usage_percentage': 60,
                'n8n_cpu_usage_percentage': 20, # If monitored
                'n8n_memory_usage_percentage': 40, # If monitored
            },
            'last_updated': http.request.env['ir.fields.datetime'].now().isoformat(),
        }

        # Simulate fetching or error
        # if some_condition_fails:
        #     _logger.error("Failed to fetch some critical health metric.")
        #     return {'error': 'Failed to retrieve complete health data.', 'status': 'partial_error', 'data': health_data_partial}

        _logger.info("System health data requested by admin.")
        return {'status': 'success', 'data': health_data}

    @http.route('/influence_gen/admin/performance_dashboard_data', type='json', auth='user', methods=['POST'], csrf=False)
    def get_admin_performance_dashboard_data(self, **kwargs):
        """
        Fetches data for the admin performance dashboard.
        This would typically aggregate data from various InfluenceGen models.
        """
        try:
            self._check_admin_access()
        except AccessError as e:
            return {'error': str(e), 'status': 'access_denied'}
        except Exception as e:
            _logger.error(f"Error checking admin access in get_admin_performance_dashboard_data: {e}")
            return {'error': 'Internal server error during access check.', 'status': 'error'}

        # Placeholder logic for fetching data.
        # In a real application, you would query models like:
        # - influence_gen.campaign
        # - influence_gen.campaign_application
        # - influence_gen.content_submission
        # - influence_gen.payment_record
        # - A Materialized View like 'CampaignPerformanceMV' if it exists and is defined in Odoo.
        
        # Example: Number of active campaigns
        active_campaigns = request.env['influence_gen.campaign'].search_count([
            ('status', 'in', ['published', 'open_for_applications', 'in_execution'])
        ])
        
        # Example: Total budget of active campaigns
        active_campaigns_records = request.env['influence_gen.campaign'].search([
            ('status', 'in', ['published', 'open_for_applications', 'in_execution'])
        ])
        total_budget_active = sum(active_campaigns_records.mapped('budget'))
        
        # Example: Total influencers registered (assuming a way to count them, e.g., from influencer_profile)
        total_influencers = request.env['influence_gen.influencer_profile'].search_count([('active','=',True)]) # or based on kyc_status etc.

        # Example: Pending KYC submissions
        pending_kyc = request.env['influence_gen.kyc_data'].search_count([('verification_status', '=', 'pending')])

        # Example: Campaign status distribution
        campaign_statuses = request.env['influence_gen.campaign'].read_group(
            domain=[],
            fields=['status'],
            groupby=['status']
        )
        campaign_status_data = {item['status']: item['status_count'] for item in campaign_statuses}


        dashboard_data = {
            'key_metrics': {
                'active_campaigns': active_campaigns,
                'total_budget_active_campaigns': total_budget_active,
                'total_influencers': total_influencers,
                'pending_kyc_submissions': pending_kyc,
            },
            'campaign_summary': {
                'status_distribution': campaign_status_data,
                # Add more like: campaigns_by_type, top_performing_campaigns (placeholder)
            },
            'influencer_activity': {
                'new_signups_last_30d': 0, # Placeholder
                'active_influencers_in_campaigns': 0, # Placeholder
            },
            'financial_overview': {
                'total_payouts_pending': 0.0, # Placeholder, sum from payment_record
                'total_paid_last_30d': 0.0, # Placeholder
            },
            'last_updated': http.request.env['ir.fields.datetime'].now().isoformat(),
        }
        
        _logger.info("Admin performance dashboard data requested.")
        return {'status': 'success', 'data': dashboard_data}

    # Example of a route that could render a QWeb template for a dashboard component
    # @http.route('/influence_gen/admin/widgets/some_widget', type='http', auth='user', website=False)
    # def render_some_widget(self, **kwargs):
    #     try:
    #         self._check_admin_access()
    #     except AccessError:
    #         return request.make_response("Access Denied", status=403)
    #
    #     widget_data = {'title': 'My Dynamic Widget', 'value': 123} # Fetch actual data
    #     return request.render('influence_gen_admin.qweb_template_for_widget', widget_data)