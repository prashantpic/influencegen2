import logging
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class OnboardingService:
    """
    Service class for orchestrating the influencer onboarding process.
    """

    def __init__(self, env):
        self.env = env

    def process_registration_submission(self, influencer_data):
        """
        Processes influencer registration data, creates user and profile.
        REQ-IOKYC-002
        """
        _logger.info("Processing registration submission for: %s", influencer_data.get('email'))
        # 1. Validate influencer_data (required fields, formats)
        required_fields = ['fullName', 'email'] # Add other required fields from UI/contract
        for field in required_fields:
            if not influencer_data.get(field):
                raise UserError(_("Missing required field: %s") % field)

        # Basic email format validation (more robust in InfluencerProfile model)
        if not self.env['mail.thread']._mail_check_html_encoding(influencer_data.get('email')):
             raise UserError(_("Invalid email format for: %s") % influencer_data.get('email'))

        # Check for existing user/influencer profile by email
        existing_profile = self.env['influence_gen.influencer_profile'].search([('email', '=', influencer_data['email'])], limit=1)
        if existing_profile:
            raise UserError(_("An influencer profile with this email already exists: %s") % influencer_data['email'])
        
        existing_user_by_email = self.env['res.users'].search([('login', '=', influencer_data['email'])], limit=1)
        if existing_user_by_email and not influencer_data.get('user_id'): # if user_id not provided but email exists
             _logger.warning("A user with email %s already exists. Attempting to link.", influencer_data['email'])
             # Decide on linking strategy or raise error, per detailed business rules.
             # For now, let's assume if email exists, it must be an error unless explicit linking is intended.
             # raise UserError(_("A user with this email already exists: %s. Please login or use a different email.") % influencer_data['email'])


        # 2. Create res.users record (if not exists/provided)
        user_id = influencer_data.get('user_id')
        user = None
        if user_id:
            user = self.env['res.users'].browse(user_id)
            if not user.exists():
                raise UserError(_("Provided user ID does not exist."))
        elif influencer_data.get('create_user', True): # Assuming a flag to control user creation
            # Ensure the user belongs to the portal group or influencer group
            group_portal_id = self.env.ref('base.group_portal').id
            group_influencer_id = self.env.ref('influence_gen_services.group_influence_gen_influencer', raise_if_not_found=False)
            if not group_influencer_id: # Fallback if group not yet created (e.g. during install)
                _logger.warning("Influencer security group 'group_influence_gen_influencer' not found. User will be portal user.")
                user_groups = [(6, 0, [group_portal_id])]
            else:
                user_groups = [(6, 0, [group_portal_id, group_influencer_id.id])]

            user_vals = {
                'name': influencer_data['fullName'],
                'login': influencer_data['email'],
                'email': influencer_data['email'], # Odoo uses login for email too often
                'groups_id': user_groups,
                'active': True, # Or False, pending email verification if that's a step
                'password': influencer_data.get('password'), # Password should be handled securely
            }
            if influencer_data.get('phone'):
                user_vals['phone'] = influencer_data.get('phone')

            try:
                user = self.env['res.users'].create(user_vals)
                _logger.info("Created new user: %s (ID: %s)", user.login, user.id)
            except Exception as e:
                _logger.error("Error creating user for %s: %s", influencer_data['email'], e)
                raise UserError(_("Could not create user account: %s") % e)
        else:
            raise UserError(_("User ID must be provided or user creation must be allowed."))


        # 3. Create influence_gen.influencer_profile record
        profile_vals = {
            'name': influencer_data['fullName'],
            'user_id': user.id,
            'email': influencer_data['email'], # Ensure this is unique via model constraint
            'phone': influencer_data.get('phone'),
            'residential_address': influencer_data.get('residentialAddress'),
            'audience_demographics': influencer_data.get('audienceDemographics'), # Expects JSON string
            'kyc_status': 'pending',
            'account_status': 'pending_activation', # or 'inactive'
            'onboarding_checklist_json': '{}', # Initial empty checklist
        }
        if 'area_of_influence_ids' in influencer_data and influencer_data['area_of_influence_ids']:
            profile_vals['area_of_influence_ids'] = [(6, 0, influencer_data['area_of_influence_ids'])]


        try:
            profile = self.env['influence_gen.influencer_profile'].create(profile_vals)
            _logger.info("Created influencer profile: %s (ID: %s)", profile.name, profile.id)
        except Exception as e:
            _logger.error("Error creating influencer profile for %s: %s", influencer_data['email'], e)
            # Potentially rollback user creation if profile fails
            if user and not user_id: # if user was created in this transaction
                 # user.unlink() # This might be too aggressive, consider implications
                 _logger.warning("User %s created but profile creation failed. Manual cleanup might be needed.", user.login)
            raise UserError(_("Could not create influencer profile: %s") % e)

        # 4. Create influence_gen.social_media_profile records
        social_media_profiles_data = influencer_data.get('social_media_profiles', [])
        for sm_data in social_media_profiles_data:
            sm_vals = {
                'influencer_profile_id': profile.id,
                'platform': sm_data.get('platform'),
                'handle': sm_data.get('handle'),
                'url': sm_data.get('url'),
                'platform_other': sm_data.get('platform_other'),
                # verification_status defaults to 'pending'
            }
            self.env['influence_gen.social_media_profile'].create(sm_vals)

        # 5. Initialize onboarding_checklist_json (already done in profile creation)

        # 6. Log audit event
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='INFLUENCER_REGISTRATION',
            actor_user_id=self.env.user.id, # Or system user if automated
            action_performed='CREATE',
            target_object=profile,
            details_dict={'email': profile.email, 'user_id': user.id}
        )

        # 7. Trigger "Registration Received" notification
        try:
            self.env['influence_gen.infrastructure.integration.services'].send_notification(
                recipient_user_ids=[user.id],
                template_name='influencer_registration_received', # Assumed template
                context={'influencer_name': profile.name}
            )
            # Notify admins as well
            admin_group = self.env.ref('influence_gen_services.group_influence_gen_admin', raise_if_not_found=False)
            if admin_group:
                admin_users = self.env['res.users'].search([('groups_id', 'in', admin_group.id)])
                if admin_users:
                     self.env['influence_gen.infrastructure.integration.services'].send_notification(
                        recipient_user_ids=admin_users.ids,
                        template_name='admin_new_influencer_registration', # Assumed template
                        context={'influencer_name': profile.name, 'influencer_email': profile.email}
                    )
        except Exception as e:
            _logger.error("Failed to send registration notification for profile %s: %s", profile.id, e)
            # Non-critical, so don't raise UserError here, just log

        return profile

    def handle_kyc_document_submission(self, influencer_id, document_type, front_attachment_data, back_attachment_data=None, verification_method='manual'):
        """
        Handles KYC document submission for an influencer.
        REQ-IOKYC-005
        """
        _logger.info("Handling KYC document submission for influencer ID: %s", influencer_id)
        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            raise UserError(_("Influencer profile not found."))

        if not front_attachment_data:
            raise UserError(_("Front document attachment data is required."))

        # 2. Create ir.attachment records
        # Assuming front_attachment_data and back_attachment_data are dicts like:
        # {'name': 'filename.jpg', 'datas': 'base64_encoded_data', 'mimetype': 'image/jpeg'}
        
        # Max file size check (example)
        max_size_mb = self.env['influence_gen.platform_setting'].get_param('influence_gen.kyc_document_max_file_size_mb', 5)
        max_size_bytes = max_size_mb * 1024 * 1024

        if len(front_attachment_data.get('datas', '')) * 3 / 4 > max_size_bytes: # Estimate base64 decoded size
            raise UserError(_("Front document file size exceeds the maximum limit of %s MB.") % max_size_mb)

        front_attachment_vals = {
            'name': front_attachment_data.get('name'),
            'datas': front_attachment_data.get('datas'),
            'mimetype': front_attachment_data.get('mimetype'),
            'res_model': 'influence_gen.kyc_data', # Link to kyc_data eventually
            'access_token': self.env['ir.attachment']._generate_access_token(), # For security
        }
        front_attachment = self.env['ir.attachment'].create(front_attachment_vals)
        _logger.info("Created front attachment ID: %s", front_attachment.id)

        back_attachment = None
        if back_attachment_data and back_attachment_data.get('datas'):
            if len(back_attachment_data.get('datas', '')) * 3 / 4 > max_size_bytes:
                raise UserError(_("Back document file size exceeds the maximum limit of %s MB.") % max_size_mb)
            back_attachment_vals = {
                'name': back_attachment_data.get('name'),
                'datas': back_attachment_data.get('datas'),
                'mimetype': back_attachment_data.get('mimetype'),
                'res_model': 'influence_gen.kyc_data',
                'access_token': self.env['ir.attachment']._generate_access_token(),
            }
            back_attachment = self.env['ir.attachment'].create(back_attachment_vals)
            _logger.info("Created back attachment ID: %s", back_attachment.id if back_attachment else "None")


        # 3. Create influence_gen.kyc_data record
        kyc_data_vals = {
            'influencer_profile_id': influencer_profile.id,
            'document_type': document_type,
            'document_front_attachment_id': front_attachment.id,
            'document_back_attachment_id': back_attachment.id if back_attachment else False,
            'verification_method': verification_method,
            'verification_status': 'pending', # Default from model, but can be set to 'in_review' if auto-submitted
        }
        kyc_submission = self.env['influence_gen.kyc_data'].create(kyc_data_vals)
        # Link attachments to the kyc_data record for proper access control if ir.rules are strict
        front_attachment.write({'res_id': kyc_submission.id})
        if back_attachment:
            back_attachment.write({'res_id': kyc_submission.id})
        
        # 4. Update influencer_profile_id.kyc_status to 'in_review'
        influencer_profile.write({'kyc_status': 'in_review'})
        
        # 5. Update influencer_profile_id.onboarding_checklist_json for kyc submission
        influencer_profile.update_onboarding_step_status('kyc_submitted', True)

        # 6. Log audit
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_DOCUMENT_SUBMITTED',
            actor_user_id=influencer_profile.user_id.id, # Action by influencer
            action_performed='CREATE',
            target_object=kyc_submission,
            details_dict={'influencer_id': influencer_profile.id, 'document_type': document_type}
        )

        # 7. Trigger notifications
        try:
            # To influencer
            self.env['influence_gen.infrastructure.integration.services'].send_notification(
                recipient_user_ids=[influencer_profile.user_id.id],
                template_name='kyc_documents_received',
                context={'influencer_name': influencer_profile.name}
            )
            # To admins
            admin_group = self.env.ref('influence_gen_services.group_influence_gen_admin', raise_if_not_found=False)
            if admin_group:
                admin_users = self.env['res.users'].search([('groups_id', 'in', admin_group.id)])
                if admin_users:
                    self.env['influence_gen.infrastructure.integration.services'].send_notification(
                        recipient_user_ids=admin_users.ids,
                        template_name='admin_kyc_awaiting_review',
                        context={'influencer_name': influencer_profile.name, 'kyc_submission_id': kyc_submission.id}
                    )
        except Exception as e:
            _logger.error("Failed to send KYC submission notification for kyc_id %s: %s", kyc_submission.id, e)

        return kyc_submission

    def handle_kyc_review_decision(self, kyc_data_id, decision, reviewer_user_id, notes=None):
        """
        Handles admin's review decision on a KYC submission.
        REQ-IOKYC-005
        The 'notes' parameter from SDS seems to cover 'reason_if_rejected' and 'info_needed_if_more_info'
        """
        _logger.info("Handling KYC review decision for KYC Data ID: %s, Decision: %s", kyc_data_id, decision)
        kyc_data = self.env['influence_gen.kyc_data'].browse(kyc_data_id)
        if not kyc_data.exists():
            raise UserError(_("KYC Data record not found."))
        
        reviewer = self.env['res.users'].browse(reviewer_user_id)
        if not reviewer.exists():
            raise UserError(_("Reviewer user not found."))

        notification_template_name = None
        notification_context = {'influencer_name': kyc_data.influencer_profile_id.name, 'notes': notes}

        if decision == 'approved':
            kyc_data.action_approve(reviewer.id, notes=notes)
            notification_template_name = 'kyc_approved'
        elif decision == 'rejected':
            if not notes: # Reason is crucial for rejection
                raise UserError(_("A reason (notes) is required for rejecting KYC."))
            kyc_data.action_reject(reviewer.id, reason_notes=notes)
            notification_template_name = 'kyc_rejected'
        elif decision == 'needs_more_info':
            if not notes: # Info needed is crucial
                raise UserError(_("Details on information needed (notes) are required."))
            kyc_data.action_request_more_info(reviewer.id, info_needed_notes=notes)
            notification_template_name = 'kyc_needs_more_info'
        else:
            raise UserError(_("Invalid KYC review decision: %s") % decision)

        # Audit log is created within the kyc_data model's action methods.

        # Trigger notification to influencer
        if notification_template_name:
            try:
                self.env['influence_gen.infrastructure.integration.services'].send_notification(
                    recipient_user_ids=[kyc_data.influencer_profile_id.user_id.id],
                    template_name=notification_template_name,
                    context=notification_context
                )
            except Exception as e:
                _logger.error("Failed to send KYC decision notification for kyc_id %s: %s", kyc_data.id, e)
        
        # Potentially try to activate account if KYC approved and other conditions met
        if decision == 'approved':
            self.check_and_activate_influencer_account(kyc_data.influencer_profile_id.id)


    def initiate_social_media_verification(self, social_profile_id, method):
        """
        Initiates the verification process for a social media profile.
        REQ-IOKYC-006
        """
        _logger.info("Initiating social media verification for profile ID: %s, Method: %s", social_profile_id, method)
        social_profile = self.env['influence_gen.social_media_profile'].browse(social_profile_id)
        if not social_profile.exists():
            raise UserError(_("Social Media Profile not found."))

        verification_details = social_profile.action_initiate_verification(method)
        
        # Audit log is created within the social_profile model's action method.

        # Trigger notification to influencer with instructions if needed
        # Example for 'code_in_bio'
        if method == 'code_in_bio' and verification_details and verification_details.get('code'):
            try:
                self.env['influence_gen.infrastructure.integration.services'].send_notification(
                    recipient_user_ids=[social_profile.influencer_profile_id.user_id.id],
                    template_name='social_media_verification_code_instruction', # Assumed template
                    context={
                        'influencer_name': social_profile.influencer_profile_id.name,
                        'platform': social_profile.platform,
                        'handle': social_profile.handle,
                        'verification_code': verification_details['code']
                    }
                )
            except Exception as e:
                _logger.error("Failed to send social media verification instruction for profile %s: %s", social_profile.id, e)
        
        return verification_details


    def confirm_social_media_verification(self, social_profile_id, verification_input=None):
        """
        Confirms the verification of a social media profile.
        REQ-IOKYC-006
        """
        _logger.info("Confirming social media verification for profile ID: %s", social_profile_id)
        social_profile = self.env['influence_gen.social_media_profile'].browse(social_profile_id)
        if not social_profile.exists():
            raise UserError(_("Social Media Profile not found."))

        success = social_profile.action_confirm_verification(verification_input=verification_input)
        
        # Audit log is created within the social_profile model's action method.

        notification_template_name = 'social_media_verification_failed'
        if success:
            notification_template_name = 'social_media_verification_success'
            # Check for account activation
            self.check_and_activate_influencer_account(social_profile.influencer_profile_id.id)


        try:
            self.env['influence_gen.infrastructure.integration.services'].send_notification(
                recipient_user_ids=[social_profile.influencer_profile_id.user_id.id],
                template_name=notification_template_name,
                context={
                    'influencer_name': social_profile.influencer_profile_id.name,
                    'platform': social_profile.platform,
                    'handle': social_profile.handle
                }
            )
        except Exception as e:
            _logger.error("Failed to send social media verification confirmation for profile %s: %s", social_profile.id, e)
            
        return success

    def initiate_bank_account_verification(self, bank_account_id, method):
        """
        Initiates the verification process for a bank account.
        REQ-IOKYC-008
        """
        _logger.info("Initiating bank account verification for bank account ID: %s, Method: %s", bank_account_id, method)
        bank_account = self.env['influence_gen.bank_account'].browse(bank_account_id)
        if not bank_account.exists():
            raise UserError(_("Bank Account not found."))

        verification_details = bank_account.action_initiate_verification(method)
        # Audit log is created within the bank_account model's action method.

        # Example notification for micro-deposit
        if method == 'micro_deposit':
             try:
                self.env['influence_gen.infrastructure.integration.services'].send_notification(
                    recipient_user_ids=[bank_account.influencer_profile_id.user_id.id],
                    template_name='bank_account_micro_deposit_initiated', # Assumed template
                    context={
                        'influencer_name': bank_account.influencer_profile_id.name,
                        'bank_account_masked': bank_account.display_name # Assuming display_name is masked
                    }
                )
             except Exception as e:
                _logger.error("Failed to send bank micro-deposit initiation notification for bank account %s: %s", bank_account.id, e)
        
        return verification_details

    def confirm_bank_account_verification(self, bank_account_id, verification_input=None):
        """
        Confirms the verification of a bank account.
        REQ-IOKYC-008
        """
        _logger.info("Confirming bank account verification for bank account ID: %s", bank_account_id)
        bank_account = self.env['influence_gen.bank_account'].browse(bank_account_id)
        if not bank_account.exists():
            raise UserError(_("Bank Account not found."))

        success = bank_account.action_confirm_verification(verification_input=verification_input)
        # Audit log is created within the bank_account model's action method.
        
        notification_template_name = 'bank_account_verification_failed'
        if success:
            notification_template_name = 'bank_account_verification_success'
            # Check for account activation
            self.check_and_activate_influencer_account(bank_account.influencer_profile_id.id)
            
        try:
            self.env['influence_gen.infrastructure.integration.services'].send_notification(
                recipient_user_ids=[bank_account.influencer_profile_id.user_id.id],
                template_name=notification_template_name,
                context={
                    'influencer_name': bank_account.influencer_profile_id.name,
                    'bank_account_masked': bank_account.display_name
                }
            )
        except Exception as e:
            _logger.error("Failed to send bank account verification confirmation for bank account %s: %s", bank_account.id, e)

        return success

    def record_terms_consent(self, influencer_id, tos_version, privacy_policy_version, ip_address=None):
        """
        Records an influencer's consent to terms and policies.
        REQ-IOKYC-009
        """
        _logger.info("Recording terms consent for influencer ID: %s", influencer_id)
        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            raise UserError(_("Influencer profile not found."))
            
        if not tos_version:
            tos_version = self.env['influence_gen.platform_setting'].get_param('influence_gen.default_tos_version', 'N/A')
        if not privacy_policy_version:
            privacy_policy_version = self.env['influence_gen.platform_setting'].get_param('influence_gen.default_privacy_policy_version', 'N/A')

        consent = self.env['influence_gen.terms_consent'].create_consent(
            influencer_id=influencer_profile.id,
            tos_version=tos_version,
            privacy_policy_version=privacy_policy_version,
            ip_address=ip_address
        )
        
        # Audit log is created within TermsConsent.create_consent
        
        # Update onboarding checklist
        influencer_profile.update_onboarding_step_status('tos_agreed', True)
        
        # Check for account activation
        self.check_and_activate_influencer_account(influencer_id)
        
        _logger.info("Terms consent ID %s recorded for influencer ID: %s", consent.id, influencer_id)
        return consent


    def check_and_activate_influencer_account(self, influencer_id):
        """
        Checks if all onboarding prerequisites are met and activates the account.
        REQ-IOKYC-012
        """
        _logger.info("Checking and attempting to activate account for influencer ID: %s", influencer_id)
        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            _logger.warning("Influencer profile %s not found for activation check.", influencer_id)
            return False
        
        if influencer_profile.account_status == 'active':
            _logger.info("Influencer %s account is already active.", influencer_id)
            return True

        # Call the model method that checks all conditions
        if influencer_profile.check_onboarding_completion():
            if influencer_profile.action_activate_account():
                _logger.info("Influencer account %s successfully activated.", influencer_id)
                return True
            else:
                _logger.warning("Influencer account %s met completion criteria but activation failed (action_activate_account returned False).", influencer_id)
                return False
        else:
            _logger.info("Influencer account %s onboarding not yet complete.", influencer_id)
            return False