# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

# REQ-2-012, REQ-PAC-016, REQ-12-007: Admin Dashboard Data Provisioning
class AdminDashboardController(http.Controller):

    @http.route('/influence_gen_admin/dashboard/system_health', type='json', auth='user', methods=['POST'], csrf=False)
    def get_system_health_data(self, **kw):
        """
        Fetches system health metrics.
        This is a placeholder. Actual implementation would call services in REPO-IGBS-003.
        """
        try:
            # Placeholder: Call a service method from influence_gen_services
            # health_data = request.env['influence_gen.system.health.service'].get_health_status()
            health_data = {
                'api_status': 'Operational',
                'ai_service_health': 'Healthy',
                'database_connectivity': 'Connected',
                'queue_depth': 5, # Example metric
            }
            return health_data
        except Exception as e:
            _logger.error("Error fetching system health data: %s", e)
            return {'error': str(e)}

    @http.route('/influence_gen_admin/dashboard/campaign_performance', type='json', auth='user', methods=['POST'], csrf=False)
    def get_campaign_performance_summary(self, **kw):
        """
        Fetches campaign performance summary.
        Queries influence_gen.campaign_performance_mv or calls services.
        """
        try:
            # Placeholder: Call a service or query materialized view
            # performance_data = request.env['influence_gen.campaign.performance.service'].get_summary()
            # Or query the materialized view directly if appropriate for this layer
            # request.env.cr.execute("SELECT * FROM influence_gen_campaign_performance_mv_view LIMIT 10") # Example
            # campaign_performance = request.env.cr.dictfetchall()
            
            # Example Data Structure
            performance_data = {
                'active_campaigns': request.env['influence_gen.campaign'].search_count([('status', 'in', ['published', 'open'])]),
                'completed_campaigns_last_30d': request.env['influence_gen.campaign'].search_count([('status', '=', 'completed'), ('endDate', '>=', fields.Date.subtract(fields.Date.today(), days=30))]),
                'total_applications_pending': request.env['influence_gen.campaign_application'].search_count([('status', '=', 'submitted')]),
                'charts': {
                    'campaigns_by_status': [
                        {'status': 'Draft', 'count': request.env['influence_gen.campaign'].search_count([('status', '=', 'draft')])},
                        {'status': 'Published', 'count': request.env['influence_gen.campaign'].search_count([('status', '=', 'published')])},
                        {'status': 'Open', 'count': request.env['influence_gen.campaign'].search_count([('status', '=', 'open')])},
                        {'status': 'Closed', 'count': request.env['influence_gen.campaign'].search_count([('status', '=', 'closed')])},
                        {'status': 'Completed', 'count': request.env['influence_gen.campaign'].search_count([('status', '=', 'completed')])},
                    ]
                }
            }
            return performance_data
        except Exception as e:
            _logger.error("Error fetching campaign performance summary: %s", e)
            return {'error': str(e)}

    @http.route('/influence_gen_admin/dashboard/ops_log_summary', type='json', auth='user', methods=['POST'], csrf=False)
    def get_operational_log_summary(self, **kw):
        """
        Fetches high-level operational log summaries.
        Placeholder for fetching summaries. Direct integration with centralized logging might be complex.
        """
        try:
            # Placeholder: Call a service or query audit logs
            # log_summary = request.env['influence_gen.operational.log.service'].get_summary()
            log_summary = {
                'recent_errors_count': request.env['influence_gen.audit_log'].search_count([('eventType', 'ilike', '%error%'), ('timestamp', '>=', fields.Datetime.subtract(fields.Datetime.now(), days=1))]),
                'admin_logins_today': request.env['influence_gen.audit_log'].search_count([('eventType', '=', 'user_login'), ('timestamp', '>=', fields.Date.today())]),
                'critical_alerts_active': 0, # Placeholder
            }
            return log_summary
        except Exception as e:
            _logger.error("Error fetching operational log summary: %s", e)
            return {'error': str(e)}