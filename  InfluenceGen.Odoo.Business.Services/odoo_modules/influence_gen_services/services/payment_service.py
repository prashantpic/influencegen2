import logging
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)

class PaymentService:
    """
    Manages influencer payment calculations and batching.
    """

    def __init__(self, env):
        self.env = env

    def calculate_owed_amounts_for_influencer(self, influencer_id, campaign_id=None):
        """
        Calculates amounts owed to an influencer, optionally for a specific campaign.
        REQ-2-013, REQ-IPF-004
        This is a calculation/simulation method. Actual PaymentRecord creation is separate.
        """
        _logger.info("Calculating owed amounts for influencer ID: %s, Campaign ID: %s", influencer_id, campaign_id)
        influencer = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer.exists():
            raise UserError(_("Influencer profile not found."))

        owed_details = []
        
        # Search for approved content submissions not yet fully paid
        domain = [
            ('influencer_profile_id', '=', influencer.id),
            ('review_status', '=', 'approved'),
            ('is_final_submission', '=', True), # Consider only final approved submissions for payment
            # Add logic to exclude already paid/processed submissions
        ]
        if campaign_id:
            domain.append(('campaign_id', '=', campaign_id))
        
        approved_submissions = self.env['influence_gen.content_submission'].search(domain)

        for submission in approved_submissions:
            campaign = submission.campaign_id
            if not campaign:
                _logger.warning("Submission %s has no linked campaign, cannot calculate payment.", submission.id)
                continue

            # Check if a payment record already exists and is paid/processing for this submission
            existing_payment = self.env['influence_gen.payment_record'].search([
                ('content_submission_id', '=', submission.id),
                ('status', 'in', ['paid', 'processing', 'approved_for_payment']) # approved_for_payment means it's in a batch
            ], limit=1)
            if existing_payment:
                _logger.info("Submission %s already has a payment record %s in status %s. Skipping calculation.",
                             submission.id, existing_payment.id, existing_payment.status)
                continue


            amount_due = 0.0
            currency = self.env.company.currency_id # Default currency
            
            if campaign.compensation_model_type == 'flat_fee':
                # Assuming compensation_details stores the flat fee amount as a string or number
                try:
                    # This is a simplification. Flat fee might be per campaign, not per submission.
                    # Or 'compensation_details' on campaign might be JSON like {"submission_fee": 100}
                    # For now, assume a simple flat fee from campaign's compensation_details
                    # This logic needs refinement based on how compensation_details is structured
                    comp_details_text = campaign.compensation_details or "0"
                    amount_due = float(comp_details_text) # This is a fragile assumption
                    currency = campaign.currency_id or currency # Assuming campaign might have a currency
                except ValueError:
                    _logger.error("Invalid flat fee amount in campaign %s details: %s", campaign.name, campaign.compensation_details)
                    continue
            
            elif campaign.compensation_model_type == 'commission':
                # Commission calculation would be complex, based on performance metrics (e.g., sales, clicks)
                # This service method might not be the place for real-time commission calculation.
                # It might rely on pre-calculated commission values or another process.
                # Placeholder:
                _logger.warning("Commission-based payment calculation not fully implemented for campaign %s.", campaign.name)
                # amount_due = self._calculate_commission_for_submission(submission)
                continue # Skip for now

            elif campaign.compensation_model_type == 'product_only':
                # No monetary payment, skip.
                continue
            
            elif campaign.compensation_model_type == 'hybrid':
                _logger.warning("Hybrid compensation model calculation not fully implemented for campaign %s.", campaign.name)
                continue


            if not float_is_zero(amount_due, precision_rounding=currency.rounding):
                owed_details.append({
                    'influencer_id': influencer.id,
                    'campaign_id': campaign.id,
                    'content_submission_id': submission.id,
                    'amount': amount_due,
                    'currency_id': currency.id,
                    'description': _("Payment for approved content: %s - %s") % (campaign.name, submission.name),
                })
        
        _logger.info("Calculated %s owed items for influencer %s.", len(owed_details), influencer_id)
        return owed_details

    def create_payment_record_for_submission(self, submission_id, force_create=False):
        """
        Creates a PaymentRecord for a given approved final content submission if one doesn't exist or isn't processed.
        This is an internal helper that might be called after content approval.
        """
        submission = self.env['influence_gen.content_submission'].browse(submission_id)
        if not (submission.exists() and submission.review_status == 'approved' and submission.is_final_submission):
            _logger.warning("Cannot create payment record: Submission %s not found, not approved, or not final.", submission_id)
            return None

        # Check if a payment record already exists and is paid/processing for this submission
        existing_payment = self.env['influence_gen.payment_record'].search([
            ('content_submission_id', '=', submission.id),
            ('status', 'not in', ['failed', 'cancelled']) # Allow re-creation if previous failed/cancelled
        ], limit=1)
        
        if existing_payment and not force_create:
            _logger.info("Payment record %s already exists for submission %s with status %s. Skipping creation.",
                         existing_payment.id, submission.id, existing_payment.status)
            return existing_payment
        
        # Use calculate_owed_amounts_for_influencer to get the details
        # This is a bit circular if calculate_owed_amounts itself checks for existing payments.
        # Let's directly calculate here for simplicity, reusing parts of the logic from calculate_owed_amounts.
        
        campaign = submission.campaign_id
        if not campaign:
            _logger.error("Submission %s has no campaign. Cannot create payment record.", submission.id)
            return None

        amount_due = 0.0
        currency = campaign.currency_id or self.env.company.currency_id
            
        if campaign.compensation_model_type == 'flat_fee':
            try:
                # This needs a robust way to get the fee for THIS submission based on campaign settings.
                # Assume compensation_details on campaign has a relevant value.
                amount_due = float(campaign.compensation_details or "0") # Highly simplified.
            except ValueError:
                _logger.error("Invalid flat fee for payment record from campaign %s details: %s", campaign.name, campaign.compensation_details)
                return None
        elif campaign.compensation_model_type == 'product_only':
            _logger.info("Campaign %s is product_only. No payment record created for submission %s.", campaign.name, submission.id)
            return None
        else:
            _logger.warning("Unsupported compensation model '%s' for auto-creating payment record for campaign %s.",
                            campaign.compensation_model_type, campaign.name)
            return None # Or handle other types

        if float_is_zero(amount_due, precision_rounding=currency.rounding):
            _logger.info("Calculated amount is zero for submission %s. No payment record created.", submission.id)
            return None

        payment_vals = {
            'influencer_profile_id': submission.influencer_profile_id.id,
            'campaign_id': campaign.id,
            'content_submission_id': submission.id,
            'amount': amount_due,
            'currency_id': currency.id,
            'status': 'pending_approval', # Default status
            'notes': _("Auto-generated for approved content: %s") % submission.name,
            'due_date': fields.Date.today(), # Or based on payment terms
            'bank_account_id': submission.influencer_profile_id.get_primary_bank_account().id or False,
        }
        
        payment_record = self.env['influence_gen.payment_record'].create(payment_vals)
        _logger.info("Payment record %s created for submission %s.", payment_record.id, submission.id)
        
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PAYMENT_RECORD_CREATED',
            actor_user_id=self.env.user.id, # System action or admin who approved content
            action_performed='CREATE',
            target_object=payment_record,
            details_dict={
                'submission_id': submission.id,
                'amount': amount_due,
                'influencer_id': submission.influencer_profile_id.id
            }
        )
        return payment_record


    def generate_payment_batch_data(self, influencer_ids=None, campaign_id=None, due_date_filter=None):
        """
        Identifies pending PaymentRecord records for batch processing.
        REQ-2-014, REQ-IPF-005
        Returns data suitable for creating vendor bills.
        """
        _logger.info("Generating payment batch data. Filters: Influencers %s, Campaign %s, Due Date %s",
                     influencer_ids, campaign_id, due_date_filter)
        
        domain = [('status', '=', 'approved_for_payment')]
        if influencer_ids:
            domain.append(('influencer_profile_id', 'in', influencer_ids))
        if campaign_id:
            domain.append(('campaign_id', '=', campaign_id))
        if due_date_filter: # Expects a date object or string
            domain.append(('due_date', '<=', due_date_filter))
            
        payment_records = self.env['influence_gen.payment_record'].search(domain)
        
        batch_data = []
        if not payment_records:
            _logger.info("No payment records found for batching with current filters.")
            return batch_data

        # Group by influencer for potentially creating one bill per influencer
        # This logic can be more complex based on how accounting batches are structured
        payments_by_influencer = {}
        for record in payment_records:
            payments_by_influencer.setdefault(record.influencer_profile_id, []).append(record)

        for influencer, records in payments_by_influencer.items():
            # Data needed by accounting to create a vendor bill
            # This is a simplified structure. Real structure depends on accounting integration.
            # Assume one vendor bill per influencer per batch run.
            total_amount = sum(rec.amount for rec in records) # Assuming all same currency for simplicity
            currency_id = records[0].currency_id.id if records else self.env.company.currency_id.id
            
            if float_is_zero(total_amount, precision_digits=records[0].currency_id.decimal_places if records else 2):
                continue

            # Need partner_id for vendor bill. Assume influencer_profile links to res.partner
            # This requires influencer_profile.user_id.partner_id to be the vendor.
            partner_id = influencer.user_id.partner_id.id
            if not partner_id:
                _logger.error("Influencer %s (User %s) has no linked partner. Cannot create vendor bill.",
                              influencer.name, influencer.user_id.name)
                continue
            
            primary_bank = influencer.get_primary_bank_account()
            if not primary_bank or primary_bank.verification_status != 'verified':
                _logger.error("Influencer %s has no verified primary bank account. Cannot process payment batch.", influencer.name)
                # Potentially skip this influencer or mark records as needing attention.
                continue


            batch_item = {
                'partner_id': partner_id, # Vendor partner
                'influencer_profile_id': influencer.id,
                'total_amount': total_amount,
                'currency_id': currency_id,
                'due_date': fields.Date.today(), # Or earliest due date from records
                'payment_record_ids': [r.id for r in records],
                'lines': [{
                    'name': rec.name or _("Payment for Campaign %s") % rec.campaign_id.name,
                    'quantity': 1,
                    'price_unit': rec.amount,
                    'account_id': None, # To be determined by accounting rules/infra layer
                    'payment_record_id': rec.id # For reconciliation
                } for rec in records],
                'bank_account_details': { # For payment execution
                    'acc_number': primary_bank.account_number_encrypted, # Infra layer will decrypt if needed
                    'bank_id': primary_bank.bank_name, # Or a bank_id if using res.bank
                    # Add IBAN, SWIFT etc.
                }
            }
            batch_data.append(batch_item)
            
        _logger.info("Generated %s items for payment batch.", len(batch_data))
        return batch_data

    def process_payment_batch_creation(self, payment_record_ids_to_process):
        """
        Creates Vendor Bills for a list of PaymentRecord IDs.
        REQ-2-014, REQ-IPF-005
        This method typically groups payment_record_ids by influencer and creates one vendor bill per influencer.
        The `generate_payment_batch_data` method should ideally provide data structured for this.
        Here, we assume `payment_record_ids_to_process` are already 'approved_for_payment'.
        """
        _logger.info("Processing payment batch creation for record IDs: %s", payment_record_ids_to_process)
        if not payment_record_ids_to_process:
            return True

        records_to_process = self.env['influence_gen.payment_record'].browse(payment_record_ids_to_process)
        
        # Validate status
        if any(r.status != 'approved_for_payment' for r in records_to_process):
            raise UserError(_("Some payment records are not in 'Approved for Payment' status."))

        # Re-group by influencer from the provided IDs
        payments_by_influencer = {}
        for record in records_to_process:
            payments_by_influencer.setdefault(record.influencer_profile_id, []).append(record)

        processed_bill_ids = []
        for influencer, records_for_influencer in payments_by_influencer.items():
            # Construct vendor bill data
            # This logic should be similar to generate_payment_batch_data but more direct
            partner_id = influencer.user_id.partner_id
            if not partner_id:
                _logger.error("Skipping vendor bill for influencer %s: No linked partner.", influencer.name)
                # Mark these records as failed or needing attention?
                for r in records_for_influencer:
                    r.action_mark_as_failed(_("Influencer has no linked partner for billing."))
                continue
            
            primary_bank = influencer.get_primary_bank_account()
            if not primary_bank or primary_bank.verification_status != 'verified':
                _logger.error("Skipping vendor bill for influencer %s: No verified primary bank account.", influencer.name)
                for r in records_for_influencer:
                    r.action_mark_as_failed(_("Influencer has no verified primary bank account for payment."))
                continue


            bill_lines_data = []
            for rec in records_for_influencer:
                bill_lines_data.append({
                    'name': rec.name or _("Payment for content related to %s") % (rec.content_submission_id.name or rec.campaign_id.name or 'Platform Activity'),
                    'quantity': 1,
                    'price_unit': rec.amount,
                    # 'account_id': ... needs specific account from chart of accounts
                    'payment_record_ref': rec.id # For later linking
                })

            vendor_bill_data = {
                'partner_id': partner_id.id,
                'invoice_date': fields.Date.today(),
                'date': fields.Date.today(), # Accounting date
                'currency_id': records_for_influencer[0].currency_id.id,
                'move_type': 'in_invoice', # Vendor Bill
                'invoice_line_ids_data': bill_lines_data, # Custom key for infra layer to process
                'payment_record_ids': [r.id for r in records_for_influencer], # Pass original record IDs
                'narration': _("Payment batch for influencer %s") % influencer.name,
                # 'journal_id': ... purchase journal
                # 'invoice_payment_term_id': ...
            }
            
            try:
                # Call Infrastructure Integration Service to create Vendor Bill
                vendor_bill = self.env['influence_gen.infrastructure.integration.services'].create_odoo_vendor_bill(vendor_bill_data)
                
                if vendor_bill: # Assuming infra returns the created account.move object or its ID
                    bill_id = vendor_bill if isinstance(vendor_bill, int) else vendor_bill.id
                    processed_bill_ids.append(bill_id)
                    # Link vendor bill to payment records and update status
                    for rec in records_for_influencer:
                        rec.action_mark_as_processing(vendor_bill_id=bill_id)
                    
                    self.env['influence_gen.audit_log_entry'].create_log(
                        event_type='VENDOR_BILL_CREATED_FOR_PAYMENTS',
                        actor_user_id=self.env.user.id,
                        action_performed='CREATE_INTEGRATION',
                        target_object=self.env['account.move'].browse(bill_id), # Target is the bill
                        details_dict={
                            'influencer_id': influencer.id,
                            'payment_record_ids': [r.id for r in records_for_influencer],
                            'vendor_bill_id': bill_id
                        }
                    )
                else:
                    _logger.error("Vendor bill creation failed (no bill returned) for influencer %s.", influencer.name)
                    for r in records_for_influencer:
                         r.action_mark_as_failed(_("Vendor bill creation failed (infrastructure layer)."))

            except Exception as e:
                _logger.error("Error creating vendor bill for influencer %s: %s", influencer.name, e)
                for r in records_for_influencer:
                     r.action_mark_as_failed(_("Error during vendor bill creation: %s") % e)
                # Continue with other influencers if possible
        
        _logger.info("Payment batch creation processed. Vendor bills created (if successful): %s", processed_bill_ids)
        return processed_bill_ids


    def update_payment_status_from_accounting(self, payment_record_id_or_bill_ref, new_status, transaction_id_external=None, paid_date=None, failure_reason=None):
        """
        Updates PaymentRecord status based on feedback from Odoo accounting.
        REQ-2-015
        payment_record_id_or_bill_ref: Can be ID of PaymentRecord or reference of account.move
        """
        _logger.info("Updating payment status from accounting. Ref: %s, New Status: %s", payment_record_id_or_bill_ref, new_status)
        
        payment_records_to_update = self.env['influence_gen.payment_record']
        
        # Try to find payment record(s)
        # This logic needs to be robust depending on what `payment_record_id_or_bill_ref` is.
        # Scenario 1: It's an account.move ID or name
        if isinstance(payment_record_id_or_bill_ref, (int, str)):
            # Assuming bill_ref is account.move.name or id
            domain = []
            if isinstance(payment_record_id_or_bill_ref, int): # Could be account.move id or payment_record id
                domain = ['|', ('odoo_vendor_bill_id', '=', payment_record_id_or_bill_ref), ('id', '=', payment_record_id_or_bill_ref)]
            else: # string, likely account.move.name
                 account_move = self.env['account.move'].search([('name', '=', payment_record_id_or_bill_ref)], limit=1)
                 if account_move:
                     domain = [('odoo_vendor_bill_id', '=', account_move.id)]
                 else: # Maybe it's a payment record name/ref? Unlikely based on typical flows.
                     _logger.warning("No account.move found for bill_ref: %s", payment_record_id_or_bill_ref)
                     # Attempt to find by payment_record_id if it's an int that wasn't an account.move id
                     if isinstance(payment_record_id_or_bill_ref, int):
                         payment_records_to_update = self.env['influence_gen.payment_record'].browse(payment_record_id_or_bill_ref)


            if domain:
                 payment_records_to_update = self.env['influence_gen.payment_record'].search(domain)

        if not payment_records_to_update.exists():
            _logger.error("No PaymentRecord found for reference: %s", payment_record_id_or_bill_ref)
            raise UserError(_("Payment record not found for the given reference."))

        for record in payment_records_to_update:
            original_status = record.status
            if new_status == 'paid':
                if not paid_date:
                    paid_date = fields.Date.today()
                record.action_mark_as_paid(transaction_id_external, paid_date, bank_account_id=record.bank_account_id.id)
            elif new_status == 'failed':
                record.action_mark_as_failed(failure_reason or _("Payment failed in accounting system."))
            else:
                _logger.warning("Unsupported status update '%s' from accounting for PaymentRecord %s.", new_status, record.id)
                # Potentially just update status field directly if it's a generic status
                # record.write({'status': new_status, 'notes': failure_reason or record.notes})
                continue
            
            # Audit log is created within the model's action methods.
            _logger.info("PaymentRecord %s status updated from %s to %s via accounting callback.", record.id, original_status, record.status)

        return True