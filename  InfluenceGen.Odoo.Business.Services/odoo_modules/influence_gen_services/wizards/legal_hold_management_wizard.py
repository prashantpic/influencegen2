from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class LegalHoldManagementWizard(models.TransientModel):
    _name = 'influence_gen.legal_hold_management_wizard'
    _description = "Legal Hold Management Wizard"

    TARGET_MODEL_SELECTION = [
        ('influence_gen.influencer_profile', 'Influencer Profile'),
        ('influence_gen.campaign', 'Campaign'),
        ('influence_gen.content_submission', 'Content Submission'),
        ('influence_gen.generated_image', 'Generated Image'),
        # Add other relevant models that can be put on legal hold
    ]

    target_model_selection = fields.Selection(
        selection=TARGET_MODEL_SELECTION,
        string="Target Model",
        required=True,
    )
    target_record_ids_char = fields.Char(
        string="Record IDs (comma-separated)",
        required=True,
        help="Enter a comma-separated list of record IDs for the selected model."
    )
    hold_reason = fields.Text(
        string="Reason for Hold/Lift",
        required=True,
    )
    action_type = fields.Selection(
        [('apply', 'Apply Hold'), ('lift', 'Lift Hold')],
        string="Action",
        required=True,
    )

    def _parse_record_ids(self):
        self.ensure_one()
        if not self.target_record_ids_char:
            raise ValidationError(_("Record IDs cannot be empty."))
        try:
            record_ids = [int(rid.strip()) for rid in self.target_record_ids_char.split(',') if rid.strip()]
            if not record_ids:
                raise ValidationError(_("No valid Record IDs provided."))
            return record_ids
        except ValueError:
            raise ValidationError(_("Record IDs must be a comma-separated list of numbers."))

    def action_process_legal_hold(self):
        """
        Processes the legal hold action (apply or lift) based on wizard parameters.
        REQ-DRH-009
        """
        self.ensure_one()
        DataManagementService = self.env['influence_gen.services.data_management_service'] # Assuming service is registered

        try:
            record_ids = self._parse_record_ids()
            # As per SDS, assuming DataManagementService can be instantiated with env
            data_management_service_instance = DataManagementService.new(env=self.env)

            success = False
            if self.action_type == 'apply':
                success = data_management_service_instance.apply_legal_hold(
                    model_name=self.target_model_selection,
                    record_ids=record_ids,
                    hold_reason=self.hold_reason,
                    applied_by_user_id=self.env.user.id
                )
            elif self.action_type == 'lift':
                # The SDS method signature for lift_legal_hold is (self, model_name, record_ids, lifted_by_user_id)
                # It does not take hold_reason, but the wizard has it. We will pass lifted_by_user_id.
                success = data_management_service_instance.lift_legal_hold(
                    model_name=self.target_model_selection,
                    record_ids=record_ids,
                    lifted_by_user_id=self.env.user.id
                    # lifted_reason=self.hold_reason, # If service method is updated to accept it
                )
            
            if success:
                action_performed = "applied" if self.action_type == 'apply' else "lifted"
                message = _("Legal hold successfully %s for selected records.") % action_performed
                notif_type = 'success'
            else:
                message = _("Failed to process legal hold action. Check logs for details.")
                notif_type = 'warning'
                
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Legal Hold Process'),
                    'message': message,
                    'sticky': False,
                    'type': notif_type,
                }
            }

        except ValidationError as ve:
             return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Validation Error'),
                    'message': str(ve),
                    'sticky': True,
                    'type': 'danger',
                }
            }
        except Exception as e:
            # Log the exception e
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Error'),
                    'message': _("Failed to process legal hold: %s") % str(e),
                    'sticky': True,
                    'type': 'danger',
                }
            }