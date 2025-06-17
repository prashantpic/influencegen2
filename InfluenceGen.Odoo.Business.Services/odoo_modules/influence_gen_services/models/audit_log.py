# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AuditLog(models.Model):
    """
    InfluenceGen Audit Log
    Stores detailed records of auditable events within the InfluenceGen platform.
    This model provides a dedicated, tamper-evident store for all significant
    system events and user actions.
    Access to this model should be highly restricted. Creation is handled by
    BaseAuditMixin or dedicated services.
    REQ-ATEL-005, REQ-ATEL-006, REQ-ATEL-007, REQ-IOKYC-016, REQ-2-018,
    REQ-AIGS-012, REQ-IPF-009
    """
    _name = 'influence_gen.audit_log'
    _description = 'InfluenceGen Audit Log'
    _order = 'timestamp desc, id desc' # Added id desc for secondary sort for very close timestamps

    timestamp = fields.Datetime(
        string='Timestamp (UTC)', 
        required=True, 
        default=fields.Datetime.now, 
        readonly=True, 
        index=True,
        help="The exact date and time (UTC) when the event occurred."
    )
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string='User/Actor', 
        readonly=True, 
        ondelete='set null', # Keep log even if user is deleted
        index=True, 
        help="User who performed the action. System if None (for automated processes)."
    )
    event_type = fields.Char(
        string='Event Type', 
        required=True, 
        readonly=True, 
        index=True, 
        help="Categorization of the event, e.g., 'model_name.action', 'user.login', 'kyc.status.change'."
    )
    target_model = fields.Char(
        string='Target Model', 
        readonly=True, 
        index=True, 
        help="Technical name of the Odoo model affected by the event, e.g., 'influence_gen.campaign'."
    )
    # Using Integer for res_id as it's common in Odoo, though Char could offer flexibility for non-integer IDs.
    target_res_id = fields.Integer(
        string='Target Record ID', 
        readonly=True, 
        index=True, 
        help="ID of the affected record in the target_model. 0 or None if not applicable."
    )
    action = fields.Char(
        string='Action Performed', 
        required=True, 
        readonly=True, 
        help="Specific action performed, e.g., 'create', 'write', 'unlink', 'approve', 'login_success', 'login_failure'."
    )
    details_json = fields.Text(
        string='Details (JSON)', 
        readonly=True, 
        help="JSON string containing event-specific details, such as changed field values (old/new), parameters, or context information."
    )
    ip_address = fields.Char(
        string='Source IP Address', 
        readonly=True,
        help="IP address from which the action originated, if available."
    )
    outcome = fields.Selection([
        ('success', 'Success'), 
        ('failure', 'Failure')
        ], 
        string='Outcome', 
        required=True, 
        readonly=True, 
        default='success',
        help="Indicates whether the logged action was successful or resulted in a failure."
    )
    failure_reason = fields.Text(
        string='Failure Reason', 
        readonly=True, 
        help="Detailed reason if the outcome of the action was a failure."
    )
    legal_hold_status = fields.Boolean(
        string='Under Legal Hold', 
        default=False, 
        copy=False, 
        readonly=True,
        help="Indicates if this specific log entry itself is under a legal hold (rare, but for completeness or specific regulatory needs)."
    )
    correlation_id = fields.Char(
        string='Correlation ID', 
        readonly=True, 
        index=True, 
        help="An ID used to trace a single request or operation across multiple system components or log entries."
    )

    # To prevent direct modification or deletion of audit logs through standard UI/ORM by non-privileged users.
    # Actual enforcement will primarily be via ir.model.access.csv and ir.rule.
    # This is more of a declaration of intent for the model.
    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        """
        Override to potentially restrict write/unlink for most users.
        Actual security is defined in XML/CSV. This is a safeguard.
        """
        if operation in ('write', 'unlink'):
            # Allow for superuser or specific audit admin group if defined
            if not self.env.is_superuser() and not self.env.user.has_group('base.group_system'): # Example admin group
                if raise_exception:
                    raise models.AccessError(_("Audit log records cannot be modified or deleted."))
                return False
        return super(AuditLog, self).check_access_rights(operation, raise_exception=raise_exception)

    @api.model
    def create(self, vals):
        # Ensure that create is only possible by system/sudo context (e.g. from BaseAuditMixin)
        # This is a soft check; main security is via ir.model.access.csv
        if not self.env.is_superuser() and self.env.uid: # Check if not superuser and not a system call (uid is set)
             # Allow if called via sudo() by checking effective user vs session user
            if self.env.uid != self.env.su:
                 pass # Likely a sudo() call, allow
            # else:
            #     # This might be too restrictive if services need to create logs directly without sudo
            #     # For now, rely on BaseAuditMixin's sudo() and CSV security.
            #     pass
            _logger.debug(f"Attempt to create audit log by non-superuser/non-system context. User: {self.env.user.login if self.env.user else 'N/A'}")
        return super(AuditLog, self).create(vals)