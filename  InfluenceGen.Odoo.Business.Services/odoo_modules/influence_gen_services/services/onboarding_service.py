# -*- coding: utf-8 -*-
import logging
import json
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class OnboardingService(models.AbstractModel):
    _name = 'influence_gen.onboarding.service'
    _description = 'InfluenceGen Onboarding Service'

    def __init__(self, env):
        super(OnboardingService, self).__init__(env)
        self.env = env

    def process_registration_submission(self, influencer_data):
        """
        Processes influencer registration submission. REQ-IOKYC-002.
        :param influencer_data: dict containing influencer details
            (fullName, email, phone, residentialAddress, socialMediaProfiles (list of dicts))
        :return: influence_gen.influencer_profile record
        """
        if not influencer_data.get('email') or not influencer_data.get('fullName'):
            raise UserError("Full Name and Email are required for registration.")

        # Basic email format validation
        if not fields.Char.mail_validate(influencer_data['email']):
            raise UserError("Invalid email format.")

        # Check for existing user by email
        user_model = self.env['res.users']
        user = user_model.search([('login', '=', influencer_data['email'])], limit=1)
        if not user:
            user_vals = {
                'name': influencer_data['fullName'],
                'login': influencer_data['email'],
                'email': influencer_data['email'],
                'sel_groups_1_9_10': self.env.ref('base.group_portal').id, # Add to portal group
                # Ensure user is inactive until profile fully set up or email verified
                'active': True, # Or False, depending on desired flow
            }
            try:
                user = user_model.create(user_vals)
                _logger.info(f"Created new user for {influencer_data['email']}")
            except Exception as e:
                _logger.error(f"Failed to create user for {influencer_data['email']}: {e}")
                raise UserError(f"Could not create user account: {e}")
        else:
             # Check if this user is already linked to an influencer profile
            if self.env['influence_gen.influencer_profile'].search_count([('user_id', '=', user.id)]):
                raise UserError("An influencer profile already exists for this email address.")


        influencer_profile_model = self.env['influence_gen.influencer_profile']
        profile_vals = {
            'name': influencer_data['fullName'],
            'user_id': user.id,
            'email': influencer_data['email'],
            'phone': influencer_data.get('phone'),
            'residential_address': influencer_data.get('residentialAddress'),
            'kyc_status': 'pending',
            'account_status': 'inactive', # Starts as inactive
            'onboarding_checklist_json': json.dumps({
                'profile_created': True,
                'kyc_submitted': False,
                'bank_submitted': False,
                'tos_agreed': False,
                'social_media_verified': False
            })
        }
        
        try:
            influencer_profile = influencer_profile_model.create(profile_vals)
        except Exception as e:
            # If user was newly created and profile creation fails, consider deactivating/removing user
            _logger.error(f"Failed to create influencer profile for {user.login}: {e}")
            raise UserError(f"Could not create influencer profile: {e}")

        social_media_profiles_data = influencer_data.get('socialMediaProfiles', [])
        social_media_profile_model = self.env['influence_gen.social_media_profile']
        for sm_data in social_media_profiles_data:
            if sm_data.get('platform') and sm_data.get('handle'):
                try:
                    social_media_profile_model.create({
                        'influencer_profile_id': influencer_profile.id,
                        'platform': sm_data['platform'],
                        'handle': sm_data['handle'],
                        'url': sm_data.get('url'),
                        'verification_status': 'pending',
                    })
                except Exception as e:
                    _logger.warning(f"Could not create social media profile {sm_data['handle']} for {influencer_profile.name}: {e}")
                    # Decide if this should be a critical error or just a warning

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='INFLUENCER_REGISTRATION',
            actor_user_id=self.env.user.id, # or system user if automated
            action_performed='CREATE',
            target_object=influencer_profile,
            details_dict={'email': influencer_profile.email, 'user_id': user.id}
        )

        # Trigger "Registration Received" notification
        try:
            self.env['influence_gen.infrastructure.integration.service'].send_notification(
                recipient_user_ids=[user.id],
                template_ref='influence_gen_services.email_template_registration_received', # Placeholder
                subject='InfluenceGen Registration Received',
                body_html=f"<p>Dear {influencer_profile.name},</p><p>Your registration for InfluenceGen has been received. We will guide you through the next steps.</p>"
            )
        except Exception as e:
            _logger.error(f"Failed to send registration received notification: {e}")

        return influencer_profile

    def handle_kyc_document_submission(self, influencer_id, document_type, front_attachment_data, back_attachment_data=None, verification_method='manual'):
        """
        Handles KYC document submission. REQ-IOKYC-005.
        :param influencer_id: ID of the influence_gen.influencer_profile
        :param document_type: e.g., 'passport', 'driver_license'
        :param front_attachment_data: dict for ir.attachment creation (name, datas, mimetype) or binary data
        :param back_attachment_data: dict for ir.attachment creation or binary data (optional)
        :param verification_method: e.g., 'manual', 'third_party_api'
        :return: influence_gen.kyc_data record
        """
        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            raise UserError(f"Influencer profile with ID {influencer_id} not found.")

        attachment_model = self.env['ir.attachment']
        
        front_attach_vals = {
            'name': front_attachment_data.get('name', f"{document_type}_front_{influencer_profile.name}"),
            'datas': front_attachment_data.get('datas'), # Expects base64 encoded string
            'res_model': 'influence_gen.kyc_data',
            # res_id will be set later if needed, or keep it generic
        }
        front_attachment = attachment_model.create(front_attach_vals)

        back_attachment = None
        if back_attachment_data and back_attachment_data.get('datas'):
            back_attach_vals = {
                'name': back_attachment_data.get('name', f"{document_type}_back_{influencer_profile.name}"),
                'datas': back_attachment_data.get('datas'),
                'res_model': 'influence_gen.kyc_data',
            }
            back_attachment = attachment_model.create(back_attach_vals)

        kyc_data_vals = {
            'influencer_profile_id': influencer_profile.id,
            'document_type': document_type,
            'document_front_attachment_id': front_attachment.id,
            'document_back_attachment_id': back_attachment.id if back_attachment else False,
            'verification_method': verification_method,
            'verification_status': 'pending', # Default from model, can be explicit
        }
        kyc_data_record = self.env['influence_gen.kyc_data'].create(kyc_data_vals)
        kyc_data_record.action_submit_for_review() # This should set status to in_review

        influencer_profile.update_onboarding_step_status('kyc_submitted', True)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_DOCUMENT_SUBMITTED',
            actor_user_id=influencer_profile.user_id.id,
            action_performed='CREATE',
            target_object=kyc_data_record,
            details_dict={'influencer_id': influencer_id, 'document_type': document_type}
        )

        # Notification "KYC Documents Received" to influencer
        try:
            self.env['influence_gen.infrastructure.integration.service'].send_notification(
                recipient_user_ids=[influencer_profile.user_id.id],
                template_ref='influence_gen_services.email_template_kyc_docs_received', # Placeholder
                subject='KYC Documents Received',
                body_html=f"<p>Dear {influencer_profile.name},</p><p>We have received your KYC documents. They are now under review.</p>"
            )
        except Exception as e:
            _logger.error(f"Failed to send KYC docs received notification to influencer: {e}")

        # Notification "KYC Awaiting Review" to admins
        admin_group = self.env.ref('influence_gen_services.group_influence_gen_admin', raise_if_not_found=False)
        if admin_group:
            admin_users = self.env['res.users'].search([('groups_id', 'in', admin_group.id)])
            if admin_users:
                try:
                    self.env['influence_gen.infrastructure.integration.service'].send_notification(
                        recipient_user_ids=admin_users.ids,
                        template_ref='influence_gen_services.email_template_kyc_awaiting_review_admin', # Placeholder
                        subject='New KYC Submission Awaiting Review',
                        body_html=f"<p>A new KYC submission from {influencer_profile.name} (ID: {influencer_profile.id}) is awaiting review.</p>"
                    )
                except Exception as e:
                    _logger.error(f"Failed to send KYC awaiting review notification to admins: {e}")
            else:
                _logger.warning("No admin users found to notify for KYC review.")
        else:
            _logger.warning("Admin security group 'group_influence_gen_admin' not found.")


        return kyc_data_record

    def handle_kyc_review_decision(self, kyc_data_id, decision, reviewer_user_id, notes=None, reason_if_rejected=None, info_needed_if_more_info=None):
        """ Handles KYC review decision. REQ-IOKYC-005. """
        kyc_data_record = self.env['influence_gen.kyc_data'].browse(kyc_data_id)
        if not kyc_data_record.exists():
            raise UserError(f"KYC Data record with ID {kyc_data_id} not found.")
        
        reviewer_user = self.env['res.users'].browse(reviewer_user_id)
        if not reviewer_user.exists():
            raise UserError(f"Reviewer user with ID {reviewer_user_id} not found.")

        influencer_profile = kyc_data_record.influencer_profile_id
        notification_subject = ""
        notification_body = ""

        if decision == 'approved':
            kyc_data_record.action_approve(reviewer_user.id, notes=notes)
            notification_subject = "KYC Approved"
            notification_body = f"<p>Dear {influencer_profile.name},</p><p>Your KYC verification has been approved.</p>"
        elif decision == 'rejected':
            if not reason_if_rejected:
                raise UserError("Reason for rejection is required.")
            kyc_data_record.action_reject(reviewer_user.id, reason_if_rejected)
            notification_subject = "KYC Rejected"
            notification_body = f"<p>Dear {influencer_profile.name},</p><p>Your KYC verification has been rejected. Reason: {reason_if_rejected}.</p>"
            if notes:
                 notification_body += f"<p>Additional notes: {notes}</p>"
        elif decision == 'needs_more_info':
            if not info_needed_if_more_info:
                raise UserError("Details of information needed are required.")
            kyc_data_record.action_request_more_info(reviewer_user.id, info_needed_if_more_info)
            notification_subject = "KYC - More Information Required"
            notification_body = f"<p>Dear {influencer_profile.name},</p><p>We require more information for your KYC verification: {info_needed_if_more_info}.</p>"
            if notes:
                 notification_body += f"<p>Additional notes: {notes}</p>"
        else:
            raise UserError(f"Invalid decision: {decision}")

        # Trigger notification to influencer
        if influencer_profile.user_id:
            try:
                self.env['influence_gen.infrastructure.integration.service'].send_notification(
                    recipient_user_ids=[influencer_profile.user_id.id],
                    subject=notification_subject,
                    body_html=notification_body # Ideally use a template
                )
            except Exception as e:
                _logger.error(f"Failed to send KYC decision notification to {influencer_profile.name}: {e}")

        # Attempt to activate account if KYC approved
        if decision == 'approved':
            self.check_and_activate_influencer_account(influencer_profile.id)


    def initiate_social_media_verification(self, social_profile_id, method):
        """ Initiates social media verification. REQ-IOKYC-006. """
        social_profile = self.env['influence_gen.social_media_profile'].browse(social_profile_id)
        if not social_profile.exists():
            raise UserError(f"Social Media Profile with ID {social_profile_id} not found.")

        verification_details = social_profile.action_initiate_verification(method)
        
        influencer_profile = social_profile.influencer_profile_id
        if method == 'code_in_bio' and verification_details and verification_details.get('code'):
            # Trigger notification to influencer with instructions
            try:
                self.env['influence_gen.infrastructure.integration.service'].send_notification(
                    recipient_user_ids=[influencer_profile.user_id.id],
                    subject=f"Verify your {social_profile.platform} Account",
                    body_html=f"<p>Dear {influencer_profile.name},</p><p>To verify your {social_profile.platform} account ({social_profile.handle}), please place the following code in your bio/a new post: <strong>{verification_details['code']}</strong></p>"
                )
            except Exception as e:
                _logger.error(f"Failed to send social media verification instructions: {e}")
        
        return verification_details

    def confirm_social_media_verification(self, social_profile_id, verification_input=None):
        """ Confirms social media verification. REQ-IOKYC-006. """
        social_profile = self.env['influence_gen.social_media_profile'].browse(social_profile_id)
        if not social_profile.exists():
            raise UserError(f"Social Media Profile with ID {social_profile_id} not found.")

        success = social_profile.action_confirm_verification(verification_input=verification_input)
        influencer_profile = social_profile.influencer_profile_id

        if success:
            try:
                self.env['influence_gen.infrastructure.integration.service'].send_notification(
                    recipient_user_ids=[influencer_profile.user_id.id],
                    subject=f"{social_profile.platform} Account Verified",
                    body_html=f"<p>Dear {influencer_profile.name},</p><p>Your {social_profile.platform} account ({social_profile.handle}) has been successfully verified.</p>"
                )
            except Exception as e:
                _logger.error(f"Failed to send social media verification success notification: {e}")
            self.check_and_activate_influencer_account(influencer_profile.id)
        else:
            try:
                self.env['influence_gen.infrastructure.integration.service'].send_notification(
                    recipient_user_ids=[influencer_profile.user_id.id],
                    subject=f"{social_profile.platform} Account Verification Failed",
                    body_html=f"<p>Dear {influencer_profile.name},</p><p>Verification for your {social_profile.platform} account ({social_profile.handle}) failed. Please try again or contact support.</p>"
                )
            except Exception as e:
                _logger.error(f"Failed to send social media verification failure notification: {e}")
        return success

    def initiate_bank_account_verification(self, bank_account_id, method):
        """ Initiates bank account verification. REQ-IOKYC-008. """
        bank_account = self.env['influence_gen.bank_account'].browse(bank_account_id)
        if not bank_account.exists():
            raise UserError(f"Bank Account with ID {bank_account_id} not found.")
        
        verification_details = bank_account.action_initiate_verification(method)
        influencer_profile = bank_account.influencer_profile_id

        # Example notification for micro-deposit
        if method == 'micro_deposit':
            try:
                self.env['influence_gen.infrastructure.integration.service'].send_notification(
                    recipient_user_ids=[influencer_profile.user_id.id],
                    subject="Bank Account Verification Initiated",
                    body_html=f"<p>Dear {influencer_profile.name},</p><p>We have initiated micro-deposit verification for your bank account ending in ... (get last 4 digits if possible and unencrypted). Please check your account in 1-2 business days for two small deposits and enter them on our platform to complete verification.</p>"
                )
            except Exception as e:
                _logger.error(f"Failed to send bank account micro-deposit instructions: {e}")

        return verification_details

    def confirm_bank_account_verification(self, bank_account_id, verification_input=None):
        """ Confirms bank account verification. REQ-IOKYC-008. """
        bank_account = self.env['influence_gen.bank_account'].browse(bank_account_id)
        if not bank_account.exists():
            raise UserError(f"Bank Account with ID {bank_account_id} not found.")

        success = bank_account.action_confirm_verification(verification_input=verification_input)
        influencer_profile = bank_account.influencer_profile_id

        if success:
            try:
                self.env['influence_gen.infrastructure.integration.service'].send_notification(
                    recipient_user_ids=[influencer_profile.user_id.id],
                    subject="Bank Account Verified",
                    body_html=f"<p>Dear {influencer_profile.name},</p><p>Your bank account has been successfully verified.</p>"
                )
            except Exception as e:
                _logger.error(f"Failed to send bank account verification success notification: {e}")
            self.check_and_activate_influencer_account(influencer_profile.id)
        else:
            try:
                self.env['influence_gen.infrastructure.integration.service'].send_notification(
                    recipient_user_ids=[influencer_profile.user_id.id],
                    subject="Bank Account Verification Failed",
                    body_html=f"<p>Dear {influencer_profile.name},</p><p>Verification for your bank account failed. Please check the details and try again, or contact support.</p>"
                )
            except Exception as e:
                _logger.error(f"Failed to send bank account verification failure notification: {e}")
        return success

    def record_terms_consent(self, influencer_id, tos_version, privacy_policy_version, ip_address=None):
        """ Records terms consent. REQ-IOKYC-009. """
        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            raise UserError(f"Influencer profile with ID {influencer_id} not found.")

        # Potentially fetch current versions from PlatformSetting if not passed
        # tos_version = tos_version or self.env['influence_gen.platform_setting'].get_param('influence_gen.default_tos_version')
        # privacy_policy_version = privacy_policy_version or self.env['influence_gen.platform_setting'].get_param('influence_gen.default_privacy_policy_version')

        if not tos_version or not privacy_policy_version:
            raise UserError("Terms of Service version and Privacy Policy version are required.")

        consent = self.env['influence_gen.terms_consent'].create_consent(
            influencer_id=influencer_profile.id,
            tos_version=tos_version,
            privacy_policy_version=privacy_policy_version,
            ip_address=ip_address
        )
        if consent:
             self.check_and_activate_influencer_account(influencer_profile.id)
        return consent


    def check_and_activate_influencer_account(self, influencer_id):
        """ Checks onboarding completion and activates account if all criteria met. REQ-IOKYC-012. """
        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            _logger.warning(f"Attempted to check/activate non-existent influencer ID {influencer_id}")
            return False
        
        if influencer_profile.account_status == 'active':
            _logger.info(f"Account for {influencer_profile.name} is already active.")
            return True

        if influencer_profile.check_onboarding_completion():
            return influencer_profile.action_activate_account()
        else:
            _logger.info(f"Onboarding not yet complete for {influencer_profile.name}. Account not activated.")
            return False