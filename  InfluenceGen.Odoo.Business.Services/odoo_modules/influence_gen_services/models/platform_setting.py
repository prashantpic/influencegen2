import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class InfluenceGenPlatformSetting(models.Model):
    _name = 'influence_gen.platform_setting'
    _description = "InfluenceGen Platform Setting"

    key = fields.Char(string="Setting Key", required=True, index=True, unique=True, copy=False)
    value_text = fields.Text(string="Setting Value")
    value_type = fields.Selection([
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON')
    ], string="Value Type", required=True, default='string')
    description = fields.Text(string="Description")
    module = fields.Char(string="Module", help="Technical name of the module that defines this setting.")

    _sql_constraints = [
        ('key_uniq', 'unique(key)', 'Setting key must be unique!')
    ]

    @api.model
    def get_param(cls, key, default=None):
        setting = cls.search([('key', '=', key)], limit=1)
        if not setting:
            return default
        
        value_text = setting.value_text
        value_type = setting.value_type

        try:
            if value_type == 'string':
                return value_text
            elif value_type == 'integer':
                return int(value_text) if value_text else default # Handle empty string for int
            elif value_type == 'float':
                return float(value_text) if value_text else default # Handle empty string for float
            elif value_type == 'boolean':
                # Consider 'false', '0', '' as False too
                return value_text.lower() in ('true', '1', 'yes') if value_text else False
            elif value_type == 'json':
                return json.loads(value_text) if value_text else default
            else:
                return value_text # Default to string if type unknown
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            #_logger.warning(f"Could not cast platform setting '{key}' with value '{value_text}' to type '{value_type}': {e}")
            return default

    @api.model
    def set_param(cls, key, value, value_type, description=None, module=None):
        if not key or not value_type:
            raise ValidationError(_("Key and Value Type are required to set a platform setting."))

        setting = cls.search([('key', '=', key)], limit=1)
        
        value_str = ""
        if value_type == 'json':
            try:
                value_str = json.dumps(value)
            except TypeError:
                raise ValidationError(_("Invalid JSON value for key '%s'.", key))
        elif value_type == 'boolean':
            value_str = 'True' if value else 'False'
        else:
            value_str = str(value)

        vals = {
            'key': key,
            'value_text': value_str,
            'value_type': value_type,
        }
        if description is not None: # Allow clearing description
            vals['description'] = description
        if module:
            vals['module'] = module

        old_value = None
        if setting:
            old_value = {
                'value_text': setting.value_text,
                'value_type': setting.value_type,
                'description': setting.description,
                'module': setting.module,
            }
            setting.write(vals)
        else:
            setting = cls.create(vals)

        cls.env['influence_gen.audit_log_entry'].create_log(
            event_type='PLATFORM_SETTING_CHANGED',
            actor_user_id=cls.env.user.id,
            action_performed='WRITE' if old_value else 'CREATE',
            target_object=setting,
            details_dict={
                'key': key,
                'new_value': vals,
                'old_value': old_value if old_value else "N/A"
            }
        )
        return setting