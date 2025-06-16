from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class BroadcastNotificationWizard(models.TransientModel):
    _name = 'influence_gen.broadcast_notification_wizard'
    _description = 'InfluenceGen Broadcast Notification Wizard'

    message_subject = fields.Char(
        string='Subject',
        required=True
    )
    message_body = fields.Html(
        string='Message Body',
        required=True
    )
    target_user_group_ids = fields.Many2many(
        comodel_name='res.groups',
        string='Target User Groups',
        help="Leave empty to target all active internal users and portal users (influencers)."
    )
    target_influencer_ids = fields.Many2many(
        comodel_name='influence_gen.influencer_profile', # Assuming this model exists in influence_gen_services
        string="Specific Influencers"
    )
    send_email = fields.Boolean(
        string='Send as Email',
        default=True
    )
    show_in_app_banner_duration_hours = fields.Integer(
        string='Show In-App Banner (Hours)',
        help="0 for no banner."
    )

    def action_send_notification(self):
        self.ensure_one()
        target_users = self.env['res.users']
        
        # Collect users from groups
        if self.target_user_group_ids:
            target_users |= self.env['res.users'].search([('groups_id', 'in', self.target_user_group_ids.ids)])
        
        # Collect users from specific influencers
        if self.target_influencer_ids:
            # Assuming influence_gen.influencer_profile has a user_id field linking to res.users
            influencer_user_ids = self.target_influencer_ids.mapped('user_id').filtered(lambda u: u) # Ensure user_id exists
            if influencer_user_ids:
                target_users |= influencer_user_ids

        # If no specific targets, consider all active internal and portal users
        if not target_users and not self.target_user_group_ids and not self.target_influencer_ids:
            # This logic might need refinement based on how "all active portal users (influencers)" are identified
            # For now, let's assume all active users.
             target_users = self.env['res.users'].search([('active', '=', True)])


        _logger.info(
            "Broadcast Notification Wizard: Preparing to send to %d users.",
            len(target_users)
        )

        if self.send_email and target_users:
            # Placeholder: Actual email sending logic
            # Typically, you would create mail.mail records or use mail.template
            mail_values = []
            for user in target_users:
                if user.email: # Ensure user has an email
                    # Simplified email sending for placeholder
                    # In a real scenario, use self.env['mail.mail'].create() or mail templates
                    _logger.info(
                        "Simulating email send to %s (User: %s) with subject: %s",
                        user.email, user.name, self.message_subject
                    )
            # Example with mail.mail (requires proper setup of mail server etc.)
            # mail_server = self.env['ir.mail_server'].search([], limit=1)
            # if mail_server:
            #     for user in target_users:
            #         if user.partner_id: # mail.mail sends to partners
            #             mail = self.env['mail.mail'].create({
            #                 'subject': self.message_subject,
            #                 'body_html': self.message_body,
            #                 'email_to': user.partner_id.email,
            #                 'recipient_ids': [(4, user.partner_id.id)],
            #                 # 'author_id': self.env.user.partner_id.id, # Optional: sender
            #             })
            #             # mail.send() # or let the cron job handle it
            # else:
            #     _logger.warning("No mail server configured. Cannot send broadcast emails.")


        if self.show_in_app_banner_duration_hours > 0:
            # Placeholder: In-app banner creation logic
            # This would require a separate model and UI component for displaying banners.
            _logger.info(
                "Simulating in-app banner creation for %d hours. Message: %s",
                self.show_in_app_banner_duration_hours,
                self.message_body[:100] # Log a snippet
            )
            # Example:
            # self.env['influence_gen.system_banner'].create({
            #     'message': self.message_body,
            #     'expiry_datetime': fields.Datetime.now() + timedelta(hours=self.show_in_app_banner_duration_hours),
            #     'target_group_ids': [(6, 0, self.target_user_group_ids.ids)] # if banner is group-specific
            # })
        
        return {'type': 'ir.actions.act_window_close'}