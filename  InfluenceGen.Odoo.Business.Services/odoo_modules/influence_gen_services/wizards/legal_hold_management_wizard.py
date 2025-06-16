from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class LegalHoldManagementWizard(models.TransientModel):
    _name = 'influence_gen.legal_hold_management_wizard'
    _description = "Legal Hold Management Wizard"

    # Define a selection of models that can be put on legal hold.
    # This list should be maintained based on relevant business models.
    TARGET_MODEL_SELECTION = [
        ('influence_gen.influencer_profile', 'Influencer Profile'),
        ('influence_gen.campaign', 'Campaign'),
        ('influence_gen.campaign_application', 'Campaign Application'),
        ('influence_gen.content_submission', 'Content Submission'),
        ('influence_gen.generated_image', 'AI Generated Image'),
        ('influence_gen.kyc_data', 'KYC Data'),
        # Add other models as they become relevant for legal holds
    ]

    target_model_selection = fields.Selection(
        selection=TARGET_MODEL_SELECTION,
        string="Target Model",
        required=True,
        help="Select the Odoo model for which records will be put on/lifted from legal hold."
    )
    target_record_ids_char = fields.Char(
        string="Record IDs (comma-separated)",
        required=True,
        help="Enter a comma-separated list of database IDs for the selected model."
    )
    hold_reason = fields.Text(
        string="Reason for Hold/Lift",
        required=True,
        help="Provide a reason for applying or lifting the legal hold. This will be logged."
    )
    action_type = fields.Selection(
        selection=[
            ('apply', 'Apply Hold'),
            ('lift', 'Lift Hold')
        ],
        string="Action",
        required=True,
        default='apply',
        help="Select whether to apply or lift the legal hold."
    )

    def _parse_record_ids(self):
        """ Parses the comma-separated string of record IDs into a list of integers. """
        self.ensure_one()
        if not self.target_record_ids_char:
            raise UserError(_("Record IDs cannot be empty."))
        try:
            record_ids = [int(rid.strip()) for rid in self.target_record_ids_char.split(',') if rid.strip()]
            if not record_ids:
                raise ValueError("No valid IDs found after parsing.")
            return record_ids
        except ValueError as e:
            raise UserError(_("Invalid Record IDs format. Please provide a comma-separated list of numbers. Error: %s") % e)

    def action_process_legal_hold(self):
        """
        Processes the legal hold action (apply or lift) based on wizard parameters.
        REQ-DRH-009
        """
        self.ensure_one()
        DataManagementService = self.env['influence_gen.services.data_management_service']
        
        try:
            record_ids = self._parse_record_ids()
            if not self.target_model_selection:
                raise UserError(_("Target Model must be selected."))
            if not self.hold_reason:
                raise UserError(_("Reason for Hold/Lift must be provided."))

            audit_details = {
                'target_model': self.target_model_selection,
                'record_ids': record_ids,
                'reason': self.hold_reason,
                'action_type': self.action_type,
            }

            if self.action_type == 'apply':
                DataManagementService.apply_legal_hold(
                    model_name=self.target_model_selection,
                    record_ids=record_ids,
                    hold_reason=self.hold_reason,
                    applied_by_user_id=self.env.user.id
                )
                message = _("Legal hold successfully APPLIED to %s records of model %s.") % (len(record_ids), self.target_model_selection)
                event_type = 'LEGAL_HOLD_APPLIED'
            elif self.action_type == 'lift':
                DataManagementService.lift_legal_hold(
                    model_name=self.target_model_selection,
                    record_ids=record_ids,
                    reason_for_lift=self.hold_reason, # SDS for service mentions `lifted_by_user_id`, reason implicit via audit
                    lifted_by_user_id=self.env.user.id
                )
                message = _("Legal hold successfully LIFTED from %s records of model %s.") % (len(record_ids), self.target_model_selection)
                event_type = 'LEGAL_HOLD_LIFTED'
            else:
                # Should not happen due to field 'required' and default
                raise UserError(_("Invalid action type selected."))

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type=event_type,
                actor_user_id=self.env.user.id,
                action_performed='EXECUTE_WIZARD',
                target_model_name=self.target_model_selection, # Log against the target model
                details_dict=audit_details,
                outcome='success'
            )
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Legal Hold Management'),
                    'message': message,
                    'sticky': False,
                    'type': 'success',
                }
            }

        except (UserError, ValidationError) as e: # Catch UserError or ValidationError raised by parsing or service
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='LEGAL_HOLD_PROCESSING_FAILURE',
                actor_user_id=self.env.user.id,
                action_performed='EXECUTE_WIZARD',
                target_model_name=self.target_model_selection if self.target_model_selection else self._name,
                details_dict={'reason': self.hold_reason, 'action_type': self.action_type, 'error': str(e)},
                outcome='failure',
                failure_reason=str(e)
            )
            raise # Re-raise the caught error to display it to the user
        except Exception as e:
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='LEGAL_HOLD_PROCESSING_UNEXPECTED_FAILURE',
                actor_user_id=self.env.user.id,
                action_performed='EXECUTE_WIZARD',
                target_model_name=self.target_model_selection if self.target_model_selection else self._name,
                details_dict={'reason': self.hold_reason, 'action_type': self.action_type, 'error': str(e)},
                outcome='failure',
                failure_reason=str(e)
            )
            raise UserError(_("An unexpected error occurred while processing the legal hold: %s") % str(e))

        return {'type': 'ir.actions.act_window_close'}