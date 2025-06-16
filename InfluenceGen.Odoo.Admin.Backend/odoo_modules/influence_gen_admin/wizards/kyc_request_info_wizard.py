from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class KycRequestInfoWizard(models.TransientModel):
    _name = 'influence_gen.kyc_request_info_wizard'
    _description = 'InfluenceGen KYC Request More Information Wizard'

    kyc_submission_id = fields.Many2one(
        comodel_name='influence_gen.kyc_data', # Assuming this model exists in influence_gen_services
        string='KYC Submission',
        required=True,
        readonly=True
    )
    message_to_influencer = fields.Text(
        string='Message to Influencer',
        required=True,
        help="Detail what additional information or clarification is needed."
    )

    @api.model
    def default_get(self, fields_list):
        res = super(KycRequestInfoWizard, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'influence_gen.kyc_data' and self.env.context.get('active_id'):
            res['kyc_submission_id'] = self.env.context.get('active_id')
        return res

    def action_send_request(self):
        self.ensure_one()
        if self.kyc_submission_id:
            # Update KYC submission status
            self.kyc_submission_id.write({'verification_status': 'needs_more_info'})
            
            # Append message to a communication log (e.g., mail.message on KYC record or influencer profile)
            # This is a common Odoo pattern.
            if hasattr(self.kyc_submission_id, 'message_post'):
                self.kyc_submission_id.message_post(
                    body=f"Requested more information from influencer: <br/>{self.message_to_influencer}",
                    subject="KYC: More Information Requested",
                    message_type='comment',
                    subtype_xmlid='mail.mt_note' # Generic note subtype
                )
            
            # Trigger an email notification (placeholder for actual email sending logic)
            # This would typically use mail.template
            _logger.info(
                "KYC Request More Info: Sending simulated email to influencer for KYC ID %s. Message: %s",
                self.kyc_submission_id.id,
                self.message_to_influencer
            )
            # Example using a mail template (template needs to be defined):
            # template = self.env.ref('influence_gen_admin.email_template_kyc_request_info', raise_if_not_found=False)
            # if template and self.kyc_submission_id.influencer_profile_id and self.kyc_submission_id.influencer_profile_id.user_id:
            #     template.with_context(
            #         message_to_influencer=self.message_to_influencer
            #     ).send_mail(self.kyc_submission_id.id, force_send=True) # Send to the KYC record, template handles recipient

            # Log the action in the audit trail (placeholder, actual audit logging is usually done by service layer on write)
            _logger.info(
                "Audit: KYC ID %s - More information requested by %s. Message: %s",
                self.kyc_submission_id.id,
                self.env.user.name,
                self.message_to_influencer
            )
            # An actual audit log entry would be created by the `influence_gen.audit_log` model,
            # potentially triggered by overrides on `write` of `influence_gen.kyc_data`.
            # Example:
            # self.env['influence_gen.audit_log'].sudo().create({
            #     'actor_user_id': self.env.uid,
            #     'event_type': 'kyc_update',
            #     'action': 'request_info',
            #     'target_entity': 'influence_gen.kyc_data',
            #     'target_id': self.kyc_submission_id.id,
            #     'details': {'message': self.message_to_influencer}
            # })

        return {'type': 'ir.actions.act_window_close'}