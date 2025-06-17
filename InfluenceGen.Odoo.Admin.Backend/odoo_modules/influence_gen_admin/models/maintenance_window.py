from odoo import api, fields, models, _
from odoo.exceptions import UserError

class MaintenanceWindow(models.Model):
    _name = 'influence_gen.maintenance_window'
    _description = 'InfluenceGen Maintenance Window'
    _order = 'start_datetime desc'

    name = fields.Char(
        required=True,
        string='Title'
    )
    start_datetime = fields.Datetime(
        required=True,
        string='Start Time'
    )
    end_datetime = fields.Datetime(
        required=True,
        string='End Time'
    )
    description = fields.Text(
        string='Description/Impact'
    )
    notify_users = fields.Boolean(
        string='Notify Users',
        default=True
    )
    notification_message = fields.Text(
        string='Notification Message',
        help="Custom message for user notification. If empty, a default message will be used."
    )
    status = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        string="Status",
        default="planned",
        readonly=True,
        copy=False,
        tracking=True
    )

    def action_send_notification(self):
        self.ensure_one()
        if not self.notify_users:
            raise UserError(_("User notification is disabled for this maintenance window."))

        # Placeholder: Logic to send notification.
        # This could involve:
        # 1. Opening the `influence_gen.broadcast_notification_wizard` with pre-filled details.
        # 2. Directly creating `mail.mail` records and sending emails.
        # 3. Creating in-app banner records if such a system exists.

        message_subject = _("Maintenance Window Notification: %s") % self.name
        message_body = self.notification_message
        if not message_body:
            message_body = _("<p>Dear User,</p>"
                             "<p>Please be advised of a planned maintenance window for the InfluenceGen platform:</p>"
                             "<ul>"
                             "<li><strong>Title:</strong> %s</li>"
                             "<li><strong>Start Time:</strong> %s</li>"
                             "<li><strong>End Time:</strong> %s</li>"
                             "<li><strong>Description:</strong> %s</li>"
                             "</ul>"
                             "<p>During this period, platform services may be temporarily unavailable or experience disruptions.</p>"
                             "<p>We apologize for any inconvenience caused.</p>"
                             "<p>Sincerely,<br/>The InfluenceGen Team</p>") % (
                                 self.name,
                                 self.start_datetime,
                                 self.end_datetime,
                                 self.description or _("N/A")
                             )
        
        # Example of opening broadcast wizard:
        # This requires the wizard to handle pre-filled values from context
        # or to have a method to create a notification from parameters.
        # For simplicity here, we log it. In a real scenario, integrate with actual notification mechanisms.

        self.env['mail.message'].create({
            'model': self._name,
            'res_id': self.id,
            'body': _('Notification about maintenance window "%s" was triggered for users (simulation). Actual sending logic to be implemented.', self.name),
            'message_type': 'comment',
            'subtype_id': self.env.ref('mail.mt_note').id,
        })

        # Example: Opening broadcast notification wizard
        # action = self.env['ir.actions.actions']._for_xml_id('influence_gen_admin.action_broadcast_notification_wizard')
        # action['context'] = {
        #     'default_message_subject': message_subject,
        #     'default_message_body': message_body,
        #     # 'default_target_user_group_ids': [(6, 0, [self.env.ref('base.group_user').id])], # Example target
        # }
        # return action
        return True


    def action_start_maintenance(self):
        for record in self:
            if record.status != 'planned':
                raise UserError(_("Maintenance window can only be started if it's in 'Planned' state."))
            record.status = 'in_progress'
            record.message_post(body=_("Maintenance window started."))

    def action_complete_maintenance(self):
        for record in self:
            if record.status != 'in_progress':
                raise UserError(_("Maintenance window can only be completed if it's 'In Progress'."))
            record.status = 'completed'
            record.message_post(body=_("Maintenance window completed."))

    def action_cancel_maintenance(self):
        for record in self:
            if record.status in ('completed', 'cancelled'):
                raise UserError(_("Cannot cancel a maintenance window that is already '%s'.") % record.status)
            record.status = 'cancelled'
            record.message_post(body=_("Maintenance window cancelled."))