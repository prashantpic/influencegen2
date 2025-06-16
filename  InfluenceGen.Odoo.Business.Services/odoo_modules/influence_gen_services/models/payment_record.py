# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class InfluenceGenPaymentRecord(models.Model):
    _name = 'influence_gen.payment_record'
    _description = "Influencer Payment Record"
    _order = 'create_date desc'

    name = fields.Char(string="Payment Reference", compute='_compute_name', store=True)
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile', string="Influencer",
        required=True, ondelete='restrict', index=True
    )
    campaign_id = fields.Many2one(
        'influence_gen.campaign', string="Campaign",
        ondelete='set null', index=True
    )
    content_submission_id = fields.Many2one(
        'influence_gen.content_submission', string="Related Content Submission",
        ondelete='set null', index=True
    )
    amount = fields.Monetary(string="Amount", required=True, currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string="Currency", required=True,
        default=lambda self: self.env.company.currency_id.id
    )
    status = fields.Selection([
        ('pending_approval', 'Pending Approval'),
        ('approved_for_payment', 'Approved for Payment'),
        ('processing', 'Processing'), # Vendor bill created, awaiting actual payment
        ('paid', 'Paid'),
        ('failed', 'Failed'), # Payment attempt failed
        ('cancelled', 'Cancelled') # Payment record cancelled before processing
    ], string="Status", default='pending_approval', required=True, tracking=True, index=True)
    transaction_id_external = fields.Char(string="External Transaction ID", readonly=True)
    payment_method_type = fields.Char(
        string="Payment Method Type", 
        help="e.g., Bank Transfer, PayPal. Derived from BankAccount or set manually."
    )
    bank_account_id = fields.Many2one(
        'influence_gen.bank_account', string="Paid to Bank Account",
        ondelete='restrict'
    )
    due_date = fields.Date(string="Due Date", index=True)
    paid_date = fields.Date(string="Paid Date", readonly=True)
    notes = fields.Text(string="Notes")
    odoo_vendor_bill_id = fields.Many2one(
        'account.move', string="Odoo Vendor Bill/Payment",
        readonly=True, copy=False, index=True
    )

    @api.depends('influencer_profile_id.name', 'amount', 'currency_id.symbol', 'create_date')
    def _compute_name(self):
        for record in self:
            date_str = fields.Date.to_string(record.create_date) if record.create_date else 'N/A'
            record.name = f"{record.influencer_profile_id.name or 'N/A'} - {record.amount} {record.currency_id.symbol or ''} - {date_str}"

    def action_approve_for_payment(self):
        """Admin approves the payment record."""
        self.ensure_one()
        if self.status != 'pending_approval':
            raise UserError(_("Only payment records pending approval can be approved."))
        
        self.write({'status': 'approved_for_payment'})
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PAYMENT_RECORD_APPROVED',
            actor_user_id=self.env.user.id,
            action_performed='APPROVE_FOR_PAYMENT',
            target_object=self
        )
        # PaymentService might then batch these for vendor bill creation
        # self.env['influence_gen.payment_service'].check_for_batch_creation([self.id])
        return True

    def action_mark_as_processing(self, vendor_bill_id=None):
        """Marks payment as processing, typically when a vendor bill is created."""
        self.ensure_one()
        if self.status not in ('approved_for_payment'):
             raise UserError(_("Only payments approved for payment can be marked as processing."))

        vals = {'status': 'processing'}
        if vendor_bill_id:
            vals['odoo_vendor_bill_id'] = vendor_bill_id
        self.write(vals)
        
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PAYMENT_RECORD_PROCESSING',
            actor_user_id=self.env.user.id, # Or system if automated
            action_performed='MARK_AS_PROCESSING',
            target_object=self,
            details_dict={'vendor_bill_id': vendor_bill_id}
        )
        return True

    def action_mark_as_paid(self, transaction_id_external, paid_date, payment_method_type=None, bank_account_id=None):
        """Marks payment as paid. REQ-2-015."""
        self.ensure_one()
        if self.status not in ('processing', 'approved_for_payment'): # Allow marking paid even if not formally 'processing' via Odoo bill
            raise UserError(_("Payment must be in 'Processing' or 'Approved for Payment' state to be marked as paid. Current state: %s", self.status))

        vals = {
            'status': 'paid',
            'transaction_id_external': transaction_id_external,
            'paid_date': paid_date,
        }
        if payment_method_type:
            vals['payment_method_type'] = payment_method_type
        if bank_account_id: # Instance of bank_account record or ID
            vals['bank_account_id'] = bank_account_id.id if hasattr(bank_account_id, 'id') else bank_account_id

        self.write(vals)
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PAYMENT_RECORD_PAID',
            actor_user_id=self.env.user.id, # Or system if callback from payment gateway
            action_performed='MARK_AS_PAID',
            target_object=self,
            details_dict={
                'transaction_id': transaction_id_external,
                'paid_date': fields.Date.to_string(paid_date)
            }
        )
        # Notify influencer
        try:
            self.env['influence_gen.infrastructure.integration.services'].send_notification(
                user_ids=self.influencer_profile_id.user_id.ids,
                message_type='payment_processed',
                subject=_("Payment Processed for Campaign '%s'", self.campaign_id.name or 'General Payment'),
                body=_("A payment of %s %s has been processed for you.", self.amount, self.currency_id.symbol)
            )
        except Exception as e:
            _logger.error(f"Failed to send payment processed notification for payment record {self.id}: {e}")
        return True

    def action_mark_as_failed(self, reason):
        """Marks payment as failed."""
        self.ensure_one()
        if self.status not in ('processing', 'approved_for_payment'):
            raise UserError(_("Only payments in 'Processing' or 'Approved for Payment' state can be marked as failed."))
        if not reason:
            raise UserError(_("A reason is required for marking a payment as failed."))

        notes = (self.notes + "\n" if self.notes else "") + f"Failure Reason: {reason}"
        self.write({
            'status': 'failed',
            'notes': notes
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PAYMENT_RECORD_FAILED',
            actor_user_id=self.env.user.id, # Or system
            action_performed='MARK_AS_FAILED',
            target_object=self,
            details_dict={'reason': reason}
        )
        # Notify admin/influencer
        # Admin notification
        # Influencer notification (optional, depending on policy)
        return True

    def action_cancel_payment(self, reason):
        """Cancels the payment record if not yet processed."""
        self.ensure_one()
        if self.status not in ('pending_approval', 'approved_for_payment'):
            raise UserError(_("Only payment records in 'Pending Approval' or 'Approved for Payment' can be cancelled. Current status: %s", self.status))
        if not reason:
            raise UserError(_("A reason is required for cancelling a payment record."))
            
        notes = (self.notes + "\n" if self.notes else "") + f"Cancellation Reason: {reason}"
        self.write({
            'status': 'cancelled',
            'notes': notes
        })
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PAYMENT_RECORD_CANCELLED',
            actor_user_id=self.env.user.id,
            action_performed='CANCEL_PAYMENT',
            target_object=self,
            details_dict={'reason': reason}
        )
        return True