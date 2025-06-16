# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class InfluenceGenKycData(models.Model):
    _name = 'influence_gen.kyc_data'
    _description = "Influencer KYC Data Submission"
    _order = 'create_date desc'

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string="Influencer Profile",
        required=True, ondelete='cascade', index=True
    )
    document_type = fields.Selection([
        ('passport', 'Passport'),
        ('driver_license', "Driver's License"),
        ('national_id', 'National ID')
    ], string="Document Type", required=True)
    document_front_attachment_id = fields.Many2one(
        'ir.attachment', string="Document Front", required=True
    )
    document_back_attachment_id = fields.Many2one(
        'ir.attachment', string="Document Back (Optional)"
    )
    submission_date = fields.Datetime(
        string="Submission Date", default=fields.Datetime.now, readonly=True
    )
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
    reviewer_user_id = fields.Many2one(
        'res.users', string="Reviewed By", readonly=True, index=True
    )
    reviewed_at = fields.Datetime(string="Reviewed At", readonly=True)
    notes = fields.Text(string="Reviewer Notes / Reason for Rejection / Info Requested")
    third_party_reference_id = fields.Char(string="Third-Party Verification ID")

    def action_submit_for_review(self):
        """Marks the submission as ready for review."""
        for record in self:
            record.write({'verification_status': 'in_review'})
            record.influencer_profile_id.update_kyc_status('in_review')
            record.env['influence_gen.audit_log_entry'].create_log(
                event_type='KYC_SUBMITTED_FOR_REVIEW',
                actor_user_id=record.influencer_profile_id.user_id.id, # Or self.env.user if admin action
                action_performed='SUBMIT_FOR_REVIEW',
                target_object=record
            )
            # Notify admins (Placeholder - actual notification via infra layer)
            # self.env['influence_gen.infrastructure.integration.services'].notify_admins_kyc_review(record.id)
        return True

    def action_approve(self, reviewer_user_id, notes=None):
        """Approves the KYC submission. Called by OnboardingService or admin UI. REQ-IOKYC-005."""
        self.ensure_one()
        self.write({
            'verification_status': 'approved',
            'reviewer_user_id': reviewer_user_id.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': notes
        })
        self.influencer_profile_id.update_kyc_status('approved')
        self.influencer_profile_id.update_onboarding_step_status('kyc_approved', True)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_APPROVED',
            actor_user_id=reviewer_user_id.id,
            action_performed='APPROVE_KYC',
            target_object=self,
            details_dict={'notes': notes}
        )
        return True

    def action_reject(self, reviewer_user_id, reason_notes):
        """Rejects the KYC submission. REQ-IOKYC-005."""
        self.ensure_one()
        if not reason_notes:
            raise UserError(_("A reason is required for rejecting KYC submission."))
        self.write({
            'verification_status': 'rejected',
            'reviewer_user_id': reviewer_user_id.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': reason_notes
        })
        self.influencer_profile_id.update_kyc_status('rejected', notes=reason_notes)
        self.influencer_profile_id.update_onboarding_step_status('kyc_approved', False) # Reset step
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_REJECTED',
            actor_user_id=reviewer_user_id.id,
            action_performed='REJECT_KYC',
            target_object=self,
            details_dict={'reason': reason_notes}
        )
        return True

    def action_request_more_info(self, reviewer_user_id, info_needed_notes):
        """Requests more information for the KYC submission. REQ-IOKYC-005."""
        self.ensure_one()
        if not info_needed_notes:
            raise UserError(_("Details of the information needed are required."))
        self.write({
            'verification_status': 'needs_more_info',
            'reviewer_user_id': reviewer_user_id.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': info_needed_notes
        })
        self.influencer_profile_id.update_kyc_status('needs_more_info', notes=info_needed_notes)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_MORE_INFO_REQUESTED',
            actor_user_id=reviewer_user_id.id,
            action_performed='REQUEST_MORE_INFO_KYC',
            target_object=self,
            details_dict={'info_needed': info_needed_notes}
        )
        return True