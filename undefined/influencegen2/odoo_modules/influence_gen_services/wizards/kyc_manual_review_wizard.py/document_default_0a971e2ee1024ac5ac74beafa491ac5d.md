# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class KycManualReviewWizard(models.TransientModel):
    _name = 'influence_gen.kyc_manual_review_wizard'
    _description = 'KYC Manual Review Wizard'

    kyc_data_id = fields.Many2one(
        'influence_gen.kyc_data', string='KYC Submission',
        required=True, readonly=True, ondelete='cascade')
    
    decision = fields.Selection([
        ('approved', 'Approve'),
        ('rejected', 'Reject'),
        ('requires_more_info', 'Request More Information')
    ], string='Decision', required=True, default='approved')

    rejection_reason_text = fields.Text(
        string='Rejection Reason / Comments',
        help="Required if decision is 'Reject'. Also used for general comments if 'Request More Information'.")
    
    required_info_text = fields.Text(
        string='Specific Information Required',
        help="Details of what additional information is needed if 'Request More Information'.")
    
    reviewer_notes = fields.Text(
        string='Internal Reviewer Notes',
        help="Internal notes for audit or future reference. Not typically sent to the influencer.")

    # REQ-IOKYC-011: Wizard for manual KYC review.

    @api.model
    def default_get(self, fields_list):
        """Load default kyc_data_id if context provides one."""
        res = super(KycManualReviewWizard, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'influence_gen.kyc_data' and self.env.context.get('active_id'):
            res['kyc_data_id'] = self.env.context.get('active_id')
        return res

    def action_confirm_review(self):
        """
        Confirms the KYC review decision and calls the OnboardingService.
        """
        self.ensure_one()
        if not self.kyc_data_id:
            raise UserError(_("No KYC Submission linked to this wizard."))

        if self.decision == 'rejected' and not self.rejection_reason_text:
            raise UserError(_("Rejection reason is required when rejecting a KYC submission."))
        if self.decision == 'requires_more_info' and not self.required_info_text:
            raise UserError(_("Details of required information are necessary when requesting more info."))

        reviewer_user_id = self.env.user.id
        notes_for_service = self.reviewer_notes # Internal notes
        
        reason_or_required_info = None
        if self.decision == 'rejected':
            reason_or_required_info = self.rejection_reason_text
        elif self.decision == 'requires_more_info':
            reason_or_required_info = self.required_info_text
            if self.rejection_reason_text: # Append general comments if provided
                 notes_for_service = (notes_for_service or "") + _("\nGeneral Comments: ") + self.rejection_reason_text


        _logger.info(
            f"KYC Manual Review Wizard: Confirming review for KYC Data ID {self.kyc_data_id.id}, "
            f"Decision: {self.decision}, Reviewer: {reviewer_user_id}"
        )

        try:
            onboarding_service = self.env['influence_gen.services.onboarding']
            onboarding_service.handle_kyc_review_decision(
                kyc_data_id=self.kyc_data_id.id,
                decision=self.decision,
                reviewer_user_id=reviewer_user_id,
                notes=notes_for_service, # Internal notes
                required_info=reason_or_required_info # Public facing reason/request
            )
            
            # Post a message on the kyc_data record for traceability from wizard
            self.kyc_data_id.message_post(body=_(
                "Manual review processed via wizard. Decision: %s. Reviewer Notes: %s. Public Feedback/Reason: %s"
            ) % (self.decision, notes_for_service or _('N/A'), reason_or_required_info or _('N/A')))

        except Exception as e:
            _logger.error(f"Error calling OnboardingService from KYC wizard: {e}")
            raise UserError(_("An error occurred while processing the KYC review decision: %s") % str(e))

        # Return action to close wizard and potentially refresh view
        # This depends on how the wizard is called.
        # If called from a button on kyc_data form view, a simple close might be enough.
        return {'type': 'ir.actions.act_window_close'}