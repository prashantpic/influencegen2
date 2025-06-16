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
        ondelete='restrict', # Prevent deleting profile if payments exist
        index=True
    )
    campaign_id = fields.Many2one(
        'influence_gen.campaign',
        string="Campaign",
        ondelete='set null', # Keep payment record if campaign deleted
        index=True
    )
    content_submission_id = fields.Many2one(
        'influence_gen.content_submission',
        string="Related Content Submission",
        ondelete='set null', # Keep payment record if submission deleted
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
        ('pending_approval', 'Pending Approval'), # Created, needs admin review
        ('approved_for_payment', 'Approved for Payment'), # Admin approved, ready for batching/processing
        ('processing', 'Processing'),           # Sent to payment gateway / Vendor bill created
        ('paid', 'Paid'),                       # Confirmed paid
        ('failed', 'Failed'),                   # Payment attempt failed
        ('cancelled', 'Cancelled')              # Payment cancelled before processing
    ], string="Status", default='pending_approval', required=True, tracking=True, index=True)
    
    transaction_id_external = fields.Char(string="External Transaction ID", readonly=True, copy=False)
    payment_method_type = fields.Char(string="Payment Method Type", help="e.g., Bank Transfer, PayPal. Derived from BankAccount or set manually.")
    bank_account_id = fields.Many2one(
        'influence_gen.bank_account',
        string="Paid to Bank Account",
        ondelete='restrict' # Don't delete bank account if payments made to it
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
        ondelete='set null' # Keep payment record even if Odoo bill is deleted
    )

    @api.depends('influencer_profile_id.name', 'amount', 'currency_id.symbol', 'create_date')
    def _compute_name(self) -> None:
        for record in self:
            date_str = fields.Date.to_string(record.create_date.date()) if record.create_date else 'N/A'
            record.name = f"{record.influencer_profile_id.name or 'N/A'} - {record.amount}{record.currency_id.symbol or ''} - {date_str}"

    def _log_status_change(self, new_status: str, old_status: str, details: dict = None):
        log_details = {'old_status': old_status, 'new_status': new_status}
        if details:
            log_details.update(details)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PAYMENT_RECORD_STATUS_CHANGE',
            actor_user_id=self.env.user.id,
            action_performed=f'STATUS_CHANGE_{old_status.upper()}_TO_{new_status.upper()}',
            target_object=self,
            details_dict=log_details
        )

    def action_approve_for_payment(self) -> None:
        """
        Admin approves the payment record.
        """
        for record in self:
            if record.status != 'pending_approval':
                raise UserError(_("Payment can only be approved if it's 'Pending Approval'."))
            old_status = record.status
            record.write({'status': 'approved_for_payment'})
            record._log_status_change('approved_for_payment', old_status)
            # PaymentService might batch this for vendor bill creation

    def action_mark_as_processing(self, vendor_bill_id: int = None) -> None:
        """
        Marks payment as processing, typically when a vendor bill is created.
        """
        for record in self:
            if record.status not in ['approved_for_payment']:
                raise UserError(_("Payment must be 'Approved for Payment' to be marked as 'Processing'."))
            old_status = record.status
            vals = {'status': 'processing'}
            if vendor_bill_id:
                vals['odoo_vendor_bill_id'] = vendor_bill_id
            record.write(vals)
            record._log_status_change('processing', old_status, {'vendor_bill_id': vendor_bill_id})

    def action_mark_as_paid(self, transaction_id_external: str, paid_date: fields.Date, payment_method_type: str = None, bank_account_id: int = None) -> None:
        """
        Marks payment as paid. REQ-2-015.
        """
        for record in self:
            if record.status not in ['processing', 'approved_for_payment']: # Allow direct paid from approved if not using vendor bills
                raise UserError(_("Payment must be 'Processing' or 'Approved for Payment' to be marked as 'Paid'."))
            
            old_status = record.status
            vals = {
                'status': 'paid',
                'transaction_id_external': transaction_id_external,
                'paid_date': paid_date,
            }
            if payment_method_type:
                vals['payment_method_type'] = payment_method_type
            if bank_account_id: # Could be the primary or a specific one used
                vals['bank_account_id'] = bank_account_id
            elif not record.bank_account_id and record.influencer_profile_id: # Auto-set if not set
                 primary_bank = record.influencer_profile_id.get_primary_bank_account()
                 if primary_bank:
                     vals['bank_account_id'] = primary_bank.id

            record.write(vals)
            record._log_status_change('paid', old_status, {'transaction_id': transaction_id_external, 'paid_date': str(paid_date)})
            
            # Notify influencer
            self.env['influence_gen_integration.notification_service'].send_notification(
                user_id=record.influencer_profile_id.user_id.id,
                message_type='payment_successful',
                title=_("Payment Sent"),
                message_body=_("A payment of %s %s has been successfully processed for you. Transaction ID: %s",
                               record.amount, record.currency_id.symbol, transaction_id_external)
            )

    def action_mark_as_failed(self, reason: str) -> None:
        """
        Marks payment as failed.
        """
        for record in self:
            if record.status not in ['processing', 'approved_for_payment']:
                raise UserError(_("Payment can only fail if it was 'Processing' or 'Approved for Payment'."))
            old_status = record.status
            record.write({
                'status': 'failed',
                'notes': (record.notes + "\n" if record.notes else "") + f"Failure Reason: {reason}"
            })
            record._log_status_change('failed', old_status, {'reason': reason})
            # Notify admin/influencer
            self.env['influence_gen_integration.notification_service'].send_notification(
                user_id=record.influencer_profile_id.user_id.id, # Also notify admin
                message_type='payment_failed',
                title=_("Payment Failed"),
                message_body=_("A payment of %s %s scheduled for you has failed. Reason: %s. Please contact support.",
                               record.amount, record.currency_id.symbol, reason)
            )

    def action_cancel_payment(self, reason: str) -> None:
        """
        Cancels a payment record.
        """
        for record in self:
            if record.status in ['paid', 'failed', 'cancelled']:
                raise UserError(_("Payment is already %s and cannot be cancelled.", record.status))
            if not reason:
                raise UserError(_("A reason is required to cancel a payment."))
            
            old_status = record.status
            record.write({
                'status': 'cancelled',
                'notes': (record.notes + "\n" if record.notes else "") + f"Cancellation Reason: {reason}"
            })
            record._log_status_change('cancelled', old_status, {'reason': reason})