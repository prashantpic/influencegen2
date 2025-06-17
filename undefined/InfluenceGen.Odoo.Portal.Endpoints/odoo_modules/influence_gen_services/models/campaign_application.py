from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class CampaignApplication(models.Model):
    """
    Represents an influencer's application to participate in a specific campaign.
    Manages the lifecycle of an application, from submission to approval or rejection.
    It links an influencer to a campaign and tracks the application status and review process.
    """
    _name = 'influence_gen.campaign_application'
    _description = 'Campaign Application'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'influence_gen.base_audit_mixin']
    _order = 'submitted_at desc, id desc'

    campaign_id = fields.Many2one(
        'influence_gen.campaign',
        string='Campaign',
        required=True,
        ondelete='cascade',
        index=True,
        tracking=True,
        help="The campaign this application is for."
    )
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string='Influencer Profile',
        required=True,
        ondelete='cascade',
        index=True,
        tracking=True,
        help="The influencer applying for the campaign."
    )
    proposal = fields.Text(
        string='Proposal',
        tracking=True,
        help="Influencer's proposal or pitch for this campaign application."
    )
    status = fields.Selection([
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
        ('awaiting_content', 'Awaiting Content') # Approved and expecting content
    ], string='Status', default='submitted', required=True, tracking=True, index=True,
       help="Current status of the campaign application.")
    submitted_at = fields.Datetime(
        string='Submitted At',
        default=fields.Datetime.now,
        readonly=True,
        tracking=True,
        help="Timestamp when the application was submitted."
    )
    reviewed_at = fields.Datetime(
        string='Reviewed At',
        readonly=True,
        tracking=True,
        help="Timestamp when the application was last reviewed."
    )
    reviewer_user_id = fields.Many2one(
        'res.users',
        string='Reviewed By',
        readonly=True,
        tracking=True,
        ondelete='set null',
        help="User who last reviewed this application."
    )
    rejection_reason = fields.Text(
        string='Rejection Reason',
        tracking=True,
        help="Reason why the application was rejected, if applicable."
    )
    content_submission_ids = fields.One2many(
        'influence_gen.content_submission',
        'campaign_application_id',
        string='Content Submissions',
        help="Content submitted by the influencer for this campaign application."
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        readonly=True
    )

    _sql_constraints = [
        ('campaign_influencer_unique',
         'UNIQUE(campaign_id, influencer_profile_id)',
         'An influencer can only apply to a campaign once.')
    ]

    def name_get(self):
        """Custom display name for campaign applications."""
        result = []
        for app in self:
            name = _("Application by %s for %s") % (app.influencer_profile_id.full_name or _('Unknown Influencer'), app.campaign_id.name or _('Unknown Campaign'))
            result.append((app.id, name))
        return result

    def action_approve_application(self):
        """
        Approves the campaign application.
        This action is typically performed by a campaign manager or administrator.
        REQ-2-007: Campaign Application Review
        """
        for record in self:
            if record.status not in ['submitted', 'under_review']:
                raise UserError(_("Only submitted or under review applications can be approved."))
            
            vals = {
                'status': 'approved', # Or 'awaiting_content' if more specific state needed
                'reviewed_at': fields.Datetime.now(),
                'reviewer_user_id': self.env.user.id,
                'rejection_reason': False, # Clear any previous rejection reason
            }
            record.write(vals)
            record.message_post(body=_("Campaign application approved by %s.") % self.env.user.name)
            # REQ-16-004: Send notification for campaign application status update
            record._send_status_update_notification('approved')
            _logger.info(f"Campaign application ID {record.id} approved by user ID {self.env.user.id}.")
        return True

    def action_reject_application(self, reason=None):
        """
        Rejects the campaign application.
        A reason for rejection should be provided.
        REQ-2-007: Campaign Application Review
        """
        if not reason and not self.env.context.get('rejection_reason_provided'): # Allow calling from wizard context
            raise UserError(_("A reason must be provided for rejecting the application."))

        for record in self:
            if record.status not in ['submitted', 'under_review']:
                raise UserError(_("Only submitted or under review applications can be rejected."))
            
            vals = {
                'status': 'rejected',
                'reviewed_at': fields.Datetime.now(),
                'reviewer_user_id': self.env.user.id,
                'rejection_reason': reason or record.rejection_reason # Use reason from argument or wizard context
            }
            record.write(vals)
            record.message_post(body=_("Campaign application rejected by %s. Reason: %s") % (self.env.user.name, vals['rejection_reason']))
            # REQ-16-004: Send notification for campaign application status update
            record._send_status_update_notification('rejected')
            _logger.info(f"Campaign application ID {record.id} rejected by user ID {self.env.user.id}. Reason: {vals['rejection_reason']}")
        return True

    def action_withdraw_application(self):
        """
        Allows the influencer (or an admin on their behalf) to withdraw the application.
        """
        for record in self:
            if record.status not in ['submitted', 'under_review', 'approved']: # Allow withdrawal even if approved but not yet started
                raise UserError(_("Application cannot be withdrawn in its current state: %s.") % record.status)

            # Check if current user is the influencer or an admin
            is_influencer_user = record.influencer_profile_id.user_id == self.env.user
            is_admin_user = self.env.user.has_group('influence_gen_services.group_influence_gen_admin')

            if not (is_influencer_user or is_admin_user):
                 raise UserError(_("You do not have permission to withdraw this application."))

            record.write({
                'status': 'withdrawn',
                'reviewed_at': fields.Datetime.now(), # Mark a timestamp for the action
                'reviewer_user_id': self.env.user.id if is_admin_user else False, # Log admin if admin did it
            })
            record.message_post(body=_("Campaign application withdrawn by %s.") % self.env.user.name)
            # REQ-16-004: Send notification for campaign application status update
            record._send_status_update_notification('withdrawn')
            _logger.info(f"Campaign application ID {record.id} withdrawn by user ID {self.env.user.id}.")
        return True

    def action_set_under_review(self):
        """Sets the application status to 'Under Review'."""
        for record in self:
            if record.status != 'submitted':
                raise UserError(_("Only submitted applications can be marked as under review."))
            record.write({'status': 'under_review'})
            record.message_post(body=_("Campaign application is now under review."))
        return True
        
    def _send_status_update_notification(self, new_status):
        """
        Sends a notification to the influencer about the status change of their application.
        REQ-16-004
        """
        self.ensure_one()
        if not self.influencer_profile_id.email:
            _logger.warning(f"Cannot send application status update: Influencer {self.influencer_profile_id.id} has no email.")
            return

        template_ref = False
        if new_status == 'approved':
            template_ref = self.env.ref('influence_gen_services.email_template_campaign_application_approved', raise_if_not_found=False)
        elif new_status == 'rejected':
            template_ref = self.env.ref('influence_gen_services.email_template_campaign_application_rejected', raise_if_not_found=False)
        elif new_status == 'withdrawn': # May not need a specific template for withdrawal if initiated by user
             _logger.info(f"Application {self.id} withdrawn, no specific email template for this action by default.")
             return
        # Add more templates for other statuses if needed (e.g., 'under_review')

        if template_ref:
            try:
                template_ref.send_mail(self.id, force_send=True, email_values={'recipient_ids': [(4, self.influencer_profile_id.user_id.partner_id.id)] if self.influencer_profile_id.user_id.partner_id else None})
                _logger.info(f"Sent campaign application {new_status} notification for application ID {self.id} to {self.influencer_profile_id.email}.")
            except Exception as e:
                _logger.error(f"Failed to send campaign application {new_status} notification for ID {self.id}: {e}")
        else:
            _logger.warning(f"Email template for campaign application status '{new_status}' not found for application {self.id}.")

    @api.model
    def create(self, vals):
        """Ensure campaign is open for applications if that's a rule."""
        if 'campaign_id' in vals:
            campaign = self.env['influence_gen.campaign'].browse(vals['campaign_id'])
            if campaign.status not in ['published', 'open']: # Assuming 'published' or 'open' means accepting applications
                 raise UserError(_("Applications cannot be submitted for campaigns that are not currently open or published."))
        
        # REQ-DMG-005: Store campaign application data
        # REQ-2-018: Record audit trail (handled by BaseAuditMixin)
        return super(CampaignApplication, self).create(vals)

    def write(self, vals):
        # REQ-2-018: Record audit trail (handled by BaseAuditMixin)
        res = super(CampaignApplication, self).write(vals)
        if 'status' in vals:
            for record in self:
                _logger.info(f"Campaign application {record.id} status changed to {vals['status']}.")
                # Further logic based on status change could be here.
        return res