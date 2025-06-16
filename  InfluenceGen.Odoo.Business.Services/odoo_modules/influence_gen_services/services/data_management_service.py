# -*- coding: utf-8 -*-
import logging
import json
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

class DataManagementService(models.AbstractModel):
    _name = 'influence_gen.data.management.service'
    _description = 'InfluenceGen Data Management Service'

    def __init__(self, env):
        super(DataManagementService, self).__init__(env)
        self.env = env

    def apply_data_retention_policies(self, data_category=None, dry_run=False):
        """
        Applies data retention policies.
        REQ-DRH-001, REQ-DRH-002, REQ-DRH-005, REQ-DRH-006, REQ-IPF-008, REQ-AIGS-011.
        :param data_category: (optional) specific data category to process
        :param dry_run: boolean, if True, only log actions, do not execute
        :return: dict summary of actions
        """
        policy_domain = [('is_active', '=', True)]
        if data_category:
            policy_domain.append(('data_category', '=', data_category))
        
        policies = self.env['influence_gen.data_retention_policy'].search(policy_domain)
        summary = {'processed_policies': 0, 'actions_taken': [], 'errors': []}

        for policy in policies:
            summary['processed_policies'] += 1
            _logger.info(f"{'DRY RUN: ' if dry_run else ''}Processing retention policy: {policy.name} for model {policy.model_name}")
            
            if not policy.model_name:
                _logger.warning(f"Policy {policy.name} has no target model name. Skipping.")
                summary['errors'].append(f"Policy '{policy.name}' has no target model name.")
                continue

            try:
                target_model = self.env[policy.model_name]
            except KeyError:
                _logger.error(f"Model {policy.model_name} not found for policy {policy.name}. Skipping.")
                summary['errors'].append(f"Model '{policy.model_name}' not found for policy '{policy.name}'.")
                continue

            # Calculate cutoff date
            cutoff_date = fields.Datetime.now() - relativedelta(days=policy.retention_period_days)
            
            # Domain to find records older than retention period
            # Assuming 'create_date' is the common field for age. Some models might need specific date fields.
            record_domain = [('create_date', '<=', fields.Datetime.to_string(cutoff_date))]
            
            # REQ-DRH-009: Exclude records under legal hold
            # This assumes target models have 'legal_hold_active' field.
            if hasattr(target_model, 'legal_hold_active') and policy.legal_hold_overrideable is False:
                 record_domain.append(('legal_hold_active', '!=', True))
            elif hasattr(target_model, 'legal_hold_active') and policy.legal_hold_overrideable is True:
                 _logger.info(f"Policy {policy.name} is overrideable by legal hold, but legal hold check on records will still proceed if applicable.")
                 # If overrideable means it *can* delete even if on hold, then this logic is more complex.
                 # Current SDS for DRH-009 suggests legal hold prevents deletion.
                 # Let's assume legal_hold_overrideable=False implies STRICT non-deletion if on hold.
                 # And legal_hold_overrideable=True means the policy *could* be configured to ignore legal hold,
                 # but for safety, we will always respect legal hold for now unless explicitly told to ignore.
                 # The current implementation respects legal hold if field exists.
                 # For the policy to truly override, the legal_hold_active check needs to be conditional based on policy.legal_hold_overrideable.
                 # Given the SDS, the safest interpretation is that apply_data_retention_policies checks
                 # and *does not* delete if legal_hold_active = True, regardless of policy.legal_hold_overrideable being True,
                 # unless there's a specific "force" mode which isn't present.
                 # Let's refine: if policy.legal_hold_overrideable is TRUE, it means this policy's disposition action should
                 # proceed EVEN IF there is a legal hold. If it's FALSE, legal hold MUST stop it.
                 # So if policy.legal_hold_overrideable is False:
                 if hasattr(target_model, 'legal_hold_active') and not policy.legal_hold_overrideable:
                    record_domain.append(('legal_hold_active', '!=', True))


            records_to_process = target_model.search(record_domain)
            
            action_details = {
                'policy_name': policy.name,
                'model': policy.model_name,
                'disposition_action': policy.disposition_action,
                'records_count': len(records_to_process),
                'dry_run': dry_run
            }
            summary['actions_taken'].append(action_details)

            if not records_to_process:
                _logger.info(f"No records found for policy {policy.name} on model {policy.model_name} older than {cutoff_date}.")
                continue

            _logger.info(f"{'DRY RUN: ' if dry_run else ''}Policy {policy.name}: Found {len(records_to_process)} records for {policy.disposition_action}.")

            if not dry_run:
                for record_batch in records_to_process.split(100): # Process in batches
                    try:
                        if policy.disposition_action == 'delete':
                            record_batch.unlink()
                            _logger.info(f"Deleted {len(record_batch)} records for policy {policy.name}.")
                        elif policy.disposition_action == 'anonymize':
                            # Anonymization is model-specific.
                            # Requires a method like 'action_anonymize' on the target model.
                            if hasattr(target_model, 'action_anonymize_record'):
                                for rec in record_batch:
                                    rec.action_anonymize_record()
                                _logger.info(f"Anonymized {len(record_batch)} records for policy {policy.name}.")
                            else:
                                _logger.warning(f"Anonymization action for model {policy.model_name} not implemented (missing action_anonymize_record).")
                                summary['errors'].append(f"Anonymization not implemented for model '{policy.model_name}'.")
                        elif policy.disposition_action == 'archive':
                            # REQ-DRH-007: Flag for archival or trigger archival process via infra layer.
                            # Standard Odoo way: if model inherits 'archive.mixin', use record.action_archive()
                            # or set 'active = False'.
                            if hasattr(target_model, 'active'): # Common Odoo pattern
                                record_batch.write({'active': False})
                                _logger.info(f"Archived (set active=False) {len(record_batch)} records for policy {policy.name}.")
                            # else:
                                # self.env['influence_gen.infrastructure.integration.service'].archive_data_records(policy.model_name, record_batch.ids)
                                # _logger.info(f"Sent {len(record_batch)} records for archival via infra service for policy {policy.name}.")
                            else:
                                _logger.warning(f"Archival action for model {policy.model_name} not clear (no 'active' field).")
                                summary['errors'].append(f"Archival (active=False) not applicable for model '{policy.model_name}'.")
                        
                        self.env['influence_gen.audit_log_entry'].create_log(
                            event_type='DATA_RETENTION_APPLIED',
                            actor_user_id=self.env.user.id, # System User
                            action_performed=policy.disposition_action.upper(),
                            target_model_name=policy.model_name,
                            # target_record_id cannot be set for batch, details can list ids
                            details_dict={
                                'policy_name': policy.name, 
                                'record_ids_count': len(record_batch),
                                'cutoff_date': str(cutoff_date)
                            }
                        )
                    except Exception as e:
                        _logger.error(f"Error applying policy {policy.name} to batch of records in {policy.model_name}: {e}")
                        summary['errors'].append(f"Error on policy '{policy.name}' for model '{policy.model_name}': {str(e)}")
        
        _logger.info(f"{'DRY RUN: ' if dry_run else ''}Data retention policy application finished. Summary: {summary}")
        return summary

    def process_pii_erasure_request(self, influencer_id, data_scope_description):
        """
        Processes a PII erasure request for an influencer. REQ-DRH-003.
        :param influencer_id: ID of influence_gen.influencer_profile
        :param data_scope_description: string describing scope (e.g., 'full_profile', 'contact_info') - for logging
        :return: Boolean, True if successful (or NotFound if influencer not found implies success)
        """
        influencer = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer.exists():
            _logger.info(f"PII Erasure Request: Influencer profile {influencer_id} not found. Considered complete.")
            return True # Or False depending on desired behavior for non-existent profiles

        # Check for legal holds or overriding contractual constraints
        # This is a complex check. For simplicity, check legal_hold on InfluencerProfile itself.
        if hasattr(influencer, 'legal_hold_active') and influencer.legal_hold_active:
            _logger.warning(f"PII Erasure Request for influencer {influencer.name} (ID: {influencer.id}) cannot proceed due to active legal hold.")
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='PII_ERASURE_REQUEST_DENIED_LEGAL_HOLD',
                actor_user_id=self.env.user.id, # User initiating the request or system
                action_performed='DENY',
                target_object=influencer,
                details_dict={'scope': data_scope_description, 'reason': 'Active legal hold'}
            )
            raise UserError("Cannot process PII erasure request: Influencer data is under a legal hold.")

        # Perform secure deletion/anonymization based on scope.
        # This should be very carefully implemented.
        # Example: Anonymize specific fields on InfluencerProfile
        anonymized_fields = {}
        if hasattr(influencer, 'action_anonymize_record'): # Prefer a dedicated method
            influencer.action_anonymize_record() # This method should handle specific fields
            anonymized_fields = {'action': 'anonymize_record_called'}
            _logger.info(f"Anonymized PII for influencer {influencer.name} via action_anonymize_record.")
        else: # Fallback to manual field clearing (less ideal)
            fields_to_anonymize = {
                'phone': None,
                'residential_address': None,
                'audience_demographics': '{}', # Clear JSON
                # email is tricky as it's often a login. Anonymizing it might break user access.
                # 'email': f"anonymized_{influencer.id}@example.com", 
            }
            influencer.write(fields_to_anonymize)
            anonymized_fields = fields_to_anonymize
            _logger.info(f"Anonymized PII for influencer {influencer.name} by clearing fields: {list(fields_to_anonymize.keys())}.")
        
        # Consider related data: KYCData, BankAccount, SocialMediaProfile etc.
        # These should either be deleted or anonymized based on policies.
        # For instance, KYC documents (attachments) should be securely deleted.
        kyc_records = self.env['influence_gen.kyc_data'].search([('influencer_profile_id', '=', influencer.id)])
        for kyc in kyc_records:
            if kyc.document_front_attachment_id: kyc.document_front_attachment_id.unlink()
            if kyc.document_back_attachment_id: kyc.document_back_attachment_id.unlink()
            kyc.unlink() # Delete the KYC record itself
        
        bank_accounts = self.env['influence_gen.bank_account'].search([('influencer_profile_id', '=', influencer.id)])
        bank_accounts.unlink() # Or anonymize if required

        # Social media profiles might be unlinked or anonymized
        # social_media_profiles = self.env['influence_gen.social_media_profile'].search([('influencer_profile_id', '=', influencer.id)])
        # social_media_profiles.unlink()

        # Log action
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PII_ERASURE_PROCESSED',
            actor_user_id=self.env.user.id,
            action_performed='ANONYMIZE_OR_DELETE', # Be specific
            target_object=influencer,
            details_dict={'scope': data_scope_description, 'anonymized_fields_on_profile': anonymized_fields}
        )
        # Potentially deactivate user account if full erasure implies no more platform use
        # influencer.user_id.active = False
        # influencer.account_status = 'inactive' / 'suspended'
        # influencer.name = f"Anonymized User {influencer.id}" # If full anonymization
        
        return True


    def assess_pii_in_campaign_content_for_erasure(self, content_submission_id, influencer_id):
        """
        Assesses PII in campaign content for an erasure request. REQ-DRH-004.
        :param content_submission_id: ID of influence_gen.content_submission
        :param influencer_id: ID of the influencer requesting erasure (for context)
        :return: dict with assessment (e.g., {'can_delete': bool, 'reason': str, 'usage_rights': str})
        """
        submission = self.env['influence_gen.content_submission'].browse(content_submission_id)
        influencer = self.env['influence_gen.influencer_profile'].browse(influencer_id)

        if not submission.exists():
            raise UserError(f"Content Submission {content_submission_id} not found.")
        if not influencer.exists():
            raise UserError(f"Influencer {influencer_id} not found.")
        
        if submission.influencer_profile_id != influencer:
            raise UserError("Content submission does not belong to the specified influencer.")

        campaign = submission.campaign_id
        assessment = {
            'submission_id': submission.id,
            'influencer_id': influencer.id,
            'can_delete_or_anonymize': False, # Default to no action
            'reason': "Initial assessment",
            'usage_rights_description': campaign.usage_rights_description if campaign else "N/A (No campaign linked)",
            'usage_rights_duration_months': campaign.usage_rights_duration_months if campaign else "N/A",
            'campaign_status': campaign.status if campaign else "N/A"
        }

        if not campaign:
            assessment['can_delete_or_anonymize'] = True # No campaign, no usage rights conflict
            assessment['reason'] = "No campaign linked to content, can be processed per general PII policy."
        else:
            # Simplified logic: Check if usage rights duration has expired
            # More complex logic would involve checking if campaign is active, specific contractual terms etc.
            rights_expired = False
            if campaign.usage_rights_duration_months and campaign.end_date:
                # Assuming end_date marks the start of usage rights period effectively
                # Or a specific content publication date if available
                usage_expiry_date = fields.Date.from_string(campaign.end_date) + relativedelta(months=campaign.usage_rights_duration_months)
                if fields.Date.today() > usage_expiry_date:
                    rights_expired = True
            
            if rights_expired:
                assessment['can_delete_or_anonymize'] = True
                assessment['reason'] = "Campaign usage rights appear to have expired."
            elif campaign.status in ['completed', 'archived', 'cancelled'] and not campaign.usage_rights_duration_months: # No specific duration, campaign over
                assessment['can_delete_or_anonymize'] = True
                assessment['reason'] = f"Campaign status is '{campaign.status}' and no specific usage duration defined."
            else:
                assessment['reason'] = f"Campaign '{campaign.name}' (status: {campaign.status}) may still have active usage rights. Manual review required. Duration: {campaign.usage_rights_duration_months} months."

        # Log assessment
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PII_CONTENT_ERASURE_ASSESSMENT',
            actor_user_id=self.env.user.id, # System or admin performing assessment
            action_performed='ASSESS',
            target_object=submission,
            details_dict=assessment
        )
        
        # This service provides assessment. Actual deletion/anonymization would be a separate action
        # potentially triggered by an admin via a wizard based on this assessment.
        return assessment


    def apply_legal_hold(self, model_name, record_ids, hold_reason, applied_by_user_id):
        """
        Applies a legal hold to specified records. REQ-DRH-009.
        :param model_name: string, technical name of the Odoo model
        :param record_ids: list of integers, IDs of records in the model
        :param hold_reason: string, reason for the legal hold
        :param applied_by_user_id: ID of res.users applying the hold
        :return: Boolean True if successful
        """
        if not model_name or not record_ids or not hold_reason or not applied_by_user_id:
            raise UserError("Model name, record IDs, hold reason, and applier user ID are required.")

        try:
            target_model = self.env[model_name]
        except KeyError:
            raise UserError(f"Model {model_name} not found.")

        if not (hasattr(target_model, 'legal_hold_active') and hasattr(target_model, 'legal_hold_reason')):
            _logger.warning(f"Model {model_name} does not have 'legal_hold_active' or 'legal_hold_reason' fields. Cannot apply hold.")
            # Depending on strictness, could raise UserError here.
            # For now, let's log and proceed if some records in a batch might have it (though unlikely for same model)
            # This indicates a setup issue if a model is intended to be holdable.
            # return False 
            raise UserError(f"Model {model_name} is not configured for legal holds (missing required fields).")


        records = target_model.browse(record_ids)
        if not records.exists():
            _logger.warning(f"No records found for IDs {record_ids} in model {model_name}.")
            return False # Or raise UserError

        vals_to_write = {
            'legal_hold_active': True,
            'legal_hold_reason': hold_reason,
        }
        records.write(vals_to_write)

        for record in records:
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='LEGAL_HOLD_APPLIED',
                actor_user_id=applied_by_user_id,
                action_performed='APPLY_HOLD',
                target_object=record,
                details_dict={'reason': hold_reason}
            )
        _logger.info(f"Applied legal hold to {len(records)} records in {model_name}. Reason: {hold_reason}")
        return True

    def lift_legal_hold(self, model_name, record_ids, lifted_by_user_id):
        """
        Lifts a legal hold from specified records. REQ-DRH-009.
        :param model_name: string, technical name of the Odoo model
        :param record_ids: list of integers, IDs of records in the model
        :param lifted_by_user_id: ID of res.users lifting the hold
        :return: Boolean True if successful
        """
        if not model_name or not record_ids or not lifted_by_user_id:
            raise UserError("Model name, record IDs, and lifter user ID are required.")

        try:
            target_model = self.env[model_name]
        except KeyError:
            raise UserError(f"Model {model_name} not found.")

        if not (hasattr(target_model, 'legal_hold_active') and hasattr(target_model, 'legal_hold_reason')):
            _logger.warning(f"Model {model_name} does not have 'legal_hold_active' or 'legal_hold_reason' fields. Cannot lift hold.")
            # raise UserError(f"Model {model_name} is not configured for legal holds (missing required fields).")
            return False # Silently fail or raise depending on desired strictness

        records = target_model.browse(record_ids)
        if not records.exists():
            _logger.warning(f"No records found for IDs {record_ids} in model {model_name}.")
            return False

        vals_to_write = {
            'legal_hold_active': False,
            'legal_hold_reason': False, # Clear the reason
        }
        records.write(vals_to_write)
        
        for record in records:
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='LEGAL_HOLD_LIFTED',
                actor_user_id=lifted_by_user_id,
                action_performed='LIFT_HOLD',
                target_object=record,
                details_dict={}
            )
        _logger.info(f"Lifted legal hold from {len(records)} records in {model_name}.")
        return True