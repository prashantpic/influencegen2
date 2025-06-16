# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class CampaignService(models.AbstractModel):
    _name = 'influence_gen.campaign.service'
    _description = 'InfluenceGen Campaign Service'

    def __init__(self, env):
        super(CampaignService, self).__init__(env)
        self.env = env

    def create_campaign(self, campaign_data):
        """
        Creates a new campaign. REQ-2-001, REQ-2-002, REQ-IPF-003.
        :param campaign_data: dict of campaign values
        :return: influence_gen.campaign record
        """
        # Add basic validation for required fields if not handled by model itself
        required_fields = ['name', 'start_date', 'end_date', 'compensation_model_type']
        for field in required_fields:
            if not campaign_data.get(field):
                raise UserError(f"Missing required campaign data: {field}")
        
        try:
            campaign = self.env['influence_gen.campaign'].create(campaign_data)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='CAMPAIGN_CREATED',
                actor_user_id=self.env.user.id,
                action_performed='CREATE',
                target_object=campaign,
                details_dict={'name': campaign.name}
            )
            return campaign
        except Exception as e:
            _logger.error(f"Failed to create campaign: {e}")
            raise UserError(f"Could not create campaign: {e}")

    def update_campaign_status(self, campaign_id, new_status):
        """
        Updates the status of a campaign.
        :param campaign_id: ID of the influence_gen.campaign
        :param new_status: string, the new status
        """
        campaign = self.env['influence_gen.campaign'].browse(campaign_id)
        if not campaign.exists():
            raise UserError(f"Campaign with ID {campaign_id} not found.")

        if new_status == 'published':
            campaign.action_publish()
        elif new_status == 'in_progress':
            campaign.action_set_in_progress()
        elif new_status == 'completed':
            campaign.action_complete()
        elif new_status == 'archived':
            campaign.action_archive()
        elif new_status == 'cancelled':
            campaign.action_cancel()
        # Add other status transitions as needed (e.g., draft, pending_review)
        elif new_status == 'draft':
            campaign.write({'status': 'draft'}) # Direct write if no action method
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='CAMPAIGN_STATUS_UPDATED',
                actor_user_id=self.env.user.id,
                action_performed='WRITE',
                target_object=campaign,
                details_dict={'old_status': campaign.status, 'new_status': new_status} # old_status is before write
            )
        elif new_status == 'pending_review':
            campaign.write({'status': 'pending_review'})
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='CAMPAIGN_STATUS_UPDATED',
                actor_user_id=self.env.user.id,
                action_performed='WRITE',
                target_object=campaign,
                details_dict={'old_status': campaign.status, 'new_status': new_status}
            )
        else:
            raise UserError(f"Unsupported status transition: {new_status}")


    def process_campaign_application(self, influencer_id, campaign_id, proposal_text=None, custom_answers_json=None):
        """
        Processes a campaign application from an influencer.
        :param influencer_id: ID of influence_gen.influencer_profile
        :param campaign_id: ID of influence_gen.campaign
        :param proposal_text: string, influencer's proposal
        :param custom_answers_json: string, JSON of answers to custom questions
        :return: influence_gen.campaign_application record
        """
        influencer = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        campaign = self.env['influence_gen.campaign'].browse(campaign_id)

        if not influencer.exists():
            raise UserError(f"Influencer profile with ID {influencer_id} not found.")
        if not campaign.exists():
            raise UserError(f"Campaign with ID {campaign_id} not found.")
        
        if influencer.account_status != 'active':
            raise UserError("Your account must be active to apply for campaigns.")
        if campaign.status not in ['published', 'open']: # Assuming 'open' is a valid status for applications
            raise UserError("This campaign is not currently open for applications.")

        # Check for existing application
        if self.env['influence_gen.campaign_application'].search_count([
            ('influencer_profile_id', '=', influencer.id),
            ('campaign_id', '=', campaign.id)
        ]):
            raise UserError("You have already applied to this campaign.")

        application_vals = {
            'influencer_profile_id': influencer.id,
            'campaign_id': campaign.id,
            'proposal_text': proposal_text,
            'custom_questions_answers_json': custom_answers_json,
            'status': 'submitted',
        }
        try:
            application = self.env['influence_gen.campaign_application'].create(application_vals)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='CAMPAIGN_APPLICATION_SUBMITTED',
                actor_user_id=influencer.user_id.id,
                action_performed='CREATE',
                target_object=application,
                details_dict={'campaign_id': campaign.id, 'influencer_id': influencer.id}
            )

            # Trigger "Application Submitted" notification to influencer
            try:
                self.env['influence_gen.infrastructure.integration.service'].send_notification(
                    recipient_user_ids=[influencer.user_id.id],
                    subject=f"Application Submitted for {campaign.name}",
                    body_html=f"<p>Dear {influencer.name},</p><p>Your application for the campaign '{campaign.name}' has been successfully submitted.</p>"
                )
            except Exception as e:
                _logger.error(f"Failed to send application submitted notification to influencer: {e}")

            # Notify relevant admin/manager (e.g., campaign creator or admin group)
            # This logic can be enhanced, e.g. notify campaign.create_uid or a specific role
            admin_group = self.env.ref('influence_gen_services.group_influence_gen_campaign_manager', raise_if_not_found=False) \
                          or self.env.ref('influence_gen_services.group_influence_gen_admin', raise_if_not_found=False)
            if admin_group:
                admin_users = self.env['res.users'].search([('groups_id', 'in', admin_group.id)])
                if admin_users:
                    try:
                        self.env['influence_gen.infrastructure.integration.service'].send_notification(
                            recipient_user_ids=admin_users.ids,
                            subject=f"New Application for Campaign: {campaign.name}",
                            body_html=f"<p>Influencer {influencer.name} has applied for the campaign '{campaign.name}'.</p>"
                        )
                    except Exception as e:
                        _logger.error(f"Failed to send new application notification to admin/manager: {e}")

            return application
        except Exception as e:
            _logger.error(f"Failed to process campaign application: {e}")
            raise UserError(f"Could not process your application: {e}")


    def review_campaign_application(self, application_id, decision, reviewer_user_id, reason_if_rejected=None):
        """
        Reviews a campaign application. REQ-2-007.
        :param application_id: ID of influence_gen.campaign_application
        :param decision: 'approved' or 'rejected'
        :param reviewer_user_id: ID of res.users (reviewer)
        :param reason_if_rejected: string, reason if decision is 'rejected'
        """
        application = self.env['influence_gen.campaign_application'].browse(application_id)
        if not application.exists():
            raise UserError(f"Campaign Application with ID {application_id} not found.")
        
        reviewer_user = self.env['res.users'].browse(reviewer_user_id)
        if not reviewer_user.exists():
            raise UserError(f"Reviewer user with ID {reviewer_user_id} not found.")

        if decision == 'approved':
            application.action_approve(reviewer_user.id)
        elif decision == 'rejected':
            if not reason_if_rejected:
                raise UserError("Reason for rejection is required.")
            application.action_reject(reviewer_user.id, reason_if_rejected)
        else:
            raise UserError(f"Invalid decision: {decision}. Must be 'approved' or 'rejected'.")

    def handle_content_submission(self, application_id, content_attachments=None, content_link=None, content_caption=None, generated_image_id=None):
        """
        Handles content submission for a campaign application.
        :param application_id: ID of influence_gen.campaign_application
        :param content_attachments: List of dicts for ir.attachment creation, or list of attachment IDs
        :param content_link: string, URL to content
        :param content_caption: string, text/caption for content
        :param generated_image_id: ID of influence_gen.generated_image if applicable
        :return: influence_gen.content_submission record
        """
        application = self.env['influence_gen.campaign_application'].browse(application_id)
        if not application.exists():
            raise UserError(f"Campaign Application with ID {application_id} not found.")
        
        if application.status != 'approved':
            raise UserError("Content can only be submitted for approved applications.")

        if not content_attachments and not content_link and not generated_image_id:
            raise UserError("At least one form of content (attachment, link, or AI image) must be provided.")

        attachment_ids = []
        if content_attachments:
            attachment_model = self.env['ir.attachment']
            for attachment_data in content_attachments:
                if isinstance(attachment_data, int): # If it's already an ID
                    attachment_ids.append(attachment_data)
                elif isinstance(attachment_data, dict) and attachment_data.get('datas'):
                     # Create new attachment
                    vals = {
                        'name': attachment_data.get('name', 'campaign_content'),
                        'datas': attachment_data['datas'],
                        'res_model': 'influence_gen.content_submission', 
                        # res_id will be set later if needed, or keep generic
                    }
                    attachment = attachment_model.create(vals)
                    attachment_ids.append(attachment.id)
                else:
                    _logger.warning(f"Invalid attachment data provided: {attachment_data}")


        submission_vals = {
            'campaign_application_id': application.id,
            'content_link': content_link,
            'content_text_caption': content_caption,
            'generated_image_id': generated_image_id if generated_image_id else False,
            'review_status': 'pending_review',
        }
        if attachment_ids:
            submission_vals['content_attachment_ids'] = [(6, 0, attachment_ids)]

        try:
            submission = self.env['influence_gen.content_submission'].create(submission_vals)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='CONTENT_SUBMITTED',
                actor_user_id=application.influencer_profile_id.user_id.id,
                action_performed='CREATE',
                target_object=submission,
                details_dict={'application_id': application.id, 'campaign_id': application.campaign_id.id}
            )
            # Notify admin
            admin_group = self.env.ref('influence_gen_services.group_influence_gen_campaign_manager', raise_if_not_found=False) \
                          or self.env.ref('influence_gen_services.group_influence_gen_admin', raise_if_not_found=False)
            if admin_group:
                admin_users = self.env['res.users'].search([('groups_id', 'in', admin_group.id)])
                if admin_users:
                    try:
                        self.env['influence_gen.infrastructure.integration.service'].send_notification(
                            recipient_user_ids=admin_users.ids,
                            subject=f"New Content Submitted for {application.campaign_id.name}",
                            body_html=f"<p>Influencer {application.influencer_profile_id.name} has submitted content for the campaign '{application.campaign_id.name}'. Review needed.</p>"
                        )
                    except Exception as e:
                        _logger.error(f"Failed to send content submitted notification to admin: {e}")
            return submission
        except Exception as e:
            _logger.error(f"Failed to handle content submission: {e}")
            raise UserError(f"Could not submit content: {e}")

    def review_content_submission(self, submission_id, decision, reviewer_user_id, feedback_text=None):
        """
        Reviews a content submission. REQ-2-010. Corresponds to SEQ-CMP-005.
        :param submission_id: ID of influence_gen.content_submission
        :param decision: 'approved', 'rejected', or 'revision_requested'
        :param reviewer_user_id: ID of res.users (reviewer)
        :param feedback_text: string, feedback if decision is 'rejected' or 'revision_requested'
        """
        submission = self.env['influence_gen.content_submission'].browse(submission_id)
        if not submission.exists():
            raise UserError(f"Content Submission with ID {submission_id} not found.")

        reviewer_user = self.env['res.users'].browse(reviewer_user_id)
        if not reviewer_user.exists():
            raise UserError(f"Reviewer user with ID {reviewer_user_id} not found.")

        if decision == 'approved':
            submission.action_approve(reviewer_user.id)
        elif decision == 'rejected':
            if not feedback_text:
                raise UserError("Feedback is required for rejecting content.")
            submission.action_reject(reviewer_user.id, feedback_text)
        elif decision == 'revision_requested':
            if not feedback_text:
                raise UserError("Feedback is required for requesting revision.")
            submission.action_request_revision(reviewer_user.id, feedback_text)
        else:
            raise UserError(f"Invalid decision: {decision}. Must be 'approved', 'rejected', or 'revision_requested'.")

    def record_campaign_performance_metrics(self, campaign_id, metrics_data, influencer_id=None, submission_id=None):
        """
        Records manual campaign performance metrics. REQ-2-011.
        :param campaign_id: ID of influence_gen.campaign
        :param metrics_data: dict of metric_name: metric_value
        :param influencer_id: (optional) ID of influence_gen.influencer_profile if metrics are per influencer
        :param submission_id: (optional) ID of influence_gen.content_submission if metrics are per submission
        """
        campaign = self.env['influence_gen.campaign'].browse(campaign_id)
        if not campaign.exists():
            raise UserError(f"Campaign with ID {campaign_id} not found.")

        if not isinstance(metrics_data, dict):
            raise UserError("Metrics data must be a dictionary.")

        # The model method `add_manual_performance_metric` takes individual metric_name, metric_value.
        # This service method could iterate or the model method could be adapted to take a dict.
        # For now, let's assume the model method can be called multiple times or adapted.
        # For simplicity, if model method takes one metric, call it in a loop:
        for metric_name, metric_value in metrics_data.items():
            campaign.add_manual_performance_metric(
                metric_name=metric_name,
                metric_value=metric_value,
                influencer_id=influencer_id,
                submission_id=submission_id
            )
        
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='CAMPAIGN_PERFORMANCE_METRICS_RECORDED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=campaign,
            details_dict={
                'campaign_id': campaign.id, 
                'metrics_data': metrics_data, 
                'influencer_id': influencer_id, 
                'submission_id': submission_id
            }
        )