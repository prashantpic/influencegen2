# -*- coding: utf-8 -*-
import logging
from typing import List
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from ..models.accounting.vendor_bill_payload import VendorBillPayload, VendorBillLinePayload

_logger = logging.getLogger(__name__)

class OdooAccountingService(models.AbstractModel):
    _name = 'influence_gen.odoo.accounting.service'
    _description = 'Odoo Accounting Integration Service for Vendor Bills'

    @api.model
    def _prepare_vendor_bill_line_vals(self, line_payload: VendorBillLinePayload, currency: models.Model) -> dict:
        """
        Prepares a dictionary of values for creating a single account.move.line (vendor bill line).

        :param line_payload: DTO for the bill line.
        :param currency: The res.currency record of the bill.
        :return: Dictionary of values for account.move.line creation.
        :raises ValidationError: If essential line data is missing or invalid.
        """
        if not line_payload.name:
            raise ValidationError(_("Bill line description ('name') is required."))
        if not line_payload.account_id and not line_payload.product_id:
            raise ValidationError(_("Each bill line must have either a product_id or an explicit account_id specified."))

        line_vals = {
            'name': line_payload.name,
            'quantity': line_payload.quantity if line_payload.quantity is not None else 1.0,
            'price_unit': line_payload.price_unit if line_payload.price_unit is not None else 0.0,
            'display_type': False, # Standard line item
        }

        # Handle product selection
        if line_payload.product_id:
            product = self.env['product.product'].browse(line_payload.product_id)
            if not product.exists():
                raise ValidationError(_("Product with ID %s not found for bill line.") % line_payload.product_id)
            line_vals['product_id'] = product.id
            # Odoo will try to derive account and taxes from product if not overridden
            # Default account for vendor bill line from product is property_account_expense_id or its category's equivalent

        # Handle explicit account (can override product's default account)
        if line_payload.account_id:
            account = self.env['account.account'].browse(line_payload.account_id)
            if not account.exists():
                raise ValidationError(_("Account with ID %s not found for bill line.") % line_payload.account_id)
            if account.deprecated:
                 raise ValidationError(_("Account '%s' (ID %s) is deprecated and cannot be used for bill line.") % (account.name, account.id))
            # Basic check for account type (ideally an expense type for vendor bills)
            # This check can be more stringent based on company's CoA setup.
            if account.account_type not in ('expense', 'asset_current', 'asset_non_current', 'liability_current', 'liability_non_current', 'equity', 'off_balance'): # common types for bills
                 _logger.warning(f"Account '{account.name}' (ID {account.id}) used on bill line is not a typical expense type ({account.account_type}).")
            line_vals['account_id'] = account.id
        elif not line_payload.product_id: # If no product and no account, it's an error (caught earlier)
            pass


        # Handle taxes
        if line_payload.tax_ids:
            taxes = self.env['account.tax'].browse(line_payload.tax_ids)
            if len(taxes) != len(line_payload.tax_ids):
                raise ValidationError(_("One or more tax IDs provided for a bill line are invalid."))
            # Ensure taxes are for 'purchase' type
            for tax in taxes:
                if tax.type_tax_use != 'purchase':
                    raise ValidationError(_("Tax '%s' (ID %s) is not applicable for purchases/vendor bills.") % (tax.name, tax.id))
            line_vals['tax_ids'] = [(6, 0, line_payload.tax_ids)]
        
        # Odoo 16+ analytic distribution. `analytic_account_id` is deprecated for `account.move.line`.
        # if hasattr(line_payload, 'analytic_distribution') and line_payload.analytic_distribution:
        # line_vals['analytic_distribution'] = line_payload.analytic_distribution # Dict: {analytic_account_id: percentage}
        # For older versions or if analytic_account_id is still used for simple cases:
        # if hasattr(line_payload, 'analytic_account_id') and line_payload.analytic_account_id:
        # line_vals['analytic_account_id'] = line_payload.analytic_account_id

        return line_vals

    @api.model
    def create_vendor_bill_for_influencer_payment(self, payload: VendorBillPayload) -> models.Model:
        """
        Creates a single Vendor Bill (account.move) in Odoo Accounting for an influencer payment.
        REQ-IPF-006, REQ-2-014

        :param payload: DTO containing the vendor bill data.
        :return: The created Odoo 'account.move' record.
        :raises ValidationError: If payload data is invalid or fails Odoo's ORM validation.
        :raises UserError: For other Odoo-specific operational errors during creation.
        """
        _logger.info(f"Attempting to create vendor bill for influencer partner ID: {payload.influencer_partner_id}")

        if not payload.invoice_line_ids:
            # This should be caught by DTO's __post_init__ but double-check.
            raise ValidationError(_("Cannot create a vendor bill without any lines."))

        # Validate Partner
        partner = self.env['res.partner'].browse(payload.influencer_partner_id)
        if not partner.exists():
            raise ValidationError(_("Influencer partner with ID %s not found.") % payload.influencer_partner_id)

        # Validate Currency
        currency = self.env['res.currency'].browse(payload.currency_id)
        if not currency.exists():
            raise ValidationError(_("Currency with ID %s not found.") % payload.currency_id)

        # Validate Journal
        journal = self.env['account.journal'].browse(payload.journal_id)
        if not journal.exists():
            raise ValidationError(_("Journal with ID %s not found.") % payload.journal_id)
        if journal.type != 'purchase':
            raise ValidationError(_("Journal '%s' (ID %s) is not a 'Purchase' type journal suitable for vendor bills.") % (journal.name, journal.id))
        if journal.company_id != self.env.company: # Ensure journal belongs to current company context
             _logger.warning(f"Journal '{journal.name}' belongs to company '{journal.company_id.name}' which might differ from current context company '{self.env.company.name}'.")


        # Prepare line values
        bill_lines_vals_list = []
        for i, line_payload_item in enumerate(payload.invoice_line_ids):
            try:
                line_vals = self._prepare_vendor_bill_line_vals(line_payload_item, currency)
                bill_lines_vals_list.append((0, 0, line_vals))
            except ValidationError as e:
                 raise ValidationError(_("Error on bill line %s: %s") % (i + 1, e.args[0])) from e

        # Prepare main bill values
        invoice_date = payload.invoice_date or fields.Date.context_today(self)
        accounting_date = payload.date or invoice_date # Default accounting date to invoice date if not specified

        bill_vals = {
            'partner_id': partner.id,
            'move_type': 'in_invoice',  # Vendor Bill type
            'currency_id': currency.id,
            'journal_id': journal.id,
            'company_id': self.env.company.id, # Explicitly set company
            'invoice_date': invoice_date,
            'date': accounting_date, # Accounting Date
            'invoice_date_due': payload.invoice_date_due, # Due Date
            'narration': payload.narration, # Internal notes / memo
            'ref': payload.payment_reference, # Vendor Reference (e.g., campaign ID, payment batch ID)
            'invoice_line_ids': bill_lines_vals_list,
            # Link to InfluenceGen Campaign/Content if custom fields are added to 'account.move'
            # 'x_studio_influencegen_campaign_id': payload.campaign_id_internal, (example custom field)
        }

        _logger.debug(f"Creating account.move with vals: {bill_vals}")

        try:
            vendor_bill = self.env['account.move'].create(bill_vals)
            _logger.info(f"Vendor bill created successfully with ID: {vendor_bill.id} (Name: {vendor_bill.name}) for partner ID: {partner.id}")
            
            # The bill is created in 'Draft' state. Posting is a separate accounting step.
            # Example: If auto-posting is a requirement (use with extreme caution):
            # if vendor_bill.state == 'draft':
            #     vendor_bill.action_post()
            #     _logger.info(f"Vendor bill ID: {vendor_bill.id} automatically posted.")
            return vendor_bill
        except (UserError, ValidationError) as e:
            _logger.error(f"Odoo validation/user error creating vendor bill for partner {partner.id}: {e}")
            raise # Re-raise Odoo's specific errors
        except Exception as e:
            _logger.exception(f"Unexpected error creating vendor bill for partner {partner.id}: {e}")
            # Wrap unexpected errors in a UserError for better display in Odoo UI
            raise UserError(_("An unexpected error occurred while creating the vendor bill. Details: %s") % str(e))


    @api.model
    def create_payment_batch_vendor_bills(self, batch_payloads: List[VendorBillPayload]) -> List[models.Model]:
        """
        Creates multiple Vendor Bills for a batch of influencer payments.
        Processes each payload individually and collects successfully created bills.
        Failures are logged but do not stop the processing of subsequent items in the batch.
        REQ-IPF-006, REQ-2-014

        :param batch_payloads: List of VendorBillPayload DTOs.
        :return: A list of Odoo 'account.move' records for successfully created bills.
        """
        num_payloads = len(batch_payloads)
        _logger.info(f"Starting batch creation of {num_payloads} vendor bills.")
        
        # Use Odoo's empty recordset for accumulation
        successful_bills_recordset = self.env['account.move']
        failed_creations_info = []

        for i, payload in enumerate(batch_payloads):
            _logger.info(f"Processing batch item {i + 1}/{num_payloads} for influencer partner ID: {payload.influencer_partner_id}")
            try:
                # Using a savepoint allows atomicity per bill creation if desired.
                # However, Odoo's `create` itself is usually atomic for that record.
                # If subsequent actions on the bill (like auto-posting) were part of this loop,
                # savepoints would be more critical for rollback of that single item.
                with self.env.cr.savepoint(): # Create a savepoint for this iteration
                    bill = self.create_vendor_bill_for_influencer_payment(payload)
                    successful_bills_recordset += bill # Add to recordset
                    _logger.info(f"Successfully created vendor bill (batch item {i + 1}): ID {bill.id} for partner {payload.influencer_partner_id}")

            except (UserError, ValidationError) as e:
                # self.env.cr.rollback() # Rollback to savepoint if an Odoo error occurs
                _logger.error(
                    f"Failed to create vendor bill for partner ID {payload.influencer_partner_id} (batch item {i + 1}) due to Odoo Error: {e.args[0]}"
                )
                failed_creations_info.append({
                    "influencer_partner_id": payload.influencer_partner_id,
                    "payment_reference": payload.payment_reference,
                    "error": e.args[0]
                })
            except Exception as e:
                # self.env.cr.rollback() # Rollback for unexpected errors too
                _logger.exception(
                    f"Unexpected error creating vendor bill for partner ID {payload.influencer_partner_id} (batch item {i + 1}): {e}"
                )
                failed_creations_info.append({
                    "influencer_partner_id": payload.influencer_partner_id,
                    "payment_reference": payload.payment_reference,
                    "error": str(e)
                })

        num_successful = len(successful_bills_recordset)
        num_failed = len(failed_creations_info)
        _logger.info(f"Batch vendor bill creation completed. Successful: {num_successful}, Failed: {num_failed}.")

        if failed_creations_info:
            _logger.warning("Summary of failed vendor bill creations in batch:")
            for failure in failed_creations_info:
                _logger.warning(
                    f"- Partner ID: {failure['influencer_partner_id']}, Ref: {failure['payment_reference']}, Error: {failure['error']}"
                )
            # Depending on desired behavior, could raise a summary UserError here,
            # or simply return the list of successful bills and expect calling code to check logs.
            # For this SDS, we log and return successful ones.

        return successful_bills_recordset # Return recordset of successfully created bills