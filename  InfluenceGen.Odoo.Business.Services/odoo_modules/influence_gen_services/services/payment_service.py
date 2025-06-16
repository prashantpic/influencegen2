# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare

_logger = logging.getLogger(__name__)

class PaymentService(models.AbstractModel):
    _name = 'influence_gen.payment.service'
    _description = 'InfluenceGen Payment Service'

    def __init__(self, env):
        super(PaymentService, self).__init__(env)
        self.env = env

    def calculate_owed_amounts_for_influencer(self, influencer_id, campaign_id=None):
        """
        Calculates amounts owed to an influencer. REQ-2-013, REQ-IPF-004.
        :param influencer_id: ID of influence_gen.influencer_profile
        :param campaign_id: (optional) ID of influence_gen.campaign to filter by
        :return: list of dicts, each representing a potential payment
                 {'amount': float, 'currency_id': int, 'submission_id': int, 'campaign_id': int, 'reason': str}
        """
        influencer = self.env['influence_gen.influencer_profile'].browse(influencer_id)
        if not influencer.exists():
            raise UserError(f"Influencer profile with ID {influencer_id} not found.")

        domain = [
            ('influencer_profile_id', '=', influencer.id),
            ('review_status', '=', 'approved'),
            ('is_final_submission', '=', True), # Assuming only final approved submissions trigger payment
        ]
        if campaign_id:
            domain.append(('campaign_id', '=', campaign_id))

        approved_submissions = self.env['influence_gen.content_submission'].search(domain)
        
        payment_details_list = []

        for sub in approved_submissions:
            campaign = sub.campaign_id
            if not campaign:
                _logger.warning(f"Submission {sub.id} has no linked campaign, skipping payment calculation.")
                continue

            # Check if a payment record already exists and is not failed/cancelled for this submission
            existing_payment = self.env['influence_gen.payment_record'].search([
                ('content_submission_id', '=', sub.id),
                ('status', 'not in', ['failed', 'cancelled'])
            ], limit=1)
            if existing_payment:
                _logger.info(f"Payment record {existing_payment.name} already exists for submission {sub.id}. Skipping.")
                continue

            amount_to_pay = 0.0
            currency_id = campaign.currency_id.id if campaign.currency_id else self.env.company.currency_id.id
            reason = ""

            if campaign.compensation_model_type == 'flat_fee':
                # Assuming compensation_details stores the flat fee amount for the campaign or per submission type
                # This logic needs to be robust based on how compensation_details is structured.
                # For simplicity, let's assume Campaign model has a field 'flat_fee_amount' or it's in compensation_details
                try:
                    # Example: compensation_details = "Flat fee: 100 USD" or JSON {"type": "flat", "amount": 100}
                    # This is a placeholder for parsing logic.
                    if campaign.compensation_details: # Assuming compensation_details might hold the amount for a flat_fee
                        details_str = str(campaign.compensation_details).lower()
                        # Very naive parsing - should be structured (e.g. JSON in compensation_details)
                        # Or better, have dedicated fields on campaign for specific models.
                        # E.g., campaign.flat_fee_amount
                        # For this SDS, we only have 'compensation_details' (Text)
                        # Let's assume for a flat_fee campaign, this text field directly contains the number.
                        try:
                           amount_to_pay = float(campaign.compensation_details)
                           reason = f"Flat fee for campaign '{campaign.name}' - submission '{sub.name}'"
                        except ValueError:
                           _logger.error(f"Could not parse flat fee amount from compensation_details for campaign {campaign.id}: {campaign.compensation_details}")
                           amount_to_pay = 0.0 # Or raise error/skip
                           reason = f"Error: Could not parse flat fee for campaign '{campaign.name}'"
                    else: # Fallback if no specific detail is found
                        _logger.warning(f"Flat fee campaign {campaign.id} has no parsable compensation_details for amount.")
                        amount_to_pay = 0.0
                        reason = f"Flat fee (amount undetermined) for campaign '{campaign.name}' - submission '{sub.name}'"

                except Exception as e:
                    _logger.error(f"Error calculating flat_fee for campaign {campaign.id}: {e}")
                    amount_to_pay = 0.0
            elif campaign.compensation_model_type == 'commission':
                # Commission calculation would depend on performance metrics and rates defined in compensation_details.
                # This is complex and usually not calculated at submission approval but after performance data.
                # For this example, let's assume a base amount if defined, or skip.
                reason = f"Commission-based for campaign '{campaign.name}' - submission '{sub.name}'. Further calculation needed."
                # amount_to_pay = ... (logic based on performance data and commission_details)
                _logger.info(f"Commission for submission {sub.id} needs manual calculation or performance data.")
                continue # Skip auto-creation for commissions here, may need manual PaymentRecord.
            elif campaign.compensation_model_type == 'product_only':
                reason = f"Product only for campaign '{campaign.name}' - submission '{sub.name}'"
                # No monetary payment record typically, but could log $0 payment for tracking.
                _logger.info(f"Product only campaign {campaign.id} for submission {sub.id}. No monetary payment.")
                continue # Skip monetary payment
            elif campaign.compensation_model_type == 'hybrid':
                # Hybrid model could involve a flat fee + commission.
                # Similar complexity to 'commission'.
                reason = f"Hybrid model for campaign '{campaign.name}' - submission '{sub.name}'. Needs detailed calculation."
                _logger.info(f"Hybrid model for submission {sub.id} needs manual calculation or performance data.")
                continue
            else:
                _logger.warning(f"Unknown compensation model type: {campaign.compensation_model_type} for campaign {campaign.id}")
                continue

            if float_compare(amount_to_pay, 0.0, precision_digits=2) > 0:
                payment_details_list.append({
                    'amount': amount_to_pay,
                    'currency_id': currency_id,
                    'submission_id': sub.id,
                    'campaign_id': campaign.id,
                    'influencer_profile_id': influencer.id,
                    'reason': reason,
                    'due_date': fields.Date.today(), # Or based on payment terms
                })
        
        # This service method could also directly create PaymentRecord in 'pending_approval'
        # Or return data for UI to confirm before creating PaymentRecords.
        # SDS implies "calculating amounts", so returning list is primary.
        # Let's create PaymentRecord records here if amount > 0.
        created_payment_records = self.env['influence_gen.payment_record']
        for detail in payment_details_list:
            if detail.get('amount', 0.0) > 0:
                payment_record = self.env['influence_gen.payment_record'].create({
                    'influencer_profile_id': detail['influencer_profile_id'],
                    'campaign_id': detail['campaign_id'],
                    'content_submission_id': detail['submission_id'],
                    'amount': detail['amount'],
                    'currency_id': detail['currency_id'],
                    'status': 'pending_approval',
                    'notes': detail['reason'],
                    'due_date': detail.get('due_date'),
                    'bank_account_id': influencer.get_primary_bank_account().id if influencer.get_primary_bank_account() else False,

                })
                created_payment_records |= payment_record
                self.env['influence_gen.audit_log_entry'].create_log(
                    event_type='PAYMENT_RECORD_CALCULATED',
                    actor_user_id=self.env.user.id, # System if automated
                    action_performed='CREATE',
                    target_object=payment_record,
                    details_dict=detail
                )
        return created_payment_records # Or payment_details_list if records are not created here


    def generate_payment_batch_data(self, influencer_ids=None, campaign_id=None, due_date_filter=None):
        """
        Generates data for a payment batch. REQ-2-014, REQ-IPF-005.
        :param influencer_ids: (optional) list of influencer_profile_ids
        :param campaign_id: (optional) ID of campaign
        :param due_date_filter: (optional) date to filter due_date on or before
        :return: dict suitable for creating vendor bills (e.g., grouped by influencer/vendor)
        """
        domain = [('status', '=', 'approved_for_payment')]
        if influencer_ids:
            domain.append(('influencer_profile_id', 'in', influencer_ids))
        if campaign_id:
            domain.append(('campaign_id', '=', campaign_id))
        if due_date_filter:
            domain.append(('due_date', '<=', due_date_filter))

        payment_records = self.env['influence_gen.payment_record'].search(domain)
        
        batch_data = {} # Keyed by influencer_id (acting as vendor)
        for record in payment_records:
            influencer = record.influencer_profile_id
            # Odoo's vendor bills are typically linked to a res.partner.
            # We need to ensure influencer_profile.user_id.partner_id exists and is a vendor.
            # Or create a dedicated partner for each influencer.
            # For simplicity, we assume influencer.user_id.partner_id can be used as vendor.
            vendor_partner = influencer.user_id.partner_id
            if not vendor_partner:
                _logger.warning(f"Payment record {record.name} for influencer {influencer.name} has no linked partner. Skipping for batch.")
                continue
            
            # Ensure partner is marked as a supplier
            if not vendor_partner.supplier_rank > 0:
                 vendor_partner.supplier_rank = 1


            if vendor_partner.id not in batch_data:
                primary_bank_acc = record.bank_account_id or influencer.get_primary_bank_account()
                if not primary_bank_acc:
                    _logger.warning(f"Influencer {influencer.name} has no primary bank account for payment record {record.name}. Skipping.")
                    continue
                # The actual bank account on partner (for vendor bill) needs to be 'res.partner.bank'
                # This needs to be synchronized or selected.
                # For now, let's assume this detail is handled by vendor bill creation infra service.
                
                batch_data[vendor_partner.id] = {
                    'vendor_partner_id': vendor_partner.id,
                    'vendor_name': vendor_partner.name,
                    'payment_record_ids': [],
                    'lines': [] 
                }
            
            batch_data[vendor_partner.id]['payment_record_ids'].append(record.id)
            batch_data[vendor_partner.id]['lines'].append({
                'payment_record_id': record.id,
                'name': f"Payment for campaign: {record.campaign_id.name if record.campaign_id else 'N/A'} - {record.name}",
                'quantity': 1,
                'price_unit': record.amount,
                'currency_id': record.currency_id.id,
                # account_id for expense needs to be configured/fetched
            })
        
        return {'vendors': list(batch_data.values())}


    def process_payment_batch_creation(self, payment_record_ids_to_process):
        """
        Processes creation of vendor bills from payment records. REQ-2-014, REQ-IPF-005.
        Calls Infrastructure Integration Service.
        :param payment_record_ids_to_process: list of IDs of influence_gen.payment_record
        """
        if not payment_record_ids_to_process:
            return True
            
        records = self.env['influence_gen.payment_record'].browse(payment_record_ids_to_process)
        records_to_process = records.filtered(lambda r: r.status == 'approved_for_payment')

        if not records_to_process:
            _logger.info("No payment records in 'approved_for_payment' state found in the provided list.")
            return True
        
        # Group records by influencer (vendor partner) to create one bill per vendor
        vendor_bills_payload = {}
        for record in records_to_process:
            influencer = record.influencer_profile_id
            vendor_partner = influencer.user_id.partner_id # Assuming this is the vendor
            if not vendor_partner:
                _logger.error(f"Cannot create vendor bill for Payment Record {record.id}: Influencer {influencer.name} has no associated partner.")
                record.action_mark_as_failed(reason=f"Influencer {influencer.name} has no associated partner for vendor bill.")
                continue

            if vendor_partner.id not in vendor_bills_payload:
                 # Default expense account - this should be configurable
                default_expense_account = self.env['account.account'].search([
                    ('company_id', '=', self.env.company.id),
                    ('user_type_id', '=', self.env.ref('account.data_account_type_expenses').id)
                ], limit=1)
                if not default_expense_account:
                    _logger.error(f"Default expense account not found for company {self.env.company.name}.")
                    record.action_mark_as_failed(reason="Default expense account not configured.")
                    continue


                vendor_bills_payload[vendor_partner.id] = {
                    'partner_id': vendor_partner.id,
                    'move_type': 'in_invoice', # Vendor Bill
                    'invoice_date': fields.Date.today(),
                    'currency_id': record.currency_id.id, # Assuming all records for one vendor have same currency, or handle mix
                    'invoice_line_ids': [],
                    'payment_record_ids_for_this_bill': []
                }
            
            # Add line to vendor bill
            vendor_bills_payload[vendor_partner.id]['invoice_line_ids'].append((0, 0, {
                'name': f"InfluenceGen Payment: {record.campaign_id.name if record.campaign_id else 'General Payment'} - Ref: {record.name}",
                'quantity': 1,
                'price_unit': record.amount,
                'account_id': default_expense_account.id, # Placeholder, needs proper COA mapping
            }))
            vendor_bills_payload[vendor_partner.id]['payment_record_ids_for_this_bill'].append(record.id)

        processed_record_ids = []
        for partner_id, bill_data in vendor_bills_payload.items():
            current_bill_payment_record_ids = bill_data.pop('payment_record_ids_for_this_bill')
            try:
                vendor_bill = self.env['influence_gen.infrastructure.integration.service'].create_vendor_bill(bill_data)
                if vendor_bill: # Assuming create_vendor_bill returns the created account.move
                    for pr_id in current_bill_payment_record_ids:
                        payment_rec = self.env['influence_gen.payment_record'].browse(pr_id)
                        payment_rec.action_mark_as_processing(vendor_bill_id=vendor_bill.id)
                    processed_record_ids.extend(current_bill_payment_record_ids)
                    self.env['influence_gen.audit_log_entry'].create_log(
                        event_type='VENDOR_BILL_CREATED_FOR_PAYMENTS',
                        actor_user_id=self.env.user.id,
                        action_performed='CREATE',
                        target_object=vendor_bill, # This is account.move
                        details_dict={'vendor_partner_id': partner_id, 'payment_record_ids': current_bill_payment_record_ids, 'amount': vendor_bill.amount_total}
                    )
                else:
                    for pr_id in current_bill_payment_record_ids:
                        payment_rec = self.env['influence_gen.payment_record'].browse(pr_id)
                        payment_rec.action_mark_as_failed(reason="Vendor bill creation failed in infrastructure layer.")
            except Exception as e:
                _logger.error(f"Failed to create vendor bill for partner ID {partner_id}: {e}")
                for pr_id in current_bill_payment_record_ids:
                    payment_rec = self.env['influence_gen.payment_record'].browse(pr_id)
                    payment_rec.action_mark_as_failed(reason=f"Vendor bill creation error: {str(e)}")
        
        return processed_record_ids


    def update_payment_status_from_accounting(self, payment_record_id_or_bill_ref, new_status, transaction_id_external=None, paid_date=None, failure_reason=None):
        """
        Updates payment record status based on feedback from accounting. REQ-2-015.
        :param payment_record_id_or_bill_ref: ID of influence_gen.payment_record or Odoo Vendor Bill reference
        :param new_status: 'paid' or 'failed'
        :param transaction_id_external: string, external transaction ID if paid
        :param paid_date: date, date of payment if paid
        :param failure_reason: string, reason if failed
        """
        payment_record = None
        if isinstance(payment_record_id_or_bill_ref, int): # Assuming it's payment_record_id
            payment_record = self.env['influence_gen.payment_record'].browse(payment_record_id_or_bill_ref)
        elif isinstance(payment_record_id_or_bill_ref, str): # Assuming it's bill reference
            # Need to find account.move by ref, then find related payment_record
            vendor_bill = self.env['account.move'].search([('name', '=', payment_record_id_or_bill_ref), ('move_type', '=', 'in_invoice')], limit=1)
            if vendor_bill:
                payment_record = self.env['influence_gen.payment_record'].search([('odoo_vendor_bill_id', '=', vendor_bill.id)], limit=1)
        
        if not payment_record or not payment_record.exists():
            raise UserError(f"Payment Record not found for reference: {payment_record_id_or_bill_ref}")

        if new_status == 'paid':
            if not paid_date:
                paid_date = fields.Date.today()
            payment_record.action_mark_as_paid(
                transaction_id_external=transaction_id_external,
                paid_date=paid_date
            )
        elif new_status == 'failed':
            if not failure_reason:
                raise UserError("Failure reason is required when marking payment as failed.")
            payment_record.action_mark_as_failed(reason=failure_reason)
        else:
            raise UserError(f"Unsupported status update from accounting: {new_status}")

        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PAYMENT_STATUS_FROM_ACCOUNTING',
            actor_user_id=self.env.user.id, # Or a dedicated system user for accounting integration
            action_performed='UPDATE',
            target_object=payment_record,
            details_dict={
                'new_status': new_status, 
                'transaction_id': transaction_id_external, 
                'paid_date': str(paid_date),
                'failure_reason': failure_reason
            }
        )