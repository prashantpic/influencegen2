import logging
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta, datetime

_logger = logging.getLogger(__name__)

class DataManagementService:
    """
    Manages data retention, archival, and legal holds.
    """

    def __init__(self, env):
        self.env = env

    def apply_data_retention_policies(self, data_category_filter=None, dry_run=False):
        """
        Applies active data retention policies.
        REQ-DRH-001, REQ-DRH-002, REQ-DRH-005, REQ-DRH-006, REQ-IPF-008, REQ-AIGS-011
        """
        _logger.info("Applying data retention policies. Dry run: %s. Category filter: %s", dry_run, data_category_filter)
        AuditLog = self.env['influence_gen.audit_log_entry']
        actor_user_id = self.env.user.id # System process, so self.env.user might be OdooBot or current cron user

        domain = [('is_active', '=', True)]
        if data_category_filter:
            domain.append(('data_category', '=', data_category_filter))
        
        policies = self.env['influence_gen.data_retention_policy'].search(domain)
        summary_of_actions = {'processed_policies': 0, 'actions_taken': 0, 'errors': 0, 'details': []}

        for policy in policies:
            summary_of_actions['processed_policies'] += 1
            _logger.info("Processing policy: %s (Model: %s, Category: %s, Period: %s days, Action: %s)",
                         policy.name, policy.model_name, policy.data_category, policy.retention_period_days, policy.disposition_action)

            if not policy.model_name:
                _logger.warning("Policy %s has no target model_name. Skipping.", policy.name)
                summary_of_actions['errors'] += 1
                summary_of_actions['details'].append({'policy': policy.name, 'error': 'No target model specified'})
                continue
            
            try:
                TargetModel = self.env[policy.model_name]
            except KeyError:
                _logger.error("Invalid model name '%s' in policy %s. Skipping.", policy.model_name, policy.name)
                summary_of_actions['errors'] += 1
                summary_of_actions['details'].append({'policy': policy.name, 'error': f'Invalid model {policy.model_name}'})
                continue

            # Determine cutoff date
            cutoff_date = fields.Datetime.now() - timedelta(days=policy.retention_period_days)
            
            # Domain to find records older than retention period
            # Assumes a 'create_date' field exists on the target model.
            # This might need to be configurable per policy if date field varies.
            target_domain = [('create_date', '<=', fields.Datetime.to_string(cutoff_date))]
            
            # Add legal hold check if applicable
            # This assumes a 'legal_hold_active' field on target models or a central LegalHold model
            # For simplicity, assume 'legal_hold_active' boolean field.
            if policy.legal_hold_overrideable and 'legal_hold_active' in TargetModel._fields:
                 target_domain.append(('legal_hold_active', '=', False))
            
            records_to_process = TargetModel.search(target_domain)
            _logger.info("Found %s records in %s matching policy %s criteria.", len(records_to_process), policy.model_name, policy.name)

            if not records_to_process:
                continue

            action_details = {'policy': policy.name, 'model': policy.model_name, 'action': policy.disposition_action, 'count': 0, 'record_ids': []}

            for record in records_to_process:
                try:
                    if dry_run:
                        _logger.info("[DRY RUN] Would %s record %s (ID: %s) from model %s.",
                                     policy.disposition_action, record.display_name, record.id, policy.model_name)
                        action_details['count'] += 1
                        action_details['record_ids'].append(record.id)
                    else:
                        disposition_details = {'original_id': record.id, 'original_name': record.display_name}
                        if policy.disposition_action == 'delete':
                            record.unlink()
                            _logger.info("Deleted record %s (ID: %s) from model %s.", disposition_details['original_name'], disposition_details['original_id'], policy.model_name)
                        
                        elif policy.disposition_action == 'anonymize':
                            # Anonymization logic is highly model-specific.
                            # Placeholder: needs a method on the target model e.g., record.action_anonymize()
                            if hasattr(record, 'action_anonymize'):
                                record.action_anonymize()
                                _logger.info("Anonymized record %s (ID: %s) from model %s.", disposition_details['original_name'], disposition_details['original_id'], policy.model_name)
                            else:
                                _logger.warning("Anonymization action not implemented for model %s. Skipping record %s.",
                                                policy.model_name, record.id)
                                continue # Don't count as action taken if not implemented

                        elif policy.disposition_action == 'archive':
                            # Archival logic: set 'active=False' if model supports it, or call infra layer
                            # REQ-DRH-007
                            if 'active' in record._fields:
                                record.write({'active': False})
                                _logger.info("Archived (active=False) record %s (ID: %s) from model %s.", disposition_details['original_name'], disposition_details['original_id'], policy.model_name)
                            else:
                                # Placeholder for calling infra layer for more complex archival
                                # self.env['influence_gen.infrastructure.integration.services'].archive_record(record)
                                _logger.warning("Standard archival (active=False) not supported by model %s. Archival for record %s skipped.",
                                                policy.model_name, record.id)
                                continue

                        AuditLog.create_log(
                            event_type='DATA_RETENTION_APPLIED',
                            actor_user_id=actor_user_id, # System
                            action_performed=policy.disposition_action.upper(),
                            target_model_name=policy.model_name, # Log model name
                            target_record_id=disposition_details['original_id'], # Log original ID
                            details_dict={'policy_name': policy.name, 'disposition_details': disposition_details},
                            outcome='success'
                        )
                        action_details['count'] += 1
                        action_details['record_ids'].append(disposition_details['original_id'])
                except Exception as e:
                    _logger.error("Error applying disposition action %s on record %s (ID: %s, Model: %s) for policy %s: %s",
                                 policy.disposition_action, record.display_name if hasattr(record,'display_name') else 'N/A', record.id, policy.model_name, policy.name, e)
                    summary_of_actions['errors'] += 1
                    AuditLog.create_log(
                        event_type='DATA_RETENTION_ERROR', actor_user_id=actor_user_id, action_performed=policy.disposition_action.upper(),
                        target_model_name=policy.model_name, target_record_id=record.id,
                        details_dict={'policy_name': policy.name, 'error': str(e)}, outcome='failure', failure_reason=str(e)
                    )
            
            if action_details['count'] > 0:
                summary_of_actions['actions_taken'] += action_details['count']
                summary_of_actions['details'].append(action_details)

        _logger.info("Data retention policy application finished. Summary: %s", summary_of_actions)
        return summary_of_actions

    def process_pii_erasure_request(self, influencer_id, data_scope_description="Full PII Erasure"):
        """
        Processes a PII erasure request for an influencer.
        REQ-DRH-003
        """
        _logger.info("Processing PII erasure request for influencer ID: %s, Scope: %s", influencer_id, data_scope_description)
        influencer = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer.exists():
            raise UserError(_("Influencer profile not found for erasure request."))

        # Check for legal holds or overriding constraints
        # Assume 'legal_hold_active' field on InfluencerProfile
        if hasattr(influencer, 'legal_hold_active') and influencer.legal_hold_active:
            _logger.warning("PII erasure for influencer %s cannot proceed due to active legal hold.", influencer.id)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='PII_ERASURE_REQUEST_DENIED_LEGAL_HOLD', actor_user_id=self.env.user.id,
                action_performed='ERASURE_DENIED', target_object=influencer,
                details_dict={'reason': 'Active legal hold'}
            )
            raise UserError(_("Cannot process PII erasure: Influencer data is under a legal hold."))

        # Perform secure deletion/anonymization
        # This is highly model-specific and needs careful implementation.
        # Example: Anonymize specific fields on InfluencerProfile
        pii_fields_to_anonymize = ['phone', 'residential_address', 'email'] # 'name' might be tricky
                                                                          # email is also login, complex.
        anonymized_values = {}
        for field_name in pii_fields_to_anonymize:
            if hasattr(influencer, field_name) and getattr(influencer, field_name):
                anonymized_values[field_name] = f"ANONYMIZED_{fields.Datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if 'email' in anonymized_values and influencer.user_id:
            # Anonymizing email is complex due to user login. May need to deactivate user or change login.
            # This is a simplification. Real PII erasure for login email is very involved.
             _logger.warning("Attempting to anonymize email for influencer %s. User login might be affected.", influencer.id)
             # influencer.user_id.write({'login': anonymized_values['email'], 'active': False}) # Example, deactivates user

        if anonymized_values:
            influencer.write(anonymized_values)
            _logger.info("Anonymized PII fields for influencer %s: %s", influencer.id, list(anonymized_values.keys()))

        # Anonymize/delete related data: KYC, Bank Accounts, Social Media (if not needed for other reasons)
        # This requires careful consideration of data relationships and legal requirements.
        # For example, if bank accounts have pending payments, they shouldn't be deleted.

        # KYCData: Typically delete or heavily redact attachments
        kyc_records = self.env['influence_gen.kyc_data'].search([('influencer_profile_id', '=', influencer.id)])
        for kyc in kyc_records:
            # kyc.document_front_attachment_id.unlink() # If direct deletion
            # kyc.document_back_attachment_id.unlink()
            # kyc.unlink() # Delete the KYC record itself
            _logger.info("PII Erasure: Handling KYC data for influencer %s (Record ID %s). Specific anonymization/deletion logic needed here.", influencer.id, kyc.id)
            # For now, let's just log and assume manual or more detailed process for attachments.
            if hasattr(kyc, 'action_anonymize_for_pii_erasure'): # If model has specific method
                kyc.action_anonymize_for_pii_erasure()
            else: # Fallback: clear notes, unlink attachments if possible
                kyc.write({'notes': _('Data erased as per PII request.')})
                if kyc.document_front_attachment_id: kyc.document_front_attachment_id.sudo().unlink() # Use sudo if access rights are an issue for system process
                if kyc.document_back_attachment_id: kyc.document_back_attachment_id.sudo().unlink()
                # Consider unlinking the KYC record itself, or anonymizing its fields.


        # BankAccount: Anonymize or delete
        bank_accounts = self.env['influence_gen.bank_account'].search([('influencer_profile_id', '=', influencer.id)])
        for acc in bank_accounts:
            # acc.unlink() or acc.action_anonymize()
            _logger.info("PII Erasure: Handling bank account data for influencer %s (Record ID %s). Specific anonymization/deletion logic needed.", influencer.id, acc.id)
            if hasattr(acc, 'action_anonymize_for_pii_erasure'):
                acc.action_anonymize_for_pii_erasure()
            else: # Fallback: clear sensitive fields.
                  # Actual encrypted fields would need to be cleared, not just the placeholder shown below
                acc.write({
                    'account_holder_name': _('Erased'),
                    'account_number_encrypted': _('Erased'),
                    'bank_name': _('Erased'),
                    # ... other fields
                })


        # Potentially deactivate the influencer profile and user account
        influencer.write({'account_status': 'inactive', 'notes': _("Account deactivated due to PII erasure request.")}) # Add a notes field if needed
        if influencer.user_id:
            influencer.user_id.write({'active': False})
            _logger.info("Deactivated user account %s for influencer %s.", influencer.user_id.login, influencer.id)


        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PII_ERASURE_REQUEST_PROCESSED',
            actor_user_id=self.env.user.id, # Admin or system processing request
            action_performed='ERASURE_PROCESSED',
            target_object=influencer,
            details_dict={'scope': data_scope_description, 'anonymized_fields': list(anonymized_values.keys())}
        )
        _logger.info("PII erasure request processed for influencer ID: %s.", influencer_id)
        return True

    def assess_pii_in_campaign_content_for_erasure(self, content_submission_id, influencer_id_requesting_erasure):
        """
        Assesses PII of a specific influencer within campaign content.
        REQ-DRH-004
        """
        _logger.info("Assessing PII in content submission ID: %s for influencer ID: %s", content_submission_id, influencer_id_requesting_erasure)
        submission = self.env['influence_gen.content_submission'].browse(content_submission_id)
        if not submission.exists():
            raise UserError(_("Content submission not found."))
        
        requesting_influencer = self.env['influence_gen.influencer_profile'].browse(influencer_id_requesting_erasure)
        if not requesting_influencer.exists():
            raise UserError(_("Requesting influencer profile not found."))

        # Check if the content was submitted by the requesting influencer
        if submission.influencer_profile_id != requesting_influencer:
            _logger.info("Content submission %s was not by influencer %s. No direct PII erasure action needed for this content by this request.",
                         submission.id, requesting_influencer.id)
            return {'assessment': 'No direct PII of requesting influencer.', 'action_taken': 'None'}

        campaign = submission.campaign_id
        usage_rights_description = "N/A"
        usage_rights_duration_months = 0
        if campaign:
            usage_rights_description = campaign.usage_rights_description
            usage_rights_duration_months = campaign.usage_rights_duration_months
        
        # This assessment would typically be presented to an admin via a wizard/UI.
        # The service provides the data for that decision.
        assessment_result = {
            'submission_id': submission.id,
            'submission_name': submission.name,
            'influencer_id': submission.influencer_profile_id.id,
            'influencer_name': submission.influencer_profile_id.name,
            'campaign_name': campaign.name if campaign else "N/A",
            'campaign_usage_rights': usage_rights_description,
            'campaign_usage_duration_months': usage_rights_duration_months,
            'contains_pii_of_requesting_influencer': True, # Since submitted by them
            'recommendation': _("Review content and usage rights. If rights expired or allow erasure, consider anonymizing/deleting content or PII within."),
            'action_taken': 'Needs Admin Review'
        }
        
        # Example: If usage rights expired (simplified check)
        # content_end_date = campaign.end_date + relativedelta(months=usage_rights_duration_months) if campaign and campaign.end_date else None
        # if content_end_date and content_end_date < fields.Date.today():
        # assessment_result['recommendation'] = _("Usage rights appear expired. Erasure/anonymization may be possible.")
        #    # If automatic action were taken (not recommended without review for content):
        #    # submission.unlink() or submission.action_anonymize_content_pii()
        #    # assessment_result['action_taken'] = 'Content Anonymized/Deleted (Example)'

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PII_CONTENT_ASSESSMENT',
            actor_user_id=self.env.user.id,
            action_performed='ASSESS',
            target_object=submission,
            details_dict={'assessment': assessment_result, 'requesting_influencer_id': requesting_influencer.id}
        )
        _logger.info("PII assessment for content submission %s completed. Result: %s", submission.id, assessment_result)
        return assessment_result


    def _set_legal_hold_flag(self, model_name, record_ids, hold_status, reason=None):
        """Internal helper to set/unset legal hold flag."""
        try:
            TargetModel = self.env[model_name]
            if 'legal_hold_active' not in TargetModel._fields or \
               ('legal_hold_reason' not in TargetModel._fields and reason): # Check if reason field exists if reason is provided
                _logger.error("Model %s does not support legal hold fields ('legal_hold_active' / 'legal_hold_reason').", model_name)
                raise UserError(_("The selected data type (%s) does not support legal holds directly.") % model_name)
        except KeyError:
            _logger.error("Invalid model name '%s' for legal hold.", model_name)
            raise UserError(_("Invalid data type specified for legal hold: %s") % model_name)
        
        records = TargetModel.browse(record_ids)
        if not records.exists():
            _logger.warning("No records found for legal hold operation in model %s with IDs %s", model_name, record_ids)
            return False # Or raise error

        update_vals = {'legal_hold_active': hold_status}
        if reason is not None and 'legal_hold_reason' in TargetModel._fields:
             update_vals['legal_hold_reason'] = reason if hold_status else None # Clear reason when lifting
        
        records.write(update_vals)
        return True


    def apply_legal_hold(self, model_name, record_ids, hold_reason, applied_by_user_id):
        """
        Applies a legal hold to specified records.
        REQ-DRH-009
        """
        _logger.info("Applying legal hold to model: %s, Records: %s, Reason: %s", model_name, record_ids, hold_reason)
        if not hold_reason:
            raise UserError(_("A reason is required to apply a legal hold."))
        
        if not self._set_legal_hold_flag(model_name, record_ids, True, reason=hold_reason):
            return False # Error handled in _set_legal_hold_flag

        # Log audit for each record or a summary
        # For simplicity, one log entry if multiple records of same type
        # Ideally, log per record or use target_object with a recordset
        details = {'model': model_name, 'record_ids': record_ids, 'reason': hold_reason}
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='LEGAL_HOLD_APPLIED',
            actor_user_id=applied_by_user_id,
            action_performed='APPLY_HOLD',
            target_model_name=model_name, # Cannot set target_object for multiple disparate records easily
            details_dict=details
        )
        _logger.info("Legal hold applied successfully.")
        return True

    def lift_legal_hold(self, model_name, record_ids, lifted_by_user_id):
        """
        Lifts a legal hold from specified records.
        REQ-DRH-009
        """
        _logger.info("Lifting legal hold from model: %s, Records: %s", model_name, record_ids)
        
        if not self._set_legal_hold_flag(model_name, record_ids, False):
            return False # Error handled in _set_legal_hold_flag

        details = {'model': model_name, 'record_ids': record_ids}
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='LEGAL_HOLD_LIFTED',
            actor_user_id=lifted_by_user_id,
            action_performed='LIFT_HOLD',
            target_model_name=model_name,
            details_dict=details
        )
        _logger.info("Legal hold lifted successfully.")
        return True