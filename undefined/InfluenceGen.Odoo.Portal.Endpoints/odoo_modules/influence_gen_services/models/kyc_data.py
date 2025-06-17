import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class KycData(models.Model):
    """
    Stores information related to a single KYC verification attempt for an influencer.
    REQ-DMG-003, REQ-IOKYC-005, REQ-IOKYC-011, REQ-IOKYC-016
    """
    _name = 'influence_gen.kyc_data'
    _description = 'KYC Data Submission'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'influence_gen.base_audit_mixin']
    _order = 'create_date desc'

    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string='Influencer Profile',
        required=True, ondelete='cascade', index=True, tracking=True
    )
    document_type = fields.Selection([
        ('passport', 'Passport'),
        ('driver_license', "Driver's License"),
        ('national_id', 'National ID Card'),
        ('utility_bill', 'Utility Bill (Proof of Address)'),
        ('other', 'Other')
    ], string='Document Type', required=True, tracking=True)

    document_front_attachment_id = fields.Many2one(
        'ir.attachment', string='Document Front',
        domain="[('res_model', '=', _name), ('res_id', '=', id), ('res_field', '=', 'document_front_attachment_id')]",
        help="Front side of the KYC document.", tracking=True
    )
    document_back_attachment_id = fields.Many2one(
        'ir.attachment', string='Document Back',
        domain="[('res_model', '=', _name), ('res_id', '=', id), ('res_field', '=', 'document_back_attachment_id')]",
        help="Back side of the KYC document (if applicable).", tracking=True
    )

    verification_method = fields.Selection([
        ('manual', 'Manual Review'),
        ('third_party_api', 'Third-Party API'),
        ('system_automated', 'System Automated') # Future use
    ], string='Verification Method', default='manual', tracking=True) # Default from SDS: 'manual'

    verification_status = fields.Selection([
        ('pending_submission', 'Pending Submission'), # Initial state if created by system before docs
        ('submitted', 'Submitted, Awaiting Review'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('requires_more_info', 'Requires More Information')
    ], string='Verification Status', default='submitted', required=True, tracking=True, index=True)

    reviewer_user_id = fields.Many2one(
        'res.users', string='Reviewed By', readonly=True, tracking=True,
        help="User who performed the review."
    )
    reviewed_at = fields.Datetime(string='Reviewed At', readonly=True, tracking=True)
    notes = fields.Text(string='Reviewer Notes / Rejection Reason / Info Required', tracking=True)
    external_verification_id = fields.Char(string='External Verification ID', tracking=True, copy=False,
                                           help="ID from a third-party KYC verification service.")
    
    company_id = fields.Many2one(related='influencer_profile_id.company_id', store=True)


    @api.model
    def create(self, vals):
        """ On creation, if influencer_profile_id is set, update its status if appropriate. """
        res = super(KycData, self).create(vals)
        if res.influencer_profile_id and res.influencer_profile_id.kyc_status in ('pending', 'rejected', 'requires_more_info'):
            res.influencer_profile_id.kyc_status = 'submitted' # Or 'in_review' depending on workflow
        return res

    def _update_influencer_kyc_status(self, decision_status, notes=None):
        """Helper to update the main influencer profile's KYC status."""
        self.ensure_one()
        if self.influencer_profile_id:
            self.influencer_profile_id.update_kyc_status(decision_status, self.reviewer_user_id.id, notes or self.notes)

    def action_approve(self, reviewer_id=None, notes=None):
        """Approves the KYC submission."""
        self.ensure_one()
        if self.verification_status not in ['submitted', 'in_review', 'requires_more_info']:
            raise UserError(_("KYC submission can only be approved if it's Submitted, In Review, or Requires More Info."))
        
        user = self.env['res.users'].browse(reviewer_id) if reviewer_id else self.env.user
        
        self.write({
            'verification_status': 'approved',
            'reviewer_user_id': user.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': notes or self.notes or _("KYC Approved.")
        })
        self._update_influencer_kyc_status('approved')
        _logger.info(f"KYC data {self.id} approved for influencer {self.influencer_profile_id.id} by {user.name}.")

    def action_reject(self, reason, reviewer_id=None, notes=None):
        """Rejects the KYC submission."""
        self.ensure_one()
        if self.verification_status not in ['submitted', 'in_review', 'requires_more_info']:
            raise UserError(_("KYC submission can only be rejected if it's Submitted, In Review, or Requires More Info."))
        
        user = self.env['res.users'].browse(reviewer_id) if reviewer_id else self.env.user
        
        self.write({
            'verification_status': 'rejected',
            'reviewer_user_id': user.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': notes or reason # Reason is primary
        })
        self._update_influencer_kyc_status('rejected')
        _logger.info(f"KYC data {self.id} rejected for influencer {self.influencer_profile_id.id} by {user.name}. Reason: {reason}")

    def action_request_more_info(self, required_info, reviewer_id=None, notes=None):
        """Requests more information for the KYC submission."""
        self.ensure_one()
        if self.verification_status not in ['submitted', 'in_review']:
            raise UserError(_("More information can only be requested if KYC submission is Submitted or In Review."))
        
        user = self.env['res.users'].browse(reviewer_id) if reviewer_id else self.env.user

        self.write({
            'verification_status': 'requires_more_info',
            'reviewer_user_id': user.id,
            'reviewed_at': fields.Datetime.now(),
            'notes': notes or required_info # Required info is primary
        })
        self._update_influencer_kyc_status('requires_more_info')
        _logger.info(f"More info requested for KYC data {self.id} for influencer {self.influencer_profile_id.id} by {user.name}. Info: {required_info}")
        
        # Create activity for influencer if they have a user account
        if self.influencer_profile_id.user_id:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                summary=_('Additional Information Required for KYC'),
                note=_('Please provide the following for your KYC verification: %s. Notes: %s') % (required_info, notes or ''),
                user_id=self.influencer_profile_id.user_id.id
            )