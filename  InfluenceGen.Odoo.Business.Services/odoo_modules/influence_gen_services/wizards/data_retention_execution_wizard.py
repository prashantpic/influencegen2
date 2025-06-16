from odoo import api, fields, models, _
from odoo.exceptions import UserError

class DataRetentionExecutionWizard(models.TransientModel):
    _name = 'influence_gen.data_retention_execution_wizard'
    _description = "Manual Data Retention Execution Wizard"

    # Selection choices for data_category should ideally match those in
    # 'influence_gen.data_retention_policy' model.
    # From SDS 3.3.17: e.g., [('pii_influencer', 'Influencer PII'), ('kyc_documents', 'KYC Documents'), ... ('audit_logs', 'Audit Logs')]
    # Let's use a subset or make it more generic for the wizard, or expect it to be populated dynamically if possible in a real scenario
    # For now, using the list provided in the older SDS File Structure description:
    # [('pii', 'PII'), ('kyc', 'KYC Documents'), ('campaign_data', 'Campaign Data'), ('generated_images', 'Generated Images'), ('n8n_logs', 'N8N Logs'), ('system_logs', 'System Logs'), ('audit_logs', 'Audit Logs')]
    DATA_CATEGORY_SELECTION = [
        ('pii_influencer', 'Influencer PII'),
        ('kyc_documents', 'KYC Documents'),
        ('campaign_data', 'Campaign Data'),
        ('generated_images', 'AI Generated Images'),
        ('audit_logs', 'Audit Logs'),
        # Add other categories as defined in DataRetentionPolicy model
    ]

    data_category_filter = fields.Selection(
        selection=DATA_CATEGORY_SELECTION,
        string="Data Category to Process",
        help="Select the data category to apply retention policies for."
    )
    model_name_filter = fields.Char(
        string="Target Model (Optional)",
        help="Technical name of the Odoo model to filter by (e.g., 'influence_gen.influencer_profile')."
    )
    older_than_date_filter = fields.Date(
        string="Process Data Older Than",
        help="Only process records created before this date. If blank, processes all eligible records."
    )
    dry_run = fields.Boolean(
        string="Dry Run (Log actions only)",
        default=True,
        help="If checked, the system will only log what actions would be taken, without actually performing them."
    )

    def action_execute_retention(self):
        """
        Triggers the data retention process based on the wizard's parameters.
        REQ-DRH-002
        """
        self.ensure_one()
        DataManagementService = self.env['influence_gen.services.data_management_service']
        
        # The DataManagementService.apply_data_retention_policies method in SDS 3.4.6
        # has parameters: self, data_category=None, dry_run=False
        # It internally iterates through policies. The wizard provides filters to potentially
        # narrow down which policies or records are considered by the service if the service is enhanced
        # to accept these finer-grained filters.
        # For now, passing data_category and dry_run. The service would then filter policies based on this category.
        
        try:
            # The service method `apply_data_retention_policies` is expected to handle
            # filtering by data_category and then further by model_name_filter and older_than_date_filter
            # if such logic is built into it. The SDS for the service method is generic.
            # We pass all available filters from the wizard.
            summary = DataManagementService.apply_data_retention_policies(
                data_category=self.data_category_filter,
                model_name=self.model_name_filter if self.model_name_filter else None,
                older_than_date=self.older_than_date_filter if self.older_than_date_filter else None,
                dry_run=self.dry_run
            )
            
            # Create an audit log for the manual execution trigger
            details_dict = {
                'data_category_filter': self.data_category_filter,
                'model_name_filter': self.model_name_filter,
                'older_than_date_filter': str(self.older_than_date_filter) if self.older_than_date_filter else None,
                'dry_run': self.dry_run,
                'summary_from_service': summary, # If service returns a summary
            }
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='DATA_RETENTION_MANUAL_EXECUTION',
                actor_user_id=self.env.user.id,
                action_performed='EXECUTE_WIZARD',
                target_model_name=self._name,
                target_record_id=self.id,
                details_dict=details_dict,
                outcome='success'
            )

            # Notify user
            # For simplicity, returning a notification action or just closing.
            # Odoo's bus.bus notification system could be used for more detailed feedback.
            if self.dry_run:
                message = _("Data retention dry run initiated. Check logs for details. Summary: %s", summary)
            else:
                message = _("Data retention process initiated. Summary: %s", summary)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Data Retention'),
                    'message': message,
                    'sticky': False,
                    'type': 'info',
                }
            }

        except Exception as e:
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='DATA_RETENTION_MANUAL_EXECUTION_FAILURE',
                actor_user_id=self.env.user.id,
                action_performed='EXECUTE_WIZARD',
                target_model_name=self._name,
                target_record_id=self.id,
                outcome='failure',
                failure_reason=str(e)
            )
            raise UserError(_("Failed to execute data retention: %s") % str(e))

        return {'type': 'ir.actions.act_window_close'}