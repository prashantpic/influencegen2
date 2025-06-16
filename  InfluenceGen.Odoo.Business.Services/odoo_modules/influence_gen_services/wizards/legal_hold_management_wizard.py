from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from ..services.data_management_service import DataManagementService # Adjusted path

import logging
_logger = logging.getLogger(__name__)

class LegalHoldManagementWizard(models.TransientModel):
    _name = 'influence_gen.legal_hold_management_wizard'
    _description = "Legal Hold Management Wizard"

    _target_model_selection = [
        ('influence_gen.influencer_profile', 'Influencer Profile'),
        ('influence_gen.campaign', 'Campaign'),
        ('influence_gen.campaign_application', 'Campaign Application'),
        ('influence_gen.content_submission', 'Content Submission'),
        ('influence_gen.generated_image', 'Generated Image'),
        ('influence_gen.kyc_data', 'KYC Data'),
        # Add other relevant models here that can be subject to legal hold
    ]

    target_model_selection = fields.Selection(
        selection=_target_model_selection,
        string="Target Model",
        required=True,
        help="Select the Odoo model for which to apply or lift a legal hold."
    )
    target_record_ids_char = fields.Char(
        string="Record IDs (comma-separated)",
        required=True,
        help="Enter a comma-separated list of database IDs for the records in the selected model."
    )
    hold_reason = fields.Text(
        string="Reason for Hold/Lift",
        required=True,
        help="Provide a clear reason for applying or lifting the legal hold. This will be audited."
    )
    action_type = fields.Selection(
        [('apply', 'Apply Hold'), ('lift', 'Lift Hold')],
        string="Action",
        required=True,
        default='apply',
        help="Choose whether to apply a new legal hold or lift an existing one."
    )

    @api.constrains('target_record_ids_char')
    def _check_target_record_ids_char(self):
        for wizard in self:
            if wizard.target_record_ids_char:
                try:
                    ids = [int(x.strip()) for x in wizard.target_record_ids_char.split(',') if x.strip()]
                    if not ids:
                        raise ValidationError("Record IDs cannot be empty if provided.")
                    if any(not isinstance(id_val, int) or id_val <= 0 for id_val in ids):
                        raise ValidationError("All Record IDs must be positive integers.")
                except ValueError:
                    raise ValidationError("Record IDs must be a comma-separated list of numbers.")

    def action_process_legal_hold(self) -> dict:
        """
        Processes the legal hold action (apply or lift) based on wizard parameters.
        REQ-DRH-009: Implement a mechanism to apply and lift legal holds on specific data entities.
        """
        self.ensure_one()

        if not self.target_model_selection or not self.target_record_ids_char or not self.hold_reason:
            raise UserError("Target Model, Record IDs, and Reason are required.")

        try:
            record_ids = [int(x.strip()) for x in self.target_record_ids_char.split(',') if x.strip()]
            if not record_ids:
                raise UserError("Please provide at least one Record ID.")
        except ValueError:
            raise UserError("Invalid format for Record IDs. Please use comma-separated numbers.")

        data_management_service = DataManagementService(self.env)
        applied_by_user_id = self.env.user.id
        success = False
        log_action = 'APPLY_LEGAL_HOLD' if self.action_type == 'apply' else 'LIFT_LEGAL_HOLD'

        try:
            if self.action_type == 'apply':
                _logger.info(
                    "Applying legal hold via wizard. Model: %s, IDs: %s, Reason: %s, User: %s",
                    self.target_model_selection, record_ids, self.hold_reason, applied_by_user_id
                )
                success = data_management_service.apply_legal_hold(
                    model_name=self.target_model_selection,
                    record_ids=record_ids,
                    hold_reason=self.hold_reason,
                    applied_by_user_id=applied_by_user_id
                )
            elif self.action_type == 'lift':
                _logger.info(
                    "Lifting legal hold via wizard. Model: %s, IDs: %s, Reason: %s, User: %s",
                    self.target_model_selection, record_ids, self.hold_reason, applied_by_user_id # Reason is also useful for lifting
                )
                success = data_management_service.lift_legal_hold(
                    model_name=self.target_model_selection,
                    record_ids=record_ids,
                    lifted_by_user_id=applied_by_user_id,
                    lift_reason=self.hold_reason # Pass reason for lifting as well for audit
                )

            if success:
                message_action = "applied" if self.action_type == 'apply' else "lifted"
                message = f"Legal hold successfully {message_action} for selected records."
                
                self.env['influence_gen.audit_log_entry'].create_log(
                    event_type=log_action,
                    actor_user_id=applied_by_user_id,
                    action_performed=self.action_type.upper(),
                    target_model_name=self.target_model_selection,
                    # For multiple records, consider how to log target_record_id or summarize
                    details_dict={
                        'record_ids': record_ids,
                        'reason': self.hold_reason,
                        'model': self.target_model_selection
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
            else:
                message_action = "apply" if self.action_type == 'apply' else "lift"
                error_message = f"Failed to {message_action} legal hold. Please check logs."
                self.env['influence_gen.audit_log_entry'].create_log(
                    event_type=log_action,
                    actor_user_id=applied_by_user_id,
                    action_performed=self.action_type.upper(),
                    target_model_name=self.target_model_selection,
                    details_dict={
                        'record_ids': record_ids,
                        'reason': self.hold_reason,
                        'model': self.target_model_selection
                    },
                    outcome='failure',
                    failure_reason="Service call returned failure."
                )
                raise UserError(error_message)

        except UserError as e:
            _logger.error("UserError during legal hold processing: %s", str(e))
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type=log_action,
                actor_user_id=applied_by_user_id,
                action_performed=self.action_type.upper(),
                target_model_name=self.target_model_selection,
                details_dict={
                    'record_ids': record_ids if 'record_ids' in locals() else self.target_record_ids_char,
                    'reason': self.hold_reason,
                    'model': self.target_model_selection
                },
                outcome='failure',
                failure_reason=str(e)
            )
            raise
        except Exception as e:
            _logger.error("Exception during legal hold processing: %s", str(e), exc_info=True)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type=log_action,
                actor_user_id=applied_by_user_id,
                action_performed=self.action_type.upper(),
                target_model_name=self.target_model_selection,
                details_dict={
                    'record_ids': record_ids if 'record_ids' in locals() else self.target_record_ids_char,
                    'reason': self.hold_reason,
                    'model': self.target_model_selection
                },
                outcome='failure',
                failure_reason=f"An unexpected error occurred: {str(e)}"
            )
            raise UserError(f"An unexpected error occurred during legal hold processing: {str(e)}")

        return {'type': 'ir.actions.act_window_close'}