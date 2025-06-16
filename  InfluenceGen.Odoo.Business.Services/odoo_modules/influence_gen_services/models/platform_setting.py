# -*- coding: utf-8 -*-
import json
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class InfluenceGenPlatformSetting(models.Model):
    _name = 'influence_gen.platform_setting'
    _description = "InfluenceGen Platform Setting"

    key = fields.Char(
        string="Setting Key", required=True, index=True,
        unique=True, copy=False
    )
    value_text = fields.Text(string="Setting Value")
    value_type = fields.Selection([
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON')
    ], string="Value Type", required=True, default='string')
    description = fields.Text(string="Description")
    module = fields.Char(
        string="Module",
        help="Technical name of the module that defines this setting."
    )

    @api.model
    def get_param(self, key, default=None):
        """Retrieves a setting value, casting it to its value_type."""
        setting = self.sudo().search([('key', '=', key)], limit=1)
        if not setting:
            return default
        
        value_text = setting.value_text
        value_type = setting.value_type

        try:
            if value_type == 'integer':
                return int(value_text)
            elif value_type == 'float':
                return float(value_text)
            elif value_type == 'boolean':
                return value_text.lower() in ('true', '1', 'yes')
            elif value_type == 'json':
                return json.loads(value_text)
            # Default is string
            return value_text
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            _logger.error(f"Error casting platform setting '{key}' to type '{value_type}': {e}. Returning default.")
            return default

    @api.model
    def set_param(self, key, value, value_type, description=None, module=None):
        """Creates or updates a setting."""
        if value_type not in ('string', 'integer', 'float', 'boolean', 'json'):
            raise ValidationError(_("Invalid value_type: %s", value_type))

        value_text = ""
        try:
            if value_type == 'json':
                value_text = json.dumps(value)
            elif value_type == 'boolean':
                value_text = 'True' if value else 'False'
            else:
                value_text = str(value)
        except (TypeError, json.JSONDecodeError) as e:
            raise ValidationError(_("Failed to serialize value for key '%s' to type '%s': %s", key, value_type, e))

        setting = self.sudo().search([('key', '=', key)], limit=1)
        vals = {
            'value_text': value_text,
            'value_type': value_type,
        }
        if description is not None: # Allow clearing description by passing empty string
            vals['description'] = description
        if module: # Typically set on creation
            vals['module'] = module

        if setting:
            old_value_text = setting.value_text
            old_value_type = setting.value_type
            setting.sudo().write(vals)
            details = {'old_value': old_value_text, 'old_type': old_value_type, 'new_value': value_text, 'new_type': value_type}
        else:
            vals['key'] = key
            setting = self.sudo().create(vals)
            details = {'new_value': value_text, 'new_type': value_type}
        
        # Log audit of setting change
        self.env['influence_gen.audit_log_entry'].create_log(
            event_type='PLATFORM_SETTING_CHANGED',
            actor_user_id=self.env.user.id if self.env.user else None, # Might be called by system
            action_performed='WRITE' if 'old_value' in details else 'CREATE',
            target_object=setting,
            details_dict=details
        )
        return setting
    
    # Ensure key is unique
    _sql_constraints = [
        ('key_uniq', 'unique (key)', 'Setting key must be unique!')
    ]