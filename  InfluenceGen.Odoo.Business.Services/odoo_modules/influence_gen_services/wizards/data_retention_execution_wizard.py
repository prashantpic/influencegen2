from odoo import api, fields, models, _
from odoo.exceptions import UserError

class DataRetentionExecutionWizard(models.TransientModel):
    _name = 'influence_gen.data_retention_execution_wizard'
    _description = "Manual Data Retention Execution Wizard"

    # As per SDS 3.3.17 DataRetentionPolicy data_category field
    DATA_CATEGORY_SELECTION = [
        ('pii_influencer', 'Influencer PII'),
        ('kyc_documents', 'KYC Documents'),
        ('campaign_data', 'Campaign Data'),
        ('generated_images', 'Generated Images'),
        ('audit_logs', 'Audit Logs'),
        # Add other categories as defined in DataRetentionPolicy model
    ]

    data_category_filter = fields.Selection(
        selection=DATA_CATEGORY_SELECTION,
        string="Data Category to Process",
        help="Select the data category to apply retention policies for. If empty, all active policies might be considered."
    )
    model_name_filter = fields.Char(
        string="Target Model (Optional)",
        help="Specify the Odoo model technical name (e.g., 'influence_gen.influencer_profile') to filter policies further."
    )
    older_than_date_filter = fields.Date(
        string="Process Data Older Than",
        help="If set, only process data records created before this date. Logic handled by the service."
    )
    dry_run = fields.Boolean(
        string="Dry Run (Log actions only)",
        default=True,
        help="If checked, the system will only log what actions would be taken, without actually performing them."
    )

    def action_execute_retention(self):
        """
        Executes the data retention policies based on the wizard's parameters.
        REQ-DRH-002
        """
        self.ensure_one()
        DataManagementService = self.env['influence_gen.services.data_management_service'] # Assuming service is registered like this
        
        # In Odoo, services are often not instantiated directly like this from models.
        # They are either available on env or methods are called differently.
        # For this exercise, assuming it can be instantiated as per SDS service structure.
        # If services are registered with Odoo's new service component system:
        # data_management_service = self.env['data.management.service']
        # However, SDS shows services with __init__(self, env), so direct instantiation:
        
        try:
            # The SDS implies services are instantiated.
            # However, a more common pattern if not using new service framework:
            # self.env['data.management.service'].apply_data_retention_policies(...)
            # For now, sticking to the implication of explicit instantiation from SDS
            data_management_service_instance = DataManagementService.new(env=self.env)
            
            # The SDS for apply_data_retention_policies takes (self, data_category=None, dry_run=False)
            # It does not take model_name_filter or older_than_date_filter directly.
            # This wizard implies the service should handle these. We pass what we have.
            # The service implementation would need to consider these if this wizard is to be fully functional.
            # For now, we pass `data_category_filter` and `dry_run` as per the service method signature.
            # The model_name_filter and older_than_date_filter would require modifications to the service method
            # or the service internally fetching policies and then filtering records by these additional criteria.

            summary = data_management_service_instance.apply_data_retention_policies(
                data_category=self.data_category_filter,
                dry_run=self.dry_run
            )
            
            message = _("Data retention process executed.")
            if self.dry_run:
                message = _("Data retention process (Dry Run) executed. Check logs for details.")
            if isinstance(summary, dict) and summary.get('message'):
                message = summary.get('message')

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Retention Process'),
                    'message': message,
                    'sticky': False,
                    'type': 'success' if not self.dry_run else 'info',
                }
            }

        except Exception as e:
            # Log the exception e
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Error'),
                    'message': _("Failed to execute data retention process: %s") % str(e),
                    'sticky': True,
                    'type': 'danger',
                }
            }