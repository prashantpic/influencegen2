# -*- coding: utf-8 -*-
import json
from odoo import api, fields, models, _
from odoo.http import request

class InfluenceGenAuditLogEntry(models.Model):
    _name = 'influence_gen.audit_log_entry'
    _description = "System Audit Log Entry"
    _order = 'timestamp desc'

    timestamp = fields.Datetime(
        string="Timestamp (UTC)", default=fields.Datetime.now,
        required=True, readonly=True, index=True
    )
    event_type = fields.Char(string="Event Type", required=True, index=True)
    actor_user_id = fields.Many2one(
        'res.users', string="Actor User",
        ondelete='set null', readonly=True, index=True
    )
    actor_description = fields.Char(
        string="Actor Description", compute='_compute_actor_description',
        store=True, readonly=True
    )
    target_model_name = fields.Char(string="Target Model", readonly=True, index=True)
    target_record_id = fields.Integer(string="Target Record ID", readonly=True, index=True)
    target_record_display_name = fields.Char(
        string="Target Record Name", compute='_compute_target_display_name',
        store=False, readonly=True # Not stored due to potential performance issues and deletion
    )
    action_performed = fields.Char(string="Action Performed", required=True, readonly=True)
    details_json = fields.Text(string="Details (JSON)", readonly=True)
    ip_address = fields.Char(string="Source IP Address", readonly=True)
    outcome = fields.Selection([
        ('success', 'Success'),
        ('failure', 'Failure')
    ], string="Outcome", readonly=True, default='success') # Default to success, override on failure
    failure_reason = fields.Text(string="Failure Reason", readonly=True)

    @api.model
    def create_log(cls, event_type, actor_user_id, action_performed,
                   target_object=None, details_dict=None, ip_address=None,
                   outcome='success', failure_reason=None):
        """Central method to create audit log entries. REQ-ATEL-005, REQ-ATEL-006."""
        
        vals = {
            'event_type': event_type,
            'actor_user_id': actor_user_id.id if actor_user_id else None,
            'action_performed': action_performed,
            'outcome': outcome,
            'failure_reason': failure_reason,
        }

        if target_object and isinstance(target_object, models.BaseModel) and target_object.exists():
            # Ensure target_object is a single record if providing ID
            if len(target_object) > 1 : # If it's a multi-recordset, log generally or iterate
                 _logger.warning("Audit log target_object is a multi-recordset. Logging general model or first record.")
                 # Decide on handling: log for model, or log for first record, or error
                 # For now, let's assume it should be a single record if ID is expected
                 # If logging for multiple records, target_record_id might be better left None and details_json used
                 vals['target_model_name'] = target_object[0]._name
                 # vals['target_record_id'] = target_object[0].id # Or handle differently
            else:
                vals['target_model_name'] = target_object._name
                vals['target_record_id'] = target_object.id if target_object.id else None # handles NewId
        elif target_object and isinstance(target_object, str): # if model name is passed
             vals['target_model_name'] = target_object


        if details_dict:
            try:
                vals['details_json'] = json.dumps(details_dict, default=str) # Use str for non-serializable
            except TypeError as e:
                _logger.error(f"Failed to serialize audit log details: {e}. Details: {details_dict}")
                vals['details_json'] = json.dumps({"error": "Failed to serialize details", "original_keys": list(details_dict.keys())})


        if not ip_address and request:
            vals['ip_address'] = request.httprequest.remote_addr if request.httprequest else None
        elif ip_address:
            vals['ip_address'] = ip_address
            
        return cls.sudo().create(vals) # Use sudo() to ensure logs are always created

    @api.depends('actor_user_id')
    def _compute_actor_description(self):
        for log in self:
            if log.actor_user_id:
                log.actor_description = log.actor_user_id.name
            else:
                log.actor_description = "System Process"

    def _compute_target_display_name(self):
        # This method is non-stored due to potential issues with deleted records
        # and performance on large datasets if stored.
        for log in self:
            log.target_record_display_name = "" # Default
            if log.target_model_name and log.target_record_id:
                try:
                    target_model = self.env[log.target_model_name]
                    # Check if model has 'display_name' or 'name'
                    if hasattr(target_model, '_rec_name') and target_model._rec_name:
                        rec_name_field = target_model._rec_name
                    elif 'display_name' in target_model._fields:
                        rec_name_field = 'display_name'
                    elif 'name' in target_model._fields:
                        rec_name_field = 'name'
                    else: # No standard name field
                        log.target_record_display_name = f"Record ID: {log.target_record_id}"
                        continue
                    
                    # Sudo to read in case regular user lost access
                    record = target_model.sudo().browse(log.target_record_id).exists()
                    if record:
                        log.target_record_display_name = record[rec_name_field]
                    else:
                        log.target_record_display_name = f"Record ID: {log.target_record_id} (Not Found/Deleted)"
                except KeyError: # Model not found
                    log.target_record_display_name = f"Model: {log.target_model_name}, ID: {log.target_record_id} (Model Not Found)"
                except Exception as e:
                    _logger.error(f"Error computing target display name for audit log {log.id}: {e}")
                    log.target_record_display_name = f"Record ID: {log.target_record_id} (Error)"