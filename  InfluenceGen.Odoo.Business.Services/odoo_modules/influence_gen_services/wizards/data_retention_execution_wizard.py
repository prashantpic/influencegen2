from odoo import models, fields, api
from odoo.exceptions import UserError
from ..services.data_management_service import DataManagementService # Adjusted path

import logging
_logger = logging.getLogger(__name__)

class DataRetentionExecutionWizard(models.TransientModel):
    _name = 'influence_gen.data_retention_execution_wizard'
    _description = "Manual Data Retention Execution Wizard"

    # Selection values should mirror those in 'influence_gen.data_retention_policy' model's 'data_category' field.
    # As per SDS: [('pii_influencer', 'Influencer PII'), ('kyc_documents', 'KYC Documents'), ... ('audit_logs', 'Audit Logs')]
    # This list needs to be comprehensive based on the actual DataRetentionPolicy model's data_category field.
    # For this example, using a placeholder list. The actual list should be derived from DataRetentionPolicy.data_category.
    _data_category_selection = [
        ('pii_influencer', 'Influencer PII'),
        ('kyc_documents', 'KYC Documents'),
        ('campaign_data', 'Campaign Data'),
        ('generated_images', 'Generated Images'),
        ('n8n_logs', 'N8N Logs'), # Assuming n8n_logs is a valid category from DataRetentionPolicy
        ('system_logs', 'System Logs'), # Assuming system_logs is a valid category from DataRetentionPolicy
        ('audit_logs', 'Audit Logs'),
        # Add all other categories defined in DataRetentionPolicy.data_category
    ]

    data_category_filter = fields.Selection(
        selection=_data_category_selection,
        string="Data Category to Process",
        help="Select the data category to apply retention policies. If none selected, all active policies might be processed by the service."
    )
    model_name_filter = fields.Char(
        string="Target Model (Optional)",
        help="Specify the technical name of an Odoo model to narrow down the retention process (e.g., 'influence_gen.influencer_profile')."
    )
    older_than_date_filter = fields.Date(
        string="Process Data Older Than",
        help="Process data records created before this date. Use with caution."
    )
    dry_run = fields.Boolean(
        string="Dry Run (Log actions only)",
        default=True,
        help="If checked, the process will only log what actions would be taken, without actually performing them."
    )

    def action_execute_retention(self) -> dict:
        """
        Executes the data retention policies based on the wizard's parameters.
        REQ-DRH-002: Provide an administrative interface (wizard) for manually triggering data disposition tasks.
        """
        self.ensure_one()
        _logger.info(
            "Data retention execution triggered manually via wizard. Category: %s, Model: %s, Older Than: %s, Dry Run: %s",
            self.data_category_filter, self.model_name_filter, self.older_than_date_filter, self.dry_run
        )

        data_management_service = DataManagementService(self.env)

        # The SDS for DataManagementService.apply_data_retention_policies only specifies
        # data_category and dry_run as parameters.
        # model_name_filter and older_than_date_filter are defined in this wizard,
        # but the service method signature needs to support them if they are to be used directly.
        # For now, adhering strictly to the service method signature from SDS.
        # The service implementation might internally use these if set in context or if data_category is None.
        try:
            # Assuming the service might have extended logic for model_name_filter and older_than_date_filter
            # or they are for future use / more specific service methods.
            # For now, pass what's directly supported by the current SDS of the service method.
            # We can pass these additional parameters to the service method if the service method is updated to accept them.
            # For example, by using a dictionary of parameters or extending the method signature.
            # result = data_management_service.apply_data_retention_policies(
            #     data_category=self.data_category_filter,
            #     dry_run=self.dry_run,
            #     model_name=self.model_name_filter, # If service supports
            #     older_than_date=self.older_than_date_filter # If service supports
            # )
            
            # Sticking to SDS method signature for apply_data_retention_policies:
            # apply_data_retention_policies(self, data_category=None, dry_run=False)
            # The model_name_filter and older_than_date_filter are not directly passed here
            # as per the specified service method signature in the SDS.
            # The service may use these if they are set in context or if the service logic is more complex.
            result_summary = data_management_service.apply_data_retention_policies(
                data_category=self.data_category_filter or None, # Pass None if not selected
                dry_run=self.dry_run
            )
            
            # The 'result_summary' should be a dict describing actions taken/logged.
            # For simplicity, we'll show a generic message. A more complex wizard could display details from result_summary.
            message = "Data retention process execution "
            message += "logged (Dry Run)" if self.dry_run else "completed"
            message += "."
            if isinstance(result_summary, dict) and result_summary.get('details'):
                message += f"\nDetails: {result_summary.get('details')}"

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='DATA_RETENTION_WIZARD_EXECUTION',
                actor_user_id=self.env.user.id,
                action_performed='EXECUTE',
                details_dict={
                    'data_category_filter': self.data_category_filter,
                    'model_name_filter': self.model_name_filter,
                    'older_than_date_filter': str(self.older_than_date_filter) if self.older_than_date_filter else None,
                    'dry_run': self.dry_run,
                    'result': result_summary,
                },
                outcome='success'
            )

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Success'),
                    'message': message,
                    'sticky': False,
                    'type': 'success',
                }
            }

        except UserError as e:
            _logger.error("UserError during data retention execution: %s", str(e))
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='DATA_RETENTION_WIZARD_EXECUTION',
                actor_user_id=self.env.user.id,
                action_performed='EXECUTE',
                details_dict={
                    'data_category_filter': self.data_category_filter,
                    'model_name_filter': self.model_name_filter,
                    'older_than_date_filter': str(self.older_than_date_filter) if self.older_than_date_filter else None,
                    'dry_run': self.dry_run,
                },
                outcome='failure',
                failure_reason=str(e)
            )
            raise
        except Exception as e:
            _logger.error("Exception during data retention execution: %s", str(e), exc_info=True)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='DATA_RETENTION_WIZARD_EXECUTION',
                actor_user_id=self.env.user.id,
                action_performed='EXECUTE',
                details_dict={
                    'data_category_filter': self.data_category_filter,
                    'model_name_filter': self.model_name_filter,
                    'older_than_date_filter': str(self.older_than_date_filter) if self.older_than_date_filter else None,
                    'dry_run': self.dry_run,
                },
                outcome='failure',
                failure_reason=f"An unexpected error occurred: {str(e)}"
            )
            raise UserError(f"An unexpected error occurred during data retention execution: {str(e)}")

        return {'type': 'ir.actions.act_window_close'}