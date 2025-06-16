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
    ], string="Document Type", required=True)
    document_front_attachment_id = fields.Many2one('ir.attachment', string="Document Front", required=True)
    document_back_attachment_id = fields.Many2one('ir.attachment', string="Document Back (Optional)")
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
    third_party_reference_id = fields.Char(string="Third-Party Verification ID")

    def action_submit_for_review(self):
        for record in self:
            if record.verification_status != 'pending':
                raise UserError(_("KYC submission can only be submitted for review if it's in 'Pending Review' state."))
            record.write({'verification_status': 'in_review'})
            record.influencer_profile_id.update_kyc_status('in_review')
            record.influencer_profile_id.update_onboarding_step_status('kyc_submitted', True)

            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='KYC_SUBMITTED_FOR_REVIEW',
                actor_user_id=self.env.user.id, # Or user from portal if submitted by influencer
                action_performed='UPDATE',
                target_object=record,
                details_dict={'kyc_data_id': record.id}
            )
            # Notify admins:
            # self.env['influence_gen.infrastructure.integration.service'].send_notification_to_group(
            #     group_xml_id='influence_gen_services.group_influence_gen_admin', # Example group
            #     message_type='kyc_awaiting_review',
            #     message_params={'influencer_name': record.influencer_profile_id.name, 'kyc_id': record.id}
            # )
        return True

    def action_approve(self, reviewer_user_id, notes=None):
        self.ensure_one()
        if self.verification_status not in ['in_review', 'needs_more_info']:
            raise UserError(_("KYC can only be approved if it's 'In Review' or 'Needs More Info'."))

        vals = {
            'verification_status': 'approved',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
        }
        if notes:
            vals['notes'] = notes
        self.write(vals)

        self.influencer_profile_id.update_kyc_status('approved')
        self.influencer_profile_id.update_onboarding_step_status('kyc_approved', True)


        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_APPROVED',
            actor_user_id=vals['reviewer_user_id'],
            action_performed='UPDATE',
            target_object=self,
            details_dict={'kyc_data_id': self.id, 'notes': notes or ''}
        )
        # Notification to influencer handled by OnboardingService
        return True

    def action_reject(self, reviewer_user_id, reason_notes):
        self.ensure_one()
        if self.verification_status not in ['in_review', 'needs_more_info']:
            raise UserError(_("KYC can only be rejected if it's 'In Review' or 'Needs More Info'."))
        if not reason_notes:
            raise UserError(_("A reason is required for rejecting KYC."))

        vals = {
            'verification_status': 'rejected',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': reason_notes
        }
        self.write(vals)

        self.influencer_profile_id.update_kyc_status('rejected', notes=reason_notes)
        self.influencer_profile_id.update_onboarding_step_status('kyc_approved', False) # Reset approval flag

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_REJECTED',
            actor_user_id=vals['reviewer_user_id'],
            action_performed='UPDATE',
            target_object=self,
            details_dict={'kyc_data_id': self.id, 'reason': reason_notes}
        )
        # Notification to influencer handled by OnboardingService
        return True

    def action_request_more_info(self, reviewer_user_id, info_needed_notes):
        self.ensure_one()
        if self.verification_status not in ['in_review']:
            raise UserError(_("More info can only be requested if KYC is 'In Review'."))
        if not info_needed_notes:
            raise UserError(_("Details of information needed are required."))

        vals = {
            'verification_status': 'needs_more_info',
            'reviewer_user_id': reviewer_user_id.id if reviewer_user_id else self.env.user.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': info_needed_notes
        }
        self.write(vals)

        self.influencer_profile_id.update_kyc_status('needs_more_info', notes=info_needed_notes)

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='KYC_MORE_INFO_REQUESTED',
            actor_user_id=vals['reviewer_user_id'],
            action_performed='UPDATE',
            target_object=self,
            details_dict={'kyc_data_id': self.id, 'info_needed': info_needed_notes}
        )
        # Notification to influencer handled by OnboardingService
        return True