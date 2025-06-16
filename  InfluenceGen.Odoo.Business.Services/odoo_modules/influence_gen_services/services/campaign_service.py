import logging
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class CampaignService:
    """
    Service class for orchestrating campaign management.
    """

    def __init__(self, env):
        self.env = env

    def create_campaign(self, campaign_data):
        """
        Creates a new campaign.
        REQ-2-001, REQ-2-002, REQ-IPF-003
        """
        _logger.info("Creating campaign with data: %s", campaign_data)
        # Basic validation (model level constraints will also apply)
        if not campaign_data.get('name'):
            raise UserError(_("Campaign name is required."))
        # Add other validations as necessary based on campaign_data structure

        try:
            campaign = self.env['influence_gen.campaign'].create(campaign_data)
            _logger.info("Campaign '%s' (ID: %s) created successfully.", campaign.name, campaign.id)

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='CAMPAIGN_CREATED',
                actor_user_id=self.env.user.id,
                action_performed='CREATE',
                target_object=campaign,
                details_dict={'name': campaign.name}
            )
            return campaign
        except Exception as e:
            _logger.error("Error creating campaign: %s", e)
            raise UserError(_("Could not create campaign: %s") % e)

    def update_campaign_status(self, campaign_id, new_status):
        """
        Updates the status of a campaign.
        """
        _logger.info("Updating status for campaign ID: %s to %s", campaign_id, new_status)
        campaign = self.env['influence_gen.campaign'].browse(campaign_id)
        if not campaign.exists():
            raise UserError(_("Campaign not found."))

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
        # Add other status transitions if defined in campaign model actions
        else:
            # Generic status update if no specific action method exists (less ideal)
            # campaign.write({'status': new_status})
            # self.env['influence_gen.audit_log_entry'].create_log(
            # event_type='CAMPAIGN_STATUS_UPDATED',
            # actor_user_id=self.env.user.id,
            # action_performed='WRITE',
            # target_object=campaign,
            # details_dict={'old_status': campaign.status, 'new_status': new_status}
            # )
            raise UserError(_("Unsupported status transition or status: %s") % new_status)
        
        # Audit log is created within the campaign model's action methods.
        _logger.info("Campaign ID: %s status updated to %s", campaign_id, campaign.status)


    def process_campaign_application(self, influencer_id, campaign_id, proposal_text=None, custom_answers_json=None):
        """
        Processes a campaign application from an influencer.
        """
        _logger.info("Processing campaign application for influencer ID: %s, campaign ID: %s", influencer_id, campaign_id)
        influencer = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer.exists():
            raise UserError(_("Influencer profile not found."))
        if influencer.account_status != 'active':
            raise UserError(_("Influencer account is not active. Cannot apply to campaigns."))

        campaign = self.env['influence_gen.campaign'].browse(campaign_id)
        if not campaign.exists():
            raise UserError(_("Campaign not found."))
        if campaign.status not in ['published', 'open']: # Assuming 'open' is a valid status for applications
            raise UserError(_("This campaign is not currently open for applications."))

        # Validate eligibility (placeholder for more complex rules)
        # e.g., check against campaign.target_influencer_criteria_json

        application_vals = {
            'campaign_id': campaign.id,
            'influencer_profile_id': influencer.id,
            'proposal_text': proposal_text,
            'custom_questions_answers_json': custom_answers_json,
            'status': 'submitted',
        }
        try:
            application = self.env['influence_gen.campaign_application'].create(application_vals)
            _logger.info("Campaign application ID: %s created.", application.id)

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='CAMPAIGN_APPLICATION_SUBMITTED',
                actor_user_id=influencer.user_id.id, # Action by influencer
                action_performed='CREATE',
                target_object=application,
                details_dict={'campaign_id': campaign.id, 'influencer_id': influencer.id}
            )

            # Trigger notifications
            try:
                # To influencer
                self.env['influence_gen.infrastructure.integration.services'].send_notification(
                    recipient_user_ids=[influencer.user_id.id],
                    template_name='campaign_application_submitted_influencer',
                    context={'campaign_name': campaign.name, 'influencer_name': influencer.name}
                )
                # To admin/campaign manager
                # Determine recipient (e.g. campaign creator, specific role)
                # For now, let's assume admins.
                admin_group = self.env.ref('influence_gen_services.group_influence_gen_admin', raise_if_not_found=False)
                campaign_manager_group = self.env.ref('influence_gen_services.group_influence_gen_campaign_manager', raise_if_not_found=False)
                
                notif_recipient_ids = set()
                if admin_group:
                    notif_recipient_ids.update(self.env['res.users'].search([('groups_id', 'in', admin_group.id)]).ids)
                if campaign_manager_group:
                     notif_recipient_ids.update(self.env['res.users'].search([('groups_id', 'in', campaign_manager_group.id)]).ids)

                if notif_recipient_ids:
                    self.env['influence_gen.infrastructure.integration.services'].send_notification(
                        recipient_user_ids=list(notif_recipient_ids),
                        template_name='campaign_application_received_admin',
                        context={'campaign_name': campaign.name, 'influencer_name': influencer.name, 'application_id': application.id}
                    )
            except Exception as e:
                _logger.error("Failed to send campaign application submission notification for app %s: %s", application.id, e)

            return application
        except Exception as e:
            _logger.error("Error processing campaign application: %s", e)
            # Handle unique constraint violation gracefully
            if 'influence_gen_campaign_application_campaign_influencer_uniq' in str(e):
                 raise UserError(_("You have already applied to this campaign."))
            raise UserError(_("Could not process campaign application: %s") % e)

    def review_campaign_application(self, application_id, decision, reviewer_user_id, reason_if_rejected=None):
        """
        Processes the review of a campaign application.
        REQ-2-007
        """
        _logger.info("Reviewing campaign application ID: %s, Decision: %s", application_id, decision)
        application = self.env['influence_gen.campaign_application'].browse(application_id)
        if not application.exists():
            raise UserError(_("Campaign application not found."))
        
        reviewer = self.env['res.users'].browse(reviewer_user_id)
        if not reviewer.exists():
            raise UserError(_("Reviewer user not found."))

        if decision == 'approved':
            application.action_approve(reviewer.id)
        elif decision == 'rejected':
            if not reason_if_rejected:
                raise UserError(_("A reason is required for rejecting an application."))
            application.action_reject(reviewer.id, reason_if_rejected)
        else:
            raise UserError(_("Invalid application review decision: %s") % decision)
        
        # Notifications and audit logs are handled by the model's action methods.
        _logger.info("Campaign application ID: %s status updated to %s", application_id, application.status)

    def handle_content_submission(self, application_id, content_attachments=None, content_link=None, content_caption=None, generated_image_id=None):
        """
        Handles content submission for a campaign application.
        content_attachments is expected to be a list of dicts for ir.attachment creation:
        [{'name': 'file1.jpg', 'datas': 'base64_string1'}, ...]
        """
        _logger.info("Handling content submission for application ID: %s", application_id)
        application = self.env['influence_gen.campaign_application'].browse(application_id)
        if not application.exists():
            raise UserError(_("Campaign application not found."))
        if application.status != 'approved':
            raise UserError(_("Content can only be submitted for approved applications."))

        # Basic validation
        if not (content_attachments or content_link or generated_image_id):
            raise UserError(_("At least one form of content (attachment, link, or AI image) must be provided."))

        submission_vals = {
            'campaign_application_id': application.id,
            'content_link': content_link,
            'content_text_caption': content_caption,
            'generated_image_id': generated_image_id if generated_image_id else False,
            'review_status': 'pending_review',
        }
        
        attachment_ids = []
        if content_attachments:
            for att_data in content_attachments:
                if not att_data.get('datas') or not att_data.get('name'):
                    _logger.warning("Skipping attachment due to missing data or name: %s", att_data.get('name'))
                    continue
                # Max file size check for content could be here, from PlatformSetting
                attachment = self.env['ir.attachment'].create({
                    'name': att_data['name'],
                    'datas': att_data['datas'],
                    'res_model': 'influence_gen.content_submission', # Temp, will be updated
                    'access_token': self.env['ir.attachment']._generate_access_token(),
                })
                attachment_ids.append(attachment.id)
        
        if attachment_ids:
            submission_vals['content_attachment_ids'] = [(6, 0, attachment_ids)]
            
        try:
            submission = self.env['influence_gen.content_submission'].create(submission_vals)
            _logger.info("Content submission ID: %s created.", submission.id)
            
            # Link attachments properly if created
            if attachment_ids:
                self.env['ir.attachment'].browse(attachment_ids).write({'res_id': submission.id})


            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='CONTENT_SUBMITTED',
                actor_user_id=application.influencer_profile_id.user_id.id, # Action by influencer
                action_performed='CREATE',
                target_object=submission,
                details_dict={'application_id': application.id, 'campaign_id': application.campaign_id.id}
            )

            # Trigger notification to admin/campaign manager
            admin_group = self.env.ref('influence_gen_services.group_influence_gen_admin', raise_if_not_found=False)
            campaign_manager_group = self.env.ref('influence_gen_services.group_influence_gen_campaign_manager', raise_if_not_found=False)
            
            notif_recipient_ids = set()
            if admin_group:
                notif_recipient_ids.update(self.env['res.users'].search([('groups_id', 'in', admin_group.id)]).ids)
            if campaign_manager_group:
                 notif_recipient_ids.update(self.env['res.users'].search([('groups_id', 'in', campaign_manager_group.id)]).ids)

            if notif_recipient_ids:
                try:
                    self.env['influence_gen.infrastructure.integration.services'].send_notification(
                        recipient_user_ids=list(notif_recipient_ids),
                        template_name='content_submitted_for_review_admin',
                        context={
                            'campaign_name': application.campaign_id.name,
                            'influencer_name': application.influencer_profile_id.name,
                            'submission_id': submission.id
                        }
                    )
                except Exception as e:
                    _logger.error("Failed to send content submission notification for sub %s: %s", submission.id, e)

            return submission
        except Exception as e:
            _logger.error("Error handling content submission: %s", e)
            raise UserError(_("Could not process content submission: %s") % e)

    def review_content_submission(self, submission_id, decision, reviewer_user_id, feedback_text=None):
        """
        Processes the review of a content submission.
        REQ-2-010 (Corresponds to SEQ-CMP-005)
        """
        _logger.info("Reviewing content submission ID: %s, Decision: %s", submission_id, decision)
        submission = self.env['influence_gen.content_submission'].browse(submission_id)
        if not submission.exists():
            raise UserError(_("Content submission not found."))
            
        reviewer = self.env['res.users'].browse(reviewer_user_id)
        if not reviewer.exists():
            raise UserError(_("Reviewer user not found."))

        if decision == 'approved':
            submission.action_approve(reviewer.id)
             # Potentially trigger payment record creation if final submission approved
            if submission.is_final_submission:
                _logger.info("Final content submission %s approved. Triggering payment consideration.", submission.id)
                try:
                    self.env['influence_gen.payment_service'](self.env).create_payment_record_for_submission(submission.id)
                except Exception as e:
                    _logger.error("Failed to auto-create payment record for submission %s: %s", submission.id, e)
                    # Non-critical to content approval flow, just log.

        elif decision == 'rejected':
            if not feedback_text:
                raise UserError(_("Feedback text is required for rejecting content."))
            submission.action_reject(reviewer.id, feedback_text)
        elif decision == 'revision_requested':
            if not feedback_text:
                raise UserError(_("Feedback text is required for requesting revision."))
            submission.action_request_revision(reviewer.id, feedback_text)
        else:
            raise UserError(_("Invalid content review decision: %s") % decision)
        
        # Notifications and audit logs are handled by the model's action methods.
        _logger.info("Content submission ID: %s review status updated to %s", submission_id, submission.review_status)

    def record_campaign_performance_metrics(self, campaign_id, metrics_data, influencer_id=None, submission_id=None):
        """
        Records (manual) performance metrics for a campaign.
        REQ-2-011
        metrics_data is expected to be a dictionary or JSON string.
        """
        _logger.info("Recording performance metrics for campaign ID: %s", campaign_id)
        campaign = self.env['influence_gen.campaign'].browse(campaign_id)
        if not campaign.exists():
            raise UserError(_("Campaign not found."))

        # The SDS `campaign.add_manual_performance_metric` takes (self, metric_name, metric_value, influencer_id=None, submission_id=None)
        # This service method gets `metrics_data`. We need to adapt.
        # Assuming metrics_data is a dict like {'reach': 10000, 'engagement_rate': 0.05}
        
        # This method in Campaign model is add_manual_performance_metric(self, metric_name, metric_value, influencer_id=None, submission_id=None)
        # The service method receives metrics_data (a dict).
        # We'll assume metrics_data is a dict and campaign.add_manual_performance_metric handles updating the JSON field.
        # For simplicity, let's assume `add_manual_performance_metric` can take the whole dict.
        # If it's one metric at a time, this service needs to iterate.
        # The current campaign.py method in SDS expects metric_name and metric_value.
        # So, the service should iterate if `metrics_data` is a dict of metrics.

        if isinstance(metrics_data, dict):
            for metric_name, metric_value in metrics_data.items():
                campaign.add_manual_performance_metric(
                    metric_name=metric_name,
                    metric_value=metric_value,
                    influencer_id=influencer_id,
                    submission_id=submission_id
                )
        else:
            # If metrics_data is just a single value or needs specific parsing
            # For this example, let's assume it should be a dict.
            raise UserError(_("Metrics data should be a dictionary of metric_name: metric_value pairs."))

        # Audit log is created within the campaign model's method.
        _logger.info("Performance metrics recorded for campaign ID: %s", campaign_id)