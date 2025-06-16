# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class InfluenceGenPlatformSetting(models.Model):
    _name = 'influence_gen.platform_setting'
    _description = "InfluenceGen Platform Setting"

    key = fields.Char(
        string="Setting Key",
        required=True,
        index=True,
        unique=True,
        copy=False,
        help="Unique identifier for the setting, e.g., 'influence_gen.default_tos_version'."
    )
    value_text = fields.Text(string="Setting Value", help="The actual value of the setting, stored as text.")
    value_type = fields.Selection([
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON')
    ], string="Value Type", required=True, default='string', help="The data type of the setting's value.")
    description = fields.Text(string="Description", help="Explanation of what this setting controls.")
    module = fields.Char(string="Module", help="Technical name of the module that defines or primarily uses this setting.")

    @api.model
    def get_param(cls, key, default=None):
        """Retrieves a setting value, casting it to its value_type."""
        setting = cls.search([('key', '=', key)], limit=1)
        if not setting:
            return default

        value_str = setting.value_text
        value_type = setting.value_type

        try:
            if value_type == 'string':
                return value_str
            elif value_type == 'integer':
                return int(value_str)
            elif value_type == 'float':
                return float(value_str)
            elif value_type == 'boolean':
                return value_str.lower() in ['true', '1', 'yes']
            elif value_type == 'json':
                return json.loads(value_str)
            else: # Should not happen if value_type is enforced
                return value_str # Fallback to string
        except (ValueError, TypeError, json.JSONDecodeError):
            # Log an error or warning if casting fails
            # For now, return default on casting error to prevent system failure
            _logger = cls.env['ir.logging']._logger # Get Odoo logger
            _logger.warning(f"Failed to cast platform setting '{key}' with value '{value_str}' to type '{value_type}'. Returning default.")
            return default

    @api.model
    def set_param(cls, key, value, value_type, description=None, module=None):
        """Creates or updates a setting. Value should be of the type specified by value_type."""
        if value_type not in dict(cls._fields['value_type'].selection):
            raise ValidationError(_("Invalid value_type: %s", value_type))

        value_text_to_store = ""
        try:
            if value_type == 'string':
                value_text_to_store = str(value)
            elif value_type == 'integer':
                value_text_to_store = str(int(value))
            elif value_type == 'float':
                value_text_to_store = str(float(value))
            elif value_type == 'boolean':
                value_text_to_store = 'True' if bool(value) else 'False'
            elif value_type == 'json':
                value_text_to_store = json.dumps(value)
        except (ValueError, TypeError):
            raise ValidationError(_("Invalid value for type %s: %s", value_type, value))

        setting = cls.search([('key', '=', key)], limit=1)
        vals = {
            'value_text': value_text_to_store,
            'value_type': value_type, # Ensure value_type is also updated if it changed
        }
        if description is not None: # Allow clearing description
            vals['description'] = description
        if module:
            vals['module'] = module
        
        old_value = None
        if setting:
            old_value = {'value_text': setting.value_text, 'value_type': setting.value_type}
            setting.write(vals)
        else:
            vals['key'] = key
            setting = cls.create(vals)
        
        # Log audit of setting change
        cls.env['influence_gen.audit_log_entry'].create_log(
            event_type='PLATFORM_SETTING_CHANGED',
            actor_user_id=cls.env.user.id,
            action_performed='WRITE' if old_value else 'CREATE',
            target_object=setting,
            details_dict={'key': key, 'old_value': old_value, 'new_value': {'value_text': value_text_to_store, 'value_type': value_type}}
        )
        return setting
    
    # Ensure there's a logger if used above
    # _logger = logging.getLogger(__name__) # This line should be at module level for standard Python logging
    # For Odoo, it's better to get it via self.env['ir.logging']._logger if inside a method
    # or just use api.Environment.cr.であろう logging if need be.
    # The example above uses self.env['ir.logging']._logger