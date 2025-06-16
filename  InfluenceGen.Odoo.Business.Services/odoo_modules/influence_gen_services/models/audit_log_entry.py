# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _

class InfluenceGenAuditLogEntry(models.Model):
    _name = 'influence_gen.audit_log_entry'
    _description = "System Audit Log Entry"
    _order = 'timestamp desc'

    timestamp = fields.Datetime(
        string="Timestamp (UTC)",
        default=fields.Datetime.now,
        required=True,
        readonly=True,
        index=True
    )
    event_type = fields.Char(string="Event Type", required=True, index=True, readonly=True)
    actor_user_id = fields.Many2one(
        'res.users',
        string="Actor User",
        ondelete='set null', # Keep log even if user deleted
        readonly=True,
        index=True
    )
    actor_description = fields.Char(
        string="Actor Description", 
        compute='_compute_actor_description', 
        store=True, 
        readonly=True
    )
    target_model_name = fields.Char(string="Target Model", readonly=True, index=True)
    target_record_id = fields.Integer(string="Target Record ID", readonly=True, index=True)
    target_record_display_name = fields.Char(
        string="Target Record Name", 
        compute='_compute_target_display_name', 
        store=False, # Not stored to avoid issues with deleted records/performance
        readonly=True
    )
    action_performed = fields.Char(string="Action Performed", required=True, readonly=True)
    details_json = fields.Text(string="Details (JSON)", readonly=True)
    ip_address = fields.Char(string="Source IP Address", readonly=True)
    
    outcome = fields.Selection([
        ('success', 'Success'),
        ('failure', 'Failure')
        # Add 'info' or other relevant outcomes if needed
    ], string="Outcome", readonly=True, index=True)
    failure_reason = fields.Text(string="Failure Reason", readonly=True)

    @api.model
    def create_log(self, event_type: str, actor_user_id: int, action_performed: str,
                   target_object: models.Model = None, details_dict: dict = None,
                   ip_address: str = None, outcome: str = 'success', failure_reason: str = None) -> models.Model:
        """
        Central method to create audit log entries. REQ-ATEL-005, REQ-ATEL-006.
        """
        vals = {
            'event_type': event_type,
            'actor_user_id': actor_user_id,
            'action_performed': action_performed,
            'ip_address': ip_address or (self.env.context.get('request_ip') if hasattr(self.env, 'context') else None),
            'outcome': outcome,
            'failure_reason': failure_reason,
        }
        if target_object and isinstance(target_object, models.Model) and len(target_object) == 1: # Ensure it's a single record
            vals['target_model_name'] = target_object._name
            vals['target_record_id'] = target_object.id
            # Note: target_record_display_name is compute
        
        if details_dict:
            try:
                vals['details_json'] = json.dumps(details_dict, default=str) # Use default=str for non-serializable like datetime
            except TypeError:
                vals['details_json'] = json.dumps({'error': 'Failed to serialize details_dict'})

        return self.create(vals)

    @api.depends('actor_user_id', 'actor_user_id.name')
    def _compute_actor_description(self) -> None:
        for record in self:
            if record.actor_user_id:
                record.actor_description = record.actor_user_id.name
            else:
                # Could be "System Process" or derived from event_type/context
                record.actor_description = "System Process" 

    def _compute_target_display_name(self) -> None:
        """
        Computes the display name of the target record.
        This is non-stored and for display purposes.
        Handles potential errors if the target record is deleted.
        """
        for record in self:
            record.target_record_display_name = "" # Default
            if record.target_model_name and record.target_record_id:
                try:
                    if record.target_model_name in self.env:
                        target_model = self.env[record.target_model_name]
                        # Check if 'active' field exists for sudo access if record might be archived
                        if 'active' in target_model._fields:
                             target_rec = target_model.with_context(active_test=False).browse(record.target_record_id).exists()
                        else:
                             target_rec = target_model.browse(record.target_record_id).exists()

                        if target_rec:
                            record.target_record_display_name = target_rec.display_name
                        else:
                            record.target_record_display_name = _("[Record Deleted/Inaccessible]")
                    else:
                        record.target_record_display_name = _("[Model Not Found: %s]", record.target_model_name)
                except Exception:
                    # Catch broad exception as various ORM/access issues could occur
                    record.target_record_display_name = _("[Error Fetching Name]")