# -*- coding: utf-8 -*-
import json
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class BaseAuditMixin(models.AbstractModel):
    """
    Base Audit Mixin for InfluenceGen Models.
    Provides base audit logging functionality for key Odoo models.
    It logs create, write, and unlink operations by creating entries
    in the 'influence_gen.audit_log' model.
    REQ-ATEL-005, REQ-ATEL-006
    """
    _name = 'influence_gen.base_audit_mixin'
    _description = 'Base Audit Mixin for InfluenceGen Models'

    def _log_audit_event(self, action, target_entity_name=None, target_id=None, details=None, outcome='success', reason=None):
        """
        Creates an 'influence_gen.audit_log' record.

        :param str action: The action being logged (e.g., 'create', 'write', 'unlink').
        :param str target_entity_name: Name of the target model if different from self._name.
        :param int target_id: ID of the target record if different from self.id.
        :param dict details: Dictionary of relevant details (e.g., changed fields, old/new values).
        :param str outcome: 'success' or 'failure'.
        :param str reason: Reason for failure, if any.
        """
        self.ensure_one() # Expects to be called on a single record context for self._name and self.id defaults
        audit_log_model = self.env['influence_gen.audit_log']

        log_vals = {
            'timestamp': fields.Datetime.now(),
            'user_id': self.env.user.id if self.env.user else None,
            'event_type': f"{target_entity_name or self._name}.{action}",
            'target_model': target_entity_name or self._name,
            'target_res_id': target_id or (self.id if self and self.exists() else None),
            'action': action,
            'details_json': json.dumps(details, default=str) if details else None,
            'ip_address': self.env.context.get('remote_addr') or \
                          (self.env.request.httprequest.remote_addr if self.env.request and hasattr(self.env.request, 'httprequest') else None),
            'outcome': outcome,
            'failure_reason': reason,
        }
        try:
            # Use sudo() to ensure audit logs are created even if the current user
            # doesn't have direct create permission on audit_log model,
            # assuming the audit system itself should always be able to write.
            audit_log_model.sudo().create(log_vals)
        except Exception as e:
            _logger.error("Failed to create audit log entry: %s. Values: %s", str(e), log_vals, exc_info=True)


    @api.model_create_multi
    def create(self, vals_list):
        """
        Overrides create to log the event.
        Calls super().create(vals_list). For each created record,
        calls _log_audit_event('create', details={'created_values': vals}).
        """
        records = super(BaseAuditMixin, self).create(vals_list)
        for i, record in enumerate(records):
            try:
                # vals_list[i] contains the original values used for creation
                record._log_audit_event(
                    action='create',
                    target_id=record.id,
                    details={'created_values': vals_list[i]}
                )
            except Exception as e:
                _logger.error("Audit log error during create for model %s, record ID %s: %s",
                              record._name, record.id, str(e), exc_info=True)
        return records

    def write(self, vals):
        """
        Overrides write to log the event.
        Captures old values for fields in vals. Calls super().write(vals).
        For each record in self, calls _log_audit_event('write',
        details={'updated_values': vals, 'old_values': captured_old_values}).
        """
        old_values_by_record = {}
        # Capture old values before the write operation
        # Only capture values for fields present in 'vals' and exist on the model
        # To ensure we are comparing apples to apples, fetch current values of fields being updated.
        if vals: # Proceed only if there are values to write
            for record in self:
                record_old_values = {}
                for field_name in vals.keys():
                    if hasattr(record, field_name) and field_name in record._fields:
                        current_value = record[field_name]
                        # For relational fields, log their current representation or ID
                        if isinstance(record._fields[field_name], (fields.Many2one, fields.Many2many, fields.One2many)):
                            if isinstance(current_value, models.BaseModel):
                                if record._fields[field_name].type == 'many2one':
                                    record_old_values[field_name] = current_value.id if current_value else False
                                else: # many2many, one2many
                                    record_old_values[field_name] = current_value.ids if current_value else []
                            else: # if it's already an ID or list of IDs
                                record_old_values[field_name] = current_value
                        else:
                            record_old_values[field_name] = current_value
                old_values_by_record[record.id] = record_old_values
        
        res = super(BaseAuditMixin, self).write(vals)

        if vals: # Log only if there were values to write
            for record in self:
                try:
                    details = {'updated_values': vals}
                    if record.id in old_values_by_record:
                        # Filter old_values to only include fields actually changed.
                        # A field is considered changed if its old value differs from its new value in 'vals'.
                        # However, 'vals' only contains the values *to be set*. The actual new value is now in record[field_name].
                        # So, old_values_by_record[record.id] is what we need.
                        details['old_values'] = old_values_by_record[record.id]
                    
                    record._log_audit_event(
                        action='write',
                        details=details
                    )
                except Exception as e:
                    _logger.error("Audit log error during write for model %s, record ID %s: %s",
                                  record._name, record.id, str(e), exc_info=True)
        return res

    def unlink(self):
        """
        Overrides unlink to log the event.
        For each record in self, captures identifying information.
        Calls _log_audit_event('unlink', details=captured_info).
        Then calls super().unlink().
        """
        records_to_log = []
        for record in self:
            records_to_log.append({
                'id': record.id,
                'display_name': record.display_name if hasattr(record, 'display_name') and record.display_name else str(record.id),
                'model_name': record._name
            })

        # Log before actual unlinking, as record data might not be accessible afterwards
        for record_data in records_to_log:
            try:
                # Create a temporary browse record context for logging if needed,
                # or ensure _log_audit_event can handle being called from a record about to be unlinked.
                # Calling it on 'self.browse(record_data['id'])' won't work once unlinked.
                # Here, we call it on the 'record' instance from the loop before super().unlink().
                # Find the original record in the recordset to call _log_audit_event method from it.
                # This ensures `self` in `_log_audit_event` is correctly set.
                original_record = self.filtered(lambda r: r.id == record_data['id'])
                if original_record: # Should always be true here
                    details = {
                        'unlinked_record_id': record_data['id'],
                        'unlinked_record_display_name': record_data['display_name']
                    }
                    original_record._log_audit_event(
                        action='unlink',
                        target_entity_name=record_data['model_name'],
                        target_id=record_data['id'],
                        details=details
                    )
            except Exception as e:
                _logger.error("Audit log error during pre-unlink for model %s, record ID %s: %s",
                              record_data['model_name'], record_data['id'], str(e), exc_info=True)

        res = super(BaseAuditMixin, self).unlink()
        return res