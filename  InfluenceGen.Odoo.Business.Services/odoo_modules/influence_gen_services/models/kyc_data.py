# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InfluenceGenKycData(models.Model):
    _name = 'influence_gen.kyc_data'
    _description = "Influencer KYC Data Submission"
    _order = 'create_date desc'

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Influencer Profile",
        required=True,
        ondelete='cascade',
        index=True
    )
    document_type = fields.Selection([
        ('passport', 'Passport'),
        ('driver_license', "Driver's License"),
        ('national_id', 'National ID')
        # Add other relevant document types
    ], string="Document Type", required=True)
    document_front_attachment_id = fields.Many2one(
        'ir.attachment',
        string="Document Front",
        required=True,
        ondelete='restrict' # Or 'set null' if attachment deletion should not delete KYC record
    )
    document_back_attachment_id = fields.Many2one(
        'ir.attachment',
        string="Document Back (Optional)",
        ondelete='restrict' # Or 'set null'
    )
    submission_date = fields.Datetime(string="Submission Date", default=fields.Datetime.now, readonly=True)
    verification_method = fields.Selection([
        ('manual', 'Manual Review'),
        ('third_party_api', 'Third-Party API')
    ], string="Verification Method", required=True)
    verification_status = fields.Selection([
        ('pending', 'Pending Review'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('needs_more_info', 'Needs More Info')
    ], string="Verification Status", default='pending', required=True, tracking=True, index=True)
    reviewer_user_id = fields.Many2one('res.users', string="Reviewed By", readonly=True, index=True)
    reviewed_at = fields.Datetime(string="Reviewed At", readonly=True)
    notes = fields.Text(string="Reviewer Notes / Reason for Rejection / Info Requested")
    third_party_reference_id = fields.Char(string="Third-Party Verification ID", copy=False) # If using third-party API

    def action_submit_for_review(self) -> None:
        """
        Marks the submission as ready for review.
        """
        for record in self:
            if record.verification_status != 'pending':
                raise UserError(_("Only KYC submissions in 'Pending Review' status can be submitted for review."))
            record.write({'verification_status': 'in_review'})
            record.influencer_profile_id.update_kyc_status('in_review')
            
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='KYC_SUBMITTED_FOR_REVIEW',
                actor_user_id=record.influencer_profile_id.user_id.id, # Action by influencer
                action_performed='SUBMIT_FOR_REVIEW',
                target_object=record
            )
            # Notify admins (handled by OnboardingService usually)

    def action_approve(self, reviewer_user_id: int, notes: str = None) -> None:
        """
        Approves the KYC submission. Called by OnboardingService or admin UI. REQ-IOKYC-005.
        """
        self.ensure_one()
        if self.verification_status not in ['in_review', 'needs_more_info']:
             raise UserError(_("KYC can only be approved if it's in 'In Review' or 'Needs More Info' state."))

        self.write({
            'verification_status': 'approved',
            'reviewer_user_id': reviewer_user_id,
            'reviewed_at': fields.Datetime.now(),
            'notes': notes
        })
        self.influencer_profile_id.update_kyc_status('approved', notes=notes)
        self.influencer_profile_id.update_onboarding_step_status('kyc_approved', True)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_APPROVED',
            actor_user_id=reviewer_user_id,
            action_performed='APPROVE_KYC',
            target_object=self,
            details_dict={'notes': notes}
        )

    def action_reject(self, reviewer_user_id: int, reason_notes: str) -> None:
        """
        Rejects the KYC submission. REQ-IOKYC-005.
        """
        self.ensure_one()
        if not reason_notes:
            raise UserError(_("A reason is required for rejecting KYC submission."))
        if self.verification_status not in ['in_review', 'needs_more_info']:
             raise UserError(_("KYC can only be rejected if it's in 'In Review' or 'Needs More Info' state."))

        self.write({
            'verification_status': 'rejected',
            'reviewer_user_id': reviewer_user_id,
            'reviewed_at': fields.Datetime.now(),
            'notes': reason_notes
        })
        self.influencer_profile_id.update_kyc_status('rejected', notes=reason_notes)
        self.influencer_profile_id.update_onboarding_step_status('kyc_approved', False) # Mark as not approved

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_REJECTED',
            actor_user_id=reviewer_user_id,
            action_performed='REJECT_KYC',
            target_object=self,
            details_dict={'reason': reason_notes}
        )

    def action_request_more_info(self, reviewer_user_id: int, info_needed_notes: str) -> None:
        """
        Requests more information for the KYC submission. REQ-IOKYC-005.
        """
        self.ensure_one()
        if not info_needed_notes:
            raise UserError(_("Details of the information needed are required."))
        if self.verification_status not in ['in_review']:
             raise UserError(_("KYC can only be marked as 'Needs More Info' if it's in 'In Review' state."))

        self.write({
            'verification_status': 'needs_more_info',
            'reviewer_user_id': reviewer_user_id,
            'reviewed_at': fields.Datetime.now(),
            'notes': info_needed_notes
        })
        self.influencer_profile_id.update_kyc_status('needs_more_info', notes=info_needed_notes)
        
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_MORE_INFO_REQUESTED',
            actor_user_id=reviewer_user_id,
            action_performed='REQUEST_MORE_INFO_KYC',
            target_object=self,
            details_dict={'info_needed': info_needed_notes}
        )