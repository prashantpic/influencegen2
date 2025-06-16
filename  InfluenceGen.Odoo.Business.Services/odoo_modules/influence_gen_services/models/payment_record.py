# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InfluenceGenPaymentRecord(models.Model):
    _name = 'influence_gen.payment_record'
    _description = "Influencer Payment Record"
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Payment Reference", compute='_compute_name', store=True, readonly=True)
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Influencer",
        required=True,
        ondelete='restrict', # Don't delete payment if influencer is deleted (unless also deleted)
        index=True
    )
    campaign_id = fields.Many2one(
        'influence_gen.campaign',
        string="Campaign",
        ondelete='set null', # Payment can exist without campaign (e.g. general payment)
        index=True
    )
    content_submission_id = fields.Many2one(
        'influence_gen.content_submission',
        string="Related Content Submission",
        ondelete='set null', # Payment can exist without specific submission
        index=True
    )
    amount = fields.Monetary(string="Amount", required=True, currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id.id
    )
    status = fields.Selection([
        ('pending_approval', 'Pending Approval'),
        ('approved_for_payment', 'Approved for Payment'),
        ('processing', 'Processing'), # e.g. Vendor Bill created, awaiting actual payment
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='pending_approval', required=True, tracking=True, index=True)
    transaction_id_external = fields.Char(string="External Transaction ID", readonly=True, copy=False)
    payment_method_type = fields.Char(string="Payment Method Type", help="e.g., 'Bank Transfer', 'PayPal'")
    bank_account_id = fields.Many2one(
        'influence_gen.bank_account',
        string="Paid to Bank Account",
        ondelete='restrict' # Don't delete payment if bank account is deleted
    )
    due_date = fields.Date(string="Due Date", index=True)
    paid_date = fields.Date(string="Paid Date", readonly=True)
    notes = fields.Text(string="Notes")
    odoo_vendor_bill_id = fields.Many2one(
        'account.move',
        string="Odoo Vendor Bill/Payment",
        readonly=True,
        copy=False,
        index=True,
        ondelete='set null' # Keep payment record if Odoo bill is deleted
    )

    @api.depends('influencer_profile_id.name', 'amount', 'currency_id.symbol', 'create_date')
    def _compute_name(self):
        for record in self:
            date_str = fields.Date.from_string(record.create_date).strftime('%Y-%m-%d') if record.create_date else 'N/A'
            record.name = f"{record.influencer_profile_id.name or 'N/A'} - {record.amount}{record.currency_id.symbol or ''} - {date_str}"

    def _log_status_change(self, new_status, details=None):
        self.ensure_one()
        log_details = {'old_status': self._origin.status if self._origin else 'N/A', 'new_status': new_status}
        if details:
            log_details.update(details)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PAYMENT_RECORD_STATUS_CHANGED',
            actor_user_id=self.env.user.id,
            action_performed='UPDATE',
            target_object=self,
            details_dict=log_details
        )

    def action_approve_for_payment(self):
        """Admin approves the payment record."""
        self.ensure_one()
        if self.status != 'pending_approval':
            raise UserError(_("Payment record can only be approved if 'Pending Approval'."))
        self.write({'status': 'approved_for_payment'})
        self._log_status_change('approved_for_payment')
        # Trigger PaymentService to potentially batch this for vendor bill creation
        # This can be done by a scheduled job in PaymentService looking for 'approved_for_payment'
        # or an explicit call if needed.
        return True

    def action_mark_as_processing(self, vendor_bill_id=None):
        """Marks payment as processing, typically when a vendor bill is created."""
        self.ensure_one()
        if self.status not in ['approved_for_payment']:
            raise UserError(_("Payment can only be marked as processing if 'Approved for Payment'."))
        vals = {'status': 'processing'}
        if vendor_bill_id:
            vals['odoo_vendor_bill_id'] = vendor_bill_id
        self.write(vals)
        self._log_status_change('processing', details={'vendor_bill_id': vendor_bill_id})
        return True

    def action_mark_as_paid(self, transaction_id_external, paid_date, payment_method_type=None, bank_account_id=None):
        """Marks payment as paid. REQ-2-015."""
        self.ensure_one()
        if self.status not in ['processing', 'approved_for_payment']: # Can mark paid even if not explicitly 'processing'
            raise UserError(_("Payment can only be marked as paid if 'Processing' or 'Approved for Payment'."))
        if not paid_date:
            raise UserError(_("Paid date is required."))

        vals = {
            'status': 'paid',
            'transaction_id_external': transaction_id_external,
            'paid_date': paid_date,
        }
        if payment_method_type:
            vals['payment_method_type'] = payment_method_type
        if bank_account_id: # Instance or ID
            vals['bank_account_id'] = bank_account_id.id if isinstance(bank_account_id, models.BaseModel) else bank_account_id

        self.write(vals)
        self._log_status_change('paid', details={
            'transaction_id': transaction_id_external,
            'paid_date': str(paid_date) # ensure string for JSON
        })

        # Notify influencer
        notification_service = self.env['influence_gen.infrastructure.integration.services'].sudo()
        if hasattr(notification_service, 'send_notification') and self.influencer_profile_id.user_id:
             notification_service.send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                notification_type='payment_processed',
                title=_("Payment Processed"),
                message=_("A payment of %s %s has been processed for you. Transaction ID: %s", self.amount, self.currency_id.symbol, transaction_id_external or 'N/A'),
                target_model=self._name,
                target_res_id=self.id
            )
        return True

    def action_mark_as_failed(self, reason):
        """Marks payment as failed."""
        self.ensure_one()
        if self.status not in ['processing', 'approved_for_payment']:
            raise UserError(_("Payment can only be marked as failed if 'Processing' or 'Approved for Payment'."))
        if not reason:
            raise UserError(_("A reason is required for marking payment as failed."))

        self.write({
            'status': 'failed',
            'notes': (self.notes + "\n" if self.notes else "") + f"Failure Reason: {reason}"
        })
        self._log_status_change('failed', details={'reason': reason})

        # Notify admin/influencer
        notification_service = self.env['influence_gen.infrastructure.integration.services'].sudo()
        if hasattr(notification_service, 'send_notification') and self.influencer_profile_id.user_id:
             notification_service.send_notification(
                user_ids=self.influencer_profile_id.user_id.ids, # Also notify admins
                notification_type='payment_failed',
                title=_("Payment Failed"),
                message=_("A payment of %s %s for you has failed. Reason: %s. Please contact support.", self.amount, self.currency_id.symbol, reason),
                target_model=self._name,
                target_res_id=self.id
            )
        return True

    def action_cancel_payment(self, reason):
        """Cancels the payment record if not yet processed too far."""
        self.ensure_one()
        if self.status in ['paid', 'processing']: # Define cancellable states
            raise UserError(_("Cannot cancel a payment that is '%s'.") % self.status)
        if not reason:
            raise UserError(_("A reason is required for cancelling a payment record."))

        self.write({
            'status': 'cancelled',
            'notes': (self.notes + "\n" if self.notes else "") + f"Cancellation Reason: {reason}"
        })
        self._log_status_change('cancelled', details={'reason': reason})
        return True