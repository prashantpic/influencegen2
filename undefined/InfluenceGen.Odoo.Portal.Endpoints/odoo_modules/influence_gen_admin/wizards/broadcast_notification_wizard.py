from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class BroadcastNotificationWizard(models.TransientModel):
    _name = 'influence_gen.broadcast_notification_wizard'
    _description = 'Broadcast Notification Wizard'

    message_subject = fields.Char(string='Subject', required=True)
    message_body = fields.Html(string='Message Body', required=True)
    target_user_group_ids = fields.Many2many(
        comodel_name='res.groups',
        string='Target User Groups',
        help="Leave empty to target all active internal users and portal users (influencers if they are portal users)."
    )
    target_influencer_ids = fields.Many2many(
        comodel_name='influence_gen.influencer_profile', # Assuming this model exists
        string="Specific Influencers"
    )
    send_email = fields.Boolean(string='Send as Email', default=True)
    show_in_app_banner_duration_hours = fields.Integer(
        string='Show In-App Banner (Hours)',
        help="0 for no banner. In-app banner functionality needs a separate implementation."
    )

    def action_send_notification(self):
        self.ensure_one()
        target_partners = self.env['res.partner']
        target_user_emails = set()

        if self.target_influencer_ids:
            # Assuming influencer_profile has a partner_id or user_id.partner_id
            for influencer in self.target_influencer_ids:
                if hasattr(influencer, 'user_id') and influencer.user_id.partner_id:
                    target_partners |= influencer.user_id.partner_id
                    if influencer.user_id.partner_id.email:
                         target_user_emails.add(influencer.user_id.partner_id.email_normalized)
                elif hasattr(influencer, 'partner_id'): # Fallback if direct partner_id
                     target_partners |= influencer.partner_id
                     if influencer.partner_id.email:
                         target_user_emails.add(influencer.partner_id.email_normalized)


        if self.target_user_group_ids:
            for group in self.target_user_group_ids:
                for user in group.users:
                    if user.partner_id:
                        target_partners |= user.partner_id
                        if user.partner_id.email:
                            target_user_emails.add(user.partner_id.email_normalized)
        
        if not self.target_influencer_ids and not self.target_user_group_ids:
            # Target all active internal and portal users
            all_users = self.env['res.users'].search([('active', '=', True)])
            for user in all_users:
                 if user.partner_id:
                    target_partners |= user.partner_id
                    if user.partner_id.email:
                        target_user_emails.add(user.partner_id.email_normalized)


        if not target_partners and not target_user_emails:
            raise UserError(_("No recipients found for this notification."))

        if self.send_email:
            if not target_user_emails: # or check target_partners with email
                _logger.warning("Broadcast notification: No valid email addresses found for selected recipients.")
            else:
                # Using mail.mail to send individual emails
                # For mass mailing, consider using 'mailing.mailing' model if available and suitable
                # This ensures individual emails are sent, which is better for privacy and tracking
                mail_obj = self.env['mail.mail']
                for partner in target_partners:
                    if partner.email:
                        mail_values = {
                            'subject': self.message_subject,
                            'body_html': self.message_body,
                            'email_to': partner.email_formatted,
                            'auto_delete': True, # Delete mail.mail record after sending
                            'state': 'outgoing', # Set to outgoing to be picked by cron
                        }
                        mail_id = mail_obj.create(mail_values)
                        # mail_id.send() # Optionally send immediately, or let cron handle
                _logger.info(f"Broadcast email notifications queued for {len(target_partners)} partners.")


        if self.show_in_app_banner_duration_hours > 0:
            # Placeholder: Logic to create in-app banner records
            # This requires a dedicated model for banners (e.g., 'influence_gen.system_banner')
            # and UI components to display them.
            _logger.info(
                f"In-app banner requested for {self.show_in_app_banner_duration_hours} hours. "
                "Banner creation logic needs to be implemented using a dedicated model and UI."
            )
            # Example:
            # banner_model = self.env.get('influence_gen.system_banner')
            # if banner_model:
            #     banner_model.create({
            #         'message': self.message_body, # Potentially strip HTML or use a plain text version
            #         'subject': self.message_subject,
            #         'display_from': fields.Datetime.now(),
            #         'display_until': fields.Datetime.add(fields.Datetime.now(), hours=self.show_in_app_banner_duration_hours),
            #         'target_group_ids': [(6, 0, self.target_user_group_ids.ids)],
            #         'target_partner_ids': [(6, 0, target_partners.ids)], # if banner system supports partner targeting
            #         'is_active': True,
            #     })
            # else:
            #     _logger.warning("In-app banner model 'influence_gen.system_banner' not found.")
            pass


        # Log the broadcast action
        self.env['mail.message'].create({
            'model': self._name, # or a central log model
            'res_id': self.id, # For transient model, this might not be ideal. Could log on a config model or custom log.
            'body': _('Broadcast notification sent: "%s" to selected targets.', self.message_subject),
            'message_type': 'comment',
            'subtype_id': self.env.ref('mail.mt_note').id,
        })
        
        # Optionally create an audit log entry
        # self.env['influence_gen.audit_log'].sudo().create_log_entry(
        #     actor_user_id=self.env.user.id,
        #     event_type='broadcast_notification_sent',
        #     action='send',
        #     target_entity=self._name, # Or a more appropriate entity
        #     details={
        #         'subject': self.message_subject,
        #         'target_groups': self.target_user_group_ids.mapped('name'),
        #         'target_influencers_count': len(self.target_influencer_ids),
        #         'sent_as_email': self.send_email,
        #         'in_app_banner_hours': self.show_in_app_banner_duration_hours,
        #     }
        # )

        return {'type': 'ir.actions.act_window_close'}