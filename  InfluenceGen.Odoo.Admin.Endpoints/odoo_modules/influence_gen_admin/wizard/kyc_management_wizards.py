# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError

# REQ-IOKYC-011: KYC Management Wizards
class KycRejectionWizard(models.TransientModel):
    _name = 'influence_gen.kyc_rejection_wizard'
    _description = 'KYC Rejection Wizard'

    kyc_data_id = fields.Many2one(
        'influence_gen.kyc_data',
        string='KYC Submission',
        required=True,
        readonly=True,
        ondelete='cascade'
    )
    rejection_reason = fields.Text(string='Rejection Reason', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super(KycRejectionWizard, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'influence_gen.kyc_data' and self.env.context.get('active_id'):
            res['kyc_data_id'] = self.env.context.get('active_id')
        return res

    def action_confirm_rejection(self):
        # REQ-IOKYC-011, REQ-16-002 (Notification via Business Service)
        self.ensure_one()
        if not self.kyc_data_id:
            raise UserError(_("No KYC Submission linked to this wizard."))

        # Call the business service layer to handle the logic
        try:
            self.kyc_data_id.sudo()._service_reject_kyc(self.rejection_reason)
        except Exception as e:
            # Log the exception and show a user-friendly error
            # This allows the business service to raise specific UserErrors if needed
            raise UserError(_("Failed to reject KYC submission: %s") % str(e))

        return {'type': 'ir.actions.act_window_close'}


class KycRequestInfoWizard(models.TransientModel):
    _name = 'influence_gen.kyc_request_info_wizard'
    _description = 'KYC Request More Info Wizard'

    kyc_data_id = fields.Many2one(
        'influence_gen.kyc_data',
        string='KYC Submission',
        required=True,
        readonly=True,
        ondelete='cascade'
    )
    info_request_message = fields.Text(string='Information Request Message', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super(KycRequestInfoWizard, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'influence_gen.kyc_data' and self.env.context.get('active_id'):
            res['kyc_data_id'] = self.env.context.get('active_id')
        return res

    def action_send_info_request(self):
        # REQ-IOKYC-011, REQ-16-002 (Notification via Business Service)
        self.ensure_one()
        if not self.kyc_data_id:
            raise UserError(_("No KYC Submission linked to this wizard."))

        # Call the business service layer to handle the logic
        try:
            self.kyc_data_id.sudo()._service_request_more_kyc_info(self.info_request_message)
        except Exception as e:
            raise UserError(_("Failed to request more information for KYC: %s") % str(e))

        return {'type': 'ir.actions.act_window_close'}