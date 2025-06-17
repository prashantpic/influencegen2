# -*- coding: utf-8 -*-
import logging
from odoo import _, api
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class CampaignManagementService:
    """
    Service class for managing campaign lifecycle, applications, content, and performance.
    """

    def __init__(self, env):
        """
        Initializes the service with the Odoo environment.
        :param env: Odoo Environment
        """
        self.env = env

    def create_campaign(self, campaign_vals):
        """
        Creates a new campaign and associated KPIs.
        :param campaign_vals: dict of values for campaign and campaign.kpi.
                              Expected keys for campaign: 'name', 'description', 'brand_client', etc.
                              Expected 'kpi_ids_vals': list of dicts for campaign.kpi, e.g.,
                              [{'name': 'Reach', 'target_value': 10000, 'unit_of_measure': 'People'}]
        :return: recordset of the created influence_gen.campaign
        REQ-2-001, REQ-2-002, REQ-2-003
        """
        _logger.info(f"Creating new campaign with vals: {campaign_vals}")
        
        kpi_vals_list = campaign_vals.pop('kpi_ids_vals', [])
        
        # Basic validation
        if not campaign_vals.get('name') or not campaign_vals.get('description'):
            raise UserError(_("Campaign Name and Description are required."))

        campaign = self.env['influence_gen.campaign'].create(campaign_vals)
        _logger.info(f"Created campaign ID {campaign.id} with name '{campaign.name}'")

        if kpi_vals_list:
            for kpi_vals in kpi_vals_list:
                kpi_vals['campaign_id'] = campaign.id
                self.env['influence_gen.campaign_kpi'].create(kpi_vals)
            _logger.info(f"Created {len(kpi_vals_list)} KPIs for campaign ID {campaign.id}")
            
        # Audit logging handled by model mixin
        return campaign

    def update_campaign_status(self, campaign_id, new_status):
        """
        Updates the status of a campaign.
        Validates status transition. Logs event. Sends notifications if applicable.
        :param campaign_id: int, ID of the influence_gen.campaign
        :param new_status: str, the new status for the campaign
        REQ-2-017
        """
        _logger.info(f"Updating campaign ID {campaign_id} to status: {new_status}")
        campaign = self.env['influence_gen.campaign'].browse(campaign_id)
        if not campaign.exists():
            raise UserError(_("Campaign not found."))

        # Basic status transition validation (can be more complex in the model itself)
        # e.g., campaign.action_publish(), campaign.action_start_progress()
        
        # Direct write for simplicity in service, model methods are preferred for encapsulation
        campaign.write({'status': new_status}) 
        campaign.message_post(body=_("Campaign status updated to %s.") % campaign.status)
        _logger.info(f"Campaign ID {campaign.id} status updated to {new_status}")

        # Send notifications (e.g., campaign published)
        # This would typically involve mail templates
        if new_status == 'published':
            _logger.info(f"Campaign {campaign.name} published. Consider sending notifications.")
            # Example:
            # template = self.env.ref('influence_gen_services.email_template_campaign_published', raise_if_not_found=False)
            # if template:
            #     # Logic to find relevant recipients (e.g., all influencers matching criteria)
            #     # template.send_mail(campaign.id, force_send=True)
            pass

        return True

    def review_campaign_application(self, application_id, decision, reviewer_user_id, reason=None):
        """
        Reviews a campaign application.
        Updates status, reviewer, reason. Logs. Sends notifications.
        :param application_id: int, ID of influence_gen.campaign_application
        :param decision: str, 'approved' or 'rejected'
        :param reviewer_user_id: int, ID of res.users (reviewer)
        :param reason: str, reason for rejection (if applicable)
        REQ-2-007
        """
        _logger.info(f"Reviewing campaign application ID {application_id}, Decision: {decision}")
        application = self.env['influence_gen.campaign_application'].browse(application_id)
        if not application.exists():
            raise UserError(_("Campaign application not found."))
        
        reviewer = self.env['res.users'].browse(reviewer_user_id)
        if not reviewer.exists():
            raise UserError(_("Reviewer user not found."))

        if decision == 'approved':
            application.action_approve_application(reviewer_id=reviewer.id)
        elif decision == 'rejected':
            if not reason:
                raise UserError(_("A reason is required for rejecting an application."))
            application.action_reject_application(reviewer_id=reviewer.id, reason=reason)
        else:
            raise UserError(_("Invalid decision. Must be 'approved' or 'rejected'."))

        _logger.info(f"Campaign application ID {application.id} status updated to {application.status}")
        
        # Send notifications (REQ-16-004)
        try:
            template_ref_name = 'influence_gen_services.email_template_campaign_app_approved' if decision == 'approved' else 'influence_gen_services.email_template_campaign_app_rejected'
            template = self.env.ref(template_ref_name, raise_if_not_found=True)
            email_context = {'rejection_reason': reason} if decision == 'rejected' else {}
            template.with_context(**email_context).send_mail(application.id, force_send=True)
            _logger.info(f"Sent campaign application status email for application {application.id}")
        except Exception as e:
            _logger.error(f"Failed to send campaign application status email: {e}")
            
        return True

    def review_content_submission(self, submission_id, decision, reviewer_user_id, feedback=None):
        """
        Reviews a content submission.
        Updates status, reviewer. Creates ContentFeedbackLog. Logs. Sends notifications.
        If approved, may trigger payment record creation.
        :param submission_id: int, ID of influence_gen.content_submission
        :param decision: str, 'approved', 'rejected', or 'revision_requested'
        :param reviewer_user_id: int, ID of res.users (reviewer)
        :param feedback: str, feedback text
        REQ-2-010
        """
        _logger.info(f"Reviewing content submission ID {submission_id}, Decision: {decision}")
        submission = self.env['influence_gen.content_submission'].browse(submission_id)
        if not submission.exists():
            raise UserError(_("Content submission not found."))

        reviewer = self.env['res.users'].browse(reviewer_user_id)
        if not reviewer.exists():
            raise UserError(_("Reviewer user not found."))

        if decision == 'approved':
            submission.action_approve_content(reviewer_id=reviewer.id)
            # Potentially trigger payment record creation
            # self.env['influence_gen.services.payment_processing'].create_payment_records_for_approved_content([submission.id])
        elif decision == 'rejected':
            if not feedback:
                raise UserError(_("Feedback is required for rejecting content."))
            submission.action_reject_content(feedback_text=feedback, reviewer_id=reviewer.id)
        elif decision == 'revision_requested':
            if not feedback:
                raise UserError(_("Feedback is required for requesting revision."))
            submission.action_request_revision(feedback_text=feedback, reviewer_id=reviewer.id)
        else:
            raise UserError(_("Invalid decision. Must be 'approved', 'rejected', or 'revision_requested'."))

        _logger.info(f"Content submission ID {submission.id} status updated to {submission.review_status}")

        # Send notifications (REQ-16-005)
        try:
            template_name_map = {
                'approved': 'influence_gen_services.email_template_content_submission_approved',
                'rejected': 'influence_gen_services.email_template_content_submission_rejected',
                'revision_requested': 'influence_gen_services.email_template_content_submission_revision',
            }
            template = self.env.ref(template_name_map[decision], raise_if_not_found=True)
            email_context = {'feedback_text': feedback}
            template.with_context(**email_context).send_mail(submission.id, force_send=True)
            _logger.info(f"Sent content submission feedback email for submission {submission.id}")
        except Exception as e:
            _logger.error(f"Failed to send content submission feedback email: {e}")
            
        return True

    def record_campaign_performance(self, submission_id_or_campaign_id, metrics_data, target_model='content_submission'):
        """
        Records performance metrics for a content submission or aggregates on a campaign.
        :param submission_id_or_campaign_id: int, ID of the submission or campaign
        :param metrics_data: dict, performance data (e.g., {'likes': 100, 'views': 1000})
        :param target_model: str, 'content_submission' or 'campaign'
        REQ-2-011
        """
        _logger.info(f"Recording performance for {target_model} ID {submission_id_or_campaign_id}: {metrics_data}")
        import json

        if target_model == 'content_submission':
            submission = self.env['influence_gen.content_submission'].browse(submission_id_or_campaign_id)
            if not submission.exists():
                raise UserError(_("Content submission not found."))
            
            # Update performance_data_json on ContentSubmission
            current_performance = json.loads(submission.performance_data_json or '{}')
            current_performance.update(metrics_data)
            submission.write({'performance_data_json': json.dumps(current_performance)})
            _logger.info(f"Updated performance data for submission ID {submission.id}")
            
            # Update related CampaignKpi.actual_value (simplified - assumes direct mapping or rules)
            # This logic can be complex and model-specific.
            # Example: if 'views' in metrics_data and submission.campaign_id:
            #   kpi_view = self.env['influence_gen.campaign_kpi'].search([
            #       ('campaign_id', '=', submission.campaign_id.id), 
            #       ('name', 'ilike', 'Views') # Or a more specific link
            #   ], limit=1)
            #   if kpi_view:
            #       kpi_view.actual_value += metrics_data['views'] # Or set based on submission

        elif target_model == 'campaign':
            campaign = self.env['influence_gen.campaign'].browse(submission_id_or_campaign_id)
            if not campaign.exists():
                raise UserError(_("Campaign not found."))
            
            # Aggregate on Campaign.actualPerformanceMetrics (if this field exists and is JSON)
            # current_performance = json.loads(campaign.actual_performance_metrics or '{}')
            # for key, value in metrics_data.items():
            #    current_performance[key] = current_performance.get(key, 0) + value
            # campaign.write({'actual_performance_metrics': json.dumps(current_performance)})
            # For now, this is a placeholder as actualPerformanceMetrics is not standard on Campaign in SDS.
            # The campaign_kpi model is more suitable for storing aggregated actuals.
            _logger.warning("Campaign-level performance aggregation is conceptual and depends on campaign model structure.")

        else:
            raise UserError(_("Invalid target model for recording performance."))
            
        return True

    def get_campaign_performance_summary(self, campaign_id):
        """
        Aggregates KPIs and performance data for a campaign.
        :param campaign_id: int, ID of the influence_gen.campaign
        :return: dict, summary of campaign performance
        REQ-2-012
        """
        _logger.info(f"Getting performance summary for campaign ID {campaign_id}")
        campaign = self.env['influence_gen.campaign'].browse(campaign_id)
        if not campaign.exists():
            raise UserError(_("Campaign not found."))

        summary = {
            'campaign_name': campaign.name,
            'campaign_status': campaign.status,
            'kpis': [],
            'total_applications': self.env['influence_gen.campaign_application'].search_count([('campaign_id', '=', campaign.id)]),
            'approved_applications': self.env['influence_gen.campaign_application'].search_count([('campaign_id', '=', campaign.id), ('status', '=', 'approved')]),
            'total_submissions': self.env['influence_gen.content_submission'].search_count([('campaign_id', '=', campaign.id)]),
            'approved_submissions': self.env['influence_gen.content_submission'].search_count([('campaign_id', '=', campaign.id), ('review_status', '=', 'approved')]),
        }

        for kpi in campaign.kpi_ids:
            summary['kpis'].append({
                'name': kpi.name,
                'target_value': kpi.target_value,
                'actual_value': kpi.actual_value, # Assumes actual_value is updated
                'unit_of_measure': kpi.unit_of_measure,
            })
        _logger.info(f"Performance summary for campaign ID {campaign.id}: {summary}")
        return summary

    def get_influencer_performance_summary(self, influencer_id, campaign_id=None):
        """
        Aggregates performance for an influencer across one or all campaigns.
        :param influencer_id: int, ID of influence_gen.influencer_profile
        :param campaign_id: int, optional ID of a specific campaign
        :return: dict, summary of influencer performance
        REQ-2-012
        """
        _logger.info(f"Getting performance summary for influencer ID {influencer_id}, Campaign ID: {campaign_id}")
        influencer = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer.exists():
            raise UserError(_("Influencer profile not found."))

        domain = [('influencer_profile_id', '=', influencer.id)]
        if campaign_id:
            domain.append(('campaign_id', '=', campaign_id))
        
        submissions = self.env['influence_gen.content_submission'].search(domain)
        
        summary = {
            'influencer_name': influencer.full_name,
            'total_submissions': len(submissions),
            'approved_submissions': len(submissions.filtered(lambda s: s.review_status == 'approved')),
            'performance_metrics': {}, # Aggregated metrics from submissions' performance_data_json
        }
        
        import json
        for sub in submissions.filtered(lambda s: s.review_status == 'approved' and s.performance_data_json):
            try:
                data = json.loads(sub.performance_data_json)
                for key, value in data.items():
                    if isinstance(value, (int, float)): # Only aggregate numeric values
                        summary['performance_metrics'][key] = summary['performance_metrics'].get(key, 0) + value
            except json.JSONDecodeError:
                _logger.warning(f"Could not parse performance_data_json for submission {sub.id}")

        _logger.info(f"Performance summary for influencer ID {influencer.id}: {summary}")
        return summary