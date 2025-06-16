import json
from odoo import models, fields, api, _

class InfluenceGenAuditLogEntry(models.Model):
    _name = 'influence_gen.audit_log_entry'
    _description = "System Audit Log Entry"
    _order = 'timestamp desc'

    timestamp = fields.Datetime(string="Timestamp (UTC)", default=fields.Datetime.now, required=True, readonly=True, index=True)
    event_type = fields.Char(string="Event Type", required=True, index=True)
    actor_user_id = fields.Many2one('res.users', string="Actor User", ondelete='set null', readonly=True, index=True)
    actor_description = fields.Char(string="Actor Description", compute='_compute_actor_description', store=True, readonly=True)
    target_model_name = fields.Char(string="Target Model", readonly=True, index=True)
    target_record_id = fields.Integer(string="Target Record ID", readonly=True, index=True)
    target_record_display_name = fields.Char(string="Target Record Name", compute='_compute_target_display_name', store=False, readonly=True)
    action_performed = fields.Char(string="Action Performed", required=True, readonly=True) # e.g., 'CREATE', 'WRITE', 'UNLINK', 'LOGIN_ATTEMPT'
    details_json = fields.Text(string="Details (JSON)", readonly=True)
    ip_address = fields.Char(string="Source IP Address", readonly=True)
    outcome = fields.Selection([
        ('success', 'Success'),
        ('failure', 'Failure')
    ], string="Outcome", readonly=True, default='success') # Default to success unless specified
    failure_reason = fields.Text(string="Failure Reason", readonly=True)

    @api.model
    def create_log(cls, event_type, actor_user_id, action_performed, target_object=None, details_dict=None, ip_address=None, outcome='success', failure_reason=None):
        vals = {
            'timestamp': fields.Datetime.now(), # Ensure it's set on creation
            'event_type': event_type,
            'actor_user_id': actor_user_id.id if hasattr(actor_user_id, 'id') else actor_user_id, # Can be int or record
            'action_performed': action_performed,
            'ip_address': ip_address,
            'outcome': outcome,
            'failure_reason': failure_reason,
        }
        if target_object and isinstance(target_object, models.BaseModel) and target_object.exists():
            vals['target_model_name'] = target_object._name
            vals['target_record_id'] = target_object.id
        
        if details_dict:
            try:
                vals['details_json'] = json.dumps(details_dict, default=str) # Use default=str for non-serializable objects like datetime
            except TypeError:
                vals['details_json'] = json.dumps({'error': 'Could not serialize details_dict'})
        
        return cls.create(vals)

    @api.depends('actor_user_id')
    def _compute_actor_description(self):
        for record in self:
            if record.actor_user_id:
                record.actor_description = record.actor_user_id.name
            else:
                record.actor_description = "System Process"

    # store=False as fetching display_name can be costly and might fail if record is deleted
    def _compute_target_display_name(self):
        for record in self:
            record.target_record_display_name = "" # Default
            if record.target_model_name and record.target_record_id:
                try:
                    if record.target_model_name in self.env:
                        target_model = self.env[record.target_model_name]
                        # Check if 'active' field exists for sudo access if record might be archived
                        if hasattr(target_model, 'active'):
                             target_rec = target_model.with_context(active_test=False).browse(record.target_record_id).exists()
                        else:
                             target_rec = target_model.browse(record.target_record_id).exists()

                        if target_rec:
                            record.target_record_display_name = target_rec.display_name
                        else:
                            record.target_record_display_name = _("[Record Deleted/Inaccessible]")
                    else:
                        record.target_record_display_name = _("[Model Unknown]")
                except Exception: # Catch broad exceptions as this is a display field
                    record.target_record_display_name = _("[Error Fetching Name]")