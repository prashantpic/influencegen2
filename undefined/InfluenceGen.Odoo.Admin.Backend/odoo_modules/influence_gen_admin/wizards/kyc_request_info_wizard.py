from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class KycRequestInfoWizard(models.TransientModel):
    _name = 'influence_gen.kyc_request_info_wizard'
    _description = 'KYC Request More Information Wizard'

    kyc_submission_id = fields.Many2one(
        comodel_name='influence_gen.kyc_data', # Assuming model from influence_gen_services
        string='KYC Submission',
        required=True,
        readonly=True,
        ondelete='cascade' # If KYC submission is deleted, wizard instance becomes invalid
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
            kyc_submission = self.env['influence_gen.kyc_data'].browse(self.env.context['active_id'])
            if kyc_submission.exists():
                res['kyc_submission_id'] = kyc_submission.id
        return res

    def action_send_request(self):
        self.ensure_one()
        if not self.kyc_submission_id:
            raise UserError(_("KYC Submission is not set."))

        if self.kyc_submission_id.verification_status not in ('pending', 'in_review'):
            raise UserError(_("Cannot request more information for a KYC submission that is not 'Pending' or 'In Review'."))

        # Update KYC submission status
        self.kyc_submission_id.write({
            'verification_status': 'needs_more_info',
            'notes': (self.kyc_submission_id.notes or '') + \
                     f"\n\n--- Request for More Information ({fields.Datetime.now()}) by {self.env.user.name} ---\n" + \
                     self.message_to_influencer
        })
        
        _logger.info(
            f"KYC submission {self.kyc_submission_id.id} status updated to 'needs_more_info'."
        )

        # Trigger email notification to the influencer
        # This assumes kyc_submission_id.influencer_profile_id.user_id.partner_id.email exists
        influencer_profile = self.kyc_submission_id.influencer_profile_id
        if not influencer_profile or not hasattr(influencer_profile, 'user_id') or not influencer_profile.user_id.partner_id.email:
            _logger.warning(
                f"Cannot send 'request more info' email for KYC {self.kyc_submission_id.id}: Influencer email not found."
            )
        else:
            partner_to = influencer_profile.user_id.partner_id
            
            # Try to find a suitable mail template or send a direct mail
            # Example: using mail.template (template needs to be defined)
            # template = self.env.ref('influence_gen_admin.mail_template_kyc_request_more_info', raise_if_not_found=False)
            # if template:
            #     template.with_context(message_to_influencer=self.message_to_influencer).send_mail(
            #         self.kyc_submission_id.id,
            #         force_send=True,
            #         email_values={'recipient_ids': [(4, partner_to.id)]}
            #     )
            # else:
            # Fallback to direct mail.mail
            subject = _("Additional Information Required for Your KYC Verification")
            body_html = _("""
                <p>Dear %s,</p>
                <p>We require additional information to complete the verification of your KYC submission. Please find the details below:</p>
                <p><strong>Message from our team:</strong></p>
                <p>%s</p>
                <p>Please log in to your InfluenceGen account to provide the requested information or update your submission.</p>
                <p>Thank you for your cooperation.</p>
                <p>Sincerely,<br/>The InfluenceGen Team</p>
            """) % (partner_to.name, self.message_to_influencer.replace('\n', '<br/>'))

            mail_values = {
                'subject': subject,
                'body_html': body_html,
                'email_to': partner_to.email_formatted,
                'auto_delete': True,
                'state': 'outgoing',
                'model': 'influence_gen.kyc_data',
                'res_id': self.kyc_submission_id.id,
            }
            self.env['mail.mail'].create(mail_values) #.send() # or let cron handle
            _logger.info(f"Email notification for more KYC info sent to {partner_to.email}.")


        # Log the action in the audit trail (Placeholder - assumes audit log service/model)
        # self.env['influence_gen.audit_log'].sudo().create_log_entry(
        #     actor_user_id=self.env.user.id,
        #     event_type='kyc_request_info',
        #     action='request_more_info',
        #     target_entity='influence_gen.kyc_data',
        #     target_id=self.kyc_submission_id.id,
        #     details={'message_sent': self.message_to_influencer}
        # )
        
        # Post a message on the KYC submission chatter
        self.kyc_submission_id.message_post(
            body=_("Requested more information from influencer: %s") % self.message_to_influencer,
            subject=_("More Information Requested for KYC"),
            message_type='comment',
            subtype_id=self.env.ref('mail.mt_note').id
        )

        return {'type': 'ir.actions.act_window_close'}