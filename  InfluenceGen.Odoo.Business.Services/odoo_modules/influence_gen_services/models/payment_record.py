from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InfluenceGenPaymentRecord(models.Model):
    _name = 'influence_gen.payment_record'
    _description = "Influencer Payment Record"
    _order = 'create_date desc'

    name = fields.Char(string="Payment Reference", compute='_compute_name', store=True, index=True)
    influencer_profile_id = fields.Many2one(
        'influence_gen.influencer_profile',
        string="Influencer",
        required=True,
        ondelete='restrict', # Prevent deleting influencer if payments exist
        index=True
    )
    campaign_id = fields.Many2one('influence_gen.campaign', string="Campaign", ondelete='set null', index=True)
    content_submission_id = fields.Many2one('influence_gen.content_submission', string="Related Content Submission", ondelete='set null', index=True)
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
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='pending_approval', required=True, tracking=True, index=True)
    transaction_id_external = fields.Char(string="External Transaction ID", readonly=True, index=True)
    payment_method_type = fields.Char(string="Payment Method Type", help="e.g., Bank Transfer, PayPal")
    bank_account_id = fields.Many2one('influence_gen.bank_account', string="Paid to Bank Account", ondelete='restrict')
    due_date = fields.Date(string="Due Date", index=True)
    paid_date = fields.Date(string="Paid Date", readonly=True)
    notes = fields.Text(string="Notes")
    odoo_vendor_bill_id = fields.Many2one(
        'account.move',
        string="Odoo Vendor Bill/Payment",
        readonly=True,
        copy=False,
        index=True
    )

    @api.depends('influencer_profile_id.name', 'amount', 'currency_id.symbol', 'create_date')
    def _compute_name(self):
        for record in self:
            date_str = fields.Date.to_string(record.create_date.date()) if record.create_date else 'N/A'
            record.name = f"{record.influencer_profile_id.name or 'N/A'} - {record.amount or 0.0} {record.currency_id.symbol or ''} - {date_str}"

    def _log_status_change(self, old_status, new_status, details=None):
        self.ensure_one()
        log_details = {
            'payment_record_id': self.id,
            'old_status': old_status,
            'new_status': new_status,
            'influencer': self.influencer_profile_id.name,
            'amount': f"{self.amount} {self.currency_id.symbol}",
        }
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
        self.ensure_one()
        if self.status != 'pending_approval':
            raise UserError(_("Payment record can only be approved if 'Pending Approval'."))
        
        old_status = self.status
        self.write({'status': 'approved_for_payment'})
        self._log_status_change(old_status, 'approved_for_payment')
        # PaymentService might then pick this up for batching
        self.message_post(body=_("Payment approved for processing."))
        return True

    def action_mark_as_processing(self, vendor_bill_id=None):
        self.ensure_one()
        if self.status not in ('approved_for_payment'): # Or other valid preceding states
            raise UserError(_("Payment can only be marked as processing from 'Approved for Payment' state."))
        
        old_status = self.status
        vals = {'status': 'processing'}
        if vendor_bill_id:
            vals['odoo_vendor_bill_id'] = vendor_bill_id.id if hasattr(vendor_bill_id, 'id') else vendor_bill_id
        self.write(vals)
        self._log_status_change(old_status, 'processing', {'vendor_bill_id': vals.get('odoo_vendor_bill_id')})
        self.message_post(body=_("Payment processing initiated."))
        return True

    def action_mark_as_paid(self, transaction_id_external, paid_date, payment_method_type=None, bank_account_id=None):
        self.ensure_one()
        if self.status not in ('processing', 'approved_for_payment'): # Allow marking paid even if not formally 'processing' via Odoo bill
            raise UserError(_("Payment can only be marked as paid if 'Processing' or 'Approved for Payment'."))
        if not paid_date or not transaction_id_external:
            raise UserError(_("Paid date and external transaction ID are required to mark as paid."))

        old_status = self.status
        vals = {
            'status': 'paid',
            'transaction_id_external': transaction_id_external,
            'paid_date': paid_date,
        }
        if payment_method_type:
            vals['payment_method_type'] = payment_method_type
        if bank_account_id:
            vals['bank_account_id'] = bank_account_id.id if hasattr(bank_account_id, 'id') else bank_account_id
        
        self.write(vals)
        self._log_status_change(old_status, 'paid', {'transaction_id': transaction_id_external, 'paid_date': paid_date})

        # Notify influencer
        # self.env['influence_gen.infrastructure.integration.service'].send_notification(
        #     user_id=self.influencer_profile_id.user_id.id,
        #     message_type='payment_successful',
        #     message_params={'amount': self.amount, 'currency': self.currency_id.symbol, 'campaign_name': self.campaign_id.name or 'General'}
        # )
        self.message_post(body=_("Payment marked as paid. Transaction ID: %s", transaction_id_external))
        return True

    def action_mark_as_failed(self, reason):
        self.ensure_one()
        if self.status not in ('processing', 'approved_for_payment'):
            raise UserError(_("Payment can only be marked as failed if it was 'Processing' or 'Approved for Payment'."))
        if not reason:
            raise UserError(_("A reason is required for marking payment as failed."))

        old_status = self.status
        self.write({
            'status': 'failed',
            'notes': (self.notes + "\n" if self.notes else "") + f"Failure Reason: {reason}"
        })
        self._log_status_change(old_status, 'failed', {'reason': reason})

        # Notify admin/influencer
        self.message_post(body=_("Payment failed. Reason: %s", reason))
        return True

    def action_cancel_payment(self, reason):
        self.ensure_one()
        if self.status in ('paid', 'processing'): # Potentially allow cancelling 'processing' if not too late
            raise UserError(_("Cannot cancel payment that is already '%s'.", self.status))
        if not reason:
            raise UserError(_("A reason is required for cancelling payment."))

        old_status = self.status
        self.write({
            'status': 'cancelled',
            'notes': (self.notes + "\n" if self.notes else "") + f"Cancellation Reason: {reason}"
        })
        self._log_status_change(old_status, 'cancelled', {'reason': reason})
        self.message_post(body=_("Payment cancelled. Reason: %s", reason))
        return True