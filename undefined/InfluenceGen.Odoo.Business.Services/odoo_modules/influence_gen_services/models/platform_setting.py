# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class PlatformSetting(models.Model):
    """
    Platform Configuration Setting
    Stores configurable key-value settings for the InfluenceGen platform.
    This model provides a flexible way to store and manage various platform settings
    and business rule parameters that can be changed without code deployment.
    Changes to settings are audited via BaseAuditMixin.
    REQ-IOKYC-017 (provides mechanism for KYC settings)
    """
    _name = 'influence_gen.platform_setting'
    _description = 'Platform Configuration Setting'
    _inherit = ['influence_gen.base_audit_mixin']
    _order = 'module, key'

    key = fields.Char(
        string='Setting Key', 
        required=True, 
        index=True, 
        copy=False,
        help="Unique identifier for the setting, e.g., 'kyc.default_document_types', 'ai.quota.monthly_default'."
    )
    value_char = fields.Char(string='Character Value', help="Value if type is Character.")
    value_text = fields.Text(string='Text Value', help="Value if type is Text.")
    value_int = fields.Integer(string='Integer Value', help="Value if type is Integer.")
    value_float = fields.Float(string='Float Value', help="Value if type is Float.")
    value_bool = fields.Boolean(string='Boolean Value', help="Value if type is Boolean.")
    value_json = fields.Text(string='JSON Value', help="Value if type is JSON (stored as a string).")
    
    value_type = fields.Selection([
        ('char', 'Character'),
        ('text', 'Text'),
        ('int', 'Integer'),
        ('float', 'Float'),
        ('bool', 'Boolean'),
        ('json', 'JSON')
      ], 
      string='Value Type', 
      required=True, 
      default='char',
      help="Determines which 'value_*' field holds the actual setting value."
    )
    description = fields.Text(
        string='Description', 
        help="Explanation of the setting, its purpose, and potential impact of changing it."
    )
    module = fields.Char(
        string='Module', 
        index=True,
        help="Helps categorize the setting; indicates the Odoo module or platform area this setting primarily belongs to (e.g., 'influence_gen_services', 'kyc', 'ai_generation')."
    )
    active = fields.Boolean(default=True, help="If unchecked, this setting is ignored by get_setting method.")


    _sql_constraints = [
        ('key_unique', 'UNIQUE(key)', 'The setting key must be unique.')
    ]

    @api.constrains('value_type', 'value_char', 'value_text', 'value_int', 'value_float', 'value_bool', 'value_json')
    def _check_value_consistency(self):
        """Ensures only the correct value field is set based on value_type."""
        for setting in self:
            value_fields = {
                'char': setting.value_char, 'text': setting.value_text,
                'int': setting.value_int, 'float': setting.value_float,
                'bool': setting.value_bool, 'json': setting.value_json,
            }
            has_value = False
            for v_type, v_val in value_fields.items():
                if v_type == setting.value_type:
                    if v_val not in (None, False, 0, 0.0, ''): # Check if the primary field has a meaningful value
                        has_value = True
                    if v_type == 'json' and v_val:
                        try:
                            json.loads(v_val)
                        except json.JSONDecodeError:
                            raise ValidationError(_("Invalid JSON format for setting '%s'.") % setting.key)
                elif v_val not in (None, False, 0, 0.0, ''): # Check if other fields have meaningful values
                     # Allow bool to be False, int/float to be 0
                    if not (isinstance(v_val, bool) and v_val is False) and \
                       not (isinstance(v_val, (int, float)) and v_val == 0):
                        _logger.warning(
                            "Setting '%s' of type '%s' has a value in an alternate field 'value_%s': %s. "
                            "This might lead to confusion. Consider clearing it.",
                            setting.key, setting.value_type, v_type, v_val
                        )
            # A setting might legitimately have an empty/False/0 value. This check is more about data hygiene.
            # if not has_value and setting.value_type not in ['bool', 'int', 'float'] and any(v for v in value_fields.values()):
            #     _logger.info("Setting '%s' of type '%s' appears to have no value set in its designated field.", setting.key, setting.value_type)


    def _get_typed_value(self):
        """
        Returns the actual value from the correct value_* field based on value_type,
        performing necessary type conversions (e.g., JSON parsing).
        """
        self.ensure_one()
        if not self.active: # If setting is inactive, behave as if it's not found
            return None

        val_type = self.value_type
        if val_type == 'char':
            return self.value_char
        if val_type == 'text':
            return self.value_text
        if val_type == 'int':
            return self.value_int
        if val_type == 'float':
            return self.value_float
        if val_type == 'bool':
            return self.value_bool
        if val_type == 'json':
            if self.value_json:
                try:
                    return json.loads(self.value_json)
                except json.JSONDecodeError:
                    _logger.error("Invalid JSON content for setting key '%s': %s", self.key, self.value_json)
                    # Depending on strictness, either raise error or return None/default
                    raise UserError(_("Setting '%s' has invalid JSON content.") % self.key)
            return None # Or an empty dict/list as per convention
        return None # Should not happen if value_type is valid

    @api.model
    def get_setting(self, key_name, default=None, company_id=None):
        """
        Finds an active setting by key_name and returns its appropriately typed value.
        If not found or inactive, returns the provided default value.

        :param str key_name: The unique key of the setting.
        :param any default: The value to return if the setting is not found or inactive.
        :param int company_id: Optional company_id if settings can be company-specific (not implemented here).
        :return: Actual value (str, int, float, bool, dict/list from JSON) or default.
        """
        # Add domain for company_id if settings become company-specific
        domain = [('key', '=', key_name), ('active', '=', True)]
        # For now, company_id is not part of the model structure for uniqueness or retrieval.
        # If it were, domain would include ('company_id', '=', company_id) or similar logic.

        setting = self.search(domain, limit=1)
        if setting:
            try:
                return setting._get_typed_value()
            except UserError: # Catch specific errors like invalid JSON from _get_typed_value
                 _logger.warning("Error retrieving typed value for setting '%s', returning default.", key_name, exc_info=True)
                 return default
        return default

    @api.model
    def set_setting(self, key_name, value, value_type=None, description=None, module=None, company_id=None):
        """
        Creates or updates a setting.
        Determines value_type automatically if not provided (for basic Python types).
        Stores the value in the corresponding value_* field.

        :param str key_name: The unique key of the setting.
        :param any value: The value to set.
        :param str value_type: Optional. The type of the value ('char', 'text', 'int', 'float', 'bool', 'json').
        :param str description: Optional. Description for the setting if creating new.
        :param str module: Optional. Module associated with the setting if creating new.
        :param int company_id: Optional company_id (not currently used for differentiation).
        :return: recordset of the influence_gen.platform_setting
        """
        vals_to_write = {}

        if value_type is None:
            if isinstance(value, bool): value_type = 'bool'
            elif isinstance(value, int): value_type = 'int' # Catches bool as well, so bool must be first
            elif isinstance(value, float): value_type = 'float'
            elif isinstance(value, (dict, list)): value_type = 'json'
            elif isinstance(value, str):
                # Heuristic: if it looks like JSON, treat it as JSON if it parses.
                # Otherwise, text vs char based on length.
                try:
                    json.loads(value)
                    value_type = 'json'
                except json.JSONDecodeError:
                    if len(value) > 250: # Arbitrary length, Char default is 255 in DB usually
                        value_type = 'text'
                    else:
                        value_type = 'char'
            else:
                raise UserError(_("Could not automatically determine value type for setting '%s' with value of type %s. Please specify value_type.") % (key_name, type(value).__name__))
        
        vals_to_write['value_type'] = value_type

        if value_type == 'char': vals_to_write['value_char'] = str(value)
        elif value_type == 'text': vals_to_write['value_text'] = str(value)
        elif value_type == 'int': vals_to_write['value_int'] = int(value)
        elif value_type == 'float': vals_to_write['value_float'] = float(value)
        elif value_type == 'bool': vals_to_write['value_bool'] = bool(value)
        elif value_type == 'json':
            if isinstance(value, (dict, list)):
                vals_to_write['value_json'] = json.dumps(value, default=str)
            elif isinstance(value, str):
                 # Validate if it's a string representation of JSON
                try:
                    json.loads(value)
                    vals_to_write['value_json'] = value
                except json.JSONDecodeError:
                    raise UserError(_("Provided string value for JSON type setting '%s' is not valid JSON.") % key_name)
            else:
                raise UserError(_("Invalid value type for JSON setting '%s'. Expected dict, list, or valid JSON string.") % key_name)
        else:
            raise UserError(_("Unsupported value_type '%s' for setting '%s'.") % (value_type, key_name))

        # Clear other value fields to maintain data integrity
        all_value_field_names = ['value_char', 'value_text', 'value_int', 'value_float', 'value_bool', 'value_json']
        current_value_field_name = f'value_{value_type}'
        for field_name_to_clear in all_value_field_names:
            if field_name_to_clear != current_value_field_name:
                vals_to_write[field_name_to_clear] = False # Set to False or None based on field type defaults

        domain = [('key', '=', key_name)]
        # if company_id: domain.append(('company_id', '=', company_id)) # If company specific
        setting = self.search(domain, limit=1)

        if setting:
            if description is not None and setting.description != description : vals_to_write['description'] = description
            if module is not None and setting.module != module: vals_to_write['module'] = module
            setting.write(vals_to_write)
        else:
            vals_to_write['key'] = key_name
            if description is not None: vals_to_write['description'] = description
            if module is not None: vals_to_write['module'] = module
            # if company_id: vals_to_write['company_id'] = company_id # If company specific
            setting = self.create(vals_to_write)
        
        _logger.info("Platform setting '%s' %s with value_type '%s'.", 
                     key_name, "updated" if setting.id else "created", value_type)
        return setting

    @api.depends('key', 'value_type')
    def _compute_display_name(self):
        for record in self:
            value_preview = ""
            try:
                typed_val = record._get_typed_value()
                if isinstance(typed_val, (dict, list)):
                    value_preview = json.dumps(typed_val, default=str)
                else:
                    value_preview = str(typed_val)
                
                if len(value_preview) > 50:
                    value_preview = value_preview[:47] + "..."
            except Exception:
                value_preview = "[Error retrieving value]"

            record.display_name = f"{record.key} ({record.value_type}): {value_preview}"