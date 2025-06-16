from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class MaintenanceWindow(models.Model):
    _name = 'influence_gen.maintenance_window'
    _description = "InfluenceGen Maintenance Window"

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
        copy=False
    )

    def action_send_notification(self):
        for record in self:
            if record.notify_users:
                # Placeholder for notification logic
                # This would typically involve creating mail.mail records or using a custom notification system.
                _logger.info(
                    "Sending maintenance notification for '%s': Message: %s",
                    record.name,
                    record.notification_message or "Default maintenance notification."
                )
                # Example:
                # if record.notification_message:
                #     # Find target users (e.g., all active users or specific groups)
                #     # self.env['mail.mail'].create({...})
                #     pass
            else:
                _logger.info("Notification not enabled for maintenance window '%s'", record.name)
        return True

    def action_start_maintenance(self):
        self.write({'status': 'in_progress'})
        _logger.info("Maintenance window '%s' started.", self.mapped('name'))
        return True

    def action_complete_maintenance(self):
        self.write({'status': 'completed'})
        _logger.info("Maintenance window '%s' completed.", self.mapped('name'))
        return True

    def action_cancel_maintenance(self):
        self.write({'status': 'cancelled'})
        _logger.info("Maintenance window '%s' cancelled.", self.mapped('name'))
        return True