# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class InfluenceGenPlatformSetting(models.Model):
    _name = 'influence_gen.platform_setting'
    _description = "InfluenceGen Platform Setting"

    key = fields.Char(string="Setting Key", required=True, index=True, unique=True, copy=False)
    value_text = fields.Text(string="Setting Value")
    value_type = fields.Selection([
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'), # Stored as 'True'/'False' strings in value_text
        ('json', 'JSON')    # Stored as JSON string in value_text
    ], string="Value Type", required=True, default='string')
    description = fields.Text(string="Description")
    module = fields.Char(string="Module", help="Technical name of the Odoo module that defines or primarily uses this setting.")

    _sql_constraints = [
        ('key_uniq', 'unique(key)', 'Setting key must be unique!')
    ]
    
    @api.model
    def get_param(self, key: str, default=None):
        """
        Retrieves a setting value, casting it to its `value_type`.
        """
        setting = self.search([('key', '=', key)], limit=1)
        if not setting:
            return default
        
        value_str = setting.value_text
        value_type = setting.value_type

        if value_type == 'string':
            return value_str
        elif value_type == 'integer':
            try:
                return int(value_str)
            except (ValueError, TypeError):
                return default # Or raise error
        elif value_type == 'float':
            try:
                return float(value_str)
            except (ValueError, TypeError):
                return default # Or raise error
        elif value_type == 'boolean':
            return value_str == 'True' # Handles 'True', 'False', or other strings
        elif value_type == 'json':
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                return default # Or raise error
        return default # Should not happen if value_type is valid

    @api.model
    def set_param(self, key: str, value, value_type: str, description: str = None, module: str = None) -> models.Model:
        """
        Creates or updates a setting.
        """
        if value_type not in dict(self._fields['value_type'].selection):
            raise ValidationError(_("Invalid value_type: %s", value_type))

        setting = self.search([('key', '=', key)], limit=1)
        
        value_text_to_store = ""
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
        
        vals = {
            'key': key,
            'value_text': value_text_to_store,
            'value_type': value_type,
        }
        if description is not None: # Allow clearing description by passing empty string
            vals['description'] = description
        if module:
            vals['module'] = module

        if setting:
            old_value = setting.value_text
            setting.write(vals)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='PLATFORM_SETTING_UPDATED',
                actor_user_id=self.env.user.id,
                action_performed='UPDATE_SETTING',
                target_object=setting,
                details_dict={'key': key, 'old_value': old_value, 'new_value': value_text_to_store, 'type': value_type}
            )
        else:
            setting = self.create(vals)
            self.env['influence_gen.audit_log_entry'].create_log(
                event_type='PLATFORM_SETTING_CREATED',
                actor_user_id=self.env.user.id,
                action_performed='CREATE_SETTING',
                target_object=setting,
                details_dict={'key': key, 'value': value_text_to_store, 'type': value_type}
            )
        return setting

    # To ensure boolean values are stored consistently
    @api.onchange('value_type', 'value_text')
    def _onchange_value_text_for_boolean(self):
        if self.value_type == 'boolean':
            if self.value_text and self.value_text.lower() not in ['true', 'false', '1', '0', 'yes', 'no', '']:
                 raise UserError(_("For boolean type, please use 'True' or 'False'. Input will be standardized."))
            if self.value_text:
                 self.value_text = 'True' if self.value_text.lower() in ['true', '1', 'yes'] else 'False'

    def write(self, vals):
        # Ensure that if value_type is boolean, value_text is normalized
        if 'value_type' in vals and vals['value_type'] == 'boolean' and 'value_text' in vals and vals['value_text']:
            vals['value_text'] = 'True' if str(vals['value_text']).lower() in ['true', '1', 'yes'] else 'False'
        elif self.value_type == 'boolean' and 'value_text' in vals and vals['value_text']:
             vals['value_text'] = 'True' if str(vals['value_text']).lower() in ['true', '1', 'yes'] else 'False'
        return super(InfluenceGenPlatformSetting, self).write(vals)