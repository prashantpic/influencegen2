# -*- coding: utf-8 -*-
import logging
import json
from datetime import datetime, timedelta
from odoo import _, api, fields
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class RetentionAndLegalHoldService:
    """
    Service class for managing data retention policies, disposition, archival, and legal holds.
    """

    def __init__(self, env):
        """
        Initializes the service with the Odoo environment.
        :param env: Odoo Environment
        """
        self.env = env

    def get_retention_policy(self, data_category_key):
        """
        Fetches retention period and disposition action from PlatformSetting.
        :param data_category_key: str, e.g., 'retention.pii.inactive_influencer_days'
                                   or 'retention.generated_image.personal_use'
        :return: dict like {'period_days': 365, 'action': 'anonymize', 'is_active': True} or None
        REQ-DRH-001
        """
        _logger.debug(f"Fetching retention policy for key: {data_category_key}")
        # Example: A PlatformSetting key could be 'retention.pii.inactive_influencer'
        # Its value could be a JSON string: {"period_days": 2555, "action": "anonymize", "is_active": true}
        
        setting_value_json = self.env['influence_gen.platform_setting'].get_setting(data_category_key)
        if not setting_value_json:
            _logger.warning(f"No retention policy found for key: {data_category_key}")
            return None
        
        try:
            policy_details = json.loads(setting_value_json)
            if not isinstance(policy_details, dict) or \
               'period_days' not in policy_details or \
               'action' not in policy_details:
                _logger.error(f"Invalid retention policy format for key {data_category_key}: {policy_details}")
                return None
            
            policy_details.setdefault('is_active', True) # Default to active if not specified
            return policy_details
            
        except json.JSONDecodeError:
            _logger.error(f"Failed to parse retention policy JSON for key {data_category_key}: {setting_value_json}")
            return None

    def apply_retention_policies_automated(self):
        """
        CRON JOB METHOD: Iterates through configured data categories and applies retention.
        - Gets policy via get_retention_policy().
        - Finds records older than period_days NOT under legal_hold_status = True.
        - Performs disposition action (delete, anonymize, archive).
        - Logs disposition actions.
        REQ-DRH-002, REQ-DRH-006, REQ-ATEL-007
        """
        _logger.info("Starting automated application of data retention policies.")
        
        # Example data categories and their corresponding PlatformSetting keys for policies
        # and model details. This should be made more configurable.
        data_categories_config = [
            {
                'key_prefix': 'retention.pii.inactive_influencer', # Policy key: retention.pii.inactive_influencer_policy
                'model_name': 'influence_gen.influencer_profile',
                'date_field': 'write_date', # Or a specific 'last_activity_date' if available
                'domain_conditions': [('account_status', '=', 'inactive'), ('is_gdpr_erasure_requested', '=', False)],
                'anonymize_method': '_anonymize_profile_for_retention', # Model method
            },
            {
                'key_prefix': 'retention.generated_image.personal', # Policy key: retention.generated_image.personal_policy
                'model_name': 'influence_gen.generated_image',
                'date_field': 'create_date',
                'domain_conditions': [('retention_category', '=', 'personal_generation')],
                'anonymize_method': None, # Images are usually deleted, not anonymized
            },
            # Add more categories for audit_logs, campaign_data, etc.
             {
                'key_prefix': 'retention.audit_log.general',
                'model_name': 'influence_gen.audit_log',
                'date_field': 'timestamp',
                'domain_conditions': [], # Apply to all general audit logs after period
                'anonymize_method': None, # Usually delete or archive
            },
        ]

        for category_config in data_categories_config:
            policy_key = f"{category_config['key_prefix']}_policy" # Convention for the setting key
            policy = self.get_retention_policy(policy_key)

            if not policy or not policy.get('is_active', True):
                _logger.info(f"Skipping retention for category {category_config['key_prefix']} as policy is inactive or not found.")
                continue

            model_name = category_config['model_name']
            date_field = category_config['date_field']
            period_days = policy.get('period_days', 3650) # Default to 10 years if not set
            action = policy.get('action', 'archive') # Default action

            _logger.info(f"Processing category: {category_config['key_prefix']} for model {model_name}, action: {action}, period: {period_days} days.")

            cutoff_date = datetime.now() - timedelta(days=period_days)
            
            domain = [(date_field, '<=', fields.Datetime.to_string(cutoff_date))]
            if category_config.get('domain_conditions'):
                domain.extend(category_config['domain_conditions'])
            
            # Ensure 'legal_hold_status' field exists or handle absence
            Model = self.env[model_name]
            if 'legal_hold_status' in Model._fields:
                domain.append(('legal_hold_status', '=', False))
            
            records_to_process = Model.search(domain)
            _logger.info(f"Found {len(records_to_process)} records in {model_name} matching retention criteria for category {category_config['key_prefix']}.")

            for record in records_to_process:
                try:
                    if action == 'delete':
                        _logger.info(f"Deleting record ID {record.id} from {model_name} as per retention policy.")
                        record.unlink()
                        # Log deletion in AuditLog (BaseAuditMixin might not cover service-driven unlink well)
                        self.env['influence_gen.audit_log'].create({
                            'event_type': f'{model_name}.retention.delete',
                            'target_model': model_name,
                            'target_res_id': record.id, # record.id might not be available after unlink, capture before
                            'action': 'retention_delete',
                            'details_json': json.dumps({'policy_key': policy_key, 'record_name': record.display_name or str(record.id)}),
                            'outcome': 'success',
                        })
                    elif action == 'anonymize':
                        anonymize_method_name = category_config.get('anonymize_method')
                        if anonymize_method_name and hasattr(record, anonymize_method_name):
                            _logger.info(f"Anonymizing record ID {record.id} from {model_name} as per retention policy.")
                            getattr(record, anonymize_method_name)()
                            self.env['influence_gen.audit_log'].create({
                                'event_type': f'{model_name}.retention.anonymize',
                                'target_model': model_name, 'target_res_id': record.id,
                                'action': 'retention_anonymize', 'details_json': json.dumps({'policy_key': policy_key}),
                                'outcome': 'success',
                            })
                        else:
                             _logger.warning(f"Anonymization method '{anonymize_method_name}' not found or not specified for model {model_name}. Skipping record {record.id}.")
                    elif action == 'archive':
                        # Placeholder for archival logic
                        _logger.info(f"Archiving record ID {record.id} from {model_name} (conceptual).")
                        # record.write({'active': False}) # Example of simple archival
                        # self.archive_data_batch(model_name, [('id', '=', record.id)], archive_target_info={}) # Call more specific archive
                        self.env['influence_gen.audit_log'].create({
                            'event_type': f'{model_name}.retention.archive',
                            'target_model': model_name, 'target_res_id': record.id,
                            'action': 'retention_archive', 'details_json': json.dumps({'policy_key': policy_key}),
                            'outcome': 'success',
                        })
                    else:
                        _logger.warning(f"Unknown retention action '{action}' for policy {policy_key}. Skipping record {record.id}.")
                except Exception as e:
                    _logger.error(f"Error applying retention action '{action}' to record {record.id} of {model_name}: {e}")
                    self.env['influence_gen.audit_log'].create({
                        'event_type': f'{model_name}.retention.{action}.error',
                        'target_model': model_name, 'target_res_id': record.id,
                        'action': f'retention_{action}_error', 'details_json': json.dumps({'policy_key': policy_key, 'error': str(e)}),
                        'outcome': 'failure', 'failure_reason': str(e),
                    })
        _logger.info("Finished automated application of data retention policies.")
        return True

    def process_manual_erasure_request(self, model_name, record_id, requestor_user_id, justification_text):
        """
        Processes a manual data erasure request (e.g., GDPR Right to be Forgotten).
        - Finds record. Checks legal_hold_status.
        - Checks against financial record keeping rules, campaign usage rights (if applicable).
        - If clear, performs deletion or anonymization.
        - Logs comprehensively.
        :return: bool (success/failure)
        REQ-DRH-003, REQ-DRH-004
        """
        _logger.info(f"Processing manual erasure request for model {model_name}, record ID {record_id}, by user {requestor_user_id}")
        Model = self.env[model_name]
        if not Model:
            raise UserError(_("Model %s not found.") % model_name)
        record = Model.browse(record_id)
        if not record.exists():
            raise UserError(_("Record ID %s in model %s not found.") % (record_id, model_name))

        AuditLog = self.env['influence_gen.audit_log']
        log_details = {
            'requestor_user_id': requestor_user_id,
            'justification': justification_text,
            'target_display_name': record.display_name or str(record.id)
        }

        # Check for legal hold
        if hasattr(record, 'legal_hold_status') and record.legal_hold_status:
            _logger.warning(f"Erasure denied for {model_name} ID {record_id}: Record is under legal hold.")
            AuditLog.create({
                'event_type': f'{model_name}.erasure_request.denied', 'user_id': requestor_user_id,
                'target_model': model_name, 'target_res_id': record_id, 'action': 'erasure_denied_legal_hold',
                'details_json': json.dumps(log_details), 'outcome': 'failure', 'failure_reason': 'Legal Hold Active',
            })
            raise UserError(_("Cannot erase record: It is currently under a legal hold."))

        # Add other business rule checks here (e.g., financial records, active contracts)
        # For example, if it's an InfluencerProfile with recent payments:
        if model_name == 'influence_gen.influencer_profile':
            recent_payments = self.env['influence_gen.payment_record'].search_count([
                ('influencer_profile_id', '=', record.id),
                ('status', 'not in', ['failed', 'cancelled']), # Consider only active/paid
                ('paid_date', '>=', fields.Date.today() - timedelta(days=365*2)) # Example: within last 2 years
            ])
            if recent_payments > 0: # This rule needs to be defined by policy
                 _logger.warning(f"Erasure needs review for {model_name} ID {record_id}: Recent financial transactions exist.")
                 # Could flag for manual review instead of outright denial, or deny based on policy.
                 # For now, let's assume this requires admin override or further review.
                 # raise UserError(_("Cannot automatically erase: Recent financial activity. Please review manually."))


        # Perform erasure (anonymization or deletion based on model type or policy)
        try:
            # Prefer model-specific anonymization if available
            anonymize_method_name = '_anonymize_for_erasure_request' # Convention
            if hasattr(record, anonymize_method_name):
                getattr(record, anonymize_method_name)()
                action_taken = 'anonymized'
            else: # Fallback to unlink
                record_display_name_before_unlink = record.display_name or str(record.id) # Capture before unlink
                log_details['target_display_name_before_unlink'] = record_display_name_before_unlink
                record.unlink()
                action_taken = 'deleted'
            
            _logger.info(f"Record {model_name} ID {record_id} successfully {action_taken} for erasure request.")
            AuditLog.create({
                'event_type': f'{model_name}.erasure_request.processed', 'user_id': requestor_user_id,
                'target_model': model_name, 'target_res_id': record_id, # ID might be gone if unlinked
                'action': f'erasure_{action_taken}', 'details_json': json.dumps(log_details), 'outcome': 'success',
            })
            return True
        except Exception as e:
            _logger.error(f"Error during erasure of {model_name} ID {record_id}: {e}")
            AuditLog.create({
                'event_type': f'{model_name}.erasure_request.error', 'user_id': requestor_user_id,
                'target_model': model_name, 'target_res_id': record_id, 'action': 'erasure_error',
                'details_json': json.dumps({**log_details, 'error': str(e)}),
                'outcome': 'failure', 'failure_reason': str(e),
            })
            raise UserError(_("Failed to process erasure request: %s") % str(e))


    def archive_data_batch(self, model_name, domain, archive_target_info):
        """
        Exports data matching domain from model_name to a secure archival storage.
        Marks records as archived. Logs. This is a conceptual method.
        :param archive_target_info: dict, info about where/how to archive (e.g., S3 bucket, format)
        REQ-DRH-007
        """
        _logger.info(f"Archiving data batch for model {model_name}, Domain: {domain}, Target: {archive_target_info}")
        # 1. Fetch records based on domain.
        # 2. Export records to a specified format (e.g., CSV, JSONL, XML).
        #    - This might use Odoo's export features or custom serialization.
        # 3. Transfer exported data to the archive_target (e.g., upload to S3 via REPO-IGIA-004).
        # 4. Mark records in Odoo as archived (e.g., set 'active = False', or a specific 'archived_at' date).
        # 5. Log the archival operation.

        # This is a placeholder for a complex process.
        # Example for simple marking:
        # records = self.env[model_name].search(domain)
        # records.write({'active': False, 'archived_info_json': json.dumps(archive_target_info)}) # Example
        # for record in records:
        #     self.env['influence_gen.audit_log'].create({
        #         'event_type': f'{model_name}.archived',
        #         'target_model': model_name, 'target_res_id': record.id,
        #         'action': 'archive_data', 'details_json': json.dumps({'target': archive_target_info}),
        #         'outcome': 'success',
        #     })
        _logger.warning("Data archival is a conceptual method here. Full implementation is complex.")
        return True

    def place_legal_hold(self, model_name, record_id_or_domain, hold_reason, placed_by_user_id):
        """
        Places a legal hold on specified records.
        Sets legal_hold_status = True. Logs in AuditLog.
        :return: bool (True if any record was updated)
        REQ-DRH-008, REQ-DRH-009
        """
        _logger.info(f"Placing legal hold on {model_name}, Target: {record_id_or_domain}, Reason: {hold_reason}")
        Model = self.env[model_name]
        if not Model or not hasattr(Model, '_fields') or 'legal_hold_status' not in Model._fields:
            raise UserError(_("Model %s does not exist or does not support legal hold status.") % model_name)

        if isinstance(record_id_or_domain, int): # Single record ID
            domain = [('id', '=', record_id_or_domain)]
        elif isinstance(record_id_or_domain, list): # Odoo domain
            domain = record_id_or_domain
        else:
            raise UserError(_("Invalid target for legal hold. Must be record ID or domain."))

        records_to_hold = Model.search(domain)
        if not records_to_hold:
            _logger.warning(f"No records found matching criteria for legal hold on {model_name}.")
            return False

        updated_count = 0
        for record in records_to_hold:
            if not record.legal_hold_status: # Only update if not already on hold by this reason (or simplify)
                record.write({'legal_hold_status': True})
                self.env['influence_gen.audit_log'].create({
                    'event_type': f'{model_name}.legal_hold.placed', 'user_id': placed_by_user_id,
                    'target_model': model_name, 'target_res_id': record.id,
                    'action': 'legal_hold_place',
                    'details_json': json.dumps({'reason': hold_reason, 'record_name': record.display_name or str(record.id)}),
                    'outcome': 'success',
                })
                updated_count += 1
        
        _logger.info(f"Placed legal hold on {updated_count} records in {model_name}.")
        return updated_count > 0

    def lift_legal_hold(self, model_name, record_id_or_domain, lifted_by_user_id, lift_reason):
        """
        Lifts a legal hold from specified records.
        Sets legal_hold_status = False. Logs in AuditLog.
        :return: bool (True if any record was updated)
        REQ-DRH-008, REQ-DRH-009
        """
        _logger.info(f"Lifting legal hold on {model_name}, Target: {record_id_or_domain}, Reason: {lift_reason}")
        Model = self.env[model_name]
        if not Model or not hasattr(Model, '_fields') or 'legal_hold_status' not in Model._fields:
            raise UserError(_("Model %s does not exist or does not support legal hold status.") % model_name)

        if isinstance(record_id_or_domain, int):
            domain = [('id', '=', record_id_or_domain)]
        elif isinstance(record_id_or_domain, list):
            domain = record_id_or_domain
        else:
            raise UserError(_("Invalid target for lifting legal hold. Must be record ID or domain."))

        records_to_lift = Model.search(domain)
        if not records_to_lift:
            _logger.warning(f"No records found matching criteria for lifting legal hold on {model_name}.")
            return False

        updated_count = 0
        for record in records_to_lift:
            if record.legal_hold_status: # Only update if currently on hold
                record.write({'legal_hold_status': False})
                self.env['influence_gen.audit_log'].create({
                    'event_type': f'{model_name}.legal_hold.lifted', 'user_id': lifted_by_user_id,
                    'target_model': model_name, 'target_res_id': record.id,
                    'action': 'legal_hold_lift',
                    'details_json': json.dumps({'reason': lift_reason, 'record_name': record.display_name or str(record.id)}),
                    'outcome': 'success',
                })
                updated_count += 1
        
        _logger.info(f"Lifted legal hold from {updated_count} records in {model_name}.")
        return updated_count > 0

    def check_legal_hold(self, model_name, record_id):
        """
        Checks if a specific record is under legal hold.
        :return: bool
        REQ-DRH-009
        """
        Model = self.env[model_name]
        if not Model or not hasattr(Model, '_fields') or 'legal_hold_status' not in Model._fields:
            _logger.warning(f"Model {model_name} does not support legal hold status. Assuming not on hold.")
            return False
        
        record = Model.browse(record_id)
        if not record.exists():
            _logger.warning(f"Record {model_name} ID {record_id} not found for legal hold check.")
            return False # Or raise error

        return record.legal_hold_status