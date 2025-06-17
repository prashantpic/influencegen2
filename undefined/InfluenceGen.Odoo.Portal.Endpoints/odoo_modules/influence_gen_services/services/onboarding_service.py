# -*- coding: utf-8 -*-
import logging
from odoo import _, api
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class OnboardingService:
    """
    Service class for orchestrating influencer onboarding and KYC processes.
    It coordinates interactions between various models like InfluencerProfile, KycData,
    SocialMediaProfile, BankAccount, and TermsConsent.
    """

    def __init__(self, env):
        """
        Initializes the service with the Odoo environment.
        :param env: Odoo Environment
        """
        self.env = env

    def process_registration_submission(self, influencer_vals):
        """
        Processes a new influencer registration submission.
        - Validates influencer_vals (email uniqueness, required fields).
        - Creates res.users record (if not exists for email, or based on policy).
        - Creates influence_gen.influencer_profile record.
        - Creates influence_gen.terms_consent if ToS/PP consent provided.
        - Logs audit event (handled by model mixin).
        - Sends registration confirmation email (handled by mail template).
        :param influencer_vals: dict of values for influencer_profile and related models.
                               Expected keys: 'full_name', 'email', 'password' (for user),
                               'phone', 'residential_address', 'tos_version', 'privacy_policy_version' (optional)
        :return: recordset of the created influence_gen.influencer_profile
        REQ-IOKYC-002
        """
        _logger.info(f"Processing registration submission for email: {influencer_vals.get('email')}")

        if not influencer_vals.get('email') or not influencer_vals.get('full_name'):
            raise UserError(_("Email and Full Name are required for registration."))

        # Check for existing user/influencer by email
        existing_user = self.env['res.users'].search([('login', '=', influencer_vals['email'])], limit=1)
        if existing_user:
            existing_profile = self.env['influence_gen.influencer_profile'].search([('user_id', '=', existing_user.id)], limit=1)
            if existing_profile:
                raise UserError(_("An influencer profile with this email address already exists."))
        
        # Create res.users
        user_vals = {
            'name': influencer_vals['full_name'],
            'login': influencer_vals['email'],
            'email': influencer_vals['email'],
            # Ensure new users are added to the Influencer group and Portal group if applicable
            'groups_id': [(6, 0, [self.env.ref('influence_gen_services.group_influence_gen_influencer').id, self.env.ref('base.group_portal').id])]
        }
        if 'password' in influencer_vals: # Password should be handled securely by Odoo user creation
            user_vals['password'] = influencer_vals['password']
        
        try:
            if existing_user: # User exists but no profile, link to this user
                user = existing_user
            else:
                user = self.env['res.users'].with_context(no_reset_password=True).create(user_vals) # no_reset_password to avoid Odoo sending its own email
                _logger.info(f"Created new user {user.login} (ID: {user.id})")
        except Exception as e:
            _logger.error(f"Error creating user: {e}")
            raise UserError(_("Could not create user account: %s") % str(e))

        # Create InfluencerProfile
        profile_vals = {
            'user_id': user.id,
            'full_name': influencer_vals['full_name'],
            'email': influencer_vals['email'], # Ensure email is synced
            'phone': influencer_vals.get('phone'),
            'residential_address': influencer_vals.get('residential_address'),
            'kyc_status': 'pending',
            'account_status': 'pending_verification',
        }
        influencer_profile = self.env['influence_gen.influencer_profile'].create(profile_vals)
        _logger.info(f"Created influencer profile ID {influencer_profile.id} for user {user.login}")

        # Process Terms Consent
        if influencer_vals.get('tos_version') and influencer_vals.get('privacy_policy_version'):
            self.process_terms_consent(
                influencer_profile.id,
                influencer_vals['tos_version'],
                influencer_vals['privacy_policy_version']
            )

        # Send registration confirmation email (REQ-16-001)
        try:
            template = self.env.ref('influence_gen_services.email_template_influencer_registration_confirmation', raise_if_not_found=True)
            template.send_mail(influencer_profile.id, force_send=True)
            _logger.info(f"Sent registration confirmation email to {influencer_profile.email}")
        except Exception as e:
            _logger.error(f"Failed to send registration confirmation email to {influencer_profile.email}: {e}")

        return influencer_profile

    def submit_kyc_documents(self, influencer_id, document_data_list):
        """
        Submits KYC documents for an influencer.
        - Creates ir.attachment for document files.
        - Creates influence_gen.kyc_data record.
        - Updates influencer profile kyc_status.
        - Logs audit event (handled by model).
        - Sends KYC submission received notification (handled by mail template).
        :param influencer_id: int, ID of the influence_gen.influencer_profile
        :param document_data_list: list of dicts, each with 'document_type', 'file_name', 'file_data' (base64),
                                   'document_back_file_name' (optional), 'document_back_file_data' (optional).
        :return: bool (success/failure)
        REQ-IOKYC-004, REQ-IOKYC-005
        """
        _logger.info(f"Submitting KYC documents for influencer ID: {influencer_id}")
        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            raise UserError(_("Influencer profile not found."))

        KycData = self.env['influence_gen.kyc_data']
        Attachment = self.env['ir.attachment']

        for doc_data in document_data_list:
            if not doc_data.get('document_type') or not doc_data.get('file_name') or not doc_data.get('file_data'):
                _logger.warning("Skipping document due to missing data: %s", doc_data)
                continue

            attachment_front_id = Attachment.create({
                'name': doc_data['file_name'],
                'datas': doc_data['file_data'],
                'res_model': 'influence_gen.kyc_data',
                # res_id will be set later if needed, or keep it generic
            }).id

            attachment_back_id = None
            if doc_data.get('document_back_file_name') and doc_data.get('document_back_file_data'):
                attachment_back_id = Attachment.create({
                    'name': doc_data['document_back_file_name'],
                    'datas': doc_data['document_back_file_data'],
                    'res_model': 'influence_gen.kyc_data',
                }).id
            
            kyc_submission = KycData.create({
                'influencer_profile_id': influencer_profile.id,
                'document_type': doc_data['document_type'],
                'document_front_attachment_id': attachment_front_id,
                'document_back_attachment_id': attachment_back_id,
                'verification_status': 'submitted', # or 'pending_review'
                'verification_method': doc_data.get('verification_method', 'manual_upload'),
            })
            _logger.info(f"Created KYC submission ID {kyc_submission.id} for influencer {influencer_profile.id}")

        # Update influencer profile KYC status
        if influencer_profile.kyc_status == 'pending':
            influencer_profile.write({'kyc_status': 'submitted'}) # Or 'in_review' if it goes directly to review
        
        # Send KYC submission received notification (REQ-16-002)
        try:
            template = self.env.ref('influence_gen_services.email_template_kyc_submission_received', raise_if_not_found=True)
            template.send_mail(influencer_profile.id, force_send=True) # Assuming template is on influencer profile
            _logger.info(f"Sent KYC submission received email to {influencer_profile.email}")
        except Exception as e:
            _logger.error(f"Failed to send KYC submission received email: {e}")
            
        return True

    def handle_kyc_review_decision(self, kyc_data_id, decision, reviewer_user_id, notes=None, required_info=None):
        """
        Handles the decision from a KYC review.
        - Updates kyc_data record status, reviewer, notes.
        - Updates influencer_profile kyc_status.
        - If 'approved', may trigger account activation check.
        - Sends KYC status update notification (handled by mail template).
        - Logs audit event (handled by model).
        :param kyc_data_id: int, ID of the influence_gen.kyc_data
        :param decision: str, one of 'approved', 'rejected', 'requires_more_info'
        :param reviewer_user_id: int, ID of the res.users (reviewer)
        :param notes: str, internal reviewer notes
        :param required_info: str, information required if decision is 'requires_more_info', or rejection reason
        REQ-IOKYC-005, REQ-IOKYC-011
        """
        _logger.info(f"Handling KYC review decision for KYC data ID: {kyc_data_id}, Decision: {decision}")
        kyc_data = self.env['influence_gen.kyc_data'].browse(kyc_data_id)
        if not kyc_data.exists():
            raise UserError(_("KYC submission record not found."))
        
        reviewer = self.env['res.users'].browse(reviewer_user_id)
        if not reviewer.exists():
            raise UserError(_("Reviewer user not found."))

        update_vals = {
            'verification_status': decision,
            'reviewer_user_id': reviewer.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': notes,
        }
        if decision == 'rejected' and required_info: # Using required_info as rejection reason here
             update_vals['notes'] = (notes or "") + _("\nRejection Reason: ") + required_info
        elif decision == 'requires_more_info' and required_info:
             update_vals['notes'] = (notes or "") + _("\nInformation Required: ") + required_info

        kyc_data.write(update_vals)
        _logger.info(f"KYC data ID {kyc_data.id} updated to status {decision}")

        influencer_profile = kyc_data.influencer_profile_id
        # Update main influencer profile kyc_status based on this and other KYC items (simplified here)
        # More complex logic might check if ALL required KYC items are approved.
        if decision == 'approved':
            # Check if all KYC items are approved before setting profile to approved
            all_kyc_approved = all(k.verification_status == 'approved' for k in influencer_profile.kyc_data_ids)
            if all_kyc_approved:
                 influencer_profile.write({'kyc_status': 'approved'})
                 self.check_and_activate_influencer_account(influencer_profile.id)
            else:
                 influencer_profile.write({'kyc_status': 'in_review'}) # Or requires_more_info if one is rejected/needs more
        elif decision == 'rejected':
            influencer_profile.write({'kyc_status': 'rejected'})
        elif decision == 'requires_more_info':
            influencer_profile.write({'kyc_status': 'requires_more_info'})
        
        # Send KYC status update notification (REQ-16-002)
        try:
            template = self.env.ref('influence_gen_services.email_template_kyc_status_update', raise_if_not_found=True)
            # Pass context for dynamic email content
            email_context = {'decision': decision, 'notes': required_info or notes} 
            template.with_context(**email_context).send_mail(kyc_data.id, force_send=True) # Assuming template is on kyc_data
            _logger.info(f"Sent KYC status update email for KYC data {kyc_data.id}")
        except Exception as e:
            _logger.error(f"Failed to send KYC status update email: {e}")
            
        return True

    def verify_social_media_account(self, social_profile_id, method, verification_input=None):
        """
        Verifies a social media account.
        - Updates verification_status on SocialMediaProfile.
        - Logs audit event.
        - Calls check_and_activate_influencer_account.
        :param social_profile_id: int, ID of influence_gen.social_media_profile
        :param method: str, verification method used (e.g., 'oauth', 'code_in_bio', 'manual')
        :param verification_input: str, input for verification (e.g., code)
        :return: bool success
        REQ-IOKYC-006
        """
        _logger.info(f"Verifying social media profile ID: {social_profile_id} using method: {method}")
        social_profile = self.env['influence_gen.social_media_profile'].browse(social_profile_id)
        if not social_profile.exists():
            raise UserError(_("Social media profile not found."))

        # Placeholder for actual verification logic which might involve:
        # - Calling REPO-IGIA-004 for OAuth or API checks
        # - Manual verification by admin
        verified = False
        if method == 'manual': # Admin manually verifies
            verified = True # Assuming admin confirmed
        elif method == 'code_in_bio':
            # Example: Call an adapter to scrape profile and check for social_profile.verification_code
            # verified = self.env['influence_gen.integration.adapter'].check_bio_for_code(social_profile.url, social_profile.verification_code)
            # This is a placeholder
            if verification_input == social_profile.verification_code: # Simplified check
                 _logger.warning("Simplified code_in_bio check for demo purposes.")
                 verified = True
            else:
                 _logger.info(f"Code in bio verification failed for {social_profile_id}. Expected {social_profile.verification_code}, got {verification_input}")

        if verified:
            social_profile.write({
                'verification_status': 'verified',
                'verified_at': fields.Datetime.now(),
                'verification_method': method,
            })
            _logger.info(f"Social media profile ID {social_profile.id} verified.")
            self.check_and_activate_influencer_account(social_profile.influencer_profile_id.id)
            return True
        else:
            social_profile.write({'verification_status': 'failed'})
            _logger.warning(f"Social media profile ID {social_profile.id} verification failed.")
            return False

    def verify_bank_account(self, bank_account_id, method, verification_input=None):
        """
        Verifies a bank account.
        - Updates verification_status on BankAccount.
        - Logs audit event.
        - Calls check_and_activate_influencer_account.
        :param bank_account_id: int, ID of influence_gen.bank_account
        :param method: str, verification method used (e.g., 'micro_deposit', 'third_party_api', 'manual')
        :param verification_input: dict, input for verification (e.g., micro-deposit amounts)
        :return: bool success
        REQ-IPF-002, REQ-IOKYC-008
        """
        _logger.info(f"Verifying bank account ID: {bank_account_id} using method: {method}")
        bank_account = self.env['influence_gen.bank_account'].browse(bank_account_id)
        if not bank_account.exists():
            raise UserError(_("Bank account not found."))

        # Placeholder for actual verification logic
        verified = False
        if method == 'manual':
            verified = True # Admin manually verifies
        elif method == 'micro_deposit':
            # Example: Call an adapter or model method to confirm micro-deposit amounts
            # verified = bank_account.confirm_micro_deposit(verification_input.get('amount1'), verification_input.get('amount2'))
            # This is a placeholder
            _logger.warning("Simplified micro_deposit check for demo purposes.")
            if verification_input and verification_input.get('amount1') and verification_input.get('amount2'): # Dummy check
                 verified = True

        if verified:
            bank_account.write({
                'verification_status': 'verified',
                'verification_method': method,
            })
            _logger.info(f"Bank account ID {bank_account.id} verified.")
            if bank_account.is_primary:
                self.check_and_activate_influencer_account(bank_account.influencer_profile_id.id)
            return True
        else:
            bank_account.write({'verification_status': 'failed'})
            _logger.warning(f"Bank account ID {bank_account.id} verification failed.")
            return False

    def process_terms_consent(self, influencer_id, tos_version, privacy_policy_version):
        """
        Processes and records terms consent.
        - Creates influence_gen.terms_consent record.
        - Logs audit event.
        - Calls check_and_activate_influencer_account.
        :param influencer_id: int, ID of influence_gen.influencer_profile
        :param tos_version: str, version of Terms of Service
        :param privacy_policy_version: str, version of Privacy Policy
        REQ-IOKYC-009
        """
        _logger.info(f"Processing terms consent for influencer ID: {influencer_id}")
        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            raise UserError(_("Influencer profile not found."))

        self.env['influence_gen.terms_consent'].create({
            'influencer_profile_id': influencer_profile.id,
            'tos_version': tos_version,
            'privacy_policy_version': privacy_policy_version,
            'consent_date': fields.Datetime.now(),
        })
        _logger.info(f"Terms consent recorded for influencer ID {influencer_profile.id}")
        self.check_and_activate_influencer_account(influencer_profile.id)
        return True

    def check_and_activate_influencer_account(self, influencer_id):
        """
        Checks if all onboarding prerequisites are met and activates the account if so.
        Prerequisites: KYC approved, primary bank account verified, latest terms consented.
        Sends account activation notification (handled by model/mail template).
        :param influencer_id: int, ID of influence_gen.influencer_profile
        :return: bool (True if activated, False otherwise)
        REQ-IOKYC-012
        """
        _logger.info(f"Checking onboarding completion for influencer ID: {influencer_id}")
        influencer_profile = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer_profile.exists():
            _logger.warning(f"Influencer profile {influencer_id} not found for activation check.")
            return False

        if influencer_profile.account_status == 'active':
            _logger.info(f"Influencer account {influencer_id} is already active.")
            return False # Already active

        is_complete = influencer_profile.check_onboarding_completion()

        if is_complete:
            _logger.info(f"Onboarding complete for influencer {influencer_id}. Activating account.")
            influencer_profile.action_activate_account() # This method sends REQ-16-003
            return True
        else:
            _logger.info(f"Onboarding not yet complete for influencer {influencer_id}.")
            return False