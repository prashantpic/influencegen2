# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PaymentRecord(models.Model):
    """
    Represents a payment transaction or obligation to an influencer.
    This model tracks payments owed, their status, and manages integration
    with Odoo's accounting for processing. It links to Influencer, Campaign,
    and Content Submission. Inherits mail.thread for communication and
    BaseAuditMixin for audit logging.

    REQ-DMG-009: Defines structure for payment records.
    REQ-IPF-004: Tracks calculated payment amounts.
    REQ-IPF-005: Facilitates batching by grouping records.
    REQ-IPF-007: Manages payment status.
    REQ-2-013: Links payments to campaigns and influencers.
    REQ-2-015: Updates status based on accounting events.
    """
    _name = 'influence_gen.payment_record'
    _description = 'Influencer Payment Record'
    _inherit = ['mail.thread', 'influence_gen.base_audit_mixin']
    _order = 'create_date desc'

    name = fields.Char(string="Payment Reference", compute='_compute_name', store=True, readonly=True)
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string='Influencer Profile',
        required=True,
        ondelete='restrict',
        tracking=True,
        index=True,
        help="The influencer to whom this payment is due."
    )
    campaign_id = fields.Many2one(
        'influence_gen.campaign',
        string='Campaign',
        ondelete='set null',
        tracking=True,
        index=True,
        help="The campaign this payment is related to, if applicable."
    )
    content_submission_id = fields.Many2one(
        'influence_gen.content_submission',
        string='Content Submission',
        ondelete='set null',
        tracking=True,
        help="The specific content submission this payment is for, if applicable."
    )
    amount = fields.Monetary(
        string='Amount',
        required=True,
        tracking=True,
        help="The amount to be paid."
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
        tracking=True,
        help="Currency of the payment."
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        readonly=True,
        help="Company related to this payment."
    )
    status = fields.Selection([
        ('pending', 'Pending'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('processing_bill', 'Processing Bill'),
        ('bill_created', 'Bill Created'),
        ('paid', 'Paid'),
        ('payment_failed', 'Payment Failed'),
        ('cancelled', 'Cancelled')
        ], string='Status',
        required=True,
        default='pending',
        tracking=True,
        index=True,
        copy=False,
        help="Current status of the payment."
    )
    transaction_id = fields.Char(
        string='Transaction ID',
        tracking=True,
        copy=False,
        help="External transaction identifier from the payment gateway or bank."
    )
    payment_method = fields.Char( # Consider a selection or Many2one to a payment method model
        string='Payment Method',
        tracking=True,
        help="Method used for payment (e.g., Bank Transfer, PayPal)."
    )
    due_date = fields.Date(
        string='Due Date',
        tracking=True,
        help="Date when the payment is due."
    )
    paid_date = fields.Date(
        string='Paid Date',
        tracking=True,
        copy=False,
        help="Date when the payment was successfully made."
    )
    odoo_vendor_bill_id = fields.Many2one(
        'account.move',
        string='Odoo Vendor Bill',
        ondelete='set null',
        tracking=True,
        copy=False,
        domain="[('move_type', '=', 'in_invoice')]",
        help="Link to the vendor bill created in Odoo Accounting for this payment."
    )
    notes = fields.Text(string="Internal Notes")

    @api.depends('influencer_profile_id', 'create_date')
    def _compute_name(self):
        for record in self:
            if record.influencer_profile_id and record.create_date:
                record.name = _("PAY/%s/%s/%s") % (
                    record.create_date.year,
                    record.influencer_profile_id.id,
                    record.id
                )
            else:
                record.name = _("Payment Record/%s") % record.id


    def action_approve(self):
        """Marks the payment record as approved, ready for processing."""
        self.write({'status': 'approved'})

    def action_cancel(self):
        """Cancels the payment record."""
        # Add logic here: e.g., cannot cancel if already paid or processing
        for record in self:
            if record.status in ['paid', 'processing_bill', 'bill_created']:
                raise UserError(_("Cannot cancel a payment record that is already being processed or is paid."))
            record.write({'status': 'cancelled'})

    def action_mark_as_paid(self, transaction_id=None, paid_date=None):
        """
        Marks the payment record as paid.
        This is typically called after confirming payment externally or from accounting.
        """
        for record in self:
            if record.status == 'paid':
                raise UserError(_("Payment record %s is already marked as paid.") % record.name)

            vals = {'status': 'paid'}
            if transaction_id:
                vals['transaction_id'] = transaction_id
            if paid_date:
                vals['paid_date'] = paid_date
            else:
                vals['paid_date'] = fields.Date.today()
            record.write(vals)
            record.message_post(body=_("Payment marked as paid. Transaction ID: %s, Paid Date: %s") % (vals.get('transaction_id', 'N/A'), vals['paid_date']))
        return True

    def action_process_via_odoo_accounting(self):
        """
        Triggers the processing of these payment records to create vendor bills
        by calling the PaymentProcessingService.
        """
        self.ensure_one() # This action is usually for one record from form view, or multi from tree view
        
        eligible_records = self.filtered(lambda p: p.status in ['approved'])
        if not eligible_records:
            raise UserError(_("Only approved payment records can be processed for Odoo Accounting integration."))

        # The service method process_payment_batch_with_odoo_accounting expects a list of IDs.
        payment_service = self.env['influence_gen.services.payment_processing']
        result = payment_service.process_payment_batch_with_odoo_accounting(eligible_records.ids)
        
        # Optionally, handle the result from the service (e.g., display a message)
        # For now, the service call is fire-and-forget from the model's perspective for this action.
        # The service itself should update the payment_record status accordingly.
        
        # This method could return an Odoo action to refresh the view or show results,
        # but for simplicity and as per initial design, it's void.
        return True

    def action_view_vendor_bill(self):
        """
        Redirects to the vendor bill associated with this payment record.
        """
        self.ensure_one()
        if not self.odoo_vendor_bill_id:
            raise UserError(_("No vendor bill is associated with this payment record."))
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.odoo_vendor_bill_id.id,
            'target': 'current',
        }