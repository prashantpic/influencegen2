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
        # Add more as needed
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
    third_party_reference_id = fields.Char(string="Third-Party Verification ID", copy=False)

    def action_submit_for_review(self):
        """Marks the submission as ready for review."""
        for record in self:
            if record.verification_status != 'pending':
                raise UserError(_("KYC submission can only be sent for review if it's in 'Pending' state."))
            record.write({'verification_status': 'in_review'})
            record.influencer_profile_id.update_onboarding_step_status('kyc_submitted', True)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='KYC_SUBMITTED_FOR_REVIEW',
                actor_user_id=record.influencer_profile_id.user_id.id, # Submitted by influencer
                action_performed='UPDATE',
                target_object=record
            )
            # Notify admins (implementation might be via mail.activity or custom notification service)
            # Example: self.activity_schedule(...) for admin group
        return True

    def action_approve(self, reviewer_user_id, notes=None):
        """Approves the KYC submission. Called by OnboardingService or admin UI. REQ-IOKYC-005."""
        self.ensure_one()
        if self.verification_status not in ['in_review', 'needs_more_info']:
            raise UserError(_("KYC can only be approved if it's 'In Review' or 'Needs More Info'."))

        self.write({
            'verification_status': 'approved',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': notes
        })
        self.influencer_profile_id.update_kyc_status('approved', notes=notes)
        self.influencer_profile_id.update_onboarding_step_status('kyc_approved', True)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_APPROVED',
            actor_user_id=reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'notes': notes}
        )
        return True

    def action_reject(self, reviewer_user_id, reason_notes):
        """Rejects the KYC submission. REQ-IOKYC-005."""
        self.ensure_one()
        if self.verification_status not in ['in_review', 'needs_more_info']:
            raise UserError(_("KYC can only be rejected if it's 'In Review' or 'Needs More Info'."))
        if not reason_notes:
            raise UserError(_("A reason is required for rejecting KYC."))

        self.write({
            'verification_status': 'rejected',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': reason_notes
        })
        self.influencer_profile_id.update_kyc_status('rejected', notes=reason_notes)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_REJECTED',
            actor_user_id=reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'reason': reason_notes}
        )
        return True

    def action_request_more_info(self, reviewer_user_id, info_needed_notes):
        """Requests more information for the KYC submission. REQ-IOKYC-005."""
        self.ensure_one()
        if self.verification_status not in ['in_review']: # Usually from 'in_review'
            raise UserError(_("More information can only be requested if KYC is 'In Review'."))
        if not info_needed_notes:
            raise UserError(_("Details of information needed are required."))

        self.write({
            'verification_status': 'needs_more_info',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': info_needed_notes
        })
        self.influencer_profile_id.update_kyc_status('needs_more_info', notes=info_needed_notes)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_MORE_INFO_REQUESTED',
            actor_user_id=reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict={'info_needed': info_needed_notes}
        )
        return True