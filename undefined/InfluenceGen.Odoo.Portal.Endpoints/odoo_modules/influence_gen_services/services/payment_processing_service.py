# -*- coding: utf-8 -*-
import logging
from odoo import _, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)

class PaymentProcessingService:
    """
    Service class for managing influencer payment calculations, batching,
    and Odoo accounting integration.
    """

    def __init__(self, env):
        """
        Initializes the service with the Odoo environment.
        :param env: Odoo Environment
        """
        self.env = env

    def calculate_amounts_owed(self, campaign_id=None, influencer_id=None, for_date=None):
        """
        Calculates amounts owed to influencers based on approved content, campaign terms, etc.
        This is a placeholder for potentially complex logic.
        :param campaign_id: int, optional ID of a campaign
        :param influencer_id: int, optional ID of an influencer
        :param for_date: date, optional date to calculate up to
        :return: list of dicts with {'influencer_id': X, 'amount': Y, 'currency_id': Z, 'reason': '...'}
        REQ-IPF-004, REQ-2-013
        """
        _logger.info(f"Calculating amounts owed. Campaign: {campaign_id}, Influencer: {influencer_id}, Date: {for_date}")
        # This method would typically:
        # 1. Find all approved content submissions not yet paid or partially paid.
        # 2. For each submission, determine the compensation based on campaign.compensation_model_type
        #    and campaign.compensation_details.
        # 3. Aggregate amounts per influencer.
        # This is highly dependent on the specific compensation models implemented.
        # For simplicity, this example does not implement the full calculation logic.
        # It's assumed that `create_payment_records_for_approved_content` is the primary way
        # payment records are generated based on specific content.
        
        # Example: Find approved submissions without a 'paid' payment record.
        domain = [('review_status', '=', 'approved')]
        if campaign_id:
            domain.append(('campaign_id', '=', campaign_id))
        if influencer_id:
            domain.append(('influencer_profile_id', '=', influencer_id))
        
        approved_submissions = self.env['influence_gen.content_submission'].search(domain)
        
        owed_amounts = []
        for sub in approved_submissions:
            # Check if a payment record already exists and is not 'failed'
            existing_payment = self.env['influence_gen.payment_record'].search([
                ('content_submission_id', '=', sub.id),
                ('status', 'not in', ['failed']) # Avoid duplicate for non-failed
            ], limit=1)
            if existing_payment:
                continue

            # Placeholder for compensation calculation based on campaign
            # REQ-IPF-003: Campaign compensation models
            amount = 0.0
            currency_id = sub.campaign_id.currency_id.id or self.env.company.currency_id.id
            reason = _("Payment for approved content: %s") % (sub.name_get()[0][1] if sub.name_get() else sub.id)

            if sub.campaign_id.compensation_model_type == 'flat_fee':
                # Assuming compensation_details stores the flat fee, e.g., as JSON or simple text parseable
                try:
                    # This is a very simplified example, real parsing would be needed
                    amount = float(sub.campaign_id.compensation_details or "0") 
                except ValueError:
                    _logger.error(f"Could not parse compensation_details for campaign {sub.campaign_id.id}")
                    amount = 0.0 # Default to 0 if parsing fails
            elif sub.campaign_id.compensation_model_type == 'per_submission':
                 # Similar logic for per_submission
                try:
                    amount = float(sub.campaign_id.compensation_details or "0")
                except ValueError:
                    amount = 0.0
            # Add other compensation models here (cpm, cpa, performance_based)

            if float_compare(amount, 0.0, precision_digits=2) > 0:
                owed_amounts.append({
                    'influencer_id': sub.influencer_profile_id.id,
                    'campaign_id': sub.campaign_id.id,
                    'content_submission_id': sub.id,
                    'amount': amount,
                    'currency_id': currency_id,
                    'reason': reason,
                    'due_date': fields.Date.today(), # Or based on campaign terms
                })
        _logger.info(f"Calculated {len(owed_amounts)} owed amounts.")
        return owed_amounts


    def create_payment_records_for_approved_content(self, content_submission_ids=None):
        """
        Creates PaymentRecord entries for approved content submissions if compensation criteria are met.
        This could be called after content approval or by calculate_amounts_owed.
        :param content_submission_ids: list of int, IDs of influence_gen.content_submission
        :return: recordset of created influence_gen.payment_record
        REQ-IPF-004
        """
        if content_submission_ids is None: # Calculate for all applicable
            calculated_dues = self.calculate_amounts_owed()
            created_records = self.env['influence_gen.payment_record']
            for due in calculated_dues:
                payment_vals = {
                    'influencer_profile_id': due['influencer_id'],
                    'campaign_id': due.get('campaign_id'),
                    'content_submission_id': due.get('content_submission_id'),
                    'amount': due['amount'],
                    'currency_id': due['currency_id'],
                    'status': 'pending_approval', # Or 'pending' if no approval step
                    'payment_method': 'bank_transfer', # Default or from influencer profile
                    'due_date': due.get('due_date', fields.Date.today()),
                    'notes': due.get('reason')
                }
                created_records |= self.env['influence_gen.payment_record'].create(payment_vals)
            _logger.info(f"Created {len(created_records)} payment records from calculated dues.")
            return created_records
        else:
            submissions = self.env['influence_gen.content_submission'].browse(content_submission_ids)
            created_records = self.env['influence_gen.payment_record']
            for sub in submissions:
                if sub.review_status != 'approved':
                    _logger.warning(f"Skipping payment record creation for non-approved submission {sub.id}")
                    continue
                
                # Check if a payment record already exists and is not 'failed'
                existing_payment = self.env['influence_gen.payment_record'].search([
                    ('content_submission_id', '=', sub.id),
                    ('status', 'not in', ['failed'])
                ], limit=1)
                if existing_payment:
                    _logger.info(f"Payment record already exists for submission {sub.id}")
                    continue

                # Calculate amount for this specific submission
                # This duplicates some logic from calculate_amounts_owed but is more targeted.
                amount = 0.0
                currency_id = sub.campaign_id.currency_id.id or self.env.company.currency_id.id
                reason = _("Payment for approved content: %s") % (sub.name_get()[0][1] if sub.name_get() else sub.id)

                if sub.campaign_id.compensation_model_type == 'flat_fee' or sub.campaign_id.compensation_model_type == 'per_submission':
                    try:
                        amount = float(sub.campaign_id.compensation_details or "0")
                    except ValueError:
                        _logger.error(f"Could not parse compensation_details for campaign {sub.campaign_id.id}")
                        amount = 0.0
                
                if float_compare(amount, 0.0, precision_digits=2) > 0:
                    payment_vals = {
                        'influencer_profile_id': sub.influencer_profile_id.id,
                        'campaign_id': sub.campaign_id.id,
                        'content_submission_id': sub.id,
                        'amount': amount,
                        'currency_id': currency_id,
                        'status': 'pending_approval',
                        'payment_method': 'bank_transfer',
                        'due_date': fields.Date.today(), # Or based on campaign terms
                        'notes': reason,
                    }
                    created_records |= self.env['influence_gen.payment_record'].create(payment_vals)
            _logger.info(f"Created {len(created_records)} payment records for specified submissions.")
            return created_records

    def generate_payment_batch_for_review(self, payment_record_ids):
        """
        Groups specified PaymentRecords (e.g., in 'pending_approval') for review.
        This method is more about preparing data for a UI or report rather than creating a new entity.
        :param payment_record_ids: list of int, IDs of influence_gen.payment_record
        :return: dict representing the batch summary (total_amount, count, currency summaries)
        REQ-IPF-005
        """
        _logger.info(f"Generating payment batch for review for record IDs: {payment_record_ids}")
        records = self.env['influence_gen.payment_record'].browse(payment_record_ids)
        if not records:
            return {'count': 0, 'total_amount': 0, 'currency_summaries': {}}

        currency_summaries = {}
        total_records = 0
        
        for rec in records:
            if rec.status not in ['pending_approval', 'pending']: # Only batch these statuses
                _logger.warning(f"Skipping record {rec.id} with status {rec.status} from batch.")
                continue
            total_records +=1
            currency_code = rec.currency_id.name
            if currency_code not in currency_summaries:
                currency_summaries[currency_code] = {'amount': 0.0, 'count': 0}
            currency_summaries[currency_code]['amount'] += rec.amount
            currency_summaries[currency_code]['count'] += 1
            
        # Overall total amount (if all same currency, or just sum of USD equivalents) - simplified here
        # For multi-currency, proper conversion would be needed or just list per currency.
        batch_summary = {
            'count': total_records,
            'payment_record_ids': records.filtered(lambda r: r.status in ['pending_approval', 'pending']).ids, # IDs actually included
            'currency_summaries': currency_summaries,
            'generated_at': fields.Datetime.now(),
        }
        _logger.info(f"Payment batch summary: {batch_summary}")
        return batch_summary

    def process_payment_batch_with_odoo_accounting(self, payment_record_ids_to_process):
        """
        Processes a batch of approved payment records by creating Odoo Vendor Bills.
        :param payment_record_ids_to_process: list of int, IDs of influence_gen.payment_record (assumed approved)
        :return: dict with {'success_count': X, 'failure_count': Y, 'failed_ids': [...]}
        REQ-IPF-006, REQ-2-014
        """
        _logger.info(f"Processing payment batch with Odoo Accounting for record IDs: {payment_record_ids_to_process}")
        payment_records = self.env['influence_gen.payment_record'].browse(payment_record_ids_to_process)
        
        success_count = 0
        failure_count = 0
        failed_ids = []

        AccountMove = self.env['account.move']
        Product = self.env['product.product'] # Need a service product for bill lines

        # Ensure a default payable product exists or create one
        payable_product = Product.search([('name', '=', 'Influencer Services Payable'), ('can_be_expensed', '=', False)], limit=1)
        if not payable_product:
            payable_product = Product.create({
                'name': 'Influencer Services Payable',
                'type': 'service',
                'invoice_policy': 'order', # Or based on company policy
                'purchase_ok': True,
                'sale_ok': False,
                 # TODO: Set appropriate expense account if needed, or default will be used
            })
            _logger.info(f"Created default payable product: {payable_product.name}")

        for rec in payment_records:
            if rec.status not in ['pending_approval', 'pending', 'retry']: # Ensure it's ready for processing
                 _logger.warning(f"Skipping payment record {rec.id} with status {rec.status}, not ready for bill creation.")
                 failed_ids.append(rec.id)
                 failure_count += 1
                 continue
            if rec.odoo_vendor_bill_id and rec.odoo_vendor_bill_id.state != 'cancel':
                _logger.warning(f"Payment record {rec.id} already has an active vendor bill {rec.odoo_vendor_bill_id.name}.")
                failed_ids.append(rec.id)
                failure_count += 1
                continue

            influencer_profile = rec.influencer_profile_id
            if not influencer_profile.user_id.partner_id:
                _logger.error(f"Influencer {influencer_profile.full_name} (ID: {influencer_profile.id}) does not have an associated partner record.")
                failed_ids.append(rec.id)
                failure_count += 1
                continue
            
            partner = influencer_profile.user_id.partner_id

            try:
                invoice_line_vals = [(0, 0, {
                    'product_id': payable_product.id,
                    'name': rec.notes or _('Influencer Services - Campaign: %s') % (rec.campaign_id.name or 'N/A'),
                    'quantity': 1,
                    'price_unit': rec.amount,
                    'currency_id': rec.currency_id.id,
                    # Add account_id if specific accounting is needed, otherwise default from product/partner
                })]

                vendor_bill_vals = {
                    'partner_id': partner.id,
                    'move_type': 'in_invoice', # Vendor Bill
                    'invoice_date': rec.due_date or fields.Date.today(),
                    'currency_id': rec.currency_id.id,
                    'invoice_line_ids': invoice_line_vals,
                    'ref': f"PaymentRec-{rec.id}", # Reference
                }
                
                vendor_bill = AccountMove.create(vendor_bill_vals)
                # Optionally, confirm the bill: vendor_bill.action_post() if to be auto-confirmed
                
                rec.write({
                    'odoo_vendor_bill_id': vendor_bill.id,
                    'status': 'processing_bill', # Or 'submitted_to_accounting'
                    'transaction_id': vendor_bill.name, # Use bill name as initial transaction ID
                })
                _logger.info(f"Created Vendor Bill {vendor_bill.name} for payment record {rec.id}")
                success_count += 1
            except Exception as e:
                _logger.error(f"Failed to create Vendor Bill for payment record {rec.id}: {e}")
                rec.write({'status':'failed', 'notes': (rec.notes or "") + _("\nBill Creation Failed: %s") % str(e)})
                failed_ids.append(rec.id)
                failure_count += 1
        
        return {'success_count': success_count, 'failure_count': failure_count, 'failed_ids': failed_ids}

    def update_payment_status_from_accounting(self, vendor_bill_id, new_accounting_status_info):
        """
        Updates PaymentRecord status based on changes in Odoo accounting (e.g., bill paid).
        This would typically be called by a webhook or Odoo automation.
        :param vendor_bill_id: int, ID of the account.move (Vendor Bill)
        :param new_accounting_status_info: dict, e.g. {'payment_state': 'paid', 'paid_date': '...', 'transaction_ref': '...'}
        REQ-IPF-006, REQ-2-015
        """
        _logger.info(f"Updating payment status from accounting for vendor bill ID {vendor_bill_id}")
        vendor_bill = self.env['account.move'].browse(vendor_bill_id)
        if not vendor_bill.exists() or vendor_bill.move_type != 'in_invoice':
            _logger.error(f"Vendor bill ID {vendor_bill_id} not found or not a vendor bill.")
            return False

        payment_record = self.env['influence_gen.payment_record'].search([('odoo_vendor_bill_id', '=', vendor_bill.id)], limit=1)
        if not payment_record.exists():
            _logger.warning(f"No payment record found linked to vendor bill ID {vendor_bill.id}")
            return False

        new_status = payment_record.status
        update_vals = {}

        payment_state = new_accounting_status_info.get('payment_state') # Odoo's payment_state: 'not_paid', 'in_payment', 'paid', 'partial', 'reversed'
        
        if payment_state == 'paid':
            new_status = 'paid'
            update_vals['paid_date'] = new_accounting_status_info.get('paid_date', fields.Date.today())
            if new_accounting_status_info.get('transaction_ref'):
                 update_vals['transaction_id'] = new_accounting_status_info.get('transaction_ref')
        elif payment_state in ['in_payment', 'partial']:
            new_status = 'processing_payment'
        elif payment_state == 'not_paid' and vendor_bill.state == 'posted': # Bill posted but not paid
            new_status = 'submitted_to_accounting' # Or back to pending if it was processing
        elif vendor_bill.state == 'cancel':
            new_status = 'failed' # Or 'cancelled'
            update_vals['notes'] = (payment_record.notes or "") + _("\nAssociated vendor bill cancelled.")
        
        if new_status != payment_record.status or update_vals:
            update_vals['status'] = new_status
            payment_record.write(update_vals)
            _logger.info(f"Payment record ID {payment_record.id} status updated to {new_status} based on bill {vendor_bill.name}")
            
            # Send notification to influencer if paid or failed (REQ-IPF-007, REQ-IPF-010 related)
            if new_status == 'paid':
                _logger.info(f"Payment {payment_record.id} marked as paid. Consider sending notification.")
            elif new_status == 'failed':
                 self.handle_payment_failure(payment_record.id, _("Issue during accounting processing or bill cancellation."))

        return True

    def handle_payment_failure(self, payment_record_id, failure_reason):
        """
        Handles a payment failure. Updates status, logs, triggers alert.
        :param payment_record_id: int, ID of influence_gen.payment_record
        :param failure_reason: str, reason for the failure
        REQ-IPF-010
        """
        _logger.error(f"Handling payment failure for record ID {payment_record_id}. Reason: {failure_reason}")
        payment_record = self.env['influence_gen.payment_record'].browse(payment_record_id)
        if not payment_record.exists():
            _logger.error(f"Payment record ID {payment_record_id} not found for failure handling.")
            return

        payment_record.write({
            'status': 'failed',
            'notes': (payment_record.notes or "") + _("\nPayment Failed: %s") % failure_reason,
        })
        payment_record.message_post(body=_("Payment failed. Reason: %s") % failure_reason)

        # Trigger alert to finance/admin team
        # This could be an Odoo activity, email, or a call to an alerting system.
        try:
            mail_activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=True)
            admin_user = self.env.ref('base.user_admin', raise_if_not_found=False) # Or a finance group
            user_to_assign = admin_user.id if admin_user else self.env.user.id

            self.env['mail.activity'].create({
                'activity_type_id': mail_activity_type.id,
                'summary': _('Payment Failed for Influencer'),
                'note': _('Payment record ID %s for influencer %s has failed. Reason: %s. Please investigate.') % (
                    payment_record.id, payment_record.influencer_profile_id.full_name, failure_reason
                ),
                'res_id': payment_record.id,
                'res_model_id': self.env['ir.model']._get('influence_gen.payment_record').id,
                'user_id': user_to_assign, 
            })
            _logger.info(f"Created activity for failed payment {payment_record.id}")
        except Exception as e:
            _logger.error(f"Could not create activity for failed payment {payment_record.id}: {e}")

        return True